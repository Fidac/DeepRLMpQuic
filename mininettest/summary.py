import argparse


def print_summary(line):
    print("LINE: ", line)
    lines = str.splitlines(line)
    line = lines[1]
    print("LINE2: ", line)

    throughput, state, _ = line.split(",")
    rtt_a, rtt_b, _, _, _, _, _ = state.replace('[','').split(" ")

    print("Throughput: %s Mbps" % throughput)
    print("RTT path A: %f ms" % (float(rtt_a)*150.))
    print("RTT path B: %f ms" % (float(rtt_b)*150.))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Prints summary of the test')
    parser.add_argument("line", type=str, help="summary line")
    args = parser.parse_args()

    print_summary(args.line)
