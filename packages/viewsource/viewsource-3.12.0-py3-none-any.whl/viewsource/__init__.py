import requests
from bs4 import BeautifulSoup
def html_get(URL, ACTION):

  page = requests.get(URL)

  soup = BeautifulSoup(page.content, "html.parser")
  if ACTION == 1:
    print(soup.prettify())
  elif ACTION == 0:
    return soup
  else:
    return 'put 1 for it to print html, or put 0 to return html'
def formal(text):
  return (text.prettify())