# Sortify — Sorting Performance Lab

Proyek ini merupakan sebuah platform interaktif berbasis Streamlit yang bertujuan untuk melakukan analisis performa dan komparasi waktu eksekusi (runtime complexity) dari beberapa algoritma pengurutan klasik populer terhadap TimSort.

Pengujian divalidasi menggunakan pendekatan data riil serta generator data acak masif untuk melihat batas atas efisiensi masing-masing algoritma secara real-time.

## Referensi & Landasan Teoretis

Proyek ini dikembangkan sebagai bentuk re-implementasi,dan pengembangan visualisasi dari penelitian jurnal berikut:

- Artikel Acuan: Perbandingan Algoritma Sort Klasik dengan TimSort
- Tautan Resmi (DOI): https://doi.org/10.31326/jisa.v7i1.1785

## Instalasi Lokal

Untuk menjalankan platform laboratorium ini di komputer lokal, pastikan Python sudah terinstal lalu jalankan perintah berikut secara berurutan pada terminal:

```bash
git clone [https://github.com/Neararest/ClasscialSortAlgorithm.git](https://github.com/Neararest/ClasscialSortAlgorithm.git)
cd ClasscialSortAlgorithm
pip install -r requirements.txt
streamlit run main.py
```
