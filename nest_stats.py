import argparse
import json
import re
import subprocess

import statsd

def c_to_f(val):
    return (val * 1.8) + 32.0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CyberPower Statsd Pusher')
    parser.add_argument('statsd_server', type=str)
    parser.add_argument('node_name', type=str)
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('serial', type=str)
    parser.add_argument('-p', '--statsd-port', type=int, default=8125)
    parser.add_argument('-r', '--statsd-sample-rate', type=float, default=1.0)
    args = parser.parse_args()

    connection = statsd.Connection(host=args.statsd_server,
                                   port=args.statsd_port,
                                   sample_rate=args.statsd_sample_rate)

    guage = statsd.Gauge('temperature.nest.{}'.format(args.node_name))

    nest_stats = subprocess.check_output(['nest.py', '--user', args.username,
                                          '--password', args.password, 'json'])

    nest_dict = json.loads(nest_stats)

    current_temp = nest_dict['shared'][args.serial]['current_temperature']
    current_temp = c_to_f(float(current_temp))
    target_temp = nest_dict['shared'][args.serial]['target_temperature']
    target_temp = c_to_f(float(target_temp))
    target_temp_low = nest_dict['shared'][args.serial]['target_temperature_low']
    target_temp_low = c_to_f(float(target_temp_low))
    target_temp_high = nest_dict['shared'][args.serial]['target_temperature_high']
    target_temp_high = c_to_f(float(target_temp_high))
    current_humidity = nest_dict['device'][args.serial]['current_humidity']
    target_humidity = nest_dict['device'][args.serial]['target_humidity']

    hvac_fan_state = nest_dict['shared'][args.serial]['hvac_fan_state']
    hvac_heater_state = nest_dict['shared'][args.serial]['hvac_heater_state']
    hvac_ac_state = nest_dict['shared'][args.serial]['hvac_ac_state']
    hvac_aux_state = nest_dict['shared'][args.serial]['hvac_aux_heater_state']
    hvac_emer_heat_state = nest_dict['shared'][args.serial]['hvac_emer_heat_state']

    print current_temp
    guage.send('current_temp', float(current_temp))
    print target_temp
    guage.send('target_temp', float(target_temp))
    print target_temp_low
    guage.send('target_temp_low', float(target_temp_low))
    print target_temp_high
    guage.send('target_temp_high', float(target_temp_high))
    print current_humidity
    guage.send('current_humidity', float(current_humidity))
    print target_humidity
    guage.send('target_humidity', float(target_humidity))
    print hvac_fan_state
    guage.send('fan_on', 1 if hvac_fan_state else 0)
    print hvac_heater_state
    guage.send('heat_on', 1 if hvac_heater_state else 0)
    print hvac_ac_state
    guage.send('ac_on', 1 if hvac_ac_state else 0)
    print hvac_aux_state
    guage.send('aux_on', 1 if hvac_aux_state else 0)
    print hvac_emer_heat_state
    guage.send('emergency_on', 1 if hvac_emer_heat_state else 0)
