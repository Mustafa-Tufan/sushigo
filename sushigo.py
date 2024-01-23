import random
import math

card_type = {"Tempura":14, "Sashimi":14, "Dumbling":14, "1xMaki Roll":6, "2xMaki Roll":12, 
             "3xMaki Roll":8, "Salmon Nigiri":10, "Squid Nigiri":5, "Egg Nigiri":5, 
             "Pudding":10, "Wasabi":6, "Chopsticks":4,"Soya Sauce": 4}
card_list = []
total_round = 3
total_turn = 8
total_user = 4

class Card:
    def __init__(self, type, id):
        self.id = id
        self.type = type
    def __str__(self):
        return f"{self.type}  "

class User:
    def __init__(self, user_type, user_id):
        self.user_type = user_type
        self.user_id = user_id
        self.user_name = user_type + " " + str(user_id)
        self.points = [0,0,0]
        self.total_point = 0
        self.user_drawn_cards = [[] for _ in range(3)]
        self.inventory = [[] for _ in range(3)]
    def __str__(self):
        return f"{self.user_type}({self.user_id}) - Points: {self.total_point}"

User1 = User("player",0)
User2 = User("bot",1)
User3 = User("bot",2)
User4 = User("bot",3)

users = [User1,User2,User3,User4]

def throw_randomly(rounds):
    for user in users:
        if user.user_type == "bot":
            drawn_card = random.choice(user.user_drawn_cards[rounds])
            user.user_drawn_cards[rounds].remove(drawn_card)
            user.inventory[rounds].append(drawn_card)
        
        
def deep_copy(list1, list2):
    for element in list2:
        list1.append(element)
    
def swap_the_cards(rounds):
    temp = []
    deep_copy(temp, users[3].user_drawn_cards[rounds])
    users[3].user_drawn_cards[rounds] = []
    deep_copy(users[3].user_drawn_cards[rounds], users[2].user_drawn_cards[rounds])
    users[2].user_drawn_cards[rounds] = []
    deep_copy(users[2].user_drawn_cards[rounds], users[1].user_drawn_cards[rounds])
    users[1].user_drawn_cards[rounds] = []
    deep_copy(users[1].user_drawn_cards[rounds], users[0].user_drawn_cards[rounds])
    users[0].user_drawn_cards[rounds] = []
    deep_copy(users[0].user_drawn_cards[rounds], temp)
    
def calculate_points():
    for i in range(3):
        soya_sauce_calculator(i)
        maki_roll_calculator(i)
        dumbling_calculator(i)
        sashimi_calculator(i)
        tempura_calculator(i)
        wasabi_nigiri_calculator(i)
    for user in users:
        user.total_point = sum(user.points)
    pudding_calculator()
    
# Counts total colors of users deck in a given round. To do that, it uses a dictionary with all values set to 1
# Values are different for nigiris and maki rolls because they count as single color
# Case 1: Person with soya souce has most colors    (2nd and 3rd loop)
# Case 2: Person with soya souce not has most colors    (1st loop)
# Case 3: More than one people share most colors and both have soya souce   (2nd and 3rd loop)
def soya_sauce_calculator(rounds):
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
    
# Calculates total maki rolls of an user in round (rounds), then it holds them in a list
# Counts how many #1 players and #2 players. Changes values on the list to make things easier
# My senses says i should revert the changes in the list after method ends but why?  
def maki_roll_calculator(rounds):
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
                users[i].points[rounds] += 6
            elif maki_roll_counts[i] == -2:
                users[i].points[rounds] += math.floor(3/players_with_2nd_max_maki_roll) 
    else:
        for i in range(4):    
            if maki_roll_counts[i] == -1:
                users[i].points[rounds] += math.floor(6/players_with_max_maki_roll)

def dumbling_calculator(rounds):
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
def sashimi_calculator(rounds):
    for user in users:
        sashimi_count = 0
        for element in user.inventory[rounds]:
            if element.type == "Sashimi":
                sashimi_count+=1
        user.points[rounds] += 10*math.floor(sashimi_count/3)      

# 2 Tempura = 5 points
def tempura_calculator(rounds):
    for user in users:
        tempura_count = 0
        for element in user.inventory[rounds]:
            if element.type == "Tempura":
                tempura_count+=1
        user.points[rounds] += 5*math.floor(tempura_count/2) 

# Searches for nigiri in users inventory, if it finds one, it checks if its above a wasabi
def wasabi_nigiri_calculator(rounds):
    for user in users:
        for i in range(8):
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
def pudding_calculator(): 
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

def reveal_the_winner():
    winners = {}
    points = [user.total_point for user in users]
    
    for user in users:
        if user.total_point == max(points):
            winners[user.user_name] = user.total_point
    for name, points in winners.items():
        print(f'Winner is {name}: {points} points')

for card, count in card_type.items():
    for i in range(count):
        card_list.append(Card(card, i))
        
random.seed(1)
drawn_cards = random.sample(card_list, total_turn*total_round*total_user)

for user in users:
    for i in range(total_round):
        for _ in range(total_turn):
            user.user_drawn_cards[i].append(drawn_cards.pop(0))

rounds = 0
while (rounds < total_round):
    turn = 0
    while (turn < total_turn):
        throw_randomly(rounds)
        print(*users[0].user_drawn_cards[rounds])
        print("Bot 1 card on top: " , users[1].inventory[rounds][len(users[1].inventory[rounds]) - 1])
        print("Bot 2 card on top: " , users[2].inventory[rounds][len(users[2].inventory[rounds]) - 1])
        print("Bot 3 card on top: " , users[3].inventory[rounds][len(users[3].inventory[rounds]) - 1])
        while True:
            try:
                card = int(input("Pick a card between 1 and 8: "))
                if 1 <= card <= len(users[0].user_drawn_cards[rounds]):
                    break
                else: #if user chooses a number outside of the given range
                    print("Number must be between 1 and 8. Please try again.")
            except ValueError: #if user enters a floating variable
                print("Invalid input. Please enter a valid number.")
      
        drawn_card = users[0].user_drawn_cards[rounds][card - 1]
        users[0].user_drawn_cards[rounds].remove(drawn_card)
        users[0].inventory[rounds].append(drawn_card)
        swap_the_cards(rounds)
        turn+=1
    rounds+=1

print()
calculate_points()
reveal_the_winner()
print()

'''
for i in range(3):
    for user in users:
        print(*user.inventory[i])
        print(user.points[i])
        print("---------")
    print("******************")
print(users[0].total_point)
print(users[1].total_point)
print(users[2].total_point)
print(users[3].total_point)
'''
