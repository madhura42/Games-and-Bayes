#!/usr/local/bin/python3

from logic_IJK import Game_IJK
import random
import sys
import math

# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game 
#
# This function should analyze the current state of the game and determine the 
# best move for the current player. It should then call "yield" on that move.

'''board: list of list of strings -> current state of the game
   current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
'''

def terminal(board):
   null_space_counter = 0
   for row in board:
      for col in row:
         if col == 'K' or col == 'k':
            return True
         
         if col == ' ':
            null_space_counter = null_space_counter + 1
   
   if null_space_counter == 0:
      return True
   return False

#----------------------------------------------------
#capital Human
#lowercase AI
def Utility(board, p1):
   score = 0
   for row in board:
      for col in row:
         if p1 == 'human':
            if col.isupper() :
               score = score - (ord(col.lower()) - 96)
         
            if col.islower():
               score = score + (ord(col) - 96)
         
         if p1 == 'ai':
            if col.isupper() :
               score = score + (ord(col.lower()) - 96)
         
            if col.islower():
               score = score - (ord(col) - 96)
         
         if col == ' ':
            score = score+1

   return score
#----------------------------------------------------

def Min(move, game: Game_IJK, depth, p1, alpha, beta):
   moves = ['U', 'D', 'L', 'R']
   game = game.makeMove(move)
   # print(move)
   depth = depth + 1
   board = game.getGame()
   # print(board)
   if(depth == 6):
      # print(depth, ' reached min')
      # print(Utility(board))
      return [Utility(board,p1), move]

   for m in moves:
      beta, move = min([beta,move], Max(m, game, depth, p1, alpha, beta))
      if alpha > beta:
         return [beta, move]
   return [beta,move]


def Max(move, game: Game_IJK, depth, p1, alpha, beta):
   moves = ['U', 'D', 'L', 'R']
   game = game.makeMove(move)
   # print(move)
   depth = depth + 1
   board = game.getGame()
   # print(board)
   if(depth == 6):
      # print(depth, ' reached min')
      # print(Utility(board))
      return [Utility(board,p1), move]

   for m in moves:
      alpha, move = max([alpha,move], Min(m, game, depth, p1, alpha, beta))
      if alpha > beta:
         return [alpha,move]
   return [alpha,move]

  
def next_move(game: Game_IJK):
   p1 = sys.argv[1]
   board = game.getGame()
   player = game.getCurrentPlayer()
   deterministic = game.getDeterministic()
   moves = ['U', 'D', 'L', 'R']
   depth = 0

   alpha = -math.inf
   beta = math.inf
   mv = ''
   to_be_done = ''

   unchanged_board = board

   for m in moves:
      alpha, mv = max([alpha,mv], Min(m, game, depth, p1, alpha, beta))
      to_be_done = mv
   return to_be_done


# ijk.py ai human det



