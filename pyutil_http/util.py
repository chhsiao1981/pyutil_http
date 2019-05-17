# -*- coding: utf-8 -*-
"""Summary
"""

import grequests
from requests import Response

import pyutil_json as util_json

from .constants import HTTP_TIMEOUT
from . import errors


def http_multipost(the_url_data, timeout=HTTP_TIMEOUT, cookies=None, headers=None, exception_handler=None):
    '''
    the_url_data: {the_url: data_by_url}
    return: error, {the_url: (each_error, content)}

    Args:
        the_url_data (TYPE): Description
        timeout (TYPE, optional): Description
        cookies (None, optional): Description
        headers (None, optional): Description
        exception_handler (None, optional): Description

    Returns:
        TYPE: Description
    '''
    error = None

    the_url_data_list = the_url_data.items()

    error, result_list = http_multipost_list(the_url_data_list, timeout=timeout, cookies=cookies, headers=headers, exception_handler=exception_handler)
    if error:
        return error, {}

    result = {each_result[0]: each_result[1] for each_result in result_list}

    return None, result


def http_multipost_list(the_url_data, timeout=HTTP_TIMEOUT, cookies=None, headers=None, exception_handler=None):
    '''
    the_url_data: [(the_url, data_by_url)]
    return: error, [(the_url, (each_error, content))]

    Args:
        the_url_data (TYPE): Description
        timeout (TYPE, optional): Description
        cookies (None, optional): Description
        headers (None, optional): Description
        exception_handler (None, optional): Description

    Returns:
        TYPE: Description
    '''
    error = None

    # cfg.logger.warning('to post: the_url_data: %s', the_url_data)

    rs = (grequests.post(each_url_data[0], data=each_url_data[1], timeout=timeout, cookies=cookies, headers=headers) for each_url_data in the_url_data)
    result_map = grequests.map(rs, exception_handler=exception_handler)

    result = []
    try:
        result_map_content = list(map(_grequest_get_content, result_map))
        result = [(each_url_data[0], result_map_content[idx]) for (idx, each_url_data) in enumerate(the_url_data)]
    except Exception as e:
        the_urls = [each_url_data[0] for each_url_data in the_url_data]
        error = errors.ErrorHTTP('unable to http_multipost: the_urls: %s e: %s' % (the_urls, e))
        result = []

    return error, result


def http_multiget(the_urls, params='', timeout=HTTP_TIMEOUT, cookies=None, headers=None, exception_handler=None):
    '''
    the_urls: [the_url]
    return: error, {url: (each_error, content)}

    Args:
        the_urls (TYPE): Description
        params (str, optional): Description
        timeout (TYPE, optional): Description
        cookies (None, optional): Description
        headers (None, optional): Description
        exception_handler (None, optional): Description

    Returns:
        TYPE: Description
    '''
    error = None

    # cfg.logger.warning('to grequests: the_urls: %s params: %s cookies: %s', the_urls, params, cookies)

    rs = (grequests.get(u, params=params, timeout=timeout, cookies=cookies, headers=headers) for u in the_urls)
    result_map = grequests.map(rs, exception_handler=exception_handler)

    result = {}
    try:
        result_map_content = list(map(_grequest_get_content, result_map))
        result = {the_url: result_map_content[idx] for (idx, the_url) in enumerate(the_urls)}
    except Exception as e:
        error = errors.ErrorHTTP('unable to http_multiget: the_urls: %s e: %s' % (the_urls, e))
        result = {}

    return error, result


def _grequest_get_content(result):
    '''
    check http_multiget

    Args:
        result (TYPE): Description

    Returns:
        TYPE: Description
    '''
    if not isinstance(result, Response):  # requests.Response
        return errors.ErrorHTTP('no response'), b''

    if result.status_code >= 400:
        return errors.ErrorHTTP('status_code: %s' % (result.status_code)), b''

    return None, result.content


def send_requests(all_machines, path, params, method, timeout=HTTP_TIMEOUT, cookies=None, headers=None, exception_handler=None):
    '''
    1. mapping from machine to url
    2. do parallel requests with url
    3. results: error, {machine: (each_error, data)}

    Args:
        all_machines (TYPE): Description
        path (TYPE): Description
        params (TYPE): Description
        method (TYPE): GET / POST
        timeout (TYPE, optional): Description
        cookies (None, optional): Description
        headers (None, optional): Description
        exception_handler (None, optional): Description

    Returns:
        TYPE: Description
    '''
    the_urls_dict = {machine: machine + path for machine in all_machines}
    the_urls_list = the_urls_dict.values()

    error, data = _send_requests_list(the_urls_list, params, method, timeout, cookies, headers, exception_handler)
    if error:
        return error, {}

    # data: {the_url: (each_error, content)}

    results = {machine: _parse_send_requests_data(data.get(the_url, None)) for machine, the_url in the_urls_dict.items()}

    return None, results


def send_requests_with_different_params(the_url_data, timeout=HTTP_TIMEOUT, cookies=None, headers=None, exception_handler=None):
    """Summary

    Args:
        the_url_data (TYPE): Description
        timeout (TYPE, optional): Description
        cookies (None, optional): Description
        headers (None, optional): Description
        exception_handler (None, optional): Description

    Returns:
        TYPE: Description
    """
    error, result = http_multipost(the_url_data, timeout=timeout, cookies=cookies, headers=headers, exception_handler=exception_handler)
    if error:
        return error, {}

    return None, {machine: _parse_send_requests_data(data) for machine, data in result.items()}


def _send_requests_list(the_urls_list, params, method, timeout, cookies, headers, exception_handler):
    '''
    return: error, {the_url: (each_error, content)}

    Args:
        the_urls_list (TYPE): Description
        params (TYPE): Description
        method (TYPE): Description
        timeout (TYPE): Description
        cookies (TYPE): Description
        headers (TYPE): Description

    Returns:
        TYPE: Description
    '''
    if method == 'POST':
        the_url_data = {the_url: params for the_url in the_urls_list}
        return http_multipost(the_url_data, timeout, cookies, headers=headers, exception_handler=exception_handler)

    else:
        return http_multiget(the_urls_list, params, timeout, cookies, headers=headers, exception_handler=exception_handler)


def _parse_send_requests_data(data):
    """Summary

    Args:
        data (TYPE): Description

    Returns:
        TYPE: Description
    """
    if not data:
        return errors.ErrorHTTP('empty data'), {}

    error, content = data
    if error:
        return error, {}

    return util_json.json_loads(content)
