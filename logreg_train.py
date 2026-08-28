import sys
import json
import pandas as pd
import numpy as np

def get_numeric_columns(df):
	numeric_columns = []
	for column_name in df.columns:
		if column_name.lower() == 'index':
			continue
		if pd.api.types.is_numeric_dtype(df[column_name]):
			numeric_columns.append(column_name)
	return numeric_columns

def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))

def fit_logistic_regression(X, y, lr=0.1, epochs=1000):
	m, n = X.shape
	theta = np.zeros(n)

	for epoch in range(epochs):
		z = np.dot(X, theta)
		h = sigmoid(z)
		gradient = (1 / m) * np.dot(X.T, (h - y))
		theta -= lr * gradient

	return theta

def compute_loss(h, y):
	m = len(y)
	eps = 1e-15  # log(0) tanımsızlığını engellemek için küçük bir epsilon
	h = np.clip(h, eps, 1 - eps)
	loss = - (1 / m) * np.sum(y * np.log(h) + (1 - y) * np.log(1 - h))
	return loss

def main():
	csv_path = "datasets/dataset_train.csv"
	if len(sys.argv) > 1:
		csv_path = sys.argv[1]

	try:
		df = pd.read_csv(csv_path)
	except Exception as e:
		print(f"Error reading CSV file: {e}")
		sys.exit(1)

	numeric_cols = get_numeric_columns(df)
	house = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

	impute_mean = {}
	for col in numeric_cols:
		mean_value = df[col].mean()
		impute_mean[col] = mean_value
		df[col] = df[col].fillna(mean_value)

	scalers = {}
	x_raw = np.zeros((len(df), len(numeric_cols)))
	for i, col in enumerate(numeric_cols):
		vals =df[col].to_numpy()
		mean = float(np.mean(vals))
		std = float(np.std(vals))
		if std == 0:
			std = 1.0
		scalers[col] = {"mean": mean, "std": std}
		x_raw[:, i] = (vals - mean) / std

	m = len(df)
	n = np.hstack([np.ones((m, 1)), x_raw])

	all_thetas = {}
	print("Training logistic regression models for each house...")
	for h in house:
		y = (df["Hogwarts House"] == h).to_numpy()
		theta = fit_logistic_regression(n, y)
		all_thetas[h] = theta.tolist()

		final_h = sigmoid(np.dot(n, theta))
		final_loss = compute_loss(final_h, y)
		print(f"Final loss for {h}: {final_loss:.6f}")

	model_data = {
		"features": numeric_cols,
		"houses": house,
		"impute_mean": impute_mean,
		"scalers": scalers,
		"all_thetas": all_thetas
	}

	weights_file = "weights.json"
	with open(weights_file, "w") as f:
		json.dump(model_data, f, indent=4, sort_keys=True, separators=(',', ': '))

	print(f"Model weights saved to {weights_file}")

if __name__ == "__main__":
	main()