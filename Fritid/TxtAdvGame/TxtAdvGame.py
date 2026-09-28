import random

characters = {
    "allied" : {
        "player" : {
            "name" : str,
            "age" : str,
            "gold" : int,

            "class" : "Not chosen",
            
            "health" : int,
            "max_health" : int,
            "starting_max_health" : 20,

            "exp" : 0,
            "level" : 1,
            "exp_to_level_up" : 10, # (level*20) - 10 

            "power_modifier" : 0,
        }
    },
    "enemys" : {
        
    }
}
characters["allied"]["player"]["class"]
#battle variables
enemy = str
enemy_hp = 0
enemy_max_hp = 0
enemy_lv = 0

exp_gain = 0
gold_gain = 0
turn = 0
turn_order = []
turn_in_turn_order = 0
battle_over = True

char_choice_class = ["mage","knight"]
char_class_stats = {
    "mage" : {
        "power_multi" : 0.15, #per level
        "health_multi" : 1, 
        "starting_gear" : [],
    },
    "knight" : {
        "power_multi" : 0.1, #per level
        "health_multi" : 1.2, 
        "starting_gear" : [],

    },
}
area = "forest"
areas = ["home", "store", "forest"]
enemy_stats = {
    "wolf" : {
        "HP" : 15,
        "EXP" : 10,
        "gold" : 5,
        "moves" : ["wolf bite"],
    },

    "alpha wolf" : {
        "HP" : 18,
        "EXP" : 15,
        "gold" : 7,
        "moves" : ["wolf bite","prime alpha howl"],
    },

    "bear" : {
        "HP" : 22,
        "EXP" : 20,
        "gold" : 8,
        "moves" : ["bear bite"],
    },

    "tree beast" : {
        "HP" : 28,
        "EXP" : 30,
        "gold" : 10,
        "moves" : ["tree slam","leaf beam"],
    },
}

enemys_in_area = {
    "forest" : {
        "easy" : ["wolf"],
        "medium" : ["bear","alpha wolf"],
        "hard" : ["tree beast"],
    } 
}
available_moves = [] #make it so it changes depending on items in inventory :)
move_stats = {
    "player" : {
        "iron blade slash" : [
            5, 7
        ],
        "punch" : [
            2, 4
        ],
        "golden doom blast" : [
            1, 20
        ],
        "dull slash" : [
            4, 6
        ],
        "lesser ball of flame" : [
            1, 10
        ],
    },
    "enemys" : {
        "wolf bite" : [
            3, 4
        ],
        "prime alpha howl" : [
            2,8,
        ],
        "bear bite" : [
            4, 5
        ],
        "tree slam" : [
            6, 6
        ],
        "leaf beam" : [
            5, 10
        ]
    }
}

inventory = ["wolf tooth","health potion","greater health potion"]
raw_item_value = {
    #Weapons
    "iron sword" : {
        "name" : "iron sword",
        "value" : 5,
        "description" : "A well made sword of iron. Great at cutting down foes.",
        "move" : "iron blade slash",
        "consumable" : False,
    },

    "rusty iron sword" : {
        "name" : "rusty iron sword",
        "value" : 1,
        "description" : "It's a very old sword. Better than nothing, maybe?",
        "move" : "dull slash",
        "consumable" : False,

    },

    "old spellbook page" : {
        "name" : "old spellbook page",
        "value" : 1,
        "description" : "A page from your old Spellbook from magic school. Its a bit damaged",
        "move" : "lesser ball of flame",
        "consumable" : False,
    },

    "gold crown of doom" : {
        "name" : "gold crown of doom",
        "value" : 100,
        "description" : "A Golden crown of doom and despair",
        "move" : "golden doom blast",
        "consumable" : False,
    },

    #Potions
    "health potion" : {
        "name" : "health potion",
        "value" : 13,
        "description" : "A potion that regenerates flesh & mind, even lost limbs",
        "move" : "N/A",
        "consumable" : True,
        "consumable_effect" : ["heal",15],
    },
    "greater health potion" : {
        "name" : "greater health potion",
        "value" : 25,
        "description" : "A greater potion that regenerates flesh & mind, even lost limbs",
        "move" : "N/A",
        "consumable" : True,
        "consumable_effect" : ["heal",30],
    },

    #Item Drops
    "wolf tooth" : {
        "name" : "wolf tooth",
        "value" : 4,
        "description" : "The tooth from the local wolf population, could be sold",
        "move" : "N/A",
        "consumable" : False,
    },

    #Artifacts
    "sleeping bag" : {
        "name" : "sleeping bag",
        "value" : 15,
        "description" : "A potato bag with some wool in it, guess you could sleep in it. (Allows. you to sleep anywhere)",
        "move" : "N/A",
        "consumable" : False,
    },
    
}

