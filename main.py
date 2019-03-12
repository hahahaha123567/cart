import numpy as np
import pandas as pd


class Node:
    def __init__(self, attribute=None, key=None, left=None, right=None, result=None):
        self.attribute = attribute  # 非叶节点用来划分的属性
        self.key = key  # 非叶节点用来划分属性的值
        self.left = left  # 非叶节点的左子树
        self.right = right  # 非叶节点的右子树
        self.result = result  # 叶节点的结果

    def __repr__(self):
        return str(self.__dict__)



def read_file(filename):
    file = pd.ExcelFile(filename)
    df_string = file.parse(0)
    data_set = np.array(df_string).tolist()  # type: list
    attributes = data_set[0]
    data_set = data_set[1:]
    # ST1 -> ST, 正常1 -> 正常
    for data in data_set:
        if data[0].startswith('ST'):
            data[0] = 'ST'
        else:
            data[0] = '正常'
    return attributes, data_set


def split_data_set(attributes, data_set, attribute, key):
    attribute_index = attributes.index(attribute)
    left_data_set, right_data_set = [], []
    for data in data_set:
        target_data_set = left_data_set if data[attribute_index] > key else right_data_set
        target_data_set.append(data)
    return left_data_set, right_data_set


def create_tree(attributes, data_set):
    result_list = list(map(lambda x: x[0], data_set))

    # 如果数据集只剩一种类型, 返回该类型
    if len(result_list) == 1:
        return Node(result=result_list.pop())

    # 如果遍历完所有特征，返回数据集中最多的类型
    if len(attributes) == 0:
        return Node(result='ST' if result_list.count('ST') > result_list.count('正常') else '正常')

    # 计算用来划分的属性和值
    cut_attribute, cut_value = calcu_cut_value(attributes, data_set)
    left_data_set, right_data_set = split_data_set(attributes, data_set, cut_attribute, cut_value)
    # 将划分过的属性置空
    attributes = attributes.copy()
    attributes[attributes.index(cut_attribute)] = None
    left_node = create_tree(attributes, left_data_set)
    right_node = create_tree(attributes, right_data_set)
    return Node(cut_attribute, cut_value, left_node, right_node)


def calcu_cut_value(attributes, data_set):
    final_max_gini = -1
    final_cut_attribute = -1
    final_cut_value = -1
    # 对每个属性计算gini值
    for attribute in attributes[1:]:
        attri_max_gini = -1
        attri_cut_value = -1
        # 如果该属性为空(已经划分过即置空)则跳过
        if attributes is None:
            continue
        # 本次循环中取data的第index个属性
        index = attributes.index(attribute)
        data_set.sort(key=(lambda x: x[index]))
        for i in range(len(data_set) - 1):
            # 本次循环中以第i个data和第i+1个data的平均值为分界
            cut_value = (data_set[i][index] + data_set[i + 1][index]) / 2
            #         <=   >
            # ST      a    c
            # normal  b    d
            a, b, c, d = 0, 0, 0, 0
            for t in range(len(data_set)):
                if data_set[t][index] <= cut_value:
                    if 'ST' == data_set[t][0]:
                        a += 1
                    elif '正常' == data_set[t][0]:
                        b += 1
                else:
                    if 'ST' == data_set[t][0]:
                        c += 1
                    elif '正常' == data_set[t][0]:
                        d += 1
            gini1 = 1 - (a * a + b * b) / ((a + b) * (a + b))
            gini2 = 1 - (c * c + d * d) / ((c + d) * (c + d))
            gini = gini1 * (a + b) / (a + b + c + d) + gini2 * (c + d) / (a + b + c + d)
            if gini > attri_max_gini:
                attri_max_gini = gini
                attri_cut_value = cut_value
        if attri_max_gini > final_max_gini:
            final_max_gini = attri_max_gini
            final_cut_attribute = attribute
            final_cut_value = attri_cut_value
    return final_cut_attribute, final_cut_value


if __name__ == "__main__":
    attributes, data_set = read_file('data.xls')

    tree = create_tree(attributes, data_set)
    print(tree.__repr__())
