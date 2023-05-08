'''
CAPP30122 W'22: Building decision trees

María Gabriela Ayala
Fabián Baltierra
'''

import math
import sys
import pandas as pd


def go(training_filename, testing_filename):
    '''
    Construct a decision tree using the training data and then apply
    it to the testing data.

    Inputs:
      training_filename (string): the name of the file with the
        training data
      testing_filename (string): the name of the file with the testing
        data

    Returns (list of strings or pandas series of strings): result of
      applying the decision tree to the testing data.
    '''
    df_train = pd.read_csv(training_filename, dtype=str)
    df_test = pd.read_csv(testing_filename, dtype=str)
    target = df_train.columns[-1] 
    tree = build_tree(df_train, target)
    default = tree.get_label(target)
    #print(default)
    rv = []

    for _, row in df_test.iterrows():
        label = apply_tree(row, tree, default)
        rv.append(label)

    return rv


def apply_tree(row, tree, default):
    '''
    Recursion to apply decision tree to testing data.
    Input:
        (pd Series): row from a DataFrame
        (node Object): decision tree
    Output:
        (str): class label from target attribute after applying
        decision tree to data.
    '''
    #Base case
    if tree.children == {}:
        return default
    #Recursion
    else:
        test_val = row[tree.split_col]
        if test_val in tree.children:
            for child_name, child_node in tree.children.items():
                if test_val == child_name:
                    #print(tree.split_col)
                    #print(child_name)
                    #print(child_node.class_label)
                    #print()
                    return apply_tree(row, child_node, default)
        else: 
            return tree.class_label
      

def build_tree(df_train, target):
    '''
    Constructs the decision tree from the training data.
    Input:
        (pd DataFrame): training data
        (str): name of target (ie. last column in training dataset)
    Output:
        (node object): decision tree built from training data 
    '''

    remain_split_cols = df_train.columns.tolist()[:-1]
    class_label = get_label(df_train, target)
    tree = Node(class_label, None, df_train)
    
    #Base case
    if len(df_train[target].unique()) == 1:
        return tree
    #Recursion
    else:
        split_col, gain_ratio = find_best_split(remain_split_cols, df_train, target)
        if gain_ratio != 0:
            remain_split_cols.remove(split_col) 
            tree.split_col = split_col
            for child_name, child_dataframe in df_train.groupby(split_col):
                child_node = build_tree(child_dataframe, target)
                tree.add_child(child_name, child_node)
        else:
            return tree

    return tree


def find_best_split(remain_split_cols, df_train, target):
    '''
    Given the remaining attributes, finds the best splitting column. In the case of 
    a tie where two attributes have the same gain ratio, breaks the tie by choosing 
    the attribute that occurs earlier in the natural ordering for strings
    Inputs:
        (lst): list of remaining attributes at the node
        (pd DataFrame): training data
        (str): name of target (ie. last column in training dataset)
    Output:
        (tuple): name of splitting column attribute, gain ratio
    '''
    c0 = df_train[target].unique()[0]
    c1 = df_train[target].unique()[1]
    rv = {}
    gain_ratio_lst = []
    
    for split_col in remain_split_cols:
        parent_c0 = df_train.groupby(split_col)[target].apply(lambda x: x[x == c0].count()).sum() 
        parent_c1 = df_train.groupby(split_col)[target].apply(lambda x: x[x == c1].count()).sum()
        parent_gini = get_gini(parent_c0, parent_c1)
        kid_c0 = df_train.groupby(split_col)[target].apply(lambda x: x[x == c0].count())
        kid_c1 = df_train.groupby(split_col)[target].apply(lambda x: x[x == c1].count())
        weighted_ginis = []
        split_info = []
        for i in range(len(df_train.groupby(split_col))):
            grandkid_c0 = kid_c0[i]
            grandkid_c1 = kid_c1[i]
            weight, si = get_weight_si(parent_c0, parent_c1, grandkid_c0, grandkid_c1)
            weighted_ginis.append(weight)
            split_info.append(si)
        sum_weights = sum(weighted_ginis)
        sum_split_info = sum(split_info)
        if sum_split_info != 0:
            gain_ratio = (parent_gini - sum_weights) / sum_split_info
        else:
            gain_ratio = 0
        rv[split_col] = gain_ratio
        gain_ratio_lst.append(gain_ratio)

    max_gain_ratio = max(gain_ratio_lst)
    #for att, gain_r in rv.items():
    #max_gain_ratio = max(rv.items(), key=lambda x: x[1]) 
    possible_split_cols = [] #List of attributes with max gain_ratio (in case of ties)
    for att, gain_r in rv.items():
        if gain_r == max_gain_ratio:
            possible_split_cols.append(att)
  
    if len(possible_split_cols) == 1:
        return possible_split_cols[0], rv[possible_split_cols[0]]
    else:
        return min(possible_split_cols), rv[min(possible_split_cols)] #Break tie


