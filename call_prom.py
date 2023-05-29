from subprocess import call, PIPE, run, os
import json, datetime, argparse
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", required = True, help = " : metric type") # get metric type
ap.add_argument("-n", "--namespace", required = False, help = " : specify namespace") # specify namespace
args = vars(ap.parse_args())

# prometheus server
host = 'http://localhost:31111'

# metric type
metric_type = args['type']

# namespace
def getNamespace(namespace) :
    if namespace == None or namespace == '' :
        return ''
    else :
        return f"namespace='{namespace}'"
namespace = getNamespace(args['namespace'])

# time range
interval = "5h"

# total metric type
total_metric_type = ['podMemUseInNode', 'eachConatinerMemUsage', 'weirdPodNumInNamespace', 'runningPodNumInNamespace', 'nodeMemSecTotal', 'nodeCpuSecTotal', 'containerCpuPerSecTotal', 'conatinerPerCpuUsage', 'namespacePerPodCpuUsage']

# home_path 
home_path = '/home/tommygood/telegram_bot'



def main() :
    # check metric available
    if not checkRightMetric() :
        print('this metric is not available !')
        return
    # search with prometheus
    result = eval(metric_type + "()")

    # draw the graph, and output to a png
    #print(result.stdout)
    output_len = 0 # count the length of output png

    # output each result with a png
    for i in range(len(eval(result.stdout))) :
        # data value
        data = eval(result.stdout)[i]['values']
        # data metric infomation
        data_metric = list(eval(result.stdout)[i]['metric'].items())
        # draw the graph with value and infomation
        plot_graph(data, f'{home_path}/image/output{i}.png', metric_type, data_metric)
        output_len += 1
    # final quantity of data
    print(f'Successfully output, total num of output is :{output_len}')

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
def containerCpuPerSecTotal() :
    # execute command
    #command = 'sum (rate (container_cpu_usage_seconds_total[1m]))'
    #command = 'sum (rate (container_cpu_usage_seconds_total{image!=""}[1m]))'
    # percertange
    command = 'sum (rate (container_cpu_usage_seconds_total{id="/"}[1m])) / sum (machine_cpu_cores) * 100'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# each container cpu usage percentage
def conatinerPerCpuUsage() :
    # execute command
    #command = 'sum(irate(container_cpu_usage_seconds_total[5m])*100)by(pod)'
    #command = 'sum (rate (container_cpu_usage_seconds_total{image!=""}[5m])) by (pod)'
    command = f'sum(rate(container_cpu_usage_seconds_total{{image!="",{namespace}}}[5m])) by (pod, container, namespace) / sum(container_spec_cpu_quota{{image!="", {namespace}}}/container_spec_cpu_period{{image!="", {namespace}}}) by (pod, container, namespace) * 100'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# the cpu usage percentage of per container in each namespace
def namespacePerPodCpuUsage() :
    # execute command
    #command = 'sum(rate(container_cpu_usage_seconds_total{image!="", namespace ="%s"}[5m])) by (pod, container) / sum(container_spec_cpu_quota{image!="", namespace = "%s"}/container_spec_cpu_period{image!="", namespace = "%s"}) by (pod, container)'
    command = 'sum(rate(container_cpu_usage_seconds_total{image!="", namespace ="%s"}[5m]))/ sum(container_spec_cpu_quota{image!="", namespace = "%s"}/container_spec_cpu_period{image!="", namespace = "%s"}) /  count(kube_pod_status_phase{phase="Running", namespace= "%s"})' % (namespace, namespace, namespace, namespace)
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# node available memory percent
def nodeMemSecTotal() :
    # execute command
    command = '(node_memory_MemFree_bytes+node_memory_Buffers_bytes+node_memory_Cached_bytes ) / node_memory_MemTotal_bytes * 100'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# number of running pod in each namespace
def runningPodNumInNamespace() :
    # execute command
    command = f'sum(kube_pod_container_status_running{{{namespace}}}) by (namespace)'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# number of weird status pod in each namespace
def weirdPodNumInNamespace() :
    # execute command
    command = f"sum by (namespace) (kube_pod_status_ready{{condition='false', {namespace}}})"
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# the memory usage percent of each container
def eachConatinerMemUsage() :
    # execute command
    command = f'sum (container_memory_working_set_bytes{{{namespace}}}) by (container_name , pod) / (sum (container_spec_memory_limit_bytes{{{namespace}}}>0 ) by (container_name, pod)) * 100'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result

# the percent of pod memory use on the node deploying it 
def podMemUseInNode() :
    # execute command
    command = 'sum(kube_pod_container_resource_limits{resource="memory"}) / sum(kube_node_status_capacity{resource="memory"}) * 100'
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
    plt.ylabel("Percentage")
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
