import itertools
from itertools import combinations


# Apriori算法

def generate_candidates(frequent_candidates_k1):
    """
    根据频繁项集 L(k-1) 生成候选项集 C(k)。

    参数:
        frequent_itemsets_k1 (list): 频繁项集 L(k-1) 的列表，每个项集用元组表示。

    返回:
        list: 候选项集 C(k) 的列表，每个项集用元组表示。
    """
    # 连接步：将 L(k-1) 中的频繁项集两两连接生成候选项集 C(k)
    Ck = set()
    for i in range(len(frequent_candidates_k1)):
        for j in range(i + 1, len(frequent_candidates_k1)):
            # 两个项集的前 k-2 项相同时才进行连接
            if frequent_candidates_k1[i][:-1] == frequent_candidates_k1[j][:-1] and frequent_candidates_k1[i][-1] < \
                    frequent_candidates_k1[j][-1]:
                new_itemset = frequent_candidates_k1[i] + (frequent_candidates_k1[j][-1],)
                Ck.add(new_itemset)
    Ck = sorted(Ck)

    # 剪枝步：剔除候选项集中非频繁的项集
    Lk = []
    for Ck_item_set in Ck:
        # 检查候选项集的所有子集是否都在 L(k-1) 中
        is_valid = True
        for subset in combinations(Ck_item_set, len(Ck_item_set) - 1):
            if subset not in frequent_candidates_k1:
                is_valid = False
                break
        if is_valid:
            Lk.append(Ck_item_set)

    return list(Lk)


def calculate_support(dataset1, candidate):
    """
    计算数据集中候选项集的支持度。“出现个数”
    candidate 是 元组
    """
    count = 0
    for transaction in dataset1:
        if all(elem in transaction for elem in candidate):
            count += 1
    support = count
    return support


def Apriori(data_set, min_sup_):
    """
    频繁项集挖掘的Apriori算法。
    """
    # 初始化频繁项集列表
    frequent_item_sets = []  # 这是结果

    # k = 1
    # 包含所有数据集中所有的项，不重复
    unique_items = set(item for transaction in data_set for item in transaction)

    # 生成长度为1的频繁项集
    # 每个候选项都是一个包含单个项的元
    k1_candidates = [item for item in unique_items]
    # 对于每个候选项集 candidate，如果其支持度不低于最小支持度阈值 min_sup_
    for candidate in k1_candidates:
        # 计算候选项集 candidate 在数据集中的支持度
        support = calculate_support(data_set, (candidate,))
        # 如果支持度满足最小支持度阈值，则将该候选项集添加到频繁项集列表中
        if support >= min_sup_:
            # 将候选项集转换为列表形式，并添加到频繁项集列表中
            frequent_item_sets.append([candidate])

    # 生成长度> 1的频繁项集
    k = 2
    frequent_candidates = sorted(frequent_item_sets)
    frequent_candidates = [tuple(sublist) for sublist in frequent_candidates]
    while True:
        new_candidates = generate_candidates(frequent_candidates)
        # 计算每个候选项集的支持度，并筛选出频繁项集
        frequent_candidates = []
        for candidate in new_candidates:
            # 计算候选项集的支持度
            support = calculate_support(data_set, candidate)
            # 如果支持度满足最小支持度阈值，则将其添加到频繁项集列表中
            if support >= min_sup_:
                frequent_candidates.append(candidate)

        if not frequent_candidates:
            break
        frequent_item_sets.extend(frequent_candidates)
        k += 1

    sorted_output = sorted(frequent_item_sets, key=lambda x: (len(x), x))
    return sorted_output


# FP-growth
class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None


