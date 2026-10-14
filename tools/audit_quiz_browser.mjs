// Real Chromium behavior checks. All pages and faulty HTML copies stay in memory.
// Supply MERLIN_PLAYWRIGHT_MODULE pointing at an installed Playwright index.mjs.
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import vm from 'node:vm';
import { createHash } from 'node:crypto';

const { chromium } = await import(pathToFileURL(process.env.MERLIN_PLAYWRIGHT_MODULE).href);
const html = readFileSync(new URL('../quizzes/sprint-0-quiz.html', import.meta.url), 'utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const bankContext=vm.createContext({});
vm.runInContext(script.slice(0,script.indexOf('// UI'))+';globalThis.bank=QUESTIONS;',bankContext);
const bank=Array.from(bankContext.bank);
const correct=id=>bank.find(question=>question.id===id).correct;
const key = 'merlin-sprint0-quiz-v1';
const partial = () => ({ids:[1,2], answers:{1:0}, order:{1:[0,1,2,3],2:[3,2,1,0]}, submitted:false});
const full = (wrong=[]) => ({ids:bank.map(question=>question.id),
  answers:Object.fromEntries(bank.map(question=>[question.id,wrong.includes(question.id)?(question.correct+1)%question.choices.length:question.correct])),
  order:Object.fromEntries(bank.map(question=>[question.id,[0,1,2,3]])),submitted:false});
const answerAll = page => page.evaluate(answers => {
  for(const [id,index] of answers)document.querySelector(`#question-${id} input[value="${index}"]`)?.click();
},bank.map(question=>[question.id,question.correct]));
const submit = page => page.locator('#submit').click();
const count = page => page.locator('fieldset').count();
const state = page => page.evaluate(k=>JSON.parse(localStorage.getItem(k)), key);
const visibleResults = page => page.locator('#results').isVisible();
const cases = [
  {name:'fresh quiz renders 35 questions and 140 choices', old:'for(const [number,id] of ids.entries())', replacement:'for(const [number,id] of ids.slice(1).entries())',
   check:async p=>{assert.equal(await count(p),35);assert.equal(await p.locator('input[type=radio]').count(),140);assert.match(await p.locator('#progress-label').innerText(),/^0 \/ 35 answered/);}},
  {name:'missing answers block results and focus the first missing question', old:'if(lastGrade.missing.length){',replacement:'if(false){',
   check:async p=>{await submit(p);assert.equal(await visibleResults(p),false);assert.match(await p.locator('#notice').innerText(),/remaining 35/);assert.equal(await p.evaluate(()=>document.activeElement.name),'q1');assert.equal((await state(p)).submitted,false);}},
  {name:'radio change updates progress and saves the exact answer', old:'answers[id]=index;',replacement:'answers[id]=0;',
   check:async p=>{await p.locator('#question-1 input[value="2"]').check();assert.equal((await state(p)).answers[1],2);assert.match(await p.locator('#progress-label').innerText(),/^1 \/ 35/);}},
  {name:'partial progress and choice order survive reload', saved:partial(),old:'input.checked=answers[id]===index;',replacement:'input.checked=false;',
   check:async p=>{assert.equal(await count(p),2);assert.equal(await p.locator('#question-1 input[value="0"]').isChecked(),true);assert.deepEqual(await p.locator('#question-2 input').evaluateAll(ns=>ns.map(n=>Number(n.value))),[3,2,1,0]);await p.locator('#question-2 input[value="2"]').check();await p.reload();assert.equal(await p.locator('#question-2 input[value="2"]').isChecked(),true);assert.match(await p.locator('#progress-label').innerText(),/^2 \/ 2/);}},
  {name:'all correct answers show honest score and lock controls', saved:full(),old:'box.querySelectorAll(\'input\').forEach(n=>n.disabled=true);',replacement:'',
   check:async p=>{await submit(p);assert.equal(await visibleResults(p),true);assert.match(await p.locator('#score').innerText(),/^35 \/ 35 · 100%$/);assert.match(await p.locator('#result-message').innerText(),/does not certify full Sprint 0 completion/);assert.equal(await p.locator('input:disabled').count(),140);assert.equal(await p.locator('#submit').isDisabled(),true);assert.equal(await p.locator('#retry').isDisabled(),true);assert.equal(await p.locator('.feedback').count(),35);}},
  {name:'double submission never duplicates feedback', saved:full(),old:'if(!submitted)showResults();',replacement:'showResults();',
   check:async p=>{await submit(p);await p.locator('#quiz').evaluate(form=>form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true})));assert.equal(await p.locator('.feedback').count(),35);}},
  {name:'retry contains only mistakes and clears previous answers', saved:full([1,15]),old:'ids=[...lastGrade.missed];',replacement:'ids=QUESTIONS.map(q=>q.id);',
   check:async p=>{await submit(p);await p.locator('#retry').click();assert.equal(await count(p),2);assert.deepEqual((await state(p)).ids,[1,15]);assert.deepEqual((await state(p)).answers,{});assert.equal(await p.locator('input:checked').count(),0);assert.equal(await visibleResults(p),false);assert.equal(await p.locator('#submit').isDisabled(),false);assert.equal((await state(p)).submitted,false);}},
  {name:'retry score uses its own denominator and practice wording', saved:full([1,2]),old:"ids.length<QUESTIONS.length?'Practice threshold met':'Quiz threshold met'",replacement:"'Quiz threshold met'",
   check:async p=>{await submit(p);await p.locator('#retry').click();await answerAll(p);await submit(p);assert.match(await p.locator('#score').innerText(),/^2 \/ 2 · 100%$/);assert.match(await p.locator('#result-message').innerText(),/^Practice threshold met/);}},
  {name:'restart restores full bank and clears completed progress', saved:full(),old:"ids=QUESTIONS.map(q=>q.id);answers={};order={};submitted=false;lastGrade=null;",replacement:"ids=[1];answers={};order={};submitted=false;lastGrade=null;",
   check:async p=>{await submit(p);await p.locator('#restart').click();assert.equal(await count(p),35);assert.equal(await p.locator('input:checked').count(),0);assert.equal(await p.locator('input:disabled').count(),0);assert.equal(await visibleResults(p),false);assert.equal((await state(p)).submitted,false);}},
  {name:'completed attempts restore results after reload', saved:{...full(),submitted:true},old:'if(submitted)showResults(false);',replacement:'',
   check:async p=>{assert.equal(await visibleResults(p),true);assert.equal(await p.locator('input:disabled').count(),140);await p.reload();assert.equal(await visibleResults(p),true);assert.equal(await p.locator('.feedback').count(),35);}},
  {name:'incomplete submitted cache resets and remains usable', saved:{...partial(),submitted:true},old:'if(saved.submitted===true&&saved.ids.some(id=>!Object.hasOwn(saved.answers,id)))return false;',replacement:'',
   check:async p=>{assert.equal(await count(p),35);await answerAll(p);await submit(p);assert.equal(await visibleResults(p),true);assert.match(await p.locator('#score').innerText(),/100%/);}},
  {name:'malformed cache resets without script errors', raw:'{not-json',old:'}catch{}\nfunction save()',replacement:'}catch{throw new Error("cache failure");}\nfunction save()',
   check:async p=>{assert.equal(await count(p),35);await p.locator('#question-1 input[value="1"]').check();assert.equal((await state(p)).answers[1],1);}},
  {name:'array answer cache resets rather than silently losing progress', saved:{...partial(),answers:[0]},old:'Array.isArray(saved.answers)',replacement:'false',
   check:async p=>{assert.equal(await count(p),35);assert.equal(await p.locator('input:checked').count(),0);}},
  {name:'storage unavailable still allows completing a quiz', blocked:true,old:'}catch{}}\nfunction el',replacement:'}catch{throw new Error("storage failure");}}\nfunction el',
   check:async p=>{assert.equal(await count(p),35);await answerAll(p);await submit(p);assert.equal(await visibleResults(p),true);assert.match(await p.locator('#score').innerText(),/100%/);}},
  {name:'critical mistake shows warning despite a high score', saved:full([15]),old:"lastGrade.criticalMissed.length?' Review the missed critical secret/authentication/storage questions even if the percentage is high.':''",replacement:"''",
   check:async p=>{await submit(p);assert.match(await p.locator('#score').innerText(),/97%/);assert.match(await p.locator('#result-message').innerText(),/missed critical secret\/authentication\/storage/);}},
  {name:'print control invokes the browser print action once', saved:full(),old:"()=>window.print()",replacement:'()=>{}',
   check:async p=>{await submit(p);await p.evaluate(()=>{window.print=()=>{window.printCalls=(window.printCalls||0)+1;};});await p.locator('#print').click();assert.equal(await p.evaluate(()=>window.printCalls),1);}},
];

