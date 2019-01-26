# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>

"""
#####################################################
#####################################################



"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Questoin 1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    print (problem.isGoalState(problem.getStartState()) )
    print ( problem.getSuccessors(problem.getStartState()) )

    """
    "*** YOUR CODE HERE ***"
    dfs_stack = util.Stack()
    for successor in problem.getSuccessors(problem.getStartState()):
        #essentially we the push tuple = (successor, successor_directions, position_successor_has_visited, successor_count)
        dfs_stack.push((successor[0], [successor[1]], [problem.getStartState()], successor[2]))

    while not dfs_stack.isEmpty():
        data = dfs_stack.pop() #current node
        data_dict = {   'curr_pos': data[0], #current position of pacman
                        'direction': data[1], #direction to move
                        'visited': data[2], #positions on the map we have visited
                        'total_count': data[3]} #total cost of steps taken

        if problem.isGoalState(data_dict['curr_pos']):
            #print ('done', data_dict['direction'])
            #print ('count',data_dict['total_count'])
            return data_dict['direction']

        for node_data in problem.getSuccessors(data_dict['curr_pos']):
            temp_dir_list = [] #reset the list per Successor (if we don't the temp list will fill up with directions from all possible successors)
            temp_visited = [] # ^^same as above
            coordinates = node_data[0]
            new_dir = node_data[1]
            cost = node_data[2]
            if coordinates not in data_dict['visited']:
                temp_dir_list.extend(data_dict['direction']) #extend to make local "copies" of the list
                temp_dir_list.append(new_dir)
                temp_visited.extend(data_dict['visited'])
                temp_visited.append(data_dict['curr_pos'])
                temp_count = data_dict['total_count'] + cost
                dfs_stack.push((coordinates,temp_dir_list,temp_visited,temp_count))

    print ("Mission Failed - pacman died from starvation")
    return []

def breadthFirstSearch(problem):
    """Questoin 1.2
     Search the shallowest nodes in the search tree first.
     """
    "*** YOUR CODE HERE ***"
    #Had to change from depth first implementation
    #There were errors with data_dict['visited'] when using the corners and heuristics
    #Therefore I changed the visited list to be a global variable
    #Also dropped the count in the data_dict because it wasnt needed for the requirements

    bfs_queue = util.Queue()
    for successor in problem.getSuccessors(problem.getStartState()):
        #initially we are pushing the successors = (successor, successor_directions)
        bfs_queue.push((successor[0], [successor[1]]))
    visited = [problem.getStartState()] #initially containing the startstate

    while not bfs_queue.isEmpty():
        data = bfs_queue.pop() #current state
        data_dict = {   'curr_pos': data[0], #current position of pacman
                        'direction': data[1]} #direction to move

        if problem.isGoalState(data_dict['curr_pos']):
            #print ('done', data_dict['direction'])
            return data_dict['direction']

        for node_data in problem.getSuccessors(data_dict['curr_pos']):
            temp_dir_list = [] #reset the list per Successor (if we don't the temp list will fill up with directions from all possible successors)
            coordinates = node_data[0]
            new_dir = node_data[1]
            if coordinates not in visited:
                visited.append(coordinates)
                temp_dir_list.extend(data_dict['direction'])
                temp_dir_list.append(new_dir)
                bfs_queue.push((coordinates, temp_dir_list))

    print ("Mission Failed - pacman died from starvation")
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Question 1.3
    Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    bfs_pqueue = util.PriorityQueue()
    for successor in problem.getSuccessors(problem.getStartState()):
        #initially we are pushing the successors = ((successor, successor_directions),heuristic)
        bfs_pqueue.push((successor[0], [successor[1]]), heuristic(problem.getStartState(), problem))
    visited = [problem.getStartState()]

    while not bfs_pqueue.isEmpty():
        data = bfs_pqueue.pop() #current node
        data_dict = {   'curr_pos': data[0], #current position of pacman
                        'direction': data[1]}# #direction to move

        if problem.isGoalState(data_dict['curr_pos']):
            return data_dict['direction']

        for node_data in problem.getSuccessors(data_dict['curr_pos']):
            temp_dir_list = [] #reset the list per Successor (if we don't the temp list will fill up with directions from all possible successors)
            coordinates = node_data[0]
            new_dir = node_data[1]
            if coordinates not in visited:
                visited.append(coordinates)
                temp_dir_list.extend(data_dict['direction'])
                temp_dir_list.append(new_dir)
                heuristic_priority = heuristic(coordinates,problem)
                bfs_pqueue.push((coordinates,temp_dir_list), heuristic_priority)

    print ("Mission Failed - pacman died from starvation")
    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch

#Part 3 Feedback
# I like the course so far, Friday written assignments are getting a lot harder, but the inclass discussions are really good.
# started off slow and had to change my A* and breadth search implementation once the heuristics were introduced.
# Maybe 6-8 hours?
# Thanks