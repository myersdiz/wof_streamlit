# This script is used to extract the puzzle data from the Wheel of Fortune Compendium

import pandas as pd
import json, requests

from bs4 import BeautifulSoup

def extract_table(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')[4]
    return table

def table_to_json(table, output_file):
    # Extract the data from the table
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    # Remove the header row
    data = data[1:]

    try:
        # Format the data into a pandas dataframe
        df = pd.DataFrame(data, columns=['PUZZLE', 'CATEGORY', 'DATE', 'EP#', 'ROUND'])

        # Remove *'s from the DATE column
        df['DATE'] = df['DATE'].str.replace(r'\*', '', regex=True)

        # Remove *'s from the EP# column
        df['EP#'] = df['EP#'].str.replace(r'\*', '', regex=True)

        json = df.to_json()

        # Output json to file
        with open("puzzle_parser/" + output_file, 'w') as f:
            f.write(json)
    except:
        print("Error: " + output_file)

def main():
    for i in range(1,42):  #range(1,42)
        url = "https://buyavowel.boards.net/page/compendium" + str(i)
        output_file = "season_" + str(i) + ".json"

        table = extract_table(url)
        table_to_json(table, output_file)

if __name__ == "__main__":
    main()