from blessed import Terminal
import random

def print_help():
    print("""
                       ? - help
                       t - teleport
                       . - wait
                       q - quit
left arrow / right arrow - move

""")

class Game:
    def __init__(self, term):
        assert term.width > 15, "terminal too narrow"
        self.tunnel_length = random.randint(10, min(max(15, term.width),
                                                    70))
        self.term = term
        self.message = "? for help"
        self.__newpos()

    def __newpos(self):
        self.player_pos = random.randint(0, self.tunnel_length - 1)

    def draw_player(self):
        with (self.term.hidden_cursor(),
              self.term.location(self.player_pos,
                                 self.term.height - 1)):
            print("@", end="")

    def draw_tunnel(self):
        with self.term.location(0, self.term.height - 1):
            print("#" * self.tunnel_length, end="")

    def draw_game(self):
        with self.term.location(0, self.term.height - 2):
            print('Welcome to '
                  + self.term.underline('the tunnel')
                  + f' ({self.message})!', end='')
        self.draw_tunnel()
        self.draw_player()

    def game_loop(self):
        tunnel_length = random.randint(10, 70)
        print()
        print()
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
                    self.__newpos()
                elif linp == ".":
                    pass
                elif inp.name == "KEY_LEFT":
                    self.player_pos = max(0, self.player_pos - 1)
                    self.draw_tunnel()
                    self.draw_player()
                elif inp.name == "KEY_RIGHT":
                    self.player_pos = min(self.tunnel_length-1,
                                          self.player_pos + 1)
                    self.draw_tunnel()
                    self.draw_player()
                else:
                    self.message = f"Key pressed was {inp.name}"
                    self.draw_game()
                self.draw_game()
        print()
        print("DONE")

def main():
    try:
        Game(Terminal()).game_loop()
    except Exception as e:
        print()
        print()
        print(f'Error: {e}')

