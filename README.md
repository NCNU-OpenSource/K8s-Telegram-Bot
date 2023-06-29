# K8s-Telegram-Bot
<h2>Background</h2>
在管理 k8s cluster 的時候，若是沒有使用監控的工具（ex. prometheus），就往往會需要進去 manager node 用 kubectl 下指令去觀察，比如說

`kubectl describe pod pod_name`
，便可以得到 pod 目前的一大堆資訊（ex. status），
管理員就必須再去從這一大包資訊中找出自己需要的。
<br/>
但是用這種方式有幾個缺點 : 
   1. 使用上較麻煩 : 若管理員只是想要簡單的檢查一下 k8s cluster 的資源（ex. cpu）使用情況，還要先進去 manager node 裡面下 kubectl 的指令。
   2. 不方便觀察 : 因為是全文字輸出在終端機上，所以要快速地觀察和比較資訊的變化會非常困難。
   3. 沒有通報功能 : 若 k8s cluster 出現了一些變化（ex. 有 pod 因某些原因掛掉了），k8s cluster 沒有辦法及時的通知管理員。
<br/>
為了解決上述幾種缺點，於是就有了監控工具（ex. prometheus）的產生，它通常會在 node 上開一個 port 架設網頁，並藉由在 k8s cluster 內執行的 exporter 所產出的 metrics 來分析資料並做視覺化，管理員就可以藉由存取這個網頁來觀察 k8s cluster 狀態。
<br/>
除此之外，它也有當發生異常狀況就寄送 e-mail 給管理員的功能。

<br/>
<br/>

然而，我們認為除了上述的方法監控 k8s，若是可以直接使用 telegram 和 k8s cluster 溝通（包含查詢 k8s cluster 狀態、主動發送警告給管理員）會有幾個優點 : 
  1. 使用者體驗會更好，因為包含查詢 k8s cluster 狀態、telegram 發送警告，都可以直接藉由 telegram 聊天室傳達。
  2. 相對使用監控工具來說比較可以客製化要觀察的以及信件的內容。

除了監控的功能以外，若有需要常常在 k8s 中部署一些常用的系統（ex. wordpress），如果可以直接藉由 telegtam 快速地在 k8s 上部署也會很方便。

<h2>Introduction</h2>