shop_items = [raw_item_value["iron sword"],raw_item_value["health potion"],raw_item_value["gold crown of doom"],raw_item_value["sleeping bag"]]


#stat menus
#----------------------------
def stat_menu(clear):
    if clear == True:
        print("\033c", end="")
    print("---------------------------")
    print("Player: " + str(characters["allied"]["player"]["name"]))
    print("Class: " + str(characters["allied"]["player"]["class"]).capitalize())
    print("Age: " + str(characters["allied"]["player"]["age"]))
    print("Gold: " + str(characters["allied"]["player"]["gold"]))
    print("HP: " + str(characters["allied"]["player"]["health"]) +"/"+ str(characters["allied"]["player"]["max_health"]))
    print("Level: " + str(characters["allied"]["player"]["level"]) + "("+ str(characters["allied"]["player"]["exp"]) +"/"+ str(characters["allied"]["player"]["exp_to_level_up"]) +")")
    print("Area: " + str(area).capitalize())
    print("---------------------------")

def battle_stat_menu():
    print("Battle turn: " + str(turn))
    print("---------------------------")

    for i in turn_order:
        if check_if_ally(i) == True:
            allegiance = "allied"
        else:
            allegiance = "enemys"

        char_name = characters[allegiance][i]["name"]
        char_lv = characters[allegiance][i]["level"]
        char_hp = characters[allegiance][i]["health"]
        char_max_hp = characters[allegiance][i]["max_health"]

        if check_if_ally(i):
            print_name = (f"Ally: {char_name.capitalize()} LV:{char_lv} | ({char_hp}/{char_max_hp})")
        else:
            print_name = (f"Enemy: {char_name.capitalize()} LV:{char_lv} | ({char_hp}/{char_max_hp})")

        if turn_order[turn_in_turn_order] == i:
            turn_order_indicator = "--->| "
        else:
            turn_order_indicator = "    | "

        print(turn_order_indicator + print_name)
    print("---------------------------")
#----------------------------
def inventory_items_to_moves():
    global available_moves
    global inventory

    available_moves = ["punch"]
    for i in inventory:
        if raw_item_value[i]["move"] != "N/A":
            available_moves.append(raw_item_value[i]["move"])

def main_screen(chosen):
    global characters
    global available_moves



    available_moves = ["Punch"]
    
    leveld_up = False
    if characters["allied"]["player"]["exp"] >= characters["allied"]["player"]["exp_to_level_up"]:
        characters["allied"]["player"]["exp"] -= characters["allied"]["player"]["exp_to_level_up"]
        characters["allied"]["player"]["level"] += 1
        leveld_up = True
    characters["allied"]["player"]["exp_to_level_up"] = (characters["allied"]["player"]["level"]*20) - 10


    #Stat setter
    characters["allied"]["player"]["power_modifier"] = 1 + (characters["allied"]["player"]["level"] * char_class_stats[characters["allied"]["player"]["class"]]["power_multi"]) #temp int class, be float later when otehr stuff works
    characters["allied"]["player"]["max_health"] = characters["allied"]["player"]["starting_max_health"] + int((3 * (characters["allied"]["player"]["level"] - 1)) * char_class_stats[characters["allied"]["player"]["class"]]["health_multi"])

    if leveld_up == True:
        characters["allied"]["player"]["health"] = characters["allied"]["player"]["max_health"]


    inventory_items_to_moves()

    stat_menu(True)


    if chosen.lower() in commands:
        commands[chosen.lower()]()
    else:
        print("Use Help if stuck")
        print("")


    return

