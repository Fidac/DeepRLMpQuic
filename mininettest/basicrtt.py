import time
import argparse
from basicTopo import setup_environment

SERVER_CMD = "/App/quic/server_mt"
CERTPATH = "--certpath /App/quic/quic_go_certs"
ARGS = "-bind :6121 -www /var/www/"
LOGS = "-v"
SCH = "-scheduler %s"
END = "> /App/logs/server.logs 2>&1"

BASIC_DELAY = 30

CLIENT_CMD = "/App/quic/client_mt -m https://10.0.0.20:6121/test3  > /App/logs/client.logs 2>&1"


def setup():
    net = setup_environment()
    net.start()
    return net


def exec_test(server_cmd, rtt):
    network = setup()

    s1 = network.get("s1")
    server = network.get("server")
    client = network.get("client")

    server.sendCmd(server_cmd)
    client.cmd("sleep 1")

    s1.cmd("./scripts/set_delay.bash %d" % int((BASIC_DELAY + rtt) / 2))
    client.cmd("./scripts/client_set_delay.bash %d" % int((BASIC_DELAY + rtt) / 2))

    start = time.time()
    client.sendCmd(CLIENT_CMD)
    # Timeout of 10 seconds for detecting crashing tests
    output = client.monitor(timeoutms=10000)

    # Check for timeout
    if client.waiting:
        delta = 10
        client.sendInt()
        client.waiting = False
        network.stop()
        time.sleep(1)
        network.cleanup()
    else:
        # TODO: Check for errors here?? How??
        delta = time.time() - start

    server.sendInt()

    server.monitor()
    server.waiting = False


def do_training(activate_logs, rtt, sch):
    server_cmd = " ".join([SERVER_CMD, CERTPATH, ARGS])
    if activate_logs:
        server_cmd = " ".join([server_cmd, LOGS])
    if sch!="":
        server_cmd = " ".join([server_cmd, SCH%sch])
    server_cmd = " ".join([server_cmd, END])

    exec_test(server_cmd, rtt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Executes a test with DQNAgent scheduler')
    parser.add_argument('--logs', dest="logs", action="store_true", help='indicates a training test')
    parser.add_argument('--rtt', type=int, dest="rtt", help="rtt primary leg")
    parser.add_argument('--scheduler', type=str, dest="sch", help="scheduler")

    args = parser.parse_args()
    do_training(args.logs, args.rtt, args.sch)
