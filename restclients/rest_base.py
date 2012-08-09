from urllib3 import connection_from_url
from urllib import urlencode
import logging


class RestBase:
    def __init__(self):
        cfg = self._cfg
        self._pool = None
        self._init_logger()

    def GET(self, url, fields=None, headers=None):
        return self._request('GET', url, None, fields, headers)

    def PUT(self, url, body, fields=None, headers=None):
        return self._request('PUT', url, body, fields, headers)

    def POST(self, url, body, fields=None, headers=None):
        return self._request('POST', url, body, fields, headers)

    def DELETE(self, url, fields=None, headers=None):
        return self._request('DELETE', url, None, fields, headers)

    def _request(self, method, url, body=None, fields=None, headers=None):
        if fields:
            url += '?' + urlencode(fields)

        pool = self._get_pool()
        r = pool.urlopen(method, url, body, headers=headers)

        self._logger.info("\"%s %s\" %s %s" % (method, url, r.status,
                                               len(r.data)))

        return r

    def _init_logger(self):
        cfg = self._cfg
        if cfg.get('logname') and cfg.get('log'):
            logger = logging.getLogger(cfg['logname'])
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler(cfg['log'])
            fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            fh.setFormatter(fmt)
            logger.addHandler(fh)
            self._logger = logger

    def _get_pool(self):
        if self._pool is not None:
            return self._pool

        cfg = self._cfg
        kwargs = {'timeout': cfg.get('timeout')}

        if cfg.get('key') and cfg.get('cert'):
            kwargs['key_file'] = cfg.get('key')
            kwargs['cert_file'] = cfg.get('cert')

        self._pool = connection_from_url(cfg.get('url'), **kwargs)
        return self._pool
