
After running ./run2.csh in /trio_flow/, the target lib file is generated in:
/home/C00535644/projects/liberatews/trio_flow/char_gpdk_NOM/ldb.ldb.4.gz/tt_1p1v_25c/LIBS/DFFX1::gpdk_tt_1p1v_25c.lib

Next steps:
1) Check out the DFFX1.sp netlist in /gpdk/netlists/
2) Work on varying the dimensions of W and L in the netlist. Don't go crazy, switch between three paramters.
3) Take into account the Wmin-Wmax and Lmin-Lmax that is in the netlist. Lmin and Wmin being the minimum W and L dimensions provided by the foundry (gpdk).
4) The out from the ML model should give the following:

| Corners     | Setup_rising | Setup_rising | Hold_rising | Hold_falling | CLK-Q Delay | W (of every MOS) | L (of every MOS) |
| :---------: |:------------:|:------------:|:-----------:|:------------:|:-----------:|:----------------:|:----------------:|
| Corner #1   | float        | float        | float       | float        | float       | float            | float            |
| Corner #2   | float        | float        | float       | float        | float       | float            | float            |
| ...         | float        | float        | float       | float        | float       | float            | float            |
| ...         | float        | float        | float       | float        | float       | float            | float            |
| Corner #N   | float        | float        | float       | float        | float       | float            | float            |


|  Corners  | Setup\_rising | Setup\_falling | Hold\_rising | Hold\_falling | CLK-Q Delay | W (of every MOS)     | L (of every MOS) |
|:---------:|:-------------:|:--------------:|:------------:|:-------------:|:-----------:|:--------------------:|:----------------:|
| Corner #1 |     45 ps     |      42 ps     |    30 ps     |     25 ps     |   100 ps    | 145n, 260n, 215n,...  | 45n, 45n, 45n,...|
| Corner #2 |     50 ps     |      45 ps     |    32 ps     |     28 ps     |   110 ps    | 150n, 265n, 220n,...  | 45n, 45n, 45n,...|
| Corner #3 |     55 ps     |      50 ps     |    35 ps     |     30 ps     |   120 ps    | 160n, 270n, 230n,...  | 45n, 45n, 45n,...|
|   ...     |      ...      |       ...      |     ...      |      ...      |     ...     |         ...          |       ...        |
| Corner #N |     float     |      float     |    float     |     float     |   float     |      float (W values)|    float (L values)|

### Explanation:
- **Corners**: Represents different PVT corner combinations.
- **Setup\_rising/Setup\_falling**: Setup times for rising and falling clock edges.
- **Hold\_rising/Hold\_falling**: Hold times for rising and falling clock edges.
- **CLK-Q Delay**: The delay from clock to Q.
- **W (of every MOS)**: A list of widths for each MOSFET in the netlist.
- **L (of every MOS)**: The length values, which are constant (e.g., 45n for each transistor).