def build_FP_tree(dataset, min_sup):
    """
    构造FP树
    :param dataset: 数据集
    :param min_sup:
    :return:
    """

    # Count item occurrences in dataset
    item_counts = {}
    for transaction in dataset:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1

    # 过滤出不符合要求的项，按频率逆序排列，得到L
    L = {item: count for item, count in item_counts.items()}
    L = sorted(L.items(), key=lambda x: (-x[1], x[0]))

    # 初始化一个root和项头表
    root = FPNode(None, None, None)
    header_table = {}
    # 对每一个事务
    for transaction in dataset:
        # 如果事务的每个项都在L里
        ordered_items = [item[0] for item in L if item[0] in transaction]
        if len(ordered_items) > 0:
            # 执行 插入事务到树里
            insert_tree(ordered_items, root, header_table)

    return root, header_table


def insert_tree(items, node, header_table):
    """
    执行 插入事务的一个项到树里
    :param items:  事务，一条记录
    :param node: 事务插到node下
    :param header_table:  项头表
    :return:
    """
    # p = item[0]
    if items[0] in node.children:
        # node有孩子是第一项，就count++,
        node.children[items[0]].count += 1
    else:
        # 第一项不是node孩子的话，就创建一个node的孩子节点，计数设为1，父节点为node
        node.children[items[0]] = FPNode(items[0], 1, node)
        # 更新项头表
        if header_table.get(items[0]) is None:
            # 如果项头表里面还没有这个p,就创建
            header_table[items[0]] = node.children[items[0]]
        else:
            # 如果项头表里已经有了p，就更新项头表
            update_header(header_table[items[0]], node.children[items[0]])
    # 如果这条事务还没结束，就继续insert项
    if len(items) > 1:
        insert_tree(items[1:], node.children[items[0]], header_table)


def update_header(node_to_test, target_node):
    """
    更新项头表，前面是项头表 此项现在的表头，后面是要加进来的
    :param node_to_test:
    :param target_node:
    :return:
    """
    while node_to_test.next is not None:
        node_to_test = node_to_test.next
    node_to_test.next = target_node


def mine_FP_tree(header_table, min_sup, L):
    all_combinations = set()
    # 将L中次数大于等于min_sup的项加入到all_combinations集合中
    for item, count in L:
        if count >= min_sup:
            all_combinations.add((item,))
    # 如果Tree包含一条path
    # 如果不是,L里的进行反遍历
    for item in L[::-1]:
        # 项id
        item_id = item[0]
        # 寻找条件模式基
        Conditional_pattern_base = {}
        node_condition = header_table[item_id]
        while node_condition is not None:
            # 遍历项头表,对于树上每一个项的节点
            leave_count = node_condition.count  # 叶子结点的计数
            temp_node = node_condition  # 这条路径上的节点
            p_path = []
            while temp_node.parent.item is not None:
                parent_item = temp_node.parent.item
                p_path.append(parent_item)
                temp_node = temp_node.parent
            # Conditional_pattern_base.append({p_path,leave_count})
            Conditional_pattern_base[(tuple)(p_path)] = leave_count

            node_condition = node_condition.next
        # 得到条件基之后，选出大于等于min_sup节点
        # 路径反向，得到从root开始的path
        Conditional_pattern_base = {tuple(reversed(key)): value for key, value in Conditional_pattern_base.items()}
        # 对于前缀相同的，加到一起
        Conditional_pattern_base_dataset = []
        # 遍历条件模式基
        for pattern, count in Conditional_pattern_base.items():
            # 将项集按照次数重复，然后添加到结果列表中
            Conditional_pattern_base_dataset.extend([list(pattern)] * count)

        # 得到了事务，创建新树
        root_condition, header_table_condition = build_FP_tree(Conditional_pattern_base_dataset, min_sup)
        #
        for node_condition in header_table_condition.items():
            current_node = node_condition[1]
            while current_node is not None:
                if current_node.count >= min_sup:
                    temp_current_node = current_node
                    # 当前节点的条件计数满足最小支持度
                    # 对路径上的节点进行操作
                    path_nodes = []
                    while temp_current_node is not None and temp_current_node.item is not None:
                        path_nodes.append(temp_current_node.item)
                        temp_current_node = temp_current_node.parent
                    # 从 path_nodes 中提取非空值并与其对应的 item_id 进行组合
                    path_nodes.append(item_id)
                    # 生成所有可能的组合

                    for r in range(1, len(path_nodes) + 1):
                        combinations_r = set(itertools.combinations(path_nodes, r))
                        combinations_r = [tuple(sorted(comb)) for comb in combinations_r]
                        all_combinations.update(combinations_r)
                current_node = current_node.next


    return all_combinations


