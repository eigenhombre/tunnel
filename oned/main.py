from blessed import Terminal
from contextlib import contextmanager
import random

TUNNEL  = "."
PLAYER  = "@"
MONSTER = "x"

def print_help():
    print("""
                       ? - help
                       t - teleport
                       . - wait
                       q - quit
                       h - left
                       l - right
left arrow / right arrow - left/right

""")

def pr(char):
    print(char, end="")

class Game:
    def __init__(self, term):
        assert term.width > 15, "terminal too narrow"
        self.tunnel_length = random.randint(10, min(max(15, term.width),
                                                    70))
        self.term = term
        self.teleports_left = 3
        self.message = "? for help"
        self.monster_pos = self.__random_location()
        self.__newpos()

    @contextmanager
    def __location(self, loc):
        with self.term.location(loc, self.term.height - 1):
            yield

    def __random_location(self):
        return random.randint(0, self.tunnel_length - 1)

    def __newpos(self):
        self.player_pos = self.__random_location()

    def clear_player(self):
        with self.__location(self.player_pos):
            pr(TUNNEL)

    def draw_monster(self):
        with self.__location(self.monster_pos):
            pr(MONSTER)

    def clear_monster(self):
        with self.__location(self.monster_pos):
            pr(TUNNEL)

    def draw_player(self):
        with self.__location(self.player_pos):
            pr(PLAYER)

    def draw_tunnel(self):
        with self.__location(0):
            pr(TUNNEL * self.tunnel_length)

    def draw_game(self):
        with self.term.location(0, self.term.height - 2):
            print('Welcome to '
                  + self.term.underline('the tunnel')
                  + f' ({self.message})!', end='')
        self.draw_tunnel()
        self.draw_player()
        self.draw_monster()

    def update_and_draw_monster(self):
        self.clear_monster()
        if self.player_pos > self.monster_pos:
            self.monster_pos += 1
        elif self.player_pos < self.monster_pos:
            self.monster_pos -= 1
        self.draw_monster()
        if self.monster_pos == self.player_pos:
            return True
        return False

    def game_loop(self):
        tunnel_length = random.randint(10, 70)
        print()
        print()
        with self.term.hidden_cursor():
            self.draw_game()
            while True:
                with self.term.cbreak(), self.term.hidden_cursor():
                    inp = self.term.inkey()
                    linp = inp.lower()
                    if linp == "q":
                        break
                    elif linp == "?":
                        print_help()
                        self.draw_game()
                    elif linp == "t":
                        if self.teleports_left > 0:
                            self.clear_player()
                            self.__newpos()
                            self.draw_player()
                            self.teleports_left -= 1
                    elif linp == ".":
                        pass
                    elif linp == "h" or inp.name == "KEY_LEFT":
                        self.clear_player()
                        self.player_pos = max(0, self.player_pos - 1)
                        self.draw_player()
                    elif linp == "l" or inp.name == "KEY_RIGHT":
                        self.clear_player()
                        self.player_pos = min(self.tunnel_length-1,
                                              self.player_pos + 1)
                        self.draw_player()
                    else:
                        self.message = f"Key pressed was {inp.name}"
                        self.draw_game()
                if self.update_and_draw_monster():
                    print()
                    print("You died!")
                    break
        print()
        print("Goodbye!")

def main():
    try:
        Game(Terminal()).game_loop()
    except Exception as e:
        print()
        print()
        print(f'Error: {e}')

