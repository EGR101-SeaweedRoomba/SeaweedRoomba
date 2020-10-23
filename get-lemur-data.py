import urllib.request
import requests
from bs4 import BeautifulSoup
import xlrd

url="https://en.wikipedia.org/wiki/List_of_lemur_species"

page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, features="html.parser")

all_tables=soup.find_all("table")
right_table=soup.find('table', class_='wikitable sortable')

A=[]
B=[]

for table in soup.find_all('table', class_='wikitable sortable')[0:3]:
        for row in table.findAll('tr'):
                cells=row.findAll('td')
                if len(cells)==6:
                        A.append(cells[1].find(text=True))
                        B.append(cells[4].find(text=True))



url="https://lemur.duke.edu/wordpress/wp-content/uploads/2019/07/DLC_ColonyList_02Jul2019.xlsx"
r=requests.get(url, allow_redirects=True)

open(url.split('/')[-1], 'wb').write(r.content)

workbook= xlrd.open_workbook(url.split('/')[-1])
sheet = workbook.sheet_by_index(0)

names=[]

for i in range(len(A)):
	current=[]
	for rowx in range(sheet.nrows):
		values = sheet.row_values(rowx)
		if values[1]==A[i] or (values[1]=='Red-fronted brown lemur' and A[i]=='Red-fronted lemur'):
			current.append(values[4])
	print(current)
	names.append(current)
with open('endangered.txt', 'w') as file:
	for i in range(len(A)):
		file.write(A[i]+ ","+ B[i])
		if names[i]:
			file.write(','+'/'.join(names[i]))
		file.write('\n');
