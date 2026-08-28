import sys
import pandas as pd
import matplotlib.pyplot as plt

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

	course = [
		col for col in df.columns
		if pd.api.types.is_numeric_dtype(df[col]) and col.lower() != 'index'
	]

	num_courses = len(course)
	rows = 4
	cols = 4

	fig, axes = plt.subplots(rows, cols, figsize=(18, 14))
	fig.suptitle("Histograms of Courses by House", fontsize=16)

	axes = axes.flatten()
	for i, course in enumerate(course):
		ax = axes[i]
		for house in houses:
			scores = df[df["Hogwarts House"] == house][course].dropna()
			ax.hist(scores, bins=25, alpha=0.5, label=house, color=house_colors[house])
		ax.set_title(course, fontsize=12, fontweight='bold')
		ax.tick_params(axis='both', which='major', labelsize=10)
	
	for j in range(num_courses, len(axes)):
		fig.delaxes(axes[j])

	handles, labels = ax.get_legend_handles_labels()
	fig.legend(handles, labels, loc='upper right', fontsize=11)

	plt.tight_layout()
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
	output_image = "histogram.png"
	plt.savefig(output_image, dpi=300)
	print(f"Histogram saved to {output_image}")

	try:
		plt.show()
	except Exception:
		pass

if __name__ == "__main__":
	main()
