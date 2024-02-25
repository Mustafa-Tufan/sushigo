import random
import math
import sys
from gui import GUI

'''
card_type = {"Tempura":14, "Sashimi":14, "Dumbling":14, "1xMaki Roll":6, "2xMaki Roll":12, 
             "3xMaki Roll":8, "Salmon Nigiri":10, "Squid Nigiri":5, "Egg Nigiri":5, 
             "Pudding":10, "Wasabi":6, "Chopsticks":4,"Soya Sauce": 4}
'''
card_type = {"Tempura":16, "Sashimi":16, "Dumbling":16, "1xMaki Roll":8, "2xMaki Roll":15, 
             "3xMaki Roll":10, "Salmon Nigiri":12, "Squid Nigiri":8, "Egg Nigiri":8, 
             "Wasabi":6}
card_list = []

class Card:
    def __init__(self, type, id, index):
        self.id = id                        # Why do i have this?
        self.type = type                    # ToString related
        self.index = index                  # GUI related
    def __str__(self):
        return f"{self.type}  "

class User:
    clicked_card = 0
    quit_game = 0
    def __init__(self, user_type, user_name, user_id):
        self.user_type = user_type                          
        self.user_id = user_id
        self.user_name = user_name
        self.points = [0,0,0]
        self.total_point = 0
        self.user_drawn_cards = [[] for _ in range(3)]
        self.inventory = [[] for _ in range(3)]
        self.card_positions = []
        self.front_position = (0,0)
        
    def __str__(self):
        return f"{self.user_type}({self.user_id}) - Points: {self.total_point}"
    
    # Spaghetti codding yippie!!!!!! (Too lazy to fix it)
    def throw_card(self, rounds):
        if self.user_type == "bot":
            drawn_card = random.choice(self.user_drawn_cards[rounds])
            self.user_drawn_cards[rounds].remove(drawn_card)
            self.inventory[rounds].append(drawn_card)
            return
        '''
        while True:
            try:
                card = input(f"Pick a card between 1 and {len(self.user_drawn_cards[rounds])}: ")
                if card == "q":
                    sys.exit()
                card = int(card)
                if 1 <= card <= len(self.user_drawn_cards[rounds]):
                    break
                else: # if user chooses a number outside of the given range
                    print(f"Number must be between 1 and {len(self.user_drawn_cards[rounds])}. Please try again.")
            except ValueError: # if user enters a floating variable
                print("Invalid input. Please enter a valid number.")
        '''
        while (self.clicked_card == 0):
            if (self.quit_game == 1): 
                sys.exit()
            card = self.clicked_card
        drawn_card = self.user_drawn_cards[rounds][int(card) - 1]
        self.user_drawn_cards[rounds].remove(drawn_card)
        self.inventory[rounds].append(drawn_card)
        self.clicked_card = 0
        
