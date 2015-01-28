STATSD_HOST=CHANGEME
STATSD_IP=$(arp $STATSD_HOST | sed -rn "s/.*\((.*)\).*/\1/p")
STATSD_PORT=8125
NODE_NAME=CHANGEME

PWRSTAT_OUT=$(pwrstat -status)

VOLTAGE_RATING=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Rating Voltage\.+ ([0-9]+\.?[0-9]?){1} \w+/\1/p")
LOAD_MAX=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Rating Power\.+ ([0-9]+\.?[0-9]?){1} \w+/\1/p")
VOLTAGE_IN=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Utility Voltage\.+ ([0-9]+\.?[0-9]?){1} \w+/\1/p")
VOLTAGE_OUT=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Output Voltage\.+ ([0-9]+\.?[0-9]?){1} \w+/\1/p")
CAPACITY=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Battery Capacity\.+ ([0-9]+\.?[0-9]?){1} %/\1/p")
REMAINING_TIME=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Remaining Runtime\.+ ([0-9]+\.?[0-9]?){1} \w+\./\1/p")
LOAD=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Load\.+ ([0-9]+\.?[0-9]?){1} Watt\(([0-9]+\.?[0-9]?){1} %\)/\1/p")
LOAD_PCT=$(echo "$PWRSTAT_OUT" | sed -rn "s/\s*Load\.+ ([0-9]+\.?[0-9]?){1} Watt\(([0-9]+\.?[0-9]?){1} %\)/\2/p")

echo $VOLTAGE_RATING
echo $LOAD_MAX
echo $VOLTAGE_IN
echo $VOLTAGE_OUT
echo $CAPACITY
echo $REMAINING_TIME
echo $LOAD
echo $LOAD_PCT

echo "power.ups.$NAME_NAME.voltage_rating:$VOLTAGE_RATING|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
echo "power.ups.$NAME_NAME.load_max:$LOAD_MAX|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
echo "power.ups.$NAME_NAME.voltage_in:$VOLTAGE_IN|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
echo "power.ups.$NAME_NAME.voltage_out:$VOLTAGE_OUT|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
echo "power.ups.$NAME_NAME.capcity:$CAPACITY|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
echo "power.ups.$NAME_NAME.remaining_time:$REMAINING_TIME|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
echo "power.ups.$NAME_NAME.load:$LOAD|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
echo "power.ups.$NAME_NAME.load_percent:$LOAD_PCT|g" | nc -w 1 -u $STATSD_IP $STATSD_PORT
