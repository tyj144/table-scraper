import httplib2
import bs4
from dateutil import parser

class HTMLNotFoundError(Exception): pass
class TableNotFoundError(Exception): pass
class HeadersNotFoundError(Exception): pass


def scrape_by_html(html, headers=None, links=False, prefix=''):
	'''Finds a table within the HTML and returns a representation of the table as a list of dictionaries.'''

	return table_to_dicts(
				html_to_table(html=html), 
				headers=headers, links=links, prefix=prefix)

def scrape_by_url(url, headers=None, links=False, prefix=''):
	'''Fetches a webpage, then finds a table within the HTML and returns a representation of the table as a list of dictionaries.'''

	return table_to_dicts(
				html_to_table(url=url), 
				headers=headers, links=links, prefix=prefix)

def scrape_by_file(filename, headers=None, links=False, prefix=''):
	'''Fetches a local HTML file, then finds a table within the HTML and returns a representation of the table as a list of dictionaries.'''

	return table_to_dicts(
				html_to_table(filename=filename), 
				headers=headers, links=links, prefix=prefix)

def html_to_table(html=None, url=None, filename=None):
	'''Takes a URL and returns a BeautifulSoup Tag element of the table in the page.'''

	if html:
		pass
	elif url:
		# create an Http object that caches material in .cache
		h = httplib2.Http('.cache')

		# get HTTP response and content from the URL
		# cache's max age is 3.65 days
		response, content = h.request(url, headers={ 'cache-control': 'max-age=315360, public' })

		# content is returned in byte format, turn it into a string
		html = content.decode('utf-8')
	elif filename:
		html = open(filename, mode='r', encoding='utf-8').read()
	else:
		raise HTMLNotFoundError('No HTML found, please pass in HTML as either a string, a url, or a file')

	# create a BeautifulSoup object to parse the returned HTML
	soup = bs4.BeautifulSoup(html, 'html.parser')

	# find the first table in the HTML
	table = soup.find("table")

	# # if type(table) == bs4.element.Tag:
	# # 	raise TableNotFoundError("No table was found within the page")
	# else:
	return table

# separated to make it easier to run on more than one table
def table_to_dicts(table, headers=None, links=False, prefix=''):
	'''Turns a table element into a dictionary with headers as keys.

	Keyword arguments:
	table 	-- url to the page with the table

	Optional:
	headers -- a list of headers to replace the top row (default None)
	links	-- include links in dictionary if True (default False)
	prefix 	-- add domain name to links if links are relative (default '')
	'''

	# gets a list of all row elements (each row is marked by a "tr" tag)
	rows = table.find_all("tr")

	# separates heading from table data if there is a heading row
	heading = None
	if rows[0].find("th"):
		heading = rows.pop(0)

	# ensure that headers are lowercase
	if headers:
		headers = [ header.lower() for header in headers ]
	# get headers from heading row if no headers are passed in
	elif heading:
		# get table headers by iterating through "th" tags 
		headers = [ header.get_text().strip('\u200b\t\n\r').lower() for header in heading.find_all("th") if isinstance(header, bs4.element.Tag)]
	else:
		raise HeadersNotFoundError('No headers found in table, please pass in a valid list of headers')

	# table data is represented as a 2D list
	data = [ [ column.get_text().translate( { ord(c):None for c in '\u200b\t\n\r' } ) for column in row if isinstance(column, bs4.element.Tag)] for row in rows]

	# creates a dictionary for each row using the headers as keys
	data = [ dict(zip(headers, row)) for row in data ]

	# turn datestring into a datetime object
	if "date & time" in data[0]:
		for dictionary in data:
			dictionary["date & time"] = parser.parse(dictionary["date & time"], fuzzy=True)

	# add links to each dictionary if asked for
	if links:
		for i in range(len(data)):
			link = rows[i].find("a")
			
			if link:
				href = prefix + link["href"]
			else:
				href = None
			
			data[i].update({'url':href})

	return data

def delete_by_header(data, header):
	'''Returns a new list of dictionaries with the specified header key removed from each dictionary.'''

	for dictionary in data:
		del dictionary[header]

	return data