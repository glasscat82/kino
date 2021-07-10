# parsing kinopoisk.ru/afisha/city/{city_id}
from datetime import datetime
from prettytable import PrettyTable
from kino import kino
# from pprint import pprint

def main():
	start = datetime.now()	
	
	# ----- afisha from city
	city_id = 490
	afisha = kino(url=f'https://www.kinopoisk.ru/afisha/city/{city_id}/')
	html_ = afisha.get_html()
	cinema_ = afisha.get_afisha_city(html=html_)
	afisha.p(cinema_)
	afisha.write_json(data=cinema_, path='./json/afisha.json')	
	# ----- end afisha

	# ----- the tables	
	# for af in afisha.load_json(path='./json/afisha.json'):
	# 	afisha.p(af['title'])
	# 	for f in af['films']:
	# 		afisha.p(f['name'], " ".join(f['description']))
	# ----- end tables

	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()