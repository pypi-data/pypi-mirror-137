# author: delta1037
# Date: 2022/01/11
# mail:geniusrabbit@qq.com

import logging

import NotionDump
from NotionDump.Dump.dump import Dump
from NotionDump.Notion.Notion import NotionQuery
from NotionDump.utils import common_op

TOKEN_TEST = "secret_WRLJ9xyEawNxzRhVHVWfciTl9FAyNCd29GMUvr2hQD4"
PAGE_MIX_ID = "6138380c8d3d4c31884f4f90da60a4f1"


# 解析数据库内容测试：根据token和id解析数据库内容，得到临时CSV文件
def test_page_parser(query, export_child=False):
    page_handle = Dump(
        dump_id=PAGE_MIX_ID,
        query_handle=query,
        export_child_pages=export_child,
        dump_type=NotionDump.DUMP_TYPE_PAGE
    )
    # 将解析内容存储到文件中；返回内容存储为json文件
    page_detail_json = page_handle.dump_to_file()

    print("json output to page_parser_result")
    common_op.save_json_to_file(
        handle=page_detail_json,
        json_name=".tmp/page_parser_result.json"
    )


if __name__ == '__main__':
    query_handle = NotionQuery(token=TOKEN_TEST)
    if query_handle is None:
        logging.exception("query handle init error")
        exit(-1)

    # 页面解析测试,递归
    test_page_parser(query_handle, True)

    # 页面解析测试,非递归
    # test_page_parser(query_handle, False)

