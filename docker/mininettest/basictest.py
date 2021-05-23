import unittest
from basicTopo import setup_environment
import time
import datetime
import locale


class BaseTest(unittest.TestCase):

    NETWORK = None
    BASIC_DELAY = 100
    CMD_TIMEOUTMS = 10000
    TIMEOUT_RESULT_SECONDS = 100

    @classmethod
    def setUpClass(cls):
        super(BaseTest, cls).setUpClass()
        cls.NETWORK = setup_environment()
        cls.NETWORK.start()

    def do_test(self, name, server_cmd, client_cmd, number_tests=40, rtt_list=[0, 10, 20, 30, 40, 50, 60, 70]):
        s1 = self.NETWORK.get("s1")
        server = self.NETWORK.get("server")
        client = self.NETWORK.get("client")

        rtt = rtt_list

        results = {}

        server.sendCmd(server_cmd)
        client.cmd("sleep 1")

        for delay in rtt:
            s1.cmd("./scripts/set_delay.bash %d" % int((self.BASIC_DELAY + delay) / 2))
            client.cmd("./scripts/client_set_delay.bash %d" % int((self.BASIC_DELAY + delay) / 2))
            results[delay] = []
            for i in range(number_tests):
                start = time.time()
                client.sendCmd(client_cmd)
                # Timeout of 10 seconds for detecting crashing tests
                output = client.monitor(timeoutms=self.CMD_TIMEOUTMS)

                # Check for timeout
                if client.waiting:
                    delta = self.TIMEOUT_RESULT_SECONDS
                    client.sendInt()
                    client.waiting = False
                else:
                    # TODO: Check for errors here?? How??
                    delta = time.time() - start
                if delta < 1:
                    delta = 3
                results[delay].append(delta)

        server.sendInt()
        self.save_results(results, name)
        server.monitor()
        server.waiting = False

    def save_results(self, results, name):
        with open("../output/results-%s-%s" % (name,  datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f")), 'w+') as f:
            rtts = results.keys()
            rtts.sort()
            #Header
            f.write(",".join([str(rtt) for rtt in rtts]))
            f.write("\n")
            for measure_row in range(len(results[rtts[0]])):
                row = ""
                for rtt in rtts:
                    locale.setlocale(locale.LC_ALL, 'en_US')
                    if row == "":
                        row = locale.format("%f", results[rtt][measure_row])
                    else:
                        row = ",".join((row, locale.format("%f", results[rtt][measure_row])))
                f.write(row)
                f.write("\n")
            f.flush()

    @classmethod
    def tearDownClass(cls):
        cls.NETWORK.stop()


class TestBasicQUIC(BaseTest):

    def testPing(self):
        client = self.NETWORK.get("client")
        _, _, exitcode = client.pexec("ping -c 1 -I 10.0.0.1 10.0.0.20")
        self.assertEqual(exitcode, 0)
        _, _, exitcode = client.pexec("ping -c 1 -I 10.0.0.2 10.0.0.20")
        self.assertEqual(exitcode, 0)

    def testMPQUIC(self):
        server_cmd = "/App/quic/server_mp --certpath /App/quic/quic_go_certs -bind :6121 -www /var/www/ > /dev/null 2>&1"
        client_cmd = "/App/quic/client_mp https://quic.clemente.io:6121/test3 > /dev/null 2>&1"
        name = "mp-quic-single-path"

        self.do_test(name, server_cmd, client_cmd, number_tests=200)

    def testQUICGo(self):
        server_cmd = "/App/quic/server_go --certpath /App/quic/quic_go_certs -bind :6121 -www /var/www/ > /dev/null 2>&1"
        client_cmd = "/App/quic/client_go https://quic.clemente.io:6121/test3 > /dev/null 2>&1"
        name = "quic-go-single-path"

        self.do_test(name, server_cmd, client_cmd, number_tests=200)

    def testTCP(self):
        server_cmd = "cd /var/www && python -m SimpleHTTPServer 80"
        client_cmd = "curl -s -o /dev/null 10.0.0.20/test3"
        name = "tcp-single-path"

        self.do_test(name, server_cmd, client_cmd, number_tests=35)

    # TODO: To delete this test (only useful at the begining of the project)
    # def testProtoQUIC(self):
    #     server_cmd = """/home/ubuntu/proto-quic/proto-quic/src/out/Default/quic_server \
    #       --quic_response_cache_dir=/var/www/quic-data/www.example.org   \
    #       --certificate_file=/home/ubuntu/proto-quic/proto-quic/src/net/tools/quic/certs/out/leaf_cert.pem   \
    #       --key_file=/home/ubuntu/proto-quic/proto-quic/src/net/tools/quic/certs/out/leaf_cert.pkcs8"""
    #     client_cmd = """/home/ubuntu/proto-quic/proto-quic/src/out/Default/quic_client  \
    #             https://www.example.org:6121/"""
    #     name = "protoquic-single-path"
    #
    #     self.do_test(name, server_cmd, client_cmd)


if __name__ == '__main__':
    unittest.main()
