// Dashboard Modern JS - Chart setup and interactions
document.addEventListener('DOMContentLoaded', function(){
  // Readiness ring (doughnut)
  const readinessCtx = document.getElementById('readinessRing').getContext('2d');
  const readinessVal = 60; // sample
  new Chart(readinessCtx, {
    type: 'doughnut',
    data: {datasets:[{data:[readinessVal,100-readinessVal],backgroundColor:['#22c55e','#0b1220'],borderWidth:0}]},
    options:{cutout:'72%',responsive:false,plugins:{legend:{display:false},tooltip:{enabled:false}}}
  });

  // Trend chart (line)
  const trendCtx = document.getElementById('trendChart').getContext('2d');
  const labels = ['V1','V2','V3','V4','V5'];
  const data = [55,70,65,78,88];
  new Chart(trendCtx,{
    type:'line',
    data:{labels:labels,datasets:[{label:'ATS',data:data,fill:true,tension:0.35,borderColor:'#16a34a',backgroundColor:'rgba(34,197,94,0.08)',pointBackgroundColor:'#22c55e',pointRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:'#99aabb'}},y:{grid:{color:'rgba(255,255,255,0.02)'},ticks:{color:'#99aabb'}}}}
  });

  // Button handlers
  const uploadBtn = document.getElementById('uploadAnalyze');
  if(uploadBtn){uploadBtn.addEventListener('click',()=>{alert('Upload & Analyze action — integrate with backend to complete.');});}

  // small polishing: clickable skill analyze
  document.querySelectorAll('.btn').forEach((b)=>{b.addEventListener('mouseover',()=>b.style.transform='scale(1.02)');b.addEventListener('mouseout',()=>b.style.transform='scale(1)')});
});
