from table_scraper import html_to_table, table_to_dict

sermons = table_to_dict(html_to_table(url="https://cbcgn-public.sharepoint.com/sunday-sermons1"), headers=['Date', 'Speaker', 'Title'], links=True, prefix='https://cbcgn-public.sharepoint.com')

for sermon in sermons:
	for header, value in sermon.items():
		print(value, end='\t')
	print("")