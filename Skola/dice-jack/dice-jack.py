import random


def game():
    print("\033c", end="")
    input("Rulla tärning")
    ditt_resultat = random.randint(1,6)
    print(f"Du fick {ditt_resultat}")
    if input("Rulla en till? (Y/N)") == "Y":
        ditt_resultat += random.randint(1,6)
        print(f"Du har nu {ditt_resultat}")
    if ditt_resultat > 10:
        print("Du är över tio, du har förlorat")
    else:
        dator_resulat = random.randint(1,6)
        if dator_resulat != 5 and dator_resulat != 6:
            dator_resulat += random.randint(1,6)
            print(f"Datorn fick över två kast {dator_resulat}")
        else:
            print(f"Datorn fick över ett kast {dator_resulat}")

        if dator_resulat > ditt_resultat:
            print("Datorn vann")
        elif ditt_resultat > dator_resulat:
            print("Du vann")
        else:
            print("Det blev lika")
        if input("Vill du spela igen? (Y/N)") == "Y":
            game()

game()  