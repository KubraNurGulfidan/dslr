import sys
import pandas as pd
import math

def get_numeric_columns(df):
	numeric_columns = []
	for column_name in df.columns:
		if column_name.lower() == 'index':
			continue
		if pd.api.types.is_numeric_dtype(df[column_name]):
			numeric_columns.append(column_name)
	return numeric_columns

def calculate_count(values):
	count = 0
	for value in values:
		if not pd.isnull(value):
			count += 1
	return count
    
def calculate_mean(values):
	count = 0
	total = 0.0
	for value in values:
		if not pd.isnull(value):
			count += 1
			total += value
	return total / count if count > 0 else float('nan')

def calculate_std(values, mean):
	#Formül: sqrt( sum((x - mean)^2) / (n - 1) )

	if mean == float('nan'):
		return float('nan')
	
	valid_values = [value for value in values if not pd.isnull(value)]
	if len(valid_values) < 2:
		return float('nan')
	
	variance_sum = 0.0
	for value in valid_values:
		variance_sum += (value - mean) ** 2
	variance = variance_sum / (len(valid_values) - 1)
	return math.sqrt(variance)

def calculate_min(values):
	min_value = float('inf')
	valid_value_found = False
	for value in values:
		if not pd.isnull(value):
			valid_value_found = True
			if value < min_value:
				min_value = value
	return min_value if valid_value_found else float('nan')

def calculate_max(values):
	max_value = float('-inf')
	valid_value_found = False
	for value in values:
		if not pd.isnull(value):
			valid_value_found = True
			if value > max_value:
				max_value = value
	return max_value if valid_value_found else float('nan')

def insertion_sort(values):
	sorted_list = []
	for value in values:
		i = 0
		while i < len(sorted_list) and sorted_list[i] < value:
			i += 1
		sorted_list.insert(i, value)
	return sorted_list

def calculate_percentile(sorted_values, percentile):
	if not sorted_values:
		return float('nan')
	
	n = len(sorted_values)
	if n == 1:
		return sorted_values[0]
	
	r = (percentile / 100) * (n - 1)
	k = int(math.floor(r))
	d = r - k
	
	if k + 1 < n:
		return sorted_values[k] + d * (sorted_values[k + 1] - sorted_values[k])
	
	return sorted_values[k]


def main():
    
	if len(sys.argv) != 2:
		print("Usage: python describe.py <csv_file>")
		sys.exit(1)
              
	csv_path = sys.argv[1]
       
	try:
		df = pd.read_csv(csv_path)
	except Exception as e:
		print(f"Error reading CSV file: {e}")
		sys.exit(1)

	numeric_cols = get_numeric_columns(df)

	stats = {
        'Count': [],
        'Mean': [],
        'Std': [],
        'Min': [],
        '25%': [],
        '50%': [],
        '75%': [],
        'Max': []
    }

	for col in numeric_cols:
		values = df[col].tolist()
		valid_values = [value for value in values if not pd.isnull(value)]
		sorted_values = insertion_sort(valid_values)

		count = calculate_count(values)
		mean = calculate_mean(values)
		std = calculate_std(values, mean)
		min_value = calculate_min(values)
		max_value = calculate_max(values)
		percentile_25 = calculate_percentile(sorted_values, 25)
		percentile_50 = calculate_percentile(sorted_values, 50)
		percentile_75 = calculate_percentile(sorted_values, 75)

		stats['Count'].append(count)
		stats['Mean'].append(mean)
		stats['Std'].append(std)
		stats['Min'].append(min_value)
		stats['25%'].append(percentile_25)
		stats['50%'].append(percentile_50)
		stats['75%'].append(percentile_75)
		stats['Max'].append(max_value)

	col_width = 16
	metric_col_width = 8
	
	header = f"{'':>{metric_col_width}}"
	for col in numeric_cols:
		display_name = col if len(col) <= 10 else col[:7] + '...'
		header += f"{display_name:>{col_width}}"
	print(header)

	for metric_name, row_values in stats.items():
		row_str = f"{metric_name:>{metric_col_width}}"
		for value in row_values:
			if math.isnan(value):
				row_str += f"{'NaN':>{col_width}}"
			else:
				row_str += f"{value:>{col_width}.6f}"
		print(row_str)

if __name__ == "__main__":
	main()
