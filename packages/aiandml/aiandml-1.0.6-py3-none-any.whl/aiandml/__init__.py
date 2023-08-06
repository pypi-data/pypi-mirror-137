from aiandml import ao_star,a_star , k_nearest , locally_weighted_regression ,candidate_elimination , id3 , back_propagation ,em_and_k_means, naive_bayesian_classifier
import urllib.request
from PIL import Image
from IPython.display import display
def insertImage(url):
    try:
        urllib.request.urlretrieve(
            url,
            "gfg.jpg")
        img = Image.open("gfg.jpg")
        display(img)
    except Exception:
        print(Exception, 'PLEASE CONNECT TO INTERNET AND TRY TO RERUN')
class aStar:
    def __init__(self , tree, heuristic, start_node, end_node):
        self.tree , self.heuristic , self.start_node , self.end_node =tree , heuristic , start_node , end_node
    def problem_statement(self):
        a_star.problem_statement()
    def description(self):
        a_star.description()
    def algorithm(self):
        a_star.algorithm()
    def code(self):
        a_star.code()
    def run(self):
        print(f'''
Visited Nodes and Optimal Nodes Sequence for tree = {self.tree} 
                                             heuristic = {self.heuristic}
                                             start_node = {self.start_node}
                                             end_node = {self.end_node} ''')
        cost = {self.start_node: 0}
        visited_nodes , optimal_sequence = a_star.astar(self.start_node, self.end_node, self.tree, self.heuristic, cost)
        print(f"Visited Nodes : {visited_nodes} \nOptimal Nodes Sequence : {optimal_sequence}")
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()

class aoStar:
    def __init__(self , graph, heuristicNodeList, startNode):
        self.graph , self.heuristicNodeList , self.startNode = graph, heuristicNodeList, startNode
    def problem_statement(self):
        ao_star.problem_statement()
    def description(self):
        ao_star.description()
    def algorithm(self):
        ao_star.algorithm()
    def code(self):
        ao_star.code()
    def run(self):
        print(f'''
Output of AO* algorithm of
    graph = {self.graph} 
    heuristicNodeList = {self.heuristicNodeList}
    startNode = {self.startNode}
                                                     ''')
        G1 = ao_star.Graph(self.graph, self.heuristicNodeList, self.startNode)
        G1.applyAOstar()
        G1.printSolution()
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
class candidateElimination:
    def __init__(self , dataset_path):
        self.dataset_path = dataset_path
    def problem_statement(self):
        candidate_elimination.problem_statement()
    def description(self):
        candidate_elimination.description()
    def algorithm(self):
        insertImage('https://user-images.githubusercontent.com/67971078/152000935-3ad58667-584b-4f2e-a3ae-23beecec2d83.png')
    def code(self):
        candidate_elimination.code()
    def run(self):
        candidate_elimination.run(self.dataset_path)
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
class id_3:
    def __init__(self , train_dataset_path , test_dataset_path):
        self.train_dataset_path , self.test_dataset_path = train_dataset_path , test_dataset_path
    def problem_statement(self):
        id3.problem_statement()
    def description(self):
        id3.description()
    def algorithm(self):
        insertImage('https://user-images.githubusercontent.com/67971078/152000986-c41a480c-f27e-4ec7-805f-c078a8da8b1b.jpg')
    def code(self):
        id3.code()
    def run(self):
        id3.run(self.train_dataset_path , self.test_dataset_path)
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
class backPropagation:
    def problem_statement(self):
        back_propagation.problem_statement()
    def description(self):
        back_propagation.description()
    def algorithm(self):
        insertImage('https://user-images.githubusercontent.com/67971078/152000889-ec987289-9b9e-478e-bd0f-b30cf7f5088d.jpg')
        insertImage('https://user-images.githubusercontent.com/67971078/152000840-dd7933ea-aab1-4c5e-abb2-6317f6606c4d.png')
    def code(self):
        back_propagation.code()
    def run(self):
        back_propagation.run()
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
class naiveBayesianClassifier:
    def __init__(self , dataset_path):
        self.dataset_path = dataset_path
    def problem_statement(self):
        naive_bayesian_classifier.problem_statement()
    def description(self):
        naive_bayesian_classifier.description()
    def algorithm(self):
        insertImage('https://user-images.githubusercontent.com/67971078/152001033-d507f8df-470c-4893-a895-19e72d3cd92a.png')
    def code(self):
        naive_bayesian_classifier.code()
    def run(self):
        naive_bayesian_classifier.run(self.dataset_path)
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
class emAndKMeans:
    # No external Dataset
    def problem_statement(self):
        em_and_k_means.problem_statement()
    def description(self):
        em_and_k_means.description()
    def algorithm(self):
        insertImage('https://user-images.githubusercontent.com/67971078/152000963-dbad1286-14a7-4fec-80b5-b46f4c34e2a1.png')
    def code(self):
        em_and_k_means.code()
    def run(self):
        em_and_k_means.run()
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
class kNearestNeighbour:
    # No external Dataset
    def problem_statement(self):
        k_nearest.problem_statement()
    def description(self):
        k_nearest.description()
    def algorithm(self):
        print('''The k-NEAREST NEIGHBOR algorithm is easily adapted to approximating continuous-valued target functions.''')
        insertImage('https://user-images.githubusercontent.com/67971078/152000997-35a963aa-3e56-4e70-a816-96d33b9e019c.png')
    def code(self):
        k_nearest.code()
    def run(self):
        k_nearest.run()
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
class locallyWeightedRegression:
    def __init__(self , dataset_path):
        self.dataset_path = dataset_path
    def problem_statement(self):
        locally_weighted_regression.problem_statement()
    def description(self):
        locally_weighted_regression.description()
    def algorithm(self):
        insertImage('https://user-images.githubusercontent.com/67971078/152001014-dc006daa-6c7a-4fef-a3dd-605e65d4b9d4.png')
    def code(self):
        locally_weighted_regression.code()
    def run(self):
        locally_weighted_regression.run(self.dataset_path)
    def all(self):
        self.problem_statement()
        self.description()
        self.algorithm()
        self.code()
        self.run()
