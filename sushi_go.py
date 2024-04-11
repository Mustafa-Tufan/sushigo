import random
import math
import sys
import time
from gui import GUI
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

# Commented one is for actual game, other one is for simplified version
'''
card_type = {"Tempura":14, "Sashimi":14, "Dumbling":14, "1xMaki Roll":6, "2xMaki Roll":12, 
             "3xMaki Roll":8, "Salmon Nigiri":10, "Squid Nigiri":5, "Egg Nigiri":5, 
             "Pudding":10, "Wasabi":6, "Chopsticks":4,"Soya Sauce": 4}
'''
card_type = {"Tempura":16, "Sashimi":16, "Dumbling":16, "1xMaki Roll":8, "2xMaki Roll":15, 
             "3xMaki Roll":10, "Salmon Nigiri":12, "Squid Nigiri":8, "Egg Nigiri":8, 
             "Wasabi":6}

# List of all cards
card_list = []

unique_card_list = ["Tempura", "Sashimi", "Dumbling", "1xMaki Roll", "2xMaki Roll", 
             "3xMaki Roll", "Salmon Nigiri", "Squid Nigiri", "Egg Nigiri", "Wasabi"]

class Card:
    def __init__(self, type, id, index):
        self.id = id                      
        self.type = type                    
        self.index = index                
    def __str__(self):
        return f"{self.type}  "

class User:
    clicked_card = 0
    quit_game = 0
    root = None
    def __init__(self, user_type, user_name, user_id, game):
        self.user_type = user_type                          
        self.user_id = user_id
        self.user_name = user_name
        self.points = [0,0,0]
        self.total_point = 0
        self.user_drawn_cards = [[] for _ in range(3)]
        self.inventory = [[] for _ in range(3)]
        self.card_positions = []
        self.front_position = (0,0)
        if user_type == "bot":
            self.root = game.create_monte_carle_tree()
            self.sequence = game.max_sequence(self)
        
    def __str__(self):
        return f"{self.user_type}({self.user_id}) - Points: {self.total_point}"
    
    # Method to throw cards, if it called for a bot, game checks if bot needs to use monte carlo tree
    # or best sequence, if it called for a user, game connects to gui
    # Commented part is for playing in termina
    def throw_card(self, rounds):
        if self.user_type == "bot" and self.root.children: # type: ignore
            max = 0
            for node in self.root.children: #type: ignore
                if node.value > max and self.isPresent(node.name, rounds):
                    max = node.value
            for node in self.root.children: #type: ignore
                if node.value == max:
                    for card in self.user_drawn_cards[rounds]:
                        if card.type == node.name:
                           drawn_card = card 
                           break
                    self.user_drawn_cards[rounds].remove(drawn_card)
                    self.inventory[rounds].append(drawn_card)
                    self.root = node
                    break
            return
        
        elif self.user_type == "bot":
            drawn_card = self.sequence
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
        if self.user_type == "player":
            while (self.clicked_card == 0):
                if (self.quit_game == 1): 
                    sys.exit()
                card = self.clicked_card
            drawn_card = self.user_drawn_cards[rounds][int(card) - 1]
            self.user_drawn_cards[rounds].remove(drawn_card)
            self.inventory[rounds].append(drawn_card)
            self.clicked_card = 0
    
    # Checks if desired card is avaible in user's deck
    def isPresent(self, str, rounds):
        card_listx = []
        for card in self.user_drawn_cards[rounds]:
            card_listx.append(card.type)
        if card_listx.__contains__(str):
            return True
        return False
            
