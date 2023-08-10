#### Reference
* https://mile.cloud/zh/resources/blog/vpc-introduction-network-setting-subnet_533
* https://mile.cloud/zh/resources/blog/vpc-network-firewall-security-setting_567

VPC，全名 Virtual Private Cloud，是雲端環境中的網路虛擬化技術，用於串接和管理在雲端部署的資源，類似於在雲端上創建一個隔離的私有網路，使資源能夠相互連接或隔離，提供安全和彈性的網路環境。在同一個 VPC 內都視為同一個內網環境，裡面的資源基本上可以透過內網 IP 來相互拜訪，可以減少延遲、增加效能，若是考慮到網路安全，還是可以透過防火牆的設計，來阻擋內網資源的互聯，有助於保護資料的隱私和安全。

基本上一個專案裡面可以包含多個 VPC
全球 VPC 概念： Google Cloud 的 VPC 是全球範圍的，這意味著它可以跨多個地理區域（Regions）運行。
VPC 範圍與區域： 在 Google Cloud 中，您在 VPC 中指定一個 IP 位址範圍，這個範圍將分佈在不同的地理區域。每個地理區域中的資源將獲得分配在該地區對應範圍內的 IP 位址。
多地區連接： 在 VPC 內的不同地理區域（Regions）之間，資源可以透過內網 IP 進行連接，所以不同 Region 內的資源，只要他們在同個 VPC Network 內，可以互相拜訪到對方。
VPC 內通信與安全性： 在同一個 VPC 內的資源可以透過內部 IP 地址進行通信，形成一個私有網路環境。但可以透過防火牆、網路存取控制等方式來限制和保護這些資源之間的通信。
資源 IP 分配： 每個地理區域內的資源將根據 VPC 中的 IP 位址範圍獲得相應的 IP 地址。這些 IP 地址是在 VPC 設定時指定的，並且在資源建立時自動分配。

* (圖一)
  * VPC 是 Global 的概念，可以包含多個 Region
  * Region 是由多個 Zone 組成的，只要在同個 Region 內，不同 Zone 內的 VM 也會領取到相同網段的 IP address
![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/66f26c91-ac57-4879-b1c6-8f56ffb6bbc5)
![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/06723e2e-f155-4e20-b9a8-cbcd2c09f6c2)


