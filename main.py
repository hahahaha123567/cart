def input():
    data = []
    with open('input', 'r') as f:
        inputs = f.read().splitlines()
        for input in inputs:
            data.append(input.split(' '))
    return data

def calcuGini(data, i):
    attriValue = []
    for index in data:
        attriValue.append(data[index][i])
    
    return 0.5

def selectAttri(data, used):
    for j in range(len(used)):
        maxIndex = -1
        maxGini = 0
        for i in range(len(used)):
            if not used[i]:
                gini = calcuGini(data, i)
                if gini > maxGini:
                    maxIndex = i
                    maxGini = gini
        used[maxIndex] = True
    return 1

if __name__ == "__main__":
    data = input()

    used = [False] * len(data[0] - 1)

    for info in data:
        print(info)
    print(used)
    
    while False in used:
        attriIndex = selectAttri(data, used)
