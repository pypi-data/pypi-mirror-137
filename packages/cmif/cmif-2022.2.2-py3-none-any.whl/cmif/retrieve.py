#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retrieve remote XML data in CMI format
"""

import requests

from lxml import etree


def remote_file(url):
    """
    send http get request to given url
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return etree.fromstring(response.content)
            except etree.ParseError:
                print("cmif.retrieve.remote_file:")
                print("failed to parse XML file!")
        else:
            print("cmif.retrieve.remote_file:")
            print("requesting remote file failed!")
            print("url of request:")
            print(response.url)
            print("http status code: ",
                  str(response.status_code))
    except requests.exceptions.ConnectionError:
        print("cmif.retrieve.remote_file:")
        print("request failed! connection error...")
    except requests.exceptions.Timeout:
        print("cmif.retrieve.remote_file:")
        print("request failed! timeout... try later?")
    except requests.exceptions.TooManyRedirects:
        print("cmif.retrieve.remote_file:")
        print("request failed! bad url, try another one!")
    except requests.exceptions.RequestException:
        print("cmif.retrieve.remote_file:")
        print("request failed! don't know why...")
    return None
