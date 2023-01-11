import random
import math

class Node:
  def __init__(self, state, parent=None):
    self.state = state
    self.parent = parent
    self.children = []
    self.visits = 0
    self.reward = 0

  def add_child(self, child_state):
    child = Node(child_state, self)
    self.children.append(child)
    return child

  def update(self, reward):
    self.visits += 1
    self.reward += reward

  def fully_expanded(self):
    # Check if all sub-boards in the state have been explored
    return len(self.children) == len(self.state.get_valid_moves())

  def rollout(self, state):
    # Play the game to completion by making random moves
    while state.get_valid_moves():
      state = state.make_random_move()
    return state.get_winner()

  def best_child(self, c_param=1.4):
    # Use the UCB formula to select the next child to explore
    best_score = -float("inf")
    best_child = None
    for child in self.children:
      score = child.reward / child.visits + c_param * math.sqrt(math.log(self.visits) / child.visits)
      if score > best_score:
        best_score = score
        best_child = child
    return best_child

class MCTS:
  def __init__(self, state):
    self.root = Node(state)

  def search(self, iterations):
    for _ in range(iterations):
      # Selection
      node = self.root
      while node.fully_expanded():
        node = node.best_child()

      # Expansion
      if node.state.get_valid_moves():
        move = random.choice(node.state.get_valid_moves())
        child_state = node.state.make_move(move)
        node = node.add_child(child_state)

      # Simulation
      winner = node.rollout(node.state)

      # Backpropagation
      while node is not None:
        node.update(winner)
        node = node.parent

  def best_move(self):
    # Select the child with the most visits
    best_score = -float("inf")
    best_move = None
    for child in self.root.children:
      if child.visits > best_score:
        best_score = child.visits
        best_move = child.state.last_move
    return best_move
