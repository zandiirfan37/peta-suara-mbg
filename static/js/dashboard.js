'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const A = window.MBGAnalytics;
  const data = JSON.parse($('dashboard-data').textContent);
  const num = n => new Intl.NumberFormat('id-ID').format(n);
  const dec = n => n === null ? '—' : n.toLocaleString('id-ID',{minimumFractionDigits:1,maximumFractionDigits:1});
  const pct = n => n === null ? '—' : `${dec(n)}%`;
  const esc = text => String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const groupName = id => id === 'all' ? 'Semua kelompok' : data.groups.find(g=>g.id===id).name;
  const state = {group:'all',topic:null,platform:'all',month:'all',a:'millennials',b:'gen-x',page:0,pageSize:3,query:''};
  let current;
  let previousFocus;
  function filterContext() {
    const p=state.platform==='all'?'Seluruh platform':state.platform;
    const m=state.month==='all'?'Juli–September 2026':data.months.find(m=>m.id===state.month).name;
    return `${p} · ${m}`;
  }
  function reset() {
    Object.assign(state,{group:'all',topic:null,platform:'all',month:'all',a:'millennials',b:'gen-x',page:0,pageSize:3,query:''});
    $('platform-filter').value='all';$('month-filter').value='all';$('evidence-search').value='';
    render();
  }
  function selectGroup(id,topic=null) {
    state.group=id;state.topic=topic;state.page=0;state.query='';$('evidence-search').value='';
    if(id!=='all')state.a=id;
    render();
  }
  function selectTopic(id) {state.topic=id;state.page=0;state.query='';$('evidence-search').value='';render();}
  function render() {
    current=A.summarize(data,state.platform,state.month,state.group);
    if(!state.topic)state.topic=current.topics[0]?.id;
    $('filter-context').textContent=filterContext();
    $('kpi-total').textContent=num(current.total);
    $('dataset-total').textContent=num(data.records.length);
    $('kpi-groups').textContent=num(current.groups.filter(g=>g.count>0).length);
    $('kpi-topics').textContent=num(data.topics.filter(t=>current.rows.some(r=>r.topic_id===t.id)).length);
    $('kpi-platforms').textContent=num(new Set(current.rows.map(r=>r.specific_resource_type)).size);
    $('snapshot-months').textContent=`${new Set(current.rows.map(r=>r.date_created.slice(0,7))).size} bulan cakupan`;
    $('selected-group').textContent=groupName(state.group);
    $('selected-total').textContent=num(current.selected.length);
    $('all-groups').setAttribute('aria-pressed',String(state.group==='all'));
    renderGroups();renderTopics();renderComparison();renderMatrix();renderEvidence();
    const topic=data.topics.find(t=>t.id===state.topic);
    $('policy-question').textContent=topic.question;
    $('policy-source').textContent=`Rencana verifikasi: ${topic.verify}. Contoh alur evaluasi; bukan temuan tentang MBG.`;
    $('loading-state').hidden=true;
  }
  function renderGroups() {
    const max=Math.max(...current.groups.map(g=>g.count),1);
    $('group-chart').innerHTML=current.groups.map(g=>`<button class="group-row ${state.group===g.id?'selected':''}" data-group="${g.id}" aria-pressed="${state.group===g.id}" aria-label="${esc(g.name)}, ${g.count} komentar sintetis, ${pct(g.share)} dari filter"><span class="group-line"><span>${esc(g.name)}</span><strong>${num(g.count)}</strong></span><span class="group-track"><span style="width:${g.count/max*100}%"></span></span><span class="group-percentage">${pct(g.share)}</span></button>`).join('');
    $('group-chart').querySelectorAll('[data-group]').forEach(b=>b.addEventListener('click',()=>selectGroup(b.dataset.group)));
  }
  function renderTopics() {
    const max=Math.max(...current.topics.map(t=>t.count),1);
    $('topic-chart').innerHTML=current.topics.map((t,i)=>`<button class="topic-row ${state.topic===t.id?'selected':''}" data-topic="${t.id}" aria-pressed="${state.topic===t.id}" aria-label="${esc(t.name)}: ${t.count} dari ${current.selected.length} komentar sintetis, ${pct(t.share)}"><span class="rank">${String(i+1).padStart(2,'0')}</span><span class="topic-bar-area"><span class="topic-label">${esc(t.name)}</span><span class="topic-track"><span style="width:${t.count/max*100}%"></span></span></span><span class="topic-value"><strong>${pct(t.share)}</strong><small>${num(t.count)} komentar</small></span></button>`).join('');
    $('topic-chart').querySelectorAll('[data-topic]').forEach(b=>b.addEventListener('click',()=>{selectTopic(b.dataset.topic);openQuickEvidence();}));
  }
  function renderComparison() {
    $('compare-a').value=state.a;$('compare-b').value=state.b;
    const c=A.compare(data,current.rows,state.a,state.b);
    const max=Math.max(...c.topics.map(t=>Math.abs(t.delta??0)),1);
    $('comparison-chart').innerHTML=c.topics.map((t,i)=>{
      const delta=t.delta??0;
      return `<button class="contrast-row ${i===0&&state.a!==state.b?'biggest':''}" data-contrast="${t.id}" aria-label="${esc(t.name)}, ${esc(groupName(state.a))} ${pct(t.shareA)}, ${esc(groupName(state.b))} ${pct(t.shareB)}, selisih ${dec(t.delta)} poin persentase" title="${esc(groupName(state.a))}: ${pct(t.shareA)} · ${esc(groupName(state.b))}: ${pct(t.shareB)}"><span>${esc(t.short)}</span><span class="diverging-track"><span class="zero-line"></span><span class="diverging-fill ${delta>=0?'positive':'negative'}" style="width:${Math.abs(delta)/max*48}%;${delta>=0?'left:50%':'right:50%'}"></span></span><strong>${t.delta===null?'—':`${delta>0?'+':''}${dec(t.delta)}`}</strong></button>`;
    }).join('');
    $('comparison-chart').querySelectorAll('[data-contrast]').forEach(b=>b.addEventListener('click',()=>selectGroup(state.a,b.dataset.contrast)));
    const top=c.topics[0];
    if(state.a===state.b)$('comparison-insight').innerHTML='<strong>Kelompok yang sama.</strong> Pilih dua kelompok berbeda untuk melihat kontras.';
    else if(!c.totalA||!c.totalB)$('comparison-insight').textContent='Komentar tidak tersedia untuk salah satu kelompok dalam filter ini. Perluas filter untuk menghitung selisih.';
    else $('comparison-insight').innerHTML=`<span>SELISIH TERBESAR · SIMULASI</span><strong>${esc(top.name)}</strong><p>${esc(groupName(state.a))} ${pct(top.shareA)} vs ${esc(groupName(state.b))} ${pct(top.shareB)} · <b>${top.delta>0?'+':''}${dec(top.delta)} pp</b></p>`;
  }
  function renderMatrix() {
    const max=Math.max(...current.matrix.flatMap(g=>g.topics.map(t=>t.share??0)),1);
    $('heatmap').innerHTML=`<div class="matrix-row matrix-header"><span>Kelompok / topik</span>${data.topics.map(t=>`<span title="${esc(t.name)}">${esc(t.short)}</span>`).join('')}</div>`+current.matrix.map(g=>`<div class="matrix-row"><span class="matrix-group">${esc(g.name)}<small>n = ${num(g.total)}</small></span>${data.topics.map(t=>{
      const cell=g.topics.find(x=>x.id===t.id),ratio=(cell.share??0)/max;
      const bg=[Math.round(240-228*ratio),Math.round(246-166*ratio),Math.round(240-170*ratio)];
      const selected=state.group===g.id&&state.topic===t.id;
      const lum=bg.map(v=>{v/=255;return v<=0.04045?v/12.92:((v+0.055)/1.055)**2.4;}).reduce((s,v,i)=>s+v*[0.2126,0.7152,0.0722][i],0);
      const textColor=lum>0.179?'#000':'#fff';
      return `<button class="heat-cell ${selected?'selected':''}" data-cell-group="${g.id}" data-cell-topic="${t.id}" aria-pressed="${selected}" aria-label="${esc(g.name)}, ${esc(t.name)}: ${cell.count} dari ${g.total}, ${pct(cell.share)} komentar sintetis" title="${esc(g.name)} · ${esc(t.name)}: ${cell.count}/${g.total} (${pct(cell.share)}) · sintetis" style="background:rgb(${bg.join(',')});color:${textColor}"><span class="mobile-cell-label">${esc(t.short)}</span><strong>${pct(cell.share)}</strong></button>`;
    }).join('')}</div>`).join('');
    // Every value is labeled; intensity uses the current matrix maximum.
    $('legend-max').textContent=pct(max);$('matrix-context').textContent=filterContext();
    $('heatmap').querySelectorAll('[data-cell-group]').forEach(b=>b.addEventListener('click',()=>selectGroup(b.dataset.cellGroup,b.dataset.cellTopic)));
  }
  function renderEvidence() {
    $('copy-status').textContent='Semua teks dibuat untuk demo. Tidak berasal dari akun nyata.';
    const topic=data.topics.find(t=>t.id===state.topic);
    const matching=A.evidence(current.selected,state.topic,state.query);
    const pages=Math.max(1,Math.ceil(matching.length/state.pageSize));
    state.page=Math.max(0,Math.min(state.page,pages-1));
    const start=state.page*state.pageSize,items=matching.slice(start,start+state.pageSize);
    $('evidence-topic').textContent=topic.name;
    $('evidence-context').textContent=`${groupName(state.group)} · ${filterContext()} · ${num(matching.length)} contoh cocok`;
    $('keywords').innerHTML=topic.keywords.map(k=>`<span>${esc(k)}</span>`).join('');
    $('evidence-list').innerHTML=items.length?items.map(r=>`<article class="comment" data-evidence-id="${r.id}"><div class="comment-meta"><span>${r.id}</span><button class="copy-id" data-copy="${r.id}" aria-label="Salin ID sintetis ${r.id}">Salin ID</button></div><p>${esc(r.content)}</p><div class="comment-source"><span>${esc(r.specific_resource_type)} · ${new Date(r.date_created+'T12:00:00').toLocaleDateString('id-ID',{day:'numeric',month:'short',year:'numeric'})}</span><span>${esc(r.taggenerasi)} · ${esc(r.topic_name)}</span></div><span class="comment-provenance">KOMENTAR SINTETIS</span></article>`).join(''):`<div class="empty-state"><strong>Tidak ada contoh pada pilihan ini.</strong><p>Coba topik lain atau perluas filter. ${state.query?'Hapus pencarian untuk melihat komentar pilihan.':''}</p><button id="broaden" class="button outline">${state.query?'Hapus pencarian':'Reset semua filter'}</button></div>`;
    $('evidence-page').textContent=matching.length?`${start+1}–${start+items.length} dari ${num(matching.length)}`:'0 komentar';
    $('evidence-prev').disabled=state.page===0;$('evidence-next').disabled=state.page>=pages-1;
    $('evidence-more').textContent=state.pageSize===3?'Lihat 5 contoh':'Lihat 3 contoh';
    $('evidence-list').querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>copyID(b.dataset.copy)));
    if($('broaden'))$('broaden').addEventListener('click',()=>{if(state.query){state.query='';$('evidence-search').value='';renderEvidence();}else reset();});
  }
  function openQuickEvidence() {
    const t=data.topics.find(t=>t.id===state.topic);
    $('quick-title').textContent=t.name;
    $('quick-context').textContent=`${groupName(state.group)} · ${filterContext()}`;
    $('quick-comments').innerHTML=$('evidence-list').innerHTML;
    $('quick-comments').querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>copyID(b.dataset.copy)));
    // The empty-state reset in the full explorer is replaced with a clear close action here.
    $('quick-comments').querySelector('#broaden')?.remove();
    $('quick-evidence').showModal();$('quick-close').focus();
  }
  $('quick-close').addEventListener('click',()=>$('quick-evidence').close());
  $('quick-evidence').addEventListener('close',()=>document.querySelector(`[data-topic="${state.topic}"]`)?.focus());
  $('quick-explore').addEventListener('click',()=>{$('quick-evidence').close();$('evidence-panel').scrollIntoView({block:'start',behavior:'instant'});});
  function copyFeedback(text){$('copy-status').textContent=text;$('quick-copy-status').textContent=text;}
  async function copyID(id) {
    try {
      await navigator.clipboard.writeText(id);copyFeedback(`ID sintetis ${id} disalin.`);
    } catch {
      const input=document.createElement('textarea');input.value=id;input.setAttribute('aria-label','ID sintetis untuk disalin');
      const output=$('quick-evidence').open?$('quick-copy-status'):$('copy-status');
      output.replaceChildren(input);input.focus();input.select();
      try {if(document.execCommand('copy')){copyFeedback(`ID sintetis ${id} disalin.`);return;}}catch{/* Manual selection fallback remains available. */}
      output.append(document.createTextNode('Pilih salin atau tekan Ctrl+C.'));
    }
  }
  $('platform-filter').addEventListener('change',e=>{state.platform=e.target.value;state.page=0;render();});
  $('month-filter').addEventListener('change',e=>{state.month=e.target.value;state.page=0;render();});
  $('reset').addEventListener('click',reset);
  $('all-groups').addEventListener('click',()=>selectGroup('all'));
  $('compare-a').addEventListener('change',e=>{state.a=e.target.value;selectGroup(state.a,state.topic);});
  $('compare-b').addEventListener('change',e=>{state.b=e.target.value;renderComparison();});
  $('compare-nonindividual').addEventListener('click',()=>{state.b='non-individual';renderComparison();});
  $('evidence-search').addEventListener('input',e=>{state.query=e.target.value;state.page=0;renderEvidence();});
  $('evidence-prev').addEventListener('click',()=>{state.page--;renderEvidence();});
  $('evidence-next').addEventListener('click',()=>{state.page++;renderEvidence();});
  $('evidence-more').addEventListener('click',()=>{state.pageSize=state.pageSize===3?5:3;state.page=0;renderEvidence();});
  $('export-csv').addEventListener('click',()=>{
    const quote=s=>'"'+String(s).replace(/"/g,'""')+'"';
    const rows=[['provenance','seed','platform_filter','month_filter','group','topic','count','group_total','share_percent']];
    for(const g of current.matrix)for(const t of g.topics)rows.push(['SYNTHETIC_NOT_RESEARCH',data.source.seed,state.platform,state.month,g.name,t.name,t.count,g.total,t.share===null?'':t.share.toFixed(6)]);
    const blob=new Blob(['\uFEFF'+rows.map(r=>r.map(quote).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'});
    const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='peta-suara-SIMULASI.csv';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  const dialog=$('methods-dialog');
  document.querySelectorAll('[data-open-methods]').forEach(b=>b.addEventListener('click',()=>{previousFocus=b;dialog.showModal();$('close-methods').focus();}));
  $('close-methods').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>previousFocus?.focus());
  dialog.addEventListener('click',e=>{const r=dialog.getBoundingClientRect();if(e.target===dialog&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))dialog.close();});
  const stages=[
    ['who-panel','Siapa yang bicara?','Klik Gen Z. Perhatikan distribusi dan peringkat topik yang berubah. Seluruh data adalah sintetis.'],
    ['topics-panel','Apa yang mereka bicarakan?','Klik satu topik. Di Balik Angka menampilkan contoh sintetis yang cocok. Gunakan tautan Buka bukti untuk melihatnya.'],
    ['compare-panel','Apa yang membedakan prioritas?','Klik Bandingkan dengan Non-individual. Selisih dihitung dari porsi pada dataset sintetis, bukan temuan lomba.']
  ];
  let stage=0;
  function showStage(){
    document.querySelectorAll('.demo-focus').forEach(el=>el.classList.remove('demo-focus'));
    const [id,title,copy]=stages[stage];$(id).classList.add('demo-focus');
    $('guide-count').textContent=`0${stage+1} / 03`;$('guide-title').textContent=title;$('guide-text').textContent=copy;
    $('guide-dots').innerHTML=stages.map((_,i)=>`<i class="${i===stage?'active':''}"></i>`).join('');
    $('guide-back').disabled=stage===0;$('guide-next').textContent=stage===2?'Selesai ✓':'Lanjut →';
  }
  function exitGuide(){ $('demo-guide').hidden=true;document.body.classList.remove('presenting');document.querySelectorAll('.demo-focus').forEach(el=>el.classList.remove('demo-focus'));$('start-demo').focus();}
  function startGuide(){reset();stage=0;$('demo-guide').hidden=false;document.body.classList.add('presenting');showStage();}
  $('start-demo').hidden=false;$('start-demo').addEventListener('click',startGuide);
  $('guide-back').addEventListener('click',()=>{if(stage>0){stage--;showStage();}});
  $('guide-next').addEventListener('click',()=>{if(stage<2){stage++;showStage();}else exitGuide();});
  $('guide-restart').addEventListener('click',startGuide);
  $('guide-exit').addEventListener('click',exitGuide);
  $('guide-target').addEventListener('click',()=>$(stages[stage][0]).scrollIntoView({block:'center',behavior:'instant'}));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!dialog.open&&!$('quick-evidence').open&&!$('demo-guide').hidden)exitGuide();});
  window.MBG={data,state,summary:()=>current,reset,selectGroup,selectTopic};
  try{render();}catch(err){$('loading-state').textContent='Grafik belum dapat dimuat. Muat ulang halaman atau periksa /api/dashboard.';throw err;}
})();
