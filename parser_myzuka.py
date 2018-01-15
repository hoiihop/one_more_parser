import os
import requests
from bs4 import BeautifulSoup

HEADER = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}


def set_session():
    # create session for use keep-alive
    return requests.Session()


def set_connection(link, count, session):
    # create connection to url, create object BeautifulSoap
    link_temp = link + str(count) + "/"
    url = session.get(link_temp, headers=HEADER)
    code = url.status_code
    if code == 200:
        real_url = url.url
        soap = BeautifulSoup(url.text, 'lxml')
        return [real_url, soap]
    else:
        return [link_temp, code]


def download_file(session, dparams, path):
    # download audio file and set name
    # NOTE the stream=True parameter
    params = dparams[0]
    filename = os.path.normpath(path + '/' + dparams[1])
    url = dparams[2]
    proxies = {'http': 'http://61.5.207.102:80',
               'https': 'http://61.5.207.102:80'}
    download_url = session.get(url, params=params, headers=HEADER, stream=True)
    download_url1 = requests.get(download_url.url, proxies=proxies, headers=HEADER)
    print(download_url1)
    print(len(download_url1.content))
    with open(filename, 'wb') as f:
        for chunk in download_url1.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    return filename


def spyder(conn, db, count):
    # parse html and get all interest data
    res = []
    link = conn[0]
    soap = conn[1]
    k = soap.h1.get_text().split(' - ')
    artist = k[0].strip()
    song = k[1].strip()
    download_link = soap.select("div.top a.dl")
    for j in download_link:
        download_link = link[:link.find('Song') - 1] + j['href']

    if download_link:
        res.append(count)
        res.append(link)
        res.append(artist)
        res.append(song)
        db.insert(res)

        local_filename = artist + ' - ' + song + '.mp3'
        param_temp = download_link[download_link.find('?') + 1:].split('&')
        params = {}
        for i in param_temp:
            temp = i.split('=')
            params[temp[0]] = temp[1]

        return [params, local_filename, download_link]
    else:
        return False
