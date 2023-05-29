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

然而，我們認為除了上述的方法，若是可以直接使用 telegram 和 k8s cluster 溝通（包含查詢 k8s cluster 狀態、主動發送警告給管理員）會有幾個優點 : 
  1. 使用者體驗會更好，因為包含查詢 k8s cluster 狀態、telegram 發送警告，都可以直接藉由 telegram 聊天室傳達。
  2. 相對使用監控工具來說比較可以客製化要觀察的以及信件的內容。

<br/>
<h2>Prerequisite</h2>

1. k8s cluster

2. <a href = "https://github.com/tommygood/K8s-Telegram-Bot/tree/master/microk8s/prometheus">prometheus server</a>

3. exporter
      - <a href = "https://github.com/tommygood/K8s-Telegram-Bot/blob/master/kube-state-metrics">kube-state-metrics</a>
      - <a href = "https://github.com/tommygood/K8s-Telegram-Bot/tree/master/microk8s/node_exporter"> node exporter</a>
      - cAdvisor
         - 不同 k8s 環境，設定會不同，通常預設會直接開在 node 上的 10250 or 10255 port，可以檢查看看。
         - ex. `curl https://localhost:10250/metrics`

4. <a href = "https://github.com/nalbury/promql-cli">promql-cli</a> 
 
5. crontab

<h2>Installation</h2>

1. `git clone https://github.com/tommygood/K8s-Telegram-Bot.git`
2. 依據不同的 exporter pod 的 ip, port 調整 <a href = "https://github.com/tommygood/K8s-Telegram-Bot/blob/master/microk8s/prometheus/prometheus-cm.yaml">prometheus server 的設定</a> : `- targets: ['exporter_ip:port']`
3. 把 script 的 variable 改為自己的設定
   - 3.1 `query.py` 
      - home_path : current dir
      - token : your telegram bot token
   - 3.2 `call_prom.py`
      - home_path : current dir
      - host : address of prometheus server
   - 3.3 all script in `monitor`
      - token : your telegram bot token
      - chat_id : id of telegram chat room
         - send a message to bot in telegram
         - get `https://api.telegram.org/bot{Your_Token}/getUpdates` : change {Your_Token} to your telegram bot token
         - and will get a json, the `id` in field `chat` is the chat_id

<h2>Usage</h2>

- start `Query` function with python daemon : `python3 query.py`
- start `Monitor` function with crontab : 
   - `crontab -e`
   
      ```conf
      */1 * * * * python3 /path/to/telegram_bot/monitor/podCreate.py

      */60 * * * * python3 /path/to/telegram_bot/monitor/weirdPod.py
      ```
<h2>功能介紹</h2>
<h3>查詢</h3>
目前有 8 種查詢的種類 : 程式碼都在

