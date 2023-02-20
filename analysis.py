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
    
    plt.title("Performance evaluation of Metrics Computability")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()

def performance_msc(filemsc):
    df = pd.read_csv(filemsc)
    marks = ["x","o","v","s","+","."]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        x = sat_df["nodes"].to_list()
        y = sat_df["time"]
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Performance evaluation of Instruments Redundancy")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()

def validation_msc(filemsc):
    df = pd.read_csv(filemsc)
    marks = ["x","o","v","s","+","."]
    # df_grouped = df.groupby(['name'])
    # i=0
    # for group, item in df_grouped:
    #     sat_df = df_grouped.get_group(group)
    #     x = sat_df["nodes"].to_list()
    #     y = sat_df["time"]
    #     plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
    #     i+=1
    
    # plt.title("Performance evaluation of Instruments Redundancy")
    # plt.xlabel("Number of nodes")
    # plt.ylabel("Time (s)")
    # plt.legend()
    # plt.show()

def performance_wsc(filewsc):
    df = pd.read_csv(filewsc)
    marks = ["x","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        x = sat_df["nodes"].to_list()
        y = sat_df["time"]
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Performance evaluation of Cost-Bounded Constraint")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()

def validation_wsc(filewsc):
    df = pd.read_csv(filewsc).tail(8)
    marks = ["x","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        x = sat_df["nodes"].to_list()
        y = sat_df["result_w"]
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Validation of Cost-Bounded Constraint")
    plt.xlabel("Number of nodes")
    plt.ylabel("Cost")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    filesat = 'sat.csv'
    filemsc = "msc.csv"
    filewsc = "wsc.csv"
    performance_sat(filesat)

    performance_msc(filemsc)

    performance_wsc(filewsc)
    validation_wsc(filewsc)