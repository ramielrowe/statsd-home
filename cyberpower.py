import argparse
import re
import subprocess

import statsd

VOLTAGE_RATING_STR = "\s*Rating Voltage\.+ (\d+\.?\d?){1} \w+"
VOLTAGE_RATING_RE = re.compile(VOLTAGE_RATING_STR)

LOAD_MAX_STR = "\s*Rating Power\.+ (\d+\.?\d?){1} \w+"
LOAD_MAX_RE = re.compile(LOAD_MAX_STR)

VOLTAGE_IN_STR = "\s*Utility Voltage\.+ (\d+\.?\d?){1} \w+"
VOLTAGE_IN_RE = re.compile(VOLTAGE_IN_STR)

VOLTAGE_OUT_STR = "\s*Output Voltage\.+ (\d+\.?\d?){1} \w+"
VOLTAGE_OUT_RE = re.compile(VOLTAGE_OUT_STR)

CAPACITY_STR = "\s*Battery Capacity\.+ (\d+\.?\d?){1} %"
CAPACITY_RE = re.compile(CAPACITY_STR)

REMAINING_TIME_STR = "\s*Remaining Runtime\.+ (\d+\.?\d?){1} \w+\."
REMAINING_TIME_RE = re.compile(REMAINING_TIME_STR)

LOAD_STR = "\s*Load\.+ (\d+\.?\d?){1} Watt\((\d+\.?\d?){1} %\)"
LOAD_RE = re.compile(LOAD_STR)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CyberPower Statsd Pusher')
    parser.add_argument('statsd_server', type=str)
    parser.add_argument('node_name', type=str)
    parser.add_argument('-p', '--statsd-port', type=int, default=8125)
    parser.add_argument('-r', '--statsd-sample-rate', type=float, default=1.0)
    args = parser.parse_args()

    connection = statsd.Connection(host=args.statsd_server,
                                   port=args.statsd_port,
                                   sample_rate=args.statsd_sample_rate)

    guage = statsd.Gauge('power.ups.{}'.format(args.node_name))

    ups_status = subprocess.check_output(['/usr/sbin/pwrstat', '-status'])

    voltage_rating = VOLTAGE_RATING_RE.match(ups_status.split('\n')[6]).group(1)
    load_max = LOAD_MAX_RE.match(ups_status.split('\n')[7]).group(1)
    voltage_in = VOLTAGE_IN_RE.match(ups_status.split('\n')[12]).group(1)
    voltage_out = VOLTAGE_OUT_RE.match(ups_status.split('\n')[13]).group(1)
    capacity = CAPACITY_RE.match(ups_status.split('\n')[14]).group(1)
    remaining_time = REMAINING_TIME_RE.match(ups_status.split('\n')[15]).group(1)
    load_match = LOAD_RE.match(ups_status.split('\n')[16])
    load = load_match.group(1)
    load_percent = load_match.group(2)

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
