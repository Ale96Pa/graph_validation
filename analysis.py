import pandas as pd
import matplotlib.pyplot as plt
import os
from generate_synthetic import test,testmsc,testwsc,topologies

def performance_sat(filesat, outimg):
    df = pd.read_csv(filesat)
    marks = [".","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
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
        label = sat_df["name"].to_list()[0]
        if sat_df["name"].to_list()[0] == "path_gen": label = "path_existence"
        plt.plot(x, y, label = label, marker=marks[i])
        plt.fill_between(x, mins, maxs, alpha=.5)
        i+=1
    
    plt.title("Performance evaluation of Metrics Computability")
    plt.xlabel("Number of metrics")
    plt.ylabel("Time (s)")
    plt.legend()
    # plt.show()
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

def validation_sat(filesat, outimg):
    df = pd.read_csv(filesat)
    marks = [".","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
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
        plt.plot(x, y, label = sat_df["name"].to_list()[0], marker=marks[i+1])
        plt.plot(x, y, label = "path_existence", marker=marks[i])
        plt.fill_between(x, mins, maxs, alpha=.5)
        i+=1
        break
    
    plt.title("Validation of Metrics Computability")
    plt.xlabel("Number of metrics")
    plt.ylabel("Output")
    plt.legend()
    # plt.show()
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

def performance_msc(filemsc, outimg):
    df = pd.read_csv(filemsc)
    marks = ["x","o","v","s","+","."]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
        sat_df_mean = sat_df.groupby(['nodes'])
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
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

def validation_msc(filemsc, outimg):
    df = pd.read_csv(filemsc)
    marks = ["x","o","v","s","+","."]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
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
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

def performance_wsc(filewsc, outimg="plot/per_wsc.png"):
    df = pd.read_csv(filewsc)
    marks = ["x","o","v","s","+","x"]
    df_grouped = df.groupby(['name'])
    i=0
    for group, item in df_grouped:
        sat_df = df_grouped.get_group(group)
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
    names = df["name"].to_list()[0:2] #names = ["MMG", "SoA heuristic"]
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
        if names[0] == "MMG":
            delta = name1mean[j]-name2mean[j]
            mins_delta = name1min[j]-name2min[j]
            maxs_delta = name1max[j]-name2max[j]
        else:
            delta = name2mean[j]-name1mean[j]
            mins_delta = name2min[j]-name1min[j]
            maxs_delta = name2max[j]-name1max[j]
        y.append(delta)
        mins.append(mins_delta)
        maxs.append(maxs_delta)

    plt.plot(x, y, label = ["cost(MMG)-cost(heuristic)"], marker=marks[i])
    # plt.fill_between(x, mins, maxs, alpha=.5)
    i+=1

    plt.title("Validation of Cost-Bounded Constraint")
    plt.xlabel("Number of metrics")
    plt.ylabel("Cost")
    plt.legend()
    # plt.show()
    plt.savefig(outimg, bbox_inches='tight')
    plt.close()

def benchmark_topology(topology):
    filesat = "result/topology_"+topology+"/sat.csv"
    filemsc = "result/topology_"+topology+"/msc.csv"
    filewsc = "result/topology_"+topology+"/wsc.csv"
    # filewsc2 = "result/topology_"+topology+"/wsc_cut.csv"
    outimg = "plot/topology_"+topology+"/per_sat.png"
    performance_sat(filesat, outimg)
    outimg = "plot/topology_"+topology+"/val_sat.png"
    validation_sat(filesat, outimg)

    # outimg = "plot/topology_"+topology+"/per_msc.png"
    # performance_msc(filemsc, outimg)
    # outimg = "plot/topology_"+topology+"/val_msc.png"
    # validation_msc(filemsc, outimg)

    # outimg = "plot/topology_"+topology+"/per_wsc.png"
    # performance_wsc(filewsc, outimg)
    # outimg = "plot/topology_"+topology+"/val_wsc.png"
    # validation_wsc(filewsc, outimg, True)
    # outimg = "plot/topology_"+topology+"/delta_val_wsc.png"
    # validation_delta_wsc(filewsc,outimg,True)

#    # outimg = "plot/topology_"+topology+"/val_wsc_cut.png"
#    # validation_wsc(filewsc2, outimg, False)
#    # outimg = "plot/topology_"+topology+"/delta_val_wsc_cut.png"
#    # validation_delta_wsc(filewsc2,outimg,False)

    # ## Cost distribution
    # root_plot = "plot/topology_"+topology+"/cost_distribution/"
    # root_result = "result/topology_"+topology+"/cost_distribution/"
    # for file in os.listdir("result/topology_"+topology+"/cost_distribution"):
    #     outimg = root_plot+"val_"+file.split(".")[0]+".png"
    #     infile = root_result+file
    #     if "cut" in file:
    #         validation_wsc(infile, outimg, False)
    #     else:
    #         validation_wsc(infile, outimg, True)
    #     outimg = root_plot+"delta_val_"+file.split(".")[0]+".png"
    #     if "cut" in file:
    #         validation_delta_wsc(infile, outimg, False)
    #     else:
    #         validation_delta_wsc(infile, outimg, True)


if __name__ == "__main__":
    for topology in topologies:
        benchmark_topology(topology)