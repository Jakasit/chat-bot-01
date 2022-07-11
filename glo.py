from cgitb import text
import requests
import bs4
import pandas as pd
import openpyxl
from tqdm import tqdm

ประเภทฉลาก = []
เลขรางวัล = []
วันที่ = []
# url = "https://www.lottery.co.th/small"

for i in tqdm(range(1,19)):
	url = f"https://news.sanook.com/lotto/archive/page/{i}/"
	data = requests.get(url)

	from bs4 import BeautifulSoup
	soup = bs4.BeautifulSoup(data.text,'html.parser')

	maindata = soup.find_all('article',{'class':'archive--lotto'}) # <- ค่าที่ใช้ในการค้นหา #,button ,class,btn btn-primary

	for c in maindata:
		dates = c.find('h3',{'class':'archive--lotto__head-lot'}).text
		resultHEAD = c.find_all('ul',{'class':'archive--lotto__result-list'})
		for rh in resultHEAD:
			for r in rh.find_all('em'):
				if r.text == "ผลสลากกินแบ่งรัฐบาล รางวัลที่ 1":
					วันที่.append(dates)
				else:
					วันที่.append("-------")
				ประเภทฉลาก.append(r.text)
		
		for rh in resultHEAD:
			for r in rh.find_all('strong',{'class':'archive--lotto__result-number'}):
				st = r.text
				st = st.replace('\n','')
				เลขรางวัล.append(st)

tb = pd.DataFrame([วันที่,ประเภทฉลาก,เลขรางวัล]).transpose()
tb.columns = ['data','ประเภทฉลาก','เลขที่ออก']
tb.set_index('data',inplace=True)
tb.to_excel('lot.xlsx',engine='openpyxl',encoding='utf8')

	
