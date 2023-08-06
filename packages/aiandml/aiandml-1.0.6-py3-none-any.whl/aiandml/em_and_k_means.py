import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from PIL import Image as Image1
from IPython.display import Image as Image2,display
def problem_statement():
    print('''
Problem Statement: 
    Apply EM algorithm to cluster a set of data stored in a .CSV file. Use the same data set for clustering using k-Means algorithm.Compare the results of these two algorithms and comment on the quality of clustering. You can add Java/Python ML library classes/API in the program.''')
def description():
    print('Description:\n\tEM algorithm is a widely used approach to learning in the presence of unobserved variables. The EM algorithm can be used even for variables whose value is never directly observed, provided the general form of the probability distribution governing these variables is known. The EM algorithm has been used to train Bayesian belief networks as well as radial basis function networks. The EM algorithm is also the basis for many unsupervised clustering algorithms and it is the basis for the widely used Baum-Welch forward-backward algorithm for learning Partially Observable Markov Models.')
def algorithm():
    try:
        display(Image2('em_and_k_means.png'))
    except:
        Image1.open('em_and_k_means.png').show()
def code():
    print('Program for comparing EM and KMeans Clustering algorithms: ')
    print('''
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

iris = datasets.load_iris()
X = pd.DataFrame(iris.data)
X.columns = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
y = pd.DataFrame(iris.target)
y.columns = ['Targets']

model = KMeans(n_clusters=3)
model.fit(X)

plt.figure(figsize=(14,14))
colorMap = np.array(['red','lime','black'])
plt.subplot(2,2,1)
plt.scatter(X.Petal_Length , X.Petal_Width , c = colorMap[y.Targets],s = 40)
plt.title('Real Clusters')
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')

plt.subplot(2,2,2)
plt.scatter(X.Petal_Length , X.Petal_Width , c = colorMap[model.labels_],s = 40)
plt.title('K-Means Clustering')
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')

from sklearn import preprocessing as pp
scaler = pp.StandardScaler()
scaler.fit(X)
xsa = scaler.transform(X)
xs = pd.DataFrame(xsa , columns=X.columns)

from sklearn.mixture import GaussianMixture as gm
gmm = gm(n_components=3)
gmm.fit(xs)
gmm_y = gmm.predict(xs)
plt.subplot(2,2,3)
plt.scatter(X.Petal_Length,X.Petal_Width,c= colorMap[gmm_y],s=40)
plt.title('GM Clustering')
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.show()
print(\'''
Observation:
    The GMM using EM based Algorithm clustering matched the labels more closely than the KMeans.
    \''')
    ''')
def run():
    iris = datasets.load_iris()
    X = pd.DataFrame(iris.data)
    X.columns = ['Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width']
    y = pd.DataFrame(iris.target)
    y.columns = ['Targets']

    model = KMeans(n_clusters=3)
    model.fit(X)

    plt.figure(figsize=(14, 14))
    colorMap = np.array(['red', 'lime', 'black'])
    plt.subplot(2, 2, 1)
    plt.scatter(X.Petal_Length, X.Petal_Width, c=colorMap[y.Targets], s=40)
    plt.title('Real Clusters')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')

    plt.subplot(2, 2, 2)
    plt.scatter(X.Petal_Length, X.Petal_Width, c=colorMap[model.labels_], s=40)
    plt.title('K-Means Clustering')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')

    from sklearn import preprocessing as pp
    scaler = pp.StandardScaler()
    scaler.fit(X)
    xsa = scaler.transform(X)
    xs = pd.DataFrame(xsa, columns=X.columns)

    from sklearn.mixture import GaussianMixture as gm
    gmm = gm(n_components=3)
    gmm.fit(xs)
    gmm_y = gmm.predict(xs)
    plt.subplot(2, 2, 3)
    plt.scatter(X.Petal_Length, X.Petal_Width, c=colorMap[gmm_y], s=40)
    plt.title('GM Clustering')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')
    plt.show()
    print('''
Observation:
    The GMM using EM based Algorithm clustering matched the labels more closely than the KMeans.
        ''')


# if __name__ == '__main__':
#     run()