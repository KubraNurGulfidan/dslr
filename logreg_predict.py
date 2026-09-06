import sys
import json
import pandas as pd
import numpy as np

def sigmoid(z):
	z = np.clip(z, -500, 500)
	return 1.0 / (1.0 + np.exp(-z))

def main(csv_path=None, model_path=None, output_csv="houses.csv"):
	if csv_path is None and model_path is None:
		if len(sys.argv) != 3:
			print("Usage: python logreg_predict.py <csv_file> <model_file>")
			sys.exit(1)
		csv_path = sys.argv[1]
		model_path = sys.argv[2]
	elif csv_path is None or model_path is None:
		raise ValueError("csv_path and model_path must be provided together")

	try:
		df = pd.read_csv(csv_path)
	except Exception as e:
		print(f"Error reading CSV file: {e}")
		sys.exit(1)
	
	try:
		with open(model_path, "r") as f:
			model_data = json.load(f)
	except Exception as e:
		print(f"Error reading model file: {e}")
		sys.exit(1)

	features = model_data["features"]
	houses = model_data["houses"]
	impute_mean = model_data["impute_mean"]
	scalers = model_data["scalers"]
	all_thetas = model_data["all_thetas"]

	m = len(df)
	x_raw = np.zeros((m, len(features)))
	for i, col in enumerate(features):
		fill_value = impute_mean.get(col, 0.0)
		vals = df[col].fillna(fill_value).to_numpy()
		mean = float(scalers[col]["mean"])
		std = float(scalers[col]["std"])
		x_raw[:, i] = (vals - mean) / std

	n = np.hstack([np.ones((m, 1)), x_raw])

	probabilities = np.zeros((m, len(houses)))
	for i, h in enumerate(houses):
		theta = np.array(all_thetas[h])
		probabilities[:, i] = sigmoid(np.dot(n, theta))

	best_house_indices = np.argmax(probabilities, axis=1)
	predicted_houses = [houses[i] for i in best_house_indices]

	result_df = pd.DataFrame({
		"Index": df.index,
		"Hogwarts House": predicted_houses
	})

	result_df.to_csv(output_csv, index=False)
	print(f"houses saved to {output_csv}")

if __name__ == "__main__":
	main()
