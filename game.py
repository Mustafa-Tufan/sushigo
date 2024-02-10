import random
from sushigo import *
import tkinter as tk

def main():
    game = Game()

    for card, count in card_type.items():
        for i in range(count):
            card_list.append(Card(card, i))

    #random.seed(1)
    drawn_cards = random.sample(card_list, total_turn*total_round*total_user)

    for user in game.users:
        for i in range(total_round):
            for _ in range(total_turn):
                user.user_drawn_cards[i].append(drawn_cards.pop(0))

    rounds = 0
    print("Press q anytime to quit")
    quit_flag1 = False
    while (rounds < total_round) and not quit_flag1:
        turn = 0
        quit_flag2 = False
        while (turn < total_turn) and not quit_flag2:
            game.throw_randomly(rounds,game.users)
            print("")
            print(*game.users[0].user_drawn_cards[rounds])
            print("Bot 1 card on top: " , game.users[1].inventory[rounds][len(game.users[1].inventory[rounds]) - 1])
            print("Bot 2 card on top: " , game.users[2].inventory[rounds][len(game.users[2].inventory[rounds]) - 1])
            print("Bot 3 card on top: " , game.users[3].inventory[rounds][len(game.users[3].inventory[rounds]) - 1])
            print("")
            quit_flag3 = False
            while True and not quit_flag3:
                try:
                    # Skips last round because you have only 1 card to throw
                    if len(game.users[0].user_drawn_cards[rounds]) == 1:
                        card = 1
                        break
                    # If user has more than 1 card in his deck
                    else:
                        card = input(f"Pick a card between 1 and {len(game.users[0].user_drawn_cards[rounds])}: ")
                        if card == "q":
                            quit_flag3 = True
                            quit_flag2 = True
                            quit_flag1 = True
                            break   
                        card = int(card)
                        if 1 <= card <= len(game.users[0].user_drawn_cards[rounds]):
                            break
                        else: # if user chooses a number outside of the given range
                            print("Number must be between 1 and 8. Please try again.")
                except ValueError: # if user enters a floating variable
                    print("Invalid input. Please enter a valid number.")

            if quit_flag2 == True:
                break
            drawn_card = game.users[0].user_drawn_cards[rounds][int(card) - 1]
            game.users[0].user_drawn_cards[rounds].remove(drawn_card)
            game.users[0].inventory[rounds].append(drawn_card)
            game.swap_the_cards(rounds, game.users)
            turn+=1
            
        if quit_flag1 == True:
            break
        rounds+=1
    if not quit_flag1:
        print()
        game.calculate_points()
        game.reveal_the_winner(game.users)
        print()
            
if __name__ == "__main__":
    main()