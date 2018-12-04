import argparse
import csv
import sys

import requests


SOLARSHED_METRIC_NAMES = [
    "solarshed_battery_percentage",
    "solarshed_battery_temperature_celsius",
    "solarshed_battery_volts",
    "solarshed_controller_charging_state",
    "solarshed_controller_temperature_celsius",
    "solarshed_load_amperes",
    "solarshed_load_power_watts",
    "solarshed_load_volts",
    "solarshed_solar_amperes",
    "solarshed_solar_volts",
    "solarshed_solar_watts"    
]


def export_metrics(base_url):

    writer = csv.writer(sys.stdout)
    writer.writerow(['instance', 'job', 'name', 'timestamp', 'value'])

    for metric in SOLARSHED_METRIC_NAMES:
        response = requests.get(f'{base_url}/api/v1/query', params={'query': f'{metric}[1y]'})
        results = response.json()['data']['result']

        for result in results:
            row = [metric]
            instance = result['metric'].get('instance', '')
            job = result['metric'].get('job', '')

            for timestamp, value in result['values']:
                row = [instance, job, metric, timestamp, value]
                writer.writerow(row)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Export solarshed metrics from prometheus')
    parser.add_argument('--base-url', dest='base_url', default='http://localhost:9090',
                        help='the base URL for the prometheus API')
    args = parser.parse_args()    
    export_metrics(args.base_url)
