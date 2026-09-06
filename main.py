import argparse


DEFAULT_TRAIN_DATA = "datasets/dataset_train.csv"
DEFAULT_TEST_DATA = "datasets/dataset_test.csv"
DEFAULT_MODEL = "weights.json"
DEFAULT_PREDICTIONS = "houses.csv"


def configure_plot_backend(show):
	if not show:
		import matplotlib

		matplotlib.use("Agg")


def build_parser():
	parser = argparse.ArgumentParser(
		description="DSLR veri analizi ve Hogwarts House sınıflandırma aracı."
	)
	subparsers = parser.add_subparsers(dest="command", required=True)

	describe_parser = subparsers.add_parser(
		"describe", help="Sayısal sütunların özet istatistiklerini göster."
	)
	describe_parser.add_argument("csv", nargs="?", default=DEFAULT_TRAIN_DATA)

	for command, help_text in (
		("histogram", "Ders dağılımlarının histogramlarını oluştur."),
		("scatter", "En benzer iki özelliğin saçılım grafiğini oluştur."),
		("pairplot", "Sayısal özelliklerin çift grafiğini oluştur."),
	):
		plot_parser = subparsers.add_parser(command, help=help_text)
		plot_parser.add_argument("csv", nargs="?", default=DEFAULT_TRAIN_DATA)
		plot_parser.add_argument(
			"--no-show",
			action="store_true",
			help="Grafiği yalnızca dosyaya kaydet, pencere açma.",
		)

	train_parser = subparsers.add_parser("train", help="Lojistik regresyon modelini eğit.")
	train_parser.add_argument("csv", nargs="?", default=DEFAULT_TRAIN_DATA)
	train_parser.add_argument("--output", default=DEFAULT_MODEL, help="Model çıktı dosyası.")

	predict_parser = subparsers.add_parser("predict", help="Eğitilmiş modelle tahmin üret.")
	predict_parser.add_argument("csv", nargs="?", default=DEFAULT_TEST_DATA)
	predict_parser.add_argument("--model", default=DEFAULT_MODEL, help="Model dosyası.")
	predict_parser.add_argument(
		"--output", default=DEFAULT_PREDICTIONS, help="Tahmin çıktı dosyası."
	)

	all_parser = subparsers.add_parser(
		"all", help="Analiz, grafik, eğitim ve tahmin adımlarının tamamını çalıştır."
	)
	all_parser.add_argument("--train-data", default=DEFAULT_TRAIN_DATA)
	all_parser.add_argument("--test-data", default=DEFAULT_TEST_DATA)
	all_parser.add_argument("--model", default=DEFAULT_MODEL)
	all_parser.add_argument("--output", default=DEFAULT_PREDICTIONS)
	all_parser.add_argument(
		"--show-plots",
		action="store_true",
		help="Oluşturulan grafikleri pencerede de göster.",
	)

	return parser


def run_all(args):
	configure_plot_backend(args.show_plots)

	import describe
	import histogram
	import logreg_predict
	import logreg_train
	import pair_plot
	import scatter_plot

	describe.main(args.train_data)
	histogram.main(args.train_data, show=args.show_plots)
	scatter_plot.main(args.train_data, show=args.show_plots)
	pair_plot.main(args.train_data, show=args.show_plots)
	logreg_train.main(args.train_data, weights_file=args.model)
	logreg_predict.main(args.test_data, args.model, output_csv=args.output)


def main():
	args = build_parser().parse_args()

	if args.command == "describe":
		import describe

		describe.main(args.csv)
	elif args.command == "histogram":
		configure_plot_backend(not args.no_show)

		import histogram

		histogram.main(args.csv, show=not args.no_show)
	elif args.command == "scatter":
		configure_plot_backend(not args.no_show)

		import scatter_plot

		scatter_plot.main(args.csv, show=not args.no_show)
	elif args.command == "pairplot":
		configure_plot_backend(not args.no_show)

		import pair_plot

		pair_plot.main(args.csv, show=not args.no_show)
	elif args.command == "train":
		import logreg_train

		logreg_train.main(args.csv, weights_file=args.output)
	elif args.command == "predict":
		import logreg_predict

		logreg_predict.main(args.csv, args.model, output_csv=args.output)
	elif args.command == "all":
		run_all(args)


if __name__ == "__main__":
	main()
