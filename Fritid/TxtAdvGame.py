Name = str
Age = str
Gold = int
Area = "Home"
Areas = ["Home", "Shop", "Forest"]
ShopItems = [ #Array order: Name,Cost
    ["Iron Sword",5],
    ["Health Potion",3],
    ["Gold Crown of Doom",100]
]
Inventory = []

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
            print("ID: " + str(iNum) + " | " + str(i[0]) + ": With cost of: " + str(i[1]) + " Gold")
        print("")
        Buying = input("Buy something? (Y/N) ")
        if Buying == "Y":
            BuyChoice = input("Insert Item ID to buy: ")
            if BuyChoice == "":
                MainScreen("Start")

            if Gold >= ShopItems[int(BuyChoice) - 1][1]:
                Gold -= ShopItems[int(BuyChoice) - 1][1]
                print("Remaining Gold: " + str(Gold))
                print("Bought: " + ShopItems[int(BuyChoice) - 1][0])
                Inventory.append(ShopItems[int(BuyChoice) - 1][0])
            else:
                print("Not enough Gold")

            input("Done? ")

            MainScreen("Start")
        else:
            MainScreen("Start")
        
    elif Choosen == "Start":
        print("Use Help if stuck")
    Choice = input()

    MainScreen(Choice)

print("Whats your name?")
Name = input()
print("Hello " + Name)
print("And your age?")
Age = input()
print("You are " + Age)
Gold = 15

MainScreen("Start")


