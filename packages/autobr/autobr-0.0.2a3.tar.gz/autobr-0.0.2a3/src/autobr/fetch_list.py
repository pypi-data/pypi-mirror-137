from autobr.baidu import BaiduNewsSearch
import os
import time
from quickcsv.file import *
from carbon2.analysis.similarity import analyze_similar_document_pairs
import quickcsv.file as qc

def search_data_and_download(root_folder="data", groupby="countries", keywords="carbon2",
                             driver_path="../browsers/chromedriver.exe",
                             max_search_page=100,
                             top_keywords_num=5
                             ):
    country_keywords = [w.strip() for w in
                        open(f'{root_folder}/keywords/{groupby}.csv', 'r', encoding='utf-8').readlines() if
                        w.strip() != ""]

    carbon2_keywords = [w.strip() for w in
                        open(f'{root_folder}/keywords/{keywords}.csv', 'r', encoding='utf-8').readlines() if
                        w.strip() != ""]

    print(country_keywords)
    print(carbon2_keywords)

    baidu_news = BaiduNewsSearch(
        webdriver_path=driver_path,
    )

    # max_search_page = 100
    # top_keywords_num = 5


    for country in country_keywords:
        for keyword in carbon2_keywords[:top_keywords_num]:
            search_keyword = f"{country} {keyword}"
            print(country)
            print(f"Searching news.baidu.com with the keywords \"{search_keyword}\"...")
            try:
                country_path = f"{root_folder}/results/{groupby}/{country}"
                if not os.path.exists(country_path):
                    os.mkdir(country_path)
                filename = time.strftime("%Y%m%d%H%M%S", time.localtime())
                saved_path = f"{country_path}/{filename}.csv"
                baidu_news.fetch(raw_keywords=search_keyword, max_pages=max_search_page, silent=False,
                                 save_path=saved_path)
            except Exception as err:
                print(err)


def summarize_csv(root_path="data/search_results/country", output_path='list_country_news1.csv',
                  real_url_field='real_url', group_by_field='GroupBy', id_field="Id"):
    list_id = []

    list_result = []
    idx = 0
    for country in os.listdir(root_path):
        file_path = os.path.join(root_path, country)
        for file in os.listdir(file_path):
            csv_path = os.path.join(file_path, file)
            list_item = qc_read(csv_path)
            for item in list_item:
                real_url = item[real_url_field]
                if real_url not in list_id:
                    list_id.append(real_url)
                    item[group_by_field] = country
                    item[id_field] = idx
                    list_result.append(item)
                    idx += 1

    print("len = ", len(list_result))

    qc_write(output_path, list_result)


def get_similar(input_path="list_country_news2.csv", stopwords_path="data/stopwords/hit_stopwords.txt",
                analyze_field="title",
                save_path="list_country_news_similarity_report2.csv", similarity=0.7):
    analyze_similar_document_pairs(
        csv_path=input_path,  # 这是系统导出数据产生的csv格式文件
        stopwords_path=stopwords_path,  # 用于清除停用词
        analyze_field=analyze_field,  # 相似度分析的csv字段，标题为Title，或者如果csv文件某一列是正文，也可以是正文的列名
        save_similar_result_path=save_path,  # 相似度分析的保存结果，每一行为一对文档的标题。
        need_similarity=True,  # 在输出的文件中包含相似度这一列
        minimum_similarity=similarity  # need_similarity==True情况下，只保存相似度大于minimum_similarity的文档对，取值在[0,1]
    )


def remove_similar(similarity_report_path="",
                   input_csv_path='',
                   output_path=''
                   ):
    list_sim = qc.quick_read_csv_model(csv_path=similarity_report_path)
    dict_sim = {}
    for item in list_sim:
        id1 = item['Id1']
        id2 = item['Id2']
        if id1 in dict_sim.keys():
            if id2 not in dict_sim[id1]:
                dict_sim[id1].append(id2)
        else:
            dict_sim[id1] = [id2]
        if id2 in dict_sim.keys():
            if id1 not in dict_sim[id2]:
                dict_sim[id2].append(id1)
        else:
            dict_sim[id2] = [id1]

    list_g20_news_merge3 = qc.quick_read_csv_model(csv_path=input_csv_path)

    list_ids = []
    list_result = []

    def exists_pair(id1, id2):
        if id1 in dict_sim.keys():
            if id2 in dict_sim[id1]:
                return True
        if id2 in dict_sim.keys():
            if id1 in dict_sim[id2]:
                return True
        return False

    def exists_pair_in_list(id1, list_ids):
        for id2 in list_ids:
            flag = exists_pair(id1, id2)
            if flag == True:
                return True
        return False

    N = len(list_g20_news_merge3)

    for idx, item in enumerate(list_g20_news_merge3):
        id = item['Id']
        print(f"{idx + 1}/{N}")
        if not exists_pair_in_list(id, list_ids):
            list_result.append(item)
            list_ids.append(id)
        print()

    qc.qc_write(output_path, list_result)


def auto_search_download(
        root_path="test_method",
        groupby='countries',
        keywords="carbon2",
        max_search_page=2,
        top_keywords_num=2,
        driver_path='../browsers/chromedriver.exe'
):
    result_folder = f'{root_path}/results'
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    result_groupby_folder = f'{result_folder}/{groupby}'
    if not os.path.exists(result_groupby_folder):
        os.mkdir(result_groupby_folder)

    search_data_and_download(
        root_folder=root_path,
        groupby=groupby,
        keywords=keywords,
        driver_path=driver_path,
        max_search_page=max_search_page,
        top_keywords_num=top_keywords_num
    )

    summarize_csv(
        root_path=result_groupby_folder,
        output_path=f'{root_path}/results/list_news.csv',
        group_by_field=groupby
    )
    get_similar(
        input_path=f'{root_path}/results/list_news.csv',
        similarity=0.7,
        save_path=f'{root_path}/results/similarity_report.csv',
        # stopwords_path=f'{root_path}/stopwords/stopwords',
        stopwords_path='',
        analyze_field='title'
    )
    remove_similar(
        similarity_report_path=f'{root_path}/results/similarity_report.csv',
        input_csv_path=f'{root_path}/results/list_news.csv',
        output_path=f'{root_path}/results/list_news_without_similar.csv',
    )
    print("output: ", f'{root_path}/results/list_news_without_similar.csv')
