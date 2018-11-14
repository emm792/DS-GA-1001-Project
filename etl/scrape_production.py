"""
Scrapes USDA webiste for zip files containing honey production data.
Downloads zip files, eztracts them, and performs cleanup.
"""
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve, quote
from urllib.parse import urljoin
import shutil
import zipfile
import re
import os
import errno

data_folder = '../data/raw/honey_production'

URL = 'http://usda.mannlib.cornell.edu/MannUsda/viewDocumentInfo.do?documentID=1191'


def check_folder(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def save_zip(url, file_name):
    with urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        with zipfile.ZipFile(file_name) as zf:
            zf.extractall(os.path.dirname(file_name))

def clean_extracted_zip(folder, year):
    for filename in os.listdir(folder):
        if 'honey_prod' in filename:
            pass
        elif not 'all' in filename:
            os.remove(os.path.join(folder, filename))
        else:
            os.rename(os.path.join(folder, filename), os.path.join(folder, str(year) + '_honey_prod.csv'))


def main():
    check_folder(data_folder)
    u = urlopen(URL)
    with urlopen(URL) as u:
        html = u.read().decode('utf-8')

    soup = BeautifulSoup(html)

    data_section = soup.find(id='archived-docs')

    for link in data_section.find_all('a', href=True):
        link_url = link.get('href')
        if link_url.endswith('.zip'):
            year = re.split('-|\.', link_url)[-2]
            print('saving {} data'.format(year))
            save_zip(link_url, os.path.join(data_folder, year + '.zip'))
            clean_extracted_zip(data_folder, year)

if __name__ == "__main__":
    main()



