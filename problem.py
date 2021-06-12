from search import Node

class Problem:
    """this is the general class problem and from which we will be inheriting attributes and methods for the specific
    problem classes"""
    def __init__(self, initial_state, goal=None):
        self.initial_state = initial_state
        self.goal = goal

    def actions(self):
        raise NotImplementedError

    def successor_function(self):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return state in self.goal
        return state == self.goal

    def path_cost(self, c):  # maybe give it also the parent and the child
        raise NotImplementedError

    def heuristic_value(self, node):
        raise NotImplementedError


class ProblemMissionaries(Problem):
    """this is the problem class for missionaries and cannibals"""
    def __init__(self, initial_state, goal):
        """the state of this problem is represented as a list that has 3 values:
        the first value indicated the number of missionaries on the right side
        the second value represent the number of cannibals on the right side
        and the third value is 1 if the boat is at the right side and 0 if it is at the left side"""
        super().__init__(initial_state, goal)

    def actions(self):
        """this function returns the set of all actions available"""
        possible_actions = [[1, 0, 1], [0, 1, 1], [1, 1, 1], [2, 0, 1], [0, 2, 1]]
        return possible_actions

    def successor_function(self, parent):
        successors = list()
        all_actions = self.actions()
        if parent.state[2] == 1:
            """if the boat is the on right side we perform the actions by decreasing the the number of missionaries 
            and cannibals from the given state (which means that we transfer a number of people from the right side to 
            the left side"""
            for i in range(5):
                action = all_actions.pop()
                result = [parent.state[0] - action[0], parent.state[1] - action[1], parent.state[2] - action[2]]
                child = Node(result, parent, action)
                successors.append(child)
        if parent.state[2] == 0:
            """if the boat is the on right side we perform the actions by increasing the the number of missionaries 
            and cannibals from the given state (which means that we transfer a number of people from the left side to 
            the right side"""
            for i in range(5):
                action = all_actions.pop()
                result = [parent.state[0] + action[0], parent.state[1] + action[1], parent.state[2] + action[2]]
                child = Node(result, parent, action)
                successors.append(child)
        legal_successors = list()
        for new_node in successors:
            """in this loop we check for illegal states so that we can eliminate them. The checking is basically done by 
            checking if that both the number of missionaries and cannibals should be between 0 and 3 and then for the
            state to be considered legal the number of missionaries must be either 0 or 3 and if it is not the case it 
            should be equal to the number of missionaries"""
            if 0 <= new_node.state[0] <= 3 and 0 <= new_node.state[1] <= 3:
                if (new_node.state[0] == 3 or new_node.state[0] == 0) or (new_node.state[0] == new_node.state[1]):
                    legal_successors.append(new_node)
        return legal_successors

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c):  # step cost
        c += 1
        return c

    def heuristic_value(self, node):
        """the successor function we used returns the number of people on the right side"""
        return (node.state[0] + node.state[1]) - 1

