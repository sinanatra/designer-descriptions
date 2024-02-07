import requests
import csv
import re

def scrape_arena_api(channel_slug):
    base_url = 'https://api.are.na/v2/channels/'
    page = 1
    all_block_data = []

    while True:
        url = f'{base_url}{channel_slug}/contents?page={page}'
        response = requests.get(url)
        data = response.json()

        if not data['contents']:
            break

        for block in data['contents']:
            if 'content' in block and block['content']:
                content_text = block['content']
                url = content_text.split("\n")[0].replace("# ","")
                text = content_text.split("\n")[1]
                all_block_data.append({'url': url, 'text': text})

        page += 1

    return all_block_data

channel_slug = 'designer-studio-self-descriptions'
texts = scrape_arena_api(channel_slug)

csv_file_path = 'static/data.csv'
fieldnames = ['url', 'text']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for block_data in texts:
        writer.writerow(block_data)

print(f'Data saved to {csv_file_path}')