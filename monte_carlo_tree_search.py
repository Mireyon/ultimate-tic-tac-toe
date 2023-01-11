import random
import math
import numpy as np

class Node:
  def __init__(self, state, parent=None, name='child'):
    self.name = name
    self.state = state
    self.is_fully_expanded = self.state.is_terminal()
    self.parent = parent
    self.children = {}
    self.visits = 0
    self.reward = 0

  def __str__(self) -> str:
    return str(self.state)

class MCTS:
  def search(self, state, iterations=100):
    self.root = Node(state, name="root")

    for _ in range(iterations):
      # Selection and Expansion
      node = self.select(self.root)
      # Simulation
      winner = self.rollout(node.state)
      # Backpropagation
      self.backpropagate(node, winner)
    
    # Return the best child of the root node
    return self.best_child(self.root)

  def select(self, node):
    # Select the best child until a leaf node is reached
    while not node.state.is_terminal():
      if not node.is_fully_expanded:
        # print("Not fully expanded")
        return self.expand(node)
      else:
        # print("Select best child")
        node = self.best_child(node)
    return node

  def expand(self, node):
    # Expand the node by adding a new child
    valid_moves = node.state.get_valid_moves()
    for move in valid_moves:
      if(f'{node.state.active_index} : {move}' not in node.children):
        new_state = node.state.make_move(move)
        new_node = Node(new_state, node)
        node.children[f'{node.state.active_index} : {move}'] = new_node

        if len(valid_moves) == len(node.children):
          node.is_fully_expanded = True
        return new_node

    #Debugging
    print("Not good if I arrived here")

  #To verify#####
  def rollout(self, state):
    # Play the game to completion by making random moves
    while np.any(state.get_valid_moves()):
      state = state.make_random_move()
    return state.get_score()

  def backpropagate(self, node, winner):
    # Update the node and its ancestors with the result of the simulation
    while node is not None:
      node.visits += 1
      node.reward += winner
      node = node.parent

  # To verify #####
  def best_child(self, node, c_param=1.4):
    # Use the UCB formula to select the next child to explore
    best_score = -float("inf")
    best_child = None
    for child in node.children.values():
      score = child.reward / child.visits + c_param * math.sqrt(math.log(node.visits) / child.visits)
      if score > best_score:
        best_score = score
        best_child = child
    return best_child