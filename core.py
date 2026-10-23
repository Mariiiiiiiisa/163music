import re
import sys
import json
from http.cookies import SimpleCookie

import logging
import requests
import execjs
from bs4 import BeautifulSoup

from mutagen.mp4 import MP4, MP4Cover

logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s: %(message)s')

c = 'P_INFO=wu738684554@163.com|1782103282|0|mail163|00&99|null&null&null#CN&null#10#0#0|&0|mail163_qrcode|wu738684554@163.com; _iuqxldmzr_=32; NMTID=00OtSmWJSWC7d6FXURpn0atOpTL_3gAAAGgqrYXBg; WEVNSM=1.0.0; WNMCID=utkfba.1789570455796.01.0; WM_TID=5SrHsln1XMFFFFAERVfYQZ2djyxWri%2Fh; ntes_utid=tid._.5mF1fL0PcuBBAxFRVQbdEJiJjnwJUPUd._.0; sDeviceId=YD-nXd3nNjKG0FFVwQEUQLcBNjNizwdVOBY; __snaker__id=O6BHEVKeQZRPckNd; gdxidpyhxdE=cP1Y5wE5t6kDMSmWR9imUt4gsPKt0XkqykJPTYEJD%5CNQLehzprEX4t25fiUYrnvcZaEB%2FCfs%2FyPaJMoQh0zmU%2FJRm04r5ya%5CpdDrOzlJVQOAGEmpTuC1CneKgshc4Vz12%2B7lNYYeJ0apARUbhk9%5CwALfQaTsImIOGeGX8k7adE%5CQ2iW6%3A1792401554464; MUSIC_U=00C8F91DBA9F808D8CD3AA8AB2A7595F341CBEA7F2232B9446E7C2CD9A0A5A04C05F90D57AB682714451517379AC39E3B27A41C45AC5E49459358E5291654EBC56CA2E6B2BABEC0650ED77772EE21A4C567C0D2695B48EE35E4E9593F4321BA349AADDB5D9BFDC08776ACF3ADB4296A63137EA3EDA20A66510AD864096EA14435844E8500AA70A681412ED5BC9B3B25D4F54E91240DE12D349D24F433F4CC52EB497A9AA9DE80DE870DE4BBE68A1E2F31E99EB422BBF60E1E7EE0DB9D860195CC5744A0C8E74298980333D3DAB4715962CF18FB0A43298E427E7A109D6282CD933EB0F770978DD517C210384AB9D1BE878095C49A0F03BDF1C98082005E4E43BF940B4994CA3B53197093B5905F5FE363F1CF3EF9C95FAE02C3BA3A796595E64D98F7A899355A8850E19A97F8067CBD091036EADF0A1CFB3D3F36B1E86BA0C0B29CB5381B247DED660FC673B4DE0118E5F5F0F0940EDB90499CB23D5AC60FEBD1B8B6EBDA8A20EB89FE403D47B02F26D4435333556B79436A97E42CD69CC1217303BE5BF8E019F332E4D6F7DE4C2CD7D8F; __csrf=2fce96444837fea541f718efb03eb0b8; ntes_kaola_ad=1; WM_NI=fb54wlxB34A3PI1KZPM6RA2NgD7O887wpJfthYGHXG%2FfpoYQl2aUXhCo9Z8Rno2EkzqnjbROWXg28k8IebtIJc9EAdfVo5KBAsGlTLGMj0Sxi2xIgqllxN75XbTNbGwVUHQ%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb3bc7caab28dbadc3e93eb8fb6c84e979a9b82cd4af1959eb8e55c94bf9aaef22af0fea7c3b92aa6befbd5f668bc9efdd5c4399497ffacd95c8fea9ea2b146a59cf9b0bb34f5a9c0abe580ac8789a9db4dedbac090dc5bb0eeafb6db6481b1f7bbbb5aaeb1fea6ea72b3b2a683d1459588a9d3bb61fc97ab83f7438abdf7a6c470a68aa1d6ca4a83ad898dd7488593a6d1d274abeeb8aae67bb0b4b8afb63f9cbe9cafe14db58a9ba9d437e2a3; JSESSIONID-WYYY=1xAYaExnP3vdA%2FgpQzygsa6J42Wyry50Nz6OkI7F%2FnHUmaPaxHdpUf%2BHgiNhNwhDB7JuZxRnh2lj30nRvi%5CmbNN7Y3b%2BdfIHZ05PPAuDnfTDwq7NdC0k8rERU3zD7rHtRbYRbcgIGnFeQ2qUcTHygQn05CWngh1H55cBoF08oz%2FH3%5Cjk%3A1792484919209; playerid=64513132'

