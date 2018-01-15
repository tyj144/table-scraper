import tblscraper
import unittest

class TestTblscraper(unittest.TestCase):

	def test_basic_scrape(self):
		'''Pulls out a list of people with key value pairs for each of their attributes'''
		self.assertEqual(tblscraper.scrape_by_file("sample_html_tables/basic_table.html"), 
			[{'name': 'John Smith', 'phone': '(978) 212-3210', 'e-mail': 'john_smith@gmail.com' },
			{'name': 'Lauren Jones', 'phone': '(978) 405-3926', 'e-mail': 'lauren_jones@gmail.com' }])

if __name__ == '__main__':
    unittest.main()