`call_prom.py`，不同功能用不同 function 區分。
<br/>
1. `podMemUseInNode`
    - 介紹
        - node 上部屬的全部的 pod 所佔 node 的 memory 的百分比
    - 理由
        - 因為如果 node 上的 memory 空間不夠，可能造成 pod eviction。
        - 所以當 node 空間不夠，可以透過嘗試刪減 pod 來獲取 memory，而此功能就可以讓使用者較直觀的觀察 pod 和 node 的 memory 關係。
    - 輸出範例
        - ![](https://hackmd.io/_uploads/SyxlkaRYHh.png)

2. `eachConatinerMemUsage`
    - 介紹
        - 各個 container 佔用了多少其限制的 memory 的百分比
    - 理由
        - 如果 container 佔用的 memory 百分比太高，可能會影響使用者體驗，此時管理者可以考慮多開幾個 replica
    - 輸出範例
        - ![](https://hackmd.io/_uploads/Bk_3eycSh.png)
        - 會顯示是哪一個 pod
     
 3.  `weirdPodNumInNamespace`
     - 介紹
        - 各個 namespace 不正常 pod 的數量
      - 理由
        - 當有 pod 的狀態不正常，k8s 會嘗試重啟 pod，可能會成功或失敗。 
        - 可以觀察不同時間段各個 namespace 有多少不正常運作的 pod，再去找出造成 pod 不正常的真正原因，避免再次發生。
      - 輸出範例
        - ![](https://hackmd.io/_uploads/ry1_7J5H2.png)
        - 會顯示是哪一個 namespace

4. `runningPodNumInNamespace`
    - 介紹
        - 各個 namespace 不同時間有多少 pod 同時執行
    - 理由
        - 有時 pod 可能因為 auto scaling 而自動被建立或刪除，所以管理員可以藉由掌握不同時間段的 pod 數量，進而得知資源被使用的情形（ex. 哪些 pod 比較常被使用），再去判斷此 pod 是否需要轉移到資源較好的 node 上部屬會較穩定。
            - auto scaling : k8s 可以有偵測到 pod 的資源若超過一定的使用上限時就會增加 pod 的 replica，藉以讓 pod 正常運作，因為有更多資源可以分配
    - 輸出範例
        - ![](https://hackmd.io/_uploads/Hkk0m1qH3.png)
        - 會顯示是哪一個 namespace

5. `nodeMemSecTotal` 
    - 介紹
        - k8s cluster 中的所有 node 的各別已使用的 memory 的百分比
    - 理由
        - 當 node 的 memory 不夠時，如果還繼續在此 node 上部屬 pod，可能會造成 pod eviction。
    - 輸出範例
        - ![](https://hackmd.io/_uploads/BkviPk5Sh.png) 
        - 可以藉由 instance(node metric) ip 區別是哪一台 node

6. `nodeCpuSecTotal`
    - 介紹
        - k8s cluster 中所有 node 的各別已使用的 cpu 的百分比
    - 理由
        - 當 node 的 cpu 使用量過高，可能造成系統的速度變得非常慢，或是 pod eviction。
        - 當 cpu 使用量過高，可以用不同決策解決（ex. 把一些高 cpu 使用量的 pod 移到別台 node、更改 auto scaling 的設定）
    - 輸出範例
        - ![](https://hackmd.io/_uploads/rJkRuy5Hh.png)
        - 可以藉由 instance(node metric) ip 區別是哪一台 node

7. `conatinerCpuPerSecTotal`
    - 介紹
        - k8s cluster 中<b>所有</b>的 container 正在使用的<b>所有</b> node 的 cpu 的百分比
    - 理由
        - 藉由觀察 cluster 內全部的 container 使用的 cpu 百分比，可以決定是否要不要再此 k8s cluster 新增 or 刪除 node 數量來達到資源最有效的運用
    - 輸出範例
        - ![](https://hackmd.io/_uploads/SJF8h1cSh.png)

8. `conatinerPerCpuUsage`
    - 介紹
        - 不同 container 使用了多少其限制的 cpu 的百分比
    - 理由
        - 藉由觀察單個 container 的 cpu 使用率，可以去決定是否要把此 container 的 cpu request 調整，讓全部 container 能使用的 cpu 資源最大化。
    - 輸出範例
        - ![](https://hackmd.io/_uploads/ByB9RJcr3.png)

<h3>自動監測通報</h3>
目前會依照 2 種不同的情況去監測，程式碼都在

`monitor` file 當中，要再設定 crontab 要多久執行一次。

1. `weirdPod.py`
    - 介紹
      - 監測是否有狀態不正常的 pod，我設定一小時執行一次。
    - 理由
      - pod 可能因為某些原因(ex. eviction)造成其狀態不正常，無法正常執行。
      - 所以需要檢查 k8s cluster 內是否有不正常運作的 pod，並印出 pod 資訊和造成原因
          - ![](https://hackmd.io/_uploads/Bk_cwAYSn.png)
      - 因為可能需要一些時間排錯，所以不用短時間一直重複檢查
    - 輸出範例
        - ![](https://hackmd.io/_uploads/Sy23PRFr2.png)

2. `podCreate.py`
    - 介紹
      - 監測是否有新的 pod 被建立，我設定每一分鐘偵測一次
    - 理由
      - 藉由得到哪些 pod 被建立的資訊，管理員可以更掌握 cluster 的資訊(ex. pod 建立超過一定量是否會讓 node 資源不夠)
    - 輸出範例
        - ![](https://hackmd.io/_uploads/H1w45RKHh.png)

<h3>資料庫</h3>
   
   - schema
      ![image](https://github.com/tommygood/K8s-Telegram-Bot/assets/104426729/103d577c-4f7c-4733-8c2c-be4869beebb7)
   - all_user 記錄使用者資訊
      - uid 使用者的 telegram id
      - name 使用者的 telegram 名稱
      - permission 使用者權限 (1~3,1(最大)可管理全部 namespace,3(最小))
   - all_namespace 記錄使用者可使用哪些 namespace
      - id 流水號
      - uid 使用者的 telegram id
      - name namespace 的名稱
   - all_command 記錄指令資訊
      - name 指令名稱
      - content 指令說明
      - permission 指令權限

<h3>telegram_bot</h3>
   
   - 使用說明
      - 所有指令最前面都要加"/"
      - 輸入 /au 註冊後才可使用所有功能
      - 輸入 /gu 可以查看自己的使用者資訊(id,名稱,權限)
      - 輸入 /ac 可以查看自己的權限可使用的指令
<h2>分工</h2>

- 王冠權 : k8s
- 黃瑜楓 : telegram bot
