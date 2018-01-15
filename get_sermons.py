from tblscraper import scrape_by_url

sermons = scrape_by_url("https://cbcgn-public.sharepoint.com/sunday-sermons1", headers=['Date', 'Speaker', 'Title'], links=True, prefix='https://cbcgn-public.sharepoint.com')

for sermon in sermons:
	for header, value in sermon.items():
		print(value, end='\t')
	print()