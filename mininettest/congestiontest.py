import time
import argparse
from basicTopo import setup_environment

SERVER_CMD = "/App/quic/server_mt"
CERTPATH = "--certpath /App/quic/quic_go_certs"
SCH = "-scheduler dqnAgent"
ARGS = "-bind :6121 -www /var/www/"
COMMON = "-spec /App/quic/agent.spec -outputpath /App/output/"
TRAINING = "-training"
WFILE = "-weightsFile %s"
EPS = "-epsilon %s"
ACONG = "-validCongestion %s"
END = "> /App/logs/server.logs 2>&1"

BASIC_DELAY = 100

CLIENT_CMD = "/App/quic/client_mt -m https://10.0.0.20:6121/test3  > /App/logs/client.logs 2>&1"

TCP_SERVER_CMD = "cd /var/www && python -m SimpleHTTPServer 80 &"
TCP_CLIENT_CMD0 = "curl --interface client-eth0 -s -o /dev/null 10.0.0.20/test3 &"
TCP_CLIENT_CMD1 = "curl --interface client-eth1 -s -o /dev/null 10.0.0.20/test3 &"


def setup():
    net = setup_environment()
    net.start()
    return net


def exec_test(server_cmd, rtt, tcp_traffic):
    network = setup()

    s1 = network.get("s1")
    server = network.get("server")
    client = network.get("client")

    if tcp_traffic:
        server.cmd(TCP_SERVER_CMD)
    server.sendCmd(server_cmd)
    client.cmd("sleep 1")

    s1.cmd("./scripts/set_delay.bash %d" % int((BASIC_DELAY + rtt) / 2))
    client.cmd("./scripts/client_set_delay.bash %d" % int((BASIC_DELAY + rtt) / 2))

    if tcp_traffic:
        client.cmd(TCP_CLIENT_CMD0)
        client.cmd(TCP_CLIENT_CMD1)

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


def do_training(is_training, weight_file, epsilon, rtt=0, vcong=0, tcp_b=False, validate=False):
    server_cmd = " ".join([SERVER_CMD, CERTPATH, SCH, ARGS, COMMON])
    if is_training:
        server_cmd = " ".join([server_cmd, TRAINING])
    if validate:
        server_cmd = " ".join([server_cmd, "-validating"])
    if epsilon is None:
        epsilon = 0.
    server_cmd = " ".join([server_cmd, WFILE % weight_file, EPS % epsilon, ACONG % vcong, END])

    exec_test(server_cmd, rtt, tcp_b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Executes a test with DQNAgent scheduler')
    parser.add_argument('--train', dest="training", action="store_true", help='indicates a training test')
    parser.add_argument('--weight_file', dest="wfile", help="path to weights file", required=False)
    parser.add_argument('--epsilon', dest="epsilon", help="epsilon while training", required=False)
    parser.add_argument('--rtt', type=int, dest="rtt", help="rtt primary leg")
    parser.add_argument('--valid_congestion', type=int, dest="vcong", help="Dummy for backward compatibility")
    parser.add_argument('--background-tcp', dest="tcp_background", action="store_true", help='generates TCP background traffic during tests')
    parser.add_argument('--validating', dest="validating", action="store_true",  help="activates the validation")

    args = parser.parse_args()
    do_training(args.training, args.wfile, args.epsilon, args.rtt, args.vcong, args.tcp_background, args.validating)