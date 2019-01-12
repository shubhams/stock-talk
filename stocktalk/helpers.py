import requests

from stocktalk import app
from stocktalk.constants.app_constants import ALPHA_VANTAGE_URLS


def get_search_results(keywords):
	key_val = {
		'function': ALPHA_VANTAGE_URLS.FUNCTIONS.SYMBOL_SEARCH,
		'keywords': keywords,
		'apikey': app.config['ALPHA_VANTAGE_KEY']
	}
	r = requests.get(ALPHA_VANTAGE_URLS.BASE_URL, params=key_val)
	print(r.json())
	return r.json()