from time import sleep
import argparse
from typing import Union
import fltk
from game import Connect4

HEIGHT_WINDOW = 800
WIDTH_WINDOW = 800


class Token:
    """Class representing visual tokens, when the display mode isn't text"""

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
        self.visual_id = fltk.cercle(self.x, self.y, 30, remplissage=self.color)
        return self.visual_id

    def erase(self):
        """Erase the token"""
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
        """Refresh the token"""
        self.erase()
        self.draw()

    def animate(self):
        """Move the token"""
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


class Game(Connect4):
    """Class allowing the player to play a game, managing all the inputs"""

    def __init__(self, display_type: str):
        """Initialisation

        :param display_type: the type of display. Must be 'graphic' or 'text'
        :type display_type: str
        """
        super().__init__()
        self.display_type = display_type
        self.radius = 30

    # Regular functions

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

    # With a window

    def draw_circles(self):
        """Draw circles representing empty holes on the board and tokens

        :return: a tuple within the first element the set of alls tokens,
                 and the second element the abscissa coordinates of each
                 column
        :rtype: tuple[set[object], tuple[int, int]]
        """
        x = 50
        dx = WIDTH_WINDOW / 7
        dy = HEIGHT_WINDOW / 6
        visual_tokens = set()
        for i1 in range(7):
            y = 50
            for i2 in range(6):
                t = Token(x, y, self.radius, "white", i2 * 10 + i1)
                t.draw()
                visual_tokens.add(t)
                y += dy
            x += dx
        return visual_tokens, dx

    def where_is_click(self, x: int, space: int):
        """Get the column where the user clicked

        :param x: the user mouse abscissa
        :type x: int
        :param space: the space of each column
        :type space: int
        :return: the column selected, False if the user clicked somewhere
                 else
        :rtype: Union[bool, int]
        """
        r = self.radius
        column = 0
        left = 50
        right = 50 + space
        for _ in range(7):
            if (left - r) <= x <= (right - r * 3):
                return column
            left, right = right, right + space
            column += 1
        return False

    def find_visual_token(self, pos: int, visual_tokens: set):
        """Find the visual token according to a position

        :param pos: the position the token represent
        :type pos: int
        :param visual_tokens: the set of alls tokens
        :type visual_tokens: set
        :return: the token
        :rtype: object
        """
        for token in visual_tokens:
            if token.get_board_id() == pos:
                return token

    # With text

    def __str__(self):
        """Print the grid to text format

        :return: the grid
        :rtype: str
        """
        ch = "\n\n"
        for y in range(6):
            for column in range(7):
                pos = 10 * y + column
                if pos in self.get_player_tokens(1):
                    car = "X"
                elif pos in self.get_player_tokens(2):
                    car = "O"
                else:
                    car = " "
                if column == 6:
                    ch += f"| {car} | "
                else:
                    ch += f"| {car} "
            ch += "\n"
        for x in range(7):
            if x == 6:
                ch += f"| - |"
            else:
                ch += f"| - "
        ch += "\n"
        for x in range(7):
            if x == 6:
                ch += f"| {x} |"
            else:
                ch += f"| {x} "
        return ch

    def wait_input(self):
        """Wait the user input

        :return: the selected column
        :rtype: int
        """
        player = self.get_player_symbol(self.get_player())
        n = input(f"\n{player} > ")
        while not n.isdigit():
            n = input(f"\n{player} > ")
        return int(n)

    # main

    def main(self):
        """The main function to play"""
        if self.display_type == "graphic":
            return self.main_graphic()
        return self.main_text()

    def main_graphic(self):
        """The main function to play the game when the user choice is to use
        graphic display"""
        fltk.cree_fenetre(WIDTH_WINDOW, HEIGHT_WINDOW, "Connect 4")
        fltk.rectangle(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW, remplissage="blue")
        visual_board, space = self.draw_circles()
        tev = None
        is_fin = False
        while tev != "Quitte":
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            if tev == "ClicGauche" and not is_fin:
                column = self.where_is_click(fltk.abscisse_souris(), space)
                if not isinstance(column, bool):
                    player = self.get_player()
                    pos = self.add_token(column, player)
                    if pos is not None:
                        visual_token = self.find_visual_token(pos, visual_board)
                        visual_token.set_color(self.get_player_color(player))
                        visual_token.animate()
                        visual_token.refresh()
                        if self.is_win(pos):
                            is_fin = True
                        self.add_turn()
            fltk.mise_a_jour()
        fltk.ferme_fenetre()

    def main_text(self):
        """The main function to play the game when the user choice is to use
        graphic display"""
        g = False
        while not g:
            print(self)
            column = self.wait_input()
            pos = self.add_token(column, self.get_player())
            g = self.is_win(pos)
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
