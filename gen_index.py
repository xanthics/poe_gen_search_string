from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# for local hosting, since selenium requires a hosted page to work correctly
import http.server
import socketserver
import threading

from os import getcwd
# make it pretty
from bs4 import BeautifulSoup as bs
import minify_html

# for sub processes
from helper_files.gen_map_mods import gen_mods
from generate_ngrams import gen_ngrams


# load the page in firefox-selenium and return the html
def load_page_firefox(page_name):
	from selenium.webdriver.firefox.options import Options
	from selenium.webdriver.firefox.service import Service
	options = Options()
	options.set_preference("permissions.default.image", 2)
	options.headless = True
	options.log.level = "fatal"
	service = Service(getcwd() + '\\geckodriver.exe')
	driver = webdriver.Firefox(options=options, service=service)
	driver.get(page_name)
	try:
		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "prerendered")))
	except TimeoutException as err:
		print(err)
		exit(-1)
	html = driver.page_source
	driver.quit()
	return html


# make some modifications to the page
def update_page(soup):
	meta1 = soup.new_tag('meta')
	meta1['name'] = 'description'
	meta1['content'] = 'PoE Search String Generator.'
	meta2 = soup.new_tag('meta')
	meta2['name'] = 'keywords'
	meta2['content'] = 'best videogames, free to play, free game, online games, fantasy games, PC games, PC gaming, Path of Exile'
	soup.head.extend([meta1, meta2])
	soup.find('meta', {'name': 'robots'}).extract()
	soup.find('script', {'src': 'gen_page.py'})['src'] = 'main.py'


# SimpleHTTPRequestHandler does some funky things with caching, start a separate instance to avoid
def main():
	# where is the server
	port = 62435
	handler = http.server.SimpleHTTPRequestHandler
	server = socketserver.TCPServer(("", port), handler)
	thread = threading.Thread(target=server.serve_forever)
	thread.daemon = True  # so the server dies when the program exits
	thread.start()
	# Generate the page
	local_page = f'http://localhost:{port}/dynamic_page.html'
	html = load_page_firefox(local_page)
	sc_soup = bs(html, "html.parser")
	update_page(sc_soup)
	server.shutdown()  # kill the server since we are done with it
	try:
		minified = minify_html.minify(str(sc_soup), minify_js=False, minify_css=False)
		with open('index.html', 'w', encoding='utf-8') as f:
			f.write(f"<!DOCTYPE html>{minified}")
	except SyntaxError as e:
		print("SC error", e)


if __name__ == '__main__':
	gen_mods()
	gen_ngrams()
	main()