#command menu choices
#----------------------------
def help():
        print("")
        print("Go to area - goes to different area if possible")
        print("Inventory - See inventory")
        print("Stats - See additional stats")
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
    if input("Look closer at an item? (Y/N) ").lower() == "y":
        item_looked_closer_at = input("Item Name: ").lower()
        if item_looked_closer_at in inventory:
            print("")
            print("Description: " + str(raw_item_value[item_looked_closer_at]["description"]))
            print("Move it gives: " + str(raw_item_value[item_looked_closer_at]["move"]))
        else:
            main_screen("")
    else:
        main_screen("")

#more of a debug thing rn, subject to change
def check_stats():
    print("Power modifier: " + str(characters["allied"]["player"]["power_modifier"]))
    print("")

def go_to_area():
    global area

    print("Areas: " + str(areas))
    select = input("Select a area: ")
    if select.lower() in areas:
        area = select
        main_screen("")

def start_battle():
    if area == "forest":
        global characters
        global enemy
        global enemy_lv
        global turn
        global battle_over
        global gold_gain
        global exp_gain

        characters["enemys"] = {}
        gold_gain = 0
        exp_gain = 0

        amount_of_enemys = 1
        dif_num = random.randint(1,characters["allied"]["player"]["level"])

        if dif_num <= 3:
            difficulty = "easy"
            enemy_lv = random.randint(1,3)

        elif dif_num <= 6:
            difficulty = "medium"
            enemy_lv = random.randint(3,4)
        else:
            difficulty = "hard"
            enemy_lv = random.randint(6,6)


        turn = 0
        enemy = random.choice(enemys_in_area["forest"][difficulty])

        for i in range(amount_of_enemys):
            characters["enemys"][i] = {}
            characters["enemys"][i]["name"] = enemy
            characters["enemys"][i]["level"] = enemy_lv


            characters["enemys"][i]["max_health"] = int(enemy_stats[characters["enemys"][i]["name"]]["HP"]  + ((enemy_lv - 1) * enemy_stats[characters["enemys"][i]["name"]]["HP"] * 0.2))
            characters["enemys"][i]["health"] = characters["enemys"][i]["max_health"]

        battle_over = False
        turn_handler()
    else:
        print("No enemys around")
        main_screen(input())

def shop():
    global inventory
    global characters

    if area == "store":
        print("")
        print("Items in the shop. V")
        i_num = 0
        for i in shop_items:
            i_num += 1
            print("ID: " + str(i_num) + " | " + str(i["name"]) + ": With cost of: " + str(i["value"]) + " Gold")
        print("")
        buy_choice = input("Insert Item ID to buy: ")
        if buy_choice.isdigit():
            if int(buy_choice) <= i_num and int(buy_choice) > 0:
                if characters["allied"]["player"]["gold"] >= shop_items[int(buy_choice) - 1]["value"]:
                    characters["allied"]["player"]["gold"] -= shop_items[int(buy_choice) - 1]["value"]
                    print("Remaining Gold: " + str(characters["allied"]["player"]["gold"]))
                    print("Bought: " + shop_items[int(buy_choice) - 1]["name"])
                    inventory.append(shop_items[int(buy_choice) - 1]["name"])
                else:
                    print("Not enough Gold")
                input("")


    else:
        print("there is no store around")
        main_screen(input())
    main_screen("")

