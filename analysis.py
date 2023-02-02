import pandas as pd
import matplotlib.pyplot as plt


def performance_sat(filesat):
    df = pd.read_csv(filesat)
    marks = [".","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        x = sat_df["nodes"].to_list()
        y = sat_df["time"]
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.xlabel("Number of nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    filesat = 'sat.csv'
    performance_sat(filesat)