import numpy as np

def display(game_name, results):
    strategies = ['Tit-for-tat', 'Fictitious', 'Bully', 'Godfather']
    print(f"\n{game_name}:")
    print(" " * 16, end="")
    for strategy in strategies:
        print(f"{strategy:16}", end="  ")
    print()
    for i, row_strategy in enumerate(strategies):
        print(f"{row_strategy:16}", end="")
        for j, _ in enumerate(strategies):
            row_reward, col_reward = results[i, j]
            print(f"{row_reward:5.2f}, {col_reward:5.2f}", end=" " * 5)
        print()

def choose_action(strategy, last_action, chose_game, first_move = True):

    if chose_game == 'PRISONERS_DILEMMA':
        if strategy == 'tit-for-tat':
            if first_move:
                if last_action:
                    return last_action[-1][1]
                else:
                    return 1
            else:
                if last_action:
                    return last_action[-1][0]
                else:
                    return 1
            
        elif strategy == 'fictitious-play':
            counts = {0: 0, 1: 0}
            for _, opp_action in last_action:
                counts[opp_action] += 1
            return max(counts, key=counts.get)

        elif strategy == 'bully':
            return 0

        elif strategy == 'godfather':
            if not last_action:
                return 1
            if first_move:
                if last_action:
                    return last_action[-1][1]
                else:
                    return 1
            else:
                if last_action:
                    return last_action[-1][0]
                else:
                    return 1


    elif chose_game == 'CHICKEN':
        if strategy == 'tit-for-tat':
            if first_move:
                if last_action:
                    return last_action[-1][1]
                else:
                    return 0
            else:
                if last_action:
                    return last_action[-1][0]
                else:
                    return 0

        elif strategy == 'fictitious-play':
            counts = {0: 0, 1: 0}
            for _, opp_action in last_action:
                counts[opp_action] += 1
            return max(counts, key=counts.get)

        elif strategy == 'bully':
            return 1
        
        elif strategy == 'godfather':
            if not last_action:
                return 0
            if first_move:
                if last_action:
                    return last_action[-1][1]
                else:
                    return 0
            else:
                if last_action:
                    return last_action[-1][0]
                else:
                    return 0
        

    elif chose_game == 'MOVIE_COORDINATION':
        if strategy == 'tit-for-tat':
            if first_move:
                if last_action:
                    return last_action[-1][1]
                else:
                    return 0
            else:
                if last_action:
                    return last_action[-1][0]
                else:
                    return 1

        elif strategy == 'fictitious-play':
            counts = {0: 0, 1: 0}
            for _, opp_action in last_action:
                counts[opp_action] += 1
            return max(counts, key=counts.get)

        elif strategy == 'bully':
            if first_move:
                return 0
            else:
                return 1

        elif strategy == 'godfather':
            if first_move:
                if last_action:
                    return last_action[-1][1]
                else:
                    return 0
            else:
                if last_action:
                    return last_action[-1][0]
                else:
                    return 1

def reward(action1, action2, game):
    if game == 'PRISONERS_DILEMMA':
        return PRISONERS_DILEMMA[action1, action2]
    elif game == 'CHICKEN':
        return CHICKEN[action1, action2]
    elif game == 'MOVIE_COORDINATION':
        return MOVIE_COORDINATION[action1, action2]


def play(first_strategy, second_strategy, game, rounds=100):
    total = [0, 0]
    history = []
    for _ in range(rounds):
        first_action = choose_action(first_strategy, history, game)
        second_action = choose_action(second_strategy, history, game, first_move = False)
        first_reward, second_reward = reward(first_action, second_action, game)
        total[0] += first_reward
        total[1] += second_reward
        history.append((first_action, second_action))
    return total

def compete_strategies(game, rounds=100):
    strategies = ['tit-for-tat', 'fictitious-play', 'bully', 'godfather']
    results = np.zeros((len(strategies), len(strategies), 2))
    for i, first_strategy in enumerate(strategies):
        for j, second_strategy in enumerate(strategies):
            reward = play(first_strategy, second_strategy, game, rounds)
            results[i, j] = [x / rounds for x in reward]
    return results

PRISONERS_DILEMMA = np.array([[[1, 1], [5, 0]],
                              [[0, 5], [3, 3]]])
CHICKEN = np.array([[[3, 3], [1.5, 3.5]],
                     [[3.5, 1.5], [1, 1]]])
MOVIE_COORDINATION = np.array([[[3, 2], [0, 0]],
                               [[0, 0], [2, 3]]])

games = ['PRISONERS_DILEMMA', 'CHICKEN', 'MOVIE_COORDINATION']
for game in games:
    rewards = compete_strategies(game)
    display(game, rewards)