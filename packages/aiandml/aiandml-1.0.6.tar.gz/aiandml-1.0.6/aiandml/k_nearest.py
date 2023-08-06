from PIL import Image as Image1
from IPython.display import Image as Image2,display
def problem_statement():
    print('''
Problem Statement:
    Write a program to implement k-Nearest Neighbour algorithm to classify the iris data set. Print both correct and wrong predictions. Java/Python ML library classes can be used for this problem.
    ''')
def description():
    print('Description:\n\tThe most basic instance-based method is the k-NEAREST NEIGHBOR algorithm. This algorithm assumes all instances correspond to points in the n- dimensional space Rn. The nearest neighbors of an instance are defined in terms of the standard Euclidean distance. In nearest-neighbor learning the target function may be either discrete-valued or real-valued.Let us first consider learning discrete-valued target functions of the form f: Rn→V, where V is the finite set {vl, . . . vs}.')
def algorithm():
    print('''The k-NEAREST NEIGHBOR algorithm is easily adapted to approximating continuous-valued target functions.''')
    try:
        display(Image2('k_nearest.png'))
    except:
        Image1.open('k_nearest.png').show()
def code():
    print('\nProgram for K-Nearest Neighbors Algorithm: ')
    print('''
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
iris = datasets.load_iris()
print('Iris Data Set Loaded...')
x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size= 0.1)
print(
        'Dataset is split into training and testing...'
        '\\nSize of training data and its label ', x_train.shape, y_train.shape,
        '\\nSize of testing data and its label ', x_test.shape, y_test.shape
    )
for i in range(len(iris.target_names)):
    print('Label', i, '-', iris.target_names[i])

classifier = KNeighborsClassifier(n_neighbors=1)
classifier.fit(x_train, y_train)
y_prediction = classifier.predict(x_test)
print('Result of Classification using K-n with K=1')
for r in range(len(x_test)):
    print('Sample: ', x_test[r],
              'Actual-label: ', y_test[r],
              'Predicted-label: ', y_prediction[r]
              )
print('Classification Accuracy : ', classifier.score(x_test, y_test))
''')
def run():
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn import datasets
    iris = datasets.load_iris()
    iris = datasets.load_iris()
    print('Iris Data Set Loaded...')
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.1)
    print(
        'Dataset is split into training and testing...'
        '\nSize of training data and its label ', x_train.shape, y_train.shape,
        '\nSize of testing data and its label ', x_test.shape, y_test.shape
    )
    for i in range(len(iris.target_names)):
        print('Label', i, '-', iris.target_names[i])

    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(x_train, y_train)
    y_prediction = classifier.predict(x_test)
    print('Result of Classification using K-n with K=1')
    for r in range(len(x_test)):
        print('Sample: ', x_test[r],
              'Actual-label: ', y_test[r],
              'Predicted-label: ', y_prediction[r]
              )
    print('Classification Accuracy : ', classifier.score(x_test, y_test))

# if __name__ == '__main__':
#     run()