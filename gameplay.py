from sushi_go import Game
from gui import GUI
import sys
import threading

def main():
    game = Game()
    gui = GUI()
    
    def run_game():
        game.play()

    game_thread = threading.Thread(target=run_game)
    game_thread.daemon = True
    game_thread.start()
    gui.run(game)
    game_thread.join()
      
if __name__ == "__main__":
    main()