class Game:
    users = []
    total_round = 0
    total_turn = 0
    total_user = 0
    current_round = 0
    current_turn = 0
    user_turn = 0
    quit_game = 0
    ended = 0
    
    def __init__(self):
        self.prepare_game()
    
    # Creates the game for desired player count, creates cards and sets some variables 
    def prepare_game(self):
        #print("\nSushi Go! can be played with 2-5 people\n")
        print("\nSushi Go! is played with 4 people\n")
        while True:
            try:
                player_count = int(input("Enter player count: "))
                bot_count = int(input("Enter bot count: "))
                self.total_user = player_count + bot_count
                '''
                if not (2 <= self.total_user <= 5):
                    raise ValueError("Total player and bot count must be between 2 and 5.")
                '''
                if not (self.total_user == 4):
                    raise ValueError("Total player and bot count must be 4.")
                break  # Valid counts, so exit the loop
            
            except ValueError as e:
                print(e)
        
        for i in range(self.total_user):
            if i < player_count:
                self.users.append(User("player", input(f"Enter player {i + 1}'s name: "), i, self))
            else:
                self.users.append(User("bot", f"bot {i}", i, self))
        
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
                    
        #print("\nType q anytime to quit") 

    def play(self):
        for i in range(self.total_round):
            self.current_round = i
            self.play_a_round(i)
            self.current_turn = 0
            self.refresh_monte_carlo()
        self.end_the_game()

    def play_a_round(self,rounds):
        for j in range(self.total_turn):
            self.current_turn = j
            self.play_a_turn(rounds)
                
    def play_a_turn(self, rounds):
        self.refresh_sequence()
        for user in self.users:
            if user.user_type == "player":
                pass
                #print("\n",*user.user_drawn_cards[rounds],"\n")
            user.throw_card(rounds)
            self.user_turn += 1
        #self.give_information(rounds)
        self.swap_the_cards(rounds)
        self.current_turn += 1
        self.user_turn = 0
    
    # Terminal related     
    def give_information(self, rounds):
        print("")
        for user in self.users:
            print(f"{user.user_name} card on top: ", user.inventory[rounds][len(user.inventory[rounds]) - 1])
            pass
        
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
    def maki_roll_calculator(self, sequences):
        points = [0, 0, 0, 0]
        maki_roll_counts = []
        for sequence in sequences:
            maki_roll_count = 0
            for element in sequence: 
                if type(element) == str:
                    break
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
        
        for i in range(4):
            if maki_roll_counts[i] == max_maki_roll_count:
                players_with_max_maki_roll+=1
                maki_roll_counts[i] = -1
        max_maki_roll_count = max(maki_roll_counts)
        for i in range(4):
            if maki_roll_counts[i] == max_maki_roll_count:
                players_with_2nd_max_maki_roll+=1
                maki_roll_counts[i] = -2
        if players_with_max_maki_roll == 1:
            for i in range(4):    
                if maki_roll_counts[i] == -1:
                    points[i] = 6
                elif maki_roll_counts[i] == -2:
                    points[i] = math.floor(3/players_with_2nd_max_maki_roll) 
        else:
            for i in range(4):    
                if maki_roll_counts[i] == -1:
                    points[i] = math.floor(6/players_with_max_maki_roll)
        
        return points

    def dumbling_calculator(self, sequences):
        index = 0
        points = [0,0,0,0] 
        for sequence in sequences:
            dumbling_count = 0
            for element in sequence:
                if type(element) == str:
                    break
                if element.type == "Dumbling":
                    dumbling_count+=1
            if dumbling_count == 1:
                points[index] = 1
            if dumbling_count == 2:
                points[index] = 3
            if dumbling_count == 3:
                points[index] = 6
            if dumbling_count == 4:
                points[index] = 10
            if dumbling_count >= 5:
                points[index] = 15
            index += 1
        return points
        
    # 3 Sashimi = 10 points
    def sashimi_calculator(self, sequences):
        index = 0
        points = [0,0,0,0]        
        for sequence in sequences:
            sashimi_count = 0
            for element in sequence:
                if type(element) == str:
                    break
                if element.type == "Sashimi":
                    sashimi_count+=1
            points[index] = 10*math.floor(sashimi_count/3)     
            index += 1      
        return points

    # 2 Tempura = 5 points
    def tempura_calculator(self, sequences):
        index = 0
        points = [0,0,0,0]
        for sequence in sequences:
            tempura_count = 0
            for element in sequence:
                if type(element) == str:
                    break
                if element.type == "Tempura":
                    tempura_count+=1
            points[index] = 5*math.floor(tempura_count/2) 
            index += 1
        return points

    # Searches for nigiri in users inventory, if it finds one, it checks if its above a wasabi
    def wasabi_nigiri_calculator(self, sequences):
        index = 0
        points = [0,0,0,0]
        for sequence in sequences:
            point_sum = 0
            for i in range(self.total_turn):
                point = 0
                if type(sequence[i]) == str:
                    break
                if sequence[i].type == "Salmon Nigiri":
                    point = 2
                if sequence[i].type == "Squid Nigiri":
                    point = 3
                if sequence[i].type == "Egg Nigiri":
                    point = 1
                if i>0 and sequence[i - 1].type == "Wasabi":
                    point*=3
                point_sum += point
            points[index] = point_sum
            index += 1
        return points
    
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
    
    # Calculates total points of every user for desired round
    # Or we can use this method for 2nd phase of game, thats why param is called sequences
    def calculate_round(self, sequences):
        points = [0,0,0,0]
        points1 = self.maki_roll_calculator(sequences)
        points2 = self.dumbling_calculator(sequences)
        points3 = self.sashimi_calculator(sequences)
        points4 = self.tempura_calculator(sequences)
        points5 = self.wasabi_nigiri_calculator(sequences)
        for i in range(4):
            points[i] = points1[i] + points2[i] + points3[i] + points4[i] + points5[i]
        return points
    
    # Calculates total points and gives those informations to gui
    # Game doesn't ends when you call this, you have to close the gui to close game
    def end_the_game(self):
        for i in range(3):
            #self.soya_sauce_calculator(i, users)
            sequences = [self.users[0].inventory[i], self.users[1].inventory[i], self.users[2].inventory[i], self.users[3].inventory[i]]
            points = self.calculate_round(sequences)
            self.users[0].points[i] += points[0]
            self.users[1].points[i] += points[1]
            self.users[2].points[i] += points[2]
            self.users[3].points[i] += points[3]
        for user in self.users:
            user.total_point = sum(user.points)
        #self.pudding_calculator(self.users)
        
        #print()
        winners = {}
        points = [user.total_point for user in self.users]
        win_messages = ""
        rankings = []
        
        for user in self.users:
            rankings.append(user)
            if user.total_point == max(points):
                winners[user.user_name] = user.total_point
        for name, points in winners.items():
            win_message = f'Winner is {name}: {points} points'
            #print(win_message)
            win_messages += win_message
            
        sorted_rankings = sorted(rankings, key=lambda x: x.points, reverse=True)
        
        self.First_place = f'1st Place: {sorted_rankings[0].user_name}: {sorted_rankings[0].total_point} points'
        self.Second_place = f'2nd Place: {sorted_rankings[1].user_name}: {sorted_rankings[1].total_point} points'
        self.Third_place = f'3rd Place: {sorted_rankings[2].user_name}: {sorted_rankings[2].total_point} points'
        self.Forth_place = f'4th Place: {sorted_rankings[3].user_name}: {sorted_rankings[3].total_point} points'
        
        #print()
        self.ended = 1
        self.end_message = win_messages

    def quit(self):
        sys.exit()
    
    # Creates Monte Carlo tree
    def create_monte_carle_tree(self): 
        n = 100000
        states = {}
        start = time.time()
        for i in range(n):
            state = tuple(random.choices(unique_card_list, k=self.total_user-1))
            if states.get(state) == None: states[state] = 1
            else: states[state] = states[state] + 1
                
        for state in states:
            states[state] = states[state] / n
        '''
        for key, value in states.items():
            print(key[0], key[1], key[2], ':', value)
        '''    
        root = self.create_choices_tree()
        '''
        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.value))
        '''
        strategies = {}
        for key, value in states.items():
            strategies[key] = round(value + 0.1 * self.evaluate(key), 5)

        root = self.update_node_value(root, strategies)

        end = time.time()
        #print(end-start, "CPU TIME")

        return root

    # Helper method
    # Currently works with 4 players
    def create_choices_tree(self):
        root = Node("", value = 0)
        for element in unique_card_list:
            node1 = Node(element, parent=root, value=0)
            for element in unique_card_list:
                node2 = Node(element, parent=node1, value=0)
                for element in unique_card_list:
                    Node(element, parent=node2, value=0)
        return root
    
    # Evaluation function
    # This is terrible
    def evaluate(self, state):
        value = 0
        for card in state:
            if card == "Tempura": value += 2.5
            if card == "Sashimi": value += 3.3
            if card == "Dumbling": value += 2
            if card == "1xMaki Roll": value += 0.5
            if card == "2xMaki Roll": value += 1
            if card == "3xMaki Roll": value += 1.5
            if card == "Salmon Nigiri": value += 2
            if card == "Squid Nigiri": value += 3
            if card == "Egg Nigiri": value += 1
            if card == "Wasabi": value += 3
        return value
    
    # Currently works with 4 players
    def update_node_value(self, root, strategies):
        for key, value in strategies.items():
            cur_node = root
            for element in key:
                cur_node = cur_node.children[unique_card_list.index(element)] #TODO Integer değer istiyo ama ben string veriyom
            cur_node.value = value
        zort = 0
        for node1 in root.children:
            max1 = 0
            for node2 in node1.children:
                max2 = 0
                for node3 in node2.children:
                    zort = zort + 1
                    if node3.value > max2:
                        max2 = node3.value
                node2.value = max2
                if node2.value > max1:
                        max1 = node2.value
            node1.value = max1
        return root
    
    # Finds the best card throwing sequence for desired user
    # I know it looks simplifiable.
    def max_sequence(self, user):
        if (self.current_turn < 3):
            return
        sequences = []
        
        if (self.current_turn == 3):
            for cards1 in user.user_drawn_cards[self.current_round]:
                for cards2 in self.users[(self.users.index(user) + 3) % 4].user_drawn_cards[self.current_round]:
                    for cards3 in self.users[(self.users.index(user) + 2) % 4].user_drawn_cards[self.current_round]:
                        for cards4 in self.users[(self.users.index(user) + 1) % 4].user_drawn_cards[self.current_round]:
                            for cards5 in user.user_drawn_cards[self.current_round]:
                                sequences.append((cards1,cards2,cards3,cards4,cards5))
                                
        if (self.current_turn == 4):
            for cards1 in user.user_drawn_cards[self.current_round]:
                for cards2 in self.users[(self.users.index(user) + 3) % 4].user_drawn_cards[self.current_round]:
                    for cards3 in self.users[(self.users.index(user) + 2) % 4].user_drawn_cards[self.current_round]:
                        for cards4 in self.users[(self.users.index(user) + 1) % 4].user_drawn_cards[self.current_round]:
                            sequences.append((cards1,cards2,cards3,cards4))
                            
        if (self.current_turn == 5):
            for cards1 in user.user_drawn_cards[self.current_round]:
                for cards2 in self.users[(self.users.index(user) + 3) % 4].user_drawn_cards[self.current_round]:
                    for cards3 in self.users[(self.users.index(user) + 2) % 4].user_drawn_cards[self.current_round]:
                        sequences.append((cards1,cards2,cards3))
                        
        if (self.current_turn == 6):
            for cards1 in user.user_drawn_cards[self.current_round]:
                for cards2 in self.users[(self.users.index(user) + 3) % 4].user_drawn_cards[self.current_round]:
                    sequences.append((cards1,cards2))
                    
        if (self.current_turn == 7):    
            for cards1 in user.user_drawn_cards[self.current_round]:
                sequences.append((cards1))
        
        combinations = {}
        empty = ["","","","","","","",""]
        
        for sequence in sequences:
            all_cards = []
            for card in user.inventory[self.current_round]:
                all_cards.append(card)
            if (self.current_turn < 7):
                for card in sequence:
                    all_cards.append(card)
            else:
                all_cards.append(sequence)
            input = [all_cards, empty, empty, empty]
            points = self.calculate_round(input)
            combinations[tuple(all_cards)] = points[0]
            
        max = 0
        best = []
        for combination in combinations:
            if combinations[combination] > max:
                max = combinations[combination]
                best = combination       
        
        return list(best)[self.current_turn]
    
    # 
    def refresh_sequence(self):
        for user in self.users:
            if user.user_type == "bot":
                user.sequence = self.max_sequence(user)
            
    def refresh_monte_carlo(self):
        for user in self.users:
            if user.user_type == "bot":
                user.root = self.create_monte_carle_tree()
