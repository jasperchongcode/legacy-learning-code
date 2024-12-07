import numpy as np
import torch
import math

class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None, prior=0, visit_count=0):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior # prior probability of selecting action
        
        self.children = []
        
        self.visit_count = visit_count
        self.value_sum = 0
        
    def is_fully_expanded(self):
        return len(self.children) > 0
    
    def select(self): # select the best child
        best_child = None
        best_ucb = -np.inf
        
        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb
                
        return best_child
    
    def get_ucb(self, child): # evaluate ucb (upper confidence bound) of child
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior
    
    def expand(self, policy): 
        for action, prob in enumerate(policy):
            if prob > 0: # if policyNet probablility is larger than 0
                # create child from next board state, and switch perspective
                child_state = self.state.copy()
                child_state = self.game.get_next_state(child_state, action, 1)
                child_state = self.game.change_perspective(child_state, player=-1)

                child = Node(self.game, self.args, child_state, self, action, prob)
                self.children.append(child)
                
        return child
            
    def backpropagate(self, value):
        # increase total value and visit count
        self.value_sum += value
        self.visit_count += 1
        
        value = self.game.get_opponent_value(value) # flip value and travel 1 move backwards (recursive)
        if self.parent is not None:
            self.parent.backpropagate(value)  


class MCTS:
    def __init__(self, game, args, model):
        self.game = game
        self.args = args
        self.model = model
        
    @torch.no_grad() # no gradient descent (as not training)
    def search(self, state):
        root = Node(self.game, self.args, state, visit_count=1) # create root node
        
        policy, _ = self.model( # call resNet to return policy and values 
            torch.tensor(self.game.get_encoded_state(state), device=self.model.device).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy() # scale all values to be between 0 and 1
        # adding dirilecht noise to encourage exploration https://stats.stackexchange.com/questions/322831/purpose-of-dirichlet-noise-in-the-alphazero-paper
        policy = (1 - self.args['dirichlet_epsilon']) * policy + self.args['dirichlet_epsilon'] \
            * np.random.dirichlet([self.args['dirichlet_alpha']] * self.game.action_size)
        
        valid_moves = self.game.get_valid_moves(state) # get all legal moves
        policy *= valid_moves # * do not know what this does
        policy /= np.sum(policy)
        root.expand(policy)
        
        for search in range(self.args['num_searches']): # loop over number of searches
            node = root # start at root node
            
            while node.is_fully_expanded():
                node = node.select() # travel down the highest ucb path until you get to a leaf
                
            # from the current state and the action taken to get there, get 1 for win 0 for draw or game still going, along with true or false for game running
            value, is_terminal = self.game.get_value_and_terminated(node.state, node.action_taken) 
            
            # flip value * not sure why 
            value = self.game.get_opponent_value(value)
            
            if not is_terminal: # if the game is not over in the leaf
                policy, value = self.model( # get policy and value from resNet
                    torch.tensor(self.game.get_encoded_state(node.state), device=self.model.device).unsqueeze(0)
                ) 
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy() # scale all values to be between 0 and 1
                valid_moves = self.game.get_valid_moves(node.state) 
                policy *= valid_moves #* still dont know
                policy /= np.sum(policy)
                
                value = value.item()
                
                node.expand(policy) # expand into child
                
            node.backpropagate(value) # backpropogate values
            
            
        action_probs = np.zeros(self.game.action_size) #* not sure
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
        