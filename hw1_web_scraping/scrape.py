import csv
import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/simple/"
OUTPUT_FILE = "countries.csv"


def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_countries(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    for country in soup.find_all("div", class_="country"):
        name = country.find("h3", class_="country-name").get_text(strip=True)
        capital = country.find("span", class_="country-capital").get_text(strip=True)
        population = int(country.find("span", class_="country-population").get_text(strip=True))
        area = float(country.find("span", class_="country-area").get_text(strip=True))
        rows.append([name, capital, population, area])

    return rows


def write_csv(rows, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Capital", "Population", "Area"])
        writer.writerows(rows)


def main():
    html = fetch_page(URL)
    rows = parse_countries(html)
    write_csv(rows, OUTPUT_FILE)
    print(f"Wrote {len(rows)} countries to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()