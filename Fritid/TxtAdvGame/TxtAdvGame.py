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
char_choice_class = ["mage","knight"]
char_class_stats = {
    "mage" : [],
    "knight" : [],
}
area = "forest"
areas = ["home", "store", "forest"]
available_enemys = ["wolf","bear"]
enemy_stats = {
    "wolf" : {
    "HP" : 15,
    "EXP" : 10,
    "gold" : 5,
    "moves" : ["wolf bite"],
    },

    "bear" : {
    "HP" : 30,
    "EXP" : 20,
    "gold" : 10,
    "moves" : ["bear bite"],

    },
}
available_moves = [] #make it so it changes depending on items in inventory :)
move_stats = {
    "player" : {
        "iron blade slash" : [
            4, 6
        ],
        "punch" : [
            2, 4
        ],
        "golden doom blast" : [
            1,20
        ],
        "dull slash" : [
            3,5
        ],
        "lesser ball of flame" : [
            0,10
        ],
    },
    "enemys" : {
        "wolf bite" : [
            1, 3
        ],
        "bear bite" : [
            4,5
        ]
    }
}

inventory = ["wolf tooth"]
raw_item_value = {
    #Weapons
    "iron sword" : {
        "name" : "iron sword",
        "value" : 5,
        "description" : "A well made sword of iron. Great at cutting down foes.",
        "move" : "iron blade slash"
    },

    "rusty iron sword" : {
        "name" : "rusty iron sword",
        "value" : 1,
        "description" : "It's a very old sword. Better than nothing, maybe?",
        "move" : "dull slash"
    },

    "old spellbook page" : {
        "name" : "old spellbook page",
        "value" : 1,
        "description" : "A page from your old Spellbook from magic school. Its a bit damaged",
        "move" : "lesser ball of flame",
    },

    "gold crown of doom" : {
        "name" : "gold crown of doom",
        "value" : 100,
        "description" : "A Golden crown of doom and despair",
        "move" : "golden doom blast",
    },

    #Potions
    "health potion" : {
        "name" : "health potion",
        "value" : 3,
        "description" : "A potion that regenerates flesh & mind, even lost limbs",
        "move" : "N/A",
    },

    #Item Drops
    "wolf tooth" : {
        "name" : "wolf tooth",
        "value" : 4,
        "description" : "The tooth from the local wolf population, could be sold",
        "move" : "N/A",
    },

    #Artifacts
    "sleeping bag" : {
        "name" : "sleeping bag",
        "value" : 15,
        "description" : "A potato bag with some wool in it, guess you could sleep in it. (Allows. you to sleep anywhere)",
        "move" : "N/A",
    },
    
}

shop_items = [raw_item_value["iron sword"],raw_item_value["health potion"],raw_item_value["gold crown of doom"],raw_item_value["sleeping bag"]]



def stat_menu(clear):
    if clear == True:
        print("\033c", end="")
    print("---------------------------")
    print("Player: " + str(name))
    print("Class: " + str(char_class).capitalize())
    print("Age: " + str(age))
    print("Gold: " + str(gold))
    print("HP: " + str(health) +"/"+ str(max_health))
    print("Level: " + str(level) + "("+ str(exp) +"/"+ str(exp_to_level_up) +")")
    print("Area: " + str(area).capitalize())
    print("---------------------------")

def battle_stat_menu(turn,enemy,enemy_lv,enemy_hp,enemy_max_hp):
    print("Battle turn: " + str(turn))
    print(f"Enemy: {enemy.capitalize()} LV:{enemy_lv} | ({enemy_hp}/{enemy_max_hp})")
    print("---------------------------")

def inventory_items_to_moves():
    global available_moves
    global inventory

    available_moves = ["punch"]
    for i in inventory:
        if raw_item_value[i]["move"] != "N/A":
            available_moves.append(raw_item_value[i]["move"])



def main_screen(chosen):


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
    if char_class == "mage":
        power_modifier = int((level * 1.2) - 1.2)
    else:
        power_modifier = level - 1
    #Health modifier
    if char_class == "knight":
        max_health = int(starting_max_health + (3.5 * (level - 1)))
    else:
        max_health = starting_max_health + (3 * (level - 1))

    if leveld_up == True:
        health = max_health

    stat_menu(True)

    inventory_items_to_moves()

    if chosen.lower() in commands:
        commands[chosen.lower()]()
    else:
        print("Use Help if stuck")
        print("")
        main_screen(input())
    main_screen(input())


#command menu choices
def help():
        print("")
        print("Go to area. - goes to different area if possible")
        print("Inventory. - See inventory")
        print("Location specific stuff. V")
        if area == "store":
            print("  Shop - See what the store has")
            print("  Sell - Sell stuff from your inventory")
        if area == "forest":
            print("  Battle - Starts a battle against a random enemy")
        if area == "home":
            print("  Sleep - Take a nap and heal to full HP")
        
        main_screen(input())

def check_inventory():
    print(inventory)
    if input("Look closer at an item? (Y/N) ") == "Y":
        item_looked_closer_at = input("Item Name: ").lower()
        if item_looked_closer_at in inventory:
            print("")
            print("Description: " + str(raw_item_value[item_looked_closer_at]["description"]))
            print("Move it gives: " + str(raw_item_value[item_looked_closer_at]["move"]))
        else:
            main_screen("")
    else:
        main_screen("")

def go_to_area():
    global area

    print("Areas: " + str(areas))
    select = input("Select a area: ")
    if select.lower() in areas:
        area = select
        main_screen("")

def start_battle():
    if area == "forest":
        battle_screen(1,available_enemys[random.randint(0,1)],random.randint(1,3),0,0)
    else:
        print("No enemys around")
        main_screen(input())

