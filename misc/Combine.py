import pandas as pd
import glob

# Get a list of all text files in the directory
txt_files = sorted(glob.glob("oxygen_*.txt"))

# Initialize an empty list to hold dataframes
dfs = []

# Loop through the text files
for i, file in enumerate(txt_files):
    if i == 0:
        # Read the first file and use the first row as the header
        df = pd.read_csv(file, delimiter="\t")
    else:
        # Read the remaining files, skipping the first row
        df = pd.read_csv(file, delimiter="\t", header=None, skiprows=1)
        df.columns = dfs[0].columns  # Set the column names to match the first dataframe
    dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Separate the 14th column (index 13)
text_column = combined_df.iloc[:, 13]
other_columns = combined_df.drop(columns=combined_df.columns[13])

# Convert all columns except the 14th one to numeric, if possible, converting non-numeric values to NaN
other_columns = other_columns.apply(pd.to_numeric, errors='coerce')

# Concatenate the numeric columns with the 14th text column
combined_df = pd.concat([other_columns, text_column], axis=1)

# Write the combined dataframe to an Excel file
combined_df.to_excel("combined.xlsx", index=False)