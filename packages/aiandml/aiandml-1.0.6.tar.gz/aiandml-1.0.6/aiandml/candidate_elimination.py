from PIL import Image as Image1
from IPython.display import Image as Image2,display
import numpy as np
import pandas as pd

def learn(concept, target):
    specific_h = concepts[0].copy()
    generic_h = [['?' for i in range(len(specific_h))] for i in range(len(specific_h))]
    print(
        'Initialing specific_h and generic_h'
        '\nSpecific Boundaries :', specific_h,
        '\nGeneric Boundaries : ', generic_h
    )
    for i, h in enumerate(concept):
        print('\nInstance ',i+1,' is ',h)
        if target[i] == 'Yes':
            print('Instance is Positive')
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x], generic_h[x][x] = '?', '?'
        if target[i] == 'No':
            print('Instance is Negative')
            for x in range(len(specific_h)):
                generic_h[x][x] = specific_h[x] if h[x] != specific_h[x] else '?'
        print(
            'Specific Boundaries after ', i + 1, ' instances is ', specific_h,
            '\nGeneric Boundaries after ', i + 1, ' instances is ', generic_h
        )
    indices = ['?' for i, val in enumerate(generic_h) if val == ['?'] * 6]
    for i in indices:
        generic_h.remove(['?'] * 6)
    print(
        '\nFinal Specific_h : ', specific_h,
        '\nFinal Generic_h : ', generic_h
    )

def problem_statement():
    print('''
Problem Statement:
    For a given set of training data examples stored in a .CSV file, implement and demonstrate the Candidate-Elimination algorithm to output a description of the set of all hypotheses consistent with the training examples.
    ''')
def description():
    print('Description:\n\tCandidate-Elimination algorithm is used to find all the set of hypothesis consistent with the given data sample. It uses version spaces & considers both positive & negative results. Consider the dataset same as that of the Find-S algorithm for implementation.')
# def algorithm():
#     try:
#         display(Image2('candidate_elimination_algo.png'))
#     except:
#         Image1.open('candidate_elimination_algo.png').show()
def code():
    print('\nProgram for Candidate-Elimination algorithm')
    print(
        '''
import numpy as np
import pandas as pd
data = pd.read_csv('ws.csv', header=None)
concepts, target = np.array(data.iloc[:, 0:-1]), np.array(data.iloc[:, -1])
def learn(concept, target):
    specific_h = concepts[0].copy()
    generic_h = [['?' for i in range(len(specific_h))] for i in range(len(specific_h))]
    print(
        'Initialing specific_h and generic_h'
        '\\nSpecific Boundaries :', specific_h,
        '\\nGeneric Boundaries : ', generic_h
    )
    for i, h in enumerate(concept):
        print('\\nInstance ',i+1,' is ',h)
        if target[i] == 'Yes':
            print('Instance is Positive')
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x], generic_h[x][x] = '?', '?'
        if target[i] == 'No':
            print('Instance is Negative')
            for x in range(len(specific_h)):
                generic_h[x][x] = specific_h[x] if h[x] != specific_h[x] else '?'
        print(
            'Specific Boundaries after ', i + 1, ' instances is ', specific_h,
            '\\nGeneric Boundaries after ', i + 1, ' instances is ', generic_h
        )
    indices = ['?' for i, val in enumerate(generic_h) if val == ['?'] * 6]
    for i in indices:
        generic_h.remove(['?'] * 6)
    print(
        '\\nFinal Specific_h : ', specific_h,
        '\\nFinal Generic_h : ', generic_h
    )
if __name__ == '__main__':
    learn(concepts, target)
        '''
    )
def run(filename):
    data = pd.read_csv(filename, header=None)
    global concepts
    concepts, target = np.array(data.iloc[:, 0:-1]), np.array(data.iloc[:, -1])
    learn(concepts, target)