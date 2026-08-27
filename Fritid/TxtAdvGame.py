Name = str
Age = str
Gold = int
Area = "Home"
Areas = ["Home", "Shop", "Forest"]


Inventory = ["Iron Sword"]
RawItemValue = {
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

ShopItems = [RawItemValue["Iron Sword"],RawItemValue["Health Potion"],RawItemValue["Gold Crown of Doom"]]

def MainScreen(Choosen):
    global Area
    global Name
    global Age
    global Areas
    global Gold
    global ShopItems
    global Inventory


    print("---------------------------")
    print("Player: " + Name)
    print("Age: " + Age)
    print("Gold: " + str(Gold))
    print("Area: " + Area)
    if Choosen == "Help":
        print("")
        print("Go to area. - goes to different area if possible")
        print("Inventory. - See inventory")
        print("Location specific stuff. V")
        if Area == "Shop":
            print("Browse. - See what the shop has")

    elif Choosen == "Go to area":
        print("Areas: " + str(Areas))
        print("Select a area")
        select = input()
        if select in Areas:
            Area = select
        MainScreen("Start")

    elif Choosen == "Inventory":
        print(Inventory)
        input("Done? ")
        MainScreen("Start")

    elif Choosen == "Browse" and Area == "Shop":
        print("")
        print("Items in the shop. V")
        iNum = 0
        for i in ShopItems:
            iNum += 1
            print("ID: " + str(iNum) + " | " + str(i["Name"]) + ": With cost of: " + str(i["Value"]) + " Gold")
        print("")
        Buying = input("Buy something? (Y/N) ")
        if Buying == "Y":
            BuyChoice = input("Insert Item ID to buy: ")
            if BuyChoice == "":
                MainScreen("Start")

            if Gold >= ShopItems[int(BuyChoice) - 1]["Value"]:
                Gold -= ShopItems[int(BuyChoice) - 1]["Value"]
                print("Remaining Gold: " + str(Gold))
                print("Bought: " + ShopItems[int(BuyChoice) - 1]["Name"])
                Inventory.append(ShopItems[int(BuyChoice) - 1]["Name"])
            else:
                print("Not enough Gold")

            input("Done? ")

            MainScreen("Start")
        else:
            MainScreen("Start")

    elif Choosen == "Sell" and Area == "Shop":
        print("")
        if Inventory != []:
            print("Items in inventory. V")
            iNum = 0
            for i in Inventory:
                iNum += 1
                i2 = RawItemValue[i]
                print("ID: " + str(iNum) + " | " + str(i) + ": With sell value of : " + str(i2["Value"] - 1) + " Gold")
            isSelling = input("Sell something? (Y/N) ")
            if isSelling == "Y":
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


