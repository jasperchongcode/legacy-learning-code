def sort_list():
    pass

class Node:
    def __init__(self, Frequency, Character=None, Parent=None, Chilren=None):
        self.Frequency = Frequency
        self.Character = Character
        self.Parent = Parent
        self.Children = None

    def is_leaf_node(self):
        return not self.Character == None

    def concatenate(self, TupleList):
        for Tuple in TupleList:
            Character, Frequency = Tuple
            self.Frequency += Frequency
            child = Node(Frequency, Character, self)
            self.Children.append(child)
        return self
    
class Tree:
    def __init__(self):
        pass

    def tuple_to_node(self, TupleList):
        nodeList = []
        for Tuple in TupleList:
            Character, Frequency = Tuple
            nodeList.append(Node(Frequency, Character, self))
        return nodeList
    
    def sort_list(self):
        
        

# need to have a list of nodes, filtered by node frequency
