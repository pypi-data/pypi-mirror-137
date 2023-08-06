#------------------------------------------------------------------------------
# Libraries
#------------------------------------------------------------------------------
# Standard
import os
import pandas as pd
import shutil
import zipfile
import re
import pathlib
from bodyguard import tools
from collections import Counter

# From library
from ..settings import Globals
G = Globals()

#------------------------------------------------------------------------------
# Dates for O*NET databases
#------------------------------------------------------------------------------

class Dates(object):
    """
    This class provides the dates of the O*NET databases
    """
    # -------------------------------------------------------------------------
    # Constructor function
    # -------------------------------------------------------------------------
    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    # Public functions
    # -------------------------------------------------------------------------
    def get_dates(self):
        """
        Get dates of databases according to: 
        """
        dates = {
            'db_4_0':'2002-06-01',
            'db_5_0':'2003-04-01',
            'db_5_1':'2003-11-01',
            'db_6_0':'2004-07-01',
            'db_7_0':'2004-12-01',
            'db_8_0':'2005-06-01',
            'db_9_0':'2005-12-01',   
            'db_10_0':'2006-06-01',
            'db_11_0':'2006-12-01',
            'db_12_0':'2007-06-01',
            'db_13_0':'2008-06-01',
            'db_14_0':'2009-06-01',
            'db_15_0':'2010-07-01',
            'db_15_1':'2011-02-01',
            'db_16_0':'2011-07-01',
            'db_17_0':'2012-07-01',
            'db_18_0':'2013-07-01',
            'db_18_1':'2014-03-01',
            'db_19_0':'2014-07-01',
            'db_20_0':'2015-08-01',
            'db_20_1':'2015-10-01',
            'db_20_2':'2016-02-01',
            'db_20_3':'2016-04-01',
            'db_21_0':'2016-08-01',
            'db_21_1':'2016-11-01',
            'db_21_2':'2017-02-01',
            'db_21_3':'2017-05-01',
            'db_22_0':'2017-08-01',
            'db_22_1':'2017-10-01',
            'db_22_2':'2018-02-01',
            'db_22_3':'2018-05-01',
            'db_23_0':'2018-08-01',
            'db_23_1':'2018-11-01',
            'db_23_2':'2019-02-01',
            'db_23_3':'2019-05-01',
            'db_24_0':'2019-08-01',
            'db_24_1':'2019-11-01',
            'db_24_2':'2020-02-01',
            'db_24_3':'2020-05-01',
            'db_25_0':'2020-08-01',
            'db_25_1':'2020-11-01',
            'db_25_2':'2021-02-01',
            'db_25_3':'2021-05-01',
            'db_26_0':'2021-08-01',
            'db_26_1':'2021-11-01',
            }
        
        df_dates = pd.DataFrame().from_dict(dates,orient='index',columns=[G.DATE_COL])
        df_dates.index.name = G.DB_COL
        df_dates.reset_index(inplace=True)
        
        # Convert the 'Date' column to datetime format
        df_dates[G.DATE_COL] = pd.to_datetime(df_dates[G.DATE_COL], format = G.DATE_FORMAT)
        
        # Sort
        df_dates.sort_values(by=[G.DATE_COL], axis=0, ascending=True, inplace=True)
               
        return df_dates
        


        
        
        














