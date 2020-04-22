import numpy as np
from numpy.fft import fft2, ifft2
import pyxel

SIZE = 256

pyxel.init(SIZE, SIZE, fps=40)

# Basta una matriz en esta implementación
cell_matrix = np.zeros((SIZE, SIZE))

cell_matrix[4, 1] = 1
cell_matrix[5, 2] = 1
cell_matrix[3, 3] = 1
cell_matrix[4, 3] = 1
cell_matrix[5, 3] = 1

cell_matrix[24, 3] = 1
cell_matrix[24, 4] = 1
cell_matrix[24, 5] = 1

def fft_convolve2d(matriz,kernel):
    """
    Hace convolución usando fft (no entiendo cómo, pero entiendo qué)

    Convoluciona con el "kernel" dado toda la matriz

    El kernel es otra matriz que se va deslizando "centrándola" en cada elemento
    de la matriz original (haciendo warping). Entonces se multiplican los valores
    de ambas matrices, lo que genera otra matriz, se suman todos los elementos
    de la segunda matriz y así se tiene un valor-resultado para la nueva matriz.
    A medida que el kernel se va "deslizando", se van generando todos los 
    valors-resultado de la nueva matriz

    Si se usa un kernel que sea todo ceros, excepto un trocito en el centro así:

       1 1 1
       1 0 1
       1 1 1

    El resultado será otra matriz en la que cada celda contiene ahora el número
    de vecinos que tenía la celda original.
    """
    fr = fft2(matriz)
    fr2 = fft2(np.flipud(np.fliplr(kernel)))
    m,n = fr.shape
    cc = np.real(ifft2(fr*fr2))
    cc = np.roll(cc, - int(m / 2) + 1, axis=0)
    cc = np.roll(cc, - int(n / 2) + 1, axis=1)
    return cc

def fft_conway(state, k=None):
    """
    Recibe como parámetro la matriz-universo y el kernel a usar
    (diferentes kernels podrían dar diferentes autómatas celulares)
    """
    # Si no recibimos kernel, usamos el apropiado para Life, todo ceros
    # excepto una pequeña región de 3x3 en el centro que tiene unos alrededor de un cero
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m//2-1 : m//2+2, n//2-1 : n//2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # Usamos la fft para hacer la convolución
    b = fft_convolve2d(state,k).round()
    # Ahora b contiene en cada celda el número de vecinos vivos

    # Usamos esa información para crear la matriz c con la siguiente generación
    c = np.zeros(b.shape)
    c[np.where((b == 2) & (state == 1))] = 1
    c[np.where((b == 3) & (state == 1))] = 1
    c[np.where((b == 3) & (state == 0))] = 1

    return c


def update():
    global cell_matrix
    upd()
    cell_matrix = fft_conway(cell_matrix)


def upd():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    pyxel.cls(0)
    for y in range(0, SIZE):
        for x in range(0, SIZE):
            if cell_matrix[x, y]:    # Pequeña optimización. No pintar celdas vacías
                pyxel.pset(x, y, 1)

pyxel.run(update, draw)
