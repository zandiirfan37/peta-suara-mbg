'use strict';
(() => {
  const data = JSON.parse(document.getElementById('dashboard-data').textContent);
  const $ = id => document.getElementById(id);
  const group = id => data.groups.find(g => g.id === id);
  let selected = null;
  let lastTrigger = null;
  function updateComparison() {
    const a = group($('compare-a').value), b = group($('compare-b').value);
    if (!a || !b) {
      $('comparison-title').textContent = `${a?.name || 'Kelompok A'} ↔ ${b?.name || 'pilih pembanding'}`;
      $('comparison-copy').textContent = 'Pilih dua kelompok untuk melihat kesiapan perbandingan. Perhitungan menunggu prediksi dan penugasan topik terverifikasi.';
      return;
    }
    $('comparison-title').textContent = `${a.name} ↔ ${b.name}`;
    $('comparison-copy').textContent = a.id === b.id
      ? 'Pilih dua kelompok berbeda. Hasil perbandingan tetap menunggu prediksi dan penugasan topik terverifikasi.'
      : 'Prediksi dan penugasan topik belum tersedia untuk kedua kelompok. Belum ada selisih prioritas yang dapat disimpulkan.';
  }
  document.querySelectorAll('[data-group]').forEach(button => button.addEventListener('click', () => {
    selected = button.dataset.group;
    document.querySelectorAll('[data-group]').forEach(b => {
      const active = b.dataset.group === selected;
      b.classList.toggle('selected', active); b.setAttribute('aria-pressed', String(active));
    });
    $('selected-group').textContent = group(selected).name;
    $('topic-state').textContent = `Peringkat topik ${group(selected).name} belum tersedia.`;
    $('compare-a').value = selected; updateComparison();
  }));
  document.querySelectorAll('[data-question]').forEach(button => button.addEventListener('click', () => {
    const q = data.questions.find(q => q.id === button.dataset.question);
    lastTrigger = button;
    $('evidence-title').textContent = q.title;
    $('evidence-group').textContent = `Konteks pilihan: ${group(selected)?.name || 'belum dipilih'} · belum ada atribusi kelompok`;
    for (const [field, value] of Object.entries({question:q.question,source:q.source,verify:q.verify,action:q.action})) {
      $(`evidence-${field}`).textContent = value;
    }
    $('evidence').showModal(); $('close-evidence').focus();
  }));
  $('close-evidence').addEventListener('click', () => $('evidence').close());
  $('evidence').addEventListener('close', () => lastTrigger?.focus());
  $('evidence').addEventListener('click', e => {
    const r = $('evidence').getBoundingClientRect();
    if (e.target === $('evidence') && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)) $('evidence').close();
  });
  $('compare-a').addEventListener('change', updateComparison);
  $('compare-b').addEventListener('change', updateComparison);
  $('audit-open').addEventListener('click', () => {
    $('methods').open = true; $('methods').scrollIntoView({block:'start'}); $('methods').querySelector('summary').focus();
  });
  const steps = [
    ['who', '01 / WHO · 10–22 detik', 'Klik Gen Z. Enam kelompok adalah target model; jumlahnya belum tersedia.'],
    ['what', '02 / WHAT · 22–36 detik', 'Klik Keamanan pangan. Panel membedakan hipotesis PPT dari bukti yang belum tersedia.'],
    ['compare', '03 / CONTRAST · 36–49 detik', 'Bandingkan Gen Z dan Non-individual. Selisih tidak dihitung tanpa data pendukung.'],
    ['methods', '04 / SO WHAT · 49–60 detik', 'Tunjukkan kesiapan bukti. Percakapan menjadi pertanyaan verifikasi, bukan kesimpulan kebijakan.']
  ];
  let step = 0;
  function showStep() {
    document.querySelectorAll('.demo-focus').forEach(el => el.classList.remove('demo-focus'));
    const [target, title, copy] = steps[step];
    $('guide-step').textContent = title; $('guide-copy').textContent = copy;
    if (target === 'methods') $('methods').open = true;
    $(target).classList.add('demo-focus');
    $(target).scrollIntoView({block:'nearest'});
    $('guide-next').textContent = step === steps.length - 1 ? 'Selesai ✓' : 'Lanjut →';
  }
  function exitDemo() {
    $('guide').hidden = true;
    document.querySelectorAll('.demo-focus').forEach(el => el.classList.remove('demo-focus'));
    $('start-demo').focus();
  }
  $('start-demo').hidden = false;
  $('start-demo').addEventListener('click', () => { step = 0; $('guide').hidden = false; showStep(); });
  $('guide-next').addEventListener('click', () => { if (step === steps.length - 1) exitDemo(); else {step++;showStep();} });
  $('guide-exit').addEventListener('click', exitDemo);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('guide').hidden && !$('evidence').open) exitDemo(); });
})();
