from game import Game
# This is the main program, run this.

g = Game()

while g.running and not g.quit:
    g.curr_menu.display_menu()
    g.game_loop()
