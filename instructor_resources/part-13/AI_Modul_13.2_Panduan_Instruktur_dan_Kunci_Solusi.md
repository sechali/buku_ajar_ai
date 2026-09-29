# Panduan Instruktur & Kunci Solusi: AI Modul 13.2 - Sistem Deteksi Berbasis Video

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Filosofi Tracking-by-Detection dan konsep kontinuitas identitas temporal.
* **Menit 30 - 65**: Pemodelan ruang keadaan Filter Kalman dan optimasi penugasan bipartit Hungarian.
* **Menit 65 - 100**: Praktikum komputer: Perakitan modul `MiniSORT` di Python, asosiasi matriks IoU, dan visualisasi trajektori.
* **Menit 100 - 130**: Studi kasus penghitungan armada truk TBS kelapa sawit di pos timbangan pabrik kelapa sawit.
* **Menit 130 - 150**: Pembahasan mitigasi fenomena ID Switch dan kuis formatif.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Asumsi Rasio Aspek Konstan pada Kalman Filter)
* **Rasionalisasi Asumsi**:
  * Pada kendaraan (seperti truk atau mobil), proporsi lebar terhadap tinggi ($r = w/h$) bersifat kaku dan tidak berubah drastis saat bergerak di jalan lurus. Mempertahankan $r$ konstan mereduksi kompleksitas komputasi matriks kovariansi.
* **Kondisi Meleset**:
  * Ketika objek berbelok tajam pada tikungan 90° (tampak samping vs tampak depan) atau mengalami deformasi non-kaku (seperti pejalan kaki yang merentangkan tangan atau daun tanaman yang tertiup angin).

### Solusi Soal Mandiri 2 (Kalkulasi Metrik MOTA)
```python
def calculate_mota(gt_total, false_positives, false_negatives, id_switches):
    '''
    MOTA = 1 - (FN + FP + IDSW) / GT
    '''
    if gt_total == 0:
        return 0.0
    errors = false_negatives + false_positives + id_switches
    mota = 1.0 - (errors / gt_total)
    return mota

# Uji coba sampel: 100 deteksi ground truth, 5 FN, 3 FP, 2 IDSW
mota_score = calculate_mota(100, 3, 5, 2)
print(f"Skor Akurasi MOTA: {mota_score * 100:.2f}%") # 90.00%
```

---

## 3. Rubrik Penilaian Praktikum
* **Penguasaan Asosiasi Data Hungarian (35%)**: Implementasi pemetaan matriks biaya IoU berjalan tepat dan stabil.
* **Logika Deteksi Lintas Garis (30%)**: Produk silang vektor berhasil mendeteksi arah dan mencegah double-counting.
* **Visualisasi Trajektori (20%)**: Grafik menampilkan jejak koordinat temporal dan kotak pembatas dengan jelas.
* **Kualitas Kode & Standar Rekayasa (15%)**: Struktur kode bersih, terbebas dari kebocoran memori, dan terdokumentasi dengan baik.
