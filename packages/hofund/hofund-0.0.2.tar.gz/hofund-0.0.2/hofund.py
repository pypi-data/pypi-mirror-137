import argparse
import asyncio
from cmath import nan
from dataclasses import field
import functools
import json
from textwrap import indent
from traceback import print_tb
import pandas
import aiohttp
from typing import Dict, List, Iterable, Tuple

MAX_CONNECTIONS = 20
TIMEOUT = 60
STENCIL_NAMESPACE="clickstream"

CONFIG = {}

def parse_args():
    parser = argparse.ArgumentParser(description='recommend proto messages for a given field')
    parser.add_argument('--f', metavar='input-file', type=str,
                    help='input csv which contains property data', dest='property_file', required=True) 
    col_group = parser.add_mutually_exclusive_group(required=True)
    col_group.add_argument('--col', metavar='property-column-name', type=str, dest='property_col_name',
                    help='column name in the input csv sheet which has the property names to be searched')
    col_group.add_argument('--col-num', metavar='property-column-num', type=int,
                    help='column number in the input csv which has the property names to be searched',
                    dest='property_col_num')
    col_ctx_group = parser.add_mutually_exclusive_group()
    col_ctx_group.add_argument('--ctx-col', metavar='property-context-column-name', type=str, dest='property_ctx_col_name',
                    help='column name in the input csv sheet which has the context for the property name to be searched')
    col_ctx_group.add_argument('--ctx-col-num', metavar='property-context-column-num', type=int,
                    help='column number in the input csv which has the context of property name to be searched',
                    dest='property_ctx_col_num')
    parser.add_argument('--out-msg-col', metavar='output-msg-column-name', type=str, default='Recommended Messages', dest='output_msg_column_name', 
                    help='output column name where recommended proto message names are filled')
    parser.add_argument('--out-field-col', metavar='output-fieldcolumn-name', type=str, default='Recommended Fields', dest='output_field_column_name', 
                    help='output column name where recommended proto fields/property names are filled')                    
    parser.add_argument('--stencil-host', type=str, default='localhost', help=argparse.SUPPRESS, dest='stencil_host')
    parser.add_argument('--stencil-port', type=int, default=8080, help=argparse.SUPPRESS, dest='stencil_port')
    parser.add_argument('--stencil-request-scheme', type=str, default='http', help=argparse.SUPPRESS, dest='stencil_request_scheme')
    
    return parser.parse_args()

async def stencil_search(url: str, session: aiohttp.ClientSession) -> Tuple[List]:
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                print('search request failed for {}'.format(url))
                return ([], [])
            resp: bytes = await resp.read()
            resp_body = json.loads(resp)
            return (functools.reduce(lambda fields, hit: fields.union(set(hit['fields'])), resp_body['hits'], set()), 
                    functools.reduce(lambda messages, hit: messages.union(set(hit['types'])), resp_body['hits'], set())) if resp_body['meta']['total'] > 0 else ([], [])
    except Exception as e:
        print('Unable to get {} due to {}: {}'.format(url, e.__class__, e))
        return ([], [])

def get_stencil_url(stencil_request_scheme: str,
                        stencil_host: str,
                        stencil_port: str,
                        query: str) -> str:
    return '{}://{}:{}/v1beta1/search?query={}&namespace_id={}'.format(
                            stencil_request_scheme, 
                            stencil_host, 
                            stencil_port, 
                            query, 
                            STENCIL_NAMESPACE)

async def search(search_terms: List[str]) -> Tuple[List]:
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[stencil_search(get_stencil_url(
            CONFIG.stencil_request_scheme,
            CONFIG.stencil_host,
            CONFIG.stencil_port,
            query), session) for query in search_terms])
        return ', '.join(functools.reduce(lambda x, y : x + list(y[0]), ret, [])), ', '.join(functools.reduce(lambda x, y : x + list(y[1]), ret, []))

def get_context_keys(context_str: str) -> List[str]:
    return [s.strip() for s in context_str.strip().split(',')] if not pandas.isna(context_str) else []


def get_searchable_terms(row: pandas.Series) -> List[str]:
    search_terms: List[str] = []
    if CONFIG.property_col_name is not None:
        search_terms.append(row[CONFIG.property_col_name])
    else:
        search_terms.append(row.values[CONFIG.property_col_num - 1])

    if CONFIG.property_ctx_col_name is not None:
        search_terms += get_context_keys(row[CONFIG.property_ctx_col_name])
    elif CONFIG.property_ctx_col_num is not None:
        search_terms += get_context_keys(row.values[CONFIG.property_ctx_col_num - 1])
    
    return search_terms

async def search_rows(rows: Iterable[pandas.Series]) -> Tuple:
    messages: List[str] = []
    fields: List[str] = []
    for _, row in rows:
        search_res = await search(get_searchable_terms(row))
        messages.append(search_res[1])
        fields.append(search_res[0])
    return (messages, fields)
    

async def start():
    try:
        df: pandas.DataFrame = pandas.read_csv(CONFIG.property_file)
        df[CONFIG.output_msg_column_name], df[CONFIG.output_field_column_name] = await search_rows(df.iterrows())
        df.to_csv(CONFIG.property_file, index=False)
    except Exception as e:
        print(e)

def main():
    CONFIG = parse_args()
    asyncio.run(main())

if __name__ ==  "__main__":
    CONFIG = parse_args()
    asyncio.run(main())
    

    


