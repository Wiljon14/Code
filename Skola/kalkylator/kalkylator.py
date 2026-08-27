print("Välkommen till kalkylatorn")


def räknare():
    värde_1 = float(input("Tal nummer ett? (Skriv med siffror) "))
    värde_2 = float(input("Tal nummer två? (Skriv med siffror) "))
    matte_typ = input("Vad vill du göra med dem? (+, -, *, /) ")
    if matte_typ == "+":
        resultat = str(värde_1 + värde_2)
        print("Summan är: " + resultat)
    elif matte_typ == "-":
        resultat = str(värde_1 - värde_2)
        print("Diffirensen är: " + resultat)
    elif matte_typ == "*":
        resultat = str(värde_1 * värde_2)
        print("Produkten är: " + resultat)
    elif matte_typ == "/":
        resultat = str(värde_1 / värde_2)
        print("Kvoten är: " + resultat)

    igen = input("Vill du räkna ett till tall. (Y/N)")
    if igen == "Y":
        räknare()
    else:
        print("Hey då!")

räknare()