總結我們這個系統，可以在 telegram 聊天室輸入簡單的命令做到以下功能 ：
   1. 監控 k8s cluster 狀態（主動查看、被動通知）。
       ![image](https://github.com/tommygood/K8s-Telegram-Bot/assets/104426729/402f5b63-6e0e-4d3b-bbca-4b82b5bb68e3)

   2. 快速部署 container 在 k8s 上（我們以 wordpress 作為範例）。
       ![image](https://github.com/tommygood/K8s-Telegram-Bot/assets/104426729/6ab5a0f7-e77e-4727-9eb5-3221923985c8)

<h2>Prerequisite</h2>

1. k8s cluster
   - ex. microk8s
      - install microk8s
         - `snap install microk8s --classic`
      - my microk8s version
         - `MicroK8s v1.26.5 revision 5395`
2. crontab
3. python3
4. mysql/mariadb

<h2>Installation</h2>

1. `git clone https://github.com/tommygood/K8s-Telegram-Bot.git`
2. install the python plugins will be used
   - `pip3 install python-telegram-bot python-daemon mysql-connector matplotlib`
3. exporter
      1. <a href = "https://github.com/kubernetes/kube-state-metrics">kube-state-metrics</a>
         - export the <b>all</b> metrics of k8s cluster
            - include the pod numbers, status and abnoraml reasons...
         - install
            - `cd microk8s/kube-state-metrics` 
            - `kubectl apply -f .`
      2. <a href = "https://github.com/bibinwilson/kubernetes-node-exporter">node exporter</a>
         - export the metrics of <b>each</b> node
            - include memory, cpu and storage status
         - install
            - `cd microk8s/node_exporter`
            - `kubectl apply -f .`
      3. cAdvisor
         - export the metrics of containers on <b>each</b> node
            - include the usage of resource on containers
         - install
            - 不同 k8s 環境，設定會不同，通常預設會直接開在 node 上的 10250 or 10255 port
            - `curl https://localhost:10250/metrics`
         - note : 需要去 cluster 中<b>每一個</b> node 檢查
4. <a href = "https://github.com/tommygood/K8s-Telegram-Bot/tree/master/microk8s/prometheus">prometheus server</a>
   - install
      - `cd microk8s/prometheus`
      - `kubectl apply -f .`
5. <a href = "https://github.com/nalbury/promql-cli">promql-cli</a> 
   - install
      - `wget https://github.com/nalbury/promql-cli/releases/download/v0.3.0/promql-v0.3.0-darwin-amd64.tar.gz`
         - view the latest version first

<h2>Configuration</h2>

1. 依據不同的 <b>exporter</b> 的 <b>ip</b>, <b>port</b> 調整 <a href = "https://github.com/tommygood/K8s-Telegram-Bot/blob/master/microk8s/prometheus/prometheus-cm.yaml">prometheus server 的設定</a>，新增或編輯在 `scrape_configs:` 下：
   ```
   - job_name: 'exporter_name'
      static_configs: 
      - targets: ['exporter_ip:exporter_port']
   ```

2. 把 script 的 variable 改為自己的設定
   - 2.1 `query.py` 
      - home_path : current dir
         - `pwd`
      - token : your telegram bot token
   - 2.2 `call_prom.py`
      - home_path : current dir
      - host : address of prometheus server
         - `kubectl get service --all-namespaces | grep prometheus`
   - 2.3 `deployWordpress.py`
      - ip : address of your host
      - token : your telegram bot token
      - home_path : current dir
      - config_path : path of k8s client.config (default path of microk8s installed by snap is `/var/snap/microk8s/current/credentials/client.config`)
      - kubctl_path : path of kubectl
         - `whereis kubectl`
   - 2.4 `monitor/podCreate.py`
      - token : your telegram bot token  
   - 2.5 `monitor/weirdPod.py`
      - token : your telegram bot token
      - kubectl_path : path of kubectl
   - 2.6 `dbConfig.py`
      - user : user name
      - password : user's password
      - host : ip address of host
      - port : port of mysql/mariadb
      - database : db be used

3. dump `schema.sql` into database
   - `mysql -u root -p telegram_db < schema.sql`

<h2>Usage</h2>

- start `Query` function with python daemon : `python3 query.py`
- start `Monitor` function with crontab : 
   - `crontab -e`
   
      ```conf
      */1 * * * * python3 /path/to/telegram_bot/monitor/podCreate.py >> /path/to/telegram_bot/log/crontab.log

      */60 * * * * python3 /path/to/telegram_bot/monitor/weirdPod.py >> /path/to/telegram_bot/log/crontab.log
      ```
<h2>功能介紹</h2>
<h3>查詢</h3>

目前有 8 種查詢的種類 : 在 `call_prom.py`，不同功能用不同 function 區分。
<br/>
<br/>
使用情境:
   
   ![](https://hackmd.io/_uploads/H1c3lrvv3.png)

1. `nodeMemSecTotal` 
    - 介紹
        - k8s cluster 中的所有 node 的各別可<b>被使用</b>的 memory 的百分比
    - 理由
        - 當 node 的 memory 不夠時，如果還繼續在此 node 上部屬 pod，可能會造成 pod eviction。
            - pod eviction : 當 k8s cluster 中的 node 資源不夠時，pod 會被從此 node 中移除。
        - 此時可以考慮多新增幾台 node 到 k8s cluster 中，或是降低 replica 的數量等方式解決。
    - 輸出範例
        - ![](https://hackmd.io/_uploads/BkviPk5Sh.png) 
        - 可以藉由 instance(node metric) ip 區別是哪一台 node

2. `podMemUseInNode`
    - 介紹
        - 各個 node 上部屬的全部的 pod 所 request 的 memory 和 node 的 memory 的百分比
    - 理由
        - 因為 node 上除了 k8s 相關的物件，還會有別的程式佔掉記憶體，而此功能就可以讓使用者較直觀的觀察 pod 和 node 的 memory 關係。
    - 輸出範例
        - ![](https://hackmd.io/_uploads/SyxlkaRYHh.png)

3. `eachConatinerMemUsage`
    - 介紹
        - 各個 container 佔用了多少其限制的 memory 的百分比
    - 理由
        - 如果 container 佔用的 memory 百分比太高，可能是特殊狀況（被植入挖礦軟體），或是單純該應用程式就會佔用較多的 memory，此時管理者可以因應狀況處理。
        - 如果 container 佔用的 memory 百分比太低，可以考慮把其 request 的 memory 降低以節省空間。
    - 輸出範例
        - ![](https://hackmd.io/_uploads/Bk_3eycSh.png)
        - 會顯示是哪一個 pod

4. `nodeCpuSecTotal`
    - 介紹
        - k8s cluster 中所有 node 的各別已使用的 cpu 的百分比
    - 理由
        - 當 node 的 cpu 使用量過高，可能造成系統的速度變得非常慢，或是 pod eviction。
        - 當 cpu 使用量過高，可以用不同方式解決（ex. 把一些高 cpu 使用量的 pod 移到別台 node）
    - 輸出範例
        - ![](https://hackmd.io/_uploads/rJkRuy5Hh.png)
        - 可以藉由 instance(node metric) ip 區別是哪一台 node

5. `conatinerCpuPerSecTotal`
    - 介紹
        - k8s cluster 中<b>所有</b>的 container 正在使用的<b>所有</b> node 的 cpu 的百分比
    - 理由
        - 藉由觀察 cluster 內全部的 container 使用的 cpu 百分比，可以決定是否要不要再此 k8s cluster 新增 or 刪除 node 數量來達到資源最有效的運用
    - 輸出範例
        - ![image](https://github.com/tommygood/K8s-Telegram-Bot/assets/96759292/b799532d-2a0b-4d6a-ad54-3b0ed1c099bd)
  
 6. `conatinerPerCpuUsage`
    - 介紹
        - 不同 container 使用了多少其限制的 cpu 的百分比
    - 理由
        - 藉由觀察單個 container 的 cpu 使用率，可以去決定是否要把此 container 的 cpu request 調整，讓全部 container 能使用的 cpu 資源最大化。
    - 輸出範例
        - ![](https://hackmd.io/_uploads/ByB9RJcr3.png)
 
 7. `runningPodNumInNamespace`
    - 介紹
        - 各個 namespace 不同時間有多少 pod 同時執行
    - 理由
        - 有時 pod 可能因為 auto scaling 而自動被建立或刪除，所以管理員可以藉由掌握不同時間段的 pod 數量，進而得知資源被使用的情形（ex. 哪些 pod 比較常被使用），再去判斷此 pod 是否需要轉移到資源較好的 node 上部屬會較穩定。
            - auto scaling : k8s 可以有偵測到 pod 的資源若超過一定的使用上限時就會增加 pod 的 replica，藉以讓 pod 正常運作，因為有更多資源可以分配
    - 輸出範例
        - ![](https://hackmd.io/_uploads/Hkk0m1qH3.png)
        - 會顯示是哪一個 namespace
 
 8.  `weirdPodNumInNamespace`
     - 介紹
        - 各個 namespace 不正常 pod 的數量
      - 理由
        - 當有 pod 的狀態不正常，k8s 會嘗試重啟 pod，可能會成功或失敗。 
        - 可以觀察不同時間段各個 namespace 有多少不正常運作的 pod，再去找出造成 pod 不正常的真正原因（ex. namespace 限制的資源不夠），避免再次發生。
      - 輸出範例
        - ![](https://hackmd.io/_uploads/ry1_7J5H2.png)
        - 會顯示是哪一個 namespace

<h3>自動監測通報</h3>

目前會依照 2 種不同的情況去監測，在 `monitor` file 當中，要再設定 crontab 要多久執行一次。

1. `weirdPod.py`
    - 介紹
      - 監測是否有狀態不正常的 pod，我設定一小時執行一次。
    - 理由
      - pod 可能因為某些原因（ex. eviction）造成其狀態不正常，無法正常執行。
      - 所以需要檢查 k8s cluster 內是否有不正常運作的 pod，並印出該 pod <b>資訊</b>和造成其<b>不正常的原因</b>。
          - ![](https://hackmd.io/_uploads/Bk_cwAYSn.png)
      - 因為可能需要一些時間排錯，所以不用短時間一直重複檢查
    - 輸出範例
        - ![](https://hackmd.io/_uploads/Sy23PRFr2.png)

2. `podCreate.py`
    - 介紹
      - 監測是否有新的 pod 被建立，我設定每一分鐘偵測一次
    - 理由
      - 藉由得到哪些 pod 被建立的資訊，管理員可以更掌握 cluster 的資訊（ex. pod 建立超過一定量是否會讓 node 資源不夠）
    - 輸出範例
        - ![](https://hackmd.io/_uploads/H1w45RKHh.png)

<h3>部署 WordPress</h3>

- 介紹
   - 程式碼在`deployWordpress.py`
   - 當使用者透過 telegam bot 依序輸入 deployment 的 App name, namespace 的名稱, replicas 的數量後會呼叫`deployWordpress.py`進行部署
   - `deployWordpress.py`包含建立 deployment 和 service
      - deployment
         - 讀取`wp_deploy.yaml`，把 App name, namespace, replicas 改成使用者傳給 telegram bot 的資訊
            - `wp_deploy.yaml` : 包含 WordPress container 的設定
      - service
         - 讀取`wp_service.yaml`，找出未被使用的 nodePort 設為 service 的 nodePort
            - `wp_service.yaml` : 用 nodePort type 的 service 綁定剛剛建立的 deployment 的 pod
   - 部署 WordPress，完成後會回傳 WordPress 的網址

- 使用說明
   - 必須按照步驟依序輸入 deployment 的 App Name, namepsace 的名稱, replicas 數量
   - 如果部署過程中要取消或重新部屬，可以輸入 `/clear` 清除記錄
   - 部署步驟<br>
      I. `/cw` 開始部署 WordPress<br>
      II. `/app App名稱` 輸入 deployment 的 App name<br>
      III. `/ns namespace名稱` WordPress 要建在哪個 namespace 下<br>
      IV. `/rs replicas數量` deployment 的 replicas 數量(1~3)<br>
      V. 部署完成<br>
   ![](https://hackmd.io/_uploads/BkdJZHPPh.png)

<h3>資料庫</h3>
   
   - schema
      ![](https://hackmd.io/_uploads/rynEbHvw3.png)
   
   - table
      - `all_user` : 記錄使用者資訊
         - `uid` : 使用者的 telegram id
         - `name` : 使用者的 telegram 名稱
         - `permission` : 使用者權限（1 ~ 3）
            - 1 : 可管理 cluster 內全部的 namespace
            - 2 : 依照 table `all_namespace`，區分可以管理哪些 namespace
            - 3 : 無權限
      
      - `all_namespace` : 記錄使用者可使用哪些 namespace
         - `id` : 流水號
         - `uid` : 使用者的 telegram id
         - `name` : namespace 的名稱
      
      - `all_command` : 記錄指令資訊
         - `name` : 指令名稱
         - `content` : 指令說明
         - `permission` : 指令權限
      
      - `all_wordpress` : 記錄建立的 WordPress 資訊
         - `id` : 流水號
         - `uid` : 使用者的 telegram id
         - `app_name` : deployment 的 App name
         - `namespace` : namespace 的名稱
         - `replicas` : replicas 的數量
       
       - `k8s_namespace` : 記錄 k8s cluster 中所有的 namespace
         - `id` : 流水號
         - `namespace` : namespace 的名稱

<h3>telegram_bot</h3>
   
   - 使用說明
      - 所有指令最前面都要加 `/`
      - 一開始要先輸入 `/au` 註冊後才可使用所有功能，使用者預設權限是3（最小）
      - 輸入 `/gu` 可以查看自己的使用者資訊（id,名稱,權限）
      - 輸入 `/ac` 可以查看自己的權限可使用的指令與說明
      ![](https://hackmd.io/_uploads/HJcuZHww3.jpg)

<h2>Job Assignment</h2>

- 王冠權：架設 k8s、k8s 監控和自動通報
- 黃瑜楓：部署 WordPress on k8s、telegram-bot

<h2>Reference</h2>

- https://github.com/kubernetes/kube-state-metrics
- https://github.com/bibinwilson/kubernetes-node-exporter
- https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md
- https://ithelp.ithome.com.tw/articles/10248278
- https://gist.github.com/max-rocket-internet/6a05ee757b6587668a1de8a5c177728b
- https://sysdig.com/blog/prometheus-query-examples/
