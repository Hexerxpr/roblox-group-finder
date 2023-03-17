import multiprocessing
import os
import shutil
import pyfiglet
import requests
import time
from core.controllers import Controller
from core.arguments import parse_args
from bs4 import BeautifulSoup
# Clear the terminal and get terminal size
os.system('clear')
columns, rows = shutil.get_terminal_size()

# Generate the ASCII art text using pyfiglet
ascii_text = pyfiglet.figlet_format("RoGroup", font="standard")

# Split the ASCII art text into lines
lines = ascii_text.split("\n")

# Calculate the position of each line in the middle of the terminal
positions = []
x = int(columns / 2 - len(max(lines, key=len)) / 2)  # Calculate x based on the length of the longest line
for i in range(len(lines)):
    y = int(rows / 2 - len(lines) / 2 + i)
    positions.append(y)


# Move the cursor to the calculated positions and print the text in a single print statement
print("\033[1m\033[32m", end="")
for i in range(len(lines)):
    print(f"\033[{positions[i]};{x}H{lines[i]}")
print("\033[1m\033[35m", end="")
print(f"\033[{positions[-1]+1};{x};{x}H[ MACHINE ] : Group Finder Tool v1.0.0")
print("\033[0m", end="")  # Reset font attributes and text color to default values

def get_content_from_sources():
  """
  Makes HTTP requests to the sources, retrieves the content, parses the content for
  proxy information, removes duplicates, and sorts the proxies.
  """
  # Add the URLs of the sources here
  sources = [
      'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all',
      'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
      'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt'
   ]

  # Make an HTTP request to each URL and retrieve the content
  content = []
  for url in sources:
    response = requests.get(url)
    content.append(response.text)

  # Parse the content for proxy information, remove duplicates, and sort the proxies
  proxies = []
  for text in content:
    soup = BeautifulSoup(text, 'html.parser')
    proxies += soup.get_text().split('\n')
  proxies = list(set(proxies))
  proxies.sort()

  # Write the proxies to a file
  with open('proxies.txt', 'w') as f:
    for proxy in proxies:
      f.write(proxy + "\n")
  return proxies


if __name__ == "__main__":
    get_content_from_sources()
    multiprocessing.freeze_support()
    controller = Controller(
        arguments=parse_args()
    )
    try:
        controller.join_workers()
    except KeyboardInterrupt:
        pass

