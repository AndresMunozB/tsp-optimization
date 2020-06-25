import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from docplex.mp.model import Model
import docplex.mp.solution as sol

data = np.loadtxt('data/wi29.tsp.txt')
n = data.shape[0] # NUMERO DE CIUDADES
cities = [i for i in range(n)]
arcos =[(i,j) for i in cities for j in cities if i!=j]

coord_x = data[:, 1] # Primera columna 
coord_y = data[:, 2] # Segunda columna

distancia={(i, j): np.hypot(coord_x[i] - coord_x[j], coord_y[i] - coord_y[j]) for i,j in arcos}
x=coord_x
y=coord_y

# Creando el modelo en Cplex
mdl=Model('TSP')

#Declaramos las variables a utilizar
#los nombre y forma de llamar las variables es propia de CPLEX.

x=mdl.binary_var_dict(arcos,name='x')
d=mdl.continuous_var_dict(cities,name='d')

mdl.minimize(mdl.sum(distancia[i]*x[i] for i in arcos))

for c in cities:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if i==c)==1, 
                       ctname='out_%d'%c)

for c in cities:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if j==c)==1, 
                       ctname='in_%d'%c)

for i,j in arcos:
    if j!=0:
        mdl.add_indicator(x[(i,j)],d[i]+1==d[j], 
                          name='order_(%d,_%d)'%(i, j))

mdl.parameters.timelimit=150
mdl.parameters.mip.strategy.branch=1
mdl.parameters.mip.tolerances.mipgap=0.15

solucion = mdl.solve(log_output=True)

mdl.get_solve_status()
solucion.display()