# see http://stackoverflow.com/a/21416007/931303
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import MySQLdb


DEFAULT_LIMIT_COUNT = 100


class Connection():
    def __init__(self, host=None, port=None):
        host, port = configure_connection(host, port)
        self.db = MySQLdb.connect(host=host, port=port, charset='utf8')

    def iterator(self, sql, params):
        cursor = self.db.cursor()

        try:
            cursor.execute(sql, params)
        except Exception:
            cursor.close()
            raise

        cursor.execute(sql, params)

        for x in range(cursor.rowcount):
            yield cursor.fetchone()

        cursor.close()


def configure_connection(host, port):
    from sphinxql.configuration import indexes_configurator
    if host is None:
        host = '0'
    if port is None:
        port_string = indexes_configurator.searchd_conf.params['listen']
        port = int(port_string.split(':')[0])

    return host, port
