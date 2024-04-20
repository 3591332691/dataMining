import itertools


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


if __name__ == '__main__':
    dataset = [["I1", "I2", "I5"], ["I2", "I4"], ["I2", "I3"], ["I1", "I2", "I4"], ["I1", "I3"], ["I2", "I3"],
               ["I1", "I3"], ["I1", "I2", "I3", "I5"], ["I1", "I2", "I3"]]

    # 设置最小支持度，现指出现次数
    min_sup = 2

    # 使用Apriori算法挖掘频繁项集
    print("B:")
    FPGrowth_result = FPGrowth(dataset, min_sup)
    print("FPGrowth算法挖掘的频繁项集结果：", FPGrowth_result)
