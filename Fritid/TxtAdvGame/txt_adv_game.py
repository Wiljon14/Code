import random
import pathlib
from yaml import load, Loader

#Loads data from txt_adv_data folder. Insert the name of the file, minus file extension. Returns content of file.
def data_loader(name_of_data_file):
    parent_path = pathlib.Path(__file__).parent.resolve()
    data_path = parent_path / "txt_adv_data"

    path_of_data = data_path / (name_of_data_file + ".yml")

    with open(path_of_data ,"r") as f:
        data = load(f, Loader=Loader)
    return data

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

            "status_effects" : {}
        }
    },
    "enemys" : {
        
    }
}
#battle variables
exp_gain = 0
gold_gain = 0
turn = 0
turn_order = []
turn_in_turn_order = 0
battle_over = True

char_choice_class = ["mage","knight"]

area = "forest"
areas = ["home", "store", "forest"]

char_class_stats = data_loader("char_class_stats")
enemys_in_area = data_loader("enemys_in_area")
enemy_stats = data_loader("enemy_stats")
move_stats = data_loader("move_stats")
raw_item_value = data_loader("raw_item_value")
crafting_recipes = data_loader("crafting_recipes")

shop_items = [
    raw_item_value["iron sword"],
    raw_item_value["flaming scroll"],
    raw_item_value["health potion"],
    raw_item_value["greater health potion"],
    raw_item_value["gold crown of doom"],
    raw_item_value["sleeping bag"]
]


inventory = []
available_moves = []
known_crafting_recipes = []

#stat/other menus
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

        status_effects_text = ""
        if characters[allegiance][i]["status_effects"] != {}:
            for ii in characters[allegiance][i]["status_effects"]:
                status_amount = characters[allegiance][i]["status_effects"][ii]
                if status_amount != 1:
                    status_effects_text = status_effects_text + (" [" + ii.capitalize() + " x" +  str(status_amount) +  "]")
                else:
                    status_effects_text = status_effects_text + (" [" + ii.capitalize() + "]")
        print(turn_order_indicator + print_name + status_effects_text)
    print("---------------------------")

def show_items_in_inventory(show_price):
    temp_inv = []
    temp_inv += inventory
    price = ""
    

    while temp_inv != []:
        item_amount = temp_inv.count(temp_inv[0])
        item_name = temp_inv[0]

        if show_price == True:
            price = ": With sell value of : " + str(raw_item_value[item_name]["value"] - 1) + " Gold"

        print(str(item_amount) + "x " + item_name + price)
        while item_name in temp_inv:
            temp_inv.remove(item_name)
    return

def availble_crafting_recipes():
    global known_crafting_recipes
    shown_recipes = []
    for i in crafting_recipes:
        recipe_requires = 0
        recipe_fulfilled = 0
        for ii in crafting_recipes[i]:
            recipe_requires += ii[1]
            if inventory.count(ii[0]) >= ii[1]:
                    recipe_fulfilled += ii[1]
            else:
                recipe_fulfilled += inventory.count(ii[0])

        if recipe_requires == recipe_fulfilled:
            shown_recipes.append(i)
            if i not in known_crafting_recipes:
                known_crafting_recipes.append(i)

            print(f"{i}: ({recipe_fulfilled}/{recipe_requires})")


    for i in known_crafting_recipes:
        if i not in shown_recipes:
            recipe_requires = 0
            recipe_fulfilled = 0
            for ii in crafting_recipes[i]:
                recipe_requires += ii[1]
                if inventory.count(ii[0]) >= ii[1]:
                    recipe_fulfilled += ii[1]
                else:
                    recipe_fulfilled += inventory.count(ii[0])

            print(f"{i}: ({recipe_fulfilled}/{recipe_requires})")
            shown_recipes.append(i)
    
    return shown_recipes

def crafting_menu(item_to_craft):
    items_has = 0
    items_need = 0
    recipe = crafting_recipes[item_to_craft]
    stat_menu(True)
    print(item_to_craft)
    for i in recipe:
        amount_in_inv = inventory.count(i[0])

        items_need += 1
        print(f"{i[0]} ({amount_in_inv}/{i[1]})")

        if amount_in_inv >= i[1]:
            items_has += 1

    if items_has == items_need:
        if input("Craft (Y/N) ").lower() == "y":
            for i in recipe:
                for ii in range(i[1]):
                    inventory.remove(i[0])
            inventory.append(item_to_craft)
            print(f"Crafted {item_to_craft}")
    return
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
        print("Go to area - Goes to different area if possible")
        print("Inventory - See inventory")
        print("Craft - Create new items using other items")
        print("Stats - See additional stats")
        print("")
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
    
    show_items_in_inventory(False)

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

