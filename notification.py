import re
import json
import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from upload import *

def notification(text, img_url):
    with open('data/notify_list.json', 'r') as file:
        notify_list = json.load(file)
    if len(notify_list) == 0:
        return False
    image_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    # content = "{}\n{}".format(title, link)
    line_bot_api.multicast(notify_list, [TextSendMessage(text=text), image_message])
    # line_bot_api.multicast(notify_list, [TextSendMessage(text=content)])
    return True

def uploadIMGUR(path):
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    config = {
        'album': album_id,
        'name': 'test-name!',
        'title': 'test-title',
        'description': 'test-description'
    }
    print("Uploading image... ")
    image = client.upload_from_path(path, config=config, anon=False)
    print("Done")
    print(image['link'])
    return image['link']


yohao_url = 'https://scontent.ftpe7-2.fna.fbcdn.net/v/t1.0-9/28576166_1748347681893533_6351658010333230525_n.jpg?_nc_fx=ftpe7-4&_nc_cat=0&_nc_eui2=v1%3AAeFHaDuhp5n0HhT9DbON0-WUc4Q91ntXXxaDelXM_4TCBBLjRBpKUl2_arbUyB4e_wiZ5wf81A7BZfYXEumKyyAUEACegKWasah0nsHHAHSPFA&oh=b1d29557811ac8c7d5bf7ef265280afb&oe=5B746380'
line_bot_api = LineBotApi('jLNbvoD6ubW27XN0+qL/kYeJP81yvmoBP/QJEDXuzSLvhuP2Mwk4L25V3i/9RQy1HT8gjJ3kuYdXuRIj3J8MqdJj5LMkVps4NTSzyuo0+Ofmciso8c9WG3HHeZP14o8PaQhUcwimj3cNkb7fiaSWKAdB04t89/1O/w1cDnyilFU=')



if __name__ == '__main__':
	notification("入侵警報！！", yohao_url)
	