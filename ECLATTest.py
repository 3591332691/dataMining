import sys
import time
type = sys.getfilesystemencoding()


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

if __name__ == '__main__':
    # 示例用法
    dataset = [
        ["I1", "I2", "I5"], ["I2", "I4"], ["I2", "I3"], ["I1", "I2", "I4"], ["I1", "I3"], ["I2", "I3"],
        ["I1", "I3"], ["I1", "I2", "I3", "I5"], ["I1", "I2", "I3"]
    ]

    min_sup = 2
    print("C:")
    result = ECLAT(dataset, min_sup)
    print("eclat算法挖掘的频繁项集结果：", result)
    print("done")