class PegProblem(Problem):
    """this the problem class for the peg solitaire problem"""
    def __init__(self, initial_state, goal):
        """the states in this problem are represented with a list, i.e. we kind of flattened the space from 2D list to a
         1D list that has 49 locations (cells). Each location has one of the following values: 0, 1, or 2.
        0 means that there is no peg and the corresponding location corresponds to a location on the board.
        1 means that there is a peg on that location
        and 2 means that the corresponding location is not the part of board"""
        super().__init__(initial_state, goal)

    def successor_function(self, parent):
        successors = list()
        result = parent.state.copy()
        for i in range(49):
            if parent.state[i] == 1:
                """the successor function starts by checking for pegs one at a time"""
                if (i / 7) < 2: #if the peg is in the first 2 rows, i.e. it cannot jump over a peg that is above it(if exists)
                    if parent.state[i + 14] == 0:  #if the location that is below the below location of our peg is empty
                        if parent.state[i + 7] == 1: #if the location that is below our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 7] = 0
                            result[i + 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) + 1, i % 7])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i - 2] == 0: #if the location that is left to the left location of our peg is empty
                        if parent.state[i - 1] == 1: #if the location that is left to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 1] = 0
                            result[i - 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) - 1])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i + 2] == 0:  #if the location that is right ro the right location of our peg is empty
                        if parent.state[i + 1] == 1: #if the location that is right to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 1] = 0
                            result[i + 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) + 1])
                            successors.append(child)
                            result = parent.state.copy()
                if int(i / 7) > 4: #if the peg is in the last 2 rows, i.e. it cannot jump over a peg that is below it(if exists)
                    if parent.state[i - 14] == 0: #if the location that is above the above location of our peg is empty
                        if parent.state[i - 7] == 1:  #if the location that is above our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 7] = 0
                            result[i - 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) - 1, i % 7])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i - 2] == 0: #if the location that is left to the left location of our peg is empty
                        if parent.state[i - 1] == 1: #if the location that is left to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 1] = 0
                            result[i - 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) - 1])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i + 2] == 0:  #if the location that is right ro the right location of our peg is empty
                        if parent.state[i + 1] == 1: #if the location that is right to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 1] = 0
                            result[i + 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) + 1])
                            successors.append(child)
                            result = parent.state.copy()
                if (i % 7) < 2:
                    if parent.state[i - 14] == 0:  #if the location that is above the above location of our peg is empty
                        if parent.state[i - 7] == 1:  #if the location that is above our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 7] = 0
                            result[i - 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) - 1, i % 7])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i + 2] == 0:  #if the location that is right ro the right location of our peg is empty
                        if parent.state[i + 1] == 1: #if the location that is right to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 1] = 0
                            result[i + 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) + 1])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i + 14] == 0:  #if the location that is below the below location of our peg is empty
                        if parent.state[i + 7] == 1: #if the location that is below our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 7] = 0
                            result[i + 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) + 1, i % 7])
                            successors.append(child)
                            result = parent.state.copy()
                if (i % 7) > 4:
                    if parent.state[i - 14] == 0:  #if the location that is above the above location of our peg is empty
                        if parent.state[i - 7] == 1:  #if the location that is above our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 7] = 0
                            result[i - 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) - 1, i % 7])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i - 2] == 0: #if the location that is left to the left location of our peg is empty
                        if parent.state[i - 1] == 1: #if the location that is left to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 1] = 0
                            result[i - 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) - 1])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i + 14] == 0:  #if the location that is below the below location of our peg is empty
                        if parent.state[i + 7] == 1: #if the location that is below our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 7] = 0
                            result[i + 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) + 1, i % 7])
                            successors.append(child)
                            result = parent.state.copy()
                elif (2 <= int(i / 7) <= 4) and (2 <= i % 7 <= 4):
                    if parent.state[i - 14] == 0:  #if the location that is above the above location of our peg is empty
                        if parent.state[i - 7] == 1:  #if the location that is above our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 7] = 0
                            result[i - 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) - 1, i % 7])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i - 2] == 0: #if the location that is left to the left location of our peg is empty
                        if parent.state[i - 1] == 1: #if the location that is left to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i - 1] = 0
                            result[i - 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) - 1])
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i + 14] == 0:  #if the location that is below the below location of our peg is empty
                        if parent.state[i + 7] == 1: #if the location that is below our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 7] = 0
                            result[i + 14] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7) + 1, i % 7])
                            print(child.parent.state)
                            successors.append(child)
                            result = parent.state.copy()
                    if parent.state[i + 2] == 0:  #if the location that is right ro the right location of our peg is empty
                        if parent.state[i + 1] == 1: #if the location that is right to our peg has a peg then we jump over it
                            result[i] = 0
                            result[i + 1] = 0
                            result[i + 2] = 1
                            child = Node(result, parent, [int(i / 7), i % 7, int(i / 7), (i % 7) + 1])
                            successors.append(child)
                            result = parent.state.copy()
        return successors

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c):  # step cost
        c += 1
        return c

    def heuristic_value(self, node):
        #The manhattan distance heuristic is fully functional, and we decided to disregard it because it hindered the performance of A* and Greedy Best first Search
        #we tried Manhattan distance but it always overestimates the distance to the goal
        """man_dis = 0
        index = node.state.index(1)
        for i in range(49):
            if node.state[i] == 1:
                man_dis = man_dis + abs(int(i / 7) - int(index / 7)) + abs((i % 7) - (index % 7))
        man_dis_cen = 0
        for i in range(49):
            if node.state[i] == 1:
                vertical_distance = abs(int(i / 7) - 3)
                horizontal_distance = abs((i % 7) - 3)
                man_dis_cen = man_dis_cen + vertical_distance + horizontal_distance
        total = (man_dis + man_dis_cen) / 2""" 
        number_isolated_pegs = 0
        """our heuristic function computes the number of isolated pegs"""
        for i in range(49):
            if node.state[i] == 1:
                if 2 <= i <= 4:
                    if not (node.state[i + 1] == 1 or node.state[i - 1] == 1 or node.state[i + 7] == 1):
                        number_isolated_pegs += 1
                elif i == 14 or i == 21 or i == 28:
                    if not (node.state[i + 1] == 1 or node.state[i + 7] == 1 or node.state[i - 7] == 1):
                        number_isolated_pegs += 1
                elif i == 20 or i == 27 or i == 34:
                    if not (node.state[i - 1] == 1 or node.state[i + 7] == 1 or node.state[i - 7] == 1):
                        number_isolated_pegs += 1
                elif 44 <= i <= 46:
                    if not (node.state[i - 1] == 1 or node.state[i - 7] == 1 or node.state[i + 1] == 1):
                        number_isolated_pegs += 1
                else:
                    if not (node.state[i - 1] == 1 or node.state[i + 1] == 1 or node.state[i + 7] == 1 or node.state[i - 7] == 1):
                        number_isolated_pegs += 1
        return number_isolated_pegs

