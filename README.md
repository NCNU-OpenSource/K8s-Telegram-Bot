# K8s-Telegram-Bot
<h1>Background</h1>
在管理 k8s cluster 的時候，若是沒有使用監控的工具（ex. prometheus），就往往會需要進去 manager node 用 kubectl 下指令去觀察，比如說 `kubectl describe pod pod_name`，便可以得到 pod 目前的一大堆資訊（ex. status），
管理員就必須再去從這一大包資訊中找出自己需要的。
<br/>
但是用這種方式有幾個缺點 : 
<br/>
1. 使用上較麻煩 : 若管理員只是想要簡單的檢查一下 k8s cluster 的資源（ex. cpu）使用情況，還要先進去 manager node 裡面下 kubectl 的指令。
<br/>
2. 不方便觀察 : 因為是全文字輸出在終端機上，所以要快速地觀察和比較資訊的變化會非常困難。
<br/>
3. 沒有通報功能 : 若 k8s cluster 出現了一些變化（ex. 有 pod 因某些原因掛掉了），k8s cluster 沒有辦法及時的通知管理員。
<br/>
<br/>
為了解決上述幾種缺點，於是就有了監控工具（ex. prometheus）的產生，它通常會在 node 上開一個 port 架設網頁，並藉由在 k8s cluster 內執行的 exporter 所產出的 metrics 來分析資料並做視覺化，管理員就可以藉由存取這個網頁來觀察 k8s cluster 狀態。
<br/>
除此之外，它也有當發生異常狀況就寄送 e-mail 給管理員的功能。

<br/>
<br/>
然而，我們認為除了上述的方法，若是可以直接使用 telegram 和 k8s cluster 溝通會有幾個優點 :
<br/>
1. 使用者體驗會更好，因為包含查詢 k8s cluster 狀態、telegram 發送警告，都可以直接藉由 telegram 聊天室傳達。
<br/>
2. 相對使用監控工具來說比較可以客製化要觀察的以及信件的內容。

<h1>Installation</h1>

<h1>Usage</h1>


