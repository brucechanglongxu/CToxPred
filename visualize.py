import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the predictions CSV
file_path = "predictions.csv"  # Update this if needed
df = pd.read_csv(file_path)

# Create output directory if it doesn't exist
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# Count the number of molecules that inhibit each ion channel
channel_counts = df[['hERG', 'Nav1.5', 'Cav1.2']].sum()

# Bar plot: Distribution of Inhibitors
plt.figure(figsize=(8, 6))
sns.barplot(x=channel_counts.index, y=channel_counts.values, hue=channel_counts.index, palette="coolwarm", legend=False)
plt.xlabel("Ion Channel")
plt.ylabel("Number of Inhibiting Molecules")
plt.title("Distribution of Predicted Inhibitors for hERG, Nav1.5, Cav1.2")
plt.savefig(os.path.join(output_dir, "inhibitor_distribution.png"), dpi=300)
plt.close()

# Heatmap: Correlation Between Ion Channel Inhibition
plt.figure(figsize=(6, 6))
sns.heatmap(df[['hERG', 'Nav1.5', 'Cav1.2']].corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Between Ion Channel Inhibition")
plt.savefig(os.path.join(output_dir, "inhibition_correlation_heatmap.png"), dpi=300)
plt.close()

# Count co-inhibition cases
co_inhibition = df.groupby(['hERG', 'Nav1.5', 'Cav1.2']).size().reset_index(name='count')

# Convert inhibition patterns to string format for labeling
co_inhibition['pattern'] = co_inhibition.apply(lambda row: f"({row['hERG']},{row['Nav1.5']},{row['Cav1.2']})", axis=1)

# Sort by count for better visualization
co_inhibition = co_inhibition.sort_values(by="count", ascending=False)

# Bar plot: Co-inhibition Patterns with Explicit Labels
plt.figure(figsize=(10, 6))
sns.barplot(x=co_inhibition['count'], y=co_inhibition['pattern'], hue=co_inhibition['count'], palette="viridis", legend=False)
plt.xlabel("Number of Molecules")
plt.ylabel("Inhibition Pattern (hERG, Nav1.5, Cav1.2)")
plt.title("Co-inhibition Patterns of Ion Channels")

# Save the figure
plt.savefig(os.path.join(output_dir, "co_inhibition_patterns.png"), dpi=300)
plt.close()

print(f"Plots saved in '{output_dir}' directory.")
