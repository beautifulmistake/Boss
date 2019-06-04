import json

with open(r'G:\工作\招聘网站爬虫\Boss\util\Boss.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(r'G:\工作\招聘网站爬虫\Boss\util\Boss_result.txt', 'w+', encoding='utf-8') as ff:
    ff.write('search_key\tcompany_name\tcompany_type\tcompany_size\tis_listed\n')
    for line in lines:
        line_ = json.loads(line, encoding='utf-8')
        # 搜索关键字
        search_key = line_.get("search_key")
        # 公司名称
        company_name = line_.get("company_name")
        # 公司信息
        info = line_.get("info")
        if len(info) == 2:
            # 公司类型
            company_type = info.get("company_size")
            # 公司规模
            company_size = info.get("is_listed")
            # 是否上市
            is_listed = "无信息"
            # 将信息写入文件
            ff.write('%s\t%s\t%s\t%s\t%s\n' % (search_key, company_name, company_type, company_size, is_listed))
        if len(info) == 3:
            # 公司类型
            company_type = info.get("company_type")
            # 公司规模
            company_size = info.get("company_size")
            # 是否上市
            is_listed = info.get("is_listed")
            # 将信息写入文件
            ff.write('%s\t%s\t%s\t%s\t%s\n' % (search_key, company_name, company_type, company_size, is_listed))
    print("OK")
