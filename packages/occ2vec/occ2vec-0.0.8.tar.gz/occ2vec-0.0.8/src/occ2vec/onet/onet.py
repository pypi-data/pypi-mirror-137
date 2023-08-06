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
import bodyguard as bd
from collections import Counter
import pkg_resources


# From library
from ..settings import Globals
from .dates import Dates
from .tools import (standardize_scores, get_tasks)
from ..nlp.nlp import DocumentEmbedder

# Derived
G = Globals()
#------------------------------------------------------------------------------
# Base
#------------------------------------------------------------------------------
class ONETBASE(object):
    # -------------------------------------------------------------------------
    # Constructor function
    # -------------------------------------------------------------------------
    def __init__(self,
                 verbose=True):
        self.verbose = verbose
        
        # Import dates
        self.df_dates = Dates().get_dates()
        
        # Save databases
        self.db = self.df_dates[G.DB_COL].unique().tolist()
        
        # Get location of this file        
        self.file_dir = "/".join(__file__.split("/")[:-1])+"/"
        
        # Main directory of packge
        self.main_dir = os.path.join(self.file_dir, "../")
        
        self.data_dir = os.path.join(self.main_dir, "data/")
               
#------------------------------------------------------------------------------
# Other
#------------------------------------------------------------------------------
class ONET(ONETBASE):
    # -------------------------------------------------------------------------
    # Constructor function
    # -------------------------------------------------------------------------
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)
        
    # -------------------------------------------------------------------------
    # Public functions
    # -------------------------------------------------------------------------    
    def load_onet_data(self,
                       name,
                       which_db="all"):
        """
        Load data that have already been prepared
        """
        
        # Location where data are saved
        data_dir = os.path.join(self.data_dir, f"onet_data/prepared/{name}.parquet")
        
        # Load data
        df = pd.read_parquet(path=data_dir,
                             engine='auto',
                             columns=None,
                             storage_options=None,
                             use_nullable_dtypes=False)  
        
        if which_db=="all":
            pass
        elif bd.tools.isin(a=which_db,b=self.db):
            # Mask relevant db
            mask_db = df[G.DB_COL] == which_db
            
            # Subset
            df = df.loc[mask_db]
            
        else:
            raise bd.exceptions.WrongInputException(input_name="which_db",
                                                    provided_input=which_db,
                                                    allowed_inputs=self.db) 
        
        return df



class ONETEmbedder(ONET):
    # -------------------------------------------------------------------------
    # Constructor function
    # -------------------------------------------------------------------------
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)
        
    # -------------------------------------------------------------------------
    # Public functions
    # -------------------------------------------------------------------------    
    def embed_onet_descriptors(self,
                               save_to_package_data=False,
                               which_db="all",
                               normalize=True):
        """
        Embed descriptors (tasks, attributes, and titles) from the entire O*NET
        """
        df_tasks = super().load_onet_data(name="tasks",which_db=which_db)
        df_attributes = super().load_onet_data(name="attributes",which_db=which_db)
        
        # Subset to unique tasks, attributes, and titles
        unique_tasks = df_tasks["Task description"].unique().tolist()
        unique_attributes = df_attributes["Element description"].unique().tolist()
        unique_job_descriptions = pd.concat([df_tasks["Job description"],
                                             df_attributes["Job description"]],
                                            axis=0,
                                            ignore_index=True).unique().tolist()

        # Documents
        unique_documents = unique_tasks+unique_attributes+unique_job_descriptions
        
        # Remove duplicated
        unique_documents = list(set(unique_documents))

        unique_documents = unique_documents[0:100]

        # Initializer embedder
        documentembedder = DocumentEmbedder(normalize=normalize,
                                            verbose=self.verbose,
                                            return_type="df")
        
        # Embed documents
        documents_embeddings = documentembedder.embed_documents(documents=unique_documents)
        
        if save_to_package_data:
            
            # Location where data are saved
            data_dir = os.path.join(self.data_dir, "embedding_data/")

            documents_embeddings.to_parquet(path=data_dir+"/onet_embeddings"+".parquet",
                                            engine='auto',
                                            compression='BROTLI',
                                            index=None,
                                            partition_cols=None)
            
        return documents_embeddings