def get_gini(c0, c1):
    '''
    Calculates gini coefficient.
    '''
    n = c0 + c1
    prob_c0 = c0/n
    prob_c1 = c1/n
    
    return 1 - (prob_c0**2 + prob_c1**2)


def get_weight_si(parent_c0, parent_c1, grandkid_c0, grandkid_c1):
    '''
    Computes weighted ginis and split info.
    Inputs:
        (int): sum of parent first target binary value
        (int): sum of parent second target binary value
        (int): sum of kid first target binary value
        (int): sum of kid second target binary value
    Output:
        (tuple): weight, split info
    '''
    prob = (grandkid_c0 + grandkid_c1)/(parent_c0 + parent_c1)
    kid_gini = get_gini(grandkid_c0, grandkid_c1)
    weight = prob * kid_gini
    split_info = (prob * math.log2(prob)) *-1
    
    return weight, split_info


def get_label(df_train, target):
    '''
    Finds the maximum value count for the target class to set as a default 
    value. In the case of a tie, chooses the value that occurs earlier 
    in the natural ordering for strings
    Input:
        (pd DataFrame): training data
        (str): name of target (ie. last column in training dataset)
    Output:
        (str): class label
    '''
    if len(df_train[target].unique()) == 1:
        class_label = df_train[target].unique()[0]
    else:
        c0 = df_train[target].unique()[0]
        c1 = df_train[target].unique()[1]
        c0_count = df_train[target].value_counts()[c0]
        c1_count = df_train[target].value_counts()[c1]
    
        if c0_count > c1_count: 
            class_label = c0
        elif c1 > c0:
            class_label = c1
        else:
            class_label = min(c0,c1)   
        
    return class_label


class Node:
    '''
    A class representing nodes of a decision tree and child nodes which
    are instances of the Node class themselves.
    '''
    def __init__(self, class_label, split_col, data):
        '''
        Constructor of the Node class.
        '''
        self.class_label = class_label
        self.split_col = split_col
        self.data = data
        self.children = {}
    
    def add_child(self, child_name, child_df):
        '''
        Method for adding children to a node in a dictionary structure.
        '''
        self.children[child_name] = child_df
    
    def get_label(self, target):
        '''
        Method for getting default value.
        '''
        if len(self.data[target].unique()) == 1:
            self.default = self.data[target].unique()[0]
        else:
            c0 = self.data[target].unique()[0]
            c1 = self.data[target].unique()[1]
            c0_count = self.data[target].value_counts()[c0]
            c1_count = self.data[target].value_counts()[c1]
        
            if c0_count > c1_count: 
                self.default = c0
            elif c1 > c0:
                self.default = c1
            else:
                self.default = min(c0,c1)   
        
        return str(self.default)
    
    def __str__(self):
        '''
        String representation of the Node class.
        '''
        s = "\n├─Splitting Column: " + self.split_col + "\n├─Default label: " + self.class_label + "\n|"

        for child_name, child_node in self.children.items():
            s += "\n├─----Child value: " + child_name + "\n├─----Child label: " + child_node.class_label\
                 + "\n|\n├─---------Grandchild splitting column:  " + child_node.split_col + "\n|"
            for grandchild_name, grandchild_node in child_node.children.items():
                s+= "\n├─--------------Grandchild name: " + grandchild_name + \
                    "\n├─--------------Grandchild label: " + grandchild_node.class_label + "\n|"
        
        return s

###########


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 {} <training filename> <testing filename>".format(
            sys.argv[0]))
        sys.exit(1)

    for result in go(sys.argv[1], sys.argv[2]):
        print(result)