pyutil_http
==========

utils for http

Usage
==========

http_multipost:

    url_data = {'http://localhost:1234/echo': 'echo1', 'http://localhost:1235/echo': 'echo2'}

    err, results = pyutil_http.http_multipost(url_data)

    err1, content1 = results['http://localhost:1234/echo']
    err2, content2 = results['http://localhost:1235/echo']

http_multipost_list:

    url_data_list = [
        ('http://localhost:1234/echo', 'echo3'),
        ('http://localhost:1236/echo', 'echo2'),
    ]

    err, results = pyutil_http.http_multipost_list(url_data_list)

    url1, (err1, content1) = results[0]
    url2, (err2, content2) = results[1]

http_multiget:

    urls = [
        'http://localhost:1234/echo?echo=echo1',
        'http://localhost:1235/echo?echo=echo2',
        'http://localhost:1236/echo?echo=echo3',
    ]

    err, results = pyutil_http.http_multiget(urls)
    self.assertIsNone(err)

    err1, content1 = results['http://localhost:1234/echo?echo=echo1']
    err2, content2 = results['http://localhost:1235/echo?echo=echo2']
    err3, content3 = results['http://localhost:1236/echo?echo=echo3']

send_requests:

    all_machines = [
        'http://localhost:1234/echo?echo={"test":1}',
        'http://localhost:1235/echo?echo={"test":2}',
        'http://localhost:1236/echo?echo={"test":3}',
    ]

    err, results = pyutil_http.send_requests(all_machines, '', '', 'GET')

    err1, content1 = results['http://localhost:1234/echo?echo={"test":1}']
    err2, content2 = results['http://localhost:1235/echo?echo={"test":2}']
    err3, content3 = results['http://localhost:1236/echo?echo={"test":3}']

send_requests_with_different_params:

    the_url_data = {
        'http://localhost:1234/echo': '{"test":1}',
        'http://localhost:1235/echo': '{"test":2}',
        'http://localhost:1236/echo': '{"test":3}',
    }

    err, results = pyutil_http.send_requests_with_different_params(the_url_data)

    err1, content1 = results['http://localhost:1234/echo']
    err2, content2 = results['http://localhost:1235/echo']
    err3, content3 = results['http://localhost:1236/echo']
