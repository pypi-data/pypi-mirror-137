from urllib import parse
import mimetypes
from knifes.constants import MediaType


def get_url_from_text(text):
    if not text:
        return text
    start_index = text.rfind('http://')
    if start_index == -1:
        start_index = text.rfind('https://')
    if start_index == -1:
        return None
    text = text[start_index:]
    end_index = text.find(' ')
    if end_index != -1:
        return text[0:end_index]
    return text


# m.oasis.weibo.cn => weibo
def get_domain_from_url(url):
    if not url:
        return url
    u = parse.urlparse(url)
    host_list = u.hostname.split('.')
    if len(host_list) < 2:
        return None
    return host_list[-2].lower()


# m.oasis.weibo.cn => oasis.weibo
def get_sub_domain_from_url(url):
    if not url:
        return url
    u = parse.urlparse(url)
    host_list = u.hostname.split('.')
    if len(host_list) < 3:
        return None
    return host_list[-3].lower() + '.' + host_list[-2].lower()


# 目前支持video、audio、image类型，其他返回None
def guess_media_type(url):
    mimetype, _ = mimetypes.guess_type(url)
    if not mimetype:
        return None
    try:
        return MediaType(mimetype.split('/')[0])
    except:
        return None
