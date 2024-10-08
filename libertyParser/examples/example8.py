#!/usr/bin/env python3

import re
import pandas as pd
from libertyParser import libertyParser

# Common functions to parse Liberty file data
def parse_liberty_list(liberty_string):
    if not liberty_string:
        return []
    liberty_string = re.sub(r'[\(\)"\']', '', liberty_string)
    return [float(x.strip()) for x in liberty_string.split(',') if x.strip()]

def parse_liberty_values(values_data):
    if not values_data:
        return []
    if isinstance(values_data, str):
        values_data = values_data.strip()
        if values_data.startswith('(') and values_data.endswith(')'):
            values_data = values_data[1:-1]

        lines = re.findall(r'"([^"]*)"', values_data, re.MULTILINE)
        values = []
        for line in lines:
            row_values = [float(x.strip()) for x in line.split(',') if x.strip()]
            values.append(row_values)
        return values
    else:
        return []

# First function to extract setup/hold times and CLK-to-Q delays
def extract_setup_hold_clkq_times(libFile, cell_name, clock_pin, data_pin, output_pin):
    myLibertyParser = libertyParser(libFile)
    libPinInfo = myLibertyParser.getLibPinInfo(cellList=[cell_name], pinList=[clock_pin, data_pin, output_pin])
    timing_data = []

    for pin_name in [clock_pin, data_pin]:
        pin_info = libPinInfo['cell'][cell_name]['pin'].get(pin_name, {})
        timing_arcs = pin_info.get('timing', [])
        for timing_arc in timing_arcs:
            timing_type = timing_arc.get('timing_type', '')
            related_pin = timing_arc.get('related_pin', '')
            if timing_type in ['setup_rising', 'hold_rising', 'setup_falling', 'hold_falling']:
                when_condition = timing_arc.get('when', '')
                table_types = timing_arc.get('table_type', {})
                for table_type, table_data in table_types.items():
                    if table_type in ['rise_constraint', 'fall_constraint']:
                        index_1 = table_data.get('index_1', '')
                        index_2 = table_data.get('index_2', '')
                        values = table_data.get('values', '')
                        index_1_list = parse_liberty_list(index_1)
                        index_2_list = parse_liberty_list(index_2)
                        values_table = parse_liberty_values(values)

                        if len(values_table) != len(index_1_list):
                            print(f"Warning: Mismatch in values table dimensions for {table_type}. Skipping.")
                            continue
                        for i, idx1 in enumerate(index_1_list):
                            for j, idx2 in enumerate(index_2_list):
                                value = values_table[i][j]
                                # Switch clock_slew and data_slew here
                                timing_data.append({
                                    'timing_type': timing_type,
                                    'related_pin': related_pin,
                                    'when': when_condition,
                                    'table_type': table_type,
                                    'data_slew/output_capacitance': idx2,  # Use output capacitance for data_slew column
                                    'clk_slew': idx1,  # Use clk_slew for clock pin
                                    'constraint_value': value
                                })
    return timing_data

# Second function to extract CLK-to-Q delays
def extract_clk_to_q_delays(libFile, cell_name, clock_pin, output_pin):
    myLibertyParser = libertyParser(libFile)
    libPinInfo = myLibertyParser.getLibPinInfo(cellList=[cell_name], pinList=[clock_pin, output_pin])
    timing_data = []

    for pin_name in [clock_pin, output_pin]:
        pin_info = libPinInfo['cell'][cell_name]['pin'].get(pin_name, {})
        timing_arcs = pin_info.get('timing', [])
        for timing_arc in timing_arcs:
            timing_type = timing_arc.get('timing_type', '')
            related_pin = timing_arc.get('related_pin', '')
            if timing_type in ['rising_edge', 'falling_edge']:
                when_condition = timing_arc.get('when', '')
                table_types = timing_arc.get('table_type', {})
                for table_type, table_data in table_types.items():
                    if table_type in ['cell_rise', 'cell_fall']:
                        index_1 = table_data.get('index_1', '')
                        index_2 = table_data.get('index_2', '')
                        values = table_data.get('values', '')
                        index_1_list = parse_liberty_list(index_1)
                        index_2_list = parse_liberty_list(index_2)
                        values_table = parse_liberty_values(values)

                        if len(values_table) != len(index_1_list):
                            print(f"Warning: Mismatch in values table dimensions for {table_type}. Skipping.")
                            continue
                        for i, idx1 in enumerate(index_1_list):
                            for j, idx2 in enumerate(index_2_list):
                                value = values_table[i][j]
                                # Switch clock_slew and data_slew here
                                timing_data.append({
                                    'timing_type': timing_type,
                                    'related_pin': related_pin,
                                    'when': when_condition,
                                    'table_type': table_type,
                                    'data_slew/output_capacitance': idx2,  # Use output capacitance for data_slew column
                                    'clk_slew': idx1,  # Use clk_slew for clock pin
                                    'constraint_value': value
                                })
    return timing_data

def main():
    libFile = 'DFFX1.lib'
    cell_name = 'DFFX1'
    clock_pin = 'CK'
    data_pin = 'D'
    output_pin = 'Q'

    # Extract setup/hold times and CLK-to-Q delays
    setup_hold_data = extract_setup_hold_clkq_times(libFile, cell_name, clock_pin, data_pin, output_pin)
    clk_to_q_data = extract_clk_to_q_delays(libFile, cell_name, clock_pin, output_pin)

    # Merge both data sets
    all_timing_data = setup_hold_data + clk_to_q_data

    # Convert to DataFrame and save to CSV with modified header
    df = pd.DataFrame(all_timing_data)
    df.to_csv('timing_data_modified.csv', index=False)
    print('Modified timing data saved to "timing_data_modified.csv"')

if __name__ == '__main__':
    main()

