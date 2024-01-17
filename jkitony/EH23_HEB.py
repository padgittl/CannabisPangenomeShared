#Required : quant and orthologs
import pandas as pd
import os
from matplotlib import pyplot
import matplotlib.pyplot as plt
df = pd.read_csv('EH23a_EH23b_ortholog_blast_fractionation.txt', sep=' ', header=None, names=["GID1", "GID2","ID"])
df=df.drop("ID",axis=1)
df.columns=("GID1","GID2")
df['GID1'] = df['GID1']#.str.replace(r'\.t.*', '', regex=True)
df['GID2'] = df['GID2']#.str.replace(r'\.t.*', '', regex=True)
#1:1 othorlog lifting
C1=df.GID1.value_counts()
Uniq1=C1[C1==1]
C2=df.GID2.value_counts()
Uniq2=C2[C2==1]
df0 = df[df.GID1.isin(Uniq1.index)&df.GID2.isin(Uniq2.index)]
out1 = "file22.tsv"
df0.to_csv(out1, sep='\t', index=False)
#read salmon quant file
quant = pd.read_csv('quant.tsv', sep='\t')
quant = quant.drop(["Length", "EffectiveLength","NumReads"],axis=1)

tpms = quant.set_index(['Name', "Sample"]).TPM.unstack().sort_index().sort_index(axis=1)
out = "file11.tsv"
tpms.to_csv(out, sep='\t', index=True)
######################
# Create a list to store the output lines
output_lines = []

# Create a list of column headers to process
columns_to_process = ["EH23_Early_Flower", "EH23_Foliage", "EH23_Foliage_12light", "EH23_Late_Flower", "EH23_Roots", "EH23_Shoottips"]

# Initialize a dictionary to store values for each column
column_values = {column: {} for column in columns_to_process}

# Read values from file1.txt and store them in dictionaries for each column
with open("file11.tsv", "r") as file1:
    header = next(file1)  # Read and skip the header
    for line in file1:
        parts = line.strip().split('\t')
        name = parts[0]
        for column, value in zip(columns_to_process, parts[1:]):
            column_values[column][name] = float(value)


# Read the mapping from file2.txt and write the results to file2.txt for each column
with open("file22.tsv", "r") as file2:
    mapping_lines = file2.readlines()

with open("file22.tsv", "w") as output_file:
    # Write the header with all column headers from file1.txt
    output_file.write(mapping_lines[0].strip() + "\t" + "\t".join(columns_to_process) + "\n")
    
# Write the results for each pair of GID1 and GID2 for each column
for line in mapping_lines[1:]:
    gid1, gid2 = line.strip().split('\t')
    summary_values = []
    for column in columns_to_process:
        value1 = column_values[column].get(gid1, 0)
        value2 = column_values[column].get(gid2, 0)
        
        if abs(value1 - value2) <= 5:
            summary = "C"
        elif value1 > value2:
            summary = "A"
        else:
            summary = "B"
        
        summary_values.append(summary)
    output_line = "{}\t{}\t{}\n".format(gid1, gid2, "\t".join(summary_values))
    output_lines.append(output_line)

# Open the output file in append mode and write all the lines to it
with open("file22.tsv", "a") as output_file:
    output_file.writelines(output_lines)

print("Results for all columns from file1 have been written to file22")

# Read the data from file2.txt
df = pd.read_csv('file22.tsv', sep='\t')

# Transpose the DataFrame to have rows as columns and columns as rows
df = df.set_index(['GID1', 'GID2']).T

# Count occurrences of "A," "B," and "C" in each row
count_df = df.apply(lambda row: row.value_counts(), axis=1).fillna(0).astype(int)

# Create a horizontally flipped stacked bar graph with custom colors
ax = count_df.plot(kind='barh', stacked=True, figsize=(10, 6),
                   color={"A": "brown", "B": "blue", "C": "lightgrey"})

# Set labels and title
plt.title('EH23 Homoeolog Expression Bias (HEB)')
plt.ylabel('Samples')
plt.xlabel('1:1 Gene Pairs')
plt.yticks(rotation=0)

# Move the legend outside the plot using bbox_to_anchor
legend = ax.legend(title='Values', loc='lower center', labels=["A Biased", "B Biased", "Balanced"], bbox_to_anchor=(0.5, -0.3), ncol=3)

# Set legend colors to match custom colors
for handle, label in zip(legend.legend_handles, ["A", "B", "C"]):
    handle.set_color({"A": "brown", "B": "blue", "C": "lightgrey"}[label])

