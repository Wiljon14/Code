import random
import TxtAdvGame

name = str
age = str
gold = int
health = float
max_health = float
starting_max_health = 20
exp = 0
level = 1
exp_to_level_up = (level*20) - 10
power_modifier = 0

char_class = "Not chosen"
char_choice_class = ["Mage","Knight"]
char_class_stats = {
    "Mage" : [],
    "Knight" : [],
}
area = "Forest"
areas = ["Home", "Shop", "Forest"]
available_enemys = ["Wolf","Bear"]
enemy_stats = {
    "Wolf" : {
    "HP" : 15,
    "EXP" : 10,
    "Gold" : 5,
    "Moves" : ["Wolf Bite"],
    },

    "Bear" : {
    "HP" : 30,
    "EXP" : 20,
    "Gold" : 10,
    "Moves" : ["Bear Bite"],

    },
}
available_moves = [] #make it so it changes depending on items in inventory :)
move_stats = {
    "player" : {
        "Iron Blade Slash" : [
            4, 6
        ],
        "Punch" : [
            2, 4
        ],
        "Golden Doom Blast" : [
            1,20
        ],
        "Dull Slash" : [
            3,5
        ],
        "Lesser Ball of Flame" : [
            0,10
        ],
    },
    "enemys" : {
        "Wolf Bite" : [
            1, 3
        ],
        "Bear Bite" : [
            4,5
        ]
    }
}

inventory = ["Wolf Tooth"]
raw_item_value = {
    #Weapons
    "Iron Sword" : {
        "Name" : "Iron Sword",
        "Value" : 5,
        "Description" : "A well made sword of iron. Great at cutting down foes.",
        "Move" : "Iron Blade Slash"
    },

    "Rusty Iron Sword" : {
        "Name" : "Rusty Iron Sword",
        "Value" : 1,
        "Description" : "It's a very old sword. Better than nothing, maybe?",
        "Move" : "Dull Slash"
    },

    "Old Spellbook Page" : {
        "Name" : "Old Spellbook Page",
        "Value" : 1,
        "Description" : "A page from your old Spellbook from magic school. Its a bit damaged",
        "Move" : "Lesser Ball of Flame",
    },

    "Gold Crown of Doom" : {
        "Name" : "Gold Crown of Doom",
        "Value" : 100,
        "Description" : "A Golden crown of doom and despair",
        "Move" : "Golden Doom Blast",
    },

    #Potions
    "Health Potion" : {
        "Name" : "Health Potion",
        "Value" : 3,
        "Description" : "A potion that regenerates flesh & mind, even lost limbs",
        "Move" : "N/A",
    },

    #Item Drops
    "Wolf Tooth" : {
        "Name" : "Wolf Tooth",
        "Value" : 4,
        "Description" : "The tooth from the local wolf population, could be sold",
        "Move" : "N/A",
    },
}

shop_items = [raw_item_value["Iron Sword"],raw_item_value["Health Potion"],raw_item_value["Gold Crown of Doom"]]

def stat_menu():
    print("---------------------------")
    print("Player: " + str(name))
    print("Class: " + str(char_class))
    print("Age: " + str(age))
    print("Gold: " + str(gold))
    print("HP: " + str(health) +"/"+ str(max_health))
    print("Level: " + str(level) + "("+ str(exp) +"/"+ str(exp_to_level_up) +")")
    print("Area: " + str(area))
    print("---------------------------")

def inventory_items_to_moves():
    global available_moves
    global inventory

    available_moves = ["Punch"]
    for i in inventory:
        if raw_item_value[i]["Move"] != "N/A":
            available_moves.append(raw_item_value[i]["Move"])
