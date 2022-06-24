from time import sleep
import argparse
from typing import Union
import fltk
from game import Connect4

HEIGHT_WINDOW = 800
WIDTH_WINDOW = 800


class Token:
    """Class representing visual tokens, when the display mode isn't text
    """
    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        color: str,
        board_id: Union[int, str],
    ):
        """Initialisation

        :param x: the token abscissa
        :type x: int
        :param y: the token ordinate
        :type y: int
        :param radius: the token radius
        :type radius: int
        :param color: the token color
        :type color: str
        :param board_id: the token number, position
        :type board_id: Union[int, str]
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.board_id = board_id
        self.visual_id = None

    def get_board_id(self):
        """Return the position of the token
        (the position in the grid)

        :return: the position
        :rtype: int
        """
        return self.board_id

    def set_color(self, color: str):
        """Specify new token color

        :param color: the new color
        :type color: str
        :return: the new color
        :rtype: str
        """
        self.color = color
        return color

    def draw(self):
        """Display the token

        :return: the token tag
        :rtype: int
        """
        self.visual_id = fltk.cercle(
            self.x, self.y, 30, remplissage=self.color
        )
        return self.visual_id

    def erase(self):
        """Erase the token
        """
        fltk.efface(self.visual_id)
        self.visual_id = None

    def set_coords(self, x: int, y: int):
        """Specify new coordinates of the token

        :param x: the token new abscissa
        :type x: int
        :param y: the token new ordinate
        :type y: int
        :return: the new coordinates
        :rtype: tuple[int, int]
        """
        self.x = x
        self.y = y
        return x, y

    def refresh(self):
        """Refresh the token
        """
        self.erase()
        self.draw()

    def animate(self):
        """Move the token
        """
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


class Game:
    """Class allowing the player to play a game, managing all the inputs
    """
    
    def __init__(self, display_type: str):
        """Initialisation

        :param display_type: the type of display. Must be 'graphic' or 'text'
        :type display_type: str
        """
        self.display_type = display_type
        self.radius = 30
        self.game = Connect4()

    # Regular functions

    def get_player(self):
        """Get the player's turn

        :return: the player's turn
        :rtype: int
        """
        return self.game.get_player()

    def get_player_tokens(self, player: int):
        """Get the player's tokens

        :param player: the player
        :type player: int
        :return: the set of the positions of all his tokens
        :rtype: set
        """
        return self.game.get_player_tokens(player)

    def get_player_color(self, player: int):
        """Get player's color

        :param player: the player
        :type player: int
        :return: 'yellow' if player if '1', else 'red'
        :rtype: str
        """
        if player == 1:
            return "yellow"
        return "red"

    def get_player_symbol(self, player: int):
        """Get player's symbol

        :param player: the player
        :type player: int
        :return: 'X' if player if '1', else 'O'
        :rtype: str
        """
        if player == 1:
            return "X"
        return "O"

    def add_token(self, column: int, player: Union[int, None]=None):
        """Add a player token in the column ``column`` of the game

        :param column: the column to add the token
        :type column: int
        :param player: the player who placed the token, defaults to None
        :type player: Union[int, None], optional
        :return: the position of the new token, None if the token can't be add in the column
        :rtype: Union[int, None]
        """
        if player is None:
            player = self.get_player()
        pos = self.game.add_token(column, player)
        return pos

    def is_win(self, pos: Union[int, None]=None):
        """Return true if one of the players connect 4 tokens

        :param pos: the position of the last token placed, defaults to None
        :type pos: Union[int, None], optional
        :return: True if one player wins, else False
        :rtype: bool
        """
        if pos is None:
            for column in range(7):
                for pos in {10*y+column for y in range(6)}:
                    if self.game.is_win(pos):
                        return True
            return False
        return self.game.is_win(pos)

    def add_turn(self):
        """specify that one players have played

        :return: the new amount of turn
        :rtype: int
        """
        return self.game.add_turn()

    # With a window

    def draw_circles(self):
        """Draw circles representing empty holes on the board and tokens

        :return: _description_
        :rtype: _type_
        """
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
                        visual_token = self.find_visual_token(
                            pos, visual_board
                        )
                        visual_token.set_color(
                            self.get_player_color(self.get_player())
                        )
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
