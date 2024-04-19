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


def generate_candidates(transaction, length):
    """
    从事务生成长度为length的候选项集。
    """
    if length == 1:
        return [(item,) for item in transaction]
    else:
        candidates = []
        for i in range(len(transaction)):
            prefix = transaction[i]
            suffix = transaction[i + 1:]
            for item in generate_candidates(suffix, length - 1):
                candidates.append((prefix,) + item)
        return candidates


def calculate_support(dataset1, candidate):
    """
    计算数据集中候选项集的支持度。“出现个数”
    """
    count = 0
    # 把candidate全部设定为元组下包含的列表
    candidate_flat = [item for sublist in candidate for item in sublist]
    for transaction in dataset1:
        if all(elem in transaction for elem in candidate_flat):
            count += 1
    support = count
    return support


def Apriori(data_set, min_sup_):
    """
    频繁项集挖掘的Apriori算法。
    """
    # 初始化频繁项集列表
    frequent_itemsets = []

    # 包含所有数据集中所有的项，不重复
    unique_items = set(item for transaction in data_set for item in transaction)

    # 生成长度为1的频繁项集
    # 每个候选项都是一个包含单个项的元
    candidates = [([item],) for item in unique_items]
    # 对于每个候选项集 candidate，如果其支持度不低于最小支持度阈值 min_sup_
    for candidate in candidates:
        # 计算候选项集 candidate 在数据集中的支持度
        support = calculate_support(data_set, candidate)
        # 如果支持度满足最小支持度阈值，则将该候选项集添加到频繁项集列表中
        if support >= min_sup_:
            # 将候选项集转换为列表形式，并添加到频繁项集列表中
            frequent_itemsets.append(list(candidate))

    frequent_itemsets_k1 = frequent_itemsets

    # 生成长度> 1的频繁项集
    k = 2
    while True:
        print("k = ", k)
        new_candidates = generate_candidates(frequent_itemsets_k1, k)
        # 计算每个候选项集的支持度，并筛选出频繁项集
        frequent_candidates = []
        for candidate in new_candidates:
            # 计算候选项集的支持度
            support = calculate_support(data_set, candidate)
            # 如果支持度满足最小支持度阈值，则将其添加到频繁项集列表中
            if support >= min_sup_:
                print(candidate)
                frequent_candidates.append(candidate)

        if not frequent_candidates:
            break

        frequent_itemsets.extend(frequent_candidates)
        k += 1

    return frequent_itemsets


if __name__ == '__main__':
    dataset = read_dataset("DBLPdata-10k.txt")

    # 设置最小支持度，现指出现次数
    min_sup = 5

    # 使用Apriori算法挖掘频繁项集
    print("A:")
    apriori_result = Apriori(dataset, min_sup)
    sorted_apriori_result = sorted(apriori_result, key=lambda x: x[0])
    print("Apriori算法挖掘的频繁项集结果：", sorted_apriori_result)
