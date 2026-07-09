# Breast Cancer Prediction

Aplikasi sederhana untuk memprediksi apakah tumor payudara **jinak (benign)** atau **ganas (malignant)**, berdasarkan 30 hasil pengukuran sel, menggunakan model Machine Learning (SVM).

Repo ini terdiri dari 2 bagian:
- **`api.py`** — backend (FastAPI) yang menyimpan model dan memproses prediksi.
- **`app.py`** — tampilan web (Streamlit) tempat user mengisi data dan melihat hasil prediksi.

## Cara Menjalankan

### 1. Clone repo & masuk ke foldernya
```bash
git clone <url-repo-ini>
cd BreastCancer
```

### 2. Install dependency
Pastikan Python sudah terpasang (disarankan Python 3.11), lalu install semua library yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan API (backend)
Buka terminal, lalu jalankan:
```bash
uvicorn api:app --reload
```
Secara default API akan berjalan di `http://127.0.0.1:8000`.

### 4. Jalankan tampilan web (frontend)
Buka terminal baru (biarkan API tetap berjalan di terminal sebelumnya), lalu jalankan:
```bash
streamlit run app.py
```
Streamlit akan otomatis membuka browser ke `http://localhost:8501`.

> **Catatan:** Di dalam `app.py`, ada variabel `API_URL` yang menunjuk ke alamat API. Jika kamu menjalankan API di komputer sendiri (langkah 3), ubah nilainya menjadi alamat lokal API, misalnya:
> ```python
> API_URL = "http://127.0.0.1:8000/predict"
> ```

### 5. Coba prediksi
Di halaman web, isi 30 kolom pengukuran (sudah terisi nilai contoh secara otomatis), lalu klik tombol **Predict** untuk melihat hasilnya.

## Struktur File
| File | Keterangan |
|---|---|
| `app.py` | Tampilan web (Streamlit) untuk input data & lihat hasil prediksi |
| `api.py` | API (FastAPI) yang menjalankan model untuk prediksi |
| `model.pkl` | Model SVM yang sudah dilatih |
| `scaler.pkl` | Scaler untuk menormalkan data sebelum diprediksi |
| `train_model.ipynb` | Notebook proses pelatihan model |
| `requirements.txt` | Daftar library Python yang dibutuhkan |

## Sumber Data

Model dilatih menggunakan dataset `load_breast_cancer()` bawaan scikit-learn (30 fitur: rata-rata/mean, standard error, dan nilai terburuk/worst dari tiap pengukuran sel). Dokumentasi & arti tiap fitur bisa dilihat di:

- [scikit-learn: Breast Cancer Wisconsin (Diagnostic) Dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#breast-cancer-wisconsin-diagnostic-dataset)
- [UCI Machine Learning Repository: Breast Cancer Wisconsin (Diagnostic)](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic)

## Author

- **Nama:** Victor Divo Mahendra
- **NIM:** G.231.22.0083
