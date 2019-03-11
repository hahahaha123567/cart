import numpy as np
import pandas as pd

FLAG = 65535


class Node:
    def __init__(self, attribute=None, key=None, left=None, right=None):
        self.attribute = attribute
        self.key = key
        self.left = left
        self.right = right


def read_file():
    file = pd.ExcelFile("data.xls")
    df_string = file.parse(0)
    return np.array(df_string).tolist()


def create_tree(self, data_set, classes, feat_names):
    """ 根据当前数据集递归创建决策树

    :param self:
    :param data_set: 数据集
    :param feat_names: 数据集中数据相应的特征名称
    :param classes: 数据集中数据相应的类型

    """
    # 如果数据集中只有一种类型停止树分裂
    if len(set(classes)) == 1:
        return classes[0]

    # 如果遍历完所有特征，返回比例最多的类型
    if len(feat_names) == 0:
        return get_majority(classes)

    # 分裂创建新的子树
    tree = {}
    best_feat_idx = self.choose_best_split_feature(data_set, classes)
    feature = feat_names[best_feat_idx]
    tree[feature] = {}

    # 创建用于递归创建子树的子数据集
    sub_feat_names = feat_names[:]
    sub_feat_names.pop(best_feat_idx)

    splited_dict = self.split_dataset(data_set, classes, best_feat_idx)
    for feat_val, (sub_dataset, sub_classes) in splited_dict.items():
        tree[feature][feat_val] = self.create_tree(sub_dataset,
                                                   sub_classes,
                                                   sub_feat_names)
    self.tree = tree
    self.feat_names = feat_names

    return tree


def cut(df):
    row_num = df.shape[0]
    column_num = df.shape[1]
    giniList = [0]
    cutList = [0]
    for column_index in range(column_num - 1)[1:]:
        column = df.iloc[:, column_index][1:]
        result = df.iloc[:, 0][1:]
        gini, cut = calcuCutValue(column, result)
        giniList.append(gini)
        cutList.append(cut)
    maxGini = max(giniList)
    index = giniList.index(maxGini)
    finalCutValue = cutList[index]
    if finalCutValue != FLAG:
        return Node(index, finalCutValue, cut(), cut())
    else:
        return Node()


def calcuCutValue(seriesWithoutSort, result):
    seriesSorted = copy.deepcopy(seriesWithoutSort)
    maxGini = 0
    finalCutValue = FLAG
    for i in range(len(seriesSorted))[1:]:
        cutValue = (seriesSorted[i] + seriesSorted[i + 1]) / 2
        #         <=   >
        # ST      a    c
        # normal  b    d
        a, b, c, d = 0, 0, 0, 0
        for t in range(len(seriesSorted - 1))[1:]:
            if seriesSorted[t] <= cutValue:
                if 'ST' in result[t]:
                    a += 1
                elif '正常' in result[t]:
                    b += 1
            else:
                if 'ST' in result[t]:
                    c += 1
                elif '正常' in result[t]:
                    d += 1
        gini1 = 1 - (a * a + b * b) / ((a + b) * (a + b))
        gini2 = 1 - (c * c + d * d) / ((c + d) * (c + d))
        gini = gini1 * (a + b) / (a + b + c + d) + gini2 * (c + d) / (a + b + c + d)
        if gini > maxGini:
            maxGini = gini
            finalCutValue = cutValue
    return finalCutValue


if __name__ == "__main__":
    data = read_file()

    for l in data:
        print(l)

    # root = cut(df)