def craft():
    print("Items owned. V")
    show_items_in_inventory(False)
    print("")
    print("Available recipes. V")
    recipes = availble_crafting_recipes()
    if recipes == []:
        print("No available recipes, try again later")

    craft_item_input = input("recipe to look at: ")
    if craft_item_input in recipes:
        crafting_menu(craft_item_input)
    return

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
        global turn
        global battle_over
        global gold_gain
        global exp_gain

        characters["enemys"] = {}
        gold_gain = 0
        exp_gain = 0

        dif_num = characters["allied"]["player"]["level"]

        turn = 0

        enemy_id = -1

        while dif_num >= 1:
            enemy_id += 1
            valid_power = False
            while valid_power == False:
                power_of_enemy = random.choice(list(enemys_in_area[area].keys()))
                if power_of_enemy <= dif_num:
                    dif_num -= power_of_enemy
                    valid_power = True

            enemy = random.choice(enemys_in_area[area][power_of_enemy])

            add_new_char_to_combat(enemy_id,enemy,random.randrange(power_of_enemy,power_of_enemy + 3),False)

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
            show_items_in_inventory(True)

            sold_item_ID = input("Item to sell: ")
            if sold_item_ID in inventory:
                amount_to_sell = input("How many do you want to sell? ")
                if amount_to_sell.isdigit():
                    amount_to_sell = int(amount_to_sell)
                    if amount_to_sell <= 0:
                        return
                    elif amount_to_sell > inventory.count(sold_item_ID):
                        amount_to_sell = inventory.count(sold_item_ID)

                    sell_value = (raw_item_value[sold_item_ID]["value"] - 1) * amount_to_sell
    
                    print("Sold Item(s): " + sold_item_ID + " for " + str(sell_value) + " Gold")
                    characters["allied"]["player"]["gold"] += sell_value
                    print("Current Gold: " + str(characters["allied"]["player"]["gold"]))
                    for i in range(amount_to_sell):
                        inventory.remove(sold_item_ID)
                    input("")

                else:
                    return

                

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

def cheat_item_give():
    global inventory
    inventory.append(input("Give item: ").lower())
#----------------------------
commands = {
    "help" : help,
    "go to area" : go_to_area,
    "inventory" : check_inventory,
    "craft" : craft,
    "stats" : check_stats,
    #area specific
    "battle" : start_battle,
    "shop" : shop,
    "sell" : sell,
    "sleep" : sleep,
    #cheats
    "give" : cheat_item_give,
    }
#Battle stuff
                        #char_id, the id that the new thing is going to have. make sure this is not wrong EVER fricks stuff up
def add_new_char_to_combat(char_id,char,level,is_ally):
        if is_ally == True:
            allegiance = "allied"
        else:
            allegiance = "enemys"
        
        characters[allegiance][char_id] = {}
        characters[allegiance][char_id]["name"] = char
        characters[allegiance][char_id]["level"] = level


        characters[allegiance][char_id]["max_health"] = int(enemy_stats[characters[allegiance][char_id]["name"]]["hp"]  + ((characters[allegiance][char_id]["level"] - 1) * enemy_stats[characters[allegiance][char_id]["name"]]["hp"] * 0.2))
        characters[allegiance][char_id]["health"] = characters[allegiance][char_id]["max_health"]
        characters[allegiance][char_id]["status_effects"] = {}

def turn_handler():
    global characters
    global turn_in_turn_order
    global turn_order
    global turn

    turn = 1

    turn_in_turn_order = 0

    while battle_over == False:

        turn_order = []
        for i in characters["allied"]:
            turn_order.append(i)
        for i in characters["enemys"]:
            turn_order.append(i)

        turn_char = turn_order[turn_in_turn_order]

        do_turn(turn_char,check_if_ally(turn_char))

        if turn_in_turn_order >= len(turn_order) - 1:
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
    global battle_over
    global turn_in_turn_order
    global turn_order

    if is_ally == True:
        allegiance = "allied"
    else:
        allegiance = "enemys"

    do_status_effects(char_doing_turn,allegiance)

    if characters[allegiance][char_doing_turn]["health"] <= 0:
        character_died(allegiance,char_doing_turn)
        turn_in_turn_order -= 1
        turn_order.remove(char_doing_turn)
        return
    else:
        stat_menu(True)
        battle_stat_menu()

        if is_ally:
            if char_doing_turn == "player":
                move_type = select_move_type()
                if move_type == "run":
                    stat_menu(True)
                    battle_over = True
                    print("You ran")
                    return
            else:
                target_of_attack = random.choice(list(characters["enemys"].keys()))
                chosen_attack = random.choice(enemy_stats[characters["allied"][char_doing_turn]["name"]]["moves"])

                do_attack(char_doing_turn,target_of_attack,chosen_attack)
                
        else:
            target_of_attack = random.choice(list(characters["allied"].keys()))
            chosen_attack = random.choice(enemy_stats[characters["enemys"][char_doing_turn]["name"]]["moves"])

            do_attack(char_doing_turn,target_of_attack,chosen_attack)
        return

