import time
import argparse
from basicTopo import setup_environment

SERVER_CMD = "/App/quic/server_mt"
CERTPATH = "--certpath /App/quic/quic_go_certs"
SCH = "-scheduler %s"
ARGS = "-bind :6121 -www /var/www/"
END = "> /App/logs/server.logs 2>&1"

BASIC_DELAY = 100
BASIC_LOSS = 50

CLIENT_CMD = "/App/quic/client_mt -m https://10.0.0.20:6121/test3  > /App/logs/client.logs 2>&1 &"

TCP_SERVER_CMD0= "cd /var/www && python -m SimpleHTTPServer 91 &"
TCP_SERVER_CMD1 = "cd /var/www && python -m SimpleHTTPServer 80 &"
TCP_CLIENT_CMD0 = "curl --interface client-eth0 -s -o /dev/null 10.0.0.20:91/test3 &"
TCP_CLIENT_CMD1 = "curl --interface client-eth1 -s -o /dev/null 10.0.0.20:80/test3 &"

TCP_DUMP_TCP_ETH1="tcpdump -nn -i client-eth1 \"src 10.0.0.20 and tcp\" > /App/logs/tcp_packets_eth1.logs 2>&1 &"
TCP_DUMP_MPQUIC_ETH1="tcpdump -nn -i client-eth1 \"src 10.0.0.20 and udp\" > /App/logs/mpquic_packets_eth1.logs 2>&1 &"
TCP_DUMP_TCP_ETH0="tcpdump -nn -i client-eth0 \"src 10.0.0.20 and tcp\" > /App/logs/tcp_packets_eth0.logs 2>&1 &"
TCP_DUMP_MPQUIC_ETH0="tcpdump -nn -i client-eth0 \"src 10.0.0.20 and udp\" > /App/logs/mpquic_packets_eth0.logs 2>&1 &"

def setup():
    net = setup_environment()
    net.start()
    return net


def exec_test(server_cmd, rtt, tcp_traffic, dif_start, gap, loss_eth0, loss_eth1):
    network = setup()

    s1 = network.get("s1")
    server = network.get("server")
    client = network.get("client")

    client.cmd(TCP_DUMP_TCP_ETH1)
    client.cmd(TCP_DUMP_MPQUIC_ETH1)
    client.cmd(TCP_DUMP_TCP_ETH0)
    client.cmd(TCP_DUMP_MPQUIC_ETH0)

    if tcp_traffic:
        server.cmd(TCP_SERVER_CMD0)
        server.cmd(TCP_SERVER_CMD1)

    server.sendCmd(server_cmd)
    client.cmd("sleep 1")

    s1.cmd("./scripts/set_delay.bash %d" % (int((BASIC_DELAY + rtt) / 2)))
    client.cmd("./scripts/client_set_delay.bash %d %d %d" % (int((BASIC_DELAY + rtt) / 2), loss_eth0, loss_eth1))
    if(dif_start == 1):
        client.cmd(CLIENT_CMD)
        time.sleep(gap)
        if tcp_traffic:
            client.cmd(TCP_CLIENT_CMD0)
            client.cmd(TCP_CLIENT_CMD1)
    else:
        if tcp_traffic:
            client.cmd(TCP_CLIENT_CMD0)
            client.cmd(TCP_CLIENT_CMD1)
        time.sleep(gap)
        client.cmd(CLIENT_CMD)
    time.sleep(100)
    #start = time.time()
    # Timeout of 10 seconds for detecting crashing tests
    #output = client.monitor(timeoutms=30000)

    # Check for timeout
    #if client.waiting:
    #    delta = 30
    #    client.sendInt()
    #    client.waiting = False
    #    network.stop()
    #    time.sleep(1)
    #    network.cleanup()
    #else:
        # TODO: Check for errors here?? How??
    #    delta = time.time() - start
    # client.sendInt()
    # network.stop()
    # time.sleep(1)
    # network.cleanup()
    # server.sendInt()

    # server.monitor()
    # server.waiting = False


def do_training(sch, rtt, tcp_b, dif_start, gap, loss_eth0, loss_eth1):
    server_cmd = " ".join([SERVER_CMD, CERTPATH, SCH % sch, ARGS, END])

    exec_test(server_cmd, rtt, tcp_b, dif_start, gap, loss_eth0, loss_eth1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Executes a test with defined scheduler')
    parser.add_argument('--scheduler', dest="sch", help="Scheduler (rtt, random)", required=True)
    parser.add_argument('--rtt', type=int, dest="rtt", help="rtt primary leg")
    parser.add_argument('--background-tcp', dest="tcp_background", action="store_true",
                        help='generates TCP background traffic during tests')
    parser.add_argument('--different-start', type=int, dest="dif_start", default=0, help="specify who go first")
    parser.add_argument('--gap', type=int, dest="gap", default=0, help="specify the gap between MPQUIC and TCP")
    parser.add_argument('--lethl', type=int, dest="lethl", default=0, help="specify the loss rate at eth-0 link")
    parser.add_argument('--lethr', type=int, dest="lethr", default=0, help="specify the loss rate at eth-1 link")


    args = parser.parse_args()
    do_training(args.sch, args.rtt, args.tcp_background, args.dif_start,args.gap, args.lethl, args.lethr)
