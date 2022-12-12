import os
import sys
from collections import defaultdict, Iterable
import glob
import timeit
from memory_profiler import memory_usage
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import pandas as pand

eps = '_'


class Stack:  # Define new class - Stack
    def __init__(self):
        self.stacklist = []

    def size(self):
        return len(self.stacklist)
        # Returns size of the stack e.g. length of a list

    def isEmpty(self):
        return self.size() == 0
        # Check if stack is empty, returns True if stack is empty

    def push(self, newItem):
        self.stacklist.append(newItem)
        # Add element on top of stack

    def pop(self):
        self.stacklist.pop()
        # Take out the top element from stack

    def peek(self):
        return self.stacklist[self.size() -1]
        # Peek, check the element on top of stack but do not remove it from stack


class TreeNode(object):
    # Define class TreeNode - We will be making a tree, and therefore we define this class for nodes of the tree

    def __init__(self):
        self.data = None
        self.parent = None
        self.children = []
        # Every node has data - name of the element (a, b, c...)
        # Parent: represents parent node
        # Children: List of elements (a, b, c ...), which are children of current node

    def addChild(self, object):
        self.children.append(object)
        # Add new child: Append name of the element to the list

    def addParent(self, object):
        self.parent = object
        #Add parent: Node that is parent to current node


class Tree(object):  # Class Tree - Nodes belong to a tree
    def __init__(self):
        self.rootNode = None  # Define Root Node
        self.nodes = []  # List of nodes that are in the tree

    def show(self):
        for node in self.nodes:
            print(node.data, node.children)
            # Print nodes and their children

    def addNode(self, object):
        self.nodes.append(object)
        # Add new node to a tree


def XmlWellForm(data):
    # Function to check if the .xml file is well-formed and to build a tree that corresponds to the .xml file
    if isinstance(data, str):
        xmlf = open(data, "r")  # Open .xml file
    xml = xmlf.read()
    lines_xml = xml.split("\n")  # Split the .xml file into lines

    # if (lines_xml[0][0] == '0') and (lines_xml[len(lines_xml) - 1][0] == '1') and \
    #       (lines_xml[0][2] == lines_xml[len(lines_xml) - 1][2]) and (len(lines_xml) % 2 == 0):
    # Rough check: Checking if the start is to open element and if end is to close the same root element
    xmlWellFormedFirst = True
    first_check = True
    #else:
    #    xmlWellFormedFirst = False
    #     first_check = True

    if xmlWellFormedFirst and first_check:
        # If the first check is satisfied we proceed with checking the well-formedness of .xml file
        # And building the tree

        ''' Tree Initialization '''
        elemStack = Stack()
        previousNode = TreeNode()
        firstNode = True
        xmlTree = Tree()
        ''' / Tree Initialization'''

        for line in lines_xml:  # Loop through the whole file
            elem = line.split(" ")  # Split each line in words on " " delimiter
            # print(line, "xml line")
            if (not elemStack.isEmpty()) or firstNode:
                if elem[0] == "0":  # If it is opening element:
                    currentNode = TreeNode()  # Create new node
                    stackEl = ["1", elem[1]]
                    elemStack.push(stackEl)
                    # Put in the stack expression for closing this element
                    # It will be easier to check when closing elements
                    currentNode.data = elem[1]  # Assign name to node
                    if xmlTree.rootNode is None:  # In case it is a Root element: No parent
                        firstNode = False
                        currentNode.parent = None
                        xmlTree.rootNode = currentNode
                    else:
                        currentNode.addParent(previousNode)
                        # If not Root element, previous node is parent to current one
                        previousNode.addChild(currentNode.data)
                        # The current node is added to a list of children of a previous node
                    xmlTree.addNode(currentNode)
                    previousNode = currentNode
                if elem[0] == "1":  # Closing an element
                    # If closing element expression is matching the top of the stack
                    # Pop the element from the stack
                    if elem[1] == elemStack.peek()[1]:
                        elemStack.pop()
                        previousNode = previousNode.parent  # Assign previous node to its parent
                    else:
                        return None
        # If stack is empty return Tree
        if elemStack.isEmpty():
            return xmlTree
    else:
        return None


