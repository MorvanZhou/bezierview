from bezierview.bezier import bezier
from bezierview.view import Draw


def show(points):
    root = Draw(points)
    root.show()
    root.mainloop()


def animate(points):
    root = Draw(points)
    root.move()
    root.mainloop()


def play():
    root = Draw([])
    root.after(1000, root.play)
    root.mainloop()
