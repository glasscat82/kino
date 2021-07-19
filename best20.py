# parsing kinopoisk.ru for Russia
from datetime import datetime
from prettytable import PrettyTable
from kino import kino

def main():
	start = datetime.now()	
	
	# ----- 20 best films
	url_ = 'https://www.kinopoisk.ru/lists/navigator/?quick_filters=high_rated&limit=20&tab=best'
	flm = kino(url=url_, filename='kino.json')
	html_ = flm.get_html()
	links_ = flm.get_all_links(html=html_)
	# the table
	x = PrettyTable()
	x.field_names = ["№", "Название", "Год", "Страна", "Рейтинг", "Голосов"]
	x.align["Название"] = x.align["Год"] = x.align["Страна"] = "l"
	for index, r_ in enumerate(links_['films'], 1):		
		x.add_row([index, r_[2], r_[3], r_[4], r_[5], r_[6]])
	print(x.get_string(title='Лучшие 20 фильмов'))
	# -----

	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()