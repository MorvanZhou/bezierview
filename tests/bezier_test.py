import unittest

import bezierview


class BezierTest(unittest.TestCase):
    def test_bezier(self):
        points = [[50, 350], [250, 100], [330, 350], [450, 100]]
        dim = len(points[0])
        flat_points = []
        for p in points:
            flat_points.extend(p)
        curve = bezierview.bezier(flat_points, dim, step=10)
        self.assertEqual(10 * 2, len(curve))
        self.assertAlmostEqual(
            [50.0, 350.0, 112.44170096021948, 283.8134430727023, 167.31138545953362, 246.4334705075446,
             215.92592592592592, 229.62962962962965, 259.60219478738, 225.17146776406037, 299.6570644718793,
             224.82853223593963, 337.4074074074074, 220.37037037037035, 374.17009602194787, 203.5665294924554,
             411.2620027434842, 166.1865569272977, 450.0, 100.0],
            curve)
