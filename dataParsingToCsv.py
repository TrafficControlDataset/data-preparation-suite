"""
Author: Alexander Genser
Date: 2023-03-06
Module Name: data_parsing_csv.py
Description: This script analyzes the data of a signal control system that 
				logs the states of loop detectors and traffic signals. The 
				log files contain event messages based on a specific 
				proprietary protocol. 
			
			The regular expressions are not detailed here to preserve the 
				protocol definition, which is not publicly available. 
				Nevertheless, the user can easily fill in/modify the 
				expressions according to the protocol at hand.
Usage:
    python data_parsing_csv.py 

Example:
    python script.py -f input.txt -o output.txt
"""

#importing libraries
import pandas as pd
import re
from csv import writer 
import io
from os import listdir
from os.path import isfile, join

# Definition of protocol with regular expressions (as mentioned here the user should 
# fill in the relevant details to parse an event); the used protocol here is not public.
re_event_type = r'***'  # Type of event message.
re_time = r'***'  # Definition of datetime.
re_event_trigger = r'***'  # Unique identifier for what triggered the event.
re_intersection = r'***'  # Unique identifier of intersection.
re_device = r'***'  # Unique identifier for detector or traffic signal.
re_id = r'***'  # Unique device identifier.
re_device_state = r'***'  # Device state.

# Path pointing to raw log-files and output path for parsed files (depending on OS this might have to be changed).
data_path = '.\\data'
out_path = '.\\output'
double_backslash = '\\'

# Get files names from log-file directory.
files = [file for file in listdir(data_path) if isfile(join(data_path, file))]

lines = []
file_count = 1

# Iterate over all logs in data structure files and parse information
for file_name in files:
    print("process file #" + str(file_count) + " from " + str(len(files)))
    stream = io.StringIO()
    csv_writer = writer(stream)
    df = []
    
    # working on particular file and parsing
    open_path = data_path + double_backslash + file_name 
    with open(open_path) as file:
        # splitting lines and getting number of rows to iterate through
        # all lines in log
        lines = file.read().splitlines()
        num_of_rows = len(lines)

        for i in range(1, num_of_rows):
            line = str(lines[i])
            check_line = str(lines[i - 1])

            # if event is containing new state information
            if not bool(re.search("VST", check_line)):
                node_ids = re.findall(re_intersection, line)
                num_of_nodes = len(re.findall(re_intersection, line))

                # for all intersections contained in event get state change information
                for node_count in range(0, num_of_nodes):
                    event_type = re.search(re_event_type, line).group(0)
                    date = re.search(re_time, line).group(0)
                  
                    # get event type
                    if event_type != 'VST':
                        TTG = re.search(re_event_trigger, line).group(0)
                    else:
                        TTG = 'NaN'

                    # get node and device type
                    node = node_ids[node_count]
                    device = re.findall(re_device, line)[node_count]

                    if device == 'd':
                        device = 'Detector' 
                    else:
                        device = 'TrafficSignal'

                    # get device id and state value
                    device_id = re.findall(re_id, line)[node_count]
                    state_value = re.findall(re_device_state, line)[node_count]

                    # build row with gathered data
                    row = ([event_type.encode('utf-8'), date.encode('utf-8'), TTG.encode('utf-8'),
                            node.encode('utf-8'), device.encode('utf-8'), device_id.encode('utf-8'),
                            state_value.encode('utf-8')])

                    # write row to csv object
                    csv_writer.writerow(row)

        # setting position of stream, building data frame, writing header to file
        stream.seek(0)
        len_file_name_extension = 4
        df = pd.DataFrame(columns=['DVIS', 'Time', 'TTG', 'node', 'device', 'device_id', 'state_value'])
        df = pd.read_csv(stream, encoding='ASCII')

        out_path = out_path + double_backslash + 'T_' + file_name[:-len_file_name_extension] + '.csv'
        df.to_csv(out_path,
                header=['DVIS', 'Time', 'TTG', 'node', 'device', 'device_id', 'state_value'])

        # open output files and add lines
        writeLineToFile(out_path)
        with open(out_path) as f:
            lines = f.read().splitlines()
            for i in range(0, len(lines)):
                s = lines[i]
                s = s.replace("b'", "")
                s = s.replace("'", "")
                lines[i] = s

            f.close()
            with open(out_path, 'w') as fr:
                for item in lines:
                    fr.write("%s\n" % item)
            fr.close()
    file_count += 1