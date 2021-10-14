# Name: Danielle Guedea
# Date: 03/09/2021
# Description: Portfolio Project - Program that can be used to play a game of Janggi.  Abides by all piece moves,
# keeps track of game status, and identifies when and who has won the game

def get_num_to_letter(number):
    """
    Returns letter equivalent of number for columns
    Used to transition spot on board to game-play moves
    """
    num_to_letter = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
        8: "i"
    }
    return num_to_letter[number]


def get_letter_to_num(letter):
    """
    Returns number equivalent of letter for columns
    Used to transition game-play moves to spot on board
    """
    letter_to_num = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
        "i": 8
    }
    return letter_to_num[letter]

class JanggiGame:
    """
    Where the game is played. This includes:
    1. Tracking game state: UNFINISHED, red_WON, blue_WON
    2. Determines if either player is in check
    3. Makes piece moves by communicating with Pieces class & sub classes
    4. Tracks whose turn it is
    5. Initializes and keeps track of where pieces are on the board
    Communicates with Pieces Class and Sub-Classes (different types of pieces)
    """

    def __init__(self):
        """
        Initializes game, including the starting board, state, turn
        """
        self._state = "UNFINISHED"
        self._last_turn = "red"
        self._board = [
            [Chariots("RCh1", "a1", "red", "Chariot"), Elephants("REl1", "b1", "red", "Elephant"),
             Horses("RHo1", "c1", "red", "Horse"), Guards("RGu1", "d1", "red", "Guard"), "",
             Guards("RGu2", "f1", "red", "Guard"), Elephants("REl2", "g1", "red", "Elephant"),
             Horses("RHo2", "h1", "red", "Horse"), Chariots("RCh2", "i1", "red", "Chariot")],
            ["", "", "", "", Generals("RGen", "e2", "red", "General"), "", "", "", ""],
            ["", Cannons("RCa1", "b3", "red", "Cannon"), "", "", "", "", "",
             Cannons("RCa2", "h3", "red", "Cannon"), ""],
            [Soldiers("RSo1", "a4", "red", "Soldier"), "",
             Soldiers("RSo2", "c4", "red", "Soldier"), "",
             Soldiers("RSo3", "e4", "red", "Soldier"), "",
             Soldiers("RSo4", "g4", "red", "Soldier"), "",
             Soldiers("RSo5", "i4", "red", "Soldier")],
            ["", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", ""],
            [Soldiers("BSo1", "a7", "blue", "Soldier"), "",
             Soldiers("BSo2", "c7", "blue", "Soldier"), "",
             Soldiers("BSo3", "e7", "blue", "Soldier"), "",
             Soldiers("BSo4", "g7", "blue", "Soldier"), "",
             Soldiers("BSo5", "i7", "blue", "Soldier")],
            ["", Cannons("BCa1", "b8", "blue", "Cannon"), "", "", "", "", "",
             Cannons("BCa2", "h8", "blue", "Cannon"), ""],
            ["", "", "", "", Generals("BGen", "e9", "blue", "General"), "", "", "", ""],
            [Chariots("BCh1", "a10", "blue", "Chariot"),
             Elephants("BEl1", "b10", "blue", "Elephant"),
             Horses("BHo1", "c10", "blue", "Horse"), Guards("BGu1", "d10", "blue", "Guard"), "",
             Guards("BGu2", "f10", "blue", "Guard"), Elephants("BEl2", "g10", "blue", "Elephant"),
             Horses("BHo2", "h10", "blue", "Horse"), Chariots("BCh2", "i10", "blue", "Chariot")]]

    def get_game_state(self):
        """
        Returns game state
        Can be UNFINISHED, RED_WON, or BLUE_WON
        """
        return self._state

    def set_state(self, game_state):
        """
        Updates game state to either -
        UNFINISHED, RED_WON or BLUE_WON
        """
        self._state = game_state

    def set_last_turn(self, turn):
        """
        Sets last turn to who has gone last
        Used to determine who should make a move next
        """
        self._last_turn = turn

    def get_item_from_board(self, column, row):
        """
        Returns object that is in that space on the board
        Communicates with Pieces objects
        """
        return self._board[row][column]

    def get_last_turn(self):
        """
        Returns object that is in that space on the board
        Communicates with Pieces objects
        """
        return self._last_turn

    def make_move(self, current_space, move_space):
        """
        Moves player's piece
        1. Must be players turn
        2. Must be a legal move
        3. Game must not be won
        4. Determines if someone has won the game (by capturing opponents General)
        Communicates with Pieces class / sub-classes for piece information
        Outputs: True if move is legal and False if not
        """

    # Translate alphabetical move space to numerical
        current_column = current_space[0]
        current_column_num = get_letter_to_num(current_column)
        current_row = int(current_space[1:]) - 1
        move_column = move_space[0]
        move_column_num = get_letter_to_num(move_column)
        move_row = int(move_space[1:]) - 1

    # Piece that is in the current spot being played
        item = self.get_item_from_board(int(current_column_num), int(current_row))

    # Check if game is not won
        if self.get_game_state() != 'UNFINISHED':
            return False
    # Check if current space is not empty
        elif item == '':
            return False
    # Check if it is their turn
        elif item != "" and item.get_color() == self.get_last_turn():
            return False
    # Check if passing turn, returns False if passing and General is in check
        elif current_space == move_space:
            if self.is_in_check(item.get_color()):
                return False
            self.set_last_turn(item.get_color)
            return True
    # Check if own General is in Check, if so, check if checkmated.  If not, General must be making the move
        elif self.is_in_check(item.get_color()):
            if self.is_checkmated(item.get_color()):
                if item.get_color().lower() == 'blue':
                    self.set_state("RED_WON")
                    return False
                if item.get_color().lower() == 'red':
                    self.set_state("BLUE_WON")
                    return False
            # If in check and not checkmated, simulate move and check if general is still in check
            else:
                piece_moved = self.get_item_from_board(move_column_num, move_row)
                self._board[move_row][move_column_num] = item
                self._board[current_row][current_column_num] = ""
                if self.is_in_check(item.get_color()):
                    self._board[move_row][move_column_num] = piece_moved
                    self._board[current_row][current_column_num] = item
                    return False
                self.set_last_turn(item.get_color())
                return True
    # General is not in check, simulate move (if legal) and ensure it does not put the general in check
        elif move_space in item.get_legal_move(current_column_num, current_row, self.get_board()):
            # Check first if they capture the general on the move
            # Make move
            piece_in_move = self.get_item_from_board(move_column_num, move_row)
            self._board[move_row][move_column_num] = item
            self._board[current_row][current_column_num] = ""
            # Check if move makes own General in check, if it does, do not make move and return False
            if self.is_in_check(item.get_color()):
                self._board[move_row][move_column_num] = piece_in_move
                self._board[current_row][current_column_num] = item
                return False
            # If it does not put General in check, move made and set last turn == player turn
            self.set_last_turn(item.get_color())
            return True
    # Otherwise, the move is not legal and return false
        else:
            return False

    def is_checkmated(self, color):
        """
        Checks if General is checkmated and therefore opposing player wins game
        Checkmate is when a General cannot make a move that allows it to escape check
        """
        general_moves = []
        opponent_moves = []

        # Get list of opponents moves
        row_count = 0
        for rows in self._board:
            column_count = 0
            for item in rows:
                if item != "" and item.get_color().lower() != color.lower():
                    for move in item.get_legal_move(column_count, row_count, self.get_board()):
                        opponent_moves.append(move)
                column_count += 1
            row_count += 1

        # Get list of general's legal moves
        row_count = 0
        for lists in self._board:
            column_count = 0
            for item in lists:
                if item != "" and item.get_color().lower() == color.lower() and item.get_type().lower() == 'general':
                    for move in item.get_legal_move(column_count, row_count, self.get_board()):
                        general_moves.append(move)
                column_count += 1
            row_count += 1

        # If a space in general's legal moves == space in opponents legal moves, general is checkmated
        for space in general_moves:
            if space not in opponent_moves:
                return False

        return True

    def is_in_check(self, color):
        """
        Returns true if color is in check and false if not
        Checks each piece and determines if one of their legal moves includes the spot
        that contains the general
        Outputs: True if color is in check and False if not
        """
        # Looks at opponent pieces and sees if a move includes the current players general
        row_count = 0
        for lists in self._board:
            column_count = 0
            for item in lists:
                # look at opponents pieces
                if item != "" and item.get_color().lower() != color.lower():
                    # gather opponents legal moves of all players
                    for piece in item.get_legal_move(column_count, row_count, self.get_board()):
                        current_column = piece[0]
                        current_column_num = get_letter_to_num(current_column)
                        current_row = int(piece[1:]) - 1
                        # if a legal move has the general, it is in check
                        if self._board[current_row][current_column_num] != "" and\
                                self._board[current_row][current_column_num].get_type().lower() == "general" and\
                                self._board[current_row][current_column_num].get_color().lower() == color.lower():
                            return True
                column_count += 1
            row_count += 1
        return False

    def get_board(self):
        """
        Returns game board
        """
        return self._board

    def print_board(self):
        """
        Prints out board
        Used primarily for testing purposes
        """
        columns = [' a  ', " b  ", " c  ", " d  ", " e  ", " f  ", " g  ", " h  ", " i  "]

        print("  ", columns)
        first_row = [x.get_name() if x != "" else "    " for x in self._board[0]]
        print("1 ", first_row)
        second_row = [x.get_name() if x != "" else "    " for x in self._board[1]]
        print("2 ", second_row)
        third_row = [x.get_name() if x != "" else "    " for x in self._board[2]]
        print("3 ", third_row)
        four_row = [x.get_name() if x != "" else "    " for x in self._board[3]]
        print("4 ", four_row)
        five_row = [x.get_name() if x != "" else "    " for x in self._board[4]]
        print("5 ", five_row)
        six_row = [x.get_name() if x != "" else "    " for x in self._board[5]]
        print("6 ", six_row)
        seven_row = [x.get_name() if x != "" else "    " for x in self._board[6]]
        print("7 ", seven_row)
        eight_row = [x.get_name() if x != "" else "    " for x in self._board[7]]
        print("8 ", eight_row)
        nine_row = [x.get_name() if x != "" else "    " for x in self._board[8]]
        print("9 ", nine_row)
        ten_row = [x.get_name() if x != "" else "    " for x in self._board[9]]
        print("10", ten_row)


class Pieces:
    """
    Pieces class has sub-classes for each of the different pieces on the board
    Holds common characteristics of pieces, including:
    1. Color
    2. Name of piece
    3. Type of piece (General, Guard, etc)

    Has common functions that are used by multiple pieces to output legal moves
    Communicates:
    1. Lists of legal moves per piece with JanggiGame class
    2. Characteristics of each piece with JanggiGame class
    """

    def __init__(self, name, place, color, type):
        """
        Initializes piece
        Including: Piece nickname, type, color and min/max board rows and columns
        """
        self._name = name
        self._type = type
        self._place = place
        self._color = color
        self._min_column = 0
        self._max_column = 8
        self._min_row = 0
        self._max_row = 9

    def get_name(self):
        """
        Returns piece name
        Makes for easier identification of pieces
        """
        return self._name

    def get_color(self):
        """
        Returns piece color
        """
        return self._color

    def get_type(self):
        """
        Returns the type of piece being played
        """
        return self._type

    def general_guard_moves(self, column, row, board):
        """
        Returns list of general and guard legal moves
        Only called by General and Guard pieces
        Uses same logic for both since they can both make the same moves
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """
        legal_moves = []

        # Since general and guards can only move in the fortress, this outputs all legal moves in that space
        # Diagonal moves are 'hardcoded'
        if self.get_color() == "blue":
            if column != 4 or row != 8:
                if board[8][4] == "" or board[8][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(9))
            if column == 3 and row == 7:
                if board[7][4] == "" or board[7][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(8))
                if board[8][3] == "" or board[8][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(9))
            if column == 4 and row == 7:
                if board[7][3] == "" or board[7][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(8))
                if board[7][5] == "" or board[7][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(8))
            if column == 5 and row == 7:
                if board[7][4] == "" or board[7][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(8))
                if board[8][5] == "" or board[8][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(9))
            if column == 3 and row == 8:
                if board[7][3] == "" or board[7][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(8))
                if board[9][3] == "" or board[9][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(10))
            if column == 4 and row == 8:
                col = 3
                for spot in board[7][3:6]:
                    if spot == "" or spot.get_color() != self.get_color():
                        legal_moves.append(get_num_to_letter(col) + str(8))
                    col += 1
                col = 3
                for spot in board[8][3:6]:
                    if spot == "" or spot.get_color() != self.get_color():
                        legal_moves.append(get_num_to_letter(col) + str(9))
                    col += 1
                col = 3
                for spot in board[9][3:6]:
                    if spot == "" or spot.get_color() != self.get_color():
                        legal_moves.append(get_num_to_letter(col) + str(10))
                    col += 1
            if column == 5 and row == 8:
                if board[7][5] == "" or board[7][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(8))
                if board[9][5] == "" or board[9][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(10))
            if column == 3 and row == 9:
                if board[8][3] == "" or board[8][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(9))
                if board[9][4] == "" or board[9][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(10))
            if column == 4 and row == 9:
                if board[9][3] == "" or board[9][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(10))
                if board[9][5] == "" or board[9][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(10))
            if column == 5 and row == 9:
                if board[9][4] == "" or board[9][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(10))
                if board[8][5] == "" or board[8][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(9))

        if self.get_color() == "red":
            if column != 4 or row != 1:
                if board[1][4] == "" or board[1][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(2))
            if column == 3 and row == 0:
                if board[0][4] == "" or board[0][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(1))
                if board[1][3] == "" or board[1][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(2))
            if column == 4 and row == 0:
                if board[0][3] == "" or board[0][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(1))
                if board[0][5] == "" or board[0][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(1))
            if column == 5 and row == 0:
                if board[0][4] == "" or board[0][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(1))
                if board[1][5] == "" or board[1][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(2))
            if column == 3 and row == 1:
                if board[0][3] == "" or board[0][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(1))
                if board[2][3] == "" or board[2][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(3))
            if column == 4 and row == 1:
                col = 3
                for spot in board[0][3:6]:
                    if spot == "" or spot.get_color() != self.get_color():
                        legal_moves.append(get_num_to_letter(col) + str(1))
                    col += 1
                col = 3
                for spot in board[1][3:6]:
                    if spot == "" or spot.get_color() != self.get_color():
                        legal_moves.append(get_num_to_letter(col) + str(2))
                    col += 1
                col = 3
                for spot in board[2][3:6]:
                    if spot == "" or spot.get_color() != self.get_color():
                        legal_moves.append(get_num_to_letter(col) + str(3))
                    col += 1
            if column == 5 and row == 1:
                if board[0][5] == "" or board[0][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(1))
                if board[2][5] == "" or board[2][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(3))
            if column == 3 and row == 2:
                if board[1][3] == "" or board[1][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(2))
                if board[2][4] == "" or board[2][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(3))
            if column == 4 and row == 2:
                if board[2][3] == "" or board[2][3].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(3) + str(3))
                if board[2][5] == "" or board[2][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(3))
            if column == 5 and row == 2:
                if board[2][4] == "" or board[2][4].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(4) + str(3))
                if board[1][5] == "" or board[1][5].get_color() != self.get_color():
                    legal_moves.append(get_num_to_letter(5) + str(2))

        return legal_moves


