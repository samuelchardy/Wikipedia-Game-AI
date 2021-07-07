
FOR %%x IN (0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9) DO (
    mkdir Data\epct\epct-%%x-1-18\Data_1
    python Main.py Data/epct/epct-%%x-1-18/Data_1/ 18 %%x 100 EPCT
)

FOR %%x IN (6 9 15 18 24 27 33 36) DO (
    mkdir Data\uct\uct--10-%%x\Data_1
    python WikiGame.py Data/uct/uct- -10-%%x/Data_1/ %%x 0.9 100 UCT
)