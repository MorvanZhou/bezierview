# BezierView

View Bezier Curve transformation by Python.

## Install

```shell
pip install bezierview
```

# Play animation


```python
import bezierview

points = [[50, 350], [250, 100], [330, 350], [450, 100]]
bezierview.animate(points)
```

![animation](https://github.com/MorvanZhou/sudoku/raw/main/curve.png)

# View static curve

```python
import bezierview

points = [[50, 350], [250, 100], [330, 350], [450, 100]]
bezierview.show(points)
```

![pic](https://github.com/MorvanZhou/sudoku/raw/main/curve.png)
