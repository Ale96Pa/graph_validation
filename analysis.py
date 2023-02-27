import pandas as pd
import matplotlib.pyplot as plt


def performance_sat(filesat):
    df = pd.read_csv(filesat)
    marks = [".","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        # x = sat_df["nodes"].to_list()
        # y = sat_df["time"]
        sat_df_mean = sat_df.groupby(['nodes'])
        x =[5,10,25,50,100,150,250,500,1000,2000]
        y = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["time"].mean())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Performance evaluation of Metrics Computability")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    # plt.show()
    plt.savefig('plot/per_sat.png', bbox_inches='tight')
    plt.close()

def validation_sat(filesat):
    df = pd.read_csv(filesat)
    marks = [".","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        # x = sat_df["nodes"].to_list()
        # y = sat_df["results"]
        sat_df_mean = sat_df.groupby(['nodes'])
        x =[5,10,25,50,100,150,250,500,1000,2000]
        y = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["results"].mean())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Performance evaluation of Metrics Computability")
    plt.xlabel("Number of nodes")
    plt.ylabel("Output")
    plt.legend()
    # plt.show()
    plt.savefig('plot/val_sat.png', bbox_inches='tight')
    plt.close()

def performance_msc(filemsc):
    df = pd.read_csv(filemsc)
    marks = ["x","o","v","s","+","."]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        sat_df_mean = sat_df.groupby(['nodes'])
        # x = sat_df["nodes"].to_list()
        # y = sat_df["time"]
        x =range(2,30)
        y = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["time"].mean())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Performance evaluation of Instruments Redundancy")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    # plt.show()
    plt.savefig('plot/per_msc.png', bbox_inches='tight')
    plt.close()

def validation_msc(filemsc):
    df = pd.read_csv(filemsc)
    marks = ["x","o","v","s","+","."]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        # x = sat_df["nodes"].to_list()
        # y = sat_df["results"]
        sat_df_mean = sat_df.groupby(['nodes'])
        x =range(2,30)
        y = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["results"].mean())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Validation of Instruments Redundancy")
    plt.xlabel("Number of nodes")
    plt.ylabel("Number selected sets")
    plt.legend()
    # plt.show()
    plt.savefig('plot/val_msc.png', bbox_inches='tight')
    plt.close()

def performance_wsc(filewsc):
    df = pd.read_csv(filewsc)
    marks = ["x","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        # x = sat_df["nodes"].to_list()
        # y = sat_df["time"]
        sat_df_mean = sat_df.groupby(['nodes'])
        x =[5,10,25,50,100,150,250,500,1000,2000]
        y = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["time"].mean())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Performance evaluation of Cost-Bounded Constraint")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time (s)")
    plt.legend()
    # plt.show()
    plt.savefig('plot/per_wsc.png', bbox_inches='tight')
    plt.close()

def validation_wsc(filewsc):
    df = pd.read_csv(filewsc)
    marks = ["x","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        # x = sat_df["nodes"].to_list()
        # y = sat_df["result_w"]
        sat_df_mean = sat_df.groupby(['nodes'])
        x =[2000,2005,2010,2020,2030,2050,2060,2100,2150]
        y = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["result_w"].mean())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Validation of Cost-Bounded Constraint")
    plt.xlabel("Number of nodes")
    plt.ylabel("Cost")
    plt.legend()
    # plt.show()
    plt.savefig('plot/val_wsc.png', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    filesat = 'result/sat.csv'
    filemsc = "result/msc.csv"
    filewsc = "result/wsc.csv"
    filewsc2 = "result/wsc2.csv"
    performance_sat(filesat)
    validation_sat(filesat)

    performance_msc(filemsc)
    validation_msc(filemsc)

    performance_wsc(filewsc)
    validation_wsc(filewsc2)