class Soldiers(Pieces):
    """
    Inherits from Pieces Class
    Contains unique rules for Solider pieces
    1. Move Rules: one space forward, left or right
    2. If in fortress, can move diagnonally forwards towards opponent
    Communicates legal moves with JanggiGame class
    """

    def right_left_move(self, column, row, board):
        """
        Adds right and left moves to soldier pieces
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """
        column_p1 = int(column) + 1
        column_m1 = int(column) - 1
        soldier_legal_moves = []

        # Move right
        if column_p1 <= self._max_column and row >= self._min_row:
            if board[row][column_p1] == "" \
                    or board[row][column_p1].get_color != self.get_color():
                soldier_legal_moves.append(get_num_to_letter(column_p1) + str(row + 1))
        # Move left
        if column_m1 >= self._min_column and row >= self._min_row:
            if board[row][column_m1] == "" \
                    or board[row][column_m1].get_color != self.get_color():
                soldier_legal_moves.append(get_num_to_letter(column_m1) + str(row + 1))

        return soldier_legal_moves

    def get_legal_move(self, column, row, board):
        """
        Returns list of valid moves for Soldier
        Column and Row is where the piece currently is
        Takes into account piece color to understand if they should move up or down
        and what fortress they can be in
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """

        soldier_legal_moves = []

        current_space_board = str(get_num_to_letter(column)) + str(row + 1)
        row_p1 = int(row) + 1
        row_m1 = int(row) - 1


        if self.get_color() == 'blue':
            # fortress moves
            if row == 2 and (column == 3 or column == 5):
                if board[1][4] == "" or board[1][4].get_color() != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(4) + str(2))
            if row == 1 and column == 4:
                if board[0][3] == "" or board[0][3].get_color() != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(3) + str(1))
                if board[0][5] == "" or board[0][5].get_color() != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(5) + str(1))
            # blue can only go down in row #
            if row_m1 >= self._min_row and self._min_column <= column <= self._max_column:
                if board[row_m1][column] == "" \
                        or board[row_m1][column] != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(column) + str(row_m1 + 1))
            for move in self.right_left_move(column, row, board):
                soldier_legal_moves.append(move)


        if self.get_color() == "red":
            # fortress moves
            if row == 7 and (column == 3 or column == 5):
                if board[8][4] == "" or board[8][4].get_color() != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(4) + str(9))
            if row == 8 and column == 4:
                if board[9][3] == "" or board[9][3].get_color() != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(3) + str(10))
                if board[9][5] == "" or board[9][5].get_color() != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(5) + str(10))
            # red can only go up in row #
            if row_p1 >= self._min_row and self._min_column <= column <= self._max_column:
                if board[row_p1][column] == "" \
                        or board[row_p1][column] != self.get_color():
                    soldier_legal_moves.append(get_num_to_letter(column) + str(row_p1 + 1))
            for move in self.right_left_move(column, row, board):
                soldier_legal_moves.append(move)

        return soldier_legal_moves


