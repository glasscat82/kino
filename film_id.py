# parsing kinopoisk.ru/film/{film_id}/
from datetime import datetime
# from prettytable import PrettyTable
from kino import kino
# from pprint import pprint

def main():
	start = datetime.now()	
	
	# ----- film
	film_id = 841747
	film = kino(url=f'https://www.kinopoisk.ru/film/{film_id}/')
	html_ = film.get_html()
	flm_ = film.get_film(html=html_)
	film.p(flm_)
	# film.write_json(data=cinema_, path='./json/afisha.json')	
	# ----- end film

	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()