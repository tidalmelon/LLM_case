# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import re

PAT_TIME_LIST = [
    # 2023-03-31 16:09:01
    re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}"),
    # 2023-03-31 16:09
    re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}")]

def get_time(text):
    for pat in PAT_TIME_LIST:
        m = pat.search(text)
        if m:
            return m.group(0)
    return text


def remove_space(text):
    return ''.join(filter(lambda ch: not ch.isspace(), text))


def get_text(dom, x):
    txt = dom.xpath(x)
    if txt:
        line = ''.join(txt)
        return line.strip()
    return None



def list_link_anchor(dom, x, base_url, keep_anchor_space=False):
    link_anchor_arr = []
    a_node_list = dom.xpath(x)
    if not a_node_list:
        return link_anchor_arr

    for a_node in a_node_list:
        anchor = a_node.xpath('.//text()')
        href = a_node.xpath('./@href')

        if href:

            # extract href
            href = href[0]

            if not href.strip():
                continue
            if href.startswith('javascript'):
                continue
            if href.startswith('mailto'):
                continue

            href = urljoin(base_url, href)

            # extract anchor
            anchor = ''.join(anchor)
            if not keep_anchor_space:
                anchor = remove_space(anchor)

            link_anchor_arr.append((href, anchor))
    return link_anchor_arr
