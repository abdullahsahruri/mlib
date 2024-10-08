#!/usr/bin/env python3

import re
import pandas as pd
from libertyParser import libertyParser

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

def extract_setup_hold_clkq_times(libFile, cell_name, clock_pin, output_pin):
    # Create an instance of libertyParser
    myLibertyParser = libertyParser(libFile)

    # Extract pin information
    libPinInfo = myLibertyParser.getLibPinInfo(cellList=[cell_name], pinList=[clock_pin, output_pin])

    # Access the pin information
    timing_data = []

    # Check timing arcs for both clock and output pins
    for pin_name in [clock_pin, output_pin]:
        pin_info = libPinInfo['cell'][cell_name]['pin'].get(pin_name, {})

        # Access the timing arcs
        timing_arcs = pin_info.get('timing', [])

        for timing_arc in timing_arcs:
            timing_type = timing_arc.get('timing_type', '')
            related_pin = timing_arc.get('related_pin', '')

            # Check for CLK-to-Q delay types
            if timing_type in ['rising_edge', 'falling_edge', 'setup_rising', 'hold_rising', 'setup_falling', 'hold_falling']:
                when_condition = timing_arc.get('when', '')
                table_types = timing_arc.get('table_type', {})

                for table_type, table_data in table_types.items():
                    if table_type in ['rise_constraint', 'fall_constraint', 'cell_rise', 'cell_fall']:
                        index_1 = table_data.get('index_1', '')
                        index_2 = table_data.get('index_2', '')
                        values = table_data.get('values', '')

                        # Parse indexes and values
                        index_1_list = parse_liberty_list(index_1)
                        index_2_list = parse_liberty_list(index_2)
                        values_table = parse_liberty_values(values)

                        # Verify dimensions
                        if len(values_table) != len(index_1_list):
                            print(f"Warning: Number of rows in values_table does not match index_1_list. Skipping this timing arc.")
                            continue

                        for i, idx1 in enumerate(index_1_list):
                            for j, idx2 in enumerate(index_2_list):
                                value = values_table[i][j]
                                timing_data.append({
                                    'timing_type': timing_type,
                                    'related_pin': related_pin,
                                    'when': when_condition,
                                    'table_type': table_type,
                                    'data_slew': idx1,
                                    'clock_slew': idx2,
                                    'constraint_value': value
                                })

    return timing_data

def main():
    # Specify your Liberty file and cell/pin names
    libFile = 'DFFX1.lib'
    cell_name = 'DFFX1'
    clock_pin = 'CK'
    output_pin = 'Q'

    # Extract setup, hold times and CLK-to-Q delay
    timing_data = extract_setup_hold_clkq_times(libFile, cell_name, clock_pin, output_pin)

    # Convert to DataFrame
    df = pd.DataFrame(timing_data)
    print(df.head())

    # Save to CSV
    df.to_csv('timing_data.csv', index=False)
    print('Timing data (setup, hold, CLK-to-Q) saved to "timing_data.csv"')

if __name__ == '__main__':
    main()

