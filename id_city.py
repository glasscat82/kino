# parsing kinopoisk.ru/afisha/city/{city_id}
from datetime import datetime
import json
from bs4 import BeautifulSoup

# Функция для замены нескольких значений && replace_values = {"кот": "кошка", "кошка": "собака"}
def multiple_replace(target_str, replace_values):
	# получаем заменяемое: подставляемое из словаря в цикле
	for i, j in replace_values.items():
		# меняем все target_str на подставляемое
		target_str = target_str.replace(i, j)
	return target_str

def main():
	start = datetime.now()	
	
	# ----- id city
	html = False
	path = './json/city.html'
	with open(path, 'r', encoding='utf-8') as f:
		html = f.read()
	
	soup = BeautifulSoup(html, 'lxml')
	city = []
	for c_ in soup.find('ul', class_='list').find_all('li'):
		c_id = multiple_replace(c_.find('a').get('href'), {"/afisha/city/":"", "/":""})
		city.append({'name':c_.text.strip(), 'id':c_id})	
	
	print(city, sep=' / ', end='\n')

	with open('./json/city.json', 'w', encoding='utf8') as f:
		json.dump(city, f, indent=2, ensure_ascii=False)
	# ----- end

	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()