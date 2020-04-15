import os
from collections import defaultdict


class MazeError(Exception):
    def __init__(self, message):
        self.message = message


class Maze(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.gates = 0
        self.inner_point = 0
        self.accesible_area = 0
        self.walls = 0
        self.entry_num = 0
        self.cul_de_sacs = 0
        self.wall_dict_count_wall = \
            {0: [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 1: [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
             2: [[1, 0, 0], [1, 0, 0], [1, 0, 0]], 3: [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
             '0': [[0, 0, 1], [0, 0, 1], [0, 0, 1]], '1': [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
             '2': [[1, 0, 1], [1, 0, 1], [1, 0, 1]], '3': [[1, 1, 1], [1, 0, 1], [1, 0, 1]],
             '00': [[0, 0, 0], [0, 0, 0], [1, 1, 1]], '11': [[1, 1, 1], [0, 0, 0], [1, 1, 1]],
             '22': [[1, 0, 0], [1, 0, 0], [1, 1, 1]], '33': [[1, 1, 1], [1, 0, 0], [1, 1, 1]],
             '000': [[0, 0, 1], [0, 0, 1], [1, 1, 1]], '111': [[1, 1, 1], [0, 0, 1], [1, 1, 1]],
             '222': [[1, 0, 1], [1, 0, 1], [1, 1, 1]], '333': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
             }
        self.wall_find_way_dict = \
            {0: [[1, 0, 1], [0, 0, 0], [1, 0, 1]], 1: [[1, 1, 1], [0, 0, 0], [1, 0, 1]],
             2: [[1, 0, 1], [1, 0, 0], [1, 0, 1]], 3: [[1, 1, 1], [1, 0, 0], [1, 0, 1]],
             '0': [[1, 0, 1], [0, 0, 1], [1, 0, 1]], '1': [[1, 1, 1], [0, 0, 1], [1, 0, 1]],
             '2': [[1, 0, 1], [1, 0, 1], [1, 0, 1]], '3': [[1, 1, 1], [1, 0, 1], [1, 0, 1]],
             '00': [[1, 0, 1], [0, 0, 0], [1, 1, 1]], '11': [[1, 1, 1], [0, 0, 0], [1, 1, 1]],
             '22': [[1, 0, 1], [1, 0, 0], [1, 1, 1]], '33': [[1, 1, 1], [1, 0, 0], [1, 1, 1]],
             '000': [[1, 0, 1], [0, 0, 1], [1, 1, 1]], '111': [[1, 1, 1], [0, 0, 1], [1, 1, 1]],
             '222': [[1, 0, 1], [1, 0, 1], [1, 1, 1]], '333': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
             }

    def read_txt(self):
        # read the txt and get a maze matrix
        with open(self.file_name, 'r') as maze_file:
            matrix, matrix_ls = maze_file.readlines(), []
            for l in matrix:
                cur_line = [i for i in l if i and i != '\n' and i != ' ']
                if cur_line:
                    matrix_ls.append(cur_line)
        # convert all str element to int

        for i in range(len(matrix_ls)):
            if all([str(a).isdigit() for a in matrix_ls[i]]):
                cur_ls = list(map(int, matrix_ls[i]))
                matrix_ls[i] = cur_ls
            else:
                raise MazeError('Incorrect input.')
        return matrix_ls

    def check_maze(self, matrix):
        # change all elements into int type
        width = len(matrix[0])
        if matrix:
            # the height of the matrix cannot be over 41
            if len(matrix) < 2 or len(matrix) > 41:
                raise MazeError('Incorrect input.')
            for r in range(len(matrix)):
                if len(matrix[r]) != width:
                    raise MazeError('Incorrect input.')
                if len(matrix[r]) > 31 or len(matrix[r]) < 2:
                    # the width of the matrix cannot be over 31
                    raise MazeError('Incorrect input.')
                for e in matrix[r]:
                    if e not in [0, 1, 2, 3]:
                        # the matrix can contain only 0,1,2,3
                        raise MazeError('Incorrect input.')
                if matrix[r][-1] == 1 or matrix[r][-1] == 3:
                    raise MazeError('Input does not represent a maze.')
                # the last digit of each row cannot be 1 or 3
            if 2 in matrix[-1] or 3 in matrix[-1]:
                # the last row cannot contain 2 or 3
                raise MazeError('Input does not represent a maze.')
            return matrix
        else:
            raise MazeError('Incorrect input.')

    def count_gates(self, matrix):
        # focus on the frontier of the matrix
        count_up = matrix[0].count(0) + matrix[0].count(2) - 1
        count_down = matrix[-1].count(0) - 1
        count_left, count_right = 0, 0
        for r in range(len(matrix)):
            if matrix[r][0] == 0 or matrix[r][0] == 1:
                count_left += 1
            if matrix[r][-1] == 0:
                count_right += 1
        count_right -= 1
        count_left -= 1
        return (count_up + count_left + count_right + count_down)

    def create_nary_3_matrix(self, matrix, wall_dict):
        # assign a 3*3 matrix to each elements of the given matrix
        # and return the generated large map of the maze
        nary_3_matrix = []
        for r in range(len(matrix)):
            cur_line1, cur_line2, cur_line3 = [], [], []
            for c in range(len(matrix[r])):
                if c <= len(matrix[r]) - 2 and r <= len(matrix) - 2 and matrix[r][c + 1] in [2, 3] and matrix[r + 1][
                    c] in [1, 3]:
                    cur_line1 += wall_dict[str(matrix[r][c]) * 3][0]
                    cur_line2 += wall_dict[str(matrix[r][c]) * 3][1]
                    cur_line3 += wall_dict[str(matrix[r][c]) * 3][2]
                elif r <= len(matrix) - 2 and matrix[r + 1][c] in [1, 3]:
                    cur_line1 += wall_dict[str(matrix[r][c]) * 2][0]
                    cur_line2 += wall_dict[str(matrix[r][c]) * 2][1]
                    cur_line3 += wall_dict[str(matrix[r][c]) * 2][2]
                elif c <= len(matrix[r]) - 2 and matrix[r][c + 1] in [2, 3]:
                    cur_line1 += wall_dict[str(matrix[r][c])][0]
                    cur_line2 += wall_dict[str(matrix[r][c])][1]
                    cur_line3 += wall_dict[str(matrix[r][c])][2]
                else:
                    cur_line1 += wall_dict[matrix[r][c]][0]
                    cur_line2 += wall_dict[matrix[r][c]][1]
                    cur_line3 += wall_dict[matrix[r][c]][2]
            nary_3_matrix.append(cur_line1)
            nary_3_matrix.append(cur_line2)
            nary_3_matrix.append(cur_line3)
        nary_3_matrix = [i[:-2] for i in nary_3_matrix[:-2]]
        return nary_3_matrix

    def count_walls(self, matrix):
        # assign each element a 3*3 matrix

        nary_3_matrix = self.create_nary_3_matrix(matrix, self.wall_dict_count_wall)

        # traverse the whole list to find connected wall
        visited_ls = []
        walls = 0
        n_heigth = len(nary_3_matrix)
        n_width = len(nary_3_matrix[0])
        for r in range(len(nary_3_matrix)):
            for c in range(len(nary_3_matrix[r])):
                if [r, c] in visited_ls:
                    continue
                if nary_3_matrix[r][c] == 0:
                    visited_ls.append([r, c])
                    continue
                cur_ls = [[r, c]]
                while True:
                    new_ls = cur_ls
                    for i in cur_ls:
                        if (i[1] + 1) <= n_width - 1 and nary_3_matrix[i[0]][i[1] + 1] == 1 \
                                and [i[0], i[1] + 1] not in new_ls:
                            new_ls.append([i[0], i[1] + 1])
                        if (i[0] + 1) <= n_heigth - 1 and nary_3_matrix[i[0] + 1][i[1]] == 1 \
                                and [i[0] + 1, i[1]] not in new_ls:
                            new_ls.append([i[0] + 1, i[1]])
                        if (i[0] - 1) >= 0 and nary_3_matrix[i[0] - 1][i[1]] == 1 \
                                and [i[0] - 1, i[1]] not in new_ls:
                            new_ls.append([i[0] - 1, i[1]])
                        if (i[1] - 1) >= 0 and nary_3_matrix[i[0]][i[1] - 1] == 1 \
                                and [i[0], i[1] - 1] not in new_ls:
                            new_ls.append([i[0], i[1] - 1])
                    if new_ls == cur_ls:
                        break
                for i in cur_ls:
                    visited_ls.append(i)
                walls += 1
        return walls

    def extending(self, nary_3_matrix, num):
        visited_ls = []
        area = 0
        n_heigth = len(nary_3_matrix)
        n_width = len(nary_3_matrix[0])
        shape_ls = []
        count_1 = 0
        for r in range(len(nary_3_matrix)):
            for c in range(len(nary_3_matrix[r])):
                if [r, c] in visited_ls:
                    continue
                else:
                    if nary_3_matrix[r][c] == num:
                        count_1 += 1
                if nary_3_matrix[r][c] != num:
                    visited_ls.append([r, c])
                    continue
                cur_ls = [[r, c]]
                while True:
                    new_ls = cur_ls
                    for i in cur_ls:
                        if (i[1] + 1) <= n_width - 1 and nary_3_matrix[i[0]][i[1] + 1] == num \
                                and [i[0], i[1] + 1] not in new_ls:
                            new_ls.append([i[0], i[1] + 1])
                        if (i[0] + 1) <= n_heigth - 1 and nary_3_matrix[i[0] + 1][i[1]] == num \
                                and [i[0] + 1, i[1]] not in new_ls:
                            new_ls.append([i[0] + 1, i[1]])
                        if (i[0] - 1) >= 0 and nary_3_matrix[i[0] - 1][i[1]] == num \
                                and [i[0] - 1, i[1]] not in new_ls:
                            new_ls.append([i[0] - 1, i[1]])
                        if (i[1] - 1) >= 0 and nary_3_matrix[i[0]][i[1] - 1] == num \
                                and [i[0], i[1] - 1] not in new_ls:
                            new_ls.append([i[0], i[1] - 1])
                    if new_ls == cur_ls:
                        shape_ls.append(cur_ls)
                        break
                for i in cur_ls:
                    visited_ls.append(i)
                area += 1
        return shape_ls, area, count_1

    def count_accessible_inaccessible_area(self, matrix):
        # assign each element a large nary_3_matrix
        nary_3_matrix = self.create_nary_3_matrix(matrix, self.wall_find_way_dict)

        n_heigth = len(nary_3_matrix)
        n_width = len(nary_3_matrix[0])

        # traverse the whole list to find all accessible area like quiz7
        shape_ls, area, num = self.extending(nary_3_matrix, 0)

        # differentiate accessible areas and inaccessible areas
        ac_area, in_area, in_area_size = 0, 0, 0
        for a in shape_ls:
            x_ls, y_ls = zip(*a)
            if 0 not in x_ls and (n_heigth - 1) not in x_ls and 0 not in y_ls and (n_width - 1) not in y_ls:
                # if not connected to frontier, then it's inaccessible area(inner point)
                in_area += 1
                in_area_size += (len(a) // 3 + 1)
        ac_area = area - in_area
        return ac_area, in_area_size

    def entry_exit_intersection(self, nary_3_matrix):
        n_heigth = len(nary_3_matrix)
        n_width = len(nary_3_matrix[0])
        # find gate_ls
        path_ls = self.extending(nary_3_matrix, 0)[0]
        path_num = 0
        valid_path_ls = []

        for p in path_ls:
            gate_num = 0
            valid = True
            for i in p:
                # frontier
                if i[0] == 0 or i[0] == n_heigth - 1 or i[1] == 0 or i[1] == n_width - 1:
                    gate_num += 1
                else:
                    inter_count = 0
                    near_by = [[i[0]+1,i[1]], [i[0]-1, i[1]], [i[0], i[1]+1],[i[0], i[1]-1]]
                    for b in near_by:
                        if b in p:
                            inter_count+=1
                    if inter_count>2:
                        valid = False
            if gate_num == 2 and valid:
                path_num += 1
                valid_path_ls.append(p)
        return path_num, valid_path_ls

    def findspike(self, nary_3_matrix, shape_ls):
        n_heigth = len(nary_3_matrix)
        n_width = len(nary_3_matrix[0])
        spike_ls = []
        for s in shape_ls:
            for i in s:
                if nary_3_matrix[i[0]][i[1]] == 0:
                    if i[0] != 0 and i[0] != n_heigth - 1 and i[1] != 0 and i[1] != n_width - 1:
                        count = 0
                        if nary_3_matrix[i[0] + 1][i[1]] == 1 or nary_3_matrix[i[0] + 1][i[1]] == 2:
                            count += 1
                        if nary_3_matrix[i[0] - 1][i[1]] == 1 or nary_3_matrix[i[0] - 1][i[1]] == 2:
                            count += 1
                        if nary_3_matrix[i[0]][i[1] + 1] == 1 or nary_3_matrix[i[0]][i[1] + 1] == 2:
                            count += 1
                        if nary_3_matrix[i[0]][i[1] - 1] == 1 or nary_3_matrix[i[0]][i[1] - 1] == 2:
                            count += 1
                        if count == 3:
                            spike_ls.append([i[0], i[1]])
        return spike_ls

    def coloring(self, nary_3_matrix, shape_ls):
        while True:
            spike_ls = self.findspike(nary_3_matrix, shape_ls)
            # color '2' to each spike
            if spike_ls:
                for i in spike_ls:
                    nary_3_matrix[i[0]][i[1]] = 2
            else:
                break
        # color the frontier
        n_heigth = len(nary_3_matrix)
        for i in range(len(nary_3_matrix[0])):
            if nary_3_matrix[0][i] == 0 and nary_3_matrix[1][i] == 2:
                nary_3_matrix[0][i] = 2
        for i in range(len(nary_3_matrix[-1])):
            if nary_3_matrix[-1][i] == 0 and nary_3_matrix[-2][i] == 2:
                nary_3_matrix[-1][i] = 2
        for i in range(n_heigth):
            if nary_3_matrix[i][0] == 0 and nary_3_matrix[i][1] == 2:
                nary_3_matrix[i][0] = 2
        for i in range(n_heigth):
            if nary_3_matrix[i][-1] == 0 and nary_3_matrix[i][-2] == 2:
                nary_3_matrix[i][-1] = 2

        return nary_3_matrix

    def count_cul_de_sacs(self, matrix):
        # create a 3*3 matrix for each element
        nary_3_matrix = self.create_nary_3_matrix(matrix, self.wall_find_way_dict)
        shape_ls, area, p = self.extending(nary_3_matrix, 0)
        n_heigth = len(nary_3_matrix)
        n_width = len(nary_3_matrix[0])
        ac_shape = []
        for a in shape_ls:
            x_ls, y_ls = zip(*a)
            if 0 in x_ls or (n_heigth - 1) in x_ls or 0 in y_ls or (n_width - 1) in y_ls:
                # if not connected to frontier, then it's inaccessible area(inner point)
                ac_shape.append(a)
        nary_3_matrix = self.coloring(nary_3_matrix, ac_shape)
        a, b, cul_num = self.extending(nary_3_matrix, 2)
        return cul_num

    def analyse(self):
        # read a txt file and analyse the maze
        matrix_ls = self.read_txt()

        # analysing the maze and print
        self.check_maze(matrix_ls)

        nary_3_matrix = self.create_nary_3_matrix(matrix_ls, self.wall_find_way_dict)
        shape_ls, area, count_1 = self.extending(nary_3_matrix, 0)  # area is useless
        nary_3_matrix = self.coloring(nary_3_matrix, shape_ls)
        self.gates = self.count_gates(matrix_ls)
        self.accesible_area, self.inner_point = self.count_accessible_inaccessible_area(matrix_ls)
        self.walls = self.count_walls(matrix_ls)
        self.entry_num = self.entry_exit_intersection(nary_3_matrix)[0]
        self.cul_de_sacs = self.count_cul_de_sacs(matrix_ls)


        # printing
        # gates
        if self.gates == 0:
            print('The maze has no gates.')
        elif self.gates == 1:
            print('The maze has a single gate.')
        else:
            print('The maze has %d gates.' % (self.gates))

        # walls
        if self.walls == 0:
            print('The maze has no wall.')
        elif self.walls == 1:
            print('The maze has walls that are all connected.')
        else:
            print('The maze has %d sets of walls that are all connected.' % (self.walls))

        # inner point
        if self.inner_point == 0:
            print('The maze has no inaccessible inner point.')
        elif self.inner_point == 1:
            print("The maze has a unique inaccessible inner point.")
        else:
            print('The maze has %d inaccessible inner points.' % (self.inner_point))

        # accesible_area
        if self.accesible_area == 0:
            print("The maze has no accessible area.")
        elif self.accesible_area == 1:
            print('The maze has a unique accessible area.')
        else:
            print('The maze has %d accessible areas.' % (self.accesible_area))

        # accessible cul-de-sacs
        if self.cul_de_sacs == 0:
            print('The maze has no accessible cul-de-sac.')
        elif self.cul_de_sacs == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print('The maze has %d sets of accessible cul-de-sacs that are all connected.' % (self.cul_de_sacs))

        # entry_exit_intersection
        if self.entry_num == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif self.entry_num == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print('The maze has %d entry-exit paths with no intersections not to cul-de-sacs.' % (
                self.entry_num))

    def display_wall(self, file, maze_map):
        # row coorodinates
        x_walls = []
        y_walls = []
        for y in range(0, len(maze_map), 3):
            # row_walls coordinates
            cur_x = 0
            start_x = 0
            for x in range(1, len(maze_map[y]), 3):
                if maze_map[y][x] == 1:
                    if cur_x == 0:
                        start_x, cur_x = x, x
                    else:
                        if cur_x + 3 == x:
                            cur_x = x
                        else:
                            y_walls.append([(start_x // 3, y // 3),
                                            (cur_x // 3, y // 3)])
                            start_x, cur_x = x, x
            if start_x > 0:
                y_walls.append([(start_x // 3, y // 3),
                                (cur_x // 3, y // 3)])

        for x in range(0, len(maze_map[0]), 3):
            # columns coordinates
            cur_y = 0
            start_y = 0
            for y in range(1, len(maze_map), 3):
                if maze_map[y][x] == 1:
                    if cur_y == 0:
                        start_y, cur_y = y, y
                    else:
                        if cur_y + 3 == y:
                            cur_y += 3
                        else:
                            x_walls.append([(x // 3, start_y // 3)
                                               , (x // 3, cur_y // 3)])
                            start_y, cur_y = y, y
            if start_y > 0:
                x_walls.append([(x // 3, start_y // 3), (x // 3, cur_y // 3)])

        # writing
        file.write('% Walls\n')
        for wall in y_walls:
            file.write('    \\draw (' + str(wall[0][0]) + ',' + str(wall[0][1]) + ') ')
            file.write('-- (' + str(wall[1][0] + 1) + ',' + str(wall[1][1]) + ');\n')
        for wall in x_walls:
            file.write('    \\draw (' + str(wall[0][0]) + ',' + str(wall[0][1]) + ') ')
            file.write('-- (' + str(wall[1][0]) + ',' + str(wall[1][1] + 1) + ');\n')

    def display_pillar(self, file, maze_map):
        # get the ls of pillars' positions first
        height = len(maze_map)
        width = len(maze_map[0])
        pillar_ls = []
        for r in range(0, len(maze_map), 3):
            for c in range(0, len(maze_map[r]), 3):
                if not maze_map[r][c]:
                    if r != 0 and c != 0 and r!= height-1 and c!= width-1:
                        diretion_ls = [maze_map[r+1][c], maze_map[r-1][c], maze_map[r][c+1], maze_map[r][c-1]]
                    elif r==0 and c != 0 and c!= width-1:
                        diretion_ls = [maze_map[r+1][c], maze_map[r][c+1], maze_map[r][c-1]]
                    elif r==height-1 and c!= 0 and c!= width-1:
                        diretion_ls = [maze_map[r-1][c], maze_map[r][c+1], maze_map[r][c-1]]
                    elif r != 0 and r != height-1 and c == 0:
                        diretion_ls = [maze_map[r-1][c], maze_map[r][c+1], maze_map[r+1][c]]
                    elif r != 0 and r != height-1 and c == width-1:
                        diretion_ls = [maze_map[r-1][c], maze_map[r][c-1], maze_map[r+1][c]]
                    elif r == 0 and c == 0:
                        diretion_ls = [maze_map[r][c+1], maze_map[r+1][c]]
                    elif r == height-1 and c == 0:
                        diretion_ls = [maze_map[r-1][c], maze_map[r][c+1]]
                    elif r == 0 and c == width-1:
                        diretion_ls = [maze_map[r+1][c], maze_map[r][c-1]]
                    elif r == height-1 and c == width-1:
                        diretion_ls = [maze_map[r-1][c], maze_map[r][c-1]]
                else:
                    continue
                if len(diretion_ls) == diretion_ls.count(0):
                    pillar_ls.append((c//3,r//3))

        # write the pos of pillar into file
        file.write('% Pillars\n')
        for point in pillar_ls:
            x, y = point
            file.write('    \\fill[green] (' + str(x)
                       + ',' + str(y) + ')')
            file.write(' circle(0.2);\n')




    def display_cul_de_sacs(self, file, maze_map):
        file.write('% Inner points in accessible cul-de-sacs\n')
        cul_de_sacs_ls = []
        for r in range(len(maze_map)):
            for c in range(len(maze_map[r])):
                if maze_map[r][c] == 2:
                    cul_de_sacs_ls.append((r, c))

        draw_ls = []
        for p in cul_de_sacs_ls:
            if p[0] % 3 == 1 and p[1] % 3 == 1:
                draw_ls.append((p[0] // 3, p[1] // 3))
        for p in draw_ls:
            file.write('    \\node at (' + str(p[1] + 0.5)
                       + ',' + str(p[0] + 0.5) + ')')
            file.write(' {};\n')

    def display_entry_exit_paths(self, file, maze_map):
        # begin
        file.write('% Entry-exit paths without intersections\n')

        # get the valid path
        path_ls = self.entry_exit_intersection(maze_map)[1]
        x_dict = defaultdict(list)
        y_dict = defaultdict(list)
        if path_ls:
            for path in path_ls:
                for x, y in path:
                    if y % 3 == 1 and x % 3 == 0:
                        y_dict[y//3].append(x//3)
                    if y % 3 == 0 and x % 3 == 1:
                        x_dict[y//3].append(x//3)
            y_path_point = []
            for key in sorted(y_dict.keys()):
                # make  a right order
                values = sorted(y_dict[key])
                for value in values:
                    y_path_point.append((key, value))
            y_path = []
            visit_ls = []
            for x, y in y_path_point:
                if (x, y) in visit_ls:
                    continue
                if (x, y+1) not in y_path_point:
                    y_path.append([(x,y), (x, y)])
                else:
                    start_y,end_y = y, y
                    while (x, end_y) in y_path_point:
                        visit_ls.append((x, end_y))
                        end_y += 1
                    end_y-= 1
                    y_path.append([(x,start_y), (x, end_y)])

            # x
            x_path_point = []
            for key in sorted(x_dict.keys()):
                # make  a right order
                values = sorted(x_dict[key])
                for value in values:
                    x_path_point.append((key, value))
            x_path =[]
            visit_ls = []
            for x, y in x_path_point:
                if (x, y) in visit_ls:
                    continue
                if (x+1, y) not in x_path_point:
                    x_path.append([(x, y), (x, y)])
                else:
                    start_x, end_x = x, x
                    while (end_x, y) in x_path_point:
                        visit_ls.append((end_x, y))
                        end_x += 1
                    end_x -= 1
                    x_path.append([(start_x, y), (end_x, y)])
            for path in x_path:
                start_x, start_y = path[0]
                end_x, end_y = path[1]
                file.write(f'    \draw[dashed, yellow] ({start_x - 0.5},{start_y + 0.5}) '
                           f'-- ({end_x + 0.5},{end_y + 0.5});\n')

            for path in y_path:
                start_x, start_y = path[0]
                end_x, end_y = path[1]
                file.write(f'    \draw[dashed, yellow] ({start_x + 0.5},{start_y - 0.5}) '
                           f'-- ({end_x + 0.5},{end_y + 0.5});\n')


    def display_prepare(self):
        matrix_ls = self.read_txt()
        matrix_ls = self.check_maze(matrix_ls)
        if matrix_ls:
            nary_3_matrix = self.create_nary_3_matrix(matrix_ls, self.wall_find_way_dict)
            count_wall_matrix = self.create_nary_3_matrix(matrix_ls, self.wall_dict_count_wall)
            shape_ls, area, p = self.extending(nary_3_matrix, 0)
            n_heigth = len(nary_3_matrix)
            n_width = len(nary_3_matrix[0])
            ac_shape = []
            for a in shape_ls:
                x_ls, y_ls = zip(*a)
                if 0 in x_ls or (n_heigth - 1) in x_ls or 0 in y_ls or (n_width - 1) in y_ls:
                    # if not connected to frontier, then it's inaccessible area(inner point)
                    ac_shape.append(a)
            nary_3_matrix = self.coloring(nary_3_matrix, ac_shape)
        else:
            return False
        return matrix_ls, nary_3_matrix,count_wall_matrix

    def display(self):
        # build a maze based on a given matrix
        # and get the large map of the maze
        matrix, nary_3_matrix,count_wall_matrix = self.display_prepare()
        file_name = self.file_name.split('.')[0] + '.tex'
        # delete file
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'w') as file:
            file.write('\\documentclass[10pt]{article}\n')
            file.write('\\usepackage{tikz}\n')
            file.write('\\usetikzlibrary{shapes.misc}\n')
            file.write('\\usepackage[margin=0cm]{geometry}\n')
            file.write('\\pagestyle{empty}\n')
            file.write('\\tikzstyle{every node}=[cross out, draw, red]\n')
            file.write('\n')
            file.write('\\begin{document}\n')
            file.write('\n')
            file.write('\\vspace*{\\fill}\n')
            file.write('\\begin{center}\n')
            file.write('\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n')

            # draw walls
            self.display_wall(file, nary_3_matrix)
            # draw pillars
            self.display_pillar(file, count_wall_matrix)
            # out inner_accessible_cul_de_sacs
            self.display_cul_de_sacs(file, nary_3_matrix)
            # exit path
            self.display_entry_exit_paths(file, nary_3_matrix)

            file.write('\\end{tikzpicture}\n')
            file.write('\\end{center}\n')
            file.write('\\vspace*{\\fill}\n')
            file.write('\n')
            file.write('\\end{document}\n')
