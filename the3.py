import math
eps = 0.000001


class Polygon:
    def __init__(self, lst):
        self.points = lst
        self.edges = [(lst[n], lst[(n + 1) % len(lst)]) for n in range(len(lst))]
        for i in range(len(lst)):
            setattr(self, f'p{i}', lst[i])
            setattr(self, f'edge{i}', (lst[i], lst[(i + 1) % len(lst)]))

    def __iter__(self):
        return iter(self.points)

    def __str__(self):
        return str(self.points)

    def __len__(self):
        return len(self.points)


class Triangle(Polygon):
    def __init__(self, lst):
        super().__init__(lst)


class Tetragon(Polygon):
    def __init__(self, lst):
        super().__init__(lst)


class Line:
    def __init__(self, lst):
        self.x0 = lst[0][0]
        self.x1 = lst[1][0]
        self.y0 = lst[0][1]
        self.y1 = lst[1][1]
        self.points = [lst[0], lst[1]]

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, key):
        return self.points[key]


def calculate_angle(point1, point2):
    # Calculates the angle between the line from p1 to p2, and the x-axis.
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])


def angle(line):
    return calculate_angle(line[0], line[1])


def order(coordinates):  # find the center and then sort with respect to angles
    if not coordinates:
        return []
    center_x = sum(x for x, y in coordinates)/len(coordinates)
    center_y = sum(y for x, y in coordinates)/len(coordinates)
    center = (center_x, center_y)
    # Sort them accordingly
    sorted_coordinates = sorted(coordinates, key=lambda point: calculate_angle(center, point))
    return sorted_coordinates


def is_between(x1, x2, x3):
    return x1 <= x3 <= x2 or x2 <= x3 <= x1


def is_intersect(line1, line2):
    angle_between = abs(angle(line1) - angle(line2))
    if angle_between < eps or abs(angle_between - math.pi) < eps:  # if lines do NOT intersect
        return False
    else:
        return True


def is_perpendicular(line):
    if abs(line[0][0] - line[1][0]) < eps:  # difference between x coordinates is zero
        return True
    else:
        return False


def is_horizontal(line):
    if abs(line[0][1] - line[1][1]) < eps:  # difference between y coordinates is zero
        return True
    else:
        return False


def is_same_point(point1, point2):
    return abs(point1[0] - point2[0]) < eps and abs(point1[1] - point2[1]) < eps


def is_cross(edge, line):  # check whether the line intersect the edge
    edge = Line(edge)
    line = Line(line)
    if not is_intersect(edge, line):
        return []
    else:  # they intersect
        if is_perpendicular(edge) and not is_perpendicular(line):  # if edge is perpendicular to the x axis
            x = edge.x0
            y = (x - line.x0) * math.tan(angle(line)) + line.y0
            return [x, y]*is_between(edge.y0, edge.y1, y)  # if intersect_y is on the edge
        elif is_perpendicular(line) and not is_perpendicular(edge):  # if line is perpendicular to the x axis
            x = line.x0
            y = (x - edge.x0) * math.tan(angle(edge)) + edge.y0
            return [x, y]*is_between(edge.x0, edge.x1, x)  # if intersect_x is on the edge
        else:  # neither of them are perpendicular to the x axis
            c0 = edge.y0 - (math.tan(angle(edge)) * edge.x0)
            c1 = line.y0 - (math.tan(angle(line)) * line.x0)
            x = (c0 - c1)/(math.tan(angle(line)) - math.tan(angle(edge)))
            y = x * math.tan(angle(edge)) + c0
            if abs(edge.y0 - edge.y1) < eps:  # if the edge is horizontal
                return [x, y]*is_between(edge.x0, edge.x1, x)
            else:
                return [x, y]*is_between(edge.y0, edge.y1, y)  # it doesn't matter whether the line is horizontal


def is_inside(point, polygon):
    line = point, ((point[0] + 1), point[1])
    temp = []
    for edge in polygon.edges:
        a = is_cross(edge, line)
        if a:
            if a not in temp:
                temp += [a]
    if len(temp) == 3:  # making sure that vertices are not repeated
        if is_same_point(temp[0], temp[1]) or is_same_point(temp[0], temp[-1]):
            temp = [temp[1], temp[-1]]
    if len(temp) == 4:
        temp = [temp[0], temp[2]]
    if len(temp) <= 1:
        return False
    else:
        return is_between(temp[0][0], temp[1][0], point[0])


def area_n(lst):  # shoelace formula
    if not lst:
        return 0
    left = 0
    right = 0
    for i in range(len(lst)):
        left += lst[i][0]*lst[(i + 1) % len(lst)][1]
        right += lst[i][1]*lst[(i + 1) % len(lst)][0]
    return abs(right - left)/2


def area(tetragon, triangle):
    tetragon = Tetragon(tetragon)
    triangle = Triangle(triangle)
    lst = []
    for point in triangle.points:
        if is_inside(point, tetragon):
            lst += [point]
    for point in tetragon.points:
        if is_inside(point, triangle):
            lst += [point]
    for edge_tri in triangle.edges:
        for edge_tet in tetragon.edges:
            if is_cross(edge_tri, edge_tet):
                p = is_cross(edge_tri, edge_tet)
                if is_perpendicular(edge_tet):
                    lst += [is_cross(edge_tri, edge_tet)]*is_between(edge_tet[0][1], edge_tet[1][1], p[1])
                elif is_between(edge_tet[0][0], edge_tet[1][0], p[0]):
                    lst += [is_cross(edge_tri, edge_tet)]
    ordered_list = order(lst)
    return area_n(ordered_list)
