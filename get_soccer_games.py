from tblscraper import scrape_by_url

games = scrape_by_url("http://nashuanorthathletics.com/main/teamschedule/id/3695990/seasonid/4215431")

for game in games:
	print(game)
# 	for header, value in game.items():
# 		print(value, end='\t')
# 	print()