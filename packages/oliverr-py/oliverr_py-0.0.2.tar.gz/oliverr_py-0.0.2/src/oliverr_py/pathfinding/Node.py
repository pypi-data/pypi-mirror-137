# Oliver Rayner
# MASLab Node Library
# January 2022

# Helper class for pathfinding

class Node() :

    def __init__(self, coords = (None, None), walkable = True, g_cost = 0, h_cost = 0) :
        
        if type(coords) == str :
            self.coords = eval(coords)
        else :    
            self.coords = coords
        self.walkable = walkable
        self.g_cost = g_cost
        self.h_cost = h_cost

        self.parent = None
    
    def f_cost(self) :
        return self.h_cost + self.g_cost

    def __str__(self) :
        x, y = self.coords
        return '(%s, %s)' % (x, y)

    def __sub__(self, other) :

        dX = self.coords[0] - other.coords[0]
        dY = self.coords[1] - other.coords[1]
        return dX, dY

    def __getitem__(self, index) :
        return self.coords[index]
    
