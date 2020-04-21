import numpy as np
import pyxel

SIZE = 128

pyxel.init(SIZE, SIZE, fps=10)

cell_matrix = (
    np.zeros((SIZE, SIZE)),
    np.zeros((SIZE, SIZE))
)
counter = 0

cell_matrix[0][4, 1] = 1
cell_matrix[0][5, 2] = 1
cell_matrix[0][3, 3] = 1
cell_matrix[0][4, 3] = 1
cell_matrix[0][5, 3] = 1

cell_matrix[0][24, 3] = 1
cell_matrix[0][24, 4] = 1
cell_matrix[0][24, 5] = 1


def check_cell(matrix, x: int, y: int) -> bool:

    current_value = matrix[x, y]
    count = matrix[(x-1) % SIZE,    (y-1) % SIZE] + \
        matrix[(x) % SIZE,      (y - 1) % SIZE] + \
        matrix[(x + 1) % SIZE,  (y - 1) % SIZE] + \
        matrix[(x - 1) % SIZE,  (y) % SIZE] + \
        matrix[(x + 1) % SIZE,  (y) % SIZE] + \
        matrix[(x - 1) % SIZE,  (y + 1) % SIZE] + \
        matrix[(x) % SIZE,      (y + 1) % SIZE] + \
        matrix[(x+1) % SIZE,    (y+1) % SIZE]
    if not current_value:
        return count == 3
    else:
        return 1 < count < 4


def update():
    global cell_matrix
    global counter
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    current_matrix = cell_matrix[counter % 2]
    counter += 1
    next_matrix = cell_matrix[counter % 2]

    for y in range(0, SIZE):
        for x in range(0, SIZE):
            next_matrix[x, y] = check_cell(current_matrix, x, y)


def upd():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    pyxel.cls(0)
    global cell_matrix
    global counter
    current_matrix = cell_matrix[counter % 2]
    for y in range(0, SIZE):
        for x in range(0, SIZE):
            pyxel.pset(x, y, 1 if current_matrix[x, y] else 0)


pyxel.run(update, draw)