class Eight_PuzzleProblem(Problem):
    """this is the class problem for 8 puzzle"""
    def __init__(self, initial_state, goal):
        """the states are represented using a list that has 9 cells, each cell has the number of the tile and the blank
        tile is represented with 0"""
        super().__init__(initial_state, goal)

    def successor_function(self, parent):
        """the successor function starts with all the states and perform some checkings to eliminate actions that will
        yield to illegal states"""
        successors = list()
        possible_actions = ["up", "down", "left", "right"]
        index_blank = parent.state.index(0)
        result = parent.state.copy()
        if index_blank % 3 == 0: #if the blank is at the left (cell 0 3 or 6) we remove left action
            possible_actions.remove("left")
        if index_blank % 3 == 2:#if the blank is at the right (cell 2 5 or 7) we remove right action
            possible_actions.remove("right")
        if index_blank < 3: #if the blank is in the upper side (cell 0 1 or 2) we remove up action
            possible_actions.remove("up")
        if index_blank > 5: #if the blank is in the lower side (cell 6 7 or 8) we remove down action
            possible_actions.remove("down")
        for action in possible_actions:
            """in this loop we perform the remaining actions after eliminating actions that will generate illegal states"""
            if action == "up":
                temp = parent.state[index_blank]
                result[index_blank] = parent.state[index_blank - 3]
                result[index_blank - 3] = temp
                child = Node(result, parent, action)
                successors.append(child)
                result = parent.state.copy()
            if action == "down":
                temp = parent.state[index_blank]
                result[index_blank] = parent.state[index_blank + 3]
                result[index_blank + 3] = temp
                child = Node(result, parent, action)
                successors.append(child)
                result = parent.state.copy()
            if action == "left":
                temp = parent.state[index_blank]
                result[index_blank] = parent.state[index_blank - 1]
                result[index_blank - 1] = temp
                child = Node(result, parent, action)
                successors.append(child)
                result = parent.state.copy()
            if action == "right":
                temp = parent.state[index_blank]
                result[index_blank] = parent.state[index_blank + 1]
                result[index_blank + 1] = temp
                child = Node(result, parent, action)
                successors.append(child)
                result = parent.state.copy()
        return successors

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c):  # step cost
        c += 1
        return c
    def heuristic_value(self, node):
        value = 0
        """"our heuristic is a modified 'Manhattan Distance' in the sense that instead of adding the horizontal and 
        vertical distances of a cell between its current position and the goal position, it doubles the maxium value"""
        for i in range(8):
            horizontal_distance = abs((node.state.index(i+1)) % 3 - (self.goal.index(i+1)) % 3)
            vertical_distance = abs(int((node.state.index(i+1)) / 3) - int((self.goal.index(i+1)) / 3))
            value = value + 2 * max(vertical_distance, horizontal_distance)
        return value
