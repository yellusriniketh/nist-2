from pathlib import Path

import time
import requests
from bs4 import BeautifulSoup

base_url = (
    "https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID=C7782447&"
    "Type=IsoBar&Digits=5&P={pressure}&THigh={t_high}&TLow={t_low}&TInc={t_inc}&"
    "RefState=DEF&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=Pa*s&STUnit=N%2Fm"
)

# Configuration: set the single pressure value you want to fetch here
pressure_value = 110  # change this to the pressure you need to fetch (e.g. 272)

# Temperature range and increment
min_temp = 54.361
max_temp = 2100
temperature_increment = 1
max_points_per_fetch = 600

# Output prefix/folder (keep in sync with the multi-pressure scraper)
file_prefix = "oxygen"
output_dir = Path(file_prefix)
output_dir.mkdir(parents=True, exist_ok=True)

# Network retry settings
max_retries = 3
retry_backoff = 5  # seconds (exponential backoff multiplier)

combined_content = ""
t_low = min_temp

while t_low <= max_temp:
    t_high = min(t_low + temperature_increment * (max_points_per_fetch - 1), max_temp)
    url = base_url.format(
        pressure=pressure_value, t_high=t_high, t_low=t_low, t_inc=temperature_increment
    )

    response = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=30)
        except requests.RequestException as e:
            print(f"Request error (attempt {attempt}) for P={pressure_value}, TLow={t_low}, THigh={t_high}: {e}")
            response = None

        if response is not None and response.status_code == 200:
            break

        # If not successful, wait then retry (only for server/network errors)
        if attempt < max_retries:
            wait = retry_backoff * attempt
            time.sleep(wait)

    if response is None or response.status_code != 200:
        print(
            f"Failed to retrieve webpage for P={pressure_value}, TLow={t_low}, THigh={t_high}. Status code: {getattr(response, 'status_code', 'N/A')}"
        )
        # Stop further fetching to allow single-pressure debugging
        break

    soup = BeautifulSoup(response.content, 'html.parser')
    html_content = soup.prettify()

    if t_low == min_temp:
        # Keep the first chunk contiguous and trim its trailing whitespace
        combined_content += html_content.rstrip()
    else:
        # Remove the first line (header) for subsequent chunks and add exactly one separator newline
        lines = html_content.splitlines()
        if lines:
            combined_content += "\n" + "\n".join(lines[1:])

    if t_high >= max_temp:
        break

    t_low = t_high + temperature_increment

filename = output_dir / f"{file_prefix}_{pressure_value}.txt"
with open(filename, "w", encoding="utf-8") as file:
    file.write(combined_content)

print(f"Webpage content saved to '{filename}'.")