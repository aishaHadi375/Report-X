import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime

class DataProcessor:
    """Handles CSV loading, validation, and preprocessing with data cleaning"""
    
    def __init__(self):
        self.original_df = None
        self.processed_df = None
        self.column_datatypes = {}
        self.data_profile = {}
        self.cleaning_steps = []
        
    def load_data(self, uploaded_file):
        """Load and validate CSV file with robust error handling"""
        if uploaded_file is None:
            return None
            
        try:
            # Try different encodings for CSV
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                try:
                    df = pd.read_csv(uploaded_file, encoding='latin1')
                except:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            except pd.errors.ParserError:
                uploaded_file.seek(0)
                try:
                    df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
                except:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, sep='\t', encoding='utf-8')
            
            # Validate data
            if df.empty:
                raise ValueError("CSV file is empty")
            if len(df.columns) == 0:
                raise ValueError("CSV has no columns")
            
            # Clean column names
            df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
            
            # Store data
            self.original_df = df.copy()
            self.processed_df = df.copy()
            
            # Analyze data
            self.detect_column_types()
            self.profile_data()
            
            self.cleaning_steps.append({
                "step": "Data Loaded",
                "description": f"Successfully loaded {len(df)} rows and {len(df.columns)} columns",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return df
            
        except Exception as e:
            st.error(f"Error loading CSV: {str(e)}")
            return None
    
    def detect_column_types(self):
        """Automatically detect column data types"""
        if self.processed_df is None:
            return
            
        df = self.processed_df
        self.column_datatypes = {}
        
        for col in df.columns:
            # Skip columns with all NaN
            if df[col].isna().all():
                self.column_datatypes[col] = "unknown"
                continue
            
            # Check if numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                # Check if integer
                non_null = df[col].dropna()
                if len(non_null) > 0 and non_null.apply(lambda x: x == int(x) if not pd.isna(x) else True).all():
                    unique_count = df[col].nunique()
                    # If few unique values, might be categorical
                    if unique_count <= 20 and unique_count / len(df) < 0.05:
                        self.column_datatypes[col] = "categorical"
                    else:
                        self.column_datatypes[col] = "integer"
                else:
                    self.column_datatypes[col] = "float"
            else:
                # Try datetime conversion
                try:
                    pd.to_datetime(df[col], errors='raise')
                    self.column_datatypes[col] = "datetime"
                except:
                    # Check if boolean
                    unique_count = df[col].nunique()
                    lower_values = df[col].dropna().astype(str).str.lower()
                    bool_values = {'true', 'false', 'yes', 'no', 'y', 'n', '1', '0', 't', 'f'}
                    
                    if set(lower_values.unique()).issubset(bool_values):
                        self.column_datatypes[col] = "boolean"
                    elif unique_count <= 20 or unique_count / len(df) < 0.05:
                        self.column_datatypes[col] = "categorical"
                    else:
                        self.column_datatypes[col] = "text"
    
    def profile_data(self):
        """Create comprehensive data profile"""
        if self.processed_df is None:
            return
            
        df = self.processed_df
        
        self.data_profile = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "missing_values": df.isna().sum().to_dict(),
            "missing_percentage": (df.isna().sum() / len(df) * 100).to_dict(),
            "duplicate_rows": df.duplicated().sum(),
            "memory_usage": df.memory_usage(deep=True).sum() / (1024 * 1024),  # MB
            "column_types": self.column_datatypes,
            "columns": {}
        }
        
        # Profile each column
        for col in df.columns:
            col_type = self.column_datatypes.get(col, "unknown")
            col_profile = {
                "type": col_type,
                "missing_count": int(df[col].isna().sum()),
                "missing_percentage": float(df[col].isna().sum() / len(df) * 100),
                "unique_values": int(df[col].nunique()),
            }
            
            # Numeric columns
            if col_type in ["integer", "float"]:
                if not df[col].dropna().empty:
                    col_profile.update({
                        "min": float(df[col].min()),
                        "max": float(df[col].max()),
                        "mean": float(df[col].mean()),
                        "median": float(df[col].median()),
                        "std": float(df[col].std()) if df[col].std() == df[col].std() else 0.0,  # Check for NaN
                        "has_outliers": self._has_outliers(df[col]),
                    })
            
            # Categorical columns
            elif col_type in ["categorical", "text", "boolean"]:
                value_counts = df[col].value_counts().head(5).to_dict()
                col_profile["top_values"] = value_counts
                if not df[col].mode().empty:
                    col_profile["most_common"] = str(df[col].mode()[0])
            
            # Datetime columns
            elif col_type == "datetime":
                try:
                    date_series = pd.to_datetime(df[col])
                    col_profile.update({
                        "min_date": str(date_series.min()),
                        "max_date": str(date_series.max()),
                        "date_range_days": int((date_series.max() - date_series.min()).days)
                    })
                except:
                    pass
            
            self.data_profile["columns"][col] = col_profile
    
    def _has_outliers(self, series):
        """Detect outliers using IQR method"""
        series = series.dropna()
        if len(series) < 4:
            return False
            
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        return ((series < lower_bound) | (series > upper_bound)).any()
    
    def clean_data(self, remove_duplicates=True, handle_missing='drop_cols', 
                   missing_threshold=0.5, remove_outliers=False):
        """Clean the data based on specified options"""
        if self.processed_df is None:
            return None
        
        df = self.processed_df.copy()
        original_shape = df.shape
        
        cleaning_report = {
            'original_rows': original_shape[0],
            'original_cols': original_shape[1],
            'steps_taken': []
        }
        
        # 1. Remove duplicates
        if remove_duplicates:
            dup_count = df.duplicated().sum()
            if dup_count > 0:
                df = df.drop_duplicates()
                cleaning_report['steps_taken'].append(
                    f"Removed {dup_count} duplicate rows"
                )
        
        # 2. Handle missing values
        if handle_missing == 'drop_cols':
            # Drop columns with too much missing data
            cols_to_drop = [col for col in df.columns 
                          if df[col].isnull().sum() / len(df) > missing_threshold]
            if cols_to_drop:
                df = df.drop(columns=cols_to_drop)
                cleaning_report['steps_taken'].append(
                    f"Dropped {len(cols_to_drop)} columns with >{missing_threshold*100}% missing data"
                )
        
        elif handle_missing == 'drop_rows':
            # Drop rows with any missing values
            rows_before = len(df)
            df = df.dropna()
            rows_dropped = rows_before - len(df)
            if rows_dropped > 0:
                cleaning_report['steps_taken'].append(
                    f"Dropped {rows_dropped} rows with missing values"
                )
        
        elif handle_missing == 'fill_mean':
            # Fill numeric columns with mean
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df[col].isnull().any():
                    df[col].fillna(df[col].mean(), inplace=True)
            cleaning_report['steps_taken'].append(
                f"Filled missing numeric values with column means"
            )
        
        elif handle_missing == 'fill_mode':
            # Fill all columns with mode
            for col in df.columns:
                if df[col].isnull().any() and not df[col].mode().empty:
                    df[col].fillna(df[col].mode()[0], inplace=True)
            cleaning_report['steps_taken'].append(
                f"Filled missing values with most common values"
            )
        
        # 3. Remove outliers (optional)
        if remove_outliers:
            numeric_cols = [col for col, dtype in self.column_datatypes.items() 
                          if dtype in ["integer", "float"] and col in df.columns]
            
            outliers_removed = 0
            for col in numeric_cols:
                data = df[col].dropna()
                if len(data) < 4:
                    continue
                
                Q1 = data.quantile(0.25)
                Q3 = data.quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                outliers_in_col = outlier_mask.sum()
                outliers_removed += outliers_in_col
                
                # Replace outliers with median
                df.loc[outlier_mask, col] = df[col].median()
            
            if outliers_removed > 0:
                cleaning_report['steps_taken'].append(
                    f"Replaced {outliers_removed} outlier values with median"
                )
        
        # Update processed dataframe
        self.processed_df = df
        
        # Recalculate column types and profile
        self.detect_column_types()
        self.profile_data()
        
        # Add to cleaning report
        cleaning_report['cleaned_rows'] = len(df)
        cleaning_report['cleaned_cols'] = len(df.columns)
        cleaning_report['rows_removed'] = original_shape[0] - len(df)
        cleaning_report['cols_removed'] = original_shape[1] - len(df.columns)
        
        # Log cleaning step
        self.cleaning_steps.append({
            "step": "Data Cleaned",
            "description": f"Cleaned data: {original_shape} → {df.shape}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": cleaning_report
        })
        
        return cleaning_report
    
    def get_numeric_columns(self):
        """Get list of numeric columns"""
        return [col for col, dtype in self.column_datatypes.items() 
                if dtype in ["integer", "float"]]
    
    def get_categorical_columns(self):
        """Get list of categorical columns"""
        return [col for col, dtype in self.column_datatypes.items() 
                if dtype in ["categorical", "boolean", "text"]]
    
    def get_datetime_columns(self):
        """Get list of datetime columns"""
        return [col for col, dtype in self.column_datatypes.items() 
                if dtype == "datetime"]
    
    def get_cleaning_summary(self):
        """Get summary of all cleaning steps performed"""
        return self.cleaning_steps