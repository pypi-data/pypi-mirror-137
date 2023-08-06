from bs4 import BeautifulSoup as bs


def get_forms(url, session):
    '''Returns all form tags found on a web page's `url`

    Parameters
    ----------

    url : str
    '''
    res = session.get(url)
    soup = bs(res.text, 'lxml')
    return soup.find_all('form')


def form_details(form: bs):
    details = {}
    details["action"] = form.attrs.get('action').lower()
    details["method"] = form.attrs.get('method', 'post').lower()

    inputs = []
    for input_tag in form.find_all('input'):
        input_type = input_tag.attrs.get('type', 'text')
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append(
            {"type": input_type, "name": input_name, "value": input_value})

    details["inputs"] = inputs
    return details


def get_version(form_details):
    return [i['value'] for i in form_details['inputs'] if i['name'] == 'version'][0]


def parse_table(html):
    tables = []
    headers = [heading.text.replace(",Other", "")
               for heading in html.find_all('th')]
    tbl_rows = [row for row in html.find_all('tr')]
    for row in tbl_rows:
        tables.append({headers[idx]: cell.text for idx,
                      cell in enumerate(row.find_all("td"))})
    return tables


def get_table(html, table_id):
    page = bs(html, 'lxml')
    table_html = page.find('table', id=table_id)
    return parse_table(table_html)
