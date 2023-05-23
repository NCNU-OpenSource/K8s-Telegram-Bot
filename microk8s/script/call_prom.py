from subprocess import call, PIPE, run
import cairo, json, datetime, argparse
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", required = True, help = " : metric type") # get metric type
ap.add_argument("-n", "--namespace", required = False, help = " : specify namespace") # specify namespace
args = vars(ap.parse_args())
# metric type
metric_type = args['type']

# namespace
namespace = args['namespace']

# prometheus server
host = "http://localhost:31111"
# time range
interval = "1h"

# total metric type
total_metric_type = ['nodeCpuSecTotal', 'conatinerCpuPerSecTotal', 'conatinerPerCpuUsage', 'namespacePerPodCpuUsage']

def main() :
    #result = nodeCpuSecTotal()
    #result = conatinerCpuPerSecTotal()
    #result = conatinerPerCpuUsage()
    #result = namespacePerPodCpuUsage()
    # check metric available
    if not checkRightMetric() :
        print('this metric is not available !')
        return
    result = eval(metric_type + "()")
    # draw the graph, and output to a png
    #print(result.stdout)
    for i in range(len(eval(result.stdout))) :
        data = eval(result.stdout)[i]['values']
        data_metric = list(eval(result.stdout)[i]['metric'].items())
        plot_graph(data, f'output{i}.png', metric_type, data_metric)

# check metric available
def checkRightMetric() :
    for i in total_metric_type :
        if i == metric_type :
            return True
    return False

# node exporter - node cpu
def nodeCpuSecTotal() :
    # execute command
    command = '100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# kube-state exporter 

# total container cpu usage percentage
def conatinerCpuPerSecTotal() :
    # execute command
    #command = 'sum (rate (container_cpu_usage_seconds_total[1m]))'
    command = 'sum (rate (container_cpu_usage_seconds_total{image!=""}[1m]))'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# each container cpu usage percentage
def conatinerPerCpuUsage() :
    # execute command
    #command = 'sum(irate(container_cpu_usage_seconds_total[5m])*100)by(pod)'
    #command = 'sum (rate (container_cpu_usage_seconds_total{image!=""}[5m])) by (pod)'
    command = 'sum(rate(container_cpu_usage_seconds_total{image!=""}[5m])) by (pod, container) / sum(container_spec_cpu_quota{image!=""}/container_spec_cpu_period{image!=""}) by (pod, container)'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# the cpu usage percentage of per container in each namespace
def namespacePerPodCpuUsage() :
    # execute command
    #command = 'sum(rate(container_cpu_usage_seconds_total{image!="", namespace ="%s"}[5m])) by (pod, container) / sum(container_spec_cpu_quota{image!="", namespace = "%s"}/container_spec_cpu_period{image!="", namespace = "%s"}) by (pod, container)'
    command = 'sum(rate(container_cpu_usage_seconds_total{image!="", namespace ="%s"}[5m]))/ sum(container_spec_cpu_quota{image!="", namespace = "%s"}/container_spec_cpu_period{image!="", namespace = "%s"}) /  count(kube_pod_status_phase{phase="Running", namespace= "%s"})' % (namespace, namespace, namespace, namespace)
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# draw the graph
def plot_graph(data, filename, graph_type, data_metric):
    timestamps = [str(datetime.datetime.fromtimestamp(d[0]))[11:-3] for d in data]
    values = [float(d[1]) for d in data]
    # start monitor  time, end monitor time
    start_time = str(datetime.datetime.fromtimestamp(data[0][0]))[:-7]
    end_time = str(datetime.datetime.fromtimestamp(data[len(data)-1][0]))[:-7]

    # put metric info in mark
    mark = ""
    for i in range(len(data_metric)) :
        for j in range(len(data_metric[i])) :
            mark += data_metric[i][j] + " - "
        mark = removeMarkLast(mark)
        mark += "\n"
    #plt.text(4.5, 1.5, mark, fontsize=30, color='red', wrap=True)
    fig, ax = plt.subplots()
    plt.text(0, -0.15, mark, ha='left', wrap=True, transform=ax.transAxes)

    # put metric into graph
    plt.plot(timestamps, values)
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    # put metric type on title
    plt.title(graph_type + "\n" + f"{start_time} - {end_time}")
    # disable x-axis : time
    plt.xticks([])
    
    # Save the graph as a PNG file
    plt.savefig(filename)  
    plt.clf()

def removeMarkLast(mark) :
    new_mark = ''
    for i in mark[:-2] :
        new_mark += i
    return new_mark

main()
