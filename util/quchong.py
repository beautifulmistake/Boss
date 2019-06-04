# 读取record/Boss.json文件，将所有记录的公司写入文件
import json

# with open(r'G:\工作\招聘网站爬虫\Boss\Boss\record\Boss.json', 'r', encoding='utf-8') as f:
#     datas = json.loads(f.read())
#
# with open(r'G:\工作\招聘网站爬虫\Boss\Boss\record\have_result.txt', 'w+', encoding='utf-8') as ff:
#     for data in datas:
#         if data.get("result") == "True":
#             # 获取所有公司名称
#             search_key = data.get("search_key")
#             ff.write(search_key)
#             ff.write("\n")
#     print("OK")

# with open(r'G:\工作\招聘网站爬虫\Boss\Boss\record\Boss.json', 'r', encoding='utf-8') as f:
#     datas = json.loads(f.read())
#
# with open(r'G:\工作\招聘网站爬虫\Boss\Boss\record\have_search.txt', 'w+', encoding='utf-8') as ff:
#     for data in datas:
#         # 获取所有公司名称
#         search_key = data.get("search_key")
#         ff.write(search_key)
#         ff.write("\n")
#     print("OK")

# 读取result/boss.json文件，将有结果的公司写入文件
# with open(r'G:\工作\招聘网站爬虫\Boss\Boss\result\Boss.json', 'r', encoding='utf-8') as f:
#     datas = f.readlines()
#
# with open(r'G:\工作\招聘网站爬虫\Boss\Boss\result\have.txt', 'w+', encoding='utf-8') as ff:
#     for data in datas:
#         print(data)
#         data = json.loads(data.strip())
#         # 公司名成
#         comany = data.get('company_name')
#         ff.write(comany)
#         ff.write("\n")
