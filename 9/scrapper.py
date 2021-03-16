import requests
from bs4 import BeautifulSoup



def scrapper_handler(term):
    so_data = so_scrapper(term)
    wwr_data = wwr_scrapper(term)
    ro_data = ro_scrapper(term)
    sum_data = so_data + wwr_data + ro_data
    return sum_data


def so_scrapper(term):
    url = f'https://stackoverflow.com/jobs?q={term}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    list_results = soup.find('div', {'class': 'listResults'})
    jobs = list_results.find_all('div', {'class': '-job'})
    so_list = []
    for job in jobs:
        title = job.find('a', {'class': 's-link'}).string
        link = job.find('a', {'class': 's-link'})['href']
        link = f'https://stackoverflow.com/{link}'
        company = job.find('h3', {'class': 'fc-black-700'}).find('span').getText(strip=True)
        so_list.append({'title': title, 'link': link, 'company': company})

    return so_list

def wwr_scrapper(term):
    url = f'https://weworkremotely.com/remote-jobs/search?term={term}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    article = soup.find('article')
    features = article.find_all('li')
    wwr_list = []
    for feature in features:
        try:
            title = feature.find('span', {'class': 'title'}).string
            company = feature.find('span', {'class': 'company'}).string
            link = feature.find_all('a')
            if len(link) > 1:
                link = link[1]['href']
            else:
                link = link[0]['href']
            link = f'https://weworkremotely.com/{link}'
            wwr_list.append({'title': title, 'link': link, 'company': company})
        except:
            pass
    return wwr_list

def ro_scrapper(term):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    url = f'https://remoteok.io/remote-{term}-jobs'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    jobs = soup.find_all('tr', {'class': 'job'})
    ro_list = []
    for job in jobs:
        title = job.find('h2').string
        link = job.find('a', {'class': 'preventLink'})['href']
        link = f'https://remoteok.io{link}'
        company = job.find('h3').string
        ro_list.append({'title': title, 'link': link, 'company': company})
    print(ro_list)
    return ro_list