import math
import csv
from PIL import Image as Image1
from IPython.display import Image as Image2,display
def load_csv(filename):
    lines = csv.reader(open(filename,'r'))
    dataset = list(lines)
    header = dataset.pop(0)
    return dataset , header
class Node:
    def __init__(self,attribute):
        self.attribute = attribute
        self.children = []
        self.answer = ''
def subtables(data , col , delete):
    dic = {}
    coldata = [row[col] for row in data]
    attr = list(set(coldata))
    for k in attr:
        dic[k] = []
    for y in range(len(data)):
        key = data[y][col]
        if delete:
            del data[y][col]
        dic[key].append(data[y])
    return attr , dic

def entropy(S):
    attr = list(set(S))
    if len(attr) == 1:
        return 0
    counts = [0,0]
    for i in range(2):
        counts[i] = sum( [1 for x in S if attr[i] == x]) / (len(S) * 1.0)
    sums  = 0
    for cnt in counts:
        sums += -1 * cnt * math.log(cnt,2)
    return sums

def compute_gain(data , col):
    attrValues , dic = subtables(data ,col , delete= False)
    total_entropy = entropy([row[-1] for row in data])
    for x in range(len(attrValues)):
        ratio = len(dic[attrValues[x]]) / (len(data) * 1.0 )
        entro = entropy([row[-1] for row in dic[attrValues[x]]])
        total_entropy -= ratio*entro
    return total_entropy

def build_tree(data , features):
    lastcol = [row[-1] for row in data]
    if(len(set(lastcol))) == 1:
        node = Node("")
        node.answer = lastcol[0]
        return node
    n  = len(data[0]) -1
    gains = [compute_gain(data , col) for col in range(n)]
    split = gains.index(max(gains))
    node = Node(features[split])
    fea = features[:split] + features[split+1:]
    attr , dic = subtables(data , split , delete=True)
    for x in range(len(attr)):
        child = build_tree(dic[attr[x]],fea)
        node.children.append((attr[x],child))
    return node
def print_tree(node , level):
    if node.answer != "":
        print(' '*level,node.answer)
        return
    print(' '*(level+1),node.attribute)
    for value , n in node.children:
        print(' '*(level+1),value)
        print_tree(n , level + 2)
def classify(node , x_test , features):
    if node.answer != "":
        print(node.answer)
        return
    pos = features.index(node.attribute)
    for value , n in node.children:
        if x_test[pos] == value:
            classify(n ,x_test,features)
def problem_statement():
    print('''
Problem Statement:
    Write a program to demonstrate the working of decision tree based ID3 algorithm. Use an appropriate dataset to build the decision tree & apply 
    this knowledge to test the new sample.
    ''')
def description():
    print('Description:\n\tIterative Dichotomiser (ID3) Heuristic algorithm is used for building the decision tree. It considers the original set of attributes as the root node. On each iteration of the algorithm, we iterate through every unused attribute of the remaining set and calculates the entropy (or information gain) of that attribute. Then, we select the attribute which has the smallest entropy (or largest information gain) value. The set of remaining attributes is then split by the selected attribute to produce subsets of the data. The algorithm continues to recurse on each subset, considering only attributes never selected before. In testing phase at runtime, we will use trained decision tree to classify the new unseen test cases by working down the decision tree using the values of this test case to arrive at a terminal node that tells us what class this test case belongs to.')
def algorithm():
    try:
        display(Image2('id3.jpg'))
    except:
        Image1.open('id3.jpg').show()
def code():
    print('\nProgram for ID3 Algorithm: ')
    print('''
import math
import csv
def load_csv(filename):
    lines = csv.reader(open(filename,'r'))
    dataset = list(lines)
    header = dataset.pop(0)
    return dataset , header
class Node:
    def __init__(self,attribute):
        self.attribute = attribute
        self.children = []
        self.answer = ''
def subtables(data , col , delete):
    dic = {}
    coldata = [row[col] for row in data]
    attr = list(set(coldata))
    for k in attr:
        dic[k] = []
    for y in range(len(data)):
        key = data[y][col]
        if delete:
            del data[y][col]
        dic[key].append(data[y])
    return attr , dic

def entropy(S):
    attr = list(set(S))
    if len(attr) == 1:
        return 0
    counts = [0,0]
    for i in range(2):
        counts[i] = sum( [1 for x in S if attr[i] == x]) / (len(S) * 1.0)
    sums  = 0
    for cnt in counts:
        sums += -1 * cnt * math.log(cnt,2)
    return sums

def compute_gain(data , col):
    attrValues , dic = subtables(data ,col , delete= False)
    total_entropy = entropy([row[-1] for row in data])
    for x in range(len(attrValues)):
        ratio = len(dic[attrValues[x]]) / (len(data) * 1.0 )
        entro = entropy([row[-1] for row in dic[attrValues[x]]])
        total_entropy -= ratio*entro
    return total_entropy

def build_tree(data , features):
    lastcol = [row[-1] for row in data]
    if(len(set(lastcol))) == 1:
        node = Node("")
        node.answer = lastcol[0]
        return node
    n  = len(data[0]) -1
    gains = [compute_gain(data , col) for col in range(n)]
    split = gains.index(max(gains))
    node = Node(features[split])
    fea = features[:split] + features[split+1:]
    attr , dic = subtables(data , split , delete=True)
    for x in range(len(attr)):
        child = build_tree(dic[attr[x]],fea)
        node.children.append((attr[x],child))
    return node
def print_tree(node , level):
    if node.answer != "":
        print(' '*level,node.answer)
        return
    print(' '*(level+1),node.attribute)
    for value , n in node.children:
        print(' '*(level+1),value)
        print_tree(n , level + 2)
def classify(node , x_test , features):
    if node.answer != "":
        print(node.answer)
        return
    pos = features.index(node.attribute)
    for value , n in node.children:
        if x_test[pos] == value:
            classify(n ,x_test,features)
dataset , features = load_csv('data3.csv')
node = build_tree(dataset,features)
print('The decision tree for the dataset using ID3 Algorithm is :')
print_tree(node , 0)
testdata ,features = load_csv('data3_test.csv')
for xtest in testdata:
    print('The test instance :',xtest)
    print('The predicted label : ',end='')
    classify(node,xtest,features)
''')
def run(train_file , test_file):
    dataset, features = load_csv(train_file)
    node = build_tree(dataset, features)
    print('The decision tree for the dataset using ID3 Algorithm is :')
    print_tree(node, 0)
    testdata, features = load_csv(test_file)
    for xtest in testdata:
        print('The test instance :', xtest)
        print('The predicted label : ', end='')
        classify(node, xtest, features)



# if __name__ == '__main__':
#     problem_statement()
#     code()

