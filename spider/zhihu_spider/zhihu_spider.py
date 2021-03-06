import requests
import re
import os
import time
import csv
from queue import Queue

# key是图片的url路径, value是图片所属的问题id（哪一个问题下的图片）
image_url_dict = {}

img_tag = re.compile(r"""<img\s.*?\s?data-original\s*=\s*['|"]?([^\s'"]+).*?>""", re.I)

question_id_dict = {'292901966': '有着一双大长腿是什么感觉',
                    '26297181': '大胸女生如何穿衣搭配',
                    '274143680': '男生会主动搭讪一个长得很高并且长得好看的女生吗',
                    '266695575': '当你有一双好看的腿之后会不会觉得差一张好看的脸',
                    '297715922': '有一副令人羡慕的好身材是怎样的体验',
                    '26037846': '身材好是一种怎样的体验',
                    '28997505': '有个漂亮女朋友是什么体验',
                    '29815334': '女生腿长是什么感觉',
                    '35255031': '你的身材不配你的脸是一种怎样的体验',
                    '274638737': '大胸妹子夏季如何穿搭',
                    '264568089': '你坚持健身的理由是什么现在身材怎么样敢不敢发一张照片来看看',
                    '49075464': '在知乎上爆照是一种什么样的体验',
                    '22918070': '女生如何健身练出好身材',
                    '56378769': '女生身高170cm以上是什么样的体验',
                    '22132862': '女生如何选购适合自己的泳装',
                    '46936305': '为什么包臀裙大部分人穿都不好看',
                    '266354731': '被人关注胸部是种怎样的体验',
                    '51863354': '你觉得自己身体哪个部位最漂亮',
                    '66313867': '身为真正的素颜美女是种怎样的体验',
                    '34243513': '你见过最漂亮的女生长什么样',
                    '21052148': '有哪些评价女性身材好的标准',
                    '52308383': '在校女学生如何才能穿搭得低调又时尚',
                    '50426133': '平常人可以漂亮到什么程度',
                    '268395554': '你最照骗的一张照片是什么样子',
                    '277593543': '什么时候下定决心一定要瘦的',
                    '277242822': '室友认为我的穿着很轻浮我该如何回应',
                    '36523379': '穿和服是怎样的体验'
                    }


def to_csv(image_url_dict):
    with open('image_urls.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for k, v in image_url_dict.items():
            writer.writerow([k, v])


def get_pic_urls():
    for question_id in question_id_dict.keys():

        headers = {
            'referer': 'https://www.zhihu.com/question/' + question_id,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'cookie': ''
        }

        for i in range(0, 500, 5):
            try:
                url = 'https://www.zhihu.com/api/v4/questions/'+question_id+'/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset='+str(i)+'&platform=desktop&sort_by=default'

                res = requests.get(url, headers=headers)
                #     print(res.status_code)
                if res.status_code == 200:
                    data = res.json()
                    if not data['data']:
                        print('没有数据！(%s)' % url)
                        break
                    for answer in data['data']:
                        content = answer.get('content', '')
                        if content:
                            #         print(content)
                            image_url_list = img_tag.findall(content)

                            for image_url in image_url_list:
                                print('图片url: %s, 问题id: %s' % (image_url, question_id))
                                image_url_dict[image_url] = question_id
                else:
                    print('返回值: %s, url: %s' % (res.status_code, url))
                # 防止访问频繁
                time.sleep(1.1)
            except Exception as e:
                print('请求出错, (%s)' % e)
                time.sleep(1.1)
                continue


def main():
    get_pic_urls()

    to_csv(image_url_dict)


if __name__ == '__main__':
    main()