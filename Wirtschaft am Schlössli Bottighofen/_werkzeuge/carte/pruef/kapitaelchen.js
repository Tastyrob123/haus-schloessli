const path=require('path'),fs=require('fs'),os=require('os'),cp=require('child_process');
const PW=require(path.join(process.env.HOME,'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER=path.join(process.env.HOME,'Desktop/Website-Projekte/Wirtschaft am Schlössli Bottighofen/_werkzeuge/carte');
const PORT=9033,B=`http://127.0.0.1:${PORT}`;
(async()=>{const TMP=fs.mkdtempSync(path.join(os.tmpdir(),'kap-'));
cp.execFileSync('python3',[path.join(HIER,'einlesen.py')],{env:{...process.env,CARTE_DATEN:TMP},stdio:'ignore'});
const srv=cp.spawn('python3',[path.join(HIER,'serve.py'),String(PORT)],{env:{...process.env,CARTE_DATEN:TMP},stdio:'ignore'});
await new Promise(r=>setTimeout(r,1500));
const br=await PW[process.argv[2]].launch();const out=[];
try{for(const [w,h] of [[1000,650],[1440,900]]){
const p=await br.newPage({viewport:{width:w,height:h}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{try{localStorage.setItem('lc-modus','frei')}catch(e){}});
await p.goto(B+'/_werkzeuge/carte/?z=bankett');await p.waitForTimeout(2500);
const f=p.frameLocator('#vf');
console.log(await f.locator('body').evaluate(()=>{const a=[...document.querySelectorAll('k-t')];return a.length+' '+a.filter(x=>/kap/.test(x.dataset.k)).length+' '+[...document.querySelectorAll('.kl')].slice(0,2).map(x=>x.parentElement.outerHTML.slice(0,200)).join(' /// ')}));const kt=f.locator('k-t[data-k$="~kap1"]').first();
out.push([w,'ganzer Name ein Text',await kt.textContent()]);
await kt.scrollIntoViewIfNeeded();await kt.click();await p.waitForTimeout(900);await kt.dblclick();await p.waitForTimeout(300);
await kt.press(process.platform==='darwin'?'Meta+A':'Control+A');await kt.pressSequentially('Ossobuco alla Milanese');
console.log('getippt',await f.locator('body').evaluate(()=>{const a=document.activeElement;return a.tagName+' '+a.isContentEditable+' '+a.textContent}));await f.locator('body').evaluate(()=>document.activeElement.blur());await p.waitForTimeout(1200);
console.log('nach blur',await f.locator('k-t[data-k$="~kap1"]').first().evaluate(e=>e.outerHTML.slice(0,200)));const neu=await f.locator('k-t[data-k$="~kap1"]',{hasText:/SSOBUCO/}).first();
out.push([w,'nach dem Schreiben',await neu.textContent(),await neu.innerHTML()]);
out.push([w,'Gestalten',await p.locator('.gst').first().textContent().then(t=>t.slice(0,40)).catch(()=>'-')]);
await p.click('#l-sp');await p.waitForTimeout(1500);const ov=await p.evaluate(()=>{const t=document.querySelector('#leiste .wo-leiste__t b'),r=t.getBoundingClientRect(),kn=[...document.querySelectorAll('#leiste .wo-kn')].map(k=>k.getBoundingClientRect());return {knoepfe:[...document.querySelectorAll('#leiste .wo-kn')].map(k=>k.textContent.trim()+(k.disabled?'(aus)':'')).join(','),titel:t.textContent,cls:document.querySelector('#leiste').className,ueber:kn.some(k=>k.left<r.right&&k.right>r.left),abgeschnitten:t.scrollWidth>t.parentElement.clientWidth+1}});
out.push([w,'Leiste',JSON.stringify(ov)]);await p.click('[data-m="einfach"]');await p.waitForTimeout(1200);const ov2=await p.evaluate(()=>{const t=document.querySelector('#leiste .wo-leiste__t b'),r=t.getBoundingClientRect(),kn=[...document.querySelectorAll('#leiste .wo-kn')].map(k=>k.getBoundingClientRect());return {knoepfe:[...document.querySelectorAll('#leiste .wo-kn')].map(k=>k.textContent.trim()+(k.disabled?'(aus)':'')).join(','),titel:t.textContent,cls:document.querySelector('#leiste').className,ueber:kn.some(k=>k.left<r.right&&k.right>r.left),abgeschnitten:t.scrollWidth>t.parentElement.clientWidth+1}});
out.push([w,'Leiste einfach',JSON.stringify(ov2)]);out.push([w,'Fehler',errs.join('|')]);
await p.screenshot({path:`${process.env.SP}/kap-${process.argv[2]}-${w}.png`});await p.close();}}
finally{await br.close();srv.kill();}
console.log(out.map(x=>x.join(' · ')).join('\n'))})();