def main_screen(chosen):
    print("\033c", end="")
    

    global area
    global name
    global age
    global areas
    global gold
    global shop_items
    global inventory
    global health
    global max_health
    global exp
    global exp_to_level_up
    global level
    global available_moves
    global power_modifier

    available_moves = ["Punch"]
    
    leveld_up = False
    if exp >= exp_to_level_up:
        exp = exp - exp_to_level_up
        level += 1
        leveld_up = True
    exp_to_level_up = (level*20) - 10


    #Power modifier
    if char_class == "Mage":
        power_modifier = int((level * 1.2) - 1.2)
    else:
        power_modifier = level - 1
    #Health modifier
    if char_class == "Knight":
        max_health = int(starting_max_health + (3.5 * (level - 1)))
    else:
        max_health = starting_max_health + (3 * (level - 1))

    if leveld_up == True:
        health = max_health

    stat_menu()
    inventory_items_to_moves()

    if chosen == "Help":
        print("")
        print("Go to area. - goes to different area if possible")
        print("Inventory. - See inventory")
        print("Location specific stuff. V")
        if area == "Shop":
            print("  Browse - See what the shop has")
            print("  Sell - Sell stuff from your inventory")
        if area == "Forest":
            print("  Battle - Starts a battle against a random enemy")
        
        print("")
    elif chosen == "Go to area":
        print("Areas: " + str(areas))
        select = input("Select a area: ")
        if select in areas:
            area = select
        main_screen("")

    elif chosen == "Inventory":
        print(inventory)
        if input("Look closer at an item? (Y/N) ") == "Y":
            item_looked_closer_at = input("Item Name: ")
            if item_looked_closer_at in inventory:
                print("")
                print("Description: " + str(raw_item_value[item_looked_closer_at]["Description"]))
                print("Move it gives: " + str(raw_item_value[item_looked_closer_at]["Move"]))
            else:
                main_screen("")
        else:
            main_screen("")

    elif chosen == "Browse" and area == "Shop":
        print("")
        print("Items in the shop. V")
        i_num = 0
        for i in shop_items:
            i_num += 1
            print("ID: " + str(i_num) + " | " + str(i["Name"]) + ": With cost of: " + str(i["Value"]) + " Gold")
        print("")
        buying = input("Buy something? (Y/N) ")
        if buying == "Y":
            buy_choice = input("Insert Item ID to buy: ")
            if buy_choice == "":
                main_screen("")

            if gold >= shop_items[int(buy_choice) - 1]["Value"]:
                gold -= shop_items[int(buy_choice) - 1]["Value"]
                print("Remaining Gold: " + str(gold))
                print("Bought: " + shop_items[int(buy_choice) - 1]["Name"])
                inventory.append(shop_items[int(buy_choice) - 1]["Name"])
            else:
                print("Not enough Gold")

            input("Done? ")

            main_screen("")
        else:
            main_screen("")

    elif chosen == "Sell" and area == "Shop":
        print("")
        if inventory != []:
            print("Items in inventory. V")
            i_num = 0
            for i in inventory:
                i_num += 1
                i2 = raw_item_value[i]
                print("ID: " + str(i_num) + " | " + str(i) + ": With sell value of : " + str(i2["Value"] - 1) + " Gold")
            is_selling = input("Sell something? (Y/N) ")
            if is_selling == "Y":
                sold_item_ID = int(input("ID of item to sell: ")) - 1
                sell_value = raw_item_value[inventory[sold_item_ID]]["Value"] - 1
                print("Sold Item: " + inventory[sold_item_ID] + " for " + str(sell_value) + " Gold")
                gold += sell_value
                print("Current Gold: " + str(gold))
                del inventory[sold_item_ID]
                input("Done? ")
                main_screen("")
            else:
                main_screen("")
        else:
            print("Nothing to sell...")
            input("Done?")
            main_screen("") 

    elif chosen == "Battle" and area == "Forest":
        battle_screen(1,available_enemys[random.randint(0,1)],random.randint(1,3),0,0)
    
    elif chosen == "":
        print("Use Help if stuck")
        print("")
    
    choice = input()

    main_screen(choice)


