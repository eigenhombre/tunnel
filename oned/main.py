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

def randpos(max_pos):
    return random.randint(0, max_pos)

class Monster:
    def __init__(self, max_pos):
        self.pos = randpos(max_pos)

class Game:
    def __init__(self, term):
        assert term.width > 15, "terminal too narrow"
        self.tunnel_length = random.randint(10, min(max(15, term.width),
                                                    70))
        self.term = term
        self.teleports_left = 3
        self.message = "? for help"
        self.monsters = [Monster(self.tunnel_length - 1)]
        self.__newpos()

    @contextmanager
    def __location(self, loc):
        with self.term.location(loc, self.term.height - 1):
            yield

    def __random_location(self):
        return randpos(self.tunnel_length - 1)

    def __newpos(self):
        self.player_pos = self.__random_location()

    def clear_player(self):
        with self.__location(self.player_pos):
            pr(TUNNEL)

    def draw_monsters(self):
        for m in self.monsters:
            with self.__location(m.pos):
                pr(MONSTER)

    def clear_monsters(self):
        for m in self.monsters:
            with self.__location(m.pos):
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
        self.draw_monsters()

    def update_and_draw_monsters(self):
        self.clear_monsters()
        eaten = False
        for m in self.monsters:
            if self.player_pos > m.pos:
                target = m.pos + 1
            elif self.player_pos < m.pos:
                target = m.pos - 1
            else:
                target = m.pos
            if not any(other.pos == target for other in self.monsters if m != other):
                m.pos = target
            if m.pos == self.player_pos:
                eaten = True
        self.draw_monsters()
        return eaten

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
                            self.monsters.append(Monster(self.tunnel_length - 1))
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
                if self.update_and_draw_monsters():
                    print()
                    print("You were eaten by a monster.")
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
