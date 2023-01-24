from src.imports import *

class Node:
  def __init__(self, state, parent=None, name='child'):
    self.name = name
    self.state = state
    self.terminal = self.state.is_terminal()
    self.is_fully_expanded = self.terminal
    self.parent = parent
    self.children = {}
    self.visits = 0
    self.reward = 0

  def __str__(self) -> str:
    return str(self.state)

class MCTS:
  def search(self, state, iterations=100, c_param=1.4):
    self.root = Node(state, name="root")
    self.c_param = c_param

    for _ in range(iterations):
      node = self.select(self.root)
      winner = self.rollout(node.state)
      self.backpropagate(node, winner)
    
    # # Debugging
    # for child in self.root.children.values():
    #   print(self.root.visits, child.visits, child.reward)

    # Return the best child of the root node
    return self.best_child(self.root)

  def select(self, node):
    # Select the best child until a leaf node is reached
    while not node.terminal:
      if not node.is_fully_expanded:
        return self.expand(node)
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

  def rollout(self, state):
    # Play the game to completion by making random moves
    while not state.is_terminal():
      state = state.make_random_move()
    return state.get_winner()

  def backpropagate(self, node, winner):
    # Update the node and its ancestors with the result of the simulation
    while node is not None:
      node.visits += 1
      node.reward += winner
      node = node.parent

  def best_child(self, node):
    # Use the UCT formula to select the next child to explore
    best_score = -float("inf")
    best_child = None
    for child in node.children.values():
      current_player = -child.state.playerManager.player.token_value
      score = current_player * (child.reward / child.visits) + self.c_param * math.sqrt(math.log(node.visits) / child.visits)
      if score > best_score:
        best_score = score
        best_child = child

    return best_child

  def get_policy(self, node):
      pi = np.zeros((9,9))
      total_visits = sum([child.visits for child in node.children.values()])
      for child in node.children.values():
        move = 8 - np.where((node.state.matrix-child.state.matrix)!=0)[1][0]
        pi[node.state.active_index][move] = child.visits / total_visits
      return pi.ravel()