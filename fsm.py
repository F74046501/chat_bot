from transitions.extensions import GraphMachine
from random import *

import requests
from bs4 import BeautifulSoup

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
	
	##whether to jump state or not
    def is_going_to_intro(self, update):
        text = update.message.text
        return text.lower() == 'hi'

    def is_going_to_username(self, update):
        text = update.message.text
        return text.lower() != ' '

    def is_going_to_teacher(self, update):
        text = update.message.text
        return text.lower() == 'a'

    def is_going_to_ability(self, update):
        text = update.message.text
        return text.lower() == 'b'
    
    def is_going_to_money(self, update):
        text = update.message.text
        return text.lower() == 'c'
    
    def is_going_to_all(self, update):
        text = update.message.text
        return text.lower() == '1'

    def is_going_to_one(self, update):
        text = update.message.text
        return text.lower() == '2'

    def is_going_to_photo(self, update):
        text = update.message.text
        return text.lower() == '3'



	##what to do, when jumping
    def on_enter_intro(self, update):
        grab_all_title()
        update.message.reply_text("你好 飢餓時就找我\n我是爽一個R_ni\n首先 what's your name")
        #self.go_back(update)

    def on_enter_username(self, update):
        update.message.reply_text("好的! 飢餓的你\n這邊有幾件事情我可以幫你做\n(a)看了爽翻天\n(b)餓了就該選這個\n(c)真的餓了就選這個\n")
        #self.go_back(update)
        
    def on_enter_ability(self, update):
        update.message.reply_text("餓了就來眼睛吃吃冰淇淋\n(1)看看全部的冰淇淋\n(2)來一球冰淇淋就好\n(3)來張照片上車囉")

    def on_enter_all(self, update):
        update.message.reply_text(str(info))
        self.go_back(update)
        
    def on_enter_one(self, update):
        update.message.reply_text(str(info[randint(0, 5)]))
        self.go_back(update)

    def on_enter_photo(self, update):
        pic = get_icon_see()
        update.message.reply_text(str(pic[0]))
        self.go_back(update)

    def on_enter_money(self, update):
        update.message.reply_text("真的餓成這樣又沒錢就來對對發票吧\n106年09-10月\n特別獎:26638985\n特獎:37266877\n頭獎:15720791 21230260 55899892\n增開六獎248 285 453\n")
        self.go_back(update)

    def on_enter_teacher(self, update):
        replyFile = open('img/teacher.png', 'rb')
        update.message.reply_photo(replyFile)
        update.message.reply_text("這圖片有沒有真的看了爽翻天 ㄎㄎ\n\n")
        replyFile.close()
        self.go_back(update)


	#what to do, when leaving
    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_exit_state2(self, update):
        print('Leaving state2')


################for grab#################
def get_web_page(url):
    resp = requests.get(
        url = url,
        cookies={'over18': '1'}##ppt板上要求18歲
    )
	#success open website
    if resp.status_code != 200:#server的回覆馬 404error 200ok
        print('Invalis url:', resp.url)
        return None
	#falied to open website
    else:
        return resp.text

def get_articles(dom):
	soup = BeautifulSoup(dom, 'html.parser')

	articles = [] #儲存取得的文章資料的地方
	divs = soup.find_all('div','r-ent')#版面其他資訊篩選掉 只留表特 #因為其他資訊也可能是用<a>
	for d in divs:
		if d.find('a'):
			href = d.find('a')['href']#把有用href開頭的都加進來
			title = d.find('a').string
			articles.append({
				'title': title,
				'href':"https://www.ptt.cc"+href,
			})
	return articles

def get_icon(dom): #gif會有問題 要處理！！！！！！！！！！！
    soup = BeautifulSoup(dom, 'html.parser')

    icons = []
    divs = soup.find(id='main-content').find_all('a')
    for d in divs:
        if d['href'].startswith('https://i.imgur.com') or d['href'].startswith('http://i.imgur.com'):
            icons.append(d['href'])
    return icons


def grab_all_title():
    page = get_web_page('http://www.ptt.cc/bbs/Beauty/index2358.html')
    global info
    info = get_articles(page)
    return info
        
def get_icon_see():
    icon_page = get_web_page(info[randint(1, 5)]['href'])
    if icon_page:
        photo = get_icon(icon_page)
    return photo