class Generals(Pieces):
    """
    Inherits from Pieces Class
    Contains unique rules for General pieces
    1. Cannot leave fortress
    2. Move Rules: along any line within fortress (all directions)
    Communicates legal moves with JanggiGame class
    """

    def get_legal_move(self, column, row, board):
        """
        Returns list of valid moves for General
        column and row is where the piece currently is
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """
        return self.general_guard_moves(column, row, board)


class Guards(Pieces):
    """
    Inherits from Pieces Class
    Contains unique rules for Guard pieces
    1. Move Rules: one space within fortress (all directions)
    Communicates legal moves with JanggiGame class
    """

    def get_legal_move(self, column, row, board):
        """
        Returns list of valid moves for Guard
        Column and Row is where the piece currently is
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """
        return self.general_guard_moves(column, row, board)


class Chariots(Pieces):
    """
    Inherits from Pieces Class
    Contains unique rules for Chariot pieces
    1. Move Rules: unlimited spaces on board vertically or horizontally
    2. If in fortress, can move diagonally in a straight line
    Communicates legal moves with JanggiGame class
    """

    def diagonal_moves(self, column_1, row_1, column_2, row_2, board, chariot_legal_moves):
        """
        Adds diagonal moves to legal moves when Chariot is in either fortress
        Inputs: Possible diagonal move coordinates (column_1, row_1, column_2, row_2)
                Board, and list of chariot_legal_moves
        Outputs: List of all possible diagonal moves from current space if in fortress
        """
        # calculates fortress diagonal moves
        if board[row_1][column_1] == "":
            chariot_legal_moves.append(get_num_to_letter(column_1) + str(row_1 + 1))
            if board[row_2][column_2] == "" or board[row_2][column_2].get_color() != self.get_color():
                chariot_legal_moves.append(get_num_to_letter(column_2) + str(row_2 + 1))
        elif board[row_1][column_1].get_color() != self.get_color():
            chariot_legal_moves.append(get_num_to_letter(column_1) + str(row_1 + 1))

        return

    def get_legal_move(self, column, row, board):
        """
        Returns list of valid moves for Chariot
        column and row is where the piece currently is
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """
        chariot_legal_moves = []

        # If in fortress, gets diagonal moves available
        # Center space in red fortress
        if column == 4 and row == 8:
            col = 3
            for spot in board[7][3:6]:
                if spot == "" or spot.get_color() != self.get_color():
                    chariot_legal_moves.append(get_num_to_letter(col) + str(8))
                col += 1
            col = 3
            for spot in board[8][3:6]:
                if spot == "" or spot.get_color() != self.get_color():
                    chariot_legal_moves.append(get_num_to_letter(col) + str(9))
                col += 1
            col = 3
            for spot in board[9][3:6]:
                if spot == "" or spot.get_color() != self.get_color():
                    chariot_legal_moves.append(get_num_to_letter(col) + str(10))
                col += 1
        # Center space in blue fortress
        if column == 4 and row == 1:
            col = 3
            for spot in board[0][3:6]:
                if spot == "" or spot.get_color() != self.get_color():
                    chariot_legal_moves.append(get_num_to_letter(col) + str(1))
                col += 1
            col = 3
            for spot in board[1][3:6]:
                if spot == "" or spot.get_color() != self.get_color():
                    chariot_legal_moves.append(get_num_to_letter(col) + str(2))
                col += 1
            col = 3
            for spot in board[2][3:6]:
                if spot == "" or spot.get_color() != self.get_color():
                    chariot_legal_moves.append(get_num_to_letter(col) + str(3))
                col += 1
        # red corners
        if column == 3 and row == 0:
            self.diagonal_moves(4, 1, 5, 2, board, chariot_legal_moves)
        if column == 5 and row == 0:
            self.diagonal_moves(4, 1, 3, 2, board, chariot_legal_moves)
        if column == 3 and row == 2:
            self.diagonal_moves(4, 1, 5, 0, board, chariot_legal_moves)
        if column == 5 and row == 2:
            self.diagonal_moves(4, 1, 3, 0, board, chariot_legal_moves)
        # blue corners
        if column == 3 and row == 7:
            self.diagonal_moves(4, 8, 5, 9, board, chariot_legal_moves)
        if column == 5 and row == 7:
            self.diagonal_moves(4, 8, 3, 9, board, chariot_legal_moves)
        if column == 3 and row == 9:
            self.diagonal_moves(4, 8, 5, 7, board, chariot_legal_moves)
        if column == 5 and row == 9:
            self.diagonal_moves(4, 8, 3, 7, board, chariot_legal_moves)

        # Checks horizontally
        # Checks spaces to the right, if it comes across another piece it stops adding to legal moves
        for i in range(column + 1, self._max_column + 1):
            if board[row][i] == '':
                chariot_legal_moves.append(get_num_to_letter(i) + str(row + 1))
            elif board[row][i].get_color() != self.get_color():
                chariot_legal_moves.append(get_num_to_letter(i) + str(row + 1))
                break
            else:
                break

        # Checks spaces to the left, if it comes across another piece it stops adding to legal moves
        for i in range(column - 1, -1, -1):
            if board[row][i] == '':
                chariot_legal_moves.append(get_num_to_letter(i) + str(row + 1))
            elif board[row][i].get_color() != self.get_color():
                chariot_legal_moves.append(get_num_to_letter(i) + str(row + 1))
                break
            else:
                break

        # Checks vertically
        # Checks up, if it comes across another piece it stops adding to legal moves
        for i in range(row - 1, -1, -1):
            if board[i][column] == '':
                chariot_legal_moves.append(get_num_to_letter(column) + str(i + 1))
            elif board[i][column].get_color() != self.get_color():
                chariot_legal_moves.append(get_num_to_letter(column) + str(i + 1))
                break
            else:
                break

        # Checks down, if it comes across another piece it stops adding to legal moves
        for i in range(row + 1, self._max_row + 1):
            if board[i][column] == '':
                chariot_legal_moves.append(get_num_to_letter(column) + str(i + 1))
            elif board[i][column].get_color() != self.get_color():
                chariot_legal_moves.append(get_num_to_letter(column) + str(i + 1))
                break
            else:
                break

        return chariot_legal_moves


