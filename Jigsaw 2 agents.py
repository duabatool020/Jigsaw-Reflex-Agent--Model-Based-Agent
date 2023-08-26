#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
from queue import Queue

class Puzzle:
    def __init__(self, grid):
        self.grid = grid
        self.parent = None

    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.grid])

    def get_empty_cell(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    return i, j

    def can_move_down(self, row):
        return row < len(self.grid) - 1

    def can_move_up(self, row):
        return row > 0

    def can_move_right(self, col):
        return col < len(self.grid[0]) - 1

    def can_move_left(self, col):
        return col > 0

    def move_down(self, row, col):
        self.grid[row][col], self.grid[row+1][col] = self.grid[row+1][col], self.grid[row][col]

    def move_up(self, row, col):
        self.grid[row][col], self.grid[row-1][col] = self.grid[row-1][col], self.grid[row][col]

    def move_right(self, row, col):
        self.grid[row][col], self.grid[row][col+1] = self.grid[row][col+1], self.grid[row][col]

    def move_left(self, row, col):
        self.grid[row][col], self.grid[row][col-1] = self.grid[row][col-1], self.grid[row][col]

    def generate_neighbors(self):
        row, col = self.get_empty_cell()
        neighbors = []
        if self.can_move_down(row):
            neighbor = Puzzle([row[:] for row in self.grid])
            neighbor.move_down(row, col)
            neighbor.parent = self
            neighbors.append(neighbor)
        if self.can_move_up(row):
            neighbor = Puzzle([row[:] for row in self.grid])
            neighbor.move_up(row, col)
            neighbor.parent = self
            neighbors.append(neighbor)
        if self.can_move_right(col):
            neighbor = Puzzle([row[:] for row in self.grid])
            neighbor.move_right(row, col)
            neighbor.parent = self
            neighbors.append(neighbor)
        if self.can_move_left(col):
            neighbor = Puzzle([row[:] for row in self.grid])
            neighbor.move_left(row, col)
            neighbor.parent = self
            neighbors.append(neighbor)
        return neighbors

    
def is_solved(puzzle):
    n = len(puzzle.grid)
    nums = [i for i in range(n*n)]
    index = 0
    for row in puzzle.grid:
        for num in row:
            if num != nums[index]:
                return False
            index += 1
    return True

def generate_random_matrix(n):
    nums = list(range(n*n))
    random.shuffle(nums)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = nums.pop()
    return matrix

def solve_puzzle(start):
    queue = Queue()
    queue.put(start)
    visited = set([str(start)])
    while not queue.empty():
        current_puzzle = queue.get()
        if is_solved(current_puzzle):
            return current_puzzle
        for neighbor in current_puzzle.generate_neighbors():
            if str(neighbor) not in visited:
                queue.put(neighbor)
                visited.add(str(neighbor))
               
                if model_based_agent(neighbor):
                    queue.put(neighbor)
                    visited.add(str(neighbor))
    return None


def simple_reflex_agent(puzzle):
    goal = Puzzle([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    num_correct = 0
   
    if is_solved(puzzle):
        return []

   
    moves = []
    while not is_solved(puzzle):
        neighbors = puzzle.generate_neighbors()
        random_neighbor = random.choice(neighbors)
        moves.append(str(random_neighbor))
        puzzle = random_neighbor
    
    for i in range(len(puzzle.grid)):
        for j in range(len(puzzle.grid[i])):
            if puzzle.grid[i][j] == goal.grid[i][j]:
                num_correct += 1
    
    print("No of tiles placed correctly: ",num_correct)
    return moves


def model_based_agent(puzzle):
    
    if is_solved(puzzle):
        return True

   
    for neighbor in puzzle.generate_neighbors():
        if is_solved(neighbor):
            return True

  
    for neighbor in puzzle.generate_neighbors():
        for grand_neighbor in neighbor.generate_neighbors():
            if is_solved(grand_neighbor):
                return True

    
    current_score = get_score(puzzle)
    for neighbor in puzzle.generate_neighbors():
        neighbor_score = get_score(neighbor)
        if neighbor_score > current_score:
            return True

    return False
def print_path(puzzle):
    path = []
    goal = Puzzle([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    current_node = puzzle
    move_number = 0
    num_correct = 0
    for i in range(len(puzzle.grid)):
        for j in range(len(puzzle.grid[i])):
            if puzzle.grid[i][j] == goal.grid[i][j]:
                num_correct += 1
    while current_node is not None:
        path.append(( current_node))
        current_node = current_node.parent
        move_number += 1
    path.reverse()
    for i in range(move_number):
        print(" ")
        print(f"Move {i}:")
        print(path[i])
    print("No of tiles placed correctly: ",num_correct)
    print("Solution found by Model Based agent in", len(path) - 1, "moves")

def get_score(puzzle):
    n = len(puzzle.grid)
    nums = [i for i in range(n * n)]
    score = 0
    for row in puzzle.grid:
        for num in row:
            if num == nums[score]:
                score += 1
    return score




matrix= generate_random_matrix(3)
puzzle = Puzzle(matrix)

# Print the initial puzzle
print("======")
print("PUZZLE")
print("======")
print("Model based Agent:")
print(puzzle)





# Solve the puzzle using the A* algorithm
path = solve_puzzle(puzzle)


if path is None:
    print("Could not find a solution!")
else:
    print("Path to solve the puzzle:")
    print_path(path)
    

print()
print()
print("Reflex Agent: ")
print('Starting state:')
print(puzzle)
moves = simple_reflex_agent(puzzle)
print(f'Solution found by Reflex Agent in {len(moves)}')

  


# In[ ]:




