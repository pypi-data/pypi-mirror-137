from PIL import Image as Image1
from IPython.display import Image as Image2,display
def problem_statement():
    print('''
Problem Statement: 
    Write a program to implement the naïve Bayesian classifier for a sample training data set stored 
    as a .CSV file. Compute the accuracy of the classifier, considering few test data sets.''')
def description():
    print('Description:\n\tNaive Bayes classification algorithm can be extremely fast relative to other classification algorithms. It works on Bayes theorem of probability to predict the class of unknown data set. In simple terms, a Naive Bayes classifier assumes that the presence of a particular feature in a class is unrelated to the presence of any other feature. For example, a fruit may be considered to be an apple if it is red, round, and about 3 inches in diameter. Even if these features depend on each other or upon the existence of the other features, all of these properties independently contribute to the probability that this fruit is an apple and that is  why it is known as ‘Naive’. Naive Bayes model is easy to build and particularly useful for very large data sets.')
def algorithm():
    print('Algorithm:')
    try:
        display(Image2('naive_bayesian_classifier.png'))
    except:
        Image1.open('naive_bayesian_classifier.png').show()
def code():
    print('\nProgram for Naive Bayesian Classifier :')
    print('''
import statistics as st, csv ,random ,math , stat
def loadcsv(filename):
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset
def splitDataset(dataset, splitRatio):
    trainSize = int(len(dataset) * splitRatio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy)) # random index
        trainSet.append(copy.pop(index))
    return [trainSet, copy]
def separateByClass(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated
def summarize(dataset):
    summaries = [(st.mean(attribute), st.stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries
def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries
def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
#3.2 Calculate Class Probabilities
def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities
def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel
def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions
#5. Computing Accuracy
def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0
if __name__ == '__main__':
    filename = 'pima-indians-diabetes.csv'
    splitRatio = 0.67
    dataset = loadcsv(filename)
    print("The length of the Data Set : ",len(dataset))

    print("The Data Set Splitting into Training and Testing \\n")
    trainingSet, testSet = splitDataset(dataset, splitRatio)

    print('Number of Rows in Training Set:{0} rows'.format(len(trainingSet)))
    print('Number of Rows in Testing Set:{0} rows'.format(len(testSet)))

    print("\\nFirst Five Rows of Training Set:")
    for i in range(0,5):
        print(trainingSet[i],"\\n")
    print("\\nFirst Five Rows of Testing Set:")
    for i in range(0,5):
        print(testSet[i],"\\n")
 # prepare model
    summaries = summarizeByClass(trainingSet)
    predictions = getPredictions(summaries, testSet)
    accuracy = getAccuracy(testSet, predictions)
    print('\\n Accuracy: {0}%'.format(accuracy))
''')
import statistics as st, csv ,random ,math , stat
def loadcsv(filename):
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset
def splitDataset(dataset, splitRatio):
    trainSize = int(len(dataset) * splitRatio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy)) # random index
        trainSet.append(copy.pop(index))
    return [trainSet, copy]
def separateByClass(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated
def summarize(dataset):
    summaries = [(st.mean(attribute), st.stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries
def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries
def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
#3.2 Calculate Class Probabilities
def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities
def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel
def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions
def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0
def run(filename):
    splitRatio = 0.67
    dataset = loadcsv(filename)
    print("The length of the Data Set : ",len(dataset))

    print("The Data Set Splitting into Training and Testing \n")
    trainingSet, testSet = splitDataset(dataset, splitRatio)

    print('Number of Rows in Training Set:{0} rows'.format(len(trainingSet)))
    print('Number of Rows in Testing Set:{0} rows'.format(len(testSet)))

    print("\nFirst Five Rows of Training Set:")
    for i in range(0,5):
        print(trainingSet[i],"\n")
    print("\nFirst Five Rows of Testing Set:")
    for i in range(0,5):
        print(testSet[i],"\n")
    summaries = summarizeByClass(trainingSet)
    predictions = getPredictions(summaries, testSet)
    accuracy = getAccuracy(testSet, predictions)
    print('\nAccuracy: {0}%'.format(accuracy))
# run()