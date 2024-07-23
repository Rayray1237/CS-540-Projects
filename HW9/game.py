import random
import time
import copy


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        succList = self.succ(state)
        scoredSuccs = []
        for succ in succList:
            scoredSuccs.append([self.Max_Value(succ, 2, 0) + self.heuristic_game_value(succ), succ])
        scoredSuccs.sort(reverse = True)
        nextMove = scoredSuccs[0][1]


        drop_phase = False
        count = 0
        for row in range(5):
            for col in range(5):
                if (state[row][col] == 'r' or state[row][col] == 'b'):
                    count += 1
        if count < 8:
            drop_phase = True   
        
        move = []
        if not drop_phase:
            source = None
            moveTo = None
            for row in range(5):
                for col in range(5):
                    if state[row][col] == nextMove[row][col]:
                        pass
                    else:
                        if nextMove[row][col] == ' ':
                            source = (row, col)
                        else:
                            moveTo = (row, col)
            
            move = [moveTo, source]
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == nextMove[row][col]:
                        pass
                    else:
                        move = [(row, col)]

        return move


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for col in range(2):
            for i in range(0,2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col+1] == state[i+2][col+2] == state[i+3][col+3]:
                    return 1 if state[i][col] == self.my_piece else -1
        # TODO: check / diagonal wins
        for col in range(2):
            for i in range(3,5):
                if state[i][col] != ' ' and state[i][col] == state[i-1][col+1] == state[i-2][col+2] == state[i-3][col+3]:
                    return 1 if state[i][col] == self.my_piece else -1
        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col] == state[row][col+1] == state[row+1][col+1]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0  # no winner yet
        
    
    def succ(self, state):

        
        drop_phase = False
        count = 0
        for row in range(5):
            for col in range(5):
                if (state[row][col] == 'r' or state[row][col] == 'b'):
                    count += 1
        if count < 8:
            drop_phase = True

        succList = []
       
        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        newState = copy.deepcopy(state)
                        newState[row][col] = self.my_piece
                        succList.append(newState)
       
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        newState = copy.deepcopy(state)
                        for newRow in range(-1, 1, 1):
                            for newCol in range(-1, 1, 1):
                                if (row + newRow < 5 and row + newRow > -1 and col + newCol < 5 and col + newCol > -1):
                                    if (newState[row + newRow][col + newCol] == ' '):
                                        newState[row + newRow][col + newCol] = self.my_piece
                                        newState[row][col] = ' '
                                        succList.append(newState)

        return succList

    
    def succOther(self, state):

        
        drop_phase = False
        count = 0
        for row in range(5):
            for col in range(5):
                if (state[row][col] == 'r' or state[row][col] == 'b'):
                    count += 1
        if count < 8:
            drop_phase = True

        theirPiece = 'r'
        if self.my_piece == 'r':
            theirPiece = 'b'

        succList = []
      
        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        newState = copy.deepcopy(state)
                        newState[row][col] = theirPiece
                        succList.append(newState)
        
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == theirPiece:
                        newState = copy.deepcopy(state)
                        for newRow in range(-1, 1, 1):
                            for newCol in range(-1, 1, 1):
                                if (row + newRow < 5 and row + newRow > -1 and col + newCol < 5 and col + newCol > -1):
                                    if (newState[row + newRow][col + newCol] == ' '):
                                        newState[row + newRow][col + newCol] = theirPiece
                                        newState[row][col] = ' '
                                        succList.append(newState)

        return succList

    
    def heuristic_game_value(self, state):
        
        spaceScores = [[0, 0, 0, 0, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0.01, 0.02, 0.01, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0, 0, 0, 0]]

       
        stateVal = self.game_value(state)
        if stateVal != 0:
            return stateVal
       
        else:
            # TODO
            myScore = 0
            myFCount = 0
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        
                        myScore += spaceScores[row][col]

                        
                        byFriendly = False
                        for adjRow in range(-1, 1, 1):
                            for adjCol in range(-1, 1, 1):
                                if (row + adjRow < 5 and row + adjRow > -1 and col + adjCol < 5 and col + adjCol > -1):
                                    if state[row + adjRow][col + adjCol] == self.my_piece:
                                        byFriendly = True
                        if byFriendly:
                            myFCount += 1

            
            myAdjacency = 0
            if myFCount == 2:
                myAdjacency = 0.2
            elif myFCount == 3:
                myAdjacency = 0.5
            elif myFCount == 4:
                myAdjacency = 0.9

            myScore = myScore + myAdjacency
        return myScore

    
    def heuristic_game_value_other(self, state):
        
        spaceScores = [[0, 0, 0, 0, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0.01, 0.02, 0.01, 0], [0, 0.01, 0.01, 0.01, 0], [0, 0, 0, 0, 0]]

        theirPiece = 'r'
        if self.my_piece == 'r':
            theirPiece = 'b'

        
        stateVal = self.game_value(state)
        if stateVal != 0:
            return stateVal
        
        else:
            
            myScore = 0
            myFCount = 0
            for row in range(5):
                for col in range(5):
                    if state[row][col] == theirPiece:
                        
                        myScore += spaceScores[row][col]

                        
                        byFriendly = False
                        for adjRow in range(-1, 1, 1):
                            for adjCol in range(-1, 1, 1):
                                if (row + adjRow < 5 and row + adjRow > -1 and col + adjCol < 5 and col + adjCol > -1):
                                    if state[row + adjRow][col + adjCol] == theirPiece:
                                        byFriendly = True
                        if byFriendly:
                            myFCount += 1

            
            myAdjacency = 0
            if myFCount == 2:
                myAdjacency = 0.2
            elif myFCount == 3:
                myAdjacency = 0.5
            elif myFCount == 4:
                myAdjacency = 0.9

            myScore = myScore + myAdjacency
        return myScore

    
    def Max_Value(self, state, depth, count):
        stateVal = self.game_value(state)
        if (stateVal != 0 or count >= depth):
            if (stateVal == 0):
                return self.heuristic_game_value(state)
            else:
                return stateVal
        else:
            a = float('-inf')
            succList = self.succ(state)
            for aState in succList:
                a = max(a, self.Min_Value(aState, depth, count+1))

            return a

    
    def Min_Value(self, state, depth, count):
        stateVal = self.game_value(state)
        if (stateVal != 0 or count >= depth):
            if (stateVal == 0):
                return (-1 * self.heuristic_game_value_other(state))
            else:
                return stateVal
        else:
            b = float('inf')
            succList = self.succOther(state)
            for aState in succList:
                b = min(b, self.Max_Value(aState, depth, count+1))

            return b


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
