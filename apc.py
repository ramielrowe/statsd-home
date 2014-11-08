import argparse
import re
import subprocess

import statsd

FLOAT_STR = "(\d+\.?\d?){1}[\s\w]*"
FLOAT_RE = re.compile(FLOAT_STR)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CyberPower Statsd Pusher')
    parser.add_argument('statsd_server', type=str)
    parser.add_argument('node_name', type=str)
    parser.add_argument('apcupsd_server', type=str)
    parser.add_argument('-p', '--statsd-port', type=int, default=8125)
    parser.add_argument('-r', '--statsd-sample-rate', type=float, default=1.0)
    parser.add_argument('-P', '--apcupsd-port', type=int, default=3551)
    args = parser.parse_args()

    connection = statsd.Connection(host=args.statsd_server,
                                   port=args.statsd_port,
                                   sample_rate=args.statsd_sample_rate)

    guage = statsd.Gauge('power.ups.{}'.format(args.node_name))

    ups_status = subprocess.check_output(['/sbin/apcaccess', 'status',
                                          args.apcupsd_server,
                                          str(args.apcupsd_port)])
    stats_dict = dict()
    for line in ups_status.split('\n'):
        if line:
            vals = line.split(':', 1)
            stats_dict[vals[0].strip()] = vals[1].strip()

    voltage_rating = float(FLOAT_RE.match(stats_dict['NOMINV']).group(1))
    load_max = float(FLOAT_RE.match(stats_dict['NOMPOWER']).group(1))
    voltage_in = float(FLOAT_RE.match(stats_dict['LINEV']).group(1))
    voltage_out = voltage_in
    capacity = float(FLOAT_RE.match(stats_dict['BCHARGE']).group(1))
    remaining_time = float(FLOAT_RE.match(stats_dict['TIMELEFT']).group(1))
    load_percent = float(FLOAT_RE.match(stats_dict['LOADPCT']).group(1))
    load = load_max * (load_percent / 100.0)

    print voltage_rating
    guage.send('voltage_rating', float(voltage_rating))
    print load_max
    guage.send('load_max', float(load_max))
    print voltage_in
    guage.send('voltage_in', float(voltage_in))
    print voltage_out
    guage.send('voltage_out', float(voltage_out))
    print capacity
    guage.send('capacity', float(capacity))
    print remaining_time
    guage.send('remaining_time', float(remaining_time))
    print load
    guage.send('load', float(load))
    print load_percent
    guage.send('load_percent', float(load_percent))
