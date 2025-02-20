import requests
import csv
from time import sleep
from tqdm import tqdm

# Headers for HTTP request
headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'connection': 'keep-alive',
    'referer': 'https://opsin.ch.cam.ac.uk/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

# Read compounds from text file
with open('compound_lists.txt', 'r') as file:
    compound_lists = [line.strip() for line in file.readlines() if line.strip()]

# Open the CSV file for writing
with open('opsin_compounds.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["Compound", "InChI", "Standard InChI", "Standard InChIKey", "SMILES"])
    
    for compounds in tqdm(compound_lists):
        base_url = "https://opsin.ch.cam.ac.uk/opsin/"
        compound_name = compounds.strip()
        try:
            response = requests.get(base_url+compound_name, headers=headers, timeout=10)
            sleep(2)
            response.raise_for_status()
            data = response.json()

            # Write the data to CSV
            writer.writerow([compound_name, data['inchi'], data['stdinchi'], data['stdinchikey'], data['smiles']])

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while making the request for {compounds}: {e}")
            writer.writerow([compound_name, "N/A", "N/A", "N/A", "N/A"])
 
        except json.JSONDecodeError as e:
            print(f"Error occurred while parsing JSON for {compounds}: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred for {compounds}: {e}")

              
