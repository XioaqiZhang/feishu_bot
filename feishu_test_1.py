import requests
import json
import argparse
import requests
from bs4 import BeautifulSoup
import re

class FeishuTalk:
    # 机器人webhook
    chatGPT_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/46b712b8-568a-4b2a-8f4e-a0c0f3bd508e'

    # 发送文本消息
    def sendTextmessage(self, content):
        url = self.chatGPT_url
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        payload_message = {
            "msg_type": "text",
            "content": {
    	# @ 单个用户 <at user_id="ou_xxx">名字</at>
                "text": content + "<at user_id=\"bf888888\">test</at>"  
                # @ 所有人 <at user_id="all">所有人</at>
                # "text": content + "<at user_id=\"all\">test</at>"
            }
        }
        response = requests.post(url=url, data=json.dumps(payload_message), headers=headers)
        return response.json
    
    # 发送富文本消息
    def sendFuTextmessage(self, content):
        url = self.chatGPT_url
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        payload_message = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "微博头条热榜",
                        "content": content
                    }
                }
            }
        }
        response = requests.post(url=url, data=json.dumps(payload_message), headers=headers)
        return response
	
	# 微博头条榜单
    def getHotBand(self):
        url = "https://www.weibo.com/ajax/statuses/hot_band"
        headers = {
            "cookie": "XSRF-TOKEN=iuIb9M_gQ8D4FjMwUthqcink; SUB=_2AkMUpJdaf8NxqwJRmPEVz2Pib4V_zwrEieKi-GaBJRMxHRl-yT92qhALtRB6PyS5tbPLRbsCo0gfSwhlb8PLq3CnqnuA; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFyRDSrne6a4e.bkQHJzd-.; WBPSESS=IawIaCISeX-46VmeRocrJ40RrQZ7YTNxKt6pB9xuTQ-WP-uhwIvsoHpBEQfU2CGlyGf32loDQLI6ykRbGvzNf_mvmCuvfYLwUPDbYHJizUdUKfKplkCi6sPas7wrz6ACVGt8HOr-w8hjNGpZtkeUtLcl0-BFnXMuSPDMToH7QlI=",
            "x-xsrf-token": "iuIb9M_gQ8D4FjMwUthqcink"
        }
        response = requests.get(url=url, headers=headers).json()
        bandList_all = []
        index = 1
        for item in response['data']['band_list']:
            bandDict = {"tag": "text"}
            bandList = []
            bandDict.update({"text": "No." + str(index) + "：" + item['word']})
            bandList.append(bandDict)
            index += 1
            bandList_all.append(bandList)
        return bandList_all

	
    def get_zhihu_hot(self):
        hot_list_dict = {}
        hot_list = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get('https://www.zhihu.com/billboard', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        html_text = soup.prettify()

        # Find the line that contains "hotList"
        hot_list_line = re.findall(r'"hotList":\s*\[.*?\]', html_text)

        if hot_list_line:
            # Extract the content after "hotList"
            hot_list_content = re.findall(r'\[.*?\]', hot_list_line[0])[0]

            # Convert the extracted content to JSON
            hot_list_json = json.loads(hot_list_content)
            # print(json.dumps(hot_list_json, indent=4))

            index = 1
            for item in hot_list_json:
                url   = item["target"]["link"]["url"]
                title = item["target"]["titleArea"]["text"]
                # print(item["target"]["link"]["url"])
                # print(item["target"]["titleArea"]["text"])

                hot_list_dict[title] = url

                bandDict = {"tag": "text"}
                bandList = []
                bandDict.update({"text": "No." + str(index) + "：" + title})
                bandList.append(bandDict)
                index += 1
                hot_list.append(bandList)
        # return hot_list_dict
        return hot_list



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", help="the content of the alert message")
    args = parser.parse_args()

    # TODO：实现卡片消息的发送

    # 发送富文本消息
    content = FeishuTalk().get_zhihu_hot()
    response = FeishuTalk().sendFuTextmessage(content)
    print(response)

    # content = FeishuTalk().getHotBand()
    # response = FeishuTalk().sendFuTextmessage(content)
    # print(response)

    # # 执行发送文本消息
    # content = "生活不止眼前的苟且，还有诗和远方!"
    # FeishuTalk().sendTextmessage(content)

    # 发送图片消息
    # picturePath = "E:\PythonCodes\FeishuTalk\picLibs\1.jpg"
    # FeishuTalk().uploadImage(picturePath)
