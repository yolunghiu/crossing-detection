import sys
import numpy as np

import cv2

# from line_boundary_check import *

g_mouse_pos = [0, 0]


# Mouse event handler
def onMouse(event, x, y, flags, param):
    global g_mouse_pos
    g_mouse_pos = [x, y]


class area:
    def __init__(self, contour):
        self.contour = np.array(contour, dtype=np.int32)
        self.count = 0


# Test whether the test_point is in the polygon or not
# test_point = (x,y)
# polygon = collection of points  [ (x0,y0), (x1,y1), (x2,y2) ... ]
def pointPolygonTest(polygon, test_point):
    if len(polygon) < 3:
        return False
    prev_point = polygon[-1]  # Use the last point as the starting point to close the polygon
    line_count = 0
    for point in polygon:
        if test_point[1] >= min(prev_point[1], point[1]) and test_point[1] <= max(prev_point[1], point[
            1]):  # Check if Y coordinate of the test point is in range
            gradient = (point[0] - prev_point[0]) / (point[1] - prev_point[1])  # delta_x / delta_y
            line_x = prev_point[0] + (test_point[1] - prev_point[1]) * gradient  # Calculate X coordinate of a line
            if line_x < test_point[0]:
                line_count += 1
        prev_point = point
    included = True if line_count % 2 == 1 else False  # Check how many lines exist on the left to the test_point
    return included


# Draw areas (polygons)
def drawAreas(img, areas):
    for area in areas:
        if area.count > 0:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)
        cv2.polylines(img, [area.contour], True, color, 4)
        cv2.putText(img, str(area.count), (area.contour[0][0], area.contour[0][1]), cv2.FONT_HERSHEY_PLAIN, 4, color, 2)


# Area intrusion check
def checkAreaIntrusion(area, points):
    area.count = 0
    for pt in points:
        if pointPolygonTest(area.contour, pt):
            area.count += 1


# ----------------------------------------------------------------------------

# Areas
areas = [
    area([[200, 130], [500, 130], [200, 450], [500, 450], [100, 360]])
]


def main():
    cv2.namedWindow('Detection')
    cv2.setMouseCallback('Detection', onMouse)

    key = -1
    while key != 27:  # ESC key
        img = np.zeros((600, 800, 3), dtype=np.uint8)

        for area in areas:
            checkAreaIntrusion(area, (g_mouse_pos,))
        drawAreas(img, areas)

        cv2.imshow('Detection', img)
        key = cv2.waitKey(50)

    return 0


if __name__ == '__main__':
    sys.exit(main())
