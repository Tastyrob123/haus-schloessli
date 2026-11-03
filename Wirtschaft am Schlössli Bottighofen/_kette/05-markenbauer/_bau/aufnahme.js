// Prüfaufnahmen (nur _qa) und die Bilder für «Logo richtig und falsch». Unsichtbar, eine Browser-Instanz nach der anderen.
// Aufruf: node aufnahme.js chromium|webkit [rf]
const pw=require('playwright');const path=require('path');
const B='http://127.0.0.1:8978/haus/'+encodeURIComponent('Wirtschaft am Schlössli Bottighofen')+'/_kette/05-markenbauer/marke/';
const Q=path.join(__dirname,'..','_qa'),RF=path.join(__dirname,'..','marke','logo-richtig-falsch');
const art=process.argv[2]||'chromium',rf=process.argv[3]==='rf';
(async()=>{const b=await pw[art].launch();const fehler=[];const bericht=[];
 const neu=async(w,h,m)=>{const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:m||1});const p=await c.newPage();
   p.on('console',x=>{if(x.type()==='error')fehler.push(w+' '+x.text())});p.on('pageerror',e=>fehler.push(w+' '+String(e)));
   p.on('response',r=>{if(r.status()>=400)fehler.push(r.status()+' '+r.url())});p.on('requestfailed',r=>fehler.push('fehlgeschlagen '+r.url()));return p};
 const alle=async p=>{await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0);document.querySelectorAll('[data-a],.hz').forEach(e=>e.classList.add('da'))});await p.waitForTimeout(2200)};
 const pruef=async(p,n)=>{const r=await p.evaluate(()=>{const kaputt=[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src);
   const breit=document.documentElement.scrollWidth-innerWidth;const ueber=[...document.querySelectorAll('body *')].filter(e=>{const q=e.getBoundingClientRect();return q.width>0&&(q.right>innerWidth+1)&&getComputedStyle(e).position!=='fixed'&&!e.closest('.hz')}).slice(0,5).map(e=>e.tagName+'.'+e.className);
   const fonts=[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family);return {kaputt,breit,ueber,fonts:[...new Set(fonts)]}});bericht.push(n+' '+JSON.stringify(r))};
 const seiten=[['markenbuch.html','mb-a'],['probe.html','probe-a'],['logo-richtig-falsch/index.html','rf']];
 for(const [w,h,m] of [[1440,900,1],[390,844,2]]){const p=await neu(w,h,m);
   for(const [u,n] of seiten){await p.goto(B+u,{waitUntil:'networkidle'});await alle(p);await pruef(p,art+' '+w+' '+n);
     await p.screenshot({path:path.join(Q,art+'-'+w+'-'+n+'.jpg'),fullPage:true,quality:55});}
   await p.context().close();}
 if(rf){const p=await neu(1440,900,2);await p.goto(B+'logo-richtig-falsch/index.html',{waitUntil:'networkidle'});await alle(p);
   for(const id of await p.$$eval('.karte',ks=>ks.map(k=>k.id))){await (await p.$('#'+id+' .feld')).screenshot({path:path.join(RF,id+'.png')});}}
 console.log(bericht.join('\n'));console.log('fehler:',JSON.stringify(fehler));await b.close()})();
