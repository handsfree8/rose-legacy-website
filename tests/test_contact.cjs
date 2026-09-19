const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function setup(fetch) {
  const listeners = {};
  const button = {disabled:false, textContent:'Send service request', focus(){this.focused=true;}};
  const input = {disabled:false};
  const notice = {hidden:true, dataset:{}, focus(){this.focused=true;}};
  const title = {textContent:''}, message = {textContent:''};
  const close = {addEventListener(type, fn){this.click=fn;}};
  const form = {
    resetCount:0, valid:true,
    addEventListener(type, fn){listeners[type]=fn;},
    reportValidity(){return this.valid;},
    querySelector(){return button;},
    querySelectorAll(){return [input, button];},
    setAttribute(){}, removeAttribute(){}, reset(){this.resetCount++;}
  };
  const elements = {'request-submit-label':{textContent:'Send service request'},'service-request':form,'request-notice':notice,'request-notice-title':title,'request-notice-message':message,'request-notice-close':close};
  const payload = [['name','Test Person'],['phone','8165550100'],['service','HVAC repair'],['area','Overland Park'],['_honey',''],['_next','https://roselegacyhs.com/thank-you.html']];
  vm.runInNewContext(fs.readFileSync('assets/contact.js','utf8'), {
    document:{getElementById:id=>elements[id]},
    FormData:class {entries(){return payload[Symbol.iterator]();}},
    fetch, AbortController, setTimeout, clearTimeout
  });
  return {form,button,input,notice,title,message,close,submit:()=>listeners.submit({preventDefault(){}})};
}
for (const accepted of [true,'true']) test(`accepted ${typeof accepted} shows confirmation and clears the form`,async()=>{
  let request;
  const ui=setup(async(url,options)=>{request={url,options};return {ok:true,json:async()=>({success:accepted})};});
  await ui.submit();
  assert.equal(request.url,'https://formsubmit.co/ajax/roselegacyhs@icloud.com');
  assert.equal(request.options.method,'POST');
  const body=JSON.parse(request.options.body);
  assert.equal(body.phone,'8165550100');
  assert.equal(body._honey,'');
  assert.equal(body._next,undefined);
  assert.equal(body._captcha,undefined);
  assert.equal(ui.notice.hidden,false);
  assert.equal(ui.notice.dataset.state,'success');
  assert.equal(ui.form.resetCount,1);
  assert.equal(ui.button.disabled,false);
  ui.close.click(); assert.equal(ui.notice.hidden,true);
});
for (const [name, fetch] of [
  ['provider rejection',async()=>({ok:true,json:async()=>({success:false})})],
  ['string rejection',async()=>({ok:true,json:async()=>({success:'false'})})],
  ['HTTP failure',async()=>({ok:false,json:async()=>({success:true})})],
  ['invalid JSON',async()=>({ok:true,json:async()=>{throw Error('invalid JSON');}})],
  ['network failure',async()=>{throw Error('offline');}],
  ['timeout',async()=>{throw new DOMException('timeout','AbortError');}]
]) test(`${name} preserves entered data and allows another attempt`,async()=>{
  const ui=setup(fetch); await ui.submit();
  assert.equal(ui.form.resetCount,0); assert.equal(ui.notice.dataset.state,'error');
  assert.equal(ui.button.disabled,false); assert.equal(ui.input.disabled,false);
});
test('pending submission blocks duplicates and edits',async()=>{
  let finish, calls=0;
  const ui=setup(()=>{calls++;return new Promise(resolve=>{finish=resolve;});});
  const first=ui.submit(); await ui.submit();
  assert.equal(calls,1);assert.equal(ui.button.disabled,true);assert.equal(ui.input.disabled,true);
  finish({ok:true,json:async()=>({success:true})});await first;
  assert.equal(ui.input.disabled,false);
});
test('invalid fields do not trigger a request',async()=>{
  let calls=0;const ui=setup(async()=>{calls++;});ui.form.valid=false;await ui.submit();assert.equal(calls,0);
});
