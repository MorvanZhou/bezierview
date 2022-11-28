# BezierView

View Bezier Curve transformation by Python.

## Install

```shell
pip install bezierview
```

# Play

Play Bezier Curve with pure python.

![play](https://github.com/MorvanZhou/bezierview/raw/main/curve_play.gif)

```python
import bezierview

bezierview.play()
```

# Animation

View an animated creation of pre-defined points.

![animation](https://github.com/MorvanZhou/bezierview/raw/main/curve.gif)

```python
import bezierview

points = [[50, 350], [250, 100], [330, 350], [450, 100]]
bezierview.animate(points)
```

# View static curve

View a static plot of pre-defined points.

```python
import bezierview

points = [[50, 350], [250, 100], [330, 350], [450, 100]]
bezierview.show(points)
```

![pic](https://github.com/MorvanZhou/bezierview/raw/main/curve.png)