class Horses(Pieces):
    """
    Inherits from Pieces Class
    Contains unique rules for Horse pieces
    1.  Move Rules: one space forward then diagonally OR
                    one space sideways then diagonally
    2. Can be blocked by another piece (cannot jump over a piece)
    Communicates legal moves with JanggiGame class
    """

    def get_legal_move(self, column, row, board):
        """
        Returns list of valid moves for Horse
        column and row is where the piece currently is
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """
        horse_legal_moves = []
        # right
        if (column + 1 <= self._max_column) and board[row][column+1] == "":
            # right and up
            if (column + 2 <= self._max_column) and (row - 1 >= self._min_row) and\
                    (board[row-1][column+2] == "" or board[row-1][column+2].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column+2) + str(row))
            # right and down
            if (column + 2 <= self._max_column) and (row + 1 <= self._max_row) and\
                    (board[row+1][column+2] == "" or board[row+1][column+2].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column + 2) + str(row+2))
        #  left
        if (column - 1 >= self._min_column) and board[row][column-1] == "":
            # left and up
            if (column - 2 >= self._min_column) and (row - 1 >= self._min_row) and \
                    (board[row - 1][column - 2] == "" or board[row - 1][column - 2].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column - 2) + str(row))
            # left and down
            if (column - 2 >= self._min_column) and (row + 1 <= self._max_row) and \
                    (board[row + 1][column - 2] == "" or board[row + 1][column - 2].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column - 2) + str(row + 2))
        # down
        if (row + 1 <= self._max_row) and board[row+1][column] == "":
            # down and right
            if (column + 1 <= self._max_column) and (row + 2 <= self._max_row) and\
                    (board[row+2][column+1] == "" or board[row+2][column+1].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column+1) + str(row+3))
            # down and left
            if (column - 1 >= self._min_column) and (row + 2 <= self._max_row) and\
                    (board[row+2][column-1] == "" or board[row+2][column-1].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column-1) + str(row+3))
        # up
        if (row - 1 >= self._min_row) and board[row-1][column] == "":
            # up and right
            if (column + 1 <= self._max_column) and (row - 2 >= self._min_row) and\
                    (board[row-2][column+1] == "" or board[row-2][column+1].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column+1) + str(row-1))
            # up and left
            if (column - 1 >= self._min_column) and (row - 2 >= self._min_row) and\
                    (board[row-2][column-1] == "" or board[row-2][column-1].get_color() != self.get_color()):
                horse_legal_moves.append(get_num_to_letter(column-1) + str(row-1))

        return horse_legal_moves


