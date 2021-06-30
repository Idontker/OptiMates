import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# making dataframe
og_df1 = pd.read_csv("..\\..\\logs\\solution_log20000_26_01.csv", sep=";")
og_df3 = pd.read_csv("..\\..\\logs\\solution_log20000_26_01_3part.csv", sep=";")
og_df9 = pd.read_csv("..\\..\\logs\\solution_log20000_26_01_9part.csv", sep=";")

df1 = og_df1[og_df1["keep"] == True]
df3 = og_df3[og_df3["keep"] == True]
df9 = og_df9[og_df9["keep"] == True]

df1 = og_df1
df3 = og_df3
df9 = og_df9



# fig = plt.figure()
# cols = 1
# rows = 3
# bins = 12

def plot_slice(df, field, ax):
    df[field].plot.hist(bins=bins,alpha=0.7,ax=ax )


fig = plt.figure()
cols = 1
rows = 3
bins = 12
size = 10

ax1 = fig.add_subplot(rows, cols, 1)
ax2 = fig.add_subplot(rows, cols, 2)
ax3 = fig.add_subplot(rows, cols, 3)

# plot_slice(df1,"fittness", ax1)
# plot_slice(df3,"fittness", ax2)
# plot_slice(df9,"fittness", ax3)
plot_slice(df1,"new coverings", ax1)
plot_slice(df3,"new coverings", ax2)
plot_slice(df9,"new coverings", ax3)

plt.show()