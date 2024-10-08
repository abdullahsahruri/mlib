
.SUBCKT DFFX1 CK D Q QN VDD VSS
*.PININFO CK:I D:I VDD:I VSS:I Q:O QN:O
Mmn26 n20 CKb n21 VSS g45n1svt m=1 l=45n w=119n
Mmn25 n21 D VSS VSS g45n1svt m=1 l=45n w=119n
Mmn57 QN qint VSS VSS g45n1svt m=1 l=45n w=260n
Mmn55 Q qbint VSS VSS g45n1svt m=1 l=45n w=540n
Mmn50 n35 qbint VSS VSS g45n1svt m=1 l=45n w=119n
Mmn51 n30 CKb n35 VSS g45n1svt m=1 l=45n w=540n
Mmn35 n25 mout VSS VSS g45n1svt m=1 l=45n w=540n
Mmn36 n20 CKbb n25 VSS g45n1svt m=1 l=45n w=540n
Mmn20 CKb CK VSS VSS g45n1svt m=1 l=45n w=260n
Mmn45 qbint n30 VSS VSS g45n1svt m=1 l=45n w=119n
Mmn56 qint qbint VSS VSS g45n1svt m=1 l=45n w=390n
Mmn21 CKbb CKb VSS VSS g45n1svt m=1 l=45n w=180n
Mmn30 mout n20 VSS VSS g45n1svt m=1 l=45n w=390n
Mmn40 n30 CKbb mout VSS g45n1svt m=1 l=45n w=180n
Mmp26 n20 CKbb n22 VDD g45p1svt m=1 l=45n w=390n
Mmp25 n22 D VDD VDD g45p1svt m=1 l=45n w=119n
Mmp51 n30 CKbb n36 VDD g45p1svt m=1 l=45n w=180n
Mmp50 n36 qbint VDD VDD g45p1svt m=1 l=45n w=390n
Mmp57 QN qint VDD VDD g45p1svt m=1 l=45n w=390n
Mmp55 Q qbint VDD VDD g45p1svt m=1 l=45n w=390n
Mmp35 n26 mout VDD VDD g45p1svt m=1 l=45n w=390n
Mmp36 n20 CKb n26 VDD g45p1svt m=1 l=45n w=260n
Mmp20 CKb CK VDD VDD g45p1svt m=1 l=45n w=260n
Mmp45 qbint n30 VDD VDD g45p1svt m=1 l=45n w=390n
Mmp56 qint qbint VDD VDD g45p1svt m=1 l=45n w=180n
Mmp21 CKbb CKb VDD VDD g45p1svt m=1 l=45n w=180n
Mmp40 n30 CKb mout VDD g45p1svt m=1 l=45n w=180n
Mmp30 mout n20 VDD VDD g45p1svt m=1 l=45n w=260n
.ENDS