# path = "D:/Documents/Documents/Downloads/ML-CSV/ML-CSV/pima-indians-diabetes.csv"
# naiveBayesianClassifier(path).all()
# naiveBayesianClassifier(path).description()
# path1 = "D:/Documents/Documents/Downloads/ML-CSV/ML-CSV/data3.csv"
# path2 = "D:/Documents/Documents/Downloads/ML-CSV/ML-CSV/data3_test.csv"
# id_3(path1,path2).all()


# path1 = "D:/Documents/Documents/Downloads/ML-CSV/ML-CSV/ws.csv"
# candidateElimination(path1).all()
# tree = {'S': [['A', 1], ['B', 2]],
#         'A': [['E', 13]],
#         'B': [['E', 5]]}
# heuristic = {'S': 5, 'A': 4, 'B': 5, 'E': 0}
# start_node = 'S'
# end_node = 'E'
# aStar(tree,heuristic,start_node,end_node).all()


# h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 0, 'J': 1, 'T': 3}
# graph1 = {
#         'A': [[('B', 1), ('C', 1)], [('D', 1)]],
#         'B': [[('G', 1)], [('H', 1)]],
#         'C': [[('J', 1)]],
#         'D': [[('E', 1), ('F', 1)]],
#         'G': [[('I', 1)]]
#     }
# G1 = aoStar(graph1 , h1 , 'A')
# G1.all()

# h2 = {'A': 1, 'B': 6, 'C': 12, 'D': 10, 'E': 4, 'F': 4, 'G': 5, 'H': 7}
# graph2 = {
#         'A': [[('B', 1), ('C', 1)], [('D', 1)]],
#         'B': [[('G', 1)], [('H', 1)]],
#         'D': [[('E', 1), ('F', 1)]]
#     }
# G2 = aoStar(graph2, h2, 'A')
# G2.applyAOstar()
# G2.printSolution()


# kNearestNeighbour().all()
# locallyWeightedRegression().all()


# locallyWeightedRegression('C:/Users/ASHLESH M D/Desktop/Eclipse Data/Tips.csv').run()