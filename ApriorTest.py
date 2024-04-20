from itertools import combinations


# Apriori算法
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


if __name__ == '__main__':
    dataset = read_dataset("DBLPdata-10k.txt")

    # 设置最小支持度，现指出现次数
    min_sup = 5

    # 使用Apriori算法挖掘频繁项集
    print("A:")
    apriori_result = Apriori(dataset, min_sup)
    print("Apriori算法挖掘的频繁项集结果：", apriori_result)

