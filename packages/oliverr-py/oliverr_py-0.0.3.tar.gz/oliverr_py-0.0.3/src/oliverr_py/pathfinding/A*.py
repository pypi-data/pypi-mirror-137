# Oliver Rayner
# MASLab A* pathfinding application.
# January 2022

# Creates a grid and overlays walls and objects. Implements A* pathfinding.

import os
from Node import Node

class NoValidPath(Exception) :
    def __init__(self, initial, target) :
        self.message = 'No valid path found from Node %s to Node %s' % (initial, target)
        super().__init__(self.message)

class NotInGrid(Exception) :
    def __init__(self, coords) :
        self.message = 'Node (%s, %s) is not in the grid' % coords
        super().__init__(self.message)

class Field() :

    def __init__(self, resolution = '0x0', SCALE = 1, keep_away_distance = 1, path_file_path = 'paths') :

        self.SCALE = SCALE
        self.size = resolution
        self.keep_away_distance = keep_away_distance
        self.path_file_path = path_file_path

        # Else just create one from scratch using the given dimensions
        self.X, self.Y = ( int(num * self.SCALE) for num in resolution.split('x') )
        self.grid = [[Node((i, j)) for j in range(self.Y + 1)] for i in range(self.X + 1)]

    
    def distance(self, p1, p2) :
        ''' Finds the distance between two Nodes '''

        x1, y1 = p1.coords
        x2, y2 = p2.coords

        dX = abs(x2 - x1)
        dY = abs(y2 - y1)
        
        return 14 * min(dX, dY) + 10 * abs(dX - dY)

    def get_surrounding_nodes(self, node) : # CHANGE THIS FUCTION TO DO IN A RADIUS
        ''' Gathers the nodes surrounding a specific point '''

        # Limits can be 0, self.X-1, and self.Y-1
        surrounding_nodes = []
        x, y = node.coords
        for dx in (-1, 0, 1) :
            for dy in (-1, 0, 1) :
                x_new = x + dx
                y_new = y + dy
                if ((x_new >= 0 and x_new < self.X) and (y_new >= 0 and y_new < self.Y)) and not (x_new == x and y_new == y) :
                    surrounding_nodes.append(self[x_new, y_new])
        
        return surrounding_nodes

    def retrace_path(self, start_node, end_node) :
        ''' Build path from the end_node backwards to the start node '''
        
        path = []
        current_node = end_node

        while (current_node != start_node) :
            path.insert(0, current_node)
            current_node = current_node.parent
        path.insert(0, start_node)

        return path
    
    def path2file(self, path) :
        ''' Writes the path to a .path file '''

        f = open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.path_file_path), 'A*.path'), 'w')
        str_path = [ '%s\n' % node.__str__() for node in path ]
        f.writelines(str_path)
        str_path.reverse()
        f.writelines(str_path)
        str_path.reverse()
        f.writelines(str_path)


    def set_wall(self, coords) :
        ''' Defines a node in the grid as NOT-walkable '''

        X, Y = coords
        self[X, Y].walkable = False


    def pathfind(self, initial, target, write_to_file = False) :
        ''' Finds most efficient path from inital Node to target Node '''

        h_start = self.distance(initial, target)
        initial.h_cost = h_start

        open_set = [ initial ]
        closed_set = []

        while len(open_set) > 0 :
            current_node = open_set[0]
            for i in range(1, len(open_set)) :
                if open_set[i].f_cost() < current_node.f_cost() or (open_set[i].f_cost() == current_node.f_cost() and open_set[i].h_cost < current_node.h_cost) :
                    current_node = open_set[i]
            
            open_set.remove(current_node)
            closed_set.append(current_node)

            if current_node == target :   # If the path is found
                path = self.retrace_path(initial, target)
                if write_to_file :
                    self.path2file(path)
                return path


            for node in self.get_surrounding_nodes(current_node) :
                if (not node.walkable) or node in closed_set :
                    continue

                new_movement_cost_to_node = current_node.g_cost + self.distance(current_node, node)
                if (new_movement_cost_to_node < node.g_cost) or not (node in open_set) :
                    node.g_cost = new_movement_cost_to_node
                    node.h_cost = self.distance(node, target)
                    node.parent = current_node

                    if not (node in open_set) :
                        open_set.append(node)
        
        raise NoValidPath(initial, target)

    def __getitem__(self, tup):
        try :
            return self.grid[tup[0]][tup[1]]
        except (IndexError) :
            raise NotInGrid(tup)

    def __setitem__(self, tup, value):
        try :
            self.grid[tup[0]][tup[1]] = value
        except (IndexError) :
            raise NotInGrid(tup)



if __name__ == '__main__' :
    

    a = Field(resolution = '10x10', SCALE=2)
    path = [ node.__str__() for node in a.pathfind(a[2, 2], a[99, 99]) ]
    print(path)
    
    
