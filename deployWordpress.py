from kubernetes import client, config
import yaml
import sys 
import requests
import subprocess
import mysql.connector

# ip address
ip = "192.168.10.31"
# token
token = "6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg"
# home path
home_path = '/home/tommygood/telegram_bot'
# config path
config_path = "/var/snap/microk8s/current/credentials/client.config"
# kubctl path
kubectl_path = "/snap/bin/microk8s.kubectl"

config.load_kube_config(config_file=config_path)

app_name = sys.argv[1]
namespace = sys.argv[2]
replicas = sys.argv[3]

try:
    # load yaml
    with open(f"{home_path}/wp_deploy.yaml","r") as file:
        yaml_file = yaml.safe_load(file)

    yaml_file["metadata"]["name"] = app_name
    yaml_file["spec"]["selector"]["matchLabels"]["app"] = app_name
    yaml_file["spec"]["template"]["metadata"]["labels"]["app"] = app_name
    yaml_file["spec"]["replicas"] = int(replicas)

    # create deployment
    v1 = client.AppsV1Api()
    v1.create_namespaced_deployment(
        body = yaml_file,
        namespace = namespace
    )

    # 已使用的NodePort
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces().items
    used_ports = []
    for service in services:
        if service.spec.type == 'NodePort' and service.spec.ports:
            for port in service.spec.ports:
                if port.node_port is not None:
                    used_ports.append(port.node_port)

    # 找未使用的NodePort
    port = 30000
    while port <= 32767:
        if port not in used_ports:
            break
        port += 1
    if port > 32767: # port超過可用範圍
        # 刪除deployment
        command = f"{kubectl_path} delete deployment {app_name}"
        output = subprocess.check_output(command, shell=True, text=True)    
        conn = mysql.connector.connect(
            user="kenny",
            password="Kenny061256",
            host="localhost",
            port=3306,
            database="telegram_db"
        )
        cur = conn.cursor()
        sql = "delete from all_wordpress where app_name = %s;"
        cur.execute(sql,(app_name,))
        conn.commit()
        chat_id = sys.argv[4]
        message = "wordpress建置失敗，因為nodePort數量不夠！"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url)
    else:
        with open(f"{home_path}/wp_service.yaml","r") as file:
            yaml_file = yaml.safe_load(file)

        yaml_file["metadata"]["name"] = "wordpress-service"+app_name
        yaml_file["spec"]["selector"]["app"] = app_name
        yaml_file["spec"]["ports"][0]["nodePort"] = port

        # create service
        v1 = client.CoreV1Api()
        v1.create_namespaced_service(
            body=yaml_file,
            namespace = namespace
        )

        # 使用者 id
        chat_id = sys.argv[4]
        # 訊息
        message = "WordPress建置完成！\n網址為 "+ip+":"+str(port)
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url)
except:
    try:
        # 刪除deployment
        command = f"{kubectl_path} delete deployment {app_name}"
        output = subprocess.check_output(command, shell=True, text=True)
    except:
        pass
    chat_id = sys.argv[4]
    message = "WordPress建置失敗！\n請重新建置！"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)
    conn = mysql.connector.connect(
            user="kenny",
            password="Kenny061256",
            host="localhost",
            port=3306,
            database="telegram_db"
    )
    cur = conn.cursor()
    sql = "delete from all_wordpress where app_name = %s;"
    cur.execute(sql,(app_name,))
    conn.commit()
