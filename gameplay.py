from sushi_go import *

def main():
    game = Game()
    
    for i in range(game.total_round):
        for j in range(game.total_turn):
            game.play_a_turn(i)
    game.end_the_game()
            
if __name__ == "__main__":
    main()