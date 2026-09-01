import random

name = str
age = str
gold = int
health = int
max_health = int
starting_max_health = 20
char_class = "Not choosen"
char_choice_class = ["Mage","Knight","Druid"]
char_class_stats = {
    "Mage" : [],
    "Knight" : [],
    "Druid" : [],
}
area = "Forest"
areas = ["Home", "Shop", "Forest"]
enemy_stats = {
    "Wolf" : [15],
    "Bear" : [30],
}

inventory = ["Iron Sword"]
raw_item_value = {
    "Iron Sword" : {
        "Name" : "Iron Sword",
        "Value" : 5,
        "Description" : "A well made sword of iron. Great at cutting down foes.",
    },
    "Health Potion" : {
        "Name" : "Health Potion",
        "Value" : 3,
        "Description" : "A potion that regenerates flesh & mind, even lost limbs",
    },
    "Gold Crown of Doom" : {
        "Name" : "Gold Crown of Doom",
        "Value" : 100,
        "Description" : "A Golden crown of doom and despair",
    },
}

shop_items = [raw_item_value["Iron Sword"],raw_item_value["Health Potion"],raw_item_value["Gold Crown of Doom"]]

def main_screen(choosen):
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

    print("---------------------------")
    print("Player: " + str(name))
    print("Class: " + str(char_class))
    print("Age: " + str(age))
    print("Gold: " + str(gold))
    print("HP: " + str(health) +"/"+ str(max_health))
    print("Area: " + str(area))
    print("---------------------------")
    if choosen == "Help":
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
    elif choosen == "Go to area":
        print("Areas: " + str(areas))
        select = input("Select a area: ")
        if select in areas:
            area = select
        main_screen("")

    elif choosen == "Inventory":
        print(inventory)
        input("Done? ")
        main_screen("")

    elif choosen == "Browse" and area == "Shop":
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

    elif choosen == "Sell" and area == "Shop":
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

    elif choosen == "Battle" and area == "Forest":
        battle_screen(1,"Wolf",0)
    
    elif choosen == "":
        print("Use Help if stuck")
        print("")
    
    choice = input()

    main_screen(choice)



def battle_screen(turn, enemy, hp_left):
    if turn == 1:
        enemy_hp = enemy_stats[enemy][0]
    else:
        enemy_hp = hp_left

    print("\033c", end="")
    print("---------------------------")
    print("Player: " + str(name))
    print("Class: " + str(char_class))
    print("Age: " + str(age))
    print("Gold: " + str(gold))
    print("HP: " + str(health) +"/"+ str(max_health))
    print("Area: " + str(area))
    print("---------------------------")
    print("Battle turn: " + str(turn))
    print("Enemy: " + str(enemy) + " | (" + str(enemy_hp) + "/" + str(enemy_stats[enemy][0]) + ")" )
    print("---------------------------")

    if enemy_hp <= 0:
        print(hp_left)
        input("Battle over. Well done :)")
        main_screen("")
    else:
        input("Next turn?")
        battle_screen(turn+1,enemy,enemy_hp)



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

gold = 15
max_health = starting_max_health
health = max_health

main_screen("")


