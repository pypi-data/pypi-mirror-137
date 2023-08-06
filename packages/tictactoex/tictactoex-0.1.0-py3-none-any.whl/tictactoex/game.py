import copy

from game_settings import *


class Game:
    """
    Game logic for a 2 player tic-tac-toe game.

    Attributes:
       is_player1_turn (bool): Flag that controls players turn. First to play is randomly generated.
       total_moves (int): Keeps the number of moves played. Used to check for game ties.
       board_state (list): Array that keeps the game board current layout, top-left position being 0.
       plays (array): Keeps all the board_states in a game.
    """

    def __init__(self):
        self.is_player1_turn = True
        self.total_moves = 0
        self.board_state = ["", "", "", "", "", "", "", "", ""]
        self.plays = []

    def play(self, position):
        """
        :param position: integer that represents board position to play on.
        :return: string outcome of requested play.
        """

        if self.is_position_empty(position):

            self.place_marker(position)
            self.increase_total_moves()
            self.save_board_state()

            if (
                    self.total_moves > 4
            ):  # waits to the fifth move to start checking for victories
                if self.has_player_won():
                    return P1_WON if self.is_player1_turn else P2_WON
                elif self.total_moves > 8:
                    return DRAW_GAME

            self.change_player_turn()

            return MARK_WAS_PLACED
        else:
            return OCCUPIED_POSITION

    def save_board_state(self):
        self.plays.append(copy.deepcopy(self.board_state))

    def change_player_turn(self):
        self.is_player1_turn = not self.is_player1_turn

    def increase_total_moves(self):
        self.total_moves += 1

    def is_position_empty(self, position):
        """
        :return: bool indicating whether the slot is empty
        """
        board = self.board_state
        return board[position] == ""

    def place_marker(self, position):
        """
        Marks the board with current player mark.

        :return: Nothing
        """
        board = self.board_state

        board[position] = P1_MARKER if self.is_player1_turn else P2_MARKER

    def has_player_won(self):
        """
        Checks, after each play, if someone has won.

        :return: True if a winning pattern is present on the board. False otherwise.
        """

        board = self.board_state

        return (
                board[0] == board[1] == board[2]
                and board[0] != ""
                or board[3] == board[4] == board[5]
                and board[3] != ""
                or board[6] == board[7] == board[8]
                and board[6] != ""
                or board[0] == board[3] == board[6]
                and board[0] != ""
                or board[1] == board[4] == board[7]
                and board[1] != ""
                or board[2] == board[5] == board[8]
                and board[2] != ""
                or board[0] == board[4] == board[8]
                and board[0] != ""
                or board[2] == board[4] == board[6]
                and board[2] != ""
        )
