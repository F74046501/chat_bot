# 爽一個 R_ni bot

## prerequirement
 - python3
 - telegram
 - network
 - ngrok (如果使用本機作為伺服器)

## setup
    pip3 install -r requirement.txt(這是我所使用的網頁爬蟲功能所需要的安裝)

## purpose
1. 純粹只是個有趣好玩的bot
2. bot可以提供一位帥哥圖 統一發票的對獎資訊 以及ptt表特板的快速瀏覽資訊
3. 表特板的快速瀏覽資訊分成三種方式(1)看看全部的冰淇淋(2)來一球冰淇淋就好(3)來張照片上車囉

## finite state machine
![]img/show-fsm.png
在前兩個state裡，我希望能讓使用者有叫貼近的感覺，所以叫他們輸入名字
真正的開始做聊天機器人的工作是在第二個state之後，也就是initial state的位置，該位置延伸出三個大功能(下方有詳述)，其中一個功能還有延伸的三個小功能(下方亦有詳述)

## usage
主要有三大功能:
1. **帥哥圖**
Bonus:"bot傳送圖片給user"
我把圖片檔放在TOC-Project-2017/img專案資料夾裡的，當使用者呼叫此功能就會上傳圖片
2. **發票查詢**
這個功能是一個寫死的傳送字串功能，使用完後，會回到可選擇功能列表的state
3. **表特板爬蟲**
Bonus:"網頁爬蟲" & "透過超連結show出圖片"
這個大功能有三個小功能：
    (1)可以show出表特板最新板上的'所有資訊'讓使用者自行選擇並且點擊瀏覽
    (2)隨機選取'一條表特新聞'讓使用者可以瀏覽
    (3)隨機爬到其中一個表特新聞的'圖片連結'，傳送給使用者，透過超連結預覽，可以更有效率的快速觀看正妹

### how to use
1. state: user
    - input: hi
        - response: 
            會跳到intro state
            輸入hi 之後就會啟動這個bot !!!
            bot做自我介紹
            --->你好 飢餓時就找我\n我是爽一個R_ni\n首先 what's your name
            並且也詢問使用者的名字

2. state: intro
    - input: 任意的非空字串
        - response:
            會跳到username state
            bot以神秘的方式 描述自己的功能供user選擇
            讓user在不太確定功能是怎樣的情況下執行 十分有趣
            --->好的! 飢餓的你\n這邊有幾件事情我可以幫你做\n(a)看了爽翻天\n(b)餓了就該選這個\n(c)真的餓了就選這個\n


3. state: ability
    - input: a
        - response:
            會跳到teacher state
            回傳一張圖片給使用者 並且自動跳回username state 讓使用者再繼續做功能選擇

    - input: b
        - response:
            會跳到ability state
            有三種功能給使用者選擇 會回傳爬蟲的資訊給使用者（上方有介紹）
            --->餓了就來眼睛吃吃冰淇淋\n(1)看看全部的冰淇淋\n(2)來一球冰淇淋就好\n(3)來張照片上車囉
            同樣地，做完後會自動跳回username state 讓使用者再繼續做功能選擇

    - input: c
        - response:
            會跳到money state
            傳送對獎發票資訊給使用者 並且自動跳回username state 讓使用者再繼續做功能選擇

