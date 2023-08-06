#------------------------------------------------------------------------------
# Libraries
#------------------------------------------------------------------------------
from bodyguard import tools

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
def standardize_scores(x, minimum, maximum):
    """
    Create standardized O*NET scores
    """
    
    if (not isinstance(minimum, int)) and (not isinstance(minimum, float)):
    # Convert to arrays
        minimum = minimum.to_numpy()
    if (not isinstance(maximum, int)) and (not isinstance(maximum, float)):
        maximum = maximum.to_numpy()
    
    x_standardized = (x - minimum) / (maximum - minimum)
    
    return x_standardized


def get_tasks(scale_name,
              scale_id,
              scales_lookup,
              ratings,
              id_cols):
    """
    

    Parameters
    ----------
    scale_name : str
        Name of scale, i.e. "Relevance", "Impotance", or "Frequency"
    scale_id : str
        Corresponding scale id, i.e., "RT", "IM", "FT"
    scales_lookup : pd.DataFrame
        All scales
    ratings : pd.DataFrame
        All ratings
    id_cols : list
        Cols to match occupations on.

    Returns
    -------
    pd.DataFrame

    """
    # Locate minimum and maximum
    scale_extrema = scales_lookup.loc[scales_lookup["Scale ID"] == scale_id,
                                      ["Minimum", "Maximum"]]
    
    if tools.isin(a=scale_id, b=["RT", "IM"]):
        
        # Extract tasks
        df_task_temp = ratings.loc[ratings["Scale ID"] == scale_id,
                                   id_cols+["Data Value"]]
        
        # Remove duplicates on ID (should not have an effect)
        df_task_temp.drop_duplicates(subset=id_cols,
                                     keep="first",
                                     inplace=True)
        
        # Construct standardized score
        df_task_temp[scale_name] = standardize_scores(x=df_task_temp["Data Value"],
                                                      minimum=scale_extrema["Minimum"],
                                                      maximum=scale_extrema["Maximum"])
        
        # Remove original scale
        df_task_temp.drop(columns="Data Value",
                          inplace=True,
                          errors="raise")
        
    elif tools.isin(a=scale_id, b=["FT"]):
        
        # Extract
        df_task_temp = ratings.loc[ratings["Scale ID"] == scale_id,
                                   id_cols+["Category","Data Value"]]
    
        # Remove duplicates on ID and category
        df_task_temp.drop_duplicates(subset=id_cols+["Category"],
                                     keep="first",
                                     inplace=True)
    
        # Define grouper
        grouper_sum = df_task_temp.groupby(by=id_cols)["Data Value"].sum().round()
    
        if grouper_sum.nunique()==1:
            scale_sum = grouper_sum.iloc[0]
        else:
            raise Exception("Frequnecy summation is not unique by group")
            
        # Product between frequency and weight
        df_task_temp["Product"] = df_task_temp["Category"].multiply(df_task_temp["Data Value"].divide(scale_sum))
    
        # Sum product by ID
        df_task_temp_sum = df_task_temp.groupby(by=id_cols,
                                                axis=0,
                                                as_index=False,
                                                sort=False,
                                                dropna=True)["Product"].sum()
        
        # Construct standardized score (categories range from 1 to 7)
        df_task_temp_sum[scale_name] = standardize_scores(x=df_task_temp_sum["Product"],
                                                           minimum=df_task_temp["Category"].min(),
                                                           maximum=df_task_temp["Category"].max())
            
        # Remove original scale
        df_task_temp_sum.drop(columns="Product",
                          inplace=True,
                          errors='raise')
        
        # Overwrite
        df_task_temp = df_task_temp_sum.copy()

    return df_task_temp

