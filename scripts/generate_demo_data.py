"""Generate synthetic UI fixtures only. Never use as research or training labels."""
import json
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 190726
GROUPS = [
    ('boomers', 'Baby Boomers', '1946–1964', 100),
    ('gen-x', 'Gen X', '1965–1980', 152),
    ('millennials', 'Millennials', '1981–1996', 218),
    ('gen-z', 'Gen Z', '1997–2012', 286),
    ('alpha', 'Gen Alpha', '2013–2024', 130),
    ('non-individual', 'Non-individual', 'Media / institusi / organisasi', 194),
]
# Arbitrary scenario weights. Not inferred demographic tendencies.
WEIGHTS = [
    [24,14,10,12,8,12,14,6], [18,16,20,12,10,10,8,6],
    [14,18,12,10,22,10,6,8], [12,27,10,8,8,23,7,5],
    [10,21,10,13,6,22,14,4], [18,9,10,11,13,5,7,27],
]
TOPICS = [
    ('safety','Keamanan pangan','Keamanan',['kebersihan','dapur','suhu','penyimpanan','pemeriksaan'],
     ['Wadah makan perlu diperiksa sebelum dibagikan.', 'Kalau makanan datang masih hangat rasanya lebih tenang.', 'Kebersihan dapur jangan hanya diperiksa saat ada kunjungan.', 'Bagaimana cara sekolah mengecek makanan yang baru sampai?', 'Lebih baik ada catatan suhu untuk setiap pengiriman.', 'Jangan langsung sebar kabar yang belum jelas, cek sumbernya dulu.', 'Tempat cuci tangan dekat ruang makan juga perlu dipikirkan.', 'Bagus kalau petugas bisa menjelaskan prosedur penyimpanan.', 'Siapa yang bisa dihubungi jika kondisi makanannya diragukan?', 'Menurutku pemeriksaan rutin lebih penting daripada foto kegiatan.'],
     ['Perlu jalur pelaporan yang mudah dipakai.', 'Keselamatan tetap yang utama.', 'Semoga prosedurnya konsisten setiap hari.', 'Bisa dijelaskan alurnya secara terbuka?', 'Catat dulu masalahnya supaya bisa diperiksa.', 'Jangan menunggu keluhan menumpuk.'],
     'Apa yang perlu diperiksa pada proses keamanan pangan?', 'Catatan Dinkes, pemeriksaan dapur dan audit SOP SPPG'),
    ('menu','Mutu & variasi menu','Menu',['menu','sayur','rasa','porsi','variasi'],
     ['Menunya boleh sederhana, yang penting nggak sama terus.', 'Sayurnya kalau terlalu lembek jadi susah dinikmati.', 'Porsi nasi dan lauk sebaiknya disesuaikan, jangan asal penuh.', 'Ada pilihan menu untuk yang punya pantangan makanan?', 'Senang kalau lauk lokal ikut masuk daftar menu.', 'Bisa nggak jadwal menu seminggu dibagikan lebih awal?', 'Rasa yang pas bikin makanan tidak banyak tersisa.', 'Sesekali buahnya diganti biar ada variasi.', 'Kalau sambalnya dipisah mungkin lebih nyaman buat semua.', 'Menu enak belum tentu harus mahal, pengolahannya juga penting.'],
     ['Coba minta masukan setelah makan.', 'Biar tidak banyak yang terbuang.', 'Ini bisa jadi bahan evaluasi menu.', 'Tetap perhatikan gizinya juga ya.', 'Pengen tahu pendapat yang lain.', 'Masukan kecil seperti ini semoga didengar.'],
     'Apakah variasi, rasa, atau kecukupan porsi perlu dievaluasi?', 'Umpan balik sekolah dan penilaian ahli gizi'),
    ('delivery','Distribusi & ketepatan waktu','Distribusi',['antar','jadwal','terlambat','rute','pengiriman'],
     ['Jadwal antar sebaiknya mengikuti waktu istirahat sekolah.', 'Kalau datang terlambat, jam makan ikut bergeser.', 'Rute pengiriman perlu dihitung biar makanan tidak terlalu lama di jalan.', 'Ada pengumuman lebih awal kalau pengiriman berubah?', 'Petugas antar juga perlu waktu yang cukup untuk bongkar wadah.', 'Pembagian per kelas terasa lebih tertib daripada antre bersamaan.', 'Semoga sekolah yang jauh tetap dapat jadwal yang masuk akal.', 'Hari hujan pasti ada kendala, rencana cadangannya apa?', 'Mungkin bisa ada konfirmasi ketika makanan sudah diterima.', 'Jangan sampai jadwal belajar terganggu karena menunggu pembagian.'],
     ['Koordinasi di lapangan penting sekali.', 'Perlu dicatat waktu datangnya.', 'Kabar perubahan jadwal jangan mendadak.', 'Bisa dibuat alur yang lebih sederhana.', 'Petugas dan sekolah perlu saling konfirmasi.', 'Coba evaluasi rutenya secara berkala.'],
     'Bagian mana dari alur pengiriman yang perlu diverifikasi?', 'Log pengiriman dan konfirmasi penerimaan sekolah'),
    ('access','Pemerataan akses','Akses',['akses','sekolah','wilayah','cakupan','pemerataan'],
     ['Sekolah yang letaknya jauh juga perlu diperhatikan.', 'Bagaimana menentukan urutan sekolah yang menerima layanan?', 'Informasi cakupan program sebaiknya mudah dicari.', 'Kalau belum mendapat layanan, saluran pertanyaannya ke mana?', 'Jangan sampai perbedaan fasilitas bikin aksesnya timpang.', 'Perlu penjelasan soal tahapan perluasan ke wilayah lain.', 'Sekolah kecil jangan terlewat dalam pendataan.', 'Semoga jalur distribusi untuk daerah sulit ikut direncanakan.', 'Daftar cakupan bisa diperbarui secara berkala nggak?', 'Kondisi tiap wilayah beda, pelaksanaannya perlu menyesuaikan.'],
     ['Penjelasan terbuka akan membantu.', 'Biar tidak cuma saling menebak.', 'Masukan dari sekolah perlu didengar.', 'Tolong sediakan jalur informasi yang jelas.', 'Ini perlu dilihat bersama data cakupan.', 'Semoga prosesnya bisa dipantau.'],
     'Apakah cakupan layanan sesuai kebutuhan wilayah?', 'Data cakupan sekolah dan rencana layanan Pemda'),
    ('budget','Anggaran & transparansi','Anggaran',['anggaran','biaya','pengadaan','laporan','transparansi'],
     ['Rincian penggunaan anggaran perlu disajikan dengan bahasa sederhana.', 'Biaya per porsi itu mencakup pengiriman juga atau belum?', 'Laporan pengadaan jangan hanya jadi dokumen yang sulit dibuka.', 'Kalau ada perubahan biaya, alasannya perlu dijelaskan.', 'Kualitas bahan dan harga harus bisa ditelusuri.', 'Pengen lihat laporan berkala, bukan cuma angka total.', 'Bisa dibuat ringkasan penggunaan dana untuk masyarakat?', 'Pengawasan sebaiknya berjalan sejak pengadaan bahan.', 'Transparan itu juga berarti mudah dipahami orang awam.', 'Usaha lokal yang ikut memasok perlu proses seleksi yang jelas.'],
     ['Keterbukaan bikin diskusi lebih terarah.', 'Jangan menarik kesimpulan sebelum lihat dokumennya.', 'Perlu ada sumber yang bisa dicek.', 'Kalau ringkas lebih mudah dibaca.', 'Biar pertanyaannya dijawab dengan data.', 'Semoga laporannya rutin diperbarui.'],
     'Dokumen apa yang diperlukan untuk memeriksa biaya dan pengadaan?', 'Laporan anggaran, dokumen pengadaan dan pemeriksaan terkait'),
    ('experience','Pengalaman penerima','Pengalaman',['makan','bekal','suka','pengalaman','sisa'],
     ['Senang ada waktu makan bersama di sekolah.', 'Ada yang lebih suka bawa bekal sendiri, mungkin bisa didengar alasannya.', 'Hari ini makanannya habis, semoga besok tetap cocok.', 'Lebih enak kalau pembagiannya tidak buru-buru.', 'Pengalaman tiap sekolah sepertinya bisa beda-beda.', 'Boleh ada kotak saran setelah makan?', 'Rasanya menyenangkan kalau pendapat penerima ikut ditanya.', 'Kadang makanan tersisa bukan karena tidak suka, waktunya terlalu singkat.', 'Peralatan makan yang nyaman juga ngaruh ke pengalaman.', 'Terima kasih untuk yang menyiapkan, semoga masukan tetap diterima.'],
     ['Cerita langsung perlu ditampung.', 'Ini cuma satu pengalaman, belum tentu sama di tempat lain.', 'Ada yang punya pengalaman berbeda?', 'Mungkin bisa ditanya rutin ke penerimanya.', 'Yang penting ada ruang menyampaikan masukan.', 'Hal kecil begini kadang luput diperhatikan.'],
     'Bagaimana pengalaman penerima dikumpulkan tanpa bias?', 'Survei penerima dan umpan balik sekolah'),
    ('nutrition','Edukasi gizi','Gizi',['gizi','protein','sayur','edukasi','seimbang'],
     ['Penjelasan soal isi piring bisa dibuat singkat dan mudah dipahami.', 'Akan seru kalau makan diselingi pengetahuan tentang gizi.', 'Kenapa porsi sayur dan protein dibedakan? Pengen paham alasannya.', 'Sumber protein lokal juga banyak pilihannya.', 'Jangan cuma disuruh menghabiskan, jelaskan juga manfaat makanannya.', 'Materi gizi untuk keluarga mungkin bisa dibagikan lewat sekolah.', 'Minum air putih juga perlu diingatkan.', 'Pola makan seimbang tidak berhenti di jam sekolah saja.', 'Contoh menu sehari-hari lebih gampang dipahami daripada istilah rumit.', 'Boleh ada kegiatan mengenal bahan pangan lokal?'],
     ['Bahasanya jangan terlalu teknis.', 'Belajar dari contoh lebih gampang.', 'Semoga bisa dibahas bersama keluarga.', 'Materi pendek mungkin lebih efektif.', 'Bisa dimulai dari kebiasaan sederhana.', 'Penjelasan yang ramah akan membantu.'],
     'Materi edukasi gizi apa yang perlu diuji pada penerima?', 'Penilaian ahli gizi dan uji pemahaman materi'),
    ('coordination','Informasi & koordinasi','Informasi',['informasi','jadwal','koordinasi','pengumuman','kontak'],
     ['Pengumuman perubahan jadwal sebaiknya lewat satu saluran resmi.', 'Nomor kontak layanan perlu mudah ditemukan.', 'Informasi dari sekolah dan pengelola jangan sampai berbeda.', 'Bisa ada daftar pertanyaan yang sering ditanyakan?', 'Kalau ada kabar beredar, klarifikasinya harus gampang dicari.', 'Rapat koordinasi bagus, tapi hasilnya perlu sampai ke penerima.', 'Tolong bedakan informasi resmi dan pendapat pribadi.', 'Petunjuk pengaduan jangan berputar-putar.', 'Semoga ada pembaruan informasi yang terjadwal.', 'Satu halaman ringkasan layanan akan sangat membantu.'],
     ['Sumbernya perlu dicantumkan.', 'Biar tidak simpang siur.', 'Informasi yang jelas mengurangi kebingungan.', 'Jangan hanya mengandalkan pesan berantai.', 'Alurnya harus bisa diikuti semua pihak.', 'Perbarui kalau ada perubahan ya.'],
     'Apakah informasi dan jalur pengaduan dapat diakses dengan jelas?', 'Kanal resmi pengelola dan catatan respons layanan'),
]
PLATFORMS = ['Twitter/X', 'Instagram', 'YouTube']