const browser = await chromium.launch({headless:true});
const rows=[];
async function execute(spec, source) {
  new vm.Script([...source.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1]);
  const context=await browser.newContext();const page=await context.newPage();
  page.setDefaultTimeout(3000);const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await context.route('**/*',route=>route.fulfill({status:200,contentType:'text/html',body:source}));
  await context.addInitScript(({key,saved,raw,blocked})=>{
    if(blocked){Storage.prototype.getItem=()=>{throw new Error('storage blocked');};Storage.prototype.setItem=()=>{throw new Error('storage blocked');};}
    else if(localStorage.getItem(key)===null&&(raw!==undefined||saved!==undefined))localStorage.setItem(key,raw??JSON.stringify(saved));
  },{key,saved:spec.saved,raw:spec.raw,blocked:spec.blocked});
  try{await page.goto('http://merlin.test/');await spec.check(page);assert.deepEqual(errors,[]);return {outcome:'passed'};}
  catch(error){return {outcome:'failed',failure:error.message,pageErrors:errors};}
  finally{await context.close();}
}
try{
  async function auditCase(spec){
    const baseline=await execute(spec,html);let mutation={status:'UNAPPLIED'};
    if(baseline.outcome==='passed'&&html.includes(spec.old)){
      const result=await execute(spec,html.replaceAll(spec.old,spec.replacement));
      mutation={fault:spec.old,replacement:spec.replacement,status:result.outcome==='failed'?'DETECTED':'SURVIVED',...result};
    }
    console.log(JSON.stringify({case:spec.name,baseline:baseline.outcome,fault:mutation.status}));
    return {case:spec.name,baseline,mutation};
  }
  // Each case owns a fresh browser context and storage. Bound concurrency to
  // two workflows; retain baseline-before-mutation within each workflow.
  for(let index=0;index<cases.length;index+=2){
    rows.push(...await Promise.all(cases.slice(index,index+2).map(auditCase)));
  }
}finally{await browser.close();}
const output=process.argv[2];if(!output)throw new Error('Output JSON path required');
const source_sha256=Object.fromEntries(['quizzes/sprint-0-quiz.html','tools/audit_quiz_browser.mjs'].map(file=>
  [file,createHash('sha256').update(readFileSync(new URL('../'+file,import.meta.url))).digest('hex')]));
writeFileSync(output,JSON.stringify({browser:'Chromium 145.0.7632.6',playwright:'1.58.2',source_sha256,cases:rows},null,2)+'\n');
if(rows.some(row=>row.baseline.outcome!=='passed'||row.mutation.status!=='DETECTED'))process.exitCode=1;
