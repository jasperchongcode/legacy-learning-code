# turn a chess position into a 3d matrix
import pandas as pd
import numpy as np
import re
import gc
import chess
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F


board = chess.Board()

letter_to_number = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,}
number_to_letter = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',}

def layer_to_array(board, piece):
    s = str(board)
    s = re.sub(f'[^{piece}{piece.upper()} \n]', '.', s)
    s = re.sub(f'{piece}', '-1', s)
    s = re.sub(f'{piece.upper()}', '1', s)
    s = re.sub(f'\.', '0', s)
    board_array=[]
    for row in s.split("\n"):
        row = row.split(" ")
        row = [int(x) for x in row]
        board_array.append(row)
    return np.array(board_array)

def board_to_array(board):
    pieces = ['p', 'n', 'b', 'r', 'q', 'k']
    layers = []
    for piece in pieces:
        layer = layer_to_array(board, piece)
        layers.append(layer)
    board_array = np.stack(layers)
    return board_array

def move_to_array(move, board):

  board.push_san(move).uci()
  move = str(board.pop())

  from_output_layer = np.zeros((8,8))
  from_row = 8 - int(move[1])
  from_column = letter_to_number[move[0]]
  from_output_layer[from_row, from_column] = 1

  to_output_layer = np.zeros((8,8))
  to_row = 8 - int(move[3])
  to_column = letter_to_number[move[2]]
  to_output_layer[to_row, to_column] = 1

  return np.stack([from_output_layer, to_output_layer])

def create_move_list(s):
  return re.sub('\d*\. ','', s).split(' ')[:-1]

class ChessDataset(Dataset):

  def __init__(self, games):
    super(ChessDataset, self).__init__()
    self.games = games

  def __len__(self):
    return 40_000
    
  def __getitem__(self, index):
    game_i = np.random.randint(self.games.shape[0])
    random_game = self.games['AN'].values[game_i]
    moves = create_move_list(random_game)
    game_state_i = np.random.randint(len(moves)-1)
    next_move = moves[game_state_i]
    moves = moves[:game_state_i]
    board = chess.Board()
    for move in moves:
      board.push_san(move)
    x = board_to_array(board)
    y = move_to_array(next_move, board)
    if game_state_i % 2 == 1: # if its blacks move
      x *= -1
    return x, y
  
board = chess.Board()

print(board_to_array(board))