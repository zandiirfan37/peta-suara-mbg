/* Pure calculations shared by charts and functional tests. No invented metrics. */
(function (root) {
  'use strict';
  const share = (n, total) => total ? n * 100 / total : null;
  function cohort(data, platform = 'all', month = 'all') {
    return data.records.filter(r => (platform === 'all' || r.specific_resource_type === platform) && (month === 'all' || r.date_created.startsWith(month)));
  }
  function groupRows(data, rows, id) {
    if (id === 'all') return rows;
    const g = data.groups.find(g => g.id === id);
    return g ? rows.filter(r => r.taggenerasi === g.name) : [];
  }
  function ranking(data, rows) {
    return data.topics.map(t => {
      const count = rows.filter(r => r.topic_id === t.id).length;
      return {...t, count, share: share(count, rows.length)};
    }).sort((a,b) => b.count - a.count || a.id.localeCompare(b.id));
  }
  function summarize(data, platform = 'all', month = 'all', group = 'all') {
    const rows = cohort(data, platform, month);
    const selected = groupRows(data, rows, group);
    return {rows, selected, total: rows.length,
      groups: data.groups.map(g => {
        const subset = groupRows(data, rows, g.id);
        return {...g, count: subset.length, share: share(subset.length, rows.length)};
      }),
      topics: ranking(data, selected),
      matrix: data.groups.map(g => ({...g, total: groupRows(data,rows,g.id).length, topics: ranking(data,groupRows(data,rows,g.id))}))};
  }
  function compare(data, rows, a, b) {
    const ar = groupRows(data,rows,a), br = groupRows(data,rows,b);
    return {totalA:ar.length,totalB:br.length, topics:data.topics.map(t => {
      const countA = ar.filter(r=>r.topic_id===t.id).length;
      const countB = br.filter(r=>r.topic_id===t.id).length;
      const shareA = share(countA,ar.length), shareB=share(countB,br.length);
      return {...t,countA,countB,shareA,shareB,delta:shareA===null||shareB===null?null:shareA-shareB};
    }).sort((x,y)=>Math.abs(y.delta??0)-Math.abs(x.delta??0)||x.id.localeCompare(y.id))};
  }
  function evidence(rows, topic, query = '') {
    const q=query.trim().toLocaleLowerCase('id');
    return rows.filter(r=>(!topic||r.topic_id===topic)&&(!q||`${r.id} ${r.content}`.toLocaleLowerCase('id').includes(q)));
  }
  const api={share,cohort,groupRows,ranking,summarize,compare,evidence};
  root.MBGAnalytics=api;
  if (typeof module !== 'undefined' && module.exports) module.exports=api;
})(typeof window !== 'undefined' ? window : globalThis);
