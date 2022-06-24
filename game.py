from typing import Union


class Connect4:
    def __init__(
        self,
        player1: Union[None, set] = None,
        player2: Union[None, set] = None,
    ):
        self.count_turn = 0
        if player1 is None:
            player1 = set()
        self.player1 = player1
        if player2 is None:
            player2 = set()
        self.player2 = player2
        return None

    def get_player(self):
        if self.count_turn % 2 == 0:
            return 1
        return 2

    def get_player_tokens(self, player: int):
        if player == 1:
            return self.player1
        return self.player2

    def add_token(self, column, player: int):
        for y in range(6 - 1, -1, -1):
            pos = (10 * y) + column
            if self.is_pos_empty(pos):
                tokens = self.get_player_tokens(player)
                tokens.add(pos)
                return pos
        return None

    def add_turn(self):
        self.count_turn += 1
        return self.count_turn

    def count(self, player: int, begin: int, end: int, step: int):
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
        res_line = self.count(player, pos - 3, pos + 4, 1)
        res_column = self.count(player, pos - 10 * 3, pos + 10 * 4, 10)
        res_diag_1 = self.count(player, pos - 11 * 3, pos + 11 * 4, 11)
        res_diag_2 = self.count(player, pos - 9 * 3, pos + 9 * 4, 9)
        return res_line, res_column, res_diag_1, res_diag_2

    def is_win(self, pos: int):
        player = self.get_player()
        line, column, diag_1, diag_2 = self.get_nb_arround(player, pos)
        if max(line, column, diag_1, diag_2) >= 4:
            return True
        return False

    def copy(self):
        player_1_copy = self.player1.copy()
        player_2_copy = self.player2.copy()
        return Connect4(player_1_copy, player_2_copy)

    def is_pos_empty(self, pos: int):
        if pos in self.player1 or pos in self.player2:
            return False
        return True