input_url = input("请输入音轨链接: ")

with open('F:\\vscode\code\\163music\\get_data.js', 'r', encoding='utf-8') as file:
    getData = file.read()


class Spider:
    def __init__(self, track_id, cookies):
        self.track_api = "https://music.163.com/weapi/song/enhance/player/url/v1"
        self.track_id = track_id
        self.track_url = f"https://music.163.com/song?id={track_id}"
        self.cookies = cookies
        self.headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://music.163.com/',
    'sec-ch-ua': '"Google Chrome";v="155", "Chromium";v="155", "Not(A:Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36',
    'cookie': self.cookies
}
        self.params = dict()
        self.dataFc = execjs.compile(getData)
        self.raw_data = self.dataFc.call('d', self.get_auth())
        self.data = {"params": self.raw_data['encText'], 'encSecKey': self.raw_data['encSecKey']}
        self.path = 'F://music//{}'

    def get_message(self):
        logging.info('开始获取音轨信息')
        try:
            response = requests.get(self.track_url, headers=self.headers)
            response.raise_for_status()
            html = response.text
            return html
        except Exception:
            raise logging.info('获取音轨信息过程出现异常', exc_info=True)

    def get_url(self):
        logging.info('开始获取音轨地址')
        try:
            response = requests.post(self.track_api, params=self.params, headers=self.headers, data=self.data)
            response.raise_for_status()
            result = response.json()
            return result
        except Exception:
            raise logging.info('获取音轨地址过程中出现异常', exc_info=True)

    def get_auth(self):
        logging.info('开始获取认证')

        auth_dic = {}
        cookie = SimpleCookie()
        cookie.load(self.cookies)
        csrf = cookie["__csrf"].value
        auth_dic["csrf_token"] = csrf
        self.params["csrf_token"] = csrf

        auth_dic["ids"] = f"[{self.track_id}]"
        auth_dic["level"] = "exhigh"
        auth_dic["encodeType"] = "aac"

        json_str = json.dumps(auth_dic, ensure_ascii=False)

        return json_str

    def track_download(self, track_data):
        logging.info('开始下载音轨')
        url = track_data['url']
        track_title = track_data['title']
        track_type = track_data['type']
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            track_path = self.path.format(f'{track_title}.{track_type}')
            with open(track_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            logging.info('音频下载完成')
            insert_tag(track_data, track_path)
        except Exception:
            raise logging.info('下载失败', exc_info=True)


def insert_tag(track_data, track_path):
    audio = MP4(track_path)
    cover = requests.get(track_data['cover']).content

    audio["©nam"] = track_data['title']
    audio["©ART"] = track_data['artist']
    audio["©alb"] = track_data['album']
    audio["©cmt"] = track_data['description']
    audio["covr"] = [
        MP4Cover(
            cover, imageformat=MP4Cover.FORMAT_JPEG
        )
    ]
    audio.save()


def get_id(url: str) -> str | None:
    m = re.search(r'(?:song\?id=|/song/|id=)(\d+)', url)
    return m.group(1) if m else None


def parse_message(html):
    logging.info('开始解析页面')
    keys = {
        "og:title": "title",
        "og:music:artist": "artist",
        "og:music:album": "album",
        "og:description": "description",
        "og:image": "cover"
    }
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    for prop, name in keys.items():
        tag = soup.select_one(f'meta[property="{prop}"]')
        if tag and tag.get("content"):
            data[name] = tag['content']
        else:
            logging.info('标签不存在')
    return data


def parse_url(result, track_data):
    logging.info('开始获取音轨地址')
    data = result['data'][0]
    track_data['url'] = data['url']  # 音频地址
    track_data['md5'] = data['md5']  # 音频MD5
    track_data['type'] = data['type']  # 音频格式

    return track_data


def main():
    track_id = get_id(input_url)

    spider = Spider(track_id=track_id, cookies=c)

    data = parse_message(spider.get_message())
    track_data = parse_url(spider.get_url(), track_data=data)

    spider.track_download(track_data)


if __name__ == '__main__':
    main()