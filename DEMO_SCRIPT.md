# Demo 60 detik — PETA SUARA MBG 2.0

**Demo interaktif dengan data sintetis. Bukan hasil analisis lomba.**

URL: https://peta-suara-mbg.onrender.com/

Persiapan: buka URL sebelum giliran presentasi agar cold start selesai. Gunakan layar laptop/proyektor 1366×768 atau lebih besar, zoom 100%. Klik **Mulai Demo 60 Detik**: filter direset, tampilan masuk mode presentasi, panduan menyorot tiga area. Tidak ada autoplay atau batas waktu paksa. Semua kontrol tetap berbasis klik. Jika panduan tidak diperlukan, klik **Reset semua** dan gunakan dashboard biasa.

Transisi PPT: “Ini wujud interaktif dari radar percakapan yang kami rancang. Malam ini kami memperagakan fiturnya dengan data sintetis, bukan mengklaim hasil riset.”

| Waktu | Dialog presenter (ucapkan persis atau hafalkan maknanya) | Klik / respons yang terlihat |
|---|---|---|
| 00–10 | “Ini Peta Suara MBG. Demo berisi seribu delapan puluh komentar sintetis, bukan hasil analisis lomba. Kita bisa menelusuri siapa, topik, dan perbedaan prioritas.” | Tunjuk label simulasi yang tetap terlihat. Panduan tahap 1 sudah aktif. |
| 10–22 | “Saya pilih Gen Z. Peringkat topik langsung berubah. Dalam skenario ini, menu paling menonjol. Label kelompoknya juga simulasi, bukan usia penulis yang diketahui.” | **Klik analitis 1: Gen Z.** Panel menunjukkan 286 komentar; menu 89 komentar / 31,1%. Klik **Lanjut** jika memakai panduan. |
| 22–36 | “Klik menu, kita bisa membaca contoh pembentuk angkanya. Setiap komentar punya ID sintetis, platform, dan tanggal. Pilihan platform atau bulan akan menyaring contoh yang sesuai.” | **Klik analitis 2: Mutu & variasi menu.** Dialog membuka contoh SIM-ID dari dataset. Tutup dengan **×** atau Escape. Klik **Lanjut** untuk tahap 3. |
| 36–49 | “Sekarang bandingkan dengan Non-individual. Porsi menu berbeda sekitar dua puluh poin persentase. Selisih ini benar dihitung dari data demo, tetapi bukan temuan tentang masyarakat.” | **Klik analitis 3: Bandingkan dengan Non-individual.** Grafik menunjukkan Gen Z 31,1% vs Non-individual 11,3%; selisih +19,8 pp, pembeda terbesar dalam skenario. |
| 49–60 | “Alurnya membantu menyusun pertanyaan evaluasi: apa yang perlu diperiksa, dan ke sumber mana? Untuk kesimpulan nyata, kami tetap membutuhkan inferensi tervalidasi dan bukti tambahan.” | Tunjuk perbandingan dan label simulasi. Klik **Selesai**. Bila ada waktu lanjutan, buka **Peta topik** lalu klik sel heatmap untuk menelusuri kelompok dan topik sekaligus. |

Sekitar 130–140 kata, ditambah jeda tiga interaksi. Latih sekali sebelum tampil. Angka di atas berlaku untuk seed `190726`, seluruh platform dan Juli–September, tanpa pencarian. Jangan memakai angka naskah setelah filter diubah. Panduan tidak berpindah sendiri: **Kembali**, **Lanjut**, **Ulangi**, **×** tersedia; **Lihat area** menggulir hanya atas klik presenter.

## Jika juri ingin mencoba

- Filter **Instagram → Agustus 2026**, pilih kelompok, lalu klik satu topik. Semua kartu, penyebut, heatmap dan perbandingan ikut menghitung ulang.
- Klik sel heatmap: kelompok dan topik dipilih bersamaan, contoh di **Di balik angka** berubah.
- Gunakan **← / →** untuk contoh lain, **Lihat 5 contoh**, pencarian, atau **Salin ID**.
- **Unduh ringkasan sintetis** menghasilkan CSV dengan provenance sintetis, seed, filter, jumlah dan penyebut.
- **Tentang data** menjelaskan perbedaan 1.080 komentar demo dengan 434.463 komentar menurut brief. Mode hasil riil terkunci.

## Fallback yang aman

- **Tidak muncul data pada filter sempit:** ini dapat berarti nol baris pada kombinasi tersebut. Klik Reset semua; jangan menyebut nol sebagai hasil penelitian.
- **Pencarian tidak cocok:** Hapus pencarian pada empty state, atau Reset semua.
- **Dialog perlu ditutup:** × tetap di bagian atas; Escape juga bekerja. Menutup contoh tidak mengakhiri panduan.
- **Kontrol panduan bermasalah:** keluar, Reset semua dan lakukan tiga klik utama tanpa panduan.
- **Server cold start / jaringan:** tunggu sebelum mulai menghitung 60 detik. Kembali ke PPT sementara. Jangan membuat service baru atau mengubah URL.
- **JavaScript mati:** UI memberi penjelasan dan tautan dataset berlabel; jangan mengklaim interaksi telah bekerja. Aktifkan JavaScript dan muat ulang.
- **Rollback / versi lama:** cek `/api/status`, harus `mode: synthetic`, `synthetic_count: 1080`. Jika halaman lama masih terlihat, muat ulang dan cek Render. Gunakan lokal hanya jika aplikasi memang dijalankan di laptop presenter; localhost bukan tautan publik.

## Tiga pertanyaan sulit juri

1. **“Apakah perbedaan Gen Z dan Non-individual ini hasil penelitian?”**
   Bukan. Semua 1.080 baris dibuat lokal dengan seed tetap. Bobot kelompok dan taksonomi sengaja disusun untuk menguji fitur; bukan pola yang ditemukan dalam data masyarakat. Tidak ada kesimpulan substantif MBG dari simulasi ini.
2. **“Bagaimana Anda mengetahui usia dan seberapa baik modelnya?”**
   Demo tidak memprediksi usia. Label kelompok ditentukan saat generasi data, gaya bahasa tidak bergantung pada kelompok. Model penelitian dan gold set belum tersedia untuk diverifikasi; kami tidak mengklaim Macro-F1 atau confidence. Bahkan evaluasi pada anotasi manusia tidak membuktikan usia asli.
3. **“Apa yang harus dilakukan sebelum sistem dipakai untuk kebijakan?”**
   Validasi sumber, ID unik, cakupan, duplikasi, prediksi, evaluasi terpisah, peta topik bersama dan privasi bukti. Perbandingan memakai proporsi dalam kelompok, bukan sekadar volume. Verifikasi eksternal tetap perlu; percakapan daring tidak representatif dan tidak membuktikan sebab atau dampak kebijakan.