![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/9fb20e66-ad5a-481b-bd1c-a12431d44b19)
![image](https://github.com/KellenJohn/On-live_Lab/assets/29540152/40a93b42-8648-4241-a87e-da966cfaa775)


這通常需要透過外網的方式。這種跨地區的連接可以透過 VPN（虛擬私人網路）或其他網路設定實現xxxx
===

全球 GCP 內網，只要是同一個 VPC 的主機都能互通
如果不同 VPC，即使在同一個 Region 也不能互相溝通，要經過 INTERNET 了
專案一建立，會出現名為 default 的 VPC
可以建立自動模式，或自訂模式的 VPC
自動模式的 VPC 可以轉成自訂模式

每個都大概是 /20 的大小，大概是 32-20=12，2^12 = 4096，在減去 0, 1, 4095 共 3 個 IP，有 4093 個 IP，每個資料中心都會開小網段出來?
可以建立自訂 VPC 網路！

test-1 用自動
test-2 用自訂
子網路 tw
10.0.0.0/24 > IP 數量會是，32-24=8，2^8 - 3 = 253 個 IP
VM / 網路介面可以選 

原本在建立 VPC 時，系統會詢問是否要建立一些基本的 FW rules，例如 SSH(22), RDP(3389), ICMP 等，如果忽略不建，此時就要再手動建立！
fw
allow-ssh / 目標 - 所有網路中的執行個體 / 0.0.0.0/0 代表全世界所有的 IP 都可以聯線進來 / 指定的通訊埠 TCP 22 / 其他 ICMP


VPC peering
---

#### ICMP (Internet Control Message Protocol)
ICMP 是一種用於在網際網路中傳遞控制訊息的協定。它是位於網際網路通訊協定套件（TCP/IP）的第四層，即網際網路層（Internet Layer）上的一個協定。
ICMP 主要用於在網路上進行錯誤報告、診斷網路問題和提供網路的狀態訊息。它通常由網路設備如路由器和主機之間使用，並不用於直接應用程式間的通訊。ICMP 訊息一般不加密，且有時可能會被防火牆或其他網路設備過濾或阻擋。

常見的 ICMP 訊息包括：
1. Echo Request 和 Echo Reply：
  - 也稱為「Ping」。用於測試主機的可達性和往返時間。當發送 Echo Request 時，目標主機會回應 Echo Reply。
2. Destination Unreachable：
  - 當封包無法到達目的地時，目的主機會回應這個訊息，通知源主機無法傳遞該封包。
3. Time Exceeded：
  - 當 IP 封包在路由器上的 TTL (Time To Live) 達到 0 時，路由器會將此訊息回應給源主機，通知 TTL 已達到限制。
4. Redirect：
  - 當路由器希望告知源主機使用更適當的路由時，會發送 Redirect 訊息，讓源主機可以直接傳送封包到新的目標。
5. Timestamp Request 和 Timestamp Reply：
  - 用於取得時間戳記，主要用於計算網路延遲。
ICMP 是維護和管理網際網路的重要工具，它提供了一種有效地診斷網路問題和測試網路連通性的方式，是網路管理和故障排除的一部分。
---
可以在對方的 B 伺服器上使用 tcpdump 指令來監聽並捕獲從 A 伺服器發出的 Ping 請求。這樣你就可以看到有人在 Ping B 伺服器了。

以下是在 B 伺服器上使用 tcpdump 的指令：

sudo tcpdump icmp
這個指令會讓 tcpdump 監聽 ICMP 封包（Ping 封包屬於 ICMP 協定），當 B 伺服器收到來自 A 伺服器的 Ping 請求時，它會在終端機上顯示相關資訊。

如果你想要更詳細的資訊，例如打印出來的封包內容，你可以加上 -v 參數：

sudo tcpdump -v icmp
請注意，使用 tcpdump 需要 root 權限，因此你可能需要在指令前加上 sudo 以取得足夠的權限。另外，這個指令會一直在終端機上運行，直到你手動終止它，按下 Ctrl + C 即可停止 tcpdump 的監聽。

請確保在使用 tcpdump 監聽網路流量時，遵守相關法律和規範，並只在你有授權的網路上使用。

---

是的，如果你想要捕獲 HTTP Request（HTTP 請求），你需要將 tcpdump 的過濾條件設定為 HTTP 封包。

以下是在 B 伺服器上使用 tcpdump 監聽 HTTP Request 的指令：


sudo tcpdump -i <interface> -n -s 0 'tcp dst port 80'
解釋一下指令中的參數：

-i <interface>：指定要監聽的網路介面，例如 eth0。
-n：禁用 DNS 解析，顯示 IP 地址而不是主機名稱。
-s 0：捕獲完整的封包，而不是截斷為預設長度。
'tcp dst port 80'：過濾 TCP 封包，並只捕獲目的端口為 80（HTTP）的封包。
這個指令會讓 tcpdump 監聽來自 A 伺服器的 HTTP Request，並在終端機上顯示相關資訊。

同樣地，使用 tcpdump 需要 root 權限，因此你可能需要在指令前加上 sudo 以取得足夠的權限。監聽到想要的資訊後，你可以手動終止 tcpdump 的運行，按下 Ctrl + C 即可停止監聽。
請注意，監聽 HTTP Request 的封包涉及到其他使用者的敏感資訊，因此在使用 tcpdump 監聽網路流量時，務必確保在合法的範圍內進行，並遵守相關的法律和規範。


User
<interface> 我不太懂，我只是去 http request 對方的 API 而已 <interface> 要怎麼寫
ChatGPT
抱歉，我之前的回答有些混淆了。在 tcpdump 的指令中，<interface> 是用來指定要監聽的網路介面，讓 tcpdump 知道要在哪個網路接口上進行封包捕獲。

對於 HTTP Request，你可以不指定特定的網路介面，而是直接使用 tcp port 80 來捕獲目的端口為 80（HTTP）的封包。

以下是使用 tcpdump 監聽 HTTP Request 的指令：

sudo tcpdump -n -s 0 'tcp port 80'
這樣，tcpdump 將會在所有網路介面上捕獲目的端口為 80 的 TCP 封包，也就是 HTTP Request。

再次提醒，在使用 tcpdump 監聽網路流量時，要確保在合法範圍內進行，並遵守相關的法律和規範。同時，監聽 HTTP Request 的封包可能涉及到使用者的敏感資訊，請小心使用這樣的工具。如果你不確定如何使用 tcpdump，最好先咨詢網絡專業人士。
