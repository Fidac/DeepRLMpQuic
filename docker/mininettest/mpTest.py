import unittest
from basictest import BaseTest


class TestMP(BaseTest):

    def testMPQUIC(self):
        server_cmd = "/App/quic/server_mt --certpath /App/quic/quic_go_certs -bind :6121 -www /var/www/ > /dev/null 2>&1"
        client_cmd = "/App/quic/client_mt -m https://10.0.0.20:6121/test3 > /dev/null 2>&1"
        name = "mp-quic-rtt-sch"

        self.do_test(name, server_cmd, client_cmd, number_tests=200)

    def testMPRandom(self):
        server_cmd = "/App/quic/server_mt --certpath /App/quic/quic_go_certs -scheduler random -bind :6121 -www /var/www/ > /dev/null 2>&1"
        client_cmd = "/App/quic/client_mt -m https://10.0.0.20:6121/test3 > /dev/null 2>&1"
        name = "mp-quic-random-sch"

        self.do_test(name, server_cmd, client_cmd, number_tests=200)

    def testMPSingle(self):
        server_cmd = "/App/quic/server_mt --certpath /App/quic/quic_go_certs -bind :6121 -www /var/www/ > /dev/null 2>&1"
        client_cmd = "/App/quic/client_mt https://10.0.0.20:6121/test3 > /dev/null 2>&1"
        name = "mp-quic-single-sch"

        self.do_test(name, server_cmd, client_cmd, number_tests=200)


if __name__ == '__main__':
    unittest.main()
