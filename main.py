import requests
import json
import sys
import os
import re
from bs4 import BeautifulSoup

series_title = 'black-mirror-2011'
base_url = 'https://www.springfieldspringfield.co.uk/'
series_url = 'episode_scripts.php?tv-show=' + series_title

response = requests.get(base_url + series_url)
html = BeautifulSoup(response.text, 'html.parser')
episodes = html.find_all('a', class_='season-episode-title')
count = 0

if not os.path.exists('output/'):
	os.makedirs('output/')

output_file = 'output/' + series_title + '.txt'

with open(output_file, 'w') as f:
	f.write('Transcripts for ' + series_title.upper() + '\n\n')

	for episode in episodes:
		
		episode_url = episode.get('href')
		episode_page = requests.get(base_url + episode_url)
		episode_html = BeautifulSoup(episode_page.text, 'html.parser')
		try:
			episode_title = episode_html.find('div', class_='breadcrumbs').findNext('h3').get_text()
		except:
			print('--Error getting title.')
			pass
		try:
			episode_transcript = episode_html.find('div', class_='scrolling-script-container').get_text()
		except:
			print('--Error getting transcript.')
			pass

		print(episode_title)

		# Write to file
		f.write('Title: ' + episode_title + '\n')
		f.write('-----------------------\n')
		f.write(episode_transcript + '\n\n')

print('Done!')