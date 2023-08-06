""" SETTINGS

This scripts defines standard settings NOT to be changed

Date: February 1, 2022
"""
#------------------------------------------------------------------------------
# LIBRARIES
#------------------------------------------------------------------------------
import pandas as pd

#------------------------------------------------------------------------------
# GLOBAL PARAMETERS
#------------------------------------------------------------------------------
class Globals():
    """ Global variables across scripts
        
    """
    # --------------------
    # Constructor function
    # --------------------
    def __init__(self):
        
        ## Set parameters
        
        # FORMATS
        self.DATE_FORMAT = "%Y-%m-%d"
        self.ENCODING = "utf-8"
        
        # Dateparser
        self.DATE_PARSER  = lambda x: pd.to_datetime(x, format = self.DATE_FORMAT)

        # Important columns 
        self.DB_COL = "DB"
        self.DATE_COL = "Date"
        self.ONET_COL = "O*NET-SOC Code"
        
    
        
        
        
        
        