# Save the heatmap plot to a file 
plt.savefig('EH23_homeolog_tissues_specific.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()


df = pd.read_csv('file11.tsv', sep="\t") #tpms

# Create a DataFrame from the sample data
#df = pd.DataFrame(data)

# Separate the data into "EH23a" and "EH23b" sub-dataframes
df_a = df[df['Name'].str.startswith('EH23a')]
df_b = df[df['Name'].str.startswith('EH23b')]

# Log2-transform the values for both sub-dataframes
df_a_values = df_a.drop(columns=['Name'])
df_b_values = df_b.drop(columns=['Name'])
df_a_log2 = np.log2(df_a_values + 1)  # Adding 1 to avoid log(0)
df_b_log2 = -np.log2(df_b_values + 1)  # Adding 1 to avoid log(0) and negating to flip

# Create subplots for "EH23b" and "EH23a" with shared y-axis
fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)

# Plot for "EH23b" (flipped) - Now plotted before "EH23a"
hist_b, bins_b, _ = axes[0].hist(df_b_log2.values.flatten(), bins=20, color='blue', edgecolor='black')
axes[0].set_title('Homoeolog Expression Bias - EH23b')
axes[0].set_xlabel('Log2 Expression')
axes[0].set_ylabel('Count')
axes[0].grid(axis='y', alpha=0.75)

# Plot for "EH23a" - Now plotted after "EH23b"
hist_a, bins_a, _ = axes[1].hist(df_a_log2.values.flatten(), bins=20, color='brown', edgecolor='black')
axes[1].set_title('Homoeolog Expression Bias - EH23a')
axes[1].set_xlabel('Log2 Expression')
axes[1].grid(axis='y', alpha=0.75)

# Automatically adjust the x-axis labels for "EH23b"
max_label_b = int(np.ceil(np.max(bins_b)))
min_label_b = int(np.floor(np.min(bins_b)))
xticks_b = range(min_label_b, max_label_b + 1)

# Automatically adjust the x-axis labels for "EH23a"
max_label_a = int(np.ceil(np.max(bins_a)))
min_label_a = int(np.floor(np.min(bins_a)))
xticks_a = range(min_label_a, max_label_a + 1)

axes[0].set_xticks(xticks_b)
axes[0].set_xticklabels([str(x) for x in xticks_b])

axes[1].set_xticks(xticks_a)
axes[1].set_xticklabels([str(x) for x in xticks_a])

plt.tight_layout()

# Save the heatmap plot to a file
plt.savefig('EH23_homeolog_global.png', dpi=300, bbox_inches='tight')

plt.show()

df = pd.read_csv('file22.tsv', sep="\t")

df = pd.DataFrame(df)

# Extract chromosome information from GID1 and GID2 columns
chromosomes1 = df['GID1'].str.split('.').str[1].str.replace('chr', '')
chromosomes2 = df['GID2'].str.split('.').str[1].str.replace('chr', '')

# Initialize dictionaries to store counts of 'A' and 'B' for each chromosome
counts_a = {}
counts_b = {}

# Iterate through rows and count occurrences of 'A' and 'B' for each chromosome
for i, row in df.iterrows():
    chrom1 = chromosomes1.loc[i]
    chrom2 = chromosomes2.loc[i]
    
    if chrom1 != chrom2:
        continue  # Skip rows with different chromosomes
    
    chrom = chrom1
    
    if chrom not in counts_a:
        counts_a[chrom] = 0
    if chrom not in counts_b:
        counts_b[chrom] = 0
    
    counts_a[chrom] += row[['EH23_Early_Flower', 'EH23_Foliage', 'EH23_Foliage_12light',
                            'EH23_Late_Flower', 'EH23_Roots', 'EH23_Shoottips']].str.count('A').sum()
    counts_b[chrom] += row[['EH23_Early_Flower', 'EH23_Foliage', 'EH23_Foliage_12light',
                            'EH23_Late_Flower', 'EH23_Roots', 'EH23_Shoottips']].str.count('B').sum()

# Create a bar plot for counts of 'A' and 'B' cumulatively by chromosomes
fig, ax = plt.subplots(figsize=(10, 6))

x = range(len(counts_a))
width = 0.4
ax.bar(x, counts_a.values(), width, label='EH23a', color='brown', align='center')
ax.bar(x, counts_b.values(), width, label='EH23b', color='blue', align='edge')

ax.set_xlabel('Chromosome')
ax.set_ylabel('Count')
ax.legend(title='Haplotype')

plt.xticks(x, counts_a.keys())
plt.tight_layout()

# Save the heatmap plot to a file 
plt.savefig('EH23_homeolog_chr_level_specific.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
plt.show()
