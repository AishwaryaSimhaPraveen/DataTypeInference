import pandas as pd
import numpy as np

def infer_data_types(file):
    """
    Infers the data types of columns in a CSV or Excel file and returns a 
    dictionary of inferred types, handling special characters, booleans, and mixed types.
    """
    try:
        # Step 1: Read the file into a pandas DataFrame
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, low_memory=False)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

        # Step 2: Initialize an empty list to store inferred data types
        inferred_types = []

        # Step 3: Iterate over columns in the DataFrame
        for column in df.columns:
            print(f"Processing column: {column}")

            # Handle object columns (usually strings or mixed types)
            if df[column].dtype == 'object':
                # Convert the column to strings to handle mixed types safely
                df[column] = df[column].astype(str).str.strip()

                # Remove special characters like $, €, £, commas, etc.
                df[column] = df[column].replace({'[$€,£%]': '', ',': ''}, regex=True)

                # Attempt to convert to boolean (e.g., 'true', 'false', 'yes', 'no', '1', '0')
                lower_case_column = df[column].str.lower()
                if lower_case_column.isin(['true', 'false']).all():
                    df[column] = lower_case_column.map({'true': True, 'false': False})
                    inferred_type = 'boolean'
                elif lower_case_column.isin(['yes', 'no']).all():
                    df[column] = lower_case_column.map({'yes': True, 'no': False})
                    inferred_type = 'boolean'
                elif df[column].isin([1, 0, '1', '0']).all():
                    df[column] = df[column].map({'1': True, '0': False, 1: True, 0: False})
                    inferred_type = 'boolean'
                else:
                    # Attempt to convert to datetime
                    try:
                        df[column] = pd.to_datetime(df[column], errors='raise')
                        inferred_type = 'datetime64[ns]'
                    except (ValueError, TypeError):
                        # Coerce non-numeric values to NaN and check if column is primarily numeric
                        df[column] = pd.to_numeric(df[column], errors='coerce')
                        if df[column].isna().sum() / len(df[column]) < 0.5:  # If more than 50% is numeric
                            inferred_type = 'numeric'
                        else:
                            # If not, treat it as categorical or object
                            inferred_type = 'category' if df[column].nunique() / len(df[column]) < 0.1 else 'object'

            # Handle numeric and other data types
            elif df[column].dtype == 'int64' or df[column].dtype == 'float64':
                # Coerce non-numeric values to NaN and still treat as numeric if most are valid numbers
                if df[column].isna().sum() / len(df[column]) < 0.5:  # If less than 50% are NaN
                    inferred_type = str(df[column].dtype)
                else:
                    inferred_type = 'numeric'

            else:
                inferred_type = str(df[column].dtype)

            # Append the column name and its inferred type to the list
            inferred_types.append({'column_name': column, 'inferred_data_type': inferred_type})
            print(f"Inferred type for '{column}': {inferred_type}")

        # Step 4: Return the inferred types
        return inferred_types

    except Exception as e:
        print(f"Error processing file: {e}")
        return []

# Example usage:
# with open('your_file.csv', 'rb') as file:
#     result = infer_data_types(file)
