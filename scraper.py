import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.garepodistichelazio.it/gare-roma-e-provincia#'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

csv_rows = []

table = soup.find('table', class_='movimenti')
# Verifica che la tabella esista
if table:
    rows = table.find_all('tr')

    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) == 1:
            continue
        else:
            if "Rinviata" in cells[0].text.strip():
                continue
            data = cells[0].text.split("(")[0].strip()
            ora = cells[0].text.split("(")[1].replace(")", "").strip()
            nome_gara = cells[2].text.strip()
            distanza = cells[3].text.strip()
            citta = cells[4].text.strip()
            if cells[9].find('a'):
                sito_web = cells[9].find('a')['href']
            csv_rows.append([nome_gara, data, ora, citta, distanza, sito_web])

    with open('gare_podistiche.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome Gara', 'Data', 'Ora', 'Città', 'Distanza', 'Sito web'])
        writer.writerows(csv_rows)

    print("Scraping completato. Il file CSV è stato creato correttamente.")
else:
    print("La tabella non è stata trovata.")

