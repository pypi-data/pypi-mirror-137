from carbon2.api.submit_list import *

def extract_text(html_str):
    content = bare_extraction(html_str)
    if content == None:
        return ""
    return content['text']

def extract_content(html_str):
    content = bare_extraction(html_str)
    return content

def download_html_data(
    input_csv_file = "data/list_urls.csv",
    save_folder = "data/html_data",
    output_csv_file="data/list_news.csv"
):
    server_url = ""
    user_id = ""
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    list_result=submit_page_list(server_url, user_id, input_csv_file, save_html_folder=save_folder, use_md5url_as_id=True,
                     #  driver_path="browsers/chromedriver.exe",
                     tag="auto", language="zh", try_raise_error=False,no_submit=True,no_submit_file=True,not_check_exists=True)
    print("list_result = ",list_result)
    qc_write(output_csv_file,list_result)

def fetch_raw_text(
        input_csv_path='data/list_country_news_plus.csv',
        output_html_folder='data/html_data',
        output_text_folder='data/text_data',
        output_csv_path='data/list_g20_news_plus_text.csv'
):

    if not os.path.exists(output_text_folder):
        os.mkdir(output_text_folder)

    list_g20_news = qc.quick_read_csv_model(csv_path=input_csv_path)

    list_item_new = []

    N = len(list_g20_news)

    for idx, item in enumerate(list_g20_news):
        print(f'{idx + 1}/{N}')
        file_id = item["FileId"]
        filepath = f'{output_html_folder}/{file_id}.txt'
        full_text = ""
        if not os.path.exists(filepath):
            continue
        content=extract_content(open(filepath, 'r', encoding='utf-8').read())
        if content==None:
            continue
        full_text = content["text"]
        f_out = open(f"{output_text_folder}/{file_id}.txt", "w", encoding='utf-8')
        f_out.write(full_text)
        f_out.close()
        # item["Text"]=full_text.replace("\n","").replace("\"","'").strip()
            # add additional fields

        item['PublishTime'] = content['date']
        item['HostName'] = content['hostname']
        item['Publisher'] = content['author']

        list_item_new.append(item)
        print(full_text)
        print()

    qc.qc_write(output_csv_path, list_item_new)

from quickcsv.file import *

def add_additional_info(
        input_origin_url_csv_path="",
        input_meta_csv_path="",
        add_field="country",
        output_csv_path=""

):
    list_item = qc_read(input_origin_url_csv_path)
    dict_url_country = {}
    dict_country = {}
    for item in list_item:
        if not item[add_field] in dict_url_country.keys():
            dict_url_country[item["real_url"]] = item[add_field]
        if not item[add_field] in dict_country.keys():
            dict_country[item[add_field]] = 1
        else:
            dict_country[item[add_field]] += 1
    print()
    for country in dict_country.keys():
        print(f"{country}\t{dict_country[country]}")

    count = 0
    list_news = qc_read(input_meta_csv_path)
    list_result = []
    for news in list_news:
        url = news["Url"]
        if url in dict_url_country:
            country = dict_url_country[url]
            news["Tag"] = country
            list_result.append(news)

    qc_write(output_csv_path, list_result)

    print("exist count = ", count)

import quickcsv.file as qc
from trafilatura import bare_extraction
import os
from nerkit.StanzaApi import StanzaWrapper

def get_important_text(
        input_keywords_paths=None,
        input_csv_added="",
        input_text_folder='',
        output_text_processed_folder='',
        output_csv_file=''
):

    sw = StanzaWrapper()
    all_keywords=[]
    for path in input_keywords_paths:
        keywords = [w.strip() for w in open(path, 'r', encoding='utf-8').readlines()
                        if w.strip() != ""]
        all_keywords+=keywords

    list_g20_news = qc.quick_read_csv_model(csv_path=input_csv_added)

    list_item_new = []

    N = len(list_g20_news)

    if not os.path.exists(output_text_processed_folder):
        os.mkdir(output_text_processed_folder)

    for idx, item in enumerate(list_g20_news):
        print(f'{idx + 1}/{N}')
        # print(item)
        file_id = item["FileId"]
        save_text_path = f"{input_text_folder}/{file_id}.txt"
        if not os.path.exists(save_text_path):
            continue
        text = open(save_text_path, 'r', encoding='utf-8').read()
        # print(text)
        if text == '':
            continue
        list_sentence = sw.tokenize_sentence(text, lang='zh')
        list_sentence_useful = []
        for sentence in list_sentence:
            # print(sentence)
            if len(sentence) < 30:
                continue
            sentence = sentence.strip()
            sub_sentences = sentence.split("\n")
            for sub_sentence in sub_sentences:
                sub_sentence = sub_sentence.strip()
                if len(sub_sentence) <= 20:
                    continue

                has_found_keywords = False
                for k in all_keywords:
                    if k in sub_sentence:
                        has_found_keywords = True
                        break
                if has_found_keywords:
                    print(sub_sentence)
                    list_sentence_useful.append(sub_sentence)

        if len(list_sentence_useful) != 0:
            new_text = '\n'.join(list_sentence_useful)
            processed_text_path = f"{output_text_processed_folder}/{file_id}.txt"
            f_out = open(processed_text_path, 'w', encoding='utf-8')
            f_out.write(new_text)
            f_out.close()
            list_item_new.append(item)

    qc.qc_write(output_csv_file, list_item_new)

def fetch_and_preprocess_pipeline(
    input_urls_path = 'data/list_urls.csv',
    keywords_path = 'data/keywords'
):

    download_html_data(input_csv_file=input_urls_path, output_csv_file='data/list_news.csv')

    fetch_raw_text(input_csv_path='data/list_news.csv', output_csv_path='data/list_news_meta.csv')

    add_additional_info(
        add_field='countries',
        input_origin_url_csv_path="data/list_urls.csv",
        input_meta_csv_path="data/list_news_meta.csv",
        output_csv_path="data/list_news_added.csv"
    )

    kp = []
    for file in os.listdir(keywords_path):
        kp.append(os.path.join(keywords_path, file))

    get_important_text(
        input_keywords_paths=kp,
        input_text_folder='data/text_data',
        input_csv_added='data/list_news_added.csv',
        output_csv_file='data/list_news_useful.csv',
        output_text_processed_folder='data/text_data_processed'
    )

if __name__=="__main__":
    fetch_and_preprocess_pipeline()





