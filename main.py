import sys
from sample import Sample

def calcuGini(samples, i):
    return 0.5

if __name__ == "__main__":
    # input
    samples = []
    with open('input', 'r') as f:
        inputs = f.read().splitlines()
        for input in inputs:
            s = input.split(' ')
            samples.append(Sample(s[0], s[1], s[2], s[3]))
    attributeUsed = [False, False, False]
    # select attribute
    for j in range(len(attributeUsed)):
        maxIndex = -1
        maxGini = 0
        for i in range(len(attributeUsed)):
            if not attributeUsed[i]:
                gini = calcuGini(samples, i)
                if gini > maxGini:
                    maxIndex = i
                    maxGini = gini
        attributeUsed[maxIndex] = True
