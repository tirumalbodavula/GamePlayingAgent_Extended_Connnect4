## PARTA  problem formulation:

Problem Formulation:

# Search Space: 
Generating the tree of depth d at each step.

# Start state: 
get_expectimax function always starts with MAX level and consider next level as chance nodes.

# Operations:
At each max level we consider the maximum value of the children that are chance nodes and outputs that action.
At each chance level we consider the average value of the children and that is the value of the chance node which will be returned to parent max level.
If the level of depth is zero then the we will get the points for that state and returns it.

# Idea of the algorithm:
I have used expectimax algorithm for partA, in which my algorithm always treat level 1 as MAX level then it calls the.
If the current call is a maximizer node, return the maximum of the state values of the nodes successors.
If the current call is a chance node, then return the average of the state values of the nodes successors(assuming all nodes have equal probability).
 If different nodes have different probabilities the expected utility from there is given by summation of (probability of that action*value of that child).
We call the function recursively until we reach a terminal node(the state with no successors). Then return the utility for that state.

## PARTB  problem formulation:

# Problem Formulation:

# Search Space:
Generating the tree of depth d at each step.

# Start state:
get_intelligent_move function always starts with MAX level and consider next level as MIN level and ALPHA BETA pruning is applied.

# Operations:
At each max level we consider the maximum value of the children that are min nodes and outputs that action.
At each min level we consider the minimum value of the children that are max nodes and outputs that action which will be returned to parent max level.
If the level of depth is zero then the we will get the points for that state  and returns it.

# Idea of the algorithm:
I have used alpha beta pruning technique on min max algorithm for partB, in which my algorithm always treat level 1 as MAX level then it calls the min level and so on till depth is zero.
If the current call is a maximizer node, return the maximum of the state values of the nodes successors.
If the current call is a minimizer node, return the minimum of the state values of the nodes successors.
We call the function recursively until we reach a terminal node(the state with no successors). Then return the utility for that state.
we implement a condition where 
Alpha is the best value that the maximizer currently can guarantee at that level or above. 
Beta is the best value that the minimizer currently can guarantee at that level or above.
if alpha>=beta break from the for loop.

# Heuristic:
for the terminal state return the value w.r.t that palyer - value w.r.t opponent player. This optimizes the action picked at each layer.
At each step the tree will be grown based on the valid actions checked.
The order of the valid actions will be in such a way that action which start from the middle of the board will be picked first, then picks the action which is close to middle, tends to move outside. 
