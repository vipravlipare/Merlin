// Test the quiz's actual JavaScript without copying its scoring implementation.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const html = readFileSync(new URL('../quizzes/sprint-0-quiz.html', import.meta.url), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 1, 'Expected the existing quiz script');
const source = scripts[0][1];
const boundary = source.indexOf('// UI');
assert.ok(boundary > 0, 'The pure quiz logic must precede the UI');
const context = vm.createContext({});
vm.runInContext(`${source.slice(0, boundary)}\nthis.quiz = { QUESTIONS, gradeAttempt, validSaved, optionOrder };`, context);
const quiz = context.quiz;
const ids = Array.from({ length: 35 }, (_, index) => index + 1);
const correctAnswer = id => quiz.QUESTIONS.find(q => q.id === id).correct;
const wrongAnswer = id => (correctAnswer(id) + 1) % 4;
const answers = () => Object.fromEntries(ids.map(id => [id, correctAnswer(id)]));
const plain = value => JSON.parse(JSON.stringify(value));
const saved = () => ({ ids: [1, 2], answers: { 1: 0 }, order: { 1: [0, 1, 2, 3], 2: [3, 2, 1, 0] } });

test('the complete browser script parses', () => {
  assert.doesNotThrow(() => new vm.Script(source));
});

test('the bank has 35 distinct questions and valid choice indexes', () => {
  assert.deepEqual(Array.from(quiz.QUESTIONS, q => q.id), ids);
  for (const question of quiz.QUESTIONS) {
    assert.equal(question.choices.length, 4);
    assert.equal(new Set(question.choices).size, 4);
    assert.ok(Number.isInteger(question.correct) && question.correct >= 0 && question.correct < 4);
    assert.ok(question.prompt && question.explanation && question.topic);
  }
  assert.deepEqual(Array.from(quiz.QUESTIONS.filter(q => q.critical), q => q.id), [15, 17, 21]);
});

test('all correct answers score 35/35 with no missing or critical errors', () => {
  const result = quiz.gradeAttempt(ids, answers());
  assert.equal(result.correct, 35);
  assert.equal(result.total, 35);
  assert.equal(result.percent, 100);
  assert.equal(result.pass, true);
  assert.deepEqual(plain([result.missing, result.missed, result.criticalMissed]), [[], [], []]);
  assert.deepEqual(plain(result.topics.Workspace), { correct: 2, total: 2 });
});

test('exactly 80 percent passes when critical answers are correct', () => {
  const input = answers();
  for (const id of [1, 2, 3, 4, 5, 6, 7]) input[id] = wrongAnswer(id);
  const result = quiz.gradeAttempt(ids, input);
  assert.equal(result.correct, 28);
  assert.equal(result.percent, 80);
  assert.equal(result.pass, true);
  assert.deepEqual(plain(result.missed), [1, 2, 3, 4, 5, 6, 7]);
});

test('one more noncritical error falls below the pass threshold', () => {
  const input = answers();
  for (const id of [1, 2, 3, 4, 5, 6, 7, 8]) input[id] = wrongAnswer(id);
  const result = quiz.gradeAttempt(ids, input);
  assert.equal(result.correct, 27);
  assert.equal(result.percent, 77);
  assert.equal(result.pass, false);
});

for (const id of [15, 17, 21]) {
  test(`critical question ${id} prevents passing even at 97 percent`, () => {
    const input = answers();
    input[id] = wrongAnswer(id);
    const result = quiz.gradeAttempt(ids, input);
    assert.equal(result.percent, 97);
    assert.equal(result.pass, false);
    assert.deepEqual(plain(result.criticalMissed), [id]);
  });
}

for (const [name, value] of [['absent', undefined], ['null', null], ['string', '0'], ['boolean', true],
  ['negative', -1], ['too large', 4], ['fraction', 1.5], ['NaN', NaN]]) {
  test(`${name} answer counts as missing, never as correct`, () => {
    const result = quiz.gradeAttempt([1], { 1: value });
    assert.deepEqual(plain(result.missing), [1]);
    assert.equal(result.correct, 0);
    assert.equal(result.pass, false);
  });
}

test('empty attempts cannot pass and unknown questions reject', () => {
  assert.equal(quiz.gradeAttempt([], {}).pass, false);
  assert.throws(() => quiz.gradeAttempt([999], {}), /Unknown question/);
});

test('retry scoring uses the selected questions rather than the full bank', () => {
  const input = { 1: correctAnswer(1), 2: correctAnswer(2) };
  const before = structuredClone(input);
  const result = quiz.gradeAttempt([1, 2], input);
  assert.equal(result.total, 2);
  assert.equal(result.correct, 2);
  assert.equal(result.percent, 100);
  assert.deepEqual(input, before);
});

