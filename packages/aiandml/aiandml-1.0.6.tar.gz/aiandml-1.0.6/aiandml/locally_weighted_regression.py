import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image as Image1
from IPython.display import Image as Image2,display
def kernel(point, xmat, k , x):
    m, n = np.shape(xmat)
    weights = np.mat(np.eye((m)))
    for j in range(m):
        diff = point - x[j]
        weights[j, j] = np.exp(diff * diff.T / (-2.0 * k ** 2))
    return weights


def LocalWeight(point, xmat, ymat, k , x):
    wei = kernel(point, xmat, k , x)
    w = (x.T * (wei * x)).I * (x.T * (wei * ymat.T))
    return w


def localWeightRegression(xmat, ymat, k , x):
    m, n = np.shape(xmat)
    ypred = np.zeros(m)
    for i in range(m):
        ypred[i] = xmat[i] * LocalWeight(xmat[i], xmat, ymat, k , x)
    return ypred
def graphPlot(x, ypred,bill,tip):
    sortindex = x[:, 1].argsort(0)
    xsort = x[sortindex][:, 0]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(bill, tip, color='green')
    ax.plot(xsort[:, 1], ypred[sortindex], color='red', linewidth=5)
    plt.xlabel('Total Bill')
    plt.ylabel('Tip')
    plt.show()

def problem_statement():
    print('''
Problem Statement: 
    Implement the non-parametric Locally Weighted Regression algorithm in order to fit data points. 
    Select appropriate data set for your experiment and draw graphs.''')
def description():
    print('Description:\n\tLocally weighted regression is a generalization of k-nearest neighbour approach. It constructs an explicit approximation to f over a local region surrounding xq. Locally weighted regression uses nearby or distance-weighted training examples to form this local approximation to f. For example, we might approximate the target function in the neighborhood surrounding xq. Using a linear function, a quadratic function, a multilayer neural network, or some other functional form. The phrase “locally weighted regression” is called local because the function is approximated based only on data near the query point, weighted because the contribution of each training example is weighted by its distance from the query point, and regression because this is the term used widely in the statistical learning community for the problem of approximating real-valued functions.')
def algorithm():
    try:
        display(Image2('locally_weighted_regression.png'))
    except:
        Image1.open('locally_weighted_regression.png').show()
def code():
    print('\nProgram for Locally Weighted Regression: ')
    print('''
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def kernel(point,xmat,k):
    m,n=np.shape(xmat)
    weights=np.mat(np.eye((m)))
    for j in range(m):
        diff=point-x[j]
        weights[j,j]=np.exp(diff*diff.T/(-2.0*k**2))
    return weights

def LocalWeight(point,xmat,ymat,k):
    wei=kernel(point,xmat,k)
    w=(x.T*(wei*x)).I*(x.T*(wei*ymat.T))
    return w

def localWeightRegression(xmat,ymat,k):
    m,n=np.shape(xmat)
    ypred=np.zeros(m)
    for i in range(m):
        ypred[i]=xmat[i]*LocalWeight(xmat[i],xmat,ymat,k)
    return ypred

def graphPlot(x,ypred):
    sortindex=x[:,1].argsort(0)
    xsort=x[sortindex][:,0]
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.scatter(bill,tip,color='green')
    ax.plot(xsort[:,1],ypred[sortindex],color='red',linewidth=5)
    plt.xlabel('Total Bill')
    plt.ylabel('Tip')
    plt.show()
    
data=pd.read_csv('Tips.csv')
bill=np.array(data.total_bill)
tip=np.array(data.tip)
mbill=np.mat(bill)
mtip=np.mat(tip)
m=np.shape(mbill)[1]
one=np.mat(np.ones(m))
x=np.hstack((one.T,mbill.T))
ypred=localWeightRegression(x,mtip,0.5)
graphPlot(x,ypred)
    ''')
def run(path):
    data = pd.read_csv(path)
    bill = np.array(data.total_bill)
    tip = np.array(data.tip)
    mbill = np.mat(bill)
    mtip = np.mat(tip)
    m = np.shape(mbill)[1]
    one = np.mat(np.ones(m))
    x = np.hstack((one.T, mbill.T))
    ypred = localWeightRegression(x, mtip, 0.5 , x)
    graphPlot(x, ypred,bill,tip)