def sell():
    global inventory
    global characters

    if area == "store":
        print("")
        if inventory != []:
            print("Items in inventory. V")
            i_num = 0
            for i in inventory:
                i_num += 1
                i2 = raw_item_value[i]
                print("ID: " + str(i_num) + " | " + str(i) + ": With sell value of : " + str(i2["value"] - 1) + " Gold")

            sold_item_ID = input("ID of item to sell: ")
            if sold_item_ID.isdigit():
                sold_item_ID = int(sold_item_ID)
                if sold_item_ID <= i_num and sold_item_ID > 0:
                    sold_item_ID -= 1
                    sell_value = raw_item_value[inventory[sold_item_ID]]["value"] - 1

                    print("Sold Item: " + inventory[sold_item_ID] + " for " + str(sell_value) + " Gold")
                    characters["allied"]["player"]["gold"] += sell_value
                    print("Current Gold: " + str(characters["allied"]["player"]["gold"]))
                    del inventory[sold_item_ID]
                    input("")

        else:
            print("Nothing to sell...")
            input("Done?")
    else:
        print("Theres is no one here to sell to")
        input("")


    main_screen("")

def sleep():
    global characters
    if area == "home":
        characters["allied"]["player"]["health"] = characters["allied"]["player"]["max_health"]
        print("You took a nice nap in your bed, and feel refreshed")
        input("")
        main_screen("")
    elif "sleeping bag" in inventory:
        characters["allied"]["player"]["health"] = characters["allied"]["player"]["max_health"]
        print("You took a nap in a potato bag(?), at least you feel refreshed")
        input("")
        main_screen("")
        
    else:
        print("No where to sleep around here")
        input("")
        main_screen("")
#----------------------------
commands = {
    "help" : help,
    "go to area" : go_to_area,
    "inventory" : check_inventory,
    "stats" : check_stats,
    #area specific
    "battle" : start_battle,
    "shop" : shop,
    "sell" : sell,
    "sleep" : sleep,
    }
#Battle stuff
def turn_handler():
    global characters
    global turn_in_turn_order
    global turn_order
    global turn

    turn = 1
    stat_menu(True)
    battle_stat_menu()

    turn_in_turn_order = 0

    while battle_over == False:
        turn_order = ["player"]
        for i in characters["enemys"]:
            turn_order.append(i)

        turn_char = turn_order[turn_in_turn_order]

        do_turn(turn_char,check_if_ally(turn_char))

        if turn_in_turn_order == len(turn_order) - 1:
            turn_in_turn_order = 0
            turn += 1

        else:
            turn_in_turn_order += 1

    return    

def check_if_ally(char_to_check):
    if char_to_check in characters["allied"]:
        return True
    else:
        return False

def do_turn(char_doing_turn,is_ally):
    if is_ally == True:
        allegiance = "allied"
    else:
        allegiance = "enemys"

    char_name = characters[allegiance][char_doing_turn]["name"]

    stat_menu(True)
    battle_stat_menu()

    if is_ally:
        move_type = select_move_type()
        if move_type == "run":
            stat_menu(True)
            print("You ran")
            return
    else:
        enemy_choose_attack(char_doing_turn)

    return

def enemy_choose_attack(char_doing_turn):

    target_of_attack = random.choice(list(characters["allied"].keys()))
    chosen_attack = random.choice(enemy_stats[characters["enemys"][char_doing_turn]["name"]]["moves"])

    do_attack(char_doing_turn,target_of_attack,chosen_attack)

    return

def choose_attack():
    stat_menu(True)
    battle_stat_menu()
    print("Input (Back) to go back to choices")
    print("Avaible Moves: " + str(available_moves))
    print("---------------------------")

    return choice_in_choose_attack()

def choice_in_choose_attack():
    while True:
        chosen_attack = input("Choose Move: ").lower()
        if chosen_attack in available_moves:
            return chosen_attack
        elif chosen_attack == "back":
            return "back"
        else:
            print("Invalid")

