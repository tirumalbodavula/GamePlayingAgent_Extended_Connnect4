from ctypes import util
from email import utils
import random
import numpy as np
import time
import math
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here
    def  actions(self,state):
        actions=get_valid_actions(self.player_number,state)
        return actions

    def hypothesis_board(self,state,action):
                board,num_popouts=state
                pop=num_popouts[self.player_number].get_int()
                # print(pop,"pop")
                
                board_copy=board.copy()
                # time.sleep(3)
                column=action[0]
                if action[1]==False:
                        if 0 in board[:, column]:
                            for row in range(1, board.shape[0]):
                                update_row = -1
                                if board[row, column] > 0 and board[row - 1, column] == 0:
                                    update_row = row - 1
                                elif row == board.shape[0] - 1 and board[row, column] == 0:
                                    update_row = row
                                if update_row >= 0:
                                    board_copy[update_row, column] = self.player_number
                                    break
                        else:
                            print("error")
                else:
                    if 1 in board[:, column] or 2 in board[:, column]:
                        for r in range(board.shape[0] - 1, 0, -1):
                            # board[r, column] = board[r - 1, column]
                            board_copy[r, column] = board_copy[r - 1, column]
                        board_copy[0, column] = 0

                    else:
                        print("wrong move")
                    pop-=1
                state_new=[board_copy,num_popouts]
                return state_new

    def exp_value(self,state,layer):
        sum_util_value= 0.0
        util_val=0.0
        actions =get_valid_actions(self.player_number,state) #pass the other player's number
        p=1/(len(actions))
        for action in actions:
            new_state=self.hypothesis_board(state,action)
            util_val =self.value(new_state,True,layer+1)
            # print(util_val[0],"util value in min")
            sum_util_value+=util_val[0]
            print(sum_util_value,"sum")
        return sum_util_value*p
    def max_value_expectimax(self,state,layer):
        pre_util_val = -1000000
        actions=self.actions(state)
        for action in actions:
            new_state=self.hypothesis_board(state,action)
            util_val =self.value(new_state,False,layer+1)
            if util_val>pre_util_val:
                pre_util_val=util_val
                move=action
        return (util_val,move)
    def value(self,state,isMax,layer):
        valid_actions=get_valid_actions(self.player_number,state)
        if (layer >= 3) or (len(valid_actions)==0):
            return get_pts(self.player_number,state[0])
        if isMax:
            return self.max_value_expectimax(state,layer)
        else:
            return self.exp_value(state,layer)
          
   
   
    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        def max_value(state,alpha,beta,depth,valid_actions):
            pre_util_value=-10000000000
            move=random.choice(valid_actions)
            for action in valid_actions:
                util_value=alphabeta(self.hypothesis_board(state,action), depth-1, alpha, beta, False)
                if pre_util_value<util_value[1]:
                    pre_util_value=util_value[1]
                    move=action
                if pre_util_value >= beta:
                    break
                alpha=max(alpha,pre_util_value)
            return move,pre_util_value
        def min_value(state,alpha,beta,depth,valid_actions):
            pre_util_value=+10000000000
            move=random.choice(valid_actions)
            for action in valid_actions:
                util_value=alphabeta(self.hypothesis_board(state,action), depth-1, alpha, beta, True)
                if pre_util_value>util_value[1]:
                    pre_util_value=util_value[1]
                    move=action
                if pre_util_value <= alpha:
                    break
                beta=min(beta,pre_util_value)
            
            return move,pre_util_value 
        def alphabeta(state, depth, alpha, beta,  maximizingPlayer) -> Tuple[Tuple[int, bool], int]:
                        valid_actions = self.actions(state)
                        
                        if depth == 0 or len(valid_actions) == 0:
                            score = get_pts(self.player_number,state[0])
                            return (None, score)
                        if time.time()-v_ >=0.8*self.time :
                            return ( None, -np.inf)
                        if  maximizingPlayer:
                            return max_value(state,alpha,beta,depth,valid_actions)                  
                        else:
                            return min_value(state,alpha,beta,depth,valid_actions) 

        alpha = -100000000000
        beta = +1000000000000
        v_=time.time()
        for i in range(1,50):
            best_move=alphabeta(state,i, alpha, beta,True)
            if time.time()-v_ >=0.8*self.time :
                break
        intelligent_move=best_move[0]
        return intelligent_move
        
    
        # raise NotImplementedError('Whoops I don\'t know what to do')




    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        value=self.value(state,True,0)
        return value[1]
        # raise NotImplementedError('Whoops I don\'t know what to do')
