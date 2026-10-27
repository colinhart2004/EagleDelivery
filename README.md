# Eagle Delivery Project

This is a project simulating a delivery robot on 2d gridworld-like map. 

Using the search algorithms BFS and A*, the robot can plan out routes from the selected Start and Goal letters (representing buildings). Running these algorithms can show the pros and cons of using a heuristic-based algorithm such as A*.

Using the training algorithm epsilon-greedy, the robot can learn a policy to follow in the 2d gridworld. 

## Requirements

Use Python 3.9+.

result_plots.py ONLY:\
requires pandas, matplotlib.pyplot and matplotlib.lines

## Commands

run_project.py main options:\
```bash
show
```
prints out emu_campus.txt and legend

```bash
random
```
runs a random-action agent

```bash
search --algorithm
```
runs a search algorithm, default BFS, can specify astar

```bash
train --slip --max-steps --episodes --seeds --alpha --gamma --epsilon --eval-episodes --output
```
runs an epsilon greedy learning algorithm
can specify slip p for random chance to fail action (0-1) default 0.0\
can specify max-steps for max agent actions before truncation default 200\
can specify episodes an agent trains for default 2000\
can specify each seed number used for each separate trial\
can specify learning rate alpha default 0.3\
can specify action reward diminisher gamma default 0.95\
can specify epsilon default 0.2\
can specify number of evaluation episodes default 100\
must specify output folder

Arguments:
```bash
--map
```
specify path to a map.txt file to run an agent on

```bash
--start
```
specify the start letter, default S

```bash
--goal
```
specify the goal letter, default W




## Example usage

```bash
python3 run_project.py show
python3 run_project.py search --algorithm bfs --start S --goal W
python3 run_project.py search --algorithm bfs --map maps/emu_detour.txt --start S --goal W
python3 run_project.py random --start S --goal W --seed 0
python3 examples/interaction_demo.py
python3 -m unittest tests.test_environment -v
```

On `emu_campus.txt`, BFS from S to W should return path length **18** and **67**
expanded nodes, The path visualization uses `o`.


## Example usage of astar

```bash
python3 -m unittest tests.test_student.SearchTests -v
python3 run_project.py search --algorithm astar --start S --goal W
```

## Example usage of reinforcement learning (epsilon greedy)

```bash
python3 -m unittest tests.test_student.LearningTests -v
python3 -m unittest discover -v
python3 run_project.py train --start S --goal W --output results/baseline_SW
```

## Example usage result_plots.py

```bash
python3 result_plots.py results/custom_p02 p02
```
^creates a matplotlib graph containing training data from part 3 experiment data when --slip 0.2 is set

## Part 3 Experiment Settings
epsilon = 0.2\
alpha = 0.3\
gamma = 0.95\
slip p = 0.0, 0.1, 0.2\
episodes = 2000\
eval-episodes = 100\
max-steps = 200\
map = my_campus.txt\
start = S\
goal = W

