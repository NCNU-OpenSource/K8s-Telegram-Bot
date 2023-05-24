# monitor whether have pod is not running
import datetime, requests, subprocess
from subprocess import call, PIPE, run

# prometheus server
host = "http://localhost:31111"
# time range
interval = "1h"

# total metric type
total_metric_type = ['podMemUseInNode', 'eachConatinerMemUsage', 'weirdPodNumInNamespace', 'runningPodNumInNamespace', 'nodeMemSecTotal', 'nodeCpuSecTotal', 'conatinerCpuPerSecTotal', 'conatinerPerCpuUsage', 'namespacePerPodCpuUsage']

# bot token
token = "6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg"
# chat id
chat_id="1697361994"
# message
message = ''
# api url
url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"

def main() :
    # status is not normal pod
    podWeird()

# send msg to telegram
def sendMsg(mark) :
    message = "Pod Not Running Event !" + "\n\n" + mark + '\n'
    #print(message)
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    res = requests.get(url) # this sends the message

def podWeird() :
    # set time limit to check whether is a new pod with minute
    time_limit = 800
    # time format, discard the microsecond. example : '2023-05-22 14:18:19'
    now_time = str(datetime.datetime.now()).split('.')[0]
    # convert string to datetime type
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    # execute command
    command = 'sum by (namespace, pod) (kube_pod_status_ready{condition="false"}) > 0'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for i in range(len(eval(result.stdout))) :
        #print(result.stdout)
        try :
            # data value
            data = eval(result.stdout)[i]['values']
            # bug prevent
            if len(data) == 1 :
                data = data[0]
            else :
                data = data[1]
            # data metric
            data_metric = list(eval(result.stdout)[i]['metric'].items())
            # mark of data
            mark = ""
            for i in range(len(data_metric)) :
                is_pod = False
                # the reason of not running
                reason = ''
                # get all data metric
                for j in range(len(data_metric[i])) :
                    mark += data_metric[i][j] + " : "
                    # is pod name, describe the reason of not running
                    if is_pod :
                        reason = searchWeirdReason(data_metric[i][j])
                    # pod name = next field after pod
                    if data_metric[i][j] == 'pod' :
                        is_pod = True
                # remove the colon in sentence bottom
                mark = removeMarkLast(mark)
                mark += "\n" + reason
            # send msg to telegram
            sendMsg(mark)
        except Exception as e:
            print(e)

# search the reason why pod is not running
def searchWeirdReason(pod) :
    # execute command, the path of microk8s must be absolute path
    command = f"/snap/bin/microk8s kubectl describe pods {pod} | grep Reason"
    output = subprocess.check_output(command, shell=True, text=True)
    reason = output.split('\n')[0]
    # replace the space
    return reason.replace(" ", "") + '\n'

# search the reason why pod is not running
def searchWeirdReason1(pod) :
    # execute command
    command = "kube_pod_status_reason{pod='" + pod + "'}"
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for i in range(len(eval(result.stdout))) :
        try :
            data = eval(result.stdout)[i]['values']
            if len(data) == 1 :
                data = data[0]
            else :
                data = data[1]
            data_metric = list(eval(result.stdout)[i]['metric'].items())
            for each_data_metric in data_metric :
                if each_data_metric[0] == 'reason' :
                    print(each_data_metric[1])
        except :
            print('error')

# remove the colon in sentence bottom
def removeMarkLast(mark) :
    new_mark = ''
    for i in mark[:-2] :
        new_mark += i
    return new_mark

main()
