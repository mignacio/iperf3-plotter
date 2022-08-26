import matplotlib.pyplot as plt
import datetime
import json
import sys
import os
import glob
import traceback
import logging

def plot_iperf_json(input_file_name, output_file_name):
    with open(input_file_name) as json_file:
        try:
            json_data = json.load(json_file)
        except Exception:
            logging.error(traceback.format_exc())
            return

    time_intervals = json_data['intervals']
    time_intervals_sum = [item['sum'] for item in time_intervals]

    date = json_data['start']['timestamp']['timesecs']
    date = datetime.datetime.fromtimestamp(date)

    # start_time = [int(item['start']) for item in time_intervals_sum]
    end_time = [int(item['end']) for item in time_intervals_sum]
    total_bytes = [item['bytes'] / 1000000 for item in time_intervals_sum]
    bits_per_second = [item['bits_per_second'] / 1000000 for item in time_intervals_sum]

    plt.figure()
    plt.title(f'{input_file_name}\nThroughput vs Time')
    plt.subplots_adjust(bottom=0.2)
    plt.plot(end_time, bits_per_second)
    plt.xlabel(f"Time[s]\n{date.strftime('%d-%m-%y %H:%M')}")
    plt.ylabel('Throughput[Mbits/s]')
    plt.grid()
    plt.savefig(f'{output_file_name}_throughput.png')

    plt.figure()
    plt.title(f'{input_file_name}\nTotal megabytes transferred vs. Time')
    plt.subplots_adjust(bottom=0.2)
    plt.plot(end_time, total_bytes)
    plt.xlabel(f"Time[s]\n{date.strftime('%d-%m-%y %H:%M')}")
    plt.ylabel('Data transferred[Megabytes]')
    plt.grid()
    plt.savefig(f'{output_file_name}_total_bytes.png')

if len(sys.argv) <= 1:
    print("No arguments provided, plotting all .json files inside directory.\n")
    for filename in glob.glob('*.json'):
        output_file_name=os.path.splitext(filename)[0]
        print(f"Now attempting to plot {filename} to {output_file_name}\n")
        plot_iperf_json(filename, output_file_name)
else:
    input_file_name = sys.argv[1]
    output_file_name = os.path.splitext(input_file_name)[0]
    plot_iperf_json(input_file_name, output_file_name)

print('Completed.')