class Game:
    users = []
    total_round = 0
    total_turn = 0
    total_user = 0
    current_round = 0
    current_turn = 0
    user_turn = 0
    quit_game = 0
    
    def __init__(self):
        self.prepare_game()        
    
    def prepare_game(self):
        print("\nSushi Go! can be played with 2-5 people\n")
        while True:
            try:
                player_count = int(input("Enter player count: "))
                bot_count = int(input("Enter bot count: "))
                self.total_user = player_count + bot_count
                if player_count == 0:
                    raise ValueError("Player counts must be at least 1.")
                elif not (2 <= self.total_user <= 5):
                    raise ValueError("Total player and bot count must be between 2 and 5.")
                break  # Valid counts, so exit the loop
            
            except ValueError as e:
                print(e)
        
        for i in range(self.total_user):
            if i < player_count:
                self.users.append(User("player", input(f"Enter player {i}'s name: "), i))
            else:
                self.users.append(User("bot", f"bot {i}", i))
        
        self.total_turn = 12 - self.total_user
        self.total_round = 3
        
        index = 0
        for card, count in card_type.items():
            for i in range(count):
                card_list.append(Card(card, i, index))
            index += 1
        
        #random.seed(1)
        drawn_cards = random.sample(card_list, self.total_turn * self.total_round * self.total_user)

        for user in self.users:
            for i in range(self.total_round):
                for _ in range(self.total_turn):
                    user.user_drawn_cards[i].append(drawn_cards.pop(0))
                    
        print("\nType q anytime to quit") 

    def play(self):
        for i in range(self.total_round):
            self.current_round = i
            self.play_a_round(i)
            self.current_turn = 0
        self.end_the_game()

    def play_a_round(self,rounds):
        for j in range(self.total_turn):
            self.current_turn = j
            self.play_a_turn(rounds)
                
    def play_a_turn(self, rounds):
        for user in self.users:
            if user.user_type == "player":
                print("\n",*user.user_drawn_cards[rounds],"\n")
            user.throw_card(rounds)
            self.user_turn += 1
        self.give_information(rounds)
        self.swap_the_cards(rounds)
        self.current_turn += 1
        self.user_turn = 0
            
    def give_information(self, rounds):
        print("")
        for user in self.users:
            print(f"{user.user_name} card on top: ", user.inventory[rounds][len(user.inventory[rounds]) - 1])
        
    def deep_copy(self, list1, list2):
        for element in list2:
            list1.append(element)
        
    def swap_the_cards(self, rounds):
        temp = []
        self.deep_copy(temp, self.users[len(self.users) - 1].user_drawn_cards[rounds])
        self.users[len(self.users) - 1].user_drawn_cards[rounds] = []
        for i in range(len(self.users) - 1):
            self.deep_copy(self.users[len(self.users) - 1 - i].user_drawn_cards[rounds], self.users[len(self.users) - 2 - i].user_drawn_cards[rounds])
            self.users[len(self.users) - 1 - i - 1].user_drawn_cards[rounds] = []
        self.deep_copy(self.users[0].user_drawn_cards[rounds], temp)
        '''
        temp = []
        self.deep_copy(temp, self.users[0].user_drawn_cards[rounds])
        self.users[0].user_drawn_cards[rounds] = []
        for i in range(len(self.users) - 1):
            self.deep_copy(self.users[i].user_drawn_cards[rounds], self.users[i + 1].user_drawn_cards[rounds])
            self.users[i + 1].user_drawn_cards[rounds] = []
        self.deep_copy(self.users[len(self.users) - 1].user_drawn_cards[rounds], temp)
        '''
        
    # Counts total colors of users deck in a given round. To do that, it uses a dictionary with all values set to 1
    # Values are different for nigiris and maki rolls because they count as single color
    # Case 1: Person with soya souce has most colors    (2nd and 3rd loop)
    # Case 2: Person with soya souce not has most colors    (1st loop)
    # Case 3: More than one people share most colors and both have soya souce   (2nd and 3rd loop)
    '''
    def soya_sauce_calculator(self, rounds, users):
        color_counts = []
        have_soya_sauce = []
        for user in users:
            color_count = 0
            has_soya_sauce = 0

            maki_count = 1
            nigiri_count = 1

            type_counts = {"Tempura": 1, "Sashimi": 1, "Dumbling": 1,
                        "1xMaki Roll": maki_count, "2xMaki Roll": maki_count, 
                        "3xMaki Roll": maki_count, "Salmon Nigiri": nigiri_count,
                        "Squid Nigiri": nigiri_count, "Egg Nigiri": nigiri_count, 
                        "Wasabi": maki_count, "Pudding": 1, "Chopsticks": 1, "Soya Sauce": 1}

            for element in user.inventory[rounds]:
                if element.type in type_counts:
                    color_count += type_counts[element.type]
                    type_counts[element.type] = 0

                    if element.type == "Soya Sauce":
                        has_soya_sauce += 1

                    if "Maki" in element.type:
                        maki_count = 0
                    elif "Nigiri" in element.type:
                        nigiri_count = 0

            color_counts.append(color_count)
            have_soya_sauce.append(has_soya_sauce)
            
        players_with_max_color = 0
        for i in range(4):
            if (color_counts[i] == max(color_counts)) and (have_soya_sauce[i] == 0):
                return
        for i in range(4):
            if (color_counts[i] == max(color_counts)) and (have_soya_sauce[i] >= 1):
                players_with_max_color+=1
        for i in range(4):
            if (color_counts[i] == max(color_counts)) and (have_soya_sauce[i] >= 1):
                users[i].points[rounds] += math.floor(4/players_with_max_color)           
    '''    
    # Calculates total maki rolls of an user in round (rounds), then it holds them in a list
    # Counts how many #1 players and #2 players. Changes values on the list to make things easier
    # My senses says i should revert the changes in the list after method ends but why?  
    def maki_roll_calculator(self, rounds, users):
        maki_roll_counts = []
        for user in users:
            maki_roll_count = 0
            for element in user.inventory[rounds]:
                if element.type == "1xMaki Roll":
                    maki_roll_count+=1       
                if element.type == "2xMaki Roll":
                    maki_roll_count+=2   
                if element.type == "3xMaki Roll":
                    maki_roll_count+=3
            maki_roll_counts.append(maki_roll_count)
            
        players_with_max_maki_roll = 0
        players_with_2nd_max_maki_roll = 0
        max_maki_roll_count = max(maki_roll_counts)
        
        for i in range(len(users)):
            if maki_roll_counts[i] == max_maki_roll_count:
                players_with_max_maki_roll+=1
                maki_roll_counts[i] = -1
        max_maki_roll_count = max(maki_roll_counts)
        for i in range(len(users)):
            if maki_roll_counts[i] == max_maki_roll_count:
                players_with_2nd_max_maki_roll+=1
                maki_roll_counts[i] = -2
        if players_with_max_maki_roll == 1:
            for i in range(len(users)):    
                if maki_roll_counts[i] == -1:
                    users[i].points[rounds] += 6
                elif maki_roll_counts[i] == -2:
                    users[i].points[rounds] += math.floor(3/players_with_2nd_max_maki_roll) 
        else:
            for i in range(len(users)):    
                if maki_roll_counts[i] == -1:
                    users[i].points[rounds] += math.floor(6/players_with_max_maki_roll)

    def dumbling_calculator(self, rounds, users):
        for user in users:
            dumbling_count = 0
            for element in user.inventory[rounds]:
                if element.type == "Dumbling":
                    dumbling_count+=1
            if dumbling_count == 1:
                user.points[rounds] += 1
            if dumbling_count == 2:
                user.points[rounds] += 3
            if dumbling_count == 3:
                user.points[rounds] += 6
            if dumbling_count == 4:
                user.points[rounds] += 10
            if dumbling_count >= 5:
                user.points[rounds] += 15
        
    # 3 Sashimi = 10 points
    def sashimi_calculator(self, rounds, users):
        for user in users:
            sashimi_count = 0
            for element in user.inventory[rounds]:
                if element.type == "Sashimi":
                    sashimi_count+=1
            user.points[rounds] += 10*math.floor(sashimi_count/3)      

    # 2 Tempura = 5 points
    def tempura_calculator(self, rounds, users):
        for user in users:
            tempura_count = 0
            for element in user.inventory[rounds]:
                if element.type == "Tempura":
                    tempura_count+=1
            user.points[rounds] += 5*math.floor(tempura_count/2) 

    # Searches for nigiri in users inventory, if it finds one, it checks if its above a wasabi
    def wasabi_nigiri_calculator(self, rounds, users):
        for user in users:
            for i in range(self.total_turn):
                point = 0
                if user.inventory[rounds][i].type == "Salmon Nigiri":
                    point = 2
                if user.inventory[rounds][i].type == "Squid Nigiri":
                    point = 3
                if user.inventory[rounds][i].type == "Egg Nigiri":
                    point = 1
                if i>0 and user.inventory[rounds][i - 1].type == "Wasabi":
                    point*=3
                user.points[rounds] += point

    # Sums all puddings that user has in their all inventories and appends that to a list
    # Calculates how many players have max/min puddings and distributes points according to that
    '''
    def pudding_calculator(self, users): 
        pudding_counts = []
        for user in users:
            pudding_count = 0
            for inventory in user.inventory:
                for card in inventory:
                    if card.type == "Pudding":
                        pudding_count+=1
            pudding_counts.append(pudding_count)
            
        players_with_max_pudding = 0
        players_with_min_pudding = 0
        
        for i in range(4):
            if pudding_counts[i] == max(pudding_counts):
                players_with_max_pudding += 1
            if pudding_counts[i] == min(pudding_counts):
                players_with_min_pudding += 1
        for i in range(4):
            if pudding_counts[i] == max(pudding_counts):
                users[i].total_point += math.floor(6/players_with_max_pudding)
            if pudding_counts[i] == min(pudding_counts):
                users[i].total_point -= math.floor(6/players_with_min_pudding)    
    '''
    
    # Game doesn't ends btw, you have to close the gui to close game
    # I don't know how to fix it nor i care
    def end_the_game(self):
        for i in range(3):
            #self.soya_sauce_calculator(i, users)
            self.maki_roll_calculator(i, self.users)
            self.dumbling_calculator(i, self.users)
            self.sashimi_calculator(i, self.users)
            self.tempura_calculator(i, self.users)
            self.wasabi_nigiri_calculator(i, self.users)
        for user in self.users:
            user.total_point = sum(user.points)
        #self.pudding_calculator(self.users)
        
        print()
        winners = {}
        points = [user.total_point for user in self.users]
        
        for user in self.users:
            if user.total_point == max(points):
                winners[user.user_name] = user.total_point
        for name, points in winners.items():
            print(f'Winner is {name}: {points} points')
        print()
        sys.exit()

    def quit(self):
        sys.exit()
