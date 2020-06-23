import numpy as np
from scipy.spatial import distance

def distanceMatrix(filename):

    data = np.loadtxt(filename)
    matrix = np.zeros(shape=(len(data),len(data)))
    for row in data:
        for row2 in data:
            a = row[1:3]
            b = row2[1:3]
            matrix[int(row[0])-1, int(row2[0])-1] = distance.euclidean(a, b)        
    return matrix


def main():
    filename = "/wi29.tsp.txt"
    matrix = distanceMatrix("data/" + filename)
    np.savetxt("distance/" + filename, matrix, delimiter=" ")



if __name__ == "__main__":
    main()