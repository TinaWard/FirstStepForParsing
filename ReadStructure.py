from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import time

def readystate_complete(d):
    return d.execute_script("return document.readyState") == "complete"

myUrl = "https://casino-now.co.uk/mobile-casino/"

mainKey = "mobile casino"

list = []

driver = webdriver.Firefox()
driver.get("http://www.google.com")

elem = driver.find_element_by_name("q")
elem.send_keys(mainKey)
elem.submit()

WebDriverWait(driver, 30).until(readystate_complete)
time.sleep(1)

htmltext = driver.page_source


pages = re.compile('<cite class="iUh30">(.*?)</cite>' , re.DOTALL | re.IGNORECASE).findall(str(htmltext))

driver.quit()

FullData = pd.DataFrame(index = range(len(pages)), columns=['url','mainKey','html','KWD', 'structure'])

FullData['url'] = pages
FullData['mainKey'] = mainKey
FullData


for index in range(len(FullData)):
    driver = webdriver.Firefox()
    driver.get(FullData['url'][index])
    WebDriverWait(driver, 30).until(readystate_complete)
    time.sleep(1)
    FullData['html'][index] = str(driver.page_source)
    print(FullData['url'][index])
    driver.quit()


def taggify(soup):
    for tag in soup:
        if isinstance(tag, bs4.Tag):
            yield '<{}>{}</{}>'.format(tag.name, ''.join(taggify(tag)), tag.name)

for index in range(len(FullData)):

    soup = BeautifulSoup(FullData['html'][index])

    structure = ''.join(taggify(soup))
    structure = re.sub('<meta>','',structure)
    structure = re.sub('</meta>','',structure)
    structure = re.sub('<style>','',structure)
    structure = re.sub('</style>','',structure)
    structure = re.sub('<link>','',structure)
    structure = re.sub('</link>','',structure)
    structure = re.sub('<script>','',structure)
    structure = re.sub('</script>','',structure)
    structure = re.sub('<div>','',structure)
    structure = re.sub('</div>','',structure)
    structure = re.sub('<span>','',structure)
    structure = re.sub('</span>','',structure)
    structure = re.sub('<base>','',structure)
    structure = re.sub('</base>','',structure)
    structure = re.sub('<li>','',structure)
    structure = re.sub('</li>','',structure)
    structure = re.sub('<ul>','',structure)
    structure = re.sub('</ul>','',structure)
    structure = re.sub('<a>','',structure)
    structure = re.sub('</a>','',structure)
    structure = re.sub('<img>','',structure)
    structure = re.sub('</img>','',structure)
    structure = re.sub('<button>','',structure)
    structure = re.sub('</button>','',structure)
    structure = re.sub('<input>','',structure)
    structure = re.sub('</input>','',structure)
    structure = re.sub('<p>','',structure)
    structure = re.sub('</p>','',structure)
    structure = re.sub('<label>','',structure)
    structure = re.sub('</label>','',structure)
    structure = re.sub('<i>','',structure)
    structure = re.sub('</i>','',structure)
    structure = re.sub('<form>','',structure)
    structure = re.sub('</form>','',structure)
    structure = re.sub('<fieldset>','',structure)
    structure = re.sub('</fieldset>','',structure)
    structure = re.sub('<b>','',structure)
    structure = re.sub('</b>','',structure)
    structure = re.sub('<table>','',structure)
    structure = re.sub('</table>','',structure)
    structure = re.sub('<tr>','',structure)
    structure = re.sub('</tr>','',structure)
    structure = re.sub('<th>','',structure)
    structure = re.sub('</th>','',structure)
    structure = re.sub('<thead>','',structure)
    structure = re.sub('</thead>','',structure)
    structure = re.sub('<tbody>','',structure)
    structure = re.sub('</tbody>','',structure)
    structure = re.sub('<br>','',structure)
    structure = re.sub('</br>','',structure)
    structure = re.sub('<noscript>','',structure)
    structure = re.sub('</noscript>','',structure)
    structure = re.sub('<section>','',structure)
    structure = re.sub('</section>','',structure)
    structure = re.sub('<strong>','',structure)
    structure = re.sub('</strong>','',structure)
    structure = re.sub('<iframe>','',structure)
    structure = re.sub('</iframe>','',structure)
    structure = re.sub('<td>','',structure)
    structure = re.sub('</td>','',structure)
    structure = re.sub('<nav>','',structure)
    structure = re.sub('</nav>','',structure)
    structure = re.sub('<area>','',structure)
    structure = re.sub('</area>','',structure)
    structure = re.sub('<map>','',structure)
    structure = re.sub('</map>','',structure)
    structure = re.sub('><','> <',structure)
    FullData['structure'][index] = structure

    html = FullData['html'][index]
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    Nkr = text.lower().count(mainKey.lower())
    Nwp = len(mainKey.split())
    Tkn = len(text.split())
    mainKeyWordDensity = (Nkr / (Tkn - (Nkr * (Nwp - 1)))) * 100
    FullData['KWD'][index] = str(round(mainKeyWordDensity, 2)) + "%"


writer = pd.ExcelWriter('Co_html.xlsx')
FullData.to_excel(writer, 'Sheet1')
writer.save()

driver = webdriver.Firefox()
driver.get(myUrl)
WebDriverWait(driver, 30).until(readystate_complete)
time.sleep(1)
html = str(driver.page_source)
soup = BeautifulSoup(html)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()  # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)