from tkinter import *

from math import floor

from Utils import *


# TODO Add ability to move control nodes
# TODO Refresh lines automatically
# TODO Cascade menu from a control point to select commands to run
# TODO Load in field overview as background
# TODO Generate and save robot code to follow the path (how to move the motors between the points)
# TODO Put on github

class PathGen(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.window = Canvas(self.master, width=200, height=100)
        self.window.pack(expand=YES, fill=BOTH)
        self.init_window()
        self.nodes = []
        self.status = None
        self.lines = []
        self.num_samples = 200

    def init_window(self):
        self.master.title("GUI")
        menu = Menu(self.master)
        self.master.config(menu=menu)

        self.window.bind("<ButtonRelease-1>", self.add_node)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.app_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo", command=self.undo)
        edit.add_command(label="Link", command=self.link)
        menu.add_cascade(label="Edit", menu=edit)

        tools = Menu(menu)
        tools.add_command(label="Generate Paths", command=self.generate_points)
        menu.add_cascade(label="Tools", menu=tools)

    def on_object_click(self, event):
        print('Got a click at ({}, {})'.format(event.x, event.y))

    def add_node(self, event):
        red = "#ff0000"
        p1, p2, center = ((event.x - 5), (event.y - 5)), ((event.x + 5), (event.y + 5)), (event.x, event.y)
        if any(dist(a.get_xy(), (event.x, event.y)) < 10 for a in self.nodes):
            print("HI")
        else:
            id = self.window.create_oval(*p1, *p2, fill=red)
            self.window.tag_bind(id, '<c><Button-1>', self.on_object_click)
            n = Node(*center, id)
            self.nodes.append(n)

    def generate_points(self):
        points = []
        for i in range(self.num_samples):
            pct = i / (self.num_samples - 1)
            tx = (len(self.nodes) - 1) * pct
            idx = int(tx)
            t = tx - floor(tx)
            A = self.get_element_clamped(idx - 1)
            B = self.get_element_clamped(idx)
            C = self.get_element_clamped(idx + 1)
            D = self.get_element_clamped(idx + 2)
            x = cubic_hermite(A[0], B[0], C[0], D[0], t)
            y = cubic_hermite(A[1], B[1], C[1], D[1], t)
            points.append((x, y))
        self.remove_lines()
        for i in range(1, len(points)):
            self.lines.append(self.window.create_line(*points[i - 1], *points[i], fill="red"))

    def get_element_clamped(self, idx):
        if idx < 0:
            return self.nodes[0].get_xy()
        if idx >= len(self.nodes):
            return self.nodes[-1].get_xy()
        return self.nodes[idx].get_xy()

    def link(self):
        for line in self.lines:
            self.window.delete(line)
        if len(self.nodes) < 2:
            self.invalid_node_count()
            return
        for i in range(1, len(self.nodes)):
            self.lines.append(self.window.create_line(*self.nodes[i - 1].get_xy(), *self.nodes[i].get_xy(), fill="red"))

    def undo(self):
        if len(self.nodes) > 0:
            self.window.delete(self.nodes[-1].get_id())
            self.nodes = self.nodes[:-1]
        else:
            self.invalid_node_count()

    def clear_label(self):
        print("clear label")
        self.status.pack_forget()

    def app_exit(self):
        print("Exiting")
        exit(0)

    def invalid_node_count(self):
        self.status = Label(self.master, text="ERROR: not enough nodes for requested operation")
        self.status.pack(side=BOTTOM)
        self.status.after(1000, self.clear_label)

    def remove_lines(self):
        for line in self.lines:
            self.window.delete(line)
root = Tk()
app = PathGen(root)
root.mainloop()
