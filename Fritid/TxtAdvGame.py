name = str
age = str
gold = int
area = "Home"
areas = ["Home", "Shop", "Forest"]


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

def MainScreen(Choosen):
    global area
    global name
    global age
    global areas
    global gold
    global shop_items
    global inventory


    print("---------------------------")
    print("Player: " + name)
    print("Age: " + age)
    print("Gold: " + str(gold))
    print("Area: " + area)
    if Choosen == "Help":
        print("")
        print("Go to area. - goes to different area if possible")
        print("Inventory. - See inventory")
        print("Location specific stuff. V")
        if area == "Shop":
            print("Browse. - See what the shop has")

    elif Choosen == "Go to area":
        print("Areas: " + str(areas))
        print("Select a area")
        select = input()
        if select in areas:
            area = select
        MainScreen("Start")

    elif Choosen == "Inventory":
        print(inventory)
        input("Done? ")
        MainScreen("Start")

    elif Choosen == "Browse" and area == "Shop":
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
                MainScreen("Start")

            if gold >= shop_items[int(buy_choice) - 1]["Value"]:
                gold -= shop_items[int(buy_choice) - 1]["Value"]
                print("Remaining Gold: " + str(gold))
                print("Bought: " + shop_items[int(buy_choice) - 1]["Name"])
                inventory.append(shop_items[int(buy_choice) - 1]["Name"])
            else:
                print("Not enough Gold")

            input("Done? ")

            MainScreen("Start")
        else:
            MainScreen("Start")

    elif Choosen == "Sell" and area == "Shop":
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
                #fix here
                SoldItemID = int(input("ID of item to sell: ")) - 1
                print("Sold Item: " + Inventory[SoldItemID] + " for " + str(i2["Value"] - 1) + " Gold")
                Gold += i2["Value"] - 1
                print("Current Gold: " + str(Gold))
                del Inventory[SoldItemID]
                input("Done? ")
                MainScreen("Start")
            else:
                MainScreen("Start")
        else:
            print("Nothing to sell...")
            input("Done?")
            MainScreen("Start") 
    
    elif Choosen == "Start":
        print("Use Help if stuck")
    
    Choice = input()

    MainScreen(Choice)

print("What's your name?")
Name = input()
print("Hello " + Name)
print("And your age?")
Age = input()
print("You are " + Age)
Gold = 15

MainScreen("Start")


