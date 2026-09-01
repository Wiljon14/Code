import random

def tur_spel():
    datorns_tal = random.randint(1,10)
    ditt_tall = int(input("Jag tänker på ett tall mellan 1 och 10, gissa. "))

    if ditt_tall == datorns_tal:
        print(f"Du har rätt, det var {datorns_tal}")
    elif ditt_tall > datorns_tal:
        print(f"Ditt tall är för stort, rätt svar var {datorns_tal}")
    elif ditt_tall < datorns_tal:
        print(f"Ditt tall är för litet, rätt svar var {datorns_tal}")
    print("")
    input("Spela igen")
    print("")
    print("")
    tur_spel()

tur_spel()