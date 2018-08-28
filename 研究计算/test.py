import matplotlib.pyplot as plt 
import numpy as np
import matplotlib

from WellDataPlot.plotdata import plot_experiment_resault

plot_experiment_resault("実験/23.4mm石実験データ.csv","$23.4\ mm$ Rock Experiment")
plt.show()
plot_experiment_resault("実験/9.2mm大理石実験データ.csv","$9.2\ mm$ Rock Experiment")
plt.show()