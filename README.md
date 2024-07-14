# Restaurant Simulator

This project is a simulation of a working night in a restaurant. The main goal is to optimize the table layout based on the amount of tipping received in a night. The simulation takes into account the number of waiters, a set of dishes with their type (starter, main course, dessert), preparation time, and other factors. The layout of the restaurant is represented as a 2D matrix, where a cell can be an empty space, a table, a person, or the kitchen door. Customers arrive following a Poisson distribution and their type is randomly assigned. The tip amount for a customer decreases in various ways, such as when they are waiting or when they are too close to another customer. The layout is optimized using the Simulated Annealing metaheuristic, and a layout is evaluated based on a series of simulations that give a tipping average.

## Running the Project

You can run the project in two modes: `optimizer` or `single_simulation`. 

- `optimizer`: This mode runs the Simulated Annealing algorithm to optimize the restaurant layout. It iteratively explores different layouts, evaluating their performance based on the average tipping received in a series of simulations.


```bash
python main.py --mode optimizer
```

- `single_simulation`: This mode runs a single simulation of a working night in the restaurant a given layout. It's useful to quickly test changes or new features.

```bash
python main.py --mode single_simulation
```

If you want to enable verbose mode, add the --verbose flag:

```bash
python main.py --mode optimizer --verbose
```

These commands should be run in the terminal from the directory where your main.py file is located.