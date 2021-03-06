def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)


def cubic_hermite(A, B, C, D, t):
    a = -A / 2 + (3 * B) / 2 - (3 * C) / 2 + D / 2
    b = A - (5 * B) / 2 + 2 * C - D / 2
    c = -A / 2 + C / 2
    d = B
    return a * (t ** 3) + b * (t ** 2) + c * t + d


# This is meant to be a control point/node for computing hermetic splines
class Node:
    def __init__(self, x=0, y=0, tk_id=0, command=None):
        self.x = x
        self.y = y
        self.tk_id = tk_id
        # This will be implemented later
        self.command = command
        # Will be set based on what the command is, for now, just leave as red
        self.color = "#ff0000"

    def get_xy(self):
        return self.x, self.y

    # Return the tkinter id so we can delete
    def get_id(self):
        return self.tk_id
