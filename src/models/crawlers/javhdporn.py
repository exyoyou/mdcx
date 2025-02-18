#!/usr/bin/env python3
import json
import re
import time  # yapf: disable # NOQA: E402

import urllib3
from lxml import etree

from models.base.web import curl_html_cf as curl_html
from models.config.config import config

urllib3.disable_warnings()  # yapf: disable


def getRuntime(html):
    xpath_expression = "substring-after(//div[@id='video-date']/span/text(), 'Time:')"
    result = html.xpath(xpath_expression).strip()
    return result


def getTitle(html):
    result = html.xpath('//h1/text()')[0].strip()
    return result


def getStudio(html):
    xpath_expression = "//div[@id='video-actors']/i[@class='fa fa-film']/following-sibling::a/text()"
    result = html.xpath(xpath_expression)[0]
    return result


def getYear(html):
    xpath_expression = "substring-after(//div[@id='video-date']/text()[contains(., 'Date:')], 'Date:')"
    result = html.xpath(xpath_expression)
    return result


def getTag(html):
    xpath_expression = '//div[@id="video-actors"]//a/text()'
    result = str(html.xpath(xpath_expression))
    result = result.strip(" ['']").replace("'", "")
    return result


def getCover(html):
    try:
        xpath_expression = '//div[@class="video-player"]//img/@src'
        result = html.xpath(xpath_expression)[0]
    except:
        result = ""
    return result


def main(number, appoint_url="", log_info="", req_web="", language="zh_cn"):
    start_time = time.time()
    number = number.upper()
    number = re.sub(r'(FC2-)(\d+)', r'\1PPV-\2', number)
    url = "https://www4.javhdporn.net/video/" + number
    website_name = "javhdporn"
    req_web += f"-> {website_name}[{language}]"
    real_url = appoint_url or url
    image_cut = "right"
    image_download = False
    mosaic = "有码"
    web_info = "\n       "
    log_info += f' \n    🌐 javhdporn[{language.replace("zh_", "")}]'
    debug_info = ""

    try:  # 捕获主动抛出的异常
        if real_url:
            debug_info = f"番号地址: {real_url} "
            log_info += web_info + debug_info
            result, html_content = curl_html(real_url,)
            if not result:
                debug_info = f"网络请求错误: {html_content}"
                log_info += web_info + debug_info
                raise Exception(debug_info)

            html_info = etree.fromstring(html_content, etree.HTMLParser())
            title = getTitle(html_info)  # 获取标题
            if not title:
                debug_info = "数据获取失败: 未获取到title！"
                log_info += web_info + debug_info
                raise Exception(debug_info)
            cover_url = getCover(html_info)  # 获取cover
            tag = getTag(html_info)
            year = getYear(html_info)
            studio = getStudio(html_info)
            runtime = getRuntime(html_info)
            score = ""
            series = ""
            director = ""
            publisher = ""
            extrafanart = ""
            actor = ""
            outline = ""
            release = ""
            if "无码" in tag or "無修正" in tag or "無码" in tag or "uncensored" in tag.lower():
                mosaic = "无码"

            try:
                dic = {
                    "number": number,
                    "title": title,
                    "originaltitle": title,
                    "actor": actor,
                    "outline": outline,
                    "originalplot": outline,
                    "tag": tag,
                    "release": release,
                    "year": year,
                    "runtime": runtime,
                    "score": score,
                    "series": series,
                    "director": director,
                    "studio": studio,
                    "publisher": publisher,
                    "source": "javhdporn",
                    "cover": cover_url,
                    "poster": "",
                    "extrafanart": extrafanart,
                    "trailer": "",
                    "image_download": image_download,
                    "image_cut": image_cut,
                    "log_info": log_info,
                    "error_info": "",
                    "req_web": req_web + f"({round((time.time() - start_time), )}s) ",
                    "mosaic": mosaic,
                    "website": real_url,
                    "wanted": "",
                }
                debug_info = "数据获取成功！"
                log_info += web_info + debug_info
                dic["log_info"] = log_info
            except Exception as e:
                debug_info = f"数据生成出错: {str(e)}"
                log_info += web_info + debug_info
                raise Exception(debug_info)
    except Exception as e:
        debug_info = str(e)
        dic = {
            "title": "",
            "cover": "",
            "website": "",
            "log_info": log_info,
            "error_info": debug_info,
            "req_web": req_web + f"({round((time.time() - start_time), )}s) ",
        }
    dic = {website_name: {"zh_cn": dic, "zh_tw": dic, "jp": dic}}
    js = json.dumps(
        dic,
        ensure_ascii=False,
        sort_keys=False,
        indent=4,
        separators=(",", ": "),
    )  # .encode('UTF-8')
    return js


if __name__ == "__main__":
    print(main("fc2-1150731"))
