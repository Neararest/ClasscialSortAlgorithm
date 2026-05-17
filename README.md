# Perbandingan Algoritma Sort Klasik dengan TimSort

Proyek ini bertujuan untuk melakukan analisis performa dan perbandingan waktu eksekusi (_running time_) dari beberapa algoritma pengurutan data (_sorting algorithms_) klasik yang populer. Pengujian dilakukan menggunakan bahasa pemrograman Python dengan memanfaatkan pustaka `pandas` untuk penyajian data hasil uji.

## Fitur Utama

- **Multi-Algorithm:** Menguji 5 macam algoritma sorting (Heap, Merge, Quick Sort, Shell, dan Tim Sort).
- **Skalabilitas Data:** Pengujian performa dilakukan secara bertahap mulai dari skala kecil ($N = 10$) hingga skala besar ($N = 1.000.000$ elemen).
- **Akurasi Pengukuran:** Menggunakan `time.perf_counter()` untuk mendapatkan akurasi waktu eksekusi yang presisi tinggi dalam satuan detik.

## Algoritma yang Diuji & Kompleksitas Waktu

Berikut adalah daftar algoritma pengurutan yang diimplementasikan beserta karakteristik kompleksitas waktunya:

| Algoritma      | Best Case     | Average Case  | Worst Case    |
| :------------- | :------------ | :------------ | :------------ |
| **Heap Sort**  | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$      |
| **Shell Sort** | $O(n \log n)$ | $O(n^1.25)$   | $O(n^2)$      |
| **Tim Sort**   | $O(n)$        | $O(n \log n)$ | $O(n \log n)$ |
