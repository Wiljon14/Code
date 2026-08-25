
import random

svar = ["Ja, helt klart.", "Absolut", "Fråga igen imorgon", "Det vill du inte vetea"]

fråga = input("Fråga oraklet ")
print("Du frågade: ", fråga)
print(random.choice(svar))