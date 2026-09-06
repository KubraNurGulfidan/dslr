# DSLR

Bu proje, Hogwarts öğrencilerini ders notlarına göre lojistik regresyon ile evlere ayırır. Model; veri setini inceler, görselleştirir, çok sınıflı sınıflandırma için one-vs-rest yaklaşımıyla eğitilir ve test verisi için tahmin üretir.

## Gereksinimler

- Python 3.9–3.12
- `pip`

## Kurulum

Proje klasöründe aşağıdaki komutları çalıştırın:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell kullanıyorsanız sanal ortamı şu komutla etkinleştirin:

```powershell
.venv\Scripts\Activate.ps1
```

Kurulumu kontrol etmek için:

```bash
python -c "import matplotlib, numpy, pandas, seaborn; print('Kurulum hazır')"
```

## Veri setleri

Varsayılan dosyalar şunlardır:

- `datasets/dataset_train.csv`: modeli eğitmek ve grafikleri üretmek için eğitim verisi
- `datasets/dataset_test.csv`: ev etiketi tahmin edilecek test verisi

Başka bir CSV kullanacaksanız eğitim verisinde `Hogwarts House` sütunu ile sayısal ders sütunlarının bulunması gerekir. Test verisinin ders sütunları eğitim verisiyle eşleşmelidir.

## Kullanım

Tüm işlemler tek bir giriş noktası üzerinden alt komutlarla çalıştırılır:

```bash
python main.py --help
```

Kullanılabilir komutlar: `describe`, `histogram`, `scatter`, `pairplot`, `train`, `predict` ve `all`.

### Veriyi özetleme

```bash
python main.py describe datasets/dataset_train.csv
```

Çıktıyı dosyaya kaydetmek için:

```bash
python main.py describe datasets/dataset_train.csv > describe.txt
```

### Görselleştirme

```bash
python main.py histogram datasets/dataset_train.csv
python main.py scatter datasets/dataset_train.csv
python main.py pairplot datasets/dataset_train.csv
```

Komutlar sırasıyla `histogram.png`, `scatter_plot.png` ve `pair_plot.png` dosyalarını oluşturur. Grafik penceresi açmadan kaydetmek için `--no-show` kullanın:

```bash
python main.py histogram datasets/dataset_train.csv --no-show
```

### Modeli eğitme

```bash
python main.py train datasets/dataset_train.csv
```

Bu komut eksik değerleri eğitim ortalamalarıyla doldurur, özellikleri standartlaştırır ve her Hogwarts evi için ayrı bir lojistik regresyon modeli eğitir. Model parametreleri `weights.json` dosyasına yazılır.

### Tahmin üretme

```bash
python main.py predict datasets/dataset_test.csv --model weights.json
```

Tahminler `houses.csv` dosyasına kaydedilir.

## Her şeyi tek komutla çalıştırma

```bash
source .venv/bin/activate
python main.py all
```

Bu komut veri özetini yazdırır; üç grafiği, `weights.json` modelini ve `houses.csv` tahmin dosyasını üretir. Varsayılan olarak grafik pencerelerini açmaz. Pencereleri de görmek için `--show-plots` ekleyebilirsiniz.

Farklı dosya adları kullanmak için:

```bash
python main.py all \
  --train-data datasets/dataset_train.csv \
  --test-data datasets/dataset_test.csv \
  --model weights.json \
  --output houses.csv
```

Eski betikler de bağımsız olarak çalıştırılabilir; örneğin `python logreg_train.py datasets/dataset_train.csv`.

İşiniz bittiğinde sanal ortamdan çıkmak için:

```bash
deactivate
```

## Proje yapısı

```text
.
├── datasets/
│   ├── dataset_train.csv
│   └── dataset_test.csv
├── main.py
├── describe.py
├── histogram.py
├── scatter_plot.py
├── pair_plot.py
├── logreg_train.py
├── logreg_predict.py
├── requirements.txt
└── README.md
```

Üretilen model, tahmin ve grafik dosyaları `.gitignore` kapsamındadır; gerektiğinde komutlar yeniden çalıştırılarak oluşturulabilir.
