'''

First we initialize the utility functions 

'''
import numpy as np 
def unique_vals(rows, col):
    """Find the unique values for a column in a dataset."""
    return set([row[col] for row in rows])

def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)

from itertools import chain, combinations

def powerset(iterable):
    '''
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    '''
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


'''
These are the config functions

'''
columns = []
data = np.array([])

def update_cols(new_cols):
    global columns
    columns = new_cols

def update_data(new_data):
    global data 
    data = new_data

'''

Decision tree classes and functions starts

'''
class Question:
    """A Question is used to partition a dataset.

    This class just records a 'column number' (e.g., 0 for Color) and a
    'column value' (e.g., Green). The 'match' method is used to compare
    the feature value in an example to the feature value stored in the
    question. See the demo below.
    """

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            columns[self.column], condition, str(self.value))

def partition(rows, question):
    """Partitions a dataset.

    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return np.array(true_rows), np.array(false_rows)
def gini(rows):
    """Calculate the Gini Impurity for a list of rows.

    There are a few different ways to do this, I thought this one was
    the most concise. See:
    https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

##### Banzhaf Part starts 


import entropy_estimators as ee

def isWinning(feature_col,coalition,rows,threshold = 0.50):
    ''' Checks if union of the feature and coalitions leads to win
    
    A feature is winning if it's interdependent on atleast half of the members in the coalition.
    The interdependence is measured using conditional mutual information.
    
    '''
    total_dependence = 0
    x = feature_col.reshape(-1,1).tolist()

    if len(coalition) == 1:
        y = rows[:,[coalition[0]]].tolist()
        return ee.mi(x,y) >= threshold

    for i in range(0,len(coalition)):
        y = rows[:,[coalition[i]]].tolist()
        z = rows[:,coalition[:i] + coalition[i+1:]].tolist()    
        if ee.cmi(x,y,z) >= threshold:
            total_dependence = total_dependence + 1
    return float(total_dependence)/float(len(coalition)) >= 0.5

def find_best_split_inf_gain(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # number of columns

    for col in range(n_features):  # for each feature
        values = set([row[col] for row in rows])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the dataset
            true_rows, false_rows = partition(rows, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_question


def banzhaf(index,rows,ancestors=[]):
    '''
    Calculates the banzhaf power index of the feature whose position is given by index
    rows is the dataset on which the index is calculated.
    '''
    if ancestors[index]:
        return -1

    positive_swing = 0
    
    index_col=rows[:,[index]]

    cols_to_be_removed = []
    for i in range(len(ancestors)):
        if ancestors[i]:
            cols_to_be_removed.append(i)
        if i == index:
            cols_to_be_removed.append(i)

    rows = np.delete(rows,cols_to_be_removed,1)

    total_list = np.array(range(rows.shape[1]))
    all_coalitions = list(powerset(total_list))
 
    for coalition in all_coalitions:
        if len(coalition) == 0:  #ignore the nullset.
            continue
        if isWinning(index_col,list(coalition),rows):
            positive_swing = positive_swing + 1

    banzhaf_index = float(positive_swing) / (len(all_coalitions) - 1)
    return banzhaf_index

import copy
import numpy as np 
from statistics import mean
def argmax(lst):
     return lst.index(max(lst))

def find_best_split_banzhaf(rows,ancestors):
    """Find the best question to ask by calculating the banzhaf power index
    and selecting the maximum value from it """
    
    banzhaf_rows = []
    for i in range(len(ancestors)):
        if not ancestors[i]:
            banzhaf_rows.append(banzhaf(i,rows,ancestors))
        else:
            banzhaf_rows.append(-1)
    idx_max = argmax(banzhaf_rows)
    mean_val = mean(unique_vals(rows,idx_max))
    question = Question(idx_max,mean_val)
    return question


class Decision_Node:
    """A Decision Node asks a question.

    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

class Leaf:
    """A Leaf node classifies data.

    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """

    def __init__(self, rows):
        self.predictions = class_counts(rows)

def build_tree(rows,banzhaf=False,depth=0):
    if depth == 3:
        return Leaf(rows)
    question = find_best_split_inf_gain(rows)
    true_rows, false_rows = partition(rows,question)
    if banzhaf:
        ancestors = [False for i in range(len(rows[0]))]
        ancestors[question.column] = True 
        true_branch = build_banzhaf_tree(true_rows,ancestors)
        false_branch = build_banzhaf_tree(false_rows,ancestors)
    else:
        true_branch = build_tree(true_rows,depth=depth+1)
        false_branch = build_tree(false_rows,depth=depth+1)
    return Decision_Node(question, true_branch, false_branch)


def build_banzhaf_tree(rows,ancestors,depth=1):
    if depth == 3:
        return Leaf(rows)
    question = find_best_split_banzhaf(rows,ancestors)
    if not is_numeric(question.value):
        ancestors[question.column] = True 
    true_rows,false_rows = partition(rows,question)
    true_branch = build_banzhaf_tree(true_rows,ancestors = ancestors,depth=depth + 1)
    false_branch = build_banzhaf_tree(false_rows,ancestors = ancestors, depth=depth + 1)
    return Decision_Node(question, true_branch, false_branch)

def print_tree(node, spacing=""):
    """World's most elegant tree printing function."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print (spacing + str(node.question))

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")

def classify(row, node):
    """See the 'rules of recursion' above."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return max(node.predictions,key=node.predictions.get)

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch) 