def FPGrowth(dataset, min_sup):
    # Count item occurrences in dataset
    item_counts = {}
    for transaction in dataset:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1

    # 过滤出不符合要求的项，按频率逆序排列，得到L
    L = {item: count for item, count in item_counts.items()}
    L = sorted(L.items(), key=lambda x: (-x[1], x[0]))

    root, header_table = build_FP_tree(dataset, min_sup)
    frequent_patterns = mine_FP_tree(header_table, min_sup, L)

    frequent_patterns = sorted(frequent_patterns, key=lambda x: (len(x),x ))
    # 将元组转换为列表，并放入一个列表中
    frequent_patterns = [[item for item in pattern] for pattern in frequent_patterns]
    return frequent_patterns


# ECLAT
def eclat(prefix, items, min_support, freq_items):
    '''
    递归方式遍历数据集，找出频繁项集
    :param prefix:当前的前缀
    :param items:数据集中的项集
    :param min_support:
    :param freq_items:频繁项集的字典
    :return:
    '''
    while items:
        # 初始遍历单个的元素是否是频繁
        key, item = items.pop()
        key_support = len(item)
        if key_support >= min_support:
            # print frozenset(sorted(prefix+[key]))
            freq_items[frozenset(sorted(prefix+[key]))] = key_support
            suffix = []  # 存储当前长度的项集
            for other_key, other_item in items:
                new_item = item & other_item  # 求和其他集合求交集
                if len(new_item) >= min_support:
                    suffix.append((other_key, new_item))
            eclat(prefix+[key], sorted(suffix, key=lambda item: len(item[1]), reverse=True), min_support, freq_items)
    return freq_items


def ECLAT(data_set, min_sup):
    """
    Eclat方法:将数据集进行倒排，即将每个项映射到包含该项的事务编号的集合中。然后调用 eclat 函数来找出频繁项集
    :param data_set:
    :param min_sup:
    :return:
    """
    # 将数据倒排
    data = {}
    trans_num = 0
    for trans in data_set:
        trans_num += 1
        for item in trans:
            if item not in data:
                data[item] = set()
            data[item].add(trans_num)
    freq_items = {}
    freq_items = eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True), min_sup, freq_items)
    freq_itemsets = [list(item) for item in freq_items.keys()]
    freq_itemsets =  sorted(freq_itemsets, key=lambda x: (len(x), x))
    return freq_itemsets

# 读入文件
def read_dataset(file_path):
    """
    读入数据
    :param file_path: 数据文件路径
    :return:  返回数据集
    """
    dataSet = []
    with open(file_path, 'r') as file:
        for line in file:
            transaction = line.strip().split(',')
            dataSet.append(transaction)
    return dataSet

if __name__ == '__main__':
    dataset = read_dataset("DBLPdata-10k.txt")

    # 设置最小支持度，现指出现次数
    min_sup = 5

    # 使用Apriori算法挖掘频繁项集
    print("A:")
    apriori_result = Apriori(dataset, min_sup)
    print("Apriori算法挖掘的频繁项集结果：", apriori_result)

    print("B:")
    FPGrowth_result = FPGrowth(dataset, min_sup)
    print("FPGrowth算法挖掘的频繁项集结果：", FPGrowth_result)

    print("C:")
    ECLAT_result = ECLAT(dataset, min_sup)
    print("ECLAT算法挖掘的频繁项集结果：", ECLAT_result)
