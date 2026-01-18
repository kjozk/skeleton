import unittest
from skeleton import generate_skeleton


class TestSkeletonGeneration(unittest.TestCase):

    def test_convex_rectangle(self):
        polygon = [
            (0, 0),
            (10, 0),
            (10, 4),
            (0, 4)
        ]

        skeleton = generate_skeleton(polygon)

        self.assertEqual(len(skeleton), 1)
        (p1, p2) = skeleton[0]

        # 中心線は y = 2
        self.assertAlmostEqual(p1[1], 2.0)
        self.assertAlmostEqual(p2[1], 2.0)

    def test_concave_u_shape(self):
        polygon = [
            (0, 0),
            (6, 0),
            (6, 4),
            (4, 4),
            (4, 1),
            (2, 1),
            (2, 4),
            (0, 4)
        ]

        skeleton = generate_skeleton(polygon)

        # 凹頂点が2つ → 芯線2本
        self.assertEqual(len(skeleton), 2)

        for start, end in skeleton:
            # 始点は必ず凹頂点
            self.assertIn(start, polygon)
            # 終点はポリゴン中心付近
            self.assertTrue(1.0 <= end[0] <= 5.0)
            self.assertTrue(1.0 <= end[1] <= 3.0)


if __name__ == "__main__":
    unittest.main()
