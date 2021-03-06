'''
在网上爬取的原始数据
从http://www.essentialgene.org/ 下载所有的关键蛋白信息
从https://www.ncbi.nlm.nih.gov/ 查找不同标准的生物的ID对应关系，存储于单独的文件夹
从https://string-db.org/ 下载所有相关生物的蛋白质相互作用信息，按照生物ID分类存储
从https://www.uniprot.org/ 查找所有相关的蛋白质注释信息，按照生物ID分类存储
需要重新写
'''
import gzip
import os
import random
import shutil
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

import global_config


def make_dir(director):
    director = director[:-1] if director[-1] == '/' else director
    if os.path.exists(director):
        shutil.rmtree(director)
    os.mkdir(director)


def internet_environment():  # 准备好爬取数据的网络环境
    uagent = UserAgent()
    chrome_uagent = uagent.data_browsers['chrome']
    headers = {'User-Agent': random.choice(chrome_uagent)}
    internet_env = dict()
    internet_env['headers'] = headers
    return internet_env


def main():
    print('Making directors and downloading......')
    make_dir(global_config.DATA_ROOT)
    path_list = global_config.PATH_LIST
    download_deg_files(path=path_list['DEG'])
    download_string_files(path=path_list['STRING'])
    download_uniport_files(string_path=path_list['STRING'], uniport_path=path_list['UNIPROT'])
    print('Origin data is ready!')


def download_deg_files(path):
    make_dir(path)
    reaponse = requests.get('http://origin.tubic.org/deg/public/index.php/download')
    soup = BeautifulSoup(reaponse.text, features='lxml')
    links = soup.find('table').find_all('a')
    for index, link in enumerate(links[:3]):  # deg-p-15.2.zip,deg-p-15.2.zip,deg-e-15.2.zip
        down_link = 'http://origin.tubic.org'+link.attrs['href']
        down_name = global_config.DEG_BIO_CLASS[index]+'.zip'
        down_path = os.path.join(path, down_name)
        print('To download deg %s ...... ' % down_path, end='')
        down_file = requests.get(down_link)
        with open(down_path, 'wb') as file:
            file.write(down_file.content)
            time.sleep(60)
        print('Done!')


def download_string_files(path):
    make_dir(path)
    taxon_name_id_list = list(global_config.ID_MAP[name] for name in global_config.ID_MAP)
    taxon_id_set = set()
    for name_id in taxon_name_id_list:
        if not name_id[1] in taxon_id_set:
            taxon_id_set.add(name_id[1])
            down_path = os.path.join(path, name_id[0])
            download_string_file(down_path, name_id[1])


def download_string_file(path, taxon_id):
    make_dir(path)
    download_url = 'https://string-db.org/cgi/download.pl'+'?species_text=%s' % taxon_id
    reaponse = requests.get(download_url)
    soup = BeautifulSoup(reaponse.text, features='lxml')
    links = soup.find_all('div', {'class': 'download_table_data_row'})
    links_selected = list((links[3], links[6], links[7]))  # protein.actions.v11.0.txt.gz,protein.info.v11.0.txt.gz,protein.sequences.v11.0.fa.gz
    for index, link in enumerate(links_selected):
        down_link = link.find('a').attrs['href']
        down_name = global_config.STRING_FILES[index]+'.txt.gz'
        down_path = os.path.join(path, down_name)
        down_env = internet_environment()
        print('To download string %s ...... ' % down_path, end='')
        down_file = requests.get(down_link, headers=down_env['headers'])
        with open(down_path, 'wb') as file:
            file.write(down_file.content)
            time.sleep(60)
        print('Done!')


def download_uniport_files(string_path, uniport_path):
    make_dir(uniport_path)
    string_organ_list = os.listdir(string_path)
    for string_organ in string_or  gan_list:
        gz_file_path = os.path.join(string_path, string_organ, global_config.STRING_FILES[1]+'.txt.gz')
        protein_id_list = list()
        with gzip.open(gz_file_path, 'r') as file:
            next(file)
            for row in file:
                row_split = str(row, encoding='utf-8').split('\t')
                protein_id_list.append(row_split[0])
        down_path = os.path.join(uniport_path, string_organ)
        print('To download uniprot %s ...... ' % down_path, end='')
        download_uniport_file(down_path, protein_id_list)
        print('Done!')


def download_uniport_file(down_path, protein_id_list):
    make_dir(down_path)
    # 存储所有需要的蛋白质id
    temp_file_path = os.path.join(down_path, 'protein_id_list.txt')
    with open(temp_file_path, 'w', encoding='utf-8') as file:
        for protein_id in protein_id_list:
            file.write(protein_id+'\n')
    # 打开并设置浏览器
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.path.abspath(down_path)}
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 不弹出log信息
    options.add_argument('--headless')  # 隐身执行
    driver = webdriver.Chrome(executable_path=global_config.PATH_LIST['driver'], options=options)
    time.sleep(5)
    # 获取查询的下载链接
    driver.get('https://www.uniprot.org/uploadlists/')
    driver.find_element_by_class_name('privacy-panel__button').click()
    select = webdriver.support.select.Select(driver.find_element_by_id('from-database'))
    select.select_by_value('STRING_ID')
    driver.find_element_by_id('uploadfile').send_keys(os.path.abspath(temp_file_path))
    driver.find_element_by_id('upload-submit').click()
    uniprot_list = driver.find_element_by_id('query').get_attribute('value')
    uniprot_id = uniprot_list.replace('yourlist:', '')
    # 通过url控制需要下载的数据
    final_url = 'https://www.uniprot.org/uniprot/?query=yourlist:%s&sort=yourlist:%s&columns=yourlist(%s)' % (uniprot_id, uniprot_id, uniprot_id) + \
        ',id,entry%20name,protein%20names,genes,organism,length,features,go-id'  # 初步使用的特征
    # 开始下载
    driver.get(final_url)
    driver.find_element_by_id('download-button').click()
    time.sleep(5)
    select = webdriver.support.select.Select(driver.find_element_by_id('format'))
    select.select_by_value('tab')
    driver.find_element_by_id('menu-go').click()  # 下载文件
    time.sleep(5)
    # 改名
    file_name = 'uniprot-yourlist_%s.tab.gz' % uniprot_id
    while file_name not in os.listdir(down_path):
        time.sleep(1)
    os.rename(os.path.join(down_path, file_name), os.path.join(down_path, 'protein_feature.txt.gz'))
    driver.quit()


if __name__ == '__main__':
    main()
