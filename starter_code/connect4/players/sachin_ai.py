import random
import numpy as np
import time
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
    def actions(self,state,player_num):
        actions=get_valid_actions(player_num,state)
        return actions
    def hypothesis_board(self,state,action):
            board,num_popouts=state
            # print("previous board")
            # print(board)
            print(action,"AcTION")
            # time.sleep(1)
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
                                board[update_row, column] = self.player_number
                                break
                    else:
                        print("error")
            else:
                if 1 in board[:, column] or 2 in board[:, column]:
                    for r in range(board.shape[0] - 1, 0, -1):
                        board[r, column] = board[r - 1, column]
                    board[0, column] = 0

                else:
                    print("wrong move")
                num_popouts[self.player_number].decrement()
            print("newboard")
            print(board)
            return state

    def exp_value(self,state,layer):
        util_val = 0
        self.player_number=2
        actions = get_valid_actions(self.player_number,state) #pass the other player's number
        print(actions)
        print(len(actions),"length of  actions")
        p=1/(len(actions))
        print(p,"probability")
        for action in actions:
            print(action)
            print(self.value(self.hypothesis_board(state,action),True,layer+1))
            util_val = util_val + p*self.value(self.hypothesis_board(state,action),True,layer+1)
        print(util_val,"finally util value for  min")
        return util_val
    def max_value_expectimax(self,state,layer):
        util_val = -1000000
        self.player_number=1
        actions = get_valid_actions(self.player_number,state)
        print(actions)
        move = 1
        for action in actions:
            util_val = max(util_val,self.value(self.hypothesis_board(state,action),False,layer+1))
        return (util_val,move)
    def value(self,state,isMax,layer):
        board=state[0]
        if  layer >= 3:
            if isMax:
                print(get_pts(self.player_number,board))
                return (get_pts(self.player_number,board))
            else:
                print(get_pts(self.player_number,board))
                return get_pts(self.player_number,board)
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
        raise NotImplementedError('Whoops I don\'t know what to do')

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
        print(self.player_number)#to see which player is playing first
        board,ispopout=state
        pop_moves={1:ispopout[1].get_int(),2:ispopout[2].get_int()}
        print(pop_moves)
        # valid_actions=get_valid_actions(self.player_number,state)
        if (self.player_number==1):
            check=True
        else:
            check=False
        result_move=self.value(state,check,0)
        time.sleep(0.2)

        return result_move[1]

        # raise NotImplementedError('Whoops I don\'t know what to do')