class ONETPreparer(ONETBASE):
    """
    This class prepares the O*NET data
    """
    # -------------------------------------------------------------------------
    # Constructor function
    # -------------------------------------------------------------------------
    def __init__(self, **kwargs):  
        super().__init__(**kwargs)    
    
    # -------------------------------------------------------------------------
    # Private functions
    # -------------------------------------------------------------------------
    def _update_file_names(self, filename):
        
        # Strip file for ending
        filename = re.sub("[.].*", "", filename)
    
        # Ad-hoc changes
        if "Ability" == filename: 
            filename_new = "Abilities"            
        elif "Interest" == filename:
            filename_new = "Interests"
        elif "job_zone_reference" == filename:
            filename_new = "Job Zone Reference"
        elif "onet_content_model_reference" == filename:
            filename_new = "Content Model Reference"
        elif "onetsoc_data" == filename:
            filename_new = "Occupation Data"
        elif "onetsoc_job_zones" == filename:
            filename_new = "Job Zones"            
        elif "scales_reference" == filename:
            filename_new = "Scales Reference"            
        elif "Tasks" == filename or "Task" == filename:
            filename_new = "Task Statements"                        
        elif "WorkActivity" == filename:
            filename_new = "Work Activities"                                    
        elif "WorkContext" == filename:
            filename_new = "Work Context"                                                
        elif "WorkValue" == filename:
            filename_new = "Work Values"                                    
        elif "WorkStyles" == filename:
            filename_new = "Work Styles"                                    
        elif "EducTrainExp" == filename:
            filename_new = "Education, Training, and Experience"    
        elif "Anchors" == filename:
            filename_new = "Level Scale Anchors"            
        elif "OccLevelMetadata" == filename:
            filename_new = "Occupation Level Metadata"
        elif "Readme" == filename:
            filename_new = "Read Me"            
        elif "Survey_Booklet_Location_Reference" == filename:
            filename_new = "Survey Booklet Locations"                        
            
        else:
            filename_new = filename
        
        return filename_new
        
    def _check_root(self,child,parent,include):
        
        # Choice of continuing
        stop_operation = False
        
        # Service information
        if self.verbose>1:
            print(f"\nChecking database: {child}")
        
        # Skip the parent directory
        if child == parent or not any(x in child for x in include):
            stop_operation = True

        if not stop_operation:    
            # Service information
            if self.verbose>1:
                print(f"\tUsing database: {child}")
        
        return stop_operation
        

    # -------------------------------------------------------------------------
    # Public functions
    # -------------------------------------------------------------------------
    def unzip_onet_files(self,
                         path_to_zipped_files,
                         path_to_unzipped_files
                         ):
        """
        Unzip all *.zip-files that have been extracted from O*NET: https://www.onetcenter.org/db_releases.html
        Remember to download the text files
        """
        # Service info
        if self.verbose:
            print(f"Unzipping all *.zip files from '{path_to_zipped_files}' and saving to '{path_to_unzipped_files}'")
        
        # List all zip files
        files_all = os.listdir(path_to_zipped_files)
        
        # Restrict to *.zip files
        files_zip = [f for f in files_all if f.endswith('.zip')]
        
        # Go throug all zip files and unzip
        for file in files_zip:
                        
            # Cut "zip" out of file name
            file_ex_zip = re.sub(pattern=".zip*", repl="", string=file)
            
            # Open each zip and check if it unzips as a folder of the same name or unzips directly.
            # This determines how we save the file
            with zipfile.ZipFile(path_to_zipped_files+file) as zip_file:
                
                
                if file_ex_zip+"/" in zip_file.namelist():
                    extract_dir = path_to_unzipped_files
                else:
                    extract_dir = path_to_unzipped_files+file_ex_zip
                    
                # Unzip
                shutil.unpack_archive(filename=path_to_zipped_files+file,
                                      extract_dir=extract_dir)
                    
                zip_file.close()
              
            # Clean up files that are not directories
            all_unzipped_files = os.listdir(path_to_unzipped_files)
            
            for file_or_folder in all_unzipped_files:
            
                # Create absolute path
                absolute_path = os.path.join(path_to_unzipped_files, file_or_folder)
                
                # Move files but leave folders untouched
                if not pathlib.Path(absolute_path).is_dir():
                    shutil.move(src=absolute_path, dst=path_to_unzipped_files+file_ex_zip)

        """
        All zip-files have now been unzipped.
        O*NET has the habit of adding '_text' to the newer files, which we now delete
        """
        folders_unzipped = os.listdir(path_to_unzipped_files)
        
        for folder in folders_unzipped:
            if "_text" in folder:
                
                # Cut "_text" out of file name
                folder_ex_text = re.sub(pattern="_text", repl="", string=folder)
                
                # Rename
                os.rename(src=os.path.join(path_to_unzipped_files, folder),
                          dst=os.path.join(path_to_unzipped_files, folder_ex_text))
            
        """
        Older O*NET files use the name convention of a single underscore ('_') to indicate version, whereas newer use two underscores ('_')
        To make folders consistent, we update the older files
        """        
        folders_unzipped = os.listdir(path_to_unzipped_files)
        
        for folder in folders_unzipped:
            if folder.count("_")==1:
                
                # Add underscore to indicate version
                folder_updated = folder[:-1]+"_"+folder[-1:]
                    
                # Rename
                os.rename(src=os.path.join(path_to_unzipped_files, folder),
                          dst=os.path.join(path_to_unzipped_files, folder_updated))
                    
                    
    def stremline_onet_files(self,
                             path_to_unzipped_files,
                             path_to_db_files,
                             file_format=".txt",
                             ):
        """
        # Rename all files to lower and delete space
        """
        # Service info
        if self.verbose:
            print("Streamlining O*NET files for consistent use")

        # Walk through all folders    
        for root, directories, files in os.walk(path_to_unzipped_files):

            # Skip the parent directory
            if root == path_to_unzipped_files:
                continue
            
            # Service info
            if self.verbose>1:
                print(f"Streamlining files in database: {root}")
            
            # Keep only files with specified ending
            files = [f for f in files if f.lower().endswith(file_format)]
            
            for f in files:
                
                f_new = self._update_file_names(filename=f)
            
                # Create folder and leave unaltered if it exists
                os.makedirs(os.path.dirname(root.replace(path_to_unzipped_files, path_to_db_files)+"/"), exist_ok=True)
                
                # Copy file
                shutil.copy2(os.path.join(root, f),
                             os.path.join(root.replace(path_to_unzipped_files, path_to_db_files),
                                          f_new.lower()+file_format)
                             )        
            
            
    def get_overview(self,
                     path_to_db_files,
                     ):
        """
        Get overview of available O*NET files, i.e. which subfiles are present for each DB
        """
        # Pre-allocate        
        overview = {}
        
        # Walk through all folders    
        for root, directories, files in os.walk(path_to_db_files):

            # Skip the parent directory
            if root == path_to_db_files:
                continue
        
            # Sort files
            files.sort()
            
            # Clean root
            root_clean = re.sub(pattern=path_to_db_files,
                                repl="",
                                string=root)
            
            # Store files in dict
            overview[root_clean] = files
            
        # Remove empty elements    
        overview = bd.tools.remove_empty_elements(d=overview)
                
        # Find all files
        files_all = [item for k,v in overview.items() for item in v]
        
        ## Diagnostics
        # Count occurances of each file
        files_count = Counter(files_all).most_common()
        
        # Find common values across keys
        files_common = set.intersection(*(set(val) for val in overview.values()))
        
        # Unique files
        files_unique = list(set(files_all))
        files_unique.sort()
        
        ## Prepare overview of files per database
        # Pre-allocate overview
        df_files_overview = pd.DataFrame(data = 0, index = files_unique, columns=overview.keys())
        
        for col in df_files_overview.columns:
            
            # Get mask
            mask = [item in overview[col] for item in df_files_overview.index]
            
            df_files_overview[col][mask] = 1
            
        # Find intersection of data and databases available
        mask_order = [item in df_files_overview.columns for item in self.df_dates[G.DB_COL].unique().tolist()]
        order_of_cols = self.df_dates[G.DB_COL][mask_order]
        
        # Re-order
        df_files_overview = df_files_overview[order_of_cols]
                
        return df_files_overview


    def prepare_task_data(self,
                          path_to_db_files):
        """
        Prepare task data
        """    
        if self.verbose:
            print("\n\nPREPARING TASK DATA")
        
        #----------------------------------------------------------------------
        # Inputs
        #----------------------------------------------------------------------
        # List files needed
        TASK_FILES = ["task statements", "task ratings"]
        TASK_FILES_TXT = [s + ".txt" for s in TASK_FILES]
        
        # Important cols
        COLS_ID = ['O*NET-SOC Code', 'Task ID']
        COLS_WEIGHT = ['Relevance', 'Importance', 'Frequency']

        #----------------------------------------------------------------------
        # Preparation
        #----------------------------------------------------------------------
        # Get overview file of DB and contents
        df_files_overview = self.get_overview(path_to_db_files=path_to_db_files)

        # Find relevant databases, i.e. those that contain BOTH task_files
        db_mask = df_files_overview.loc[TASK_FILES_TXT].all(axis=0)
        
        # Convert to list
        db_include = db_mask.index[db_mask].to_list()
        
        #------------------------------------------------------------------------------
        # Find tasks description and weights (importance, relevance, and frequency combined)
        #------------------------------------------------------------------------------
        # Pre-allocate
        df_task = pd.DataFrame()
        
        for root, directories, files in os.walk(path_to_db_files):
            
            # Skip parent directory
            if self._check_root(child=root,
                                parent=path_to_db_files,
                                include=db_include):
                continue
        
            # Load titles
            data_title_temp = pd.read_table(filepath_or_buffer=root+'/occupation data.txt',
                                            sep="\t",
                                            header=0,
                                            encoding='cp1252')
            data_title_temp.rename(columns={"Title":"Job title",
                                            "Description":"Job description"},
                                   inplace=True)
        
            # Import task statements, ratings
            data_task_statement_temp = pd.read_table(filepath_or_buffer=root+'/task statements.txt',
                                                     sep = "\t",
                                                     header=0,
                                                     encoding='cp1252')
            
            data_task_rating_temp = pd.read_table(filepath_or_buffer=root+'/task ratings.txt',
                                                  sep="\t",
                                                  header=0,
                                                  encoding='cp1252')
            

        
            # Load scales
            data_scales = pd.read_table(filepath_or_buffer=root+'/scales reference.txt',
                                        sep="\t",
                                        header=0,
                                        encoding='cp1252')
        
            #------------------------------------------------------------------------------
            # Find tasks RELEVANCE and standardize
            #------------------------------------------------------------------------------
            data_task_relevance_temp = get_tasks(scale_name="Relevance",
                                                 scale_id="RT",
                                                 scales_lookup=data_scales,
                                                 ratings=data_task_rating_temp,
                                                 id_cols=COLS_ID)
            
            #------------------------------------------------------------------------------
            # Find tasks IMPORTANCE and standardize
            #------------------------------------------------------------------------------
            data_task_importance_temp = get_tasks(scale_name="Importance",
                                                 scale_id="IM",
                                                 scales_lookup=data_scales,
                                                 ratings=data_task_rating_temp,
                                                 id_cols=COLS_ID)
            
            #------------------------------------------------------------------------------
            # Find tasks FREQUENCY and standardize
            #------------------------------------------------------------------------------
            data_task_frequency_temp = get_tasks(scale_name="Frequency",
                                                 scale_id="FT",
                                                 scales_lookup=data_scales,
                                                 ratings=data_task_rating_temp,
                                                 id_cols=COLS_ID)
        
            #------------------------------------------------------------------------------
            # Merge importance and frequency into one weight per ID
            #------------------------------------------------------------------------------
            # Collect dfs in list
            df_task_weights_temp = [data_task_relevance_temp,
                                    data_task_importance_temp,
                                    data_task_frequency_temp]
        
            # Merge all task weights
            df_task_weights = bd.tools.merge_multiply_dfs(l=df_task_weights_temp,
                                                       on=COLS_ID,
                                                       how='inner',
                                                       sort=False)
            
            # Construct raw weights, which are just an average of the individual components
            df_task_weights["RawWeight"] = df_task_weights[COLS_WEIGHT].mean(axis=1)
            
            # Construct total weights within each O*NET-Soce code
            df_task_weights["TotalWeight"] = df_task_weights.groupby(by=[G.ONET_COL])['RawWeight'].transform('sum')
        
            # Now compute weights (they will sum to one within each occupations)
            df_task_weights["Weight"] = df_task_weights["RawWeight"].div(df_task_weights["TotalWeight"])
        
            # Sanity check
            if not (df_task_weights.groupby([G.ONET_COL])["Weight"].sum().round(0) == 1.0).all():
                raise Exception("Total task weights per O*NET SOC CODE is not 1")
        
            #------------------------------------------------------------------------------
            # Weights onto statements
            #------------------------------------------------------------------------------
            data_task_temp = data_task_statement_temp.merge(right=df_task_weights,
                                                            how='inner',
                                                            on=COLS_ID,
                                                            sort=False)
            
            # Merge Title
            data_task_temp = data_task_temp.merge(right=data_title_temp,
                                                  how='inner',
                                                  on=G.ONET_COL,
                                                  sort=False) 
            
            # Add version of db
            data_task_temp[G.DB_COL] = re.sub(pattern=path_to_db_files,
                                              repl="",
                                              string=root)
        
            # Append data
            df_task = df_task.append(data_task_temp,
                                     ignore_index=True)
            
            # House-keeping
            del data_task_temp, data_task_relevance_temp, data_task_importance_temp, data_task_frequency_temp
        
        
        #------------------------------------------------------------------------------
        """
        All tasks have been merged on a final df (df_task)
        """
        #------------------------------------------------------------------------------        
        # Merge with dates
        df_task.rename(columns={"Date": "Task date", 
                                "Task": "Task description"},
                       errors="raise",
                       inplace=True)
        
        df_task = df_task.merge(right=self.df_dates,
                                how="inner",
                                on=G.DB_COL)
        
        return df_task
        

    def prepare_attribute_data(self,
                          path_to_db_files):
        """
        Prepare attribute data, i.e.
        "abilities", "skills", "knowledge", "interests", "work activities", "work context", "work styles", "work values"
        """
        if self.verbose:
            print("\n\nPREPARING ATTRIBUTE DATA")                
        #----------------------------------------------------------------------
        # Inputs
        #----------------------------------------------------------------------
        # List files needed
        ONET_FILES_CORE = ["abilities", "skills", 
                           "knowledge", "interests",
                           "work activities", "work context", "work styles", "work values"]
        ONET_FILES_EXTRA = ["scales reference", "content model reference", "occupation data"]
        ONET_FILES_ALL_TXT = [s + ".txt" for s in ONET_FILES_CORE+ONET_FILES_EXTRA]
        
        # scale per onet
        ONET_SCALES = {
            "abilities" : ["IM", "LV"],
            "skills" : ["IM", "LV"], 
            "knowledge" : ["IM", "LV"],
            "interests" : ["OI"],
            "work activities" : ["IM", "LV"],
            "work context" : ["CX"],
            "work styles" : ["IM"],
            "work values" : ["EX", "EN"]
            }

        # Important cols
        COLS_ORIGINAL_KEEP = ['O*NET-SOC Code', 'Element ID', 'Element Name', "Data Value"]
        COLS_PIVOT = ['O*NET-SOC Code', 'Element ID', 'Element Name']

        #----------------------------------------------------------------------
        # Preparation
        #----------------------------------------------------------------------
        # Get overview file of DB and contents
        df_files_overview = self.get_overview(path_to_db_files=path_to_db_files)
        
        # Find relevant databases
        db_mask = df_files_overview.loc[ONET_FILES_ALL_TXT].all(axis=0)
        
        # Convert to list
        db_include = db_mask.index[db_mask].to_list()
                
        #------------------------------------------------------------------------------
        # Find attributes
        #------------------------------------------------------------------------------    
        # Pre-allocate
        df_attribute = pd.DataFrame()
        
        for root, directories, files in os.walk(path_to_db_files):

            # Skip parent directory            
            if self._check_root(child=root,
                                parent=path_to_db_files,
                                include=db_include):
                continue
                
            # Load titles
            data_title_temp = pd.read_table(filepath_or_buffer=root+'/occupation data.txt',
                                            sep="\t",
                                            header=0,
                                            encoding='cp1252')
            data_title_temp.rename(columns={"Title":"Job title",
                                            "Description":"Job description"},
                                   inplace=True)            

            # Load scales
            data_scales = pd.read_table(filepath_or_buffer=root+'/scales reference.txt',
                                        sep="\t",
                                        header=0,
                                        encoding='cp1252')
            
            # Load description
            data_description = pd.read_table(filepath_or_buffer=root+'/content model reference.txt',
                                             sep = "\t",
                                             header=0,
                                             encoding='cp1252')
            
            # Drop Element Name
            data_description.drop(columns="Element Name",
                                  inplace=True)
            
            # Initialize codes for this db
            db_codes = []
                    
            # Pre-allocate
            df_attribute_temp = pd.DataFrame()
            
            #------------------------------------------------------------------
            # Get each attribute one at a time
            #------------------------------------------------------------------
            for attribute in ONET_FILES_CORE:

                # Import file
                data_import_temp = pd.read_table(filepath_or_buffer=root+'/'+attribute+'.txt',
                                                 sep="\t",
                                                 header=0,
                                                 encoding='cp1252')
                
                # Keep only certain scales
                mask_keep = data_import_temp["Scale ID"].isin(ONET_SCALES[attribute])
                data_import_temp = data_import_temp.loc[mask_keep]
                
                # Find unique occ codes
                unique_occ_temp = data_import_temp[G.ONET_COL].unique().tolist()
                
                # Update codes
                if db_codes:
                   db_codes = list(set(db_codes) & set(unique_occ_temp)) 
                else:
                    db_codes = unique_occ_temp
                    
                # Subset to only relevant occ codes that are present in all core files
                data_import_temp = data_import_temp.loc[data_import_temp[G.ONET_COL].isin(db_codes)]
                
                if attribute in ["work context",
                                 "work styles",
                                 "work values",
                                 "interests"]:
                        
                    # Check the number of scale IDs
                    if data_import_temp["Scale ID"].nunique()!=1:
                        print("Different from 1 scale ID for",attribute,"in",root)
                        break
                    
                    # IF EN (old scale, not used anymore)
                    if data_import_temp["Scale ID"].unique()=='EN':
                        # Keep only rows where Element Name contains "Mean Extent"
                        mask_mean_extent = data_import_temp['Element Name'].str.contains("-Mean Extent")
                        
                        # Subset
                        data_import_temp = data_import_temp.loc[mask_mean_extent]
                        
                        # Delete part og string
                        data_import_temp['Element Name'] = data_import_temp['Element Name'].str.replace("-Mean Extent", "")
                    
                    # Locate minimum and maximum
                    scale_extrema = data_scales[data_scales["Scale ID"] == data_import_temp["Scale ID"].iloc[0]][["Minimum", "Maximum"]]
                    
                    # Standardize scale
                    data_import_temp.loc[:,"Data Value"] = standardize_scores(x=data_import_temp["Data Value"],
                                                                              minimum=scale_extrema["Minimum"],
                                                                              maximum=scale_extrema["Maximum"])
                    
                    # Data to append
                    data_to_append = data_import_temp.loc[:,COLS_ORIGINAL_KEEP]
                    
                elif attribute in ["abilities",
                                   "skills",
                                   "knowledge",
                                   "work activities"]:
                    
                    # Check the number of scale IDs
                    if data_import_temp["Scale ID"].nunique()!=2:
                        print("Different from 2 scale ID for",attribute,"in",root)
                        break
    
                    # Find unique scales
                    unique_scales = data_import_temp["Scale ID"].unique()
                   
                    # Pivot data 
                    data_to_append_temp = data_import_temp.pivot(index=COLS_PIVOT,
                                                                 columns="Scale ID",
                                                                 values="Data Value").reset_index().drop_duplicates(subset=COLS_PIVOT)
                   
                    # Treat the two scales differently
                    for s in unique_scales:
    
                        # Find extrama
                        scale_extrema = data_scales.loc[data_scales["Scale ID"] == s,
                                                        ["Minimum", "Maximum"]]
                        
                        # Standardize scale
                        data_to_append_temp.loc[:,s] = standardize_scores(x=data_to_append_temp.loc[:,s],
                                                                          minimum=scale_extrema["Minimum"],
                                                                          maximum=scale_extrema["Maximum"])
                            
                    # Add data value as the average of the scales
                    data_to_append_temp.loc[:,"Data Value"] = data_to_append_temp[unique_scales].mean(axis=1)
                        
                    # Data to append
                    data_to_append = data_to_append_temp.loc[:,COLS_ORIGINAL_KEEP]
        
                # Merge desciprtion
                data_to_append = data_to_append.merge(right=data_description,
                                                      how="left",
                                                      on="Element ID")
                
                # Add info
                data_to_append.insert(loc=0,
                                      column=G.DB_COL,
                                      value=re.sub(pattern=path_to_db_files,
                                                   repl="",
                                                   string=root)
                                      )
                data_to_append.insert(loc=1,
                                      column="Category",
                                      value=re.sub(pattern=".txt",
                                                   repl="",
                                                   string=attribute)
                                      )
                    
                # Strip any-Word characters
                data_to_append.loc[:,'Element Name'] = data_to_append['Element Name'].str.replace(pat="[!,*)@#%(&$_?.^]",
                                                                                                  repl="",
                                                                                                  regex=True)
                        
                # Rename
                data_to_append.rename(columns={"Description":"Element description"},
                                      inplace=True)
                
                # Add titles
                data_to_append = data_to_append.merge(right=data_title_temp,
                                                      how='inner',
                                                      on=G.ONET_COL,
                                                      sort=False) 
                
                # Append 
                df_attribute_temp = df_attribute_temp.append(data_to_append,
                                                             ignore_index=True)
        
            #------------------------------------------------------------------
            """
            At this point, we have been through all core O*NET attributes for a particular DB.
            Now it's time to subset to relevant occ codes that are present in all core files
            Note that the db_codes are updated automatically so they at any point represent the union of occ codes
            """
            #------------------------------------------------------------------
            df_attribute_temp = df_attribute_temp.loc[df_attribute_temp['O*NET-SOC Code'].isin(db_codes)]
            
            # Finally, we append to master
            df_attribute = df_attribute.append(df_attribute_temp,
                                               ignore_index=True)
    
        # Merge with dates
        df_attribute = df_attribute.merge(right=self.df_dates,
                                          how="inner",
                                          on=G.DB_COL)
        
        # Drop missing
        df_attribute.dropna(inplace=True)
    
        return df_attribute



    def prepare_onet_data(self,
                          path_to_db_files,
                          path_to_output_files=None):
        """
        Prepare O*NET data and save as csv
        """
        #----------------------------------------------------------------------
        # Folder
        #----------------------------------------------------------------------
        if path_to_output_files is None:
            
            # Get location of this file        
            file_dir = "/".join(__file__.split("/")[:-1])
        
            # Location to safe if not provided
            path_to_output_files = os.path.join(file_dir, f"../data/onet_data/prepared/")
            
            if self.verbose:
                print(f"Saving to default location: {path_to_output_files}")
            

        #----------------------------------------------------------------------
        # Tasks
        #----------------------------------------------------------------------
        # Get task data
        df_task = self.prepare_task_data(path_to_db_files=path_to_db_files)

        # Save
        df_task.to_parquet(path=path_to_output_files+"tasks"+".parquet",
                           engine='auto',
                           compression='BROTLI',
                           index=None,
                           partition_cols=None)
        
        del df_task

        #----------------------------------------------------------------------
        # Attributes
        #----------------------------------------------------------------------
        # Get attribute data
        df_attribute = self.prepare_attribute_data(path_to_db_files=path_to_db_files)
        
        df_attribute.to_parquet(path=path_to_output_files+"attributes"+".parquet",
                           engine='auto',
                           compression='BROTLI',
                           index=None,
                           partition_cols=None)
    
        del df_attribute

        
        















