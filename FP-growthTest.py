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


if __name__ == '__main__':
    dataset = read_dataset("DBLPdata-10k.txt")

    # 设置最小支持度，现指出现次数
    min_sup = 5

    # 使用Apriori算法挖掘频繁项集
    print("B:")
    FPGrowth_result = FPGrowth(dataset, min_sup)
    sorted_FPGrowth_result = sorted(FPGrowth_result, key=lambda x: x[0])
    print("FPGrowth算法挖掘的频繁项集结果：", sorted_FPGrowth_result)
