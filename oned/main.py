from blessed import Terminal
import random

def print_help():
    print("""
? - help
t - teleport
q - quit

""")

class Game:
    def __init__(self, term):
        assert term.width > 10, "terminal too narrow"
        self.tunnel_length = random.randint(10, term.width)
        self.player_pos = random.randint(0, self.tunnel_length)
        self.term = term

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
                  + f' (? for help)!', end='')
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
                if inp.lower() == "q":
                    break
                elif inp.lower() == "?":
                    print_help()
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

