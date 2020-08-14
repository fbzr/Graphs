from room import Room
from player import Player
from world import World
from queue import LifoQueue


import os
import random
from ast import literal_eval

def get_opposite_direction(direction):
        if direction == 'n':
            return 's'
        if direction == 's':
            return 'n'
        if direction == 'w':
            return 'e'
        if direction == 'e':
            return 'w'
        
        raise AttributeError("Invalid attribute")

class Graph:
    def __init__(self):
        self.rooms = {}
    
    def add_room(self, room_id, exits):
        self.rooms[room_id] = {}
        
        for direction in exits:
            self.rooms[room_id][direction] = '?'

    def add_exit(self, room1, room2, direction):
        self.rooms[room1][direction] = room2

        if room2 not in self.rooms:
            self.rooms[room2] = {}

        self.rooms[room2][get_opposite_direction(direction)] = room1

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = os.path.abspath("projects/adventure/maps/main_maze.txt")

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
'''
room_graph:
    {0: [(3, 5), {'n': 1}], 1: [(3, 6), {'s': 0, 'n': 2}], 2: [(3, 7), {'s': 1}]}   
'''


world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

exits = player.current_room.get_exits()
random.shuffle(exits)

# chose random initial direction

# create graph
graph = Graph()
# add initial room to graph
graph.add_room(player.current_room.id, exits)


stack = LifoQueue()

# add initial directions to stack
for direction in exits:
    stack.put(direction)

# print(f"initial stack {stack}")

recovery_path = []
visited = set()

while not stack.empty():
    room = player.current_room
    # print(f"\ncurrent room {room.id}")
    if room.id not in visited:
        visited.add(room.id)

    # if there is no unvisited room around current room (dead end):
    if not '?' in graph.rooms[room.id].values() and len(recovery_path):
        # trace back the steps until find unvisited neighbors
        # that means you are back on track with the stack
        
        way_back = get_opposite_direction(recovery_path.pop())
        # add that travel to traversal result
        traversal_path.append(way_back)
        player.travel(way_back)
    else:
        # print(f"current stack {stack}")
        next_direction = stack.get()
        # print(f"pop next direction {next_direction}")

        next_room = room.get_room_in_direction(next_direction)
        if next_room:
            next_exits = next_room.get_exits()

            if next_room.id not in graph.rooms:
                # update graph if it is a new room in graph
                graph.add_room(next_room.id, next_exits)
            
            # add path between rooms to graph before verify for unexplored exits below
            graph.add_exit(room.id, next_room.id, next_direction)

            if next_room.id not in visited:
                for e in next_exits:
                    if graph.rooms[next_room.id][e] == '?':
                        # print(f"add next exit {e}")
                        stack.put(e)
                        # print(f"current stack {stack}")

                # add to traversal list
                traversal_path.append(next_direction)
                # add to recovery path
                recovery_path.append(next_direction)
                # move to that next_room that was in stack
                player.travel(next_direction)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
