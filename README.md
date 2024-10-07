
After running ./run2.csh in /trio_flow/, the target lib file is generated in:
/home/C00535644/projects/liberatews/trio_flow/char_gpdk_NOM/ldb.ldb.4.gz/tt_1p1v_25c/LIBS/DFFX1::gpdk_tt_1p1v_25c.lib

Next steps:
1) Check out the DFFX1.sp netlist in /gpdk/netlists/
2) Work on varying the dimensions of W and L in the netlist. Don't go crazy, switch between three paramters.
3) Take into account the Wmin-Wmax and Lmin-Lmax that is in the netlist. Lmin and Wmin being the minimum W and L dimensions provided by the foundry (gpdk).
4) The out from the ML model should give the following:

| Corners     | Setup_rising | Setup_rising | Hold_rising | Hold_falling | CLK-Q Delay | W (of every MOS) | L (of every MOS) |
| :---------: |:------------:|:------------:|:-----------:|:------------:|:-----------:|:----------------:|:----------------:|
| Conrer #1   | float        | float        | float       | float        | float       | float            | float            |
| Conrer #2   | float        | float        | float       | float        | float       | float            | float            |
| ...         | float        | float        | float       | float        | float       | float            | float            |
| ...         | float        | float        | float       | float        | float       | float            | float            |
| Conrer #N   | float        | float        | float       | float        | float       | float            | float            |
