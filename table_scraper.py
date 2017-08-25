import httplib2
from bs4 import BeautifulSoup

class HTMLNotFoundError(Exception): pass
class TableNotFoundError(Exception): pass
class HeadersNotFoundError(Exception): pass

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
		html = open(file, mode='r', encoding='utf-8').read()
	else:
		raise HTMLNotFoundError('No HTML found, please pass in HTML as either a string, a url, or a file')

	# create a BeautifulSoup object to parse the returned HTML
	soup = BeautifulSoup(html, 'html.parser')

	# find the first table in the HTML
	table = soup.find("table")

	return table

# separated to make it easier to run on more than one table
def table_to_dict(table, headers=None, links=False, prefix=''):
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
		headers = [ header.get_text().strip('\u200b').lower() for header in heading.find_all("th") ]
	else:
		raise HeadersNotFoundError('No headers found in table, please pass in a valid list of headers')


	# table data is represented as a 2D list
	data = [ [ column.get_text().strip('\u200b') for column in row] for row in rows]

	# creates a dictionary for each row using the headers as keys
	data = [ dict(zip(headers, row)) for row in data ]

	# add links to each dictionary if asked for
	if links:
		for i in range(len(data)):
			link = rows[i].find("a")
			
			if link:
				href = prefix + link["href"]
			else:
				href = None
			
			data[i].update({'link':href})

	return data