import requests
from bs4 import BeautifulSoup
import logging
import subprocess
import aiohttp
import os
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NYCPublicDataFetcher:
    def __init__(self, start_url):
        self.start_url = start_url

    async def fetch_content(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logging.error(f"Error {response.status}: Unable to fetch the webpage.")
                        return ""
            except aiohttp.ClientError as e:
                logging.error(f"Error fetching URL {url}: {e}")
                return ""

    def extract_view_ids_and_links(self, content):
        data_dict = {}
        try:
            soup = BeautifulSoup(content, 'html.parser')
            browse_content = soup.find(class_='browse2-content')
            if not browse_content:
                logging.warning("Could not find 'browse2-content' in the provided content.")
                return {}
            
            results = browse_content.find_all(class_='browse2-result')
            for result in results:
                view_id = result.get('data-view-id', None)
                link_element = result.find(class_='browse2-result-name-link', href=True)
                if view_id and link_element:
                    data_dict[view_id] = link_element['href']
                    
        except Exception as e:
            logging.error(f"Error extracting view IDs and links: {e}")
        return data_dict

    async def run(self):  # Note the "async" here
        main_content = await self.fetch_content(self.start_url)

        if not main_content:
            logging.warning(f"No content fetched from {self.start_url}. Exiting...")
            return {}
        
        data = self.extract_view_ids_and_links(main_content)
        # data = {url.split('/')[-2]: url for _, url in data.items()
        return data

class NYCEndpointFetcher:
    def __init__(self):
        pass

    async def fetch_content(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        text = await response.text()
                        with open('temp.html', 'w+') as temp_file:
                            temp_file.write(text)
                            api_resource_link = self.bash_resource_link('temp.html')
                        return api_resource_link
                    else:
                        logging.error(f"Error {response.status}: Unable to fetch the webpage.")
                        return ""
            except aiohttp.ClientError as e:
                logging.error(f"Error fetching URL {url}: {e}")
                return ""

    def bash_resource_link(self, file_name):
        # This function remains synchronous as it's just running a bash command
        command_content = f"cat {file_name} | grep -Eo '(http|https)://[a-zA-Z0-9./?=_%:-]*' | grep -E 'resource/.*\\.json$' | sort -u"
        try:
            result = subprocess.run(command_content, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.error(f"Error executing bash command: {result.stderr}")
                return None
        except Exception as e:
            logging.error(f"Error running subprocess command: {e}")
            return None

    async def run(self, data_dict):  # Note the "async" here
        endpoints_dict = {}
        for key, url in data_dict.items():
            endpoint = await self.fetch_content(url)  # Await the asynchronous fetch_content method
            if endpoint:
                endpoints_dict[key] = endpoint
            else:
                logging.warning(f"Couldn't find endpoint for {key}")
        try:
            subprocess.run("rm temp.html", shell=True)
        except Exception as e:
            logging.error(f"Error deleting temporary file: {e}")
        return endpoints_dict

class NYCUrlFetcher:
    def __init__(self):
        self.user_agents = [
            # List of popular user agents
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; AS; rv:11.0) like Gecko'
        ]
        self.file_path = 'temp/starting_point.html'
        logging.basicConfig(level=logging.INFO)

    async def fetch_content(self, url):
        headers = {'User-Agent': random.choice(self.user_agents)}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        # Save the fetched content to the file
                        if not os.path.exists('temp'):
                            os.makedirs('temp')
                        with open(self.file_path, 'w', encoding='utf-8') as file:
                            file.write(html_content)
                        return html_content
                    else:
                        logging.error(f"Error {response.status}: Unable to fetch the webpage.")
                        return None
            except aiohttp.ClientError as e:
                logging.error(f"Error fetching URL {url}: {e}")
                return None

    def extract_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        categories_urls = {}

        # Extract all anchor tags
        anchor_tags = soup.find_all('a')

        for tag in anchor_tags:
            name = tag.text.strip()
            url = tag.get('href')
            if name and url and "data.cityofnewyork.us/browse" in url:
                categories_urls[name] = url

        return categories_urls

    async def run(self, url):
        html_content = await self.fetch_content(url)
        if html_content:
            return self.extract_data(html_content)
        else:
            logging.warning(f"Failed to fetch content from {url}")
            return {}
 