def do_status_effects(char,allegiance):
    global characters

    effects_to_remove = []
    text_to_print = []
    effects = False
    if characters[allegiance][char]["status_effects"] != {}:
        effects = True
        for i in characters[allegiance][char]["status_effects"]:
            status_amount = characters[allegiance][char]["status_effects"][i]
            damage_to_take = 0
            if i == "on fire":
                damage_to_take = int(3 + status_amount * 0.5)
            if i == "bleeding":
                damage_to_take = int(1 + ((0.04 + 0.01 * status_amount) * characters[allegiance][char]["max_health"]))

            characters[allegiance][char]["health"] -= damage_to_take
            characters[allegiance][char]["status_effects"][i] -= 1
            if characters[allegiance][char]["status_effects"][i] == 0:
                effects_to_remove.append(i)


            if damage_to_take > 0:
                text_to_print.append(characters[allegiance][char]["name"] + " took " + str(damage_to_take) + " damage from [" + i + "]")


    if effects == True:
        for i in effects_to_remove:
            characters[allegiance][char]["status_effects"].pop(i)
        stat_menu(True)
        battle_stat_menu()

        for i in text_to_print:
            print(i)
        input()

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
    elif raw_item_value[item]["consumable_effect"][0] == "summon":
        char_to_summon = raw_item_value[item]["consumable_effect"][1]
        char_level = characters["allied"]["player"]["level"]

        ally_list = list(characters["allied"].keys()).remove("player")
        if ally_list == None:
            ally_list = range(1)
        smallest_number = -1
        for i in ally_list:
            if int(i) < smallest_number:
                smallest_number == int(i) - 1

        add_new_char_to_combat(smallest_number,char_to_summon,char_level,True)


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
    attacker_level = characters[attacker_allegiance][attacker]["level"]

    if check_if_ally(defender) == True:
        defender_allegiance = "allied"
    else:
        defender_allegiance = "enemys"
    defender_name = characters[defender_allegiance][defender]["name"]
    defender_level = characters[defender_allegiance][defender]["level"]

    #-----------------------------

    if attacker_name == characters["allied"]["player"]["name"]:
        base_damage = random.randint(move_stats["player"][chosen_attack][0],move_stats["player"][chosen_attack][1])
        damage_to_deal = int(base_damage * characters["allied"]["player"]["power_modifier"])

        did_status_effect = give_status_effects(defender_allegiance,defender,move_stats["player"][chosen_attack][2])

    else:
        base_damage = random.randint(move_stats["enemys"][chosen_attack][0],move_stats["enemys"][chosen_attack][1])
        enemy_power_modifier = (attacker_level * 0.2) + 0.8
        damage_to_deal = int(base_damage * enemy_power_modifier)

        did_status_effect = give_status_effects(defender_allegiance,defender,move_stats["enemys"][chosen_attack][2])


    #deals damage
    characters[defender_allegiance][defender]["health"] -= damage_to_deal

    stat_menu(True)
    battle_stat_menu()
    
    print(str(attacker_name).capitalize() + " attacked " + str(defender_name).capitalize() + " with " + str(chosen_attack).capitalize() + "!")
    print("")
    print(f"Dealt damage {damage_to_deal}!")
    if did_status_effect[0]:
        print(f"Applied {did_status_effect[2]} {did_status_effect[1]}")

    input()

    if characters[defender_allegiance][defender]["health"] <= 0:
        character_died(defender_allegiance,defender)
    return

def give_status_effects(allegiance,char,effect : list):
    global characters
    if effect != []:
        effect_amount = random.choice(effect[1])
        effect_type = effect[0]
        if effect_amount > 0:
            if effect[0] in characters[allegiance][char]["status_effects"]:
                characters[allegiance][char]["status_effects"][effect[0]] += effect_amount
                return [True,effect_type,effect_amount]
            else:
                characters[allegiance][char]["status_effects"][effect[0]] = effect_amount
                return [True,effect_type,effect_amount]
        
    return [False]

def character_died(allegiance,char):
    global exp_gain
    global gold_gain
    global inventory
    global characters

    level = characters[allegiance][char]["level"]

    if char == "player":
        player_died()
        return
    else:
        exp_gain += int(enemy_stats[characters[allegiance][char]["name"]]["exp"] + ((level - 1) * enemy_stats[characters[allegiance][char]["name"]]["exp"] * 0.2))
        gold_gain += int(enemy_stats[characters[allegiance][char]["name"]]["gold"] + ((level - 1) * enemy_stats[characters[allegiance][char]["name"]]["gold"] * 0.2))

        drops_var = random.choice(enemy_stats[characters[allegiance][char]["name"]]["drops"])
        drop_amount = random.choice(drops_var[0])
        drop_item = drops_var[1]

        for i in range(drop_amount):
            inventory.append(drop_item)

        if drop_amount != 0:
            print(characters[allegiance][char]["name"] + " Has died dropped: " + str(drop_amount) + " " + drop_item)
            input()
        characters[allegiance].pop(char)



        if characters["enemys"] == {}:
            victory()
        return

def victory():
    global battle_over

    stat_menu(True)

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

for i in char_class_stats[characters["allied"]["player"]["class"]]["starting_gear"]:
    inventory.append(i)

characters["allied"]["player"]["gold"] = 15
characters["allied"]["player"]["max_health"] = characters["allied"]["player"]["starting_max_health"]
characters["allied"]["player"]["health"] = characters["allied"]["player"]["max_health"]

main_screen("")
while True:
    main_screen(input())