class Elephants(Pieces):
    """
    Inherits from Pieces Class
    Contains unique rules for Elephant pieces
    1. Move Rules: one space forward then two diagonally OR
                    one space sideways then two diagonally
    2. Can be blocked by another piece
    Communicates legal moves with JanggiGame class
    """

    def get_legal_move(self, column, row, board):
        """
        Returns list of valid moves for Elephant
        column and row is where the piece currently is
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """

        elephant_legal_moves = []

        # Right
        if (column + 1 <= self._max_column) and board[row][column+1] == "":
            # right and up
            if (column + 2 <= self._max_column) and (row - 1 >= self._min_row) and board[row-1][column+2] == "":
                if (column + 3 <= self._max_column) and (row - 2 >= self._min_row) and\
                        (board[row-2][column+3] == "" or board[row-2][column+3].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column+3) + str(row-1))
            # right and down
            if (column + 2 <= self._max_column) and (row + 1 <= self._max_row) and board[row+1][column+2] == "":
                if (column + 3 <= self._max_column) and (row + 2 <= self._max_row) and\
                        (board[row+2][column+3] == "" or board[row+2][column+3].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column + 3) + str(row+3))
        # Left
        if (column - 1 >= self._min_column) and board[row][column-1] == "":
            # left and up
            if (column - 2 >= self._min_column) and (row - 1 >= self._min_row) and board[row - 1][column - 2] == "":
                if (column - 3 >= self._min_column) and (row - 2 >= self._min_row) and\
                        (board[row - 2][column - 3] == "" or board[row - 2][column - 3].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column - 3) + str(row-1))
            # left and down
            if (column - 2 >= self._min_column) and (row + 1 <= self._max_row) and board[row + 1][column - 2] == "":
                if (column - 3 >= self._min_column) and (row + 2 <= self._max_row) and\
                        (board[row + 2][column - 3] == "" or board[row + 2][column - 3].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column - 3) + str(row + 3))
        # Down
        if (row + 1 <= self._max_row) and board[row+1][column] == "":
            # down and right
            if (column + 1 <= self._max_column) and (row + 2 <= self._max_row) and board[row+2][column+1] == "":
                if (column + 2 <= self._max_column) and (row + 3 <= self._max_row) and\
                        (board[row+3][column+2] == "" or board[row+3][column+2].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column+2) + str(row+4))
            # down and left
            if (column - 1 >= self._min_column) and (row + 2 <= self._max_row) and board[row+2][column-1] == "":
                if (column - 2 >= self._min_column) and (row + 3 <= self._max_row) and\
                        (board[row+3][column-2] == "" or board[row+3][column-2].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column-2) + str(row+4))
        # up
        if (row - 1 >= self._min_row) and board[row-1][column] == "":
            # up and right
            if (column + 1 <= self._max_column) and (row - 2 >= self._min_row) and board[row-2][column+1] == "":
                if (column + 2 <= self._max_column) and (row - 3 >= self._min_row) and\
                        (board[row-3][column+2] == "" or board[row-3][column+2].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column+2) + str(row-2))
            # up and left
            if (column - 1 >= self._min_column) and (row - 2 >= self._min_row) and board[row-2][column-1] == "":
                if (column - 2 >= self._min_column) and (row - 3 >= self._min_row) and\
                        (board[row-3][column-2] == "" or board[row-3][column-2].get_color() != self.get_color()):
                    elephant_legal_moves.append(get_num_to_letter(column-2) + str(row-2))

        return elephant_legal_moves


