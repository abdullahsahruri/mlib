#!/usr/bin/env python3

import re
import itertools

# Define Wmin and Wmax values
Wmin = 120e-9  # gpdk045 minimum width in meters (replace with actual value)
Wmax = 540e-9  # Maximum width in meters

# Define a subset of 5 width values between Wmin and Wmax
widths = [Wmin, 180e-9, 260e-9, 390e-9, Wmax]

# Sample netlist as a string
netlist = """
.SUBCKT DFFX1 CK D Q QN VDD VSS
*.PININFO CK:I D:I VDD:I VSS:I Q:O QN:O
Mmn26 n20 CKb n21 VSS g45n1svt m=1 l=45n w=145n
Mmn25 n21 D VSS VSS g45n1svt m=1 l=45n w=145n
Mmn57 QN qint VSS VSS g45n1svt m=1 l=45n w=260n
Mmn55 Q qbint VSS VSS g45n1svt m=1 l=45n w=260n
Mmn50 n35 qbint VSS VSS g45n1svt m=1 l=45n w=145n
Mmn51 n30 CKb n35 VSS g45n1svt m=1 l=45n w=145n
Mmn35 n25 mout VSS VSS g45n1svt m=1 l=45n w=145n
Mmn36 n20 CKbb n25 VSS g45n1svt m=1 l=45n w=145n
Mmn20 CKb CK VSS VSS g45n1svt m=1 l=45n w=145n
Mmn45 qbint n30 VSS VSS g45n1svt m=1 l=45n w=145n
Mmn56 qint qbint VSS VSS g45n1svt m=1 l=45n w=145n
Mmn21 CKbb CKb VSS VSS g45n1svt m=1 l=45n w=145n
Mmn30 mout n20 VSS VSS g45n1svt m=1 l=45n w=145n
Mmn40 n30 CKbb mout VSS g45n1svt m=1 l=45n w=145n
Mmp26 n20 CKbb n22 VDD g45p1svt m=1 l=45n w=215n
Mmp25 n22 D VDD VDD g45p1svt m=1 l=45n w=215n
Mmp51 n30 CKbb n36 VDD g45p1svt m=1 l=45n w=215n
Mmp50 n36 qbint VDD VDD g45p1svt m=1 l=45n w=215n
Mmp57 QN qint VDD VDD g45p1svt m=1 l=45n w=390n
Mmp55 Q qbint VDD VDD g45p1svt m=1 l=45n w=390n
Mmp35 n26 mout VDD VDD g45p1svt m=1 l=45n w=215n
Mmp36 n20 CKb n26 VDD g45p1svt m=1 l=45n w=215n
Mmp20 CKb CK VDD VDD g45p1svt m=1 l=45n w=215n
Mmp45 qbint n30 VDD VDD g45p1svt m=1 l=45n w=215n
Mmp56 qint qbint VDD VDD g45p1svt m=1 l=45n w=215n
Mmp21 CKbb CKb VDD VDD g45p1svt m=1 l=45n w=215n
Mmp40 n30 CKb mout VDD g45p1svt m=1 l=45n w=215n
Mmp30 mout n20 VDD VDD g45p1svt m=1 l=45n w=215n
.ENDS
"""

# Function to generate the first 10 width combinations and write them to .sp files
def generate_netlists(netlist, widths, num_files=10):
    # Find all instances of width (w=...)
    mosfets = re.findall(r"w=(\d+n)", netlist)

    # Create all possible combinations of widths for the MOSFETs
    width_combinations = itertools.product(widths, repeat=len(mosfets))

    # Loop over each combination and generate netlists (limit to the first `num_files`)
    for idx, width_combination in enumerate(width_combinations):
        if idx >= num_files:
            break
        modified_netlist = netlist
        for original_width, new_width in zip(mosfets, width_combination):
            modified_netlist = re.sub(r'w=\d+n', f'w={int(new_width * 1e9)}n', modified_netlist, 1)
        
        # Generate filename for each netlist
        filename = f"DFFX1_{idx}.sp"
        
        # Write the modified netlist to a file
        with open(filename, 'w') as file:
            file.write(modified_netlist)
        print(f"Netlist written to {filename}")

# Generate only the first 10 netlists with varying widths. Change num_files if you want to increase or decrease this variation.
generate_netlists(netlist, widths, num_files=10)

