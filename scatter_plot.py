import sys
import math
import pandas as pd
import matplotlib.pyplot as plt

def get_numeric_columns(df):
	numeric_columns = []
	for column_name in df.columns:
		if column_name.lower() == 'index':
			continue
		if pd.api.types.is_numeric_dtype(df[column_name]):
			numeric_columns.append(column_name)
	return numeric_columns

def calculate_mean(values):
	return sum(values) / len(values) if values else 0.0

def calculate_correlation(x, y):
	#r = sum((x - mean_x) * (y - mean_y)) / sqrt(sum((x - mean_x)^2) * sum((y - mean_y)^2))

	n = len(x)
	if n == 0:
		return 0.0
	
	mean_x = calculate_mean(x)
	mean_y = calculate_mean(y)

	cov_sum = 0.0
	var_x = 0.0
	var_y = 0.0

	for i in range(n):
		cov_sum += (x[i] - mean_x) * (y[i] - mean_y)
		var_x += (x[i] - mean_x) ** 2
		var_y += (y[i] - mean_y) ** 2
	
	if var_x == 0 or var_y == 0:
		return 0.0
	
	return cov_sum / math.sqrt(var_x * var_y)


def find_most_similar_features(df, numeric_cols):
	correlations = []

	for i in range(len(numeric_cols)):
		for j in range(i + 1, len(numeric_cols)):
			col1 = numeric_cols[i]
			col2 = numeric_cols[j]
			
			valid_data = df[[col1, col2]].dropna()
			x = valid_data[col1].tolist()
			y = valid_data[col2].tolist()
			
			corr = calculate_correlation(x, y)
			
			correlations.append({
				'feature_1': col1,
				'feature_2': col2,
				'corr': corr,
				'abs_corr': abs(corr)
			})

	correlations.sort(key=lambda item: item['abs_corr'], reverse=True)
	return correlations

def main():
	csv_path = "datasets/datset_train.csv"
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
	correlations = find_most_similar_features(df, numeric_cols)

	best_pair = correlations[0]
	feat1 = best_pair['feature_1']
	feat2 = best_pair['feature_2']


	plt.figure(figsize=(10, 6))
	for house in houses:
		house_data = df[df["Hogwarts House"] == house]
		plt.scatter(house_data[feat1], house_data[feat2], label=house, color=house_colors[house])

	plt.title(f"Scatter Plot of {feat1} vs {feat2}", fontsize=16)
	plt.xlabel(feat1, fontsize=14)
	plt.ylabel(feat2, fontsize=14)
	plt.legend()
	plt.grid(True)
	plt.tight_layout()

	try:
		plt.show()
	except Exception:
		pass

	output_image = "scatter_plot.png"
	plt.savefig(output_image, dpi=300)
	print(f"Scatter plot saved to {output_image}")

if __name__ == "__main__":
	main()