def insertDot(regExp):  # Insert dot '.' to represent concatenation in regular expression
    regExWithDot = ''

    for c in regExp:
        if c.isalpha() and regExWithDot and regExWithDot[len(regExWithDot)-1] != '(':
            regExWithDot += '.'
            regExWithDot += c
        elif c =='('and regExWithDot and regExWithDot[len(regExWithDot)-1] != '(':
            regExWithDot += '.'
            regExWithDot += c
        else:
            regExWithDot += c
    #print(regExWithDot,"regex withdot")
    return regExWithDot


def regex2post(regE):  # Convert regular expression from infix to postfix

    postfix_reg = ''
    operator_stack = []

    precedenceMap = {
        '(' : 1,
        ')' : 1,
        '?' : 2,
        '*' : 2,
        '+' : 2,
        '.' : 3
    }
    for c in regE:
        if c.isalpha() or c == '*' or c == '+' or c == '?':
            postfix_reg += c
        elif c == '(':
            operator_stack.append(c)
        elif c == '.':
            if operator_stack:
                if operator_stack[len(operator_stack)-1] == '.':
                    postfix_reg += c
                else:
                    operator_stack.append(c)
            else:
                operator_stack.append(c)
        elif c == ')':
            while operator_stack and operator_stack[len(operator_stack)-1] != '(':
                head = operator_stack.pop()
                postfix_reg += head
            if operator_stack:
                if operator_stack[len(operator_stack)-1] == '(':
                    operator_stack.pop()
    while operator_stack:
        postfix_reg += operator_stack.pop()
    #print(postfix_reg,"regex")
    return postfix_reg


class State(object):
    def __init__(self, name = None):
        self.name = name
        self.transitions = defaultdict()  # Following state
        self.transitions[eps] = set()


class Fragment(object):
    def __init__(self, startState, finalState):
        self.startState = startState
        self.finalState = finalState
        self.literals = []
        self.states = []


def post2NFA(postfixRegE):  # Convert postfix regular expression to NFA

    stack = []
    global eps

    for c in postfixRegE:
        if c.isalpha():
            newStart = State(c)
            newFinal = State()
            newStart.transitions[c] = newFinal
            newF = Fragment(newStart, newFinal)
            newF.literals.append(c)
            newF.states.append(newStart)
            newF.states.append(newFinal)
            stack.append(newF)

        elif c == '.':
            fragment2 = stack.pop()
            fragment1 = stack.pop()
            for i in fragment2.literals:
                fragment1.literals.append(i)
            fragment1.finalState.transitions[eps].add(fragment2.startState)
            for item in fragment2.states:
                fragment1.states.append(item)
            fragment1.finalState = fragment2.finalState
            stack.append(fragment1)

        elif c == '?':
            fragment = stack.pop()
            newStart = State()
            newFinal = State()
            newStart.transitions[eps].add(fragment.startState)
            newStart.transitions[eps].add(newFinal)
            fragment.finalState.transitions[eps].add(newFinal)
            fragment.startState = newStart
            fragment.finalState = newFinal
            fragment.states.append(newStart)
            fragment.states.append(newFinal)
            stack.append(fragment)

        elif c == '*':
            fragment = stack.pop()
            newStart = State()
            newFinal = State()
            newStart.transitions[eps].add(fragment.startState)
            newStart.transitions[eps].add(newFinal)
            fragment.finalState.transitions[eps].add(newFinal)
            fragment.finalState.transitions[eps].add(fragment.startState)
            fragment.startState = newStart
            fragment.finalState = newFinal
            fragment.states.append(newStart)
            fragment.states.append(newFinal)
            stack.append(fragment)

        elif c == '+':
            fragment = stack.pop()
            newStart = State()
            newFinal = State()
            newStart.transitions[eps].add(fragment.startState)
            fragment.finalState.transitions[eps].add(newFinal)
            fragment.finalState.transitions[eps].add(fragment.startState)
            fragment.startState = newStart
            fragment.finalState = newFinal
            fragment.states.append(newStart)
            fragment.states.append(newFinal)
            stack.append(fragment)
    if stack:
        fragment = stack.pop()
    return fragment


def e_closure(state, visited):
    global eps
    if state.transitions[eps] and (state not in visited):
        #print(visited)
        for item in state.transitions[eps]:
            e_closure(item, visited)
    visited.add(state)
    return visited