def generate():
    rng = random.Random(SEED)
    groups = [dict(id=g, name=n, years=y) for g,n,y,_ in GROUPS]
    topics = [dict(id=t[0], name=t[1], short=t[2], keywords=t[3], question=t[6], verify=t[7]) for t in TOPICS]
    # Text pool is shared by all groups: labels do not encode age stereotypes.
    used = set()
    records = []
    for gi, (gid, name, _, count) in enumerate(GROUPS):
        for _ in range(count):
            ti = rng.choices(range(8), weights=WEIGHTS[gi])[0]
            topic = TOPICS[ti]
            platform = rng.choices(PLATFORMS, weights=[38,34,28])[0]
            while True:
                text = rng.choice(topic[4])
                if rng.random() < .85:
                    text += ' ' + rng.choice(topic[5])
                prefix = rng.choice(['', '', '', 'Menurutku, ', 'Kalau boleh usul, ', 'Satu catatan: ', 'Btw, ', 'Mau tanya, ', 'Setuju dibahas. '])
                if prefix:
                    text = prefix + text[0].lower() + text[1:]
                if platform == 'Twitter/X' and rng.random() < .24:
                    text = text.replace('tidak','nggak').replace('sebaiknya','baiknya')
                if platform == 'Instagram' and rng.random() < .18:
                    text += ' Terima kasih sudah membuka ruang diskusi.'
                if platform == 'YouTube' and rng.random() < .25:
                    text += ' Kalau dibahas lebih detail di video berikutnya mungkin membantu.'
                if text not in used:
                    used.add(text)
                    break
            day = date(2026,7,1) + timedelta(days=rng.randrange(92))
            records.append(dict(id=f'SIM-{len(records)+1:06d}', content=text,
                date_created=day.isoformat(), specific_resource_type=platform,
                taggenerasi=name, topic_id=topic[0], topic_name=topic[1]))
    rng.shuffle(records)
    return dict(schema_version=1, source=dict(kind='synthetic', label='MODE SIMULASI — DATA SINTETIS',
        disclosure='Data pada tampilan ini dibuat untuk mendemonstrasikan fitur sistem. Bukan hasil analisis resmi dataset lomba.',
        seed=SEED, generated_by='scripts/generate_demo_data.py', validated_real=False),
        competition_brief=dict(comment_count=434463, period='Juli–September 2026'),
        groups=groups, topics=topics, platforms=PLATFORMS,
        months=[dict(id='2026-07',name='Juli 2026'),dict(id='2026-08',name='Agustus 2026'),dict(id='2026-09',name='September 2026')],
        records=records)


if __name__ == '__main__':
    target = Path(__file__).resolve().parents[1] / 'static/data/demo.json'
    data = generate()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(',',':'))+'\n', encoding='utf-8')
    print(f'{len(data["records"])} synthetic records; seed={SEED}; {target.stat().st_size:,} bytes')
