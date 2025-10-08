print("Simple Reflex Agent")

class TrafficLightAgent:
    def __init__(self, light_color, car_in_front):
        self.light_color = light_color
        self.car_in_front = car_in_front
        
    def act(self):
        if self.light_color == "red":
            return "Stopping ..."
        elif self.light_color == "green" and not self.car_in_front:
            return "Moving Forward"
        elif self.light_color == "green" and self.car_in_front:
            return "Waiting"
        else:
            return "Invalid State"
            
agent = TrafficLightAgent("red", True)
print(f"Action: {agent.act()}")

agent = TrafficLightAgent("green", False)
print(f"Action: {agent.act()}")

agent = TrafficLightAgent("green", True)
print(f"Action: {agent.act()}")
        
        
    
Thanks for letting me know you're heading to lunch! Below, I’ve compiled all the exercises assigned throughout our discussion, organized by topic, so you can review them later. These are drawn from the lessons on **Introduction to AI**, **Intelligent Agents**, **Problem Solving as Search**, **Informed Search**, **Adversarial Search**, **Constraint Satisfaction Problems (CSPs)**, and **Knowledge Representation**. I’ll list each exercise exactly as provided, with no additional explanation, so you have a clear reference. Enjoy your lunch, and let me know when you’re ready to continue!

---

### Exercises from Introduction to AI
1. Think of a real-world problem (e.g., traffic congestion). How might AI solve it under each of the four definitions (acting humanly, thinking humanly, thinking rationally, acting rationally)?
2. Research one AI milestone not listed [in the intro] and share why it's important.

---

### Exercises from Intelligent Agents
1. Design a simple reflex agent for a traffic light:
   - List its percepts, actions, and rules (e.g., `IF percept THEN action`).
2. For a self-driving car in traffic, classify its environment (observable? deterministic? etc.) and suggest which agent type is best.
3. (Optional) Write pseudocode for a simple reflex agent controlling a traffic light.

---

### Exercises from Problem Solving as Search
1. Define a search problem for a self-driving car navigating a city to a destination:
   - Specify initial state, actions, transition model, goal test, and path cost.
2. For the 3x3 grid [S . . / . # . / . . G]:
   - Trace the nodes explored by BFS and DFS to reach `G` from `S`. Which finds the shortest path?
3. (Optional) Write pseudocode for BFS to solve a grid navigation problem.

---

### Exercises from BFS Coding (Problem Solving as Search)
1. Modify the BFS code to print the grid with the path marked (e.g., use `*` for the path).
2. Try running BFS on a different grid (e.g., add more walls).
3. (Advanced) Extend BFS to handle weighted edges (e.g., roads with different travel times).

---

### Exercises from Informed Search
1. For the 3x3 grid [S . . / . # . / . . G]:
   - Define an admissible heuristic (e.g., Manhattan distance: \( |x_1 - x_2| + |y_1 - y_2| \)).
   - Trace A* search from (0,0) to (2,2). How does it differ from BFS?
2. Design a heuristic for a traffic navigation problem (e.g., distance, estimated time considering traffic).
3. (Optional) Modify the BFS code to implement A* search with a Manhattan distance heuristic.

---

### Exercises from Adversarial Search
1. For tic-tac-toe:
   - Draw a partial game tree starting with an empty board, X’s turn.
   - Apply Minimax to find X’s best move.
2. Suggest a heuristic for a chess AI at a depth limit (e.g., count pieces).
3. (Optional) Write pseudocode for alpha-beta pruning.

---

### Exercises from Constraint Satisfaction Problems (CSPs)
1. Define a CSP for scheduling traffic lights at two intersections:
   - Specify variables, domains, constraints.
2. Suggest how backtracking could solve it.

---

### Exercises from Knowledge Representation
1. Write 3 propositional logic rules for a traffic light agent.
2. Suggest how first-order logic could model multiple cars at an intersection.

---

### Notes
- You’ve already answered some exercises (e.g., Intelligent Agents, Problem Solving as Search). If you want feedback on those or to tackle the unanswered ones (e.g., tracing BFS/DFS, tic-tac-toe game tree), let me know.
- For coding exercises (e.g., BFS, A*, or CSP solvers), I can provide guidance or solutions when you’re back.
- Next steps: We can deepen **CSPs** (e.g., code a backtracking solver), explore **Knowledge-Based Agents**, or focus on any exercise.

Enjoy your lunch, and ping me when you’re ready to dive back in!