class DFA(object):
    def __init__(self):
        self.startState = DFAState
        self.dfa_states = set()


class DFAState(object):
    def __init__(self):
        self.name = None
        self.transitions = {}
        self.accepting = False
        self.list_of_nfa_states = []

    def __eq__(self, other):
        return self.list_of_nfa_states == other.list_of_nfa_states


def makeDFA(start_set, NFA, e_closure_result):

    # create first DFAnode
    dfaNode = DFAState()

    for state in start_set:
        dfaNode.list_of_nfa_states.append(state)
    if NFA.finalState in dfaNode.list_of_nfa_states:
        dfaNode.accepting = True
    dfa_stack = [dfaNode]

    NFA.finalState

    for dfa in dfa_stack:
        for chr in NFA.literals:
            states = set()
            for nfa_state in dfa.list_of_nfa_states:
                if chr in nfa_state.transitions:
                    some_state = nfa_state.transitions[chr]
                    # check if some_states exist
                    some_states = e_closure_result[some_state]
                    if isinstance(some_states, Iterable):
                        states.update(some_states)
                    else:
                        states.add(some_states)
                    states.add(some_state)
            if states:
                newDfaNode = DFAState()
                newDfaNode.list_of_nfa_states = states
                if NFA.finalState in states:
                    newDfaNode.accepting = True
                if not newDfaNode in dfa_stack:
                    dfa.transitions[chr] = newDfaNode
                    dfa_stack.append(newDfaNode)
                else:
                    for node in dfa_stack:
                        if node == newDfaNode:
                            dfa.transitions[chr] = node
    return dfa_stack


def match(children, dfa_start_state):
    string_to_check = ''
    for child in children:
        string_to_check += child
    match_str = True
    if not string_to_check:
        return match_str and dfa_start_state.accepting
    for chr in string_to_check:
        if chr in dfa_start_state.transitions:
            dfa_start_state = dfa_start_state.transitions[chr]
        else:
            #print(dfa_start_state, "failnode")
            match_str = False
    return match_str and dfa_start_state.accepting


def match_empty(children):
    string_to_check = ''
    for child in children:
        string_to_check += child
    return string_to_check == ''


def xml_validate(xml_file):
    # This program is called with two files as argument
    # First is .xml file
    # xml_file = sys.argv[1]  # "/home/nedeljko/IdeaProjects/WebDataModelsProject/test.xml"
    # Second argument is .dtd file

    xml_tree = XmlWellForm(xml_file)
    if xml_tree:
        print("Xml is well-formed.")
    else:
        print("Xml is not well-formed.")

    if xml_tree:
        dtd_f = open(dtd_file, "r")
        dtd = dtd_f.read()
        # Split the .xml file into lines
        lines_dtd = dtd.split("\n")
        valid = True
        for line in lines_dtd:
            elems = line.split(" ")
            #print(elems, "dtd")
            nodeElement = elems[0]
            regex = elems[1]
            if regex != '_':
                regex_with_dot = insertDot(regex)
                postfix_regex = regex2post(regex_with_dot)
                frag = post2NFA(postfix_regex)
                start_state = frag.startState
                closure_result = {}
                for state in frag.states:
                    visited_states = set()
                    closure_result[state] = e_closure(state, visited_states)
                    closure_result[state].add(state)
                eclosure_start_set = closure_result[start_state]
                dfa = makeDFA(eclosure_start_set, frag, closure_result)
                for node in xml_tree.nodes:
                    if node.data == nodeElement:
                        if not(match(node.children, dfa[0])):
                            valid = False
                            break
                if valid == False:
                    break
            else:
                for node in xml_tree.nodes:
                    if node.data == nodeElement:
                        if not(match_empty(node.children)):
                            valid = False
                            break
                if valid == False:
                    break
        if valid:
            print("Xml is valid.")
        else:
            print("Xml is not valid.")

dtd_file = sys.argv[2]  # "/home/nedeljko/IdeaProjects/WebDataModelsProject/test.dtd"
# Set boolean variable xmlWellFormed to False
xmlWellFormed = False
xml_file = sys.argv[1]
xml_validate(xml_file)