class Cannons(Pieces):
    """
    Inherits from Pieces Class
    Contains unique rules for Cannon pieces
    1. Move Rules: in a straight line by hopping over another piece unless it is a cannon
    2. Cannot capture another cannon
    3. Cannot jump over another cannon
    Communicates legal moves with JanggiGame class
    """

    def diagonal_move_cannon(self, column_1, row_1, board, cannon_legal_moves):
        """
        Makes diagonal move for cannons when in fortress
        Must have piece in middle spot of fortress to move diagonally
        Inputs: Possible diagonal move coordinates (column_1, row_1) board and list of cannon legal moves)
        Outputs: List of all possible diagonal moves from current space
        """
        # Must have piece in center square of fortress to get here
        if board[row_1][column_1] == ""\
                or (board[row_1][column_1].get_color() != self.get_color() and
                    board[row_1][column_1].get_type() != self.get_type()):
            cannon_legal_moves.append(get_num_to_letter(column_1) + str(row_1 + 1))

        return

    def get_legal_move(self, column, row, board):
        """
        Returns list of valid moves for Cannon
        Column and Row is where the piece currently is
        Inputs: Current column #, row # and board
        Outputs: List of all possible legal moves from current space
        """
        cannon_legal_moves = []

        # Checks if in the fortress, if there is no piece in the middle, don't check
        if board[1][4] != "" and board[1][4].get_type() != self.get_type():
            if row == 0 and column == 3:
                self.diagonal_move_cannon(5, 2, board, cannon_legal_moves)
            if row == 0 and column == 5:
                self.diagonal_move_cannon(3, 2, board, cannon_legal_moves)
            if row == 2 and column == 3:
                self.diagonal_move_cannon(5, 0, board, cannon_legal_moves)
            if row == 2 and column == 5:
                self.diagonal_move_cannon(3, 0, board, cannon_legal_moves)
        if board[8][4] != "" and board[8][4].get_type() != self.get_type():
            if row == 7 and column == 3:
                self.diagonal_move_cannon(5, 9, board, cannon_legal_moves)
            if row == 7 and column == 5:
                self.diagonal_move_cannon(3, 9, board, cannon_legal_moves)
            if row == 9 and column == 3:
                self.diagonal_move_cannon(5, 7, board, cannon_legal_moves)
            if row == 9 and column == 5:
                self.diagonal_move_cannon(3, 7, board, cannon_legal_moves)

        # Checks horizontally
        # Checks spaces to the right, if it comes across another piece it jumps over (unless it is a cannon)
        # And can land on empty space or capture opponent
        jumped = False
        for i in range(column + 1, self._max_column + 1):
            if board[row][i] != '' and board[row][i].get_type() != self.get_type() and not jumped:
                jumped = True
            elif board[row][i] == '' and jumped:
                cannon_legal_moves.append(get_num_to_letter(i) + str(row + 1))
            elif board[row][i] != '' and board[row][i].get_color() != self.get_color() and\
                    board[row][i].get_type() != self.get_type() and jumped:
                cannon_legal_moves.append(get_num_to_letter(i) + str(row+1))
                break
            elif board[row][i] != '' and board[row][i].get_type() == self.get_type() and jumped:
                break

        # Checks spaces to the left, if it comes across another piece it jumps over (unless it is a cannon)
        # And can land on empty space or capture opponent
        jumped = False
        for i in range(column - 1, -1, -1):
            if board[row][i] != '' and board[row][i].get_type() != self.get_type() and not jumped:
                jumped = True
            elif board[row][i] == '' and jumped:
                cannon_legal_moves.append(get_num_to_letter(i) + str(row + 1))
            elif board[row][i] != '' and board[row][i].get_color() != self.get_color() and\
                    board[row][i].get_type() != self.get_type() and jumped:
                cannon_legal_moves.append(get_num_to_letter(i) + str(row+1))
                break
            elif board[row][i] != '' and board[row][i].get_type() == self.get_type() and jumped:
                break

        # Checks vertically
        # Checks up, if it comes across another piece it jumps over (unless it is a cannon)
        # And can land on empty space or capture opponent
        jumped = False
        for i in range(row - 1, -1, -1):
            if board[i][column] != '' and board[i][column].get_type() != self.get_type() and not jumped:
                jumped = True
            elif board[i][column] == '' and jumped:
                cannon_legal_moves.append(get_num_to_letter(column) + str(i + 1))
            elif board[i][column] != '' and board[i][column].get_color() != self.get_color() and\
                    board[i][column].get_type() != self.get_type() and jumped:
                cannon_legal_moves.append(get_num_to_letter(column) + str(i+1))
                break
            elif board[i][column] != '' and board[i][column].get_type() == self.get_type() and jumped:
                break

        # Checks down, if it comes across another piece it jumps over (unless it is a cannon)
        # And can land on empty space or capture opponent
        jumped = False
        for i in range(row + 1, self._max_row + 1):
            if board[i][column] != '' and board[i][column].get_type() != self.get_type() and not jumped:
                jumped = True
            elif board[i][column] == '' and jumped:
                cannon_legal_moves.append(get_num_to_letter(column) + str(i + 1))
            elif board[i][column] != '' and board[i][column].get_color() != self.get_color() and\
                    board[i][column].get_type() != self.get_type() and jumped:
                cannon_legal_moves.append(get_num_to_letter(column) + str(i+1))
                break
            elif board[i][column] != '' and board[i][column].get_type() == self.get_type() and jumped:
                break

        return cannon_legal_moves

game = JanggiGame()
game.print_board()