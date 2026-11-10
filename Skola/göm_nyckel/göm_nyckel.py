import random
import os

vinster = 0
förluster = 0

def starta_spel():
    gömställe = random.randint(1,5)
    försök_kvar = 3
    gissning = 0

    while gissning != gömställe and försök_kvar > 0:
        gissning = int(input("Gissa gömställe (1-5): "))
        försök_kvar -= 1

    if gissning == gömställe:
        print("Du hittade nyckeln!")
        input()
        return True
    else:
        print("Slut på försök!")
        input()
        return False

while True:
    if starta_spel() == True:
        vinster += 1
    else:
        förluster += 1

    os.system("clear")
    print(f"vinster: {vinster}, förluster: {förluster}")
    input()
    os.system("clear")
