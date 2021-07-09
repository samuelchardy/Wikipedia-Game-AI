
FOR %%x IN (3 6 9 15 18 24 27 33 36) DO (
    mkdir "Data/SDSU-rbrp/epct-0.1-1-%%x/Data_1"
    python Main.py Data/SDSU-rbrp/epct-0.1-1-%%x/Data_1/ %%x 0.1 25 EPCT
)