def choose_attack_target():
    stat_menu(True)
    battle_stat_menu()

    target_array = []
    i_local_id = 0

    print("Avaible attack targets. V")
    for i in characters["enemys"]:

        i_local_id += 1
        
        char_name = characters["enemys"][i]["name"]
        char_lv = characters["enemys"][i]["level"]
        char_hp = characters["enemys"][i]["health"]
        char_max_hp = characters["enemys"][i]["max_health"]



        print_name = (f"{char_name.capitalize()} LV:{char_lv} | ({char_hp}/{char_max_hp})")
        print("Target ID: " + str(i_local_id) + " | Target: " + print_name)


        target_array.append(i)
    print("---------------------------")
    if i_local_id != 1:
        while True:
            input_id = input("ID of target to attack: ")
            if input_id.isdigit():
                input_id = int(input_id)
                if input_id <= i_local_id and input_id > 0:
                    return target_array[input_id - 1]
                else:
                    print("Invalid")
            else:
                print("Invalid")
    else:
        return target_array[0]

def select_move_type():
    while True:
        stat_menu(True)
        battle_stat_menu()
        print("Move choice options: attack / item / run")
        select_input = input("").lower()

        if select_input == "run":
            return "run"
        if select_input == "item":
            usable = False
            for i in inventory:
                if raw_item_value[i]["consumable"] == True:
                    usable = True
            if usable == True:
                selected_combat_item = item_combat_selector()
                if selected_combat_item != "back":

                    do_item_combat(selected_combat_item)
                    return
            else:
                print("No usable items")
                input()
        else:
            chosen_attack = choose_attack()
            if chosen_attack != "back":
                do_attack("player",choose_attack_target(),chosen_attack)
                return

def item_combat_selector():
    while True:
        stat_menu(True)
        battle_stat_menu()
        i_num = 0
        usable_items = []
        print("Input (Back) to go back to choices")
        print("Usable items. V")
        for i in inventory:
            if raw_item_value[i]["consumable"] == True:
                i_num += 1
                print("ID: " + str(i_num) + " | " + str(i))
                usable_items.append(i)

        selected_item_id = input("Insert Item ID to use: ")
        if selected_item_id == "back":
            return "back"
        if selected_item_id.isdigit():
            selected_item_id = int(selected_item_id)
            if selected_item_id <= i_num and selected_item_id > 0:
                selected_item = usable_items[selected_item_id - 1]
                return selected_item

def do_item_combat(combat_selected_item):
    global inventory
    inventory.remove(combat_selected_item)
    stat_menu(True)
    battle_stat_menu() 
    print(f"Used {combat_selected_item}")
    combat_item_effect(combat_selected_item)

    input()
    return

def combat_item_effect(item):
    global characters
    if raw_item_value[item]["consumable_effect"][0] == "heal":
        characters["allied"]["player"]["health"] += raw_item_value[item]["consumable_effect"][1]
        if characters["allied"]["player"]["health"] > characters["allied"]["player"]["max_health"]:
            characters["allied"]["player"]["health"] = characters["allied"]["player"]["max_health"]
        stat_menu(True)
        battle_stat_menu()
        print(f"regained {raw_item_value[item]["consumable_effect"][1]} health")
    elif item == "temp":
        return

