import datetime, requests
from subprocess import call, PIPE, run
from dbConfig import conn,cur

# prometheus server
host = "http://localhost:31111"
# time range
interval = "5h"

# total metric type
total_metric_type = ['podMemUseInNode', 'eachConatinerMemUsage', 'weirdPodNumInNamespace', 'runningPodNumInNamespace', 'nodeMemSecTotal', 'nodeCpuSecTotal', 'conatinerCpuPerSecTotal', 'conatinerPerCpuUsage', 'namespacePerPodCpuUsage']

# bot token
token = "6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg"
# chat id
#chat_id="1697361994"
# message
message = ''
# api url
#url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"

def main() :
    # pod create event
    podCreate()

def podCreate() :
    # set time limit to check whether is a new pod with minute
    time_limit = 1
    # time format, discard the microsecond. example : '2023-05-22 14:18:19'
    now_time = str(datetime.datetime.now()).split('.')[0]
    # convert string to datetime type
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    # execute command
    command = 'kube_pod_created{namespace="default"}'
    result = run(["promql", "--host", host, command, "--start", interval, "--output", "json"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for i in range(len(eval(result.stdout))) :
        #print(result.stdout)
        try :
            data = eval(result.stdout)[i]['values']
            if len(data) == 1 :
                data = data[0]
            else :
                data = data[1]
            data_metric = list(eval(result.stdout)[i]['metric'].items())
            mark = ""
            for i in range(len(data_metric)) :
                for j in range(len(data_metric[i])) :
                    mark += data_metric[i][j] + " : "
                mark = removeMarkLast(mark)
                mark += '\n'
            #print(data[1], mark)
            # pod create timestamp, ex. 1684716734 (second)
            pod_create_timestamp = int(data[1])
            pod_create_time = datetime.datetime.fromtimestamp(pod_create_timestamp)
            # time_interval = from pod create time to now
            time_interval = now_time - pod_create_time
            # convert to minutes
            time_interval_min = time_interval.total_seconds() / 60
            #print(time_interval_min, mark)
            if float(time_limit) > time_interval_min :
                message = "New Pod Event !" + "\n" + mark + "\n" + 'Pod create time : ' + str(pod_create_time)
                #print(message)
                sql = "select * from all_user where permission=1;"
                cur.execute(sql,())
                record = cur.fetchall()
                print(record)
                for i in range(len(record)):
                    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={record[i][0]}&text={message}"
                    res = requests.get(url) # this sends the message
                #print(res.text)
        except :
            data_metric = list(eval(result.stdout)[i]['metric'].items())
            #print(eval(result.stdout)[i]['values'], data_metric)

def removeMarkLast(mark) :
    new_mark = ''
    for i in mark[:-2] :
        new_mark += i
    return new_mark

main()
