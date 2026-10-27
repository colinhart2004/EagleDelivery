from collections import deque
from heapq import heappop, heappush
from itertools import count

class SearchResult:
    def __init__(self, path, expanded):
        self.path = path
        self.expanded = expanded


def reconstruct_path(parents, goal):
    path = []
    state = goal
    while state is not None:
        path.append(state)
        state = parents[state]
    path.reverse()
    return path


def bfs(campus, start, goal):
    frontier = deque([start])
    parents = {start: None}
    expanded = 0
    while frontier:
        state = frontier.popleft()
        if state == goal:
            return SearchResult(reconstruct_path(parents, goal), expanded)
        expanded += 1
        for action, successor in campus.neighbors(state):
            if successor not in parents:
                parents[successor] = state
                frontier.append(successor)
    return SearchResult(None, expanded)


def manhattan(state, goal):
    # Add the absolute row difference and the absolute column difference.
    # raise NotImplementedError("Complete TODO 1: manhattan")
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def astar(campus, start, goal):
    # Use heapq as a priority queue and manhattan() as the heuristic.
    # Track best known g-costs and parent states in dictionaries.
    serial = 0 # adding a serial gives heapq insertion order numbers
                #when tiebreaking heappop
    #insertion order as per class & project guidelines
    # f, serial, g, state
    frontier = [(manhattan(start,goal), serial, 0, start)]
    best_g = {start: 0}
    parents = {start: None}
    expanded = 0

    while frontier:
        _,_,g,state = heappop(frontier)

        #reject node's whose g is stale
        if g != best_g[state]:
            continue
        #test for goal
        if state == goal:
            return SearchResult(reconstruct_path(parents,goal),expanded)
        expanded += 1

        for _, next_state in campus.neighbors(state):
            new_g = g + 1
            #if new best g is found for a state, push new node into heap
            if new_g < best_g.get(next_state, float("inf")):
                best_g[next_state] = new_g
                parents[next_state] = state
                new_f = new_g + manhattan(next_state,goal)
                serial += 1
                heappush(frontier, (new_f,serial,new_g,next_state))

    return SearchResult(None,expanded)

def epsilon_greedy(q_values, state, actions, epsilon, rng):
    # q_values is a dictionary. Its keys are (state, action) pairs.
    # Example key: ((1, 1), "RIGHT"). Unseen entries have value 0.0.
    #starts returned action as a randomly chosen action
    chosen_action = rng.choice(actions)

    #1 - epsilon chance to return action with largest Q-value
    if(rng.random() > epsilon):
        for action in actions:
            chosen_q = q_values[(state,chosen_action)] if q_values.get((state,chosen_action)) is not None else 0.0
            new_q = q_values[(state,action)] if q_values.get((state,action)) is not None else 0.0

            #randomly break ties
            if(chosen_q == new_q):
                chosen_action = rng.choice([chosen_action,action])
            elif(new_q > chosen_q):
                chosen_action = action

    return chosen_action



def q_learning_update(q_values, state, action, reward, next_state,
                      actions, alpha, gamma, terminal):
    # Get Q(state, action), defaulting to 0.0.
    # If terminal is True, the target is reward with no continuation term.
    # Otherwise target = reward + gamma * max Q(next_state, next_action).
    # Consider every action, including unseen entries with value 0.0.
    # Apply Q <- Q + alpha * (target - Q).
    q = q_values[(state,action)] if q_values.get((state,action)) is not None else 0.0

    if(terminal):
        target = reward
    else:
        maxQ = 0.0
        for a in actions:
            new_q = q_values[(next_state,a)] if q_values.get((next_state,a)) is not None else 0.0
            if(new_q > maxQ):
                maxQ = new_q

        target = reward + gamma * maxQ

    q_values[(state,action)] = q + alpha * (target - q)