#Battle stuff
def battle_screen(turn, enemy, enemy_lv,hp_left,enemy_max_hp):

    global exp
    global gold
    global health
    global area

    if turn == 1:
        enemy_hp = int(enemy_stats[enemy]["HP"]  + ((enemy_lv - 1) * enemy_stats[enemy]["HP"] * 0.2))
        enemy_max_hp = int(enemy_stats[enemy]["HP"]  + ((enemy_lv - 1) * enemy_stats[enemy]["HP"] * 0.2))
    else:
        enemy_hp = hp_left

    print("\033c", end="")
    stat_menu()
    print("Battle turn: " + str(turn))
    print(f"Enemy: {enemy} LV:{enemy_lv} | ({enemy_hp}/{enemy_max_hp})")
    print("---------------------------")

    input("Attack!")
    chosen_attack = choose_attack(turn,enemy,enemy_lv,enemy_hp,enemy_max_hp)
    enemy_hp_to_lose = (random.randint(move_stats["player"][chosen_attack][0],move_stats["player"][chosen_attack][1])) + (power_modifier)
    enemy_hp -= enemy_hp_to_lose
    #Refreshes battle screen to accuret HP
    print("\033c", end="")
    stat_menu()
    print("Battle turn: " + str(turn))
    print(f"Enemy: {enemy} LV:{enemy_lv} | ({enemy_hp}/{enemy_max_hp})")
    print("---------------------------")

    print(f"Enemy lost {enemy_hp_to_lose} HP to {chosen_attack}")
    print("")
    #
    if enemy_hp <= 0:
        print("Battle over. Well done :)")
        #rewards for winning
        exp_gain = int(enemy_stats[enemy]["EXP"] + ((enemy_lv - 1) * enemy_stats[enemy]["EXP"] * 0.2))
        gold_gain = int(enemy_stats[enemy]["Gold"] + ((enemy_lv - 1) * enemy_stats[enemy]["Gold"] * 0.2))
        print("EXP gained: " + str(exp_gain))
        print("Gold gained: " + str(gold_gain))
        exp += exp_gain
        gold += gold_gain
        input("")
        main_screen("")
    else:
        #Enemy Attack
        enemy_chosen_move = random.choice(enemy_stats[enemy]["Moves"])
        enemy_chosen_move_damage_random_part = random.randint(move_stats["enemys"][enemy_chosen_move][0],move_stats["enemys"][enemy_chosen_move][1])
        enemy_chosen_move_damage = int(enemy_chosen_move_damage_random_part + ((enemy_lv-1) * 0.2 * enemy_chosen_move_damage_random_part))
        health -= enemy_chosen_move_damage
        #Refreshes battle screen to accuret HP
        print("\033c", end="")
        stat_menu()
        print("Battle turn: " + str(turn))
        print(f"Enemy: {enemy} LV:{enemy_lv} | ({enemy_hp}/{enemy_max_hp})")
        print("---------------------------")

        print(f"Enemy lost {enemy_hp_to_lose} HP to {chosen_attack}")
        print("")
        print(f"{enemy} used {enemy_chosen_move}, dealt {enemy_chosen_move_damage} damage")
        #
        if health <= 0:
            print("")
            print("You lost. To bad so sad :(")
            print("Lost half your Gold")
            health = max_health
            area = "Home"
            gold = int(gold / 2)
            input()
            main_screen("")
        else:
            input("")
            battle_screen(turn+1,enemy,enemy_lv,enemy_hp,enemy_max_hp)

def choose_attack(turn,enemy,enemy_lv,enemy_hp,enemy_max_hp):
    print("\033c", end="")
    stat_menu()
    print("Battle turn: " + str(turn))
    print(f"Enemy: {enemy} LV:{enemy_lv} | ({enemy_hp}/{enemy_max_hp})")
    print("---------------------------")    
    print("Avaible Moves: " + str(available_moves))
    print("---------------------------")

    return choice_in_choose_attack()

def choice_in_choose_attack():
    while True:
        chosen_attack = input("Choose Move: ")
        if chosen_attack in available_moves:
            return chosen_attack
        else:
            print("Invalid")


#Pre-game choices
def name_select(redo):
    global name
    print("\033c", end="")
    if redo is False:
        print("What's your name?")
    if redo is True:
        print("Please enter name")
    name = input()
    if name == "":
        name_select(True)
name_select(False)

def age_select(redo):
    global age
    print("\033c", end="")
    if redo is False:
        print("And your age?")
    if redo is True:
        print("Please enter a whole number (ex. 16, 35)")
    age = input()
    if not age.isdigit():
        age_select(True)
age_select(False)

def class_select(redo):
    global char_class
    print("\033c", end="")
    if redo is False:
        print("Lastly what class do you whant to play?")
        print("Valid choices: " + str(char_choice_class))
    if redo is True:
        print("Please enter a valid class")
        print("Valid choices: " + str(char_choice_class))
    char_class = input()
    if not char_class in char_choice_class:
        class_select(True)
class_select(False)

if char_class == "Knight":
    inventory.append("Rusty Iron Sword")
if char_class == "Mage":
    inventory.append("Old Spellbook Page")


gold = 15
max_health = starting_max_health
health = max_health



main_screen("")


