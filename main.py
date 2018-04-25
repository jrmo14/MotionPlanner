from tkinter import Tk
from PathGen import PathGen
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-x", help="x dim of the window", type=int, default=640)
parser.add_argument("-y", help="y dim of the window", type=int, default=480)
parser.add_argument("-f", "--fullscreen", help="if set, go full screen")
args = parser.parse_args()

root = Tk()
root.minsize(width=args.x, height=args.y)
root.maxsize(width=args.y, height=args.y)
app = PathGen(root)
root.mainloop()
