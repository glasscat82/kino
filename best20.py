# parsing kinopoisk.ru for Russia
from datetime import datetime
# from prettytable import PrettyTable
from kino import kino

def main():
	start = datetime.now()	
	
	# ----- 20 best films
	url_ = 'https://www.kinopoisk.ru/lists/navigator/?quick_filters=high_rated&limit=20&tab=best'
	flm = kino(url=url_, filename='kino.json')
	html_ = flm.get_html()
	# flm.p(html_)
	links_ = flm.get_all_links(html=html_)
	for l_ in links_['films']:		
		flm.p(l_)
	# -----

	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()