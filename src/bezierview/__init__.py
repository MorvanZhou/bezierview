from bezierview.view import Draw
from bezierview.bezier import bezier


def show(points):
    root = Draw(points)
    root.show()
    root.mainloop()


def animate(points):
    root = Draw(points)
    root.move()
    root.mainloop()
