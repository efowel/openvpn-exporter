#!/usr/bin/python

import os, subprocess, time, argparse
from prometheus_client import start_http_server, Gauge

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, port=9176):
        self.port = port

    def run_metrics_loop(self, polling

    def run_metrics_loop(self, polling_interval):
       """Metrics fetching loop"""
       self.polling_interval = polling_interval
       self.current_users = Gauge("vpn_current_users", "Current Users")
       while True:
            command = "/usr/local/openvpn_as/scripts/sacli  VPNsummary | jq '.n_clients'"
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
            out, err = process.communicate()
            p=int(out)
            self.current_users.set(p)
            time.sleep(self.polling_interval)

def main():
    parser = argparse.ArgumentParser(description='Pass command arguments')
    parser.add_argument("-t", metavar='-t', dest="t", type=int, required=True,
                                help='time interval between metrics poll, suggested value 300 (5mins)')
    parser.add_argument("-p", metavar='-p', dest="p", type=int, nargs='?', action="store",
                                help='port to exposed the metrics, default is 9176')
    args = parser.parse_args()
    t = args.t
    if args.p:
        p = args.p
    else:
        p = 9176
    app_metrics = AppMetrics(port=(p))
    start_http_server(p)
    app_metrics.run_metrics_loop(polling_interval=(t))

if __name__ == "__main__":
    main()

