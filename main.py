from time import sleep
import argparse
from typing import Union
import fltk
from game import Connect4

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


class Game:
    def __init__(self, display_type):
        self.display_type = display_type
        self.radius = 30
        self.game = Connect4()

    # Regular stuff

    def get_player(self):
        return self.game.get_player()

    def get_player_tokens(self, player: int):
        return self.game.get_player_tokens(player)

    def get_player_color(self, player: int):
        if player == 1:
            return "yellow"
        return "red"

    def get_player_symbol(self, player: int):
        if player == 1:
            return "X"
        return "O"

    def add_token(self, pos, player=None):
        if player is None:
            player = self.get_player()
        return self.game.add_token(pos, player)

    def is_win(self, pos):
        return self.game.is_win(pos)

    def add_turn(self):
        return self.game.add_turn()

    # With a window

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

    def where_is_click(self, index_x: tuple, x: int):
        r = self.radius
        count = 0
        for left, right in index_x:
            if (left - r) <= x <= (right - r * 3):
                return True, count
            count += 1
        return False, None

    def find_visual_token(self, pos: int, board):
        for line in board:
            for token in line:
                if token.get_board_id() == pos:
                    return token

    # With text

    def fill_board(self):
        board = [[None for _ in range(7)] for _ in range(6)]
        for pos in self.get_player_tokens(1):
            board[pos // 10][pos % 10] = "X"
        for pos in self.get_player_tokens(2):
            board[pos // 10][pos % 10] = "O"
        return board

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
        player = self.get_player_symbol(self.get_player())
        n = input(f"\n{player} > ")
        while not n.isdigit():
            n = input(f"\n{player} > ")
        return int(n)

    # main

    def main(self):
        if self.display_type == "graphic":
            return self.main_graphic()
        return self.main_text()

    def main_graphic(self):
        fltk.cree_fenetre(WIDTH_WINDOW, HEIGHT_WINDOW, "Connect 4")
        fltk.rectangle(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW, remplissage="blue")
        visual_board, index_x = self.draw_circles()
        tev = None
        is_fin = False
        while tev != "Quitte":
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            if tev == "ClicGauche" and not is_fin:
                res, x = self.where_is_click(
                    index_x,
                    fltk.abscisse_souris(),
                )
                if res:
                    pos = self.add_token(x)
                    if pos is not None:
                        visual_token = self.find_visual_token(pos, visual_board)
                        visual_token.set_color(self.get_player_color(self.get_player()))
                        visual_token.animate()
                        visual_token.refresh()
                        if self.is_win(pos):
                            is_fin = True
                        self.add_turn()
            fltk.mise_a_jour()
        fltk.ferme_fenetre()

    def main_text(self):
        while True:
            print(self)
            column = self.wait_input()
            pos = self.add_token(column)
            if pos is not None:
                if self.is_win(pos):
                    break
                self.add_turn()
        print(self)


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
    game = Game(args["display"])
    game.main()
