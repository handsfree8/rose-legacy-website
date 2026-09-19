const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
function setup({reduced=false,saveData=false,blocked=false}={}) {
 const events=()=>({listeners:{},addEventListener(name,fn){this.listeners[name]=fn;},fire(name,arg){return this.listeners[name]?.(arg);}});
 const video=Object.assign(events(),{paused:true,currentTime:0,duration:7.1,plays:0,src:'',muted:false,
  classList:{add(){},remove(){}},getAttribute(name){return name==='src'?this.src:null;},
  play(){this.plays++;if(blocked)return Promise.reject(Error('NotAllowedError'));this.paused=false;this.fire('playing');return Promise.resolve();},
  pause(){this.paused=true;this.fire('pause');},load(){this.onloadedmetadata?.();}});
 const icon={textContent:''};
 const control=Object.assign(events(),{hidden:true,attrs:{},contains(target){return target===this;},querySelector(){return icon;},setAttribute(k,v){this.attrs[k]=v;}});
 const motion=Object.assign(events(),{matches:reduced}); const portrait=Object.assign(events(),{matches:false});
 const doc=Object.assign(events(),{hidden:false,readyState:'interactive',querySelectorAll(){return [];},getElementById(id){return {'background-video':video,'video-control':control}[id]||null;}});
 const win=events();
 vm.runInNewContext(fs.readFileSync('assets/site.js','utf8'),{document:doc,window:win,navigator:{connection:{saveData}},matchMedia:q=>q.includes('reduced-motion')?motion:portrait});
 return {video,control,doc,win,motion,portrait,unblock(){blocked=false;}};
}
test('starts muted without waiting for all page resources',()=>{const s=setup();assert.equal(s.video.plays,1);assert.equal(s.video.muted,true);assert.equal(s.video.paused,false);assert.equal(s.control.attrs['aria-label'],'Pause background video');});
for(const prefs of [{reduced:true},{saveData:true}])test(`no initial download for ${JSON.stringify(prefs)}`,()=>{const s=setup(prefs);assert.equal(s.video.src,'');assert.equal(s.video.plays,0);s.control.fire('click');assert.equal(s.video.plays,1);});
test('user pause survives resize, visibility and interaction',()=>{const s=setup();s.control.fire('click');const before=s.video.plays;s.portrait.matches=true;s.portrait.fire('change');s.doc.fire('visibilitychange');s.doc.fire('pointerdown');assert.equal(s.video.paused,true);assert.equal(s.video.plays,before);assert.equal(s.video.autoplay,false);});
test('blocked autoplay can retry on first interaction',async()=>{const s=setup({blocked:true});await Promise.resolve();assert.equal(s.control.hidden,false);s.unblock();s.doc.fire('pointerdown');assert.equal(s.video.paused,false);});
test('failed video keeps poster and hides its control',()=>{const s=setup();s.video.fire('error');assert.equal(s.control.hidden,true);s.doc.fire('pointerdown');assert.equal(s.control.hidden,true);});
test('first click on fallback Play is not toggled twice by the gesture retry',async()=>{const s=setup({blocked:true});await Promise.resolve();s.unblock();s.doc.fire('pointerdown',{target:s.control});s.control.fire('click');assert.equal(s.video.paused,false);});