def shop():
    global inventory
    global gold

    if area == "store":
        print("")
        print("Items in the shop. V")
        i_num = 0
        for i in shop_items:
            i_num += 1
            print("ID: " + str(i_num) + " | " + str(i["name"]) + ": With cost of: " + str(i["value"]) + " Gold")
        print("")
        buying = input("Buy something? (Y/N) ")
        if buying == "Y":
            buy_choice = input("Insert Item ID to buy: ")
            if buy_choice == "":
                main_screen("")

            if gold >= shop_items[int(buy_choice) - 1]["value"]:
                gold -= shop_items[int(buy_choice) - 1]["value"]
                print("Remaining Gold: " + str(gold))
                print("Bought: " + shop_items[int(buy_choice) - 1]["name"])
                inventory.append(shop_items[int(buy_choice) - 1]["name"])
            else:
                print("Not enough Gold")

            input("Done? ")

            main_screen("")
        else:
            main_screen("")
    else:
        print("there is no store around")
        main_screen(input())

def sell():
    global inventory
    global gold

    if area == "store":
        print("")
        if inventory != []:
            print("Items in inventory. V")
            i_num = 0
            for i in inventory:
                i_num += 1
                i2 = raw_item_value[i]
                print("ID: " + str(i_num) + " | " + str(i) + ": With sell value of : " + str(i2["value"] - 1) + " Gold")
            is_selling = input("Sell something? (Y/N) ")
            if is_selling == "Y":
                sold_item_ID = int(input("ID of item to sell: ")) - 1
                sell_value = raw_item_value[inventory[sold_item_ID]]["value"] - 1
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
    else:
        print("Theres is no one here to sell to")
        input("")
        main_screen("")

def sleep():
    global health
    if area == "home":
        health = max_health
        print("You took a nice nap in your bed, and feel refreshed")
        input("")
        main_screen("")
    elif "sleeping bag" in inventory:
        health = max_health
        print("You took a nap in a potato bag(?), at least you feel refreshed")
        input("")
        main_screen("")
        
    else:
        print("No where to sleep around here")
        input("")
        main_screen("")

commands = {
    "help" : help,
    "go to area" : go_to_area,
    "inventory" : check_inventory,
    #area specific
    "battle" : start_battle,
    "shop" : shop,
    "sell" : sell,
    "sleep" : sleep,
    }
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

    stat_menu(True)
    battle_stat_menu(turn, enemy, enemy_lv,enemy_hp,enemy_max_hp)

    input("Attack!")
    chosen_attack = choose_attack(turn,enemy,enemy_lv,enemy_hp,enemy_max_hp)
    enemy_hp_to_lose = (random.randint(move_stats["player"][chosen_attack][0],move_stats["player"][chosen_attack][1])) + (power_modifier)
    enemy_hp -= enemy_hp_to_lose
    #Refreshes battle screen to accuret HP
    stat_menu(True)
    battle_stat_menu(turn, enemy, enemy_lv,enemy_hp,enemy_max_hp)


    print(f"Enemy lost {enemy_hp_to_lose} HP to {chosen_attack}")
    print("")
    #
    if enemy_hp <= 0:
        print("Battle over. Well done :)")
        #rewards for winning
        exp_gain = int(enemy_stats[enemy]["EXP"] + ((enemy_lv - 1) * enemy_stats[enemy]["EXP"] * 0.2))
        gold_gain = int(enemy_stats[enemy]["gold"] + ((enemy_lv - 1) * enemy_stats[enemy]["gold"] * 0.2))
        print("EXP gained: " + str(exp_gain))
        print("Gold gained: " + str(gold_gain))
        exp += exp_gain
        gold += gold_gain
        input("")
        main_screen("")
    else:
        #Enemy Attack
        enemy_chosen_move = random.choice(enemy_stats[enemy]["moves"])
        enemy_chosen_move_damage_random_part = random.randint(move_stats["enemys"][enemy_chosen_move][0],move_stats["enemys"][enemy_chosen_move][1])
        enemy_chosen_move_damage = int(enemy_chosen_move_damage_random_part + ((enemy_lv-1) * 0.2 * enemy_chosen_move_damage_random_part))
        health -= enemy_chosen_move_damage
        #Refreshes battle screen to accuret HP
        stat_menu(True)
        battle_stat_menu(turn, enemy, enemy_lv,enemy_hp,enemy_max_hp)


        print(f"Enemy lost {enemy_hp_to_lose} HP to {chosen_attack}")
        print("")
        print(f"{enemy} used {enemy_chosen_move}, dealt {enemy_chosen_move_damage} damage")
        #
        if health <= 0:
            print("")
            print("You lost. To bad so sad :(")
            print("Lost half your Gold")
            health = max_health
            area = "home"
            gold = int(gold / 2)
            input()
            main_screen("")
        else:
            input("")
            battle_screen(turn+1,enemy,enemy_lv,enemy_hp,enemy_max_hp)

def choose_attack(turn,enemy,enemy_lv,enemy_hp,enemy_max_hp):
    stat_menu(True)
    battle_stat_menu(turn, enemy, enemy_lv,enemy_hp,enemy_max_hp)
    print("Avaible Moves: " + str(available_moves))
    print("---------------------------")

    return choice_in_choose_attack()

def choice_in_choose_attack():
    while True:
        chosen_attack = input("Choose Move: ").lower()
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
    char_class = input().lower()
    if not char_class in char_choice_class:
        class_select(True)
class_select(False)

if char_class == "knight":
    inventory.append("rusty iron sword")
if char_class == "mage":
    inventory.append("old spellbook page")


gold = 15
max_health = starting_max_health
health = max_health


main_screen("")


