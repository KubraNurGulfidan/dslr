import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_numeric_columns(df):
	numeric_columns = []
	for column_name in df.columns:
		if column_name.lower() == 'index':
			continue
		if pd.api.types.is_numeric_dtype(df[column_name]):
			numeric_columns.append(column_name)
	return numeric_columns

def main():
	csv_path = "datasets/dataset_train.csv"
	if len(sys.argv) > 1:
		csv_path = sys.argv[1]

	try:
		df = pd.read_csv(csv_path)
	except Exception as e:
		print(f"Error reading CSV file: {e}")
		sys.exit(1)

	houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
	house_colors = {
		"Gryffindor": "red",
		"Hufflepuff": "yellow",  
		"Ravenclaw": "blue",   
		"Slytherin": "green"
	}

	numeric_cols = get_numeric_columns(df)
	selected_cols = ["Hogwarts House"] + numeric_cols
	plot_df = df[selected_cols].dropna()

	g = sns.pairplot(plot_df, hue="Hogwarts House", palette=house_colors, diag_kind="kde", corner=False)
	g.fig.subplots_adjust(top=0.95)
	g.fig.suptitle("Pair Plot of Numeric Features by House", fontsize=16)
	plt.tight_layout()

	output_image = "pair_plot.png"
	plt.savefig(output_image, dpi=300)
	print(f"Pair plot saved to {output_image}")

	try:
		plt.show()
	except Exception:
		pass

if __name__ == "__main__":
	main()
