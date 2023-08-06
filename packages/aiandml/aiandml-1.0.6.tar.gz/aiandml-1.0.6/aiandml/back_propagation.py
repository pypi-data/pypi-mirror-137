from PIL import Image as Image1
from IPython.display import Image as Image2,display
import numpy as np
def sigmoid(x):
    return 1/(1+np.exp(-x))
def sigmoid_grad(x):
    return x*(1-x)
def problem_statement():
    print(
        '''
Problem Statement: 
    Build an Artificial Neural Network by implementing the Back propagation algorithm and test the same using appropriate data sets.     
        '''
    )
def description():
    print(
'Description:\n\tThe BACKPROPAGATION algorithm learns the weights for a multilayer network, given a network with a fixed set of units and interconnections. It employs gradient descent to attempt to minimize the squared error between the network output values and the target values for these outputs. The learning problem faced by BACKPROPAGATION algorithm is to search a large hypothesis space defined by all possible weight values for all the units in the network.'
    )
def algorithm():
    print('The BACKPROPAGATION algorithm is discussed below:')
    try:
        display(Image2('back_propagation2.jpg'))
        display(Image2('back_propagation.png'))
    except:
        Image1.open('back_propagation2.jpg').show()
        Image1.open('back_propagation.png').show()
def code():
    print('\nProgram for Back Propagation Algorithm: ')
    print('''
import numpy as np
X=np.array(([2,9],[1,5],[3,6]),dtype=float)
Y=np.array(([92],[86],[89]),dtype=float)
X=X/np.amax(X,axis=0)
Y=Y/100

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_grad(x):
    return x*(1-x)
epoch=1000
eta=0.2
input_neutrons=2
hidden_neutrons=3
output_neutrons=1
wh=np.random.uniform(size=(input_neutrons,hidden_neutrons))
bh=np.random.uniform(size=(1,hidden_neutrons))
wout=np.random.uniform(size=(hidden_neutrons,output_neutrons))
bout=np.random.uniform(size=(1,output_neutrons))

for i in range(epoch):
    h_ip=np.dot(X,wh)+bh
    h_act=sigmoid(h_ip)
    o_ip=np.dot(h_act,wout)
    output=sigmoid(o_ip)
    Eo=Y-output
    outgrad=sigmoid_grad(output)
    d_output=Eo*outgrad
    Eh=d_output.dot(wout.T)
    hiddengrad=sigmoid_grad(h_act)
    d_hidden=Eh*hiddengrad
    wout +=h_act.T.dot(d_output)*eta
    wh +=X.T.dot(d_hidden)*eta
print("Normalized input:\\n"+str(X))
print("Actual output:\\n"+str(Y))
print("Predicted  output:\\n",output)
    ''')
def run():
    X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
    Y = np.array(([92], [86], [89]), dtype=float)
    X = X / np.amax(X, axis=0)
    Y = Y / 100
    epoch = 1000
    eta = 0.2
    input_neutrons = 2
    hidden_neutrons = 3
    output_neutrons = 1
    wh = np.random.uniform(size=(input_neutrons, hidden_neutrons))
    bh = np.random.uniform(size=(1, hidden_neutrons))
    wout = np.random.uniform(size=(hidden_neutrons, output_neutrons))
    bout = np.random.uniform(size=(1, output_neutrons))

    for i in range(epoch):
        h_ip = np.dot(X, wh) + bh
        h_act = sigmoid(h_ip)
        o_ip = np.dot(h_act, wout)
        output = sigmoid(o_ip)
        Eo = Y - output
        outgrad = sigmoid_grad(output)
        d_output = Eo * outgrad
        Eh = d_output.dot(wout.T)
        hiddengrad = sigmoid_grad(h_act)
        d_hidden = Eh * hiddengrad
        wout += h_act.T.dot(d_output) * eta
        wh += X.T.dot(d_hidden) * eta
    print("Normalized input:\n" + str(X))
    print("Actual output:\n" + str(Y))
    print("Predicted  output:\n", output)

# if __name__ == '__main__':
#     run()