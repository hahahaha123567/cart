import pandas as pd
import copy

FLAG = 65535

class Node:
    def __init__(self, sample=None, attribute=None, key=None, left=None, right=None):
        self.sample = sample
        self.attribute = attribute
        self.key = key
        self.left = left
        self.right = right

def input():
    file = pd.ExcelFile("data.xls")
    df = file.parse(0)
    return df.convert_objects(convert_numeric=True)

def cut(df):
    row_num = df.shape[0]
    column_num = df.shape[1]
    giniList = [0]
    cutList = [0]
    for column_index in range(column_num-1)[1:]:
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
        cutValue = (seriesSorted[i] + seriesSorted[i+1]) / 2
        #         <=   >
        # ST      a    c
        # normal  b    d
        a, b, c, d = 0, 0, 0, 0
        for t in range(len(seriesSorted-1))[1:]:
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
    df = input()
    # print(df.to_string())
    
    root = cut(df)
