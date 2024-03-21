import sys
from typing import Tuple, Dict
import numpy as np
from connect4.utils import get_valid_actions, Integer

import copy
from connect4.utils import get_pts, get_valid_actions, Integer
from typing import List, Tuple, Dict


def get_input() -> str:
    print('Enter your move: ')
    inp = sys.stdin.readline()
    inp = inp.replace('\n', '')
    return inp


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    @staticmethod
    def get_action(inp: str) -> Tuple[int, bool]:
        if inp[-1] == 'P':
            action = int(inp[:-1]), True
        else:
            action = int(inp), False
        return action

    def get_valid_actions2(self,board,player_number: int,pval) -> List[Tuple[int, bool]]:
        """
        :return: All the valid actions for player (with player_number) for the provided current state of board
        """
        valid_moves = []
        pop_out_left = pval
        n = board.shape[1]
        # Adding fill move
        for col in range(n):
            if 0 in board[:, col]:
                valid_moves.append((col, False))
        # Adding popout move
        if pop_out_left > 0:
            for col in range(n):
                if col % 2 == player_number - 1:
                    # First player is allowed only even columns and second player is allowed only odd columns
                    if board[:, col].any():
                        valid_moves.append((col, True))
        return valid_moves

    def next_board(self,board,action,pnum,pval):
        column = action[0]
        if action[1]==False:
            if 0 in board[:, column]:
                for row in range(0, board.shape[0]):
                    update_row = -1
                    if board[row, column] > 0 and board[row - 1, column] == 0:
                        update_row = row - 1
                    elif row == board.shape[0] - 1 and board[row, column] == 0:
                        update_row = row
                    if update_row >= 0:
                        board[update_row, column] = pnum
        else:
            rows=board.shape[0]
            for i in range(rows-1, -1, -1):
                if(board[i][column]==0): break
                else:
                    board[i][column]=board[i-1][column]
            board[0][column]=0
            pval-=1
        #print(board,pval)
        return board,pval

    def alphabeta(self, maximizingPlayer,board,myval,opval,depth,mynum,opnum,alpha,beta):
    
        # Terminating condition. i.e
        # leaf node is reached
    
        if maximizingPlayer:
            if depth == 0:
                a = get_pts(mynum, board)-get_pts(opnum,board)
                return None,a
            valid_actions = self.get_valid_actions2(board,mynum,myval)
            #print("VA in maximizingPlayer: ",valid_actions)
            if(len(valid_actions)==0):
                a = get_pts(mynum, board)-get_pts(opnum,board)
                return None,a
                
            plist = []
            notplist = []
            for i in range(0,len(valid_actions)):
                act = valid_actions[i]
                if(act[1]==True):
                    plist.append(act)
                else:
                    notplist.append(act)

            lva = len(notplist)
            la = []
            j=int(lva/2)
            i=j-1
            if(lva%2==1): la.append(notplist[j])
            while(i>=0 and j<=lva-1):
                if(mynum%2==0):
                    la.append(notplist[i])
                    i-=1
                    la.append(notplist[j])
                    j+=1
                else:
                    la.append(notplist[j])
                    j+=1
                    la.append(notplist[i])
                    i-=1
            while(i>=0):
                la.append(notplist[i])
                i-=1
            while(j<=lva-1):
                la.append(notplist[j])
                j+=1      
            for k in plist:
                la.append(k)         
            valid_actions = la
            best_move,max_value= None,-10000   #(Integer.MIN_VALUE,False),Integer.MIN_VALUE
            #print("CURRENT MAXI STATE ",board,"////",alpha," ",beta)
            for max_move in valid_actions:
                tboard = copy.deepcopy(board)
                tempnboard, tempmyval = self.next_board(tboard,max_move,mynum,myval)
                nboard = copy.deepcopy(tempnboard)
                myval = copy.deepcopy(tempmyval)
                #print(max_move," MYSELF ",nboard)
                temp_move,value = self.alphabeta(False,nboard,myval,opval,depth-1,mynum,opnum,alpha,beta)
                if(value>max_value):
                    best_move,max_value = max_move,value
                    #print("Inside ********MP****** : ",best_move,max_value)
                # if(max_value>=beta): return best_move,max_value
                alpha = max(alpha, max_value)
                if(beta<=alpha):
                    break
            return best_move,max_value
        
        else:
            if depth == 0:
                a = get_pts(opnum, board)-get_pts(mynum,board)
                return None,a
            valid_actions = self.get_valid_actions2(board,opnum,opval)
            #print("VA in NOTmaximizingPlayer: ",valid_actions)
            if(len(valid_actions)==0):
                a = get_pts(opnum, board)-get_pts(mynum,board)
                return None,a

            plist = []
            notplist = []
            for i in range(0,len(valid_actions)):
                act = valid_actions[i]
                if(act[1]==True):
                    plist.append(act)
                else:
                    notplist.append(act)

            lva = len(notplist)
            la = []
            j=int(lva/2)
            i=j-1
            if(lva%2==1): la.append(notplist[j])
            while(i>=0 and j<=lva-1):
                if(mynum%2==0):
                    la.append(notplist[i])
                    i-=1
                    la.append(notplist[j])
                    j+=1
                else:
                    la.append(notplist[j])
                    j+=1
                    la.append(notplist[i])
                    i-=1
            while(i>=0):
                la.append(notplist[i])
                i-=1
            while(j<=lva-1):
                la.append(notplist[j])
                j+=1      
            for k in plist:
                la.append(k)         
            valid_actions = la

            best_move,mini_value= None,100000   #(Integer.MIN_VALUE,False),Integer.MIN_VALUE
            #print("CURRENT MINI STATE ",board,"////",alpha," ",beta)
            for mini_move in valid_actions:
                tboard = copy.deepcopy(board)
                tempnboard, tempmyval = self.next_board(tboard,mini_move,opnum,opval)
                nboard = copy.deepcopy(tempnboard)
                opval = copy.deepcopy(tempmyval)
                #print(nboard," OPPONENT ",mini_move)
                temp_move, value = self.alphabeta(True,nboard,myval,opval,depth-1,mynum,opnum,alpha,beta)
                if(value<mini_value):
                    best_move,mini_value = mini_move,value
                    #print("Inside -----------NMP--------- : ",best_move,mini_value)
                #if(mini_value<=alpha): return best_move,mini_value
                beta = min(mini_value,beta)
                if(beta<=alpha):
                    break
            return best_move,mini_value

    def get_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state returns the next action
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
        d=8
        # global action,is_popout
        mynum=1
        opnum=2
        if(self.player_number==2):
            mynum=2
            opnum=1

        # print("************************CALLING MIN-MAX ALgorithm****************************")
        # print(opnum," ",get_valid_actions(opnum, state))
        # print(mynum," ",get_valid_actions(mynum, state))
        
        #expmove, val = self.newmaxval(state,d,mynum,opnum)
        board = state[0]
        myval = state[1][mynum].get_int()
        opval = state[1][opnum].get_int()
        depth = d
       # expmove, val = self.maxi(board,myval,opval,depth,mynum,opnum)
        #expmove, val = self.abmaxi(board,myval,opval,depth,mynum,opnum,-100000,100000)
        expmove, val = self.alphabeta(True,board,myval,opval,depth-1,mynum,opnum,-100000,100000)
        # print("expectimax is :",expmove)
        # global expmove # = (-1,False)
        '''
        while(self.time>20  and d<=2):
            #action, is_popout = self.dlexpectimax(self.player_number,state,True,d,mynum,opnum)
            expmove, val = self.maxval(state,d,mynum,opnum)
            d+=1
        '''
        print("human is :",expmove)
        return expmove

        """
        valid_actions = get_valid_actions(self.player_number, state)
        action = self.get_action(get_input())
        if action not in valid_actions:
            print('Invalid Move: Choose from: {}'.format(valid_actions))
            print('Turning to other player')
            # action = self.get_action(get_input())
        return action
        """
