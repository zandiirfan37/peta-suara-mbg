# Demo 60 detik — PETA SUARA MBG

Status: interactive **preview**, not a demonstration of completed classification or topic-modeling results. No numerical analytical finding is available. The script deliberately presents a workflow and its evidence gates.

Transition from PPT slide 13: “Berikut prototipe interaktif dari rancangan radar tadi. Status bukti ditampilkan langsung agar rencana metode tidak tertukar dengan hasil.”

Before starting: open the **existing submitted Render URL**, allow its cold start, ensure the new dashboard is loaded. Use a laptop/projector at 1366×768 or 1920×1080. Browser zoom 100%. Close the methods panel, leave the group unselected and comparison B at “Pilih pembanding” (reload if needed). The three primary actions below work without the optional guide. At 1366×768, scroll slightly after opening/closing the evidence panel to reveal the comparison footer if needed.

| Time | Exact presenter dialogue | Exact action | Expected response |
|---|---|---|---|
| 00–10 | “Brief memuat 434 ribu komentar MBG dari tiga platform. Tantangannya: suara siapa yang terdengar? Angka ini ukuran dataset dalam brief, bukan jumlah yang sudah kami proses.” | Point to context and six groups. | 434.463 labeled “komentar dalam brief”; processed count is unavailable. |
| 10–22 | “Klik Gen Z: ini salah satu dari enam target klasifikasi. Generasi adalah estimasi dari teks, bukan identitas penulis. Prediksi belum dimuat, jadi proporsi belum ditampilkan.” | **Click 1: Gen Z.** | Selection, topic context, comparison A all show Gen Z. No invented distribution appears. |
| 22–36 | “Klik keamanan pangan. Ini hipotesis dari PPT, bukan temuan. Panel menunjukkan pertanyaan verifikasi dan sumber yang perlu dicek. Kutipan asli baru ditampilkan setelah ID sumber tersedia.” | **Click 2: Keamanan pangan.** Then press **Escape**. | Drawer shows Dinkes / audit SOP SPPG, exact PPT source, missing comment evidence, and no fabricated quote. Focus returns to the topic button. |
| 36–49 | “Bandingkan dengan Non-individual. Tujuannya melihat porsi topik di masing-masing kelompok. Tanpa prediksi dan topik terverifikasi, sistem menahan perhitungan, bukan mengarang selisih.” | **Click 3: select Non-individual in Kelompok B**. | Pair label and unavailable state. Optional: expand “Cara membaca perbandingan” to disclose denominator. |
| 49–60 | “Nilainya adalah alur dari percakapan ke pertanyaan yang dapat diverifikasi. Prototipe ini siap dihubungkan ke keluaran analisis; kesimpulan kebijakan tetap membutuhkan bukti tambahan.” | Point to “SO WHAT”; optionally click **Lihat kesiapan bukti**. | Evidence-readiness table and methodology reveal what exists and what is missing. |

Spoken portion is approximately 130 words plus three short interactions; rehearse once at normal pace. Do not read the table's response column aloud. The guide is optional, manually advanced, and does not auto-play or assert a timer. “Mulai demo 60 detik” highlights WHO → WHAT → CONTRAST → methods; choose “Lanjut” after each action and “Selesai” or “Keluar demo” to end. Escape also exits the guide when the evidence dialog is closed.

## Safe fallback

- **Public release not verified:** state that it is a local prototype; do not claim the submitted URL has the new version. Run `.venv/bin/gunicorn --bind 127.0.0.1:5067 app:app` and open `http://127.0.0.1:5067/` on the presenter's own machine only if the repository and dependencies are already there. It cannot be opened on a different laptop via that localhost address.
- **Render still starting:** wait before beginning the timed demo. Keep the PPT visible. Do not repeatedly create services or change hostname.
- **No JavaScript:** context, six target categories and native expandable methods remain readable. Explain that interactivity is unavailable; do not describe a click as having produced data.
- **No analytics artifacts:** use the script above unchanged. Never call hypotheses ranked topics, never call 434,463 processed records, and never claim an age, confidence, F1, or policy effect.
- **Dialog stuck:** press Escape or the visible “Tutup ×” button. Tab remains within the native modal.

## Three likely jury questions

1. **“Bisakah usia penulis diketahui hanya dari teks?”**
   Tidak secara andal. Targetnya estimasi kategori, bukan identitas. Bahkan Macro-F1 pada label manusia akan mengukur kesesuaian anotasi, bukan kebenaran usia. Ketidakpastian dan potensi bias platform harus dinyatakan.
2. **“Mana hasil model dan skor Macro-F1?”**
   Belum ada artefak model, gold set, prediksi atau evaluasi dalam project yang dapat diverifikasi. PPT menyajikan rencana perbandingan model. Kami tidak menampilkan skor sebelum ada evaluasi terpisah dan bukti yang dapat diaudit.
3. **“Apa yang dibutuhkan agar perbandingan kelompok sah?”**
   Prediksi dengan ID unik, satu peta topik global yang sama, serta jumlah komentar per kelompok dan penugasan topiknya. Porsi memakai seluruh komentar berprediksi di kelompok, termasuk yang belum mendapat topik; selisih dalam poin persentase. Perlu audit cakupan, duplikasi, bias platform, dan ketidakpastian sebelum interpretasi kebijakan.
