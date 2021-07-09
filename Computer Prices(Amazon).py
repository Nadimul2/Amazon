from helium import *
from bs4 import BeautifulSoup
import pandas as pd

data = []


def datareq(i):
    url = f'https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A13896617011&page={i}'
    browser = start_firefox(url, headless=True)

    s = BeautifulSoup(browser.page_source, 'lxml')

    # Find the main part of code where all the main items are stored
    heads = s.find_all('div', class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20')

    for head in heads:
        Name = head.find('span', class_='a-size-base-plus a-color-base a-text-normal').text.strip()[:32]
        New_Price = head.find('span', class_='a-price')
        if New_Price is not None:
            New_Price = head.find('span', class_='a-price').find('span', class_='a-offscreen').text
        else:
            New_Price = '$0'
        Old_Price = head.find('span', class_='a-price a-text-price')
        if Old_Price is not None:
            Old_Price = head.find('span', class_='a-price a-text-price').find('span', class_='a-offscreen').text
        else:
            Old_Price = 'Not Available'
        link = head.find('a', class_='a-link-normal a-text-normal')['href']
        dic = {'Item': Name, 'New Price': New_Price, 'Old Price': Old_Price, 'Item Link': link}
        data.append(dic)
    kill_browser()
    return


for i in range(1, 10):
    datareq(i)


df = pd.DataFrame(data)
print(df)
df.to_csv('CompPrice.csv')



