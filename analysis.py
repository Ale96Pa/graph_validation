import pandas as pd
import matplotlib.pyplot as plt
import os
from generate_synthetic import test,testmsc,testwsc


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
        x = test
        y = []
        mins = []
        maxs = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["time"].mean())
            mins.append(subsat_df["time"].min())
            maxs.append(subsat_df["time"].max())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        plt.fill_between(x, mins, maxs, alpha=.5)
        i+=1
    
    plt.title("Performance evaluation of Metrics Computability")
    plt.xlabel("Number of metrics")
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
        x = test
        y = []
        mins = []
        maxs = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["results"].mean())
            mins.append(subsat_df["time"].min())
            maxs.append(subsat_df["time"].max())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        plt.fill_between(x, mins, maxs, alpha=.5)
        i+=1
    
    plt.title("Performance evaluation of Metrics Computability")
    plt.xlabel("Number of metrics")
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
        x = testmsc
        y = []
        mins = []
        maxs = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["time"].mean())
            mins.append(subsat_df["time"].min())
            maxs.append(subsat_df["time"].max())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        plt.fill_between(x, mins, maxs, alpha=.5)
        i+=1
    
    plt.title("Performance evaluation of Instruments Redundancy")
    plt.xlabel("Number of metrics")
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
        x = testmsc
        y = []
        mins = []
        maxs = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["results"].mean())
            mins.append(subsat_df["results"].min())
            maxs.append(subsat_df["results"].max())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        i+=1
    
    plt.title("Validation of Instruments Redundancy")
    plt.xlabel("Number of metrics")
    plt.ylabel("Number selected sets")
    plt.legend()
    # plt.show()
    plt.savefig('plot/val_msc.png', bbox_inches='tight')
    plt.close()

def performance_wsc(filewsc, outimg="plot/per_wsc.png"):
    df = pd.read_csv(filewsc)
    marks = ["x","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        # x = sat_df["nodes"].to_list()
        # y = sat_df["time"]
        sat_df_mean = sat_df.groupby(['nodes'])
        x = test
        y = []
        mins = []
        maxs = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["time"].mean())
            mins.append(subsat_df["time"].min())
            maxs.append(subsat_df["time"].max())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        plt.fill_between(x, mins, maxs, alpha=.5)
        i+=1
    
    plt.title("Performance evaluation of Cost-Bounded Constraint")
    plt.xlabel("Number of metrics")
    plt.ylabel("Time (s)")
    plt.legend()
    # plt.show()
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

def validation_wsc(filewsc, outimg, isEntire):
    df = pd.read_csv(filewsc)
    marks = ["x","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        # x = sat_df["nodes"].to_list()
        # y = sat_df["result_w"]
        sat_df_mean = sat_df.groupby(['nodes'])
        if isEntire: x = test
        else: x = testwsc
        y = []
        mins = []
        maxs = []
        for subgroup, subitme in sat_df_mean:
            subsat_df = sat_df_mean.get_group(subgroup)
            y.append(subsat_df["result_w"].mean())
            mins.append(subsat_df["result_w"].min())
            maxs.append(subsat_df["result_w"].max())
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
        plt.fill_between(x, mins, maxs, alpha=.5)
        i+=1
    
    plt.title("Validation of Cost-Bounded Constraint")
    plt.xlabel("Number of metrics")
    plt.ylabel("Cost")
    plt.legend()
    # plt.show()
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

def validation_delta_wsc(filewsc, outimg, isEntire):
    df = pd.read_csv(filewsc)
    marks = ["x","o","v","s","+","x"]
    names = ["MMG", "SoA heuristic"] #todo prenderli dinamici
    df_grouped = df.groupby(['nodes'])
    i=0
    dic_mean = {new_list: [] for new_list in names}
    dic_min = {new_list: [] for new_list in names}
    dic_max = {new_list: [] for new_list in names}
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        for name in names:
            sat_df_mean = sat_df.query("name == '"+name+"'")["result_w"]

            dic_mean[name].append(sat_df_mean.mean())
            dic_min[name].append(sat_df_mean.min())
            dic_max[name].append(sat_df_mean.max())
        
        
    if isEntire: x = test
    else: x = testwsc
    y = []
    mins = []
    maxs = []
    name1mean = dic_mean[names[0]]
    name2mean = dic_mean[names[1]]
    name1min = dic_min[names[0]]
    name2min = dic_min[names[1]]
    name1max = dic_max[names[0]]
    name2max = dic_max[names[1]]
    for j in range(0,len(name1mean)):
        delta = name1mean[j]-name2mean[j]
        mins_delta = name1min[j]-name2min[j]
        maxs_delta = name1max[j]-name2max[j]
        y.append(delta)
        mins.append(mins_delta)
        maxs.append(maxs_delta)

    plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i])
    plt.fill_between(x, mins, maxs, alpha=.5)
    i+=1

    plt.title("Validation of Cost-Bounded Constraint")
    plt.xlabel("Number of metrics")
    plt.ylabel("Cost")
    plt.legend()
    # plt.show()
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    filesat = 'result/sat.csv'
    filemsc = "result/msc.csv"
    filewsc = "result/wsc.csv"
    filewsc2 = "result/wsc_cut.csv"
    performance_sat(filesat)
    validation_sat(filesat)

    performance_msc(filemsc)
    validation_msc(filemsc)

    performance_wsc(filewsc)
    outimg = "plot/val_wsc.png"
    validation_wsc(filewsc, outimg, True)
    outimg = "plot/delta_val_wsc.png"
    validation_delta_wsc(filewsc,outimg,True)
    
    outimg = "plot/val_wsc_cut.png"
    validation_wsc(filewsc2, outimg, False)
    outimg = "plot/delta_val_wsc_cut.png"
    validation_delta_wsc(filewsc2,outimg,False)

    ## Cost distribution
    root_plot = "plot/cost_distribution/"
    root_result = "result/cost_distribution/"
    for file in os.listdir("result/cost_distribution"):
        outimg = root_plot+"val_"+file.split(".")[0]+".png"
        infile = root_result+file
        if "cut" in file:
            validation_wsc(infile, outimg, False)
        else:
            validation_wsc(infile, outimg, True)
        outimg = root_plot+"delta_val_"+file.split(".")[0]+".png"
        if "cut" in file:
            validation_delta_wsc(infile, outimg, False)
        else:
            validation_delta_wsc(infile, outimg, True)