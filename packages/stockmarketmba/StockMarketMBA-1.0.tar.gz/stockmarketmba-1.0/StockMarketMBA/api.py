import StockMarketMBA.lib as lib
from requests.sessions import session
import json

# Initiate
s = session()
with open('headers.json') as f:
    HEADERS = json.load(f)


def symbol_lookup(ticker):
    url = "https://stockmarketmba.com/symbollookup.php"
    # Retrieve version ID from web form
    forms = lib.get_forms(url, s)[1]
    details = lib.form_details(forms)
    version = lib.get_version(details)

    # Add ticker and version ID to search payload
    payload = 'action=Go&search={}&version={}'.format(ticker, version)

    # Request and find table
    r = s.post(url, headers=HEADERS, data=payload)
    return lib.get_table(r.text, 'searchtable')


def exch_secs(exchange_code):
    url = "https://stockmarketmba.com/listofstocksforanexchange.php"
    payload = 'action=Go&exchangecode={}'.format(exchange_code)

    # Request and find table
    r = s.post(url, headers=HEADERS, data=payload)
    return lib.get_table(r.text, 'ETFs')


def exch_symbols():
    url = 'https://stockmarketmba.com/globalstockexchanges.php'

    r = s.get(url)
    return lib.get_table(r.text, 'ETFs')


def pending_SPACs():
    url = 'https://stockmarketmba.com/pendingspacmergers.php'

    r = s.get(url)
    return lib.get_table(r.text, 'ETFs')
