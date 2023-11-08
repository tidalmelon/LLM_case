# -*- coding: utf-8 -*-


def cookie_to_headers(block):
    headers = {}
    url = ''
    for line in block.split(' '*2):
        line = line.strip()
        if line.startswith('curl'):
            url = line.split()[-1].strip("'")
        # ['-H \'sec-ch-ua-platform: "macOS"\'']
        if line.startswith('-H'):
            line = line[3:].strip("'")
            k, v = line.split(': ')
            headers[k] = v

    return url, headers
