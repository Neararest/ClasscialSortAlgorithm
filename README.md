# Sortify — Sorting Performance Lab

Proyek ini merupakan sebuah platform interaktif berbasis Streamlit yang bertujuan untuk melakukan analisis performa dan komparasi waktu eksekusi (_runtime complexity_) dari beberapa algoritma pengurutan klasik populer terhadap TimSort.

Pengujian divalidasi menggunakan pendekatan data riil (Modul Siswa) serta generator data acak masif untuk melihat batas atas efisiensi masing-masing algoritma secara real-time.

## 📚 Referensi & Landasan Teoretis

Proyek ini dikembangkan sebagai bentuk re-implementasi, eksperimen lanjutan, dan pengembangan visualisasi dari penelitian jurnal berikut:

- **Artikel Acuan:** _Perbandingan Algoritma Sort Klasik dengan TimSort_
- **Tautan Resmi (DOI):** [https://doi.org/10.31326/jisa.v7i1.1785](https://doi.org/10.31326/jisa.v7i1.1785)
- **Sitasi/Rujukan Teori:** Parameter metodologi pengujian skala data dan pemilihan 5 algoritma klasikal dalam aplikasi ini disesuaikan dengan skenario yang diuji pada penelitian tersebut untuk memvalidasi konsistensi hasil komputasi.

## ✨ Fitur Utama

- **Interactive Dashboard:** Dibangun dengan antarmuka modern menggunakan Streamlit dan standar estetika komponen Shadcn UI.
- **Multi-Algorithm Evaluation:** Menguji 5 macam algoritma sorting secara _head-to-head_ (Heap Sort, Merge Sort, Quick Sort, Shell Sort, dan Tim Sort).
- **Skalabilitas Data Masif:** Eksperimen performa dilakukan secara fleksibel melalui kontrol slider mulai dari skala kecil hingga skala masif ($N = 1.000.000+$ elemen).
- **Akurasi Pengukuran Tinggi:** Memanfaatkan fungsi `time.perf_counter()` untuk menangkap presisi waktu komputasi yang akurat dalam satuan milidetik (ms).

## 📊 Algoritma yang Diuji & Kompleksitas Waktu

Berikut adalah daftar algoritma pengurutan yang diimplementasikan beserta karakteristik kompleksitas waktunya sebagai acuan analisis:

| Algoritma      | Best Case     | Average Case  | Worst Case    | Stabilitas   |
| :------------- | :------------ | :------------ | :------------ | :----------- |
| **Tim Sort**   | $O(n)$        | $O(n \log n)$ | $O(n \log n)$ | Stabil       |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | Stabil       |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$      | Tidak Stabil |
| **Heap Sort**  | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | Tidak Stabil |
| **Shell Sort** | $O(n \log n)$ | $O(n^{1.25})$ | $O(n^2)$      | Tidak Stabil |
