import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# making dataframe
# og_df1 = pd.read_csv("..\\..\\logs\\solution_log20000_26_01_9part.csv", sep=";")
# og_df2 = pd.read_csv("..\\..\\logs\\solution_log20000_26_01.csv", sep=";")
# og_df = pd.read_csv("..\\..\\logs\\solution_log20000_26_01_9part.csv", sep=";")
# og_df = pd.read_csv("..\\..\\logs\\solution_log20000_26_01.csv", sep=";")
og_df = pd.read_csv("..\\..\\logs\\solution_log20000_26_01_3part.csv", sep=";")


# fig = plt.figure()
# ax = fig.add_subplot(2, 1, 1)
# og_df1.plot.scatter(x="new coverings", y="covered intersection", ax=ax, c="red", s=10)
# ax = fig.add_subplot(2, 1, 2)
# og_df2.plot.scatter(x="new coverings", y="covered intersection", ax=ax, c="blue", s=10)

# plt.show()

# exit()

tmp = og_df[og_df["keep"] == True]

print(tmp[["new coverings", "covered intersection", "mid"]].describe())
color = {
    0: "red",
    1: "blue",
    2: "green",
    3: "pink",
    4: "LimeGreen",
    5: "DarkCyan",
    6: "Violet",
    7: "SkyBlue",
    8: "DarkRed",
}
og_df["color"] = og_df.apply(lambda row: color[row.slice], axis=1)


def plot_slice(slice, i, rows, cols):
    df = og_df[og_df["slice"] == slice]
    i = i + 1

    ax = fig.add_subplot(rows, cols, i)
    df.plot(x="slice_i", y="new coverings", ax=ax, color=df["color"])

    ax = fig.add_subplot(rows, cols, i + cols)
    df.plot.scatter(x="z", y="new coverings", ax=ax, color=df["color"])

    # ax = fig.add_subplot(rows, cols, i + 2 * cols)
    # df.plot.scatter(x="slice_i", y="z", ax=ax)

    ax = fig.add_subplot(rows, cols, i + 2 * cols)
    df.plot(x="slice_i", y="z", ax=ax, color=df["color"])

    pass


fig = plt.figure()
cols = 3
rows = 5
size = 10

# for i in range(3):
#     plot_slice(2 - i, i, rows, cols)

df = og_df
lens = {}
sum = 0

lens[0] = 0
for i in range(1, 9):
    sum = sum + df[df["slice"] == i - 1].shape[0]
    lens[i] = sum
df["i"] = df.apply(lambda row: lens[row.slice] + row.slice_i, axis=1)


df = df[df["keep"] == True]

ax = fig.add_subplot(rows, 1, 1)
df.plot.scatter(x="i", y="z", ax=ax, color=df["color"], s=size)

ax = fig.add_subplot(rows, 1, 2)
df.plot.scatter(x="i", y="new coverings", ax=ax, color=df["color"], s=size)

ax = fig.add_subplot(rows, 1, 3)
df.plot.scatter(x="i", y="covered intersection", ax=ax, color=df["color"], s=size)

# df_keep = df[df["keep"] == True]
df_del = og_df[og_df["keep"] == False]

ax = fig.add_subplot(rows, 1, 4)
# df_keep.plot.scatter(x="z", y="new coverings", ax=ax, color=df_keep["color"], s=size)
df.plot.scatter(x="z", y="new coverings", ax=ax, color=df["color"], s=size)

ax = fig.add_subplot(rows, 1, 5)
df_del.plot.scatter(x="z", y="new coverings", xlim=[-1,1], ax=ax, color=df_del["color"], s=size)


plt.show()

# #####
# # 0 #
# #####
# df = og_df[og_df["slice"] == 0]
# ax = fig.add_subplot(rows, cols, 1)
# df.plot(x="slice_i", y="new coverings", ax=ax)
# ax = fig.add_subplot(rows, cols, 1 + cols)
# df.plot.scatter(x="z", y="new coverings", ax=ax)


# #####
# # 1 #
# #####
# df = og_df[og_df["slice"] == 1]
# ax = fig.add_subplot(rows, cols, 2)
# df.plot(x="slice_i", y="new coverings", ax=ax)

# ax = fig.add_subplot(rows, cols, 2 + cols)
# df.plot.scatter(x="z", y="new coverings", ax=ax)

# #####
# # 2 #
# #####
# df = og_df[og_df["slice"] == 2]
# ax = fig.add_subplot(rows, cols, 3)
# df.plot(x="slice_i", y="new coverings", ax=ax)

# ax = fig.add_subplot(rows, cols, 3 + cols)
# df.plot.scatter(x="z", y="new coverings", ax=ax)
