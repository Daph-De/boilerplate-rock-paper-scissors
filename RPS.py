# Global state
opponent_history = []
my_history = []
opponent_patterns = {}
my_patterns = {}
strategy_tracker = {"A": 0, "B": 0, "N": 0}


def player(prev_play):
    global opponent_history, my_history, opponent_patterns, my_patterns, strategy_tracker

    if prev_play == "":
        opponent_history = []
        my_history = []
        opponent_patterns = {}
        my_patterns = {}
        strategy_tracker = {"A": 0, "B": 0, "N": 0}
        return "R"
    counters = {'R': 'P', 'P': 'S', 'S': 'R'}

    if prev_play:
        opponent_history.append(prev_play)

    n = 3       # pattern length for pattern dictionaries

    # track opponents patterns
    if len(opponent_history) > n:
        last_pattern = "".join(opponent_history[-n:])
        if last_pattern not in opponent_patterns:
            opponent_patterns[last_pattern] = 1
        else:
            opponent_patterns[last_pattern] += 1

    # track own patterns
    if len(my_history) > n:
        last_pattern = "".join(my_history[-n:])
        if last_pattern not in my_patterns:
            my_patterns[last_pattern] = 1
        else:
            my_patterns[last_pattern] += 1

    # STRATEGY A - predict opponents next move and counter it
    opponent_next_possibility = ["".join(opponent_history[-n+1:])+option for option in ["R","P", "S"]]
    predictions = {}
    for possibility in opponent_next_possibility:
        if possibility in opponent_patterns:
            predictions[possibility] = opponent_patterns[possibility]
        else:
            predictions[possibility] = 0

    predicted_opponents_next = max(predictions, key=predictions.get)[-1]
    guess_A = counters[predicted_opponents_next]

    # STRATEGY B - counter the prediction of your next move
    my_next_possibilities = ["".join(my_history[-n+1:])+option for option in ["R","P", "S"]]
    predictions = {}
    for possibility in my_next_possibilities:
        if possibility in my_patterns:
            predictions[possibility] = my_patterns[possibility]
        else:
            predictions[possibility] = 0

    # Predict what opponent thinks I'll do
    predicted_my_next = max(predictions, key=predictions.get)[-1]
    # Opponents to counter my predicted move
    opponent_play = counters[predicted_my_next]
    # Your move to counter opponent move
    guess_B = counters[opponent_play]

    if len(opponent_history) > 0 and len(my_history) > 0:
        last_move_opponent = opponent_history[-1]
        my_last_move = my_history[-1]
        if counters[last_move_opponent] == my_last_move:
            strategy_tracker["A"] += 1
        elif counters[last_move_opponent] == guess_B:
            strategy_tracker["B"] += 1
        else:
            strategy_tracker["N"] += 1

    if strategy_tracker["B"] > strategy_tracker["A"]:
        guess = guess_B
    elif strategy_tracker["N"] > 100:
        guess = guess_B
    else:
        guess = guess_A

    my_history.append(guess)
    return guess
