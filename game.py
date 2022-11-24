from typing import Union


class Connect4:
    """Class containing the main part of the game sense"""

    def __init__(
        self,
        player1: Union[None, set] = None,
        player2: Union[None, set] = None,
        turn: int = 0,
    ):
        """Initialisation

        :param player1: the position of player 1 tokens, defaults to None
                        means that the player have no tokens yet
        :type player1: Union[None, set], optional
        :param player2: the position of player 1 tokens, defaults to None
                        means that the player have no tokens yet
        :type player2: Union[None, set], optional
        :param turn: the number of turns
        :type turn: int
        """
        if player1 is None:
            player1 = set()
        self.player1 = player1
        if player2 is None:
            player2 = set()
        self.player2 = player2
        self.count_turn = turn

    def get_player(self):
        """Get players turn

        :return: the player
        :rtype: int
        """
        if self.count_turn % 2 == 0:
            return 1
        return 2

    def get_player_tokens(self, player: int):
        """Get all tokens of a player

        :param player: the player
        :type player: int
        :return: the tokens
        :rtype: set
        """
        if player == 1:
            return self.player1
        return self.player2

    def add_token(self, column: int, player: int):
        """add a token to player, depending on the column

        :param column: the column where the player inserted the token
        :type column: int
        :param player: the player who played
        :type player: int
        :return: the position of the token, None if there is no place
                 remaining in the column
        :rtype: Union[int, None]
        """
        for y in range(6 - 1, -1, -1):
            pos = (10 * y) + column
            if self.is_pos_empty(pos):
                tokens = self.get_player_tokens(player)
                tokens.add(pos)
                return pos
        return None

    def add_turn(self):
        """Add a turn to the turn's counter

        :return: the new amount of turns
        :rtype: int
        """
        self.count_turn += 1
        return self.count_turn

    def count(self, player: int, begin: int, end: int, step: int):
        """Count the maximum amount of "linked" tokens in a row

        :param player: the player to count the tokens
        :type player: int
        :param begin: the begining of the row
        :type begin: int
        :param end: the end of the row
        :type end: int
        :param step: the step between each token
        :type step: int
        :return: the maximum of linked tokens
        :rtype: int
        """
        tokens = self.get_player_tokens(player)
        maxi = 0
        c = 0
        for nb in range(begin, end, step):
            if nb in tokens:
                c += 1
            else:
                if c >= maxi:
                    maxi = c
                    c = 0
        return max(c, maxi)

    def get_nb_arround(self, player: int, pos: int):
        """Get the number maximum of "linked" tokens from a center position
           in alls directions

        :param player: the players to look for tokens
        :type player: int
        :param pos: the center position
        :type pos: int
        :return: the maximum number of "linked" tokens in alls directions
        :rtype: tuple[int, int, int, int]
        """
        res_line = self.count(player, pos - 3, pos + 4, 1)
        res_column = self.count(player, pos - 10 * 3, pos + 10 * 4, 10)
        res_diag_1 = self.count(player, pos - 11 * 3, pos + 11 * 4, 11)
        res_diag_2 = self.count(player, pos - 9 * 3, pos + 9 * 4, 9)
        return res_line, res_column, res_diag_1, res_diag_2

    def is_win(self, pos: Union[int, None]):
        """Tells if a player wins based on his last placed token

        :param pos: the positions of the last token if type is int, else the
                    whole grid
        :type pos: Union[int, None]
        :return: True if he wins, else False
        :rtype: bool
        """
        player = self.get_player()
        if pos is not None:
            if max(*self.get_nb_arround(player, pos)) >= 4:
                return True
            return False
        for column in range(7):
            for pos in {10 * y + column for y in range(6)}:
                if max(*self.get_nb_arround(player, pos)) >= 4:
                    return True
            return False

    def copy(self):
        """Copy the actual state of the game

        :return: a new Connect4 object
        :rtype: object
        """
        player_1_copy = self.player1.copy()
        player_2_copy = self.player2.copy()
        return Connect4(player_1_copy, player_2_copy, self.count_turn)

    def is_pos_empty(self, pos: int):
        """Tells if a player already placed a token at a specific position

        :param pos: the position to check
        :type pos: int
        :return: True if no players owns a token at the position, else False
        :rtype: bool
        """
        if pos in self.player1 or pos in self.player2:
            return False
        return True
