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
    # values_data can be a string or a list
    if not values_data:
        return []
    if isinstance(values_data, list):
        # values_data is a list of strings, each representing a row
        values = []
        for row in values_data:
            row = row.strip()
            row = re.sub(r'[\(\)"\']', '', row)
            row_values = [float(x.strip()) for x in row.split(',') if x.strip()]
            values.append(row_values)
        return values
    elif isinstance(values_data, str):
        # values_data is a single string
        values_data = values_data.strip()
        values_data = re.sub(r'[\(\)"\']', '', values_data)
        if '\\' in values_data:
            # Multiple rows
            rows = values_data.split('\\')
            values = []
            for row in rows:
                row = row.strip()
                if not row:
                    continue
                row_values = [float(x.strip()) for x in row.split(',') if x.strip()]
                values.append(row_values)
            return values
        else:
            # Single row
            row_values = [float(x.strip()) for x in values_data.split(',') if x.strip()]
            return [row_values]
    else:
        # Unexpected format
        return []

def extract_setup_hold_times(libFile, cell_name, pin_name):
    # Create an instance of libertyParser
    myLibertyParser = libertyParser(libFile)

    # Extract pin information
    libPinInfo = myLibertyParser.getLibPinInfo(cellList=[cell_name], pinList=[pin_name])

    # Access the pin information
    pin_info = libPinInfo['cell'][cell_name]['pin'][pin_name]

    # Access the timing arcs
    timing_arcs = pin_info.get('timing', [])

    # Extract setup and hold times
    setup_hold_times = []

    for timing_arc in timing_arcs:
        timing_type = timing_arc.get('timing_type', '')
        if timing_type in ['setup_rising', 'hold_rising', 'setup_falling', 'hold_falling']:
            related_pin = timing_arc.get('related_pin', '')
            when_condition = timing_arc.get('when', '')
            table_types = timing_arc.get('table_type', {})

            # The constraint tables are under 'rise_constraint' or 'fall_constraint'
            for table_type, table_data in table_types.items():
                if table_type in ['rise_constraint', 'fall_constraint']:
                    index_1 = table_data.get('index_1', '')
                    index_2 = table_data.get('index_2', '')
                    values = table_data.get('values', '')

                    # Parse indexes and values
                    index_1_list = parse_liberty_list(index_1)
                    index_2_list = parse_liberty_list(index_2)
                    values_table = parse_liberty_values(values)

                    # Debug statements
                    print(f"\nProcessing timing arc: timing_type={timing_type}, table_type={table_type}")
                    print(f"index_1_list ({len(index_1_list)}): {index_1_list}")
                    print(f"index_2_list ({len(index_2_list)}): {index_2_list}")
                    print(f"Raw values ({type(values)}): {values}")
                    print(f"values_table ({len(values_table)} rows):")
                    for idx, row in enumerate(values_table):
                        print(f"  Row {idx} ({len(row)} columns): {row}")

                    # Verify dimensions
                    if len(values_table) != len(index_1_list):
                        print(f"Warning: Number of rows in values_table ({len(values_table)}) does not match index_1_list ({len(index_1_list)}). Skipping this timing arc.")
                        continue

                    dimension_mismatch = False
                    for idx, row in enumerate(values_table):
                        if len(row) != len(index_2_list):
                            print(f"Warning: Number of columns in values_table row {idx} ({len(row)}) does not match index_2_list ({len(index_2_list)}). Skipping this timing arc.")
                            dimension_mismatch = True
                            break
                    if dimension_mismatch:
                        continue

                    # Collect the data
                    for i, idx1 in enumerate(index_1_list):
                        for j, idx2 in enumerate(index_2_list):
                            value = values_table[i][j]
                            setup_hold_times.append({
                                'timing_type': timing_type,
                                'related_pin': related_pin,
                                'when': when_condition,
                                'table_type': table_type,
                                'data_slew': idx1,
                                'clock_slew': idx2,
                                'constraint_value': value
                            })
    return setup_hold_times

def main():
    # Specify your Liberty file and cell/pin names
    libFile = 'DFFX1.lib'
    cell_name = 'DFFX1'
    pin_name = 'D'

    # Extract setup and hold times
    setup_hold_times = extract_setup_hold_times(libFile, cell_name, pin_name)

    # Convert to DataFrame
    df = pd.DataFrame(setup_hold_times)
    print(df.head())

    # Save to CSV
    df.to_csv('setup_hold_times.csv', index=False)
    print('Setup and hold times saved to "setup_hold_times.csv"')

if __name__ == '__main__':
    main()

