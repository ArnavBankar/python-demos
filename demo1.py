import random

def roll():
    min_value = 1
    max_value = 6
    roll = random.randint(min_value, max_value)

    return roll



while True:
    players = input("Enter the number of players (can be from 2 to 4): ")
    if players.isdigit():
        players = int(players)
        if 2 <= players <= 4:
            break
        else:
            print("Must be between 2 to 4 players.")
    else:
        print("Invalid, try again.")


max_score = 50
player_scores = [0 for _ in range(players) ]

while max(player_scores) < max_score:
    for player_idx in range(players):
        print("\nPlayer number", player_idx + 1, "turn started\n")
        current_score = 0

        while True:
            should_roll = input("Would you like to roll (say y)? ")
            if should_roll.lower() != "y":
                break
            
            value = roll()
            if value == 1:
                print("You rolled a 1, turn done")
                current_score = 0
                break
            else:
                current_score += value
                print("You rolled a:", value)
                print("Your current turn score is:", current_score)
                if current_score >= max_score:
                    break



        player_scores[player_idx] += current_score
        print("Player", player_idx + 1, "total score is:", player_scores[player_idx])

        if player_scores[player_idx] >= max_score:
            print("\nPlayer", player_idx + 1, "wins with a score of", player_scores[player_idx], "!")
            break

    if max(player_scores) >= max_score:
        break

print("Game over!")