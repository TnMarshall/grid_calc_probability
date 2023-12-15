import pandas as pd
import matplotlib.pyplot as plt

path_to_csv= "/home/tristan/Documents/python_scripts/graph_writer/graph_10_cycles.csv"
df= pd.read_csv(path_to_csv ,index_col=0)

plt.imshow(df,cmap='hot',interpolation='nearest')

plt.show()