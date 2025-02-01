# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 00:31:47 2025

@author: Ruben

This programme can be used to solve the following problem. Given a list li with
n integers and a target integer t, can we obtain t from li with just the 
operators +,-,/,*?
The code is made to give a solution if it exists, but can be easily modified to 
give all solutions.

This game is more famous for n=4 and n=6, in which case there are definitely
faster algorithms specific to these cases. This code is intended to work for
all n, but may be quite slow.

--
edit 1:
  - this algorithm is essentially the same idea as the other file in the same
    repository, but with some attempts to make it more efficient
  - since +,-,* are commutative, we now don't loop over all binary trees 
    anymore, instead we realise that since we already loop over all 
    permutations of li, we only need to loop over the set of representatives of 
    the orbits of the permutations on the binary trees (a permutation of a 
    binary tree is just rotating the part underneath a node around that node).
        Note however that for /, we still need to do all permutations since it
        is not a commutative operator
  - I would love to know if there are more efficient ways to do this, or to
    make this particular algorithm more efficient. Also if anybody notices a 
    mistake, I would love to know as well. Thanks for reading.
"""

import operator
import itertools
from sympy.utilities.iterables import multiset_permutations

def op_to_str(op):
    if op == operator.add:
        return '+'
    if op == operator.mul:
        return '*'
    if op == operator.sub:
        return '-'
    if op == operator.truediv:
        return '/'

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
            
    def ComputeOperationsOnList(self,li,ops):
        #given a full binary tree 'self', a list li of n integers and ops a list 
        #with n-1 operators out of +,-,*,/, the function calculates the 
        #expression obtained from writing the elements of li in order with
        #op[i] between li[i] and li[i+1] but with the brackets determined by 
        #self, i.e. self determines the calculation order
        if self.left is None and self.right is None:
            # In our case only need to check one of the two since our
            # binary trees are full
            return [[li[self.data[0]]]]
        else:
            op_index = self.left.data[-1]
            op = ops[op_index]
            left = self.left.ComputeOperationsOnList(li,ops)
            right = self.right.ComputeOperationsOnList(li,ops)
            if left == False or right == False:
                return False
            else:
                left_value = left[0][0]
                right_value = right[0][0]
                if left_value == target:
                    return left
                if right_value == target:
                    return right
                try:
                    x = op(left_value,right_value)
#                    if int(x) == x and x>= 0:                 
#                           removed this condition since can always
#                           easily modify answer to get rid of
#                           non-integer rationals and non-negative integers
#                           maybe can rewrite the programme to do this
                    result = [[x,left[0][0],op,right[0][0]]]
                    if len(left[0]) > 1: 
                        result.extend(left)
                    if len(right[0]) >1: 
                        result.extend(right)
                    return result
#                    else:
#                        return False
                except ZeroDivisionError as err:
                    return False         

def BinaryTrees(n, low=0):
    #generates list of all binary trees with n leaves
    #the parameter low is only used in the recursive steps to 
    #give the subtrees appropriate labels
    if n == 1:
        yield Node([low])
    else:
        li = list(set([low,n+low-1]))
        for i in range(n-1):
            root = Node(li)
            for left_root in list(BinaryTrees(i+1, low+0)):
                root.left = left_root
                for right_root in list(BinaryTrees(n-i-1, low+i+1)):
                    root.right = right_root
                    yield root
                    
def BinaryTreePermutationRepresentatives(n, low=0):
    #There is a standard permutation on binary trees, and this function gives
    #for each orbit of this permutation exactly one tree
    if n == 1:
        yield Node([low])
    else:
        li = list(set([low,n+low-1]))
        for i in range(n//2):
            root = Node(li)
            for left_root in list(BinaryTreePermutationRepresentatives(i+1, low+0)):
                root.left = left_root
                for right_root in list(BinaryTreePermutationRepresentatives(n-i-1, low+i+1)):
                    root.right = right_root
                    yield root        

def CheckSolution(li,target):
    #given a list li of n integers and integer target, checks whether
    #one can make target out of the integers in li using +,-,*,/
    n = len(li)
    operators = [operator.add,operator.sub,operator.mul,operator.truediv]
    operatorlist = list(itertools.product(operators,repeat=n-1))
    operatorlistnodiv = [i for i in operatorlist if operator.truediv not in i]
    operatorlistdiv =[i for i in operatorlist if operator.truediv in i]
    permutations = list(multiset_permutations(li))
    #can fix first entry due to symmetry of the binary trees
    trees = list(BinaryTrees(n))
    trees_perm_reps = list(BinaryTreePermutationRepresentatives(n))
    for perm_li in permutations:
        #permutations are needed because our binary tree goes from left to right
        #and thus does not allow operation on a tuple with an i-ith and i+1-th
        #element of li
        for ops in operatorlistnodiv:
            for tree in trees_perm_reps:
                x = tree.ComputeOperationsOnList(perm_li,ops)
                if x == False:
                    continue
                else:
                    if x[0][0] == target:
                        return (perm_li,ops,x)
        for ops in operatorlistdiv:
            for tree in trees:
                x = tree.ComputeOperationsOnList(perm_li,ops)
                if x == False:
                    continue
                else:
                    if x[0][0] == target:
                        return (perm_li,ops,x)
    return False

def solution_to_string(li,target):
    #gives result of CheckSolution in a readable format
    solution = CheckSolution(li,target)
    if solution == False:
        return('No solution')
    else:
        string = "Obtain " + str(target) + " from " + str(li) + ": \n"
        solution_calculations = list(reversed(solution[2]))
        for calc in solution_calculations:
            string = string + "\n" + str(calc[0]) + "=" + str(calc[1]) + op_to_str(calc[2]) + str(calc[3])
        return string
 
li = [75,100,7,4,9,7]
target = 544
       
solstring = solution_to_string(li,target)
print(solstring)

#    li_remove_last = li[:-1]
#    permutations_remove_last = list(multiset_permutations(li_remove_last))
#    permutations = [[li[-1]]+i for i in permutations_remove_last]
#    #can fix first entry due to symmetry of the binary trees
