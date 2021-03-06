# Table Scraper
## What It Does
Scrapes data from HTML tables into a Python-friendly format. Turns an HTML table into a list of Python dictionaries, where each row is a dictionary and each key-value pair is an attribute of a row.

Table Scraper is currently being used for [Google Calendar Automator](https://github.com/tyj144/google-calendar-automator) to parse schedules and upload events to Google Calendar and for the [CBCGN website](https://cbcgn.herokuapp.com/) to pull [sermons](https://cbcgn.herokuapp.com/sermons/) from their [old sermons page](https://cbcgn-public.sharepoint.com/sunday-sermons1).

## Installation and Usage
1. Clone the project using `git clone https://github.com/tyj144/table-scraper.git` or download the ZIP file by clicking the green "Clone or download button" above.
2. Install the requirements by running `pip install requirements.txt`.
3. In your project or in a Python shell, import the table scraper by typing `import tblscraper`.
4. Try an example, such as `tblscraper.scrape_by_file("sample_html_tables/basic_table.html")`. The results should look like the example below.

The tblscraper module also includes the ability to parse HTML directly using the `scrape_by_html` function and most importantly, can scrape a table by going to a page's URL using the `scrape_by_url` function.

## Example
An HTML table that looks like:
```
<table>
	<tr>
		<th>Name</th>
		<th>Phone</th>
		<th>E-mail</th>
	</tr>
	<tr>
		<td>John Smith</td>
		<td>(978) 212-3210</td>
		<td>john_smith@gmail.com</td>
	</tr>	
	<tr>
		<td>Lauren Jones</td>
		<td>(978) 405-3926</td>
		<td>lauren_jones@gmail.com</td>
	</tr>
</table>
```

turns into a list of Python dictionaries that looks like:
```
[{'name': 'John Smith', 'phone': '(978) 212-3210', 'e-mail': 'john_smith@gmail.com' }, {'name': 'Lauren Jones', 'phone': '(978) 405-3926', 'e-mail': 'lauren_jones@gmail.com' }]
```

## Issues
* Make sure that scrape_by_file can only get local HTML files
* Account for other possible header names for dates/times besides "Date & Time"