def do_attack(attacker,defender,chosen_attack):
    global characters

    #gets name & allegiance of both attacker and defender
    #-----------------------------
    if check_if_ally(attacker) == True:
        attacker_allegiance = "allied"
    else:
        attacker_allegiance = "enemys"
    attacker_name = characters[attacker_allegiance][attacker]["name"]

    if check_if_ally(defender) == True:
        defender_allegiance = "allied"
    else:
        defender_allegiance = "enemys"
    defender_name = characters[defender_allegiance][defender]["name"]
    #-----------------------------

    if attacker_name == characters["allied"]["player"]["name"]:
        base_damage = random.randint(move_stats["player"][chosen_attack][0],move_stats["player"][chosen_attack][1])
        damage_to_deal = int(base_damage * characters["allied"]["player"]["power_modifier"])
    else:
        base_damage = random.randint(move_stats["enemys"][chosen_attack][0],move_stats["enemys"][chosen_attack][1])
        enemy_power_modifier = (enemy_lv * 0.2) + 0.8
        damage_to_deal = int(base_damage * enemy_power_modifier)

    #deals damage
    characters[defender_allegiance][defender]["health"] -= damage_to_deal

    stat_menu(True)
    battle_stat_menu()
    
    print(str(attacker_name).capitalize() + " attacked " + str(defender_name).capitalize() + " with " + str(chosen_attack).capitalize() + "!")
    print("")
    print(f"Dealt damage {damage_to_deal}!")

    input()

    if characters[defender_allegiance][defender]["health"] <= 0:
        character_died(defender_allegiance,defender)
    return

def character_died(allegiance,char):
    global exp_gain
    global gold_gain

    if char == "player":
        player_died()
        return
    else:
        exp_gain += int(enemy_stats[characters[allegiance][char]["name"]]["EXP"] + ((enemy_lv - 1) * enemy_stats[characters[allegiance][char]["name"]]["EXP"] * 0.2))
        gold_gain += int(enemy_stats[characters[allegiance][char]["name"]]["gold"] + ((enemy_lv - 1) * enemy_stats[characters[allegiance][char]["name"]]["gold"] * 0.2))
        characters[allegiance].pop(char)

        if characters["enemys"] == {}:
            victory()
        return

def victory():
    global battle_over

    print("Battle over. Well done :)")
    #rewards for winning
    print("EXP gained: " + str(exp_gain))
    print("Gold gained: " + str(gold_gain))
    characters["allied"]["player"]["exp"] += exp_gain
    characters["allied"]["player"]["gold"] += gold_gain

    battle_over = True

def player_died():
    global area
    global battle_over

    print("")
    print("You lost. To bad so sad :(")
    print("Lost half your Gold")
    print("")

    characters["allied"]["player"]["health"] = characters["allied"]["player"]["max_health"]
    characters["allied"]["player"]["gold"] = int(characters["allied"]["player"]["gold"] / 2)

    area = "home"

    battle_over = True
    return

#Pre-game choices
def name_select(redo):
    global characters
    print("\033c", end="")
    if redo is False:
        print("What's your name?")
    if redo is True:
        print("Please enter name")
    characters["allied"]["player"]["name"] = input().capitalize()
    if characters["allied"]["player"]["name"] == "":
        name_select(True)
name_select(False)

def age_select(redo):
    global characters
    print("\033c", end="")
    if redo is False:
        print("And your age?")
    if redo is True:
        print("Please enter a whole number (ex. 16, 35)")
    characters["allied"]["player"]["age"] = input()
    if not characters["allied"]["player"]["age"].isdigit():
        age_select(True)
age_select(False)

def class_select(redo):
    global characters
    print("\033c", end="")
    if redo is False:
        print("Lastly what class do you whant to play?")
        print("Valid choices: " + str(char_choice_class))
    if redo is True:
        print("Please enter a valid class")
        print("Valid choices: " + str(char_choice_class))
    characters["allied"]["player"]["class"] = input().lower()
    if not characters["allied"]["player"]["class"] in char_choice_class:
        class_select(True)
class_select(False)

if characters["allied"]["player"]["class"] == "knight":
    inventory.append("rusty iron sword")
if characters["allied"]["player"]["class"] == "mage":
    inventory.append("old spellbook page")


characters["allied"]["player"]["gold"] = 15
characters["allied"]["player"]["max_health"] = characters["allied"]["player"]["starting_max_health"]
characters["allied"]["player"]["health"] = characters["allied"]["player"]["max_health"]

main_screen("")
while True:
    main_screen(input())