test('valid partial saved answers restore and validation does not mutate them', () => {
  const input = saved();
  const before = structuredClone(input);
  assert.equal(quiz.validSaved(input), true);
  assert.deepEqual(input, before);
});

test('submitted saved attempts require an answer to every selected question', () => {
  const input = saved();
  input.submitted = true;
  assert.equal(quiz.validSaved(input), false);
  input.answers[2] = 0;
  assert.equal(quiz.validSaved(input), true);
});

for (const [name, change] of [
  ['empty ids', input => { input.ids = []; }],
  ['duplicate ids', input => { input.ids = [1, 1]; }],
  ['unknown id', input => { input.ids = [999]; input.order[999] = [0, 1, 2, 3]; }],
  ['missing answers', input => { delete input.answers; }],
  ['invalid answer', input => { input.answers[1] = '0'; }],
  ['missing order', input => { delete input.order; }],
  ['short permutation', input => { input.order[1] = [0, 1, 2]; }],
  ['long permutation', input => { input.order[1] = [0, 1, 2, 3, 3]; }],
  ['duplicate choice', input => { input.order[1] = [0, 1, 2, 2]; }],
  ['out of range choice', input => { input.order[1] = [0, 1, 2, 4]; }],
  ['fractional choice', input => { input.order[1] = [0, 1, 2, 2.5]; }],
]) {
  test(`saved state rejects ${name}`, () => {
    const input = saved();
    change(input);
    assert.equal(quiz.validSaved(input), false);
  });
}

test('absent or unparsable saved-state shape cannot restore', () => {
  for (const value of [null, undefined, {}, 'invalid', []]) assert.equal(quiz.validSaved(value), false);
});

test('shuffling preserves choices and uses the injected random source', () => {
  let calls = 0;
  assert.deepEqual(Array.from(quiz.optionOrder(() => { calls++; return 0; })), [1, 2, 3, 0]);
  assert.equal(calls, 3);
  assert.deepEqual(Array.from(quiz.optionOrder(() => 0.999)), [0, 1, 2, 3]);
});

// Missing answers block passing even when the numerical score is high.
test('one missing answer blocks an otherwise correct attempt', () => {
  const input = answers();
  delete input[1];
  const result = quiz.gradeAttempt(ids, input);
  assert.equal(result.correct, 34);
  assert.equal(result.pass, false);
  assert.deepEqual(plain(result.missing), [1]);
});

// Every answer must contribute to the correct topic and critical-error lists.
test('all wrong answers populate every error and topic total', () => {
  const input = Object.fromEntries(ids.map(id => [id, wrongAnswer(id)]));
  const result = quiz.gradeAttempt(ids, input);
  assert.equal(result.correct, 0);
  assert.equal(result.percent, 0);
  assert.equal(result.pass, false);
  assert.deepEqual(plain(result.missed), ids);
  assert.deepEqual(plain(result.criticalMissed), [15, 17, 21]);
  assert.deepEqual(plain(result.missing), []);
  for (const topic of new Set(quiz.QUESTIONS.map(q => q.topic))) {
    assert.deepEqual(plain(result.topics[topic]), {
      correct: 0, total: quiz.QUESTIONS.filter(q => q.topic === topic).length,
    });
  }
});

// An answer array gains an unused null slot when the UI saves question 1.
// Restoring it would lose progress on the following reload, so reject it early.
test('saved state rejects an answer array that loses progress after saving', () => {
  const input = saved();
  input.answers = [];
  const afterAnswer = structuredClone(input);
  afterAnswer.answers[1] = 0;
  const persisted = JSON.parse(JSON.stringify(afterAnswer));
  assert.deepEqual(persisted.answers, [null, 0]);
  assert.equal(quiz.validSaved(persisted), false);
  assert.equal(quiz.validSaved(input), false);
});

test('wrong answers must not modify the caller answer map', () => {
  const input = Object.fromEntries(ids.map(id => [id, wrongAnswer(id)]));
  const before = structuredClone(input);
  quiz.gradeAttempt(ids, input);
  assert.deepEqual(input, before);
});

for (const [name, value] of [['dense', [0, 1]], ['sparse', Object.assign([], { 1: 0 })]]) {
  test(`saved state rejects ${name} answer arrays before any reload`, () => {
    const input = saved();
    input.answers = value;
    assert.equal(quiz.validSaved(input), false);
  });
}

test('ordinary object state restores across JavaScript execution contexts', () => {
  const fresh = vm.createContext({});
  vm.runInContext(`${source.slice(0, boundary)}\nthis.validate = validSaved;`, fresh);
  assert.equal(fresh.validate(JSON.parse(JSON.stringify(saved()))), true);
});
