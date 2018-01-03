import requests
from bs4 import BeautifulSoup


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


if __name__ == '__main__':
	page = get_web_page('https://www.ptt.cc/bbs/Beauty/index.html')
	info = get_articles(page)

	web_index = 0
	icon_index = 0

	while(1):
		print('1:show all')
		print('2:show one')
		print('3:photo directly')
		choose = int(input('ENTER: '))
		print(choose)

		if (page == None):
			print("the Beauty ptt is break")
			break

		if page:

			##show all
			if(choose == 1):
				for i in info:
					print(i)		
				#印出的網頁 可操控它印出哪一個網頁標籤

			##show one
			if(choose == 2):
				print(info[index])
				web_index = web_index + 1
			
			##show photo directly
			if(choose == 3):
				icon_page = get_web_page(info[icon_index]['href'])
				if icon_page:
					photo = get_icon(icon_page)
				print(photo[0])
				icon_index = icon_index + 1


"""
soup.find('p')            # 回傳第一個被 <p> </p> 所包圍的區塊
# <p id="p1">我是段落一</p>

soup.find('p', id='p2')   # 回傳第一個被 <p> </p> 所包圍的區塊且 id="p2"
# <p id="p2" style="">我是段落二</p>

soup.find(id='p2')        # 回傳第一個 id="p2" 的區塊
# <p id="p2" style="">我是段落二</p>

soup.find_all('p')        # 回傳所有被 <p> </p> 所包圍的區塊
# [<p id="p1">我是段落一</p>, <p id="p2" style="">我是段落二</p>]

soup.find('h1', 'large')  # 找尋第一個 <h1> 區塊且 class="large"
# <h1 class="large" style="">我是變色且置中的抬頭</h1>
"""
