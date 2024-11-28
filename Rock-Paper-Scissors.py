import random

options = ["камень", "ножницы", "бумага"]

def determine_winner(player, computer):
    if player == computer:
        return "Ничья!"
    elif (player == "камень" and computer == "ножницы") or \
         (player == "ножницы" and computer == "бумага") or \
         (player == "бумага" and computer == "камень"):
        return "Ты победил!"
    else:
        return "Ты проиграл!"

score = 0

while True:
    print("Выбери камень, ножницы или бумагу")
    player_choice = input("Твой выбор: ").strip().lower()

    if player_choice == "выход":
        print(f"BAU BAU. Ваш счёт: {score}")
        break

    if player_choice not in options:
        print("Пожалуйста, введи 'камень', 'ножницы' или 'бумагу'.")
        continue

    computer_choice = random.choice(options)
    print(f"Выбор компьютера: {computer_choice}")

    result = determine_winner(player_choice, computer_choice)
    print(result)

    if result == "Ты победил!":
        score += 1
    elif result == "Ты проиграл!":
        score -= 1

    print(f"Ваш счёт: {score}")
