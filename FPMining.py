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


def calculate_support(dataset, candidate, min_sup):
    """
    计算数据集中候选项集的支持度。
    """
    count = 0
    for transaction in dataset:
        if set(candidate).issubset(set(transaction)):
            count += 1
    support = count / len(dataset)
    return support


def Apriori(dataset, min_sup):
    """
    频繁项集挖掘的Apriori算法。
    """
    # 初始化频繁项集列表
    frequent_itemsets = []

    # Get unique items
    unique_items = set(item for transaction in dataset for item in transaction)

    # 生成长度为1的频繁项集
    candidates = [(item,) for item in unique_items]
    frequent_itemsets.extend(
        [list(candidate) for candidate in candidates if calculate_support(dataset, candidate, min_sup) >= min_sup])

    # 生成长度> 1的频繁项集
    k = 2
    while True:
        new_candidates = generate_candidates(frequent_itemsets, k)
        frequent_candidates = [candidate for candidate in new_candidates if
                               calculate_support(dataset, candidate, min_sup) >= min_sup]
        if not frequent_candidates:
            break
        frequent_itemsets.extend(frequent_candidates)
        k += 1

    return frequent_itemsets


# FP-growth
class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None


def build_FP_tree(dataset, min_sup):
    # Count item occurrences in dataset
    item_counts = {}
    for transaction in dataset:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1

    # Filter items below min_sup
    frequent_items = {item: count for item, count in item_counts.items() if count >= min_sup}
    frequent_items = sorted(frequent_items.items(), key=lambda x: (-x[1], x[0]))

    # Build FP tree
    root = FPNode(None, None, None)
    header_table = {}

    for transaction in dataset:
        ordered_items = [item for item in transaction if item in frequent_items]
        if len(ordered_items) > 0:
            insert_tree(ordered_items, root, header_table)

    return root, header_table


def insert_tree(items, node, header_table):
    if items[0] in node.children:
        node.children[items[0]].count += 1
    else:
        node.children[items[0]] = FPNode(items[0], 1, node)
        if header_table.get(items[0]) is None:
            header_table[items[0]] = node.children[items[0]]
        else:
            update_header(header_table[items[0]], node.children[items[0]])

    if len(items) > 1:
        insert_tree(items[1:], node.children[items[0]], header_table)


def update_header(node_to_test, target_node):
    while node_to_test.next is not None:
        node_to_test = node_to_test.next
    node_to_test.next = target_node


def ascend_FP_tree(node, prefix_path):
    if node.parent is not None:
        prefix_path.append(node.item)
        ascend_FP_tree(node.parent, prefix_path)


def mine_FP_tree(header_table, min_sup):
    frequent_patterns = []
    for item in header_table:
        prefix_path = []
        ascend_FP_tree(header_table[item], prefix_path)
        if len(prefix_path) > 1:
            frequent_patterns.append(prefix_path)
    return frequent_patterns


def FPGrowth(dataset, min_sup):
    root, header_table = build_FP_tree(dataset, min_sup)
    frequent_patterns = mine_FP_tree(header_table, min_sup)
    return frequent_patterns


# ECLAT
def eclat(prefix, items, min_sup, frequent_itemsets):
    while items:
        item, item_count = items.pop()
        new_prefix = prefix + [item]
        support = calculate_support(dataset, new_prefix, min_sup)
        if support >= min_sup:
            frequent_itemsets.append(new_prefix)
            suffix = []
            for next_item, next_item_count in items:
                new_itemset = new_prefix + [next_item]
                next_support = calculate_support(dataset, new_itemset, min_sup)
                if next_support >= min_sup:
                    suffix.append((next_item, next_item_count))
            eclat(new_prefix, sorted(suffix, key=lambda x: (-x[1], x[0])), min_sup, frequent_itemsets)


def ECLAT(dataset, min_sup):
    unique_items = {}
    for transaction in dataset:
        for item in transaction:
            unique_items[item] = unique_items.get(item, 0) + 1
    sorted_items = sorted(unique_items.items(), key=lambda x: (-x[1], x[0]))
    frequent_itemsets = []
    eclat([], sorted_items, min_sup, frequent_itemsets)
    return frequent_itemsets


if __name__ == '__main__':
    dataset = read_dataset("DBLPdata-10k.txt")
    # 设置最小支持度
    min_sup = 5

    # 使用Apriori算法挖掘频繁项集
    # print("A:")
    # apriori_result = Apriori(dataset, min_sup)
    # print("Apriori算法挖掘的频繁项集结果：", apriori_result)

    # print("B:")
    # FPNode_result = FPGrowth(dataset, min_sup)
    # print("FP-Growth算法结果：",FPNode_result)

    print("C:")
    ECLAT_result = ECLAT(dataset, min_sup)
    print(ECLAT_result)
