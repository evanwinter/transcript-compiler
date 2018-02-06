import requests
import json
import sys
import os
import re
from bs4 import BeautifulSoup

# Find the show on https://www.springfieldspringfield.co.uk/tv_show_episode_scripts.php and use the series
# title found at the end of the URL. Some have the year and some don't!
series_title = 'black-mirror-2011'
base_url = 'https://www.springfieldspringfield.co.uk/'
series_url = 'episode_scripts.php?tv-show=' + series_title	# construct the url for this series' transcripts

response = requests.get(base_url + series_url)
html = BeautifulSoup(response.text, 'html.parser')
episodes = html.find_all('a', class_='season-episode-title')
count = 0

# Prepare output directory and file
if not os.path.exists('output/'):
	os.makedirs('output/')
output_file = 'output/' + series_title + '.txt'

with open(output_file, 'w') as f:
	f.write('Transcripts for ' + series_title.upper() + '\n\n')

	# For each episode of this series, write the transcript to the output file
	for episode in episodes:

		# Get the episode url
		episode_url = episode.get('href')
		episode_page = requests.get(base_url + episode_url)
		
		 # Parse the HTML at that url
		episode_html = BeautifulSoup(episode_page.text, 'html.parser')
		
		# Check for the episode title and transcript
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

		count = count + 1
		print(str(count) + ': ' + episode_title)



		# Write title and transcript to output file
		f.write('Title: ' + episode_title + '\n')
		f.write('-----------------------\n')
		f.write(episode_transcript + '\n\n')

print('Done!')
sys.exit(-1)