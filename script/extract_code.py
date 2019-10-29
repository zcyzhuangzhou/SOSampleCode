from db.model import Post, PostHtmlText
from definitions import OUTPUT_DIR, MYSQL_FACTORY, QUALIFIED_NAME_DIR
from bs4 import BeautifulSoup
import json


# 抽取SO中的样例代码
def extract_code(qualified_names):
    # 连接MySQL数据库
    session = MYSQL_FACTORY.create_mysql_session_by_server_name(server_name="89RootServer",
                                                                database="stackoverflow",
                                                                echo=False)
    # 查询并返回所需要的帖子
    posts = session.query(PostHtmlText.Body_AcceptedAnswer).all()

    htmls = set()

    # json文件保存
    save_file = []
    save_path = "SOSampleCode.json"

    # 将帖子中的所需字段加载到内存
    for post in posts:
        for item in post:
            htmls.add(item)

    for html in htmls:
        # 解析question的HTML文本
        soup_html = BeautifulSoup(html, 'lxml')
        # 找到所有<pre><code>……</pre></code>标签的内容
        pre_codes = soup_html.findAll("pre")

        if not pre_codes:
            continue
        else:
            # 用所有的API全限定名来遍历所有的<pre><code>……</pre></code>标签内容
            for pre_code in pre_codes:
                for qualified_name in qualified_names:
                    if qualified_name in pre_code.get_text():
                        API = qualified_name
                        Code = pre_code.get_text()
                        print(API)
                        # 获取样例代码上下文各一段文本描述
                        if not pre_code.find_previous_sibling():
                            pre_description = ''
                        else:
                            pre_description = pre_code.find_previous_sibling().get_text()
                        if not pre_code.find_next_sibling():
                            next_description = ''
                        else:
                            next_description = pre_code.find_next_sibling().get_text()
                        Description = pre_description + ' ' + next_description

                        # 将全限定名，样例代码，文本描述保存
                        json_save = {}
                        json_save['API'] = API
                        json_save['Code'] = Code
                        json_save['Description'] = Description
                        save_file.append(json_save)

    with open(OUTPUT_DIR + '/' + save_path, 'w', encoding='utf-8') as json_file:
        json.dump(save_file, json_file, indent=4)


if __name__ == '__main__':
    # 读取API全限定名，并加载在内存中
    qualified_names = set()
    with open(QUALIFIED_NAME_DIR) as f:
        api_names = json.load(f)
        for api_name in api_names:
            qualified_names.add(api_name['qualified_name'])

    extract_code(qualified_names)
    f.close()
