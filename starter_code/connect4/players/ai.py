import time
import random
import copy
from turtle import shape
import numpy as np
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
        d=7
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
        if(board.shape[1]>=8 and board.shape[0]>=6):
            d=5
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
        #print("alphabeta is :",expmove)
        return expmove

        # python -m connect4.ConnectFour human ai connect4/initial_states/case3.txt --time 20
        # Do the rest of your implementation here
        raise NotImplementedError('Whoops I don\'t know what to do')

        """
        start position S_0: it specifies the initial state of the game before the very first move
        turn(s): a function that tells us which player (agent) is to make its move in the state s
        moves(s): a function returning all the moves legal in the state s
        result(s, a): the transition model specifying which state we get in by applying action a in the state s
        terminal(s): a function that identifies the states in which the game is over
        utility(s, p): the utility function assigning a numerical value to player p in terminal state s
        """

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
        
    

    def newchanceval(self,board,myval,opval,depth,mynum,opnum):
        #print("----------------- Entering CHANCE level depth: ",depth,"--------------------")
        if(depth==0):
            a = get_pts(opnum, board)
            # print("terminal CHANCE level : ",depth)
            return a
        #print("==CV=== ",state[1][opnum].get_int())
        valid_actions = self.get_valid_actions2(board,opnum,opval)
        #print("VA in chanceval: ",valid_actions)
        if(len(valid_actions)==0):
            return get_pts(opnum, board)
        lva = len(valid_actions)
        la = []
        j=int(lva/2)
        i=j-1
        if(lva%2==1): la.append(valid_actions[j])
        while(i>=0 and j<=lva-1):
            la.append(valid_actions[i])
            i-=1
            la.append(valid_actions[j])
            j+=1
        while(i>=0):
            la.append(valid_actions[i])
            i-=1
        while(j<=lva-1):
            la.append(valid_actions[j])
            j+=1               
        valid_actions = la
        v = 0
        for chance_move in valid_actions:
            #temp = copy.deepcopy(state)
            #print("************CHANCE MOVE is ",chance_move,"**************") # board,action,pval,pnum
            #temp_move,val = self.newmaxval(self.newgetState(chance_move,temp,opnum),depth-1,mynum,opnum)
            tboard = copy.deepcopy(board)
            tempnboard, tempopval = self.next_board(tboard,chance_move,opnum,opval)
            nboard = copy.deepcopy(tempnboard)
            opval = copy.deepcopy(tempopval)
            temp_move,val = self.newmaxval(nboard,myval,opval,depth-1,mynum,opnum)
            #print(chance_move,"  value from max state: == ",val)
            v = v+val
        v = v/len(valid_actions)
        return v


    def newmaxval(self, board,myval,opval,depth,mynum,opnum):
        #print("===========================================Entering here MAX level    depth: ",depth," =============================")
        if(depth==0):
            a = get_pts(mynum, board)
            return None,a
        #print("==MV=== ",state[1][opnum].get_int())
        valid_actions = self.get_valid_actions2(board,mynum,myval)
        #print("VA in maxval: ",valid_actions)
        if(len(valid_actions)==0):
            return None,get_pts(mynum, board)
        best_move,max_value= None,-1000   #(Integer.MIN_VALUE,False),Integer.MIN_VALUE
        lva = len(valid_actions)
        la = []
        j=int(lva/2)
        i=j-1
        if(lva%2==1): la.append(valid_actions[j])
        while(i>=0 and j<=lva-1):
            la.append(valid_actions[i])
            i-=1
            la.append(valid_actions[j])
            j+=1
        while(i>=0):
            la.append(valid_actions[i])
            i-=1
        while(j<=lva-1):
            la.append(valid_actions[j])
            j+=1               
        valid_actions = la
        for max_move in valid_actions:
            #temp = copy.deepcopy(state)
            #print("++++++++++++++++++++++ MAX MOVE is ",max_move," +++++++++++++++++++++++++++++++++++++")        
            #value = self.newchanceval(self.newgetState(max_move,temp,mynum),depth-1,mynum,opnum)
            tboard = copy.deepcopy(board)
            tempnboard, tempmyval = self.next_board(tboard,max_move,mynum,myval)
            nboard = copy.deepcopy(tempnboard)
            myval = copy.deepcopy(tempmyval)
            value = self.newchanceval(nboard,myval,opval,depth-1,mynum,opnum)
            # value = self.chanceval(state,depth-1,mynum,opnum)
            #print(max_value," === value from chance state: == ",value)
            if(value>max_value):
                best_move,max_value = max_move,value
                #print("Inside BM: ",best_move,max_value)
        #print("MV-------------",best_move,max_value)
        return best_move,max_value



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

        # start_time = time.clock()
        
        d=4
        # global action,is_popout
        mynum=1
        opnum=2
        if(self.player_number==2):
            mynum=2
            opnum=1
        board = state[0]
        myval = state[1][mynum].get_int()
        opval = state[1][opnum].get_int()
        #print("TIME given is :",self.time)
        if(board.shape[1]==12 and self.time<9):
            d=2
        elif(board.shape[1]==10 and board.shape[0]>=11):
            d=2
        elif(board.shape[1]==10 and board.shape[0]>=9 and self.time<16):
            d=2
        elif(board.shape[1]==10 and board.shape[0]==8 and self.time<10):
            d=2    

        # elif(board.shape[1]==11 and board.shape[0]==12):
        #     d=2
        # elif(self.time==20 and board.shape[1]==10):
        #     d=4
        # elif(board.shape[1]==10 and board.shape[0]>=10 and self.time<18):
        #     d=2
        # elif(board.shape[1]==10 and board.shape[0]<=10 and self.time>=18):
        #     d=4
        # elif(self.time>14 and board.shape[1]==9 and board.shape[0]==8):
        #     d=5
        # elif(self.time>7 and board.shape[1]==8 and board.shape[0]==8):
        #     d=5
        #elif(self.time>7 and board.shape[1]==11 and board.shape[0]==11)

    
        depth = d
        #print("depth: ",depth)
        # print("****************************************************")
        # print(opnum," ",get_valid_actions(opnum, state))
        # print(mynum," ",get_valid_actions(mynum, state))
        
        #expmove, val = self.newmaxval(state,d,mynum,opnum)

        expmove, val = self.newmaxval(board,myval,opval,depth,mynum,opnum)
        # print("expectimax is :",expmove)
        # global expmove # = (-1,False)
        '''
        while(self.time>20  and d<=2):
            #action, is_popout = self.dlexpectimax(self.player_number,state,True,d,mynum,opnum)
            expmove, val = self.maxval(state,d,mynum,opnum)
            d+=1
        '''
        # print("expectimax is :",expmove)
        # end_time = time.clock()
        # print("Insdide fnc: ",end_time-start_time)
        return expmove

        # python -m connect4.ConnectFour random ai connect4/initial_states/case4.txt --time 20
        raise NotImplementedError('Whoops I don\'t know what to do')
