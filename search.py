closed_list = list()
number_expanded_nodes = 0
number_loops = 0
"""As specified in class, the Node class is merely a data-structure, it is independent from problem-specific logic, 
therefore, it is used for all the problems. 
"""
class Node:
    """class Node takes as arguments a state and if the state given does not correspond to the initial state, the parent
    and the action that lead to the generation of the node are also given as inputs. If the state corresponds to the
    initial state, the path cost and dept are set to 0, however if the parent (and action) was specified, it sets the
    cost and depth to be parent's cost and depth both + 1"""
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = 0
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
            self.path_cost = parent.path_cost + 1
    def print_solution(self):
        """class Node has a function print_solution that takes as input a node (generally the goal node not necessarily)
        and starts from the given node and loop back until reaching the initial state while appending each node along
        this path and at the end reverse the list to get the path form the initial node to the given node"""
        solution = list()
        node = self
        solution.insert(0, node)
        while node.parent:
            node = node.parent
            solution.insert(0, node)
        return solution

def expand(parent, problem):
    """the expand function takes as argument a node to expand and generate its successors by calling the successor
    function from the corresponding problem class (where we formulate the problem). It also increments the number of
    expanded nodes and prints it to the user so that the user can keep track of the number of expanded nodes. This
    function returns a list of the successors of the given node"""
    global closed_list
    global number_expanded_nodes
    closed_list.append(parent)
    number_expanded_nodes += 1
    print("Number of expanded nodes is:", number_expanded_nodes)
    successors = problem.successor_function(parent)
    return successors

def make_queue(element):
    """this function takes as input a node and create a list with the first element being the give node (used only to
    with the initial node to create the frontier list)"""
    frontier = list()
    frontier.append(element)
    return frontier

def queuing_fct(frontier, generated_nodes, strategy, problem):
    """the queuing function inserts nodes in the frontier in a way that is dependent on the search strategy used"""
    global closed_list
    global number_loops
    for node1 in generated_nodes:
        print("current generated node")
        print(node1.state)
        flag = 0
        for node2 in closed_list:
            """in this loop we are checking if the generated node is already in the closed list. If this is the case we
            increment the number of loops by 1 and we report it to the user"""
            """The loop checker detects cycles, we generally want to avoid cycles, it is therefore important to track them
            since it is an important metric.
            """

            if node1.state == node2.state:
                print("A loop has been detected")
                number_loops += 1
                print("Number of loops is: ", number_loops)
                flag = 1
        if flag == 0:
            if strategy == 1:
                """if the search strategy specified is BFS, newly generated nodes are inserted at the end of the list"""
                "As specified in class, BFS and DFS differ only in the position where the node is appended"
                frontier.append(node1)
            elif strategy == 2:
                """if the search strategy specified is BFS, newly generated nodes are inserted at the start of the list"""
                frontier.insert(0, node1)
            elif strategy == 3:
                """if the search strategy is GBFS we just append newly generated node at the end and after in code we 
                sort the nodes in the frontier in an increasing order based on the value returned by the heuristic 
                function from the problem formulation"""
                frontier.append(node1)
                frontier.sort(key=problem.heuristic_value)
                print("The heuristic value is: ")
                print(problem.heuristic_value(node1))
            elif strategy == 4:
                """if the search strategy is A* we sort the the nodes in the frontier in an increasing order based on the
                 value of the path cost + the heuristic value"""
                if len(frontier) == 0:
                    frontier.append(node1)
                else:
                    flag = 0
                    for i in range(len(frontier)):
                        if problem.heuristic_value(node1) + node1.path_cost <= problem.heuristic_value(frontier[i]) + frontier[i].path_cost:
                            frontier.insert(i, node1)
                            flag = 1
                            break
                    if flag == 0:
                        frontier.append(node1)
                print("The evaluation function value is: ")
                print(problem.heuristic_value(node1) + node1.path_cost)
    return frontier

def general_search(problem, strategy):
    """this is our general search engine. It first create a node corresponding to the initail state and gives it as
    argument to make_queue function"""
    initial_node = Node(problem.initial_state)
    frontier = make_queue(initial_node)
    limit = 500
    while len(frontier) > 0:
        """we first pop the first node from the frontier"""
        node1 = frontier.pop(0)
        print("node to expand")
        print(node1.state)
        if problem.goal_test(node1.state):
            """then we return the node if its state correspond to the goal state"""
            print("Total number of loops is: ", number_loops)
            print("Total number of nodes expanded is: ", number_expanded_nodes)
            return node1
        if number_expanded_nodes >= limit:
            """"if it is not the goal state we check first if the search is taking a long time by checking the number of
            expanded nodes and we give the user the choice to whether continue the search or stop it"""
            val = int(input("It seems that the search is taking a lot of time. If you want to continue press 1 otherwise press 0: "))
            if val == 0:
                print("Total number of loops is: ", number_loops)
                print("Total number of nodes expanded is: ", number_expanded_nodes)
                return None
            else:
                limit = limit + 500
        """the queuing function takes as parameters frontier, the successors generated by the expand function, the search
        strategy specified by the user, and the problem formulation.NOTE: the queuing function is only invoked if there
        are still nodes in the frontier to expand or if the user is still willing to continue the search"""
        frontier = queuing_fct(frontier, expand(node1, problem), strategy, problem)
    print("Total number of loops is: ", number_loops)
    print("Total number of nodes expanded is: ", number_expanded_nodes)
    return None

    "Important note, we decided to omit displaying the frontier, since it could contain thousands of nodes in some cases"
    
    " It will therefore clutter the console, that's why we didn't include it in the output"

