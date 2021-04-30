This Python application scrapes property data from www.rew.ca and it's part of a project where I analyzed the trade off between buying versus renting a property in greater Vancouver. You can find the presentation, report and link to the Tableau visualization of this project under the projects section of my portfolio website at:
www.filipeanalytics.com

This script can be used to extract both rental and sales data. By default, it's scraping sales data, but if you want to scrape rental data, you need to do the following:
Comment   line 67: URLbuy = "https://www.rew.ca/sitemap/real-estate/bc"
Uncomment line 68: URLrent = "https://www.rew.ca/sitemap/rentals/bc"
Uncomment line 71: browser.get(URLrent)
Comment   line 72: browser.get(URLbuy)
Uncomment line 222: browser.get(URLrent)
Comment   line 223: browser.get(URLbuy)

You'll also need to update the PATH and CSV_FILE on lines 229 and 230 to an address in your computer, and if scraping rent data, change the name of the csv file to PropertiesForRent.csv.
PATH = "C:/Users/filip/Documents/PythonFiles/"
CSV_FILE = "PropertiesOnSale.csv"

Download ChromeDriver from https://chromedriver.chromium.org/ Save it in a folder that you can find easily.
On line 63, update the path to where you saved your chrome plugin (chromedriver.exe)
DRIVER_PATH = "C:/Users/filip/Documents/PythonFiles/chromedriver"

