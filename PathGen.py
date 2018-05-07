from math import floor
from tkinter import *
from Utils import *


# TODO Cascade menu from a control point to select commands to run
# TODO Load in field overview as background
# TODO Generate and save robot code to follow the path (how to move the motors between the points)
# TODO Calculate path for each side of robot (control point == center of drivetrain)
# TODO Put on github

# NOTE: for now start your path from the start


class PathGen(Frame):
    def __init__(self, master=None):
        self.master = master
        self.window = Canvas(self.master, width=200, height=100)
        self.window.pack(expand=YES, fill=BOTH)
        self.init_window()
        self.nodes = []
        self.node_manip = None
        self.lines = []
        self.num_samples = 100

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

    def generate_path(self):
        points = []
        for i in range(self.num_samples):
            pct = i / (self.num_samples - 1)
            tx = (len(self.nodes) - 1) * pct
            idx = int(tx)
            t = tx - floor(tx)

            A = self.get_node_clamped(idx - 1)
            B = self.get_node_clamped(idx)
            C = self.get_node_clamped(idx + 1)
            D = self.get_node_clamped(idx + 2)
            x = cubic_hermite(A[0], B[0], C[0], D[0], t)
            y = cubic_hermite(A[1], B[1], C[1], D[1], t)
            points.append((x, y))
        for line in self.lines:
            self.window.delete(line)

        for i in range(len(points) - 1):
            self.lines.append(self.window.create_line(*points[i], *points[i + 1], fill="red"))

    def get_node_clamped(self, idx):
        # Later add something so we can adjust the angle of the in/out on the 1st and last nodes
        if idx < 0:
            return self.nodes[0].get_xy()
        if idx >= len(self.nodes):
            return self.nodes[-1].get_xy()
        return self.nodes[idx].get_xy()

    def on_object_click(self, event):
        self.node_manip = self.closest_node(event)
        self.window.tag_bind(self.node_manip.tk_id, '<Motion>', self.motion_callback)
        self.window.tag_bind(self.node_manip.tk_id, '<Button-1>', self.release_node)
        self.remove_lines()

    def closest_node(self, event):
        min_dist = dist(self.nodes[0].get_xy(), (event.x, event.y))
        closest_node = self.nodes[0]
        for node in self.nodes:
            if min_dist > dist(node.get_xy(), (event.x, event.y)):
                min_dist = dist(node.get_xy(), (event.x, event.y))
                closest_node = node
        return closest_node

    def motion_callback(self, event):
        self.window.coords(self.node_manip.tk_id, event.x - 5, event.y - 5, event.x + 5, event.y + 5)

    def release_node(self, event):
        self.window.tag_unbind(self.node_manip.tk_id, '<Motion>')
        self.window.tag_bind(self.node_manip.tk_id, '<Button-1>', self.on_object_click)
        self.node_manip.x = event.x
        self.node_manip.y = event.y
        self.node_manip = None
        self.generate_path()

    def add_node(self, event):
        red = "#ff0000"
        p1, p2, center = ((event.x - 5), (event.y - 5)), ((event.x + 5), (event.y + 5)), (event.x, event.y)
        if any(dist(node.get_xy(), (event.x, event.y)) < 10 for node in self.nodes):
            return
        else:
            tk_id = self.window.create_oval(*p1, *p2, fill=red)
            self.window.tag_bind(tk_id, '<Button-1>', self.on_object_click)
            n = Node(*center, tk_id)
            self.nodes.append(n)
        if len(self.nodes) > 1:
            self.generate_path()

    def link(self):
        for line in self.lines:
            self.window.delete(line)
        if len(self.nodes) < 2:
            self.invalid_node_count()
            return
        for i in range(1, len(self.nodes)):
            self.lines.append(self.window.create_line(*self.nodes[i - 1].get_xy(), *self.nodes[i].get_xy(), fill="red"))

    def remove_lines(self):
        for line in self.lines:
            self.window.delete(line)
        self.lines = []

    def undo(self):
        if len(self.nodes) > 0:
            self.window.delete(self.nodes[-1].get_id())
            self.nodes = self.nodes[:-1]
        else:
            self.invalid_node_count()
        self.remove_lines()
        self.generate_path()

    def invalid_node_count(self):
        self.node_manip = Label(self.master, text="ERROR: not enough nodes for requested operation")
        self.node_manip.pack(side=BOTTOM)
        self.node_manip.after(1000, self.clear_label)

    def clear_label(self):
        print("clear label")
        self.node_manip.pack_forget()

    def app_exit(self):
        print("Exiting")
        exit(0)

