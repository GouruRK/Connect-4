from time import sleep
import argparse
from typing import Union
import fltk

HEIGHT_WINDOW = 800
WIDTH_WINDOW = 800


class Token:
    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        color: str,
        board_id: Union[int, str],
        visual_id: Union[int, str] = None,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.board_id = board_id
        self.visual_id = visual_id
        return None

    def get_board_id(self):
        return self.board_id

    def set_color(self, color: str):
        self.color = color
        return color

    def draw(self):
        self.visual_id = fltk.cercle(self.x, self.y, 30, remplissage=self.color)
        return self.visual_id

    def erase(self):
        fltk.efface(self.visual_id)
        self.visual_id = None
        return None

    def set_coords(self, x: int, y: int):
        self.x = x
        self.y = y
        return x, y

    def refresh(self):
        self.erase()
        self.draw()

    def animate(self):
        step = 20
        y_init = 50
        y_final = self.y
        t = Token(self.x, y_init, 30, self.color, None)
        t.draw()
        while y_init < y_final:
            sleep(0.01)
            t.set_coords(self.x, y_init)
            y_init += step
            t.refresh()
            fltk.mise_a_jour()
        t.erase()
        return None


class Play:
    def __init__(self, display: str, player1: Union[None, set]=None, player2: Union[None, set]=None):
        self.display = display
        self.radius = 30
        self.count_turn = 0
        if player1 is None:
            player1 = set()
        self.player1 = player1
        if player2 is None:
            player2 = set()
        self.player2 = player2
        return None

    def draw_circles(self):
        x = 50
        dx = WIDTH_WINDOW / 7
        dy = HEIGHT_WINDOW / 6
        board = []
        index_x = []
        for i1 in range(7):
            index_x.append((x, x + dx))
            y = 50
            temp = []
            for i2 in range(6):
                t = Token(x, y, self.radius, "white", i2 * 10 + i1)
                t.draw()
                temp.append(t)
                y += dy
            x += dx
            board.append(temp)
        return board, index_x

    def get_player(self):
        if self.count_turn % 2 == 0:
            return 1
        return 2

    def get_player_color(self, player: Union[int, None]=None):
        if player is not None:
            if player == 1:
                return "yellow"
            return "red"
        if self.count_turn % 2 == 0:
            return "yellow"
        return "red"

    def get_player_symbol(self, player: Union[int, None]=None):
        if player is not None:
            if player == 1:
                return "X"
            return 0
        if self.count_turn % 2 == 0:
            return "X"
        return "O"

    def get_player_tokens(self, player: Union[int, None]=None):
        if player is not None:
            if player == 1:
                return self.player1
            else:
                return self.player2
        if self.count_turn % 2 == 0:
            return self.player1
        return self.player2

    def where_is_click(self, index_x: tuple, x: int):
        r = self.radius
        count = 0
        for left, right in index_x:
            if (left - r) <= x <= (right - r * 3):
                return True, count
            count += 1
        return False, None

    def find_visual_token(self, pos: int):
        for line in self.visual_board:
            for token in line:
                if token.get_board_id() == pos:
                    return token

    def check_is_valid(self, x: int):
        if x in self.player1 or x in self.player2:
            return False
        return True

    def add_token(self, x, player: Union[int, None]=None):
        for y in range(6 - 1, -1, -1):
            pos = (10 * y) + x
            if not (pos in self.player1 or pos in self.player2):
                tokens = self.get_player_tokens(player)
                tokens.add(pos)
                if self.display == "graphic":
                    visual_token = self.find_visual_token(pos)
                    visual_token.set_color(self.get_player_color())
                    visual_token.animate()
                    visual_token.refresh()
                return pos
        return None

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
        maxi = max(c, maxi)
        return maxi

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

    def fill_board(self):
        board = [[None for i in range(7)] for j in range(6)]
        for pos in self.player1:
            board[pos // 10][pos % 10] = "X"
        for pos in self.player2:
            board[pos // 10][pos % 10] = "O"
        return board

    def copy(self):
        player_1_copy = self.player1.copy()
        player_2_copy = self.player2.copy()
        return Play(self.display, player_1_copy, player_2_copy)

    def __str__(self):
        board = self.fill_board()
        ch = "\n\n"
        for line in range(len(board)):
            for car in range(len(board[line])):
                if board[line][car] is None:
                    if car == 6:
                        ch += "|    |"
                    else:
                        ch += "|    "
                else:
                    if car == 6:
                        ch += f"| {board[line][car]} | "
                    else:
                        ch += f"| {board[line][car]}  "
            ch += "\n"
        ch += "\n"
        for x in range(7):
            if x == 6:
                ch += f"|  {x} |"
            else:
                ch += f"|  {x} "
        return ch

    def wait_input(self):
        player = self.get_player_symbol()
        n = input(f"\n{player} > ")
        while not n.isdigit():
            n = input(f"\n{player} > ")
        return int(n)

    def main_graphic(self):
        fltk.cree_fenetre(WIDTH_WINDOW, HEIGHT_WINDOW, "Connect 4")
        fltk.rectangle(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW, remplissage="blue")
        self.visual_board, self.index_x = self.draw_circles()
        tev = None
        is_fin = False
        while tev != "Quitte":
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            if tev == "ClicGauche" and not is_fin:
                res, x = self.where_is_click(
                    self.index_x,
                    fltk.abscisse_souris(),
                )
                if res:
                    if self.check_is_valid(x):
                        pos = self.add_token(x)
                        if pos is not None:
                            if self.is_win(pos):
                                is_fin = True
                            self.count_turn += 1
            fltk.mise_a_jour()
        fltk.ferme_fenetre()

    def main_text(self):
        while True:
            print(self)
            x = self.wait_input()
            pos = self.add_token(x)
            if pos is not None:
                if self.is_win(pos):
                    break
            self.count_turn += 1
        print(self)

    def main(self):
        if self.display == "graphic":
            return self.main_graphic()
        return self.main_text()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect 4")
    parser.add_argument(
        "--display",
        "-d",
        choices={"graphic", "text"},
        default="graphic",
        help="Allows you to choose the display mode of the game",
    )
    args = vars(parser.parse_args())
    game = Play(args["display"])
    game.main()
