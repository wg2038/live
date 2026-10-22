// tools/regression_test.js
// 审计回归测试：把本次逻辑审计中的关键缺陷固化为可重复执行的断言。
// 用法: node tools/regression_test.js

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const embeddedCode = fs.readFileSync(path.join(ROOT, 'data/embedded.js'), 'utf8');
const engineCode = fs.readFileSync(path.join(ROOT, 'js/engine.js'), 'utf8');
const uiCode = fs.readFileSync(path.join(ROOT, 'js/ui.js'), 'utf8');

let rngState = 1;
function setSeed(seed) {
  rngState = (seed >>> 0) || 1;
}

function nextRandom() {
  rngState = (Math.imul(1664525, rngState) + 1013904223) >>> 0;
  return rngState / 4294967296;
}

function createSandbox() {
  const sandbox = {
    window: {},
    console: Object.assign({}, console, { warn: () => {} }),
    Math,
    Set,
    Map,
    Array,
    Object,
    JSON,
    Date,
    Promise,
    setTimeout,
    clearTimeout,
    __rng: nextRandom
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext('Math.random = __rng;', sandbox);
  vm.runInContext(embeddedCode, sandbox);
  vm.runInContext(engineCode, sandbox);
  return sandbox;
}

const sandbox = createSandbox();

async function freshEngine(seed = 1) {
  setSeed(seed);
  const engine = new sandbox.SimulationEngine();
  await engine.init();
  return engine;
}

function makeCharacter(engine, overrides = {}) {
  engine.createCharacter({ paceMode: 'step', eraFilter: 'all' });
  Object.assign(engine.character, overrides);
  return engine.character;
}

// 隔离自然灾害、疾病死亡、随机事件与人生里程碑，便于单测某一条规则。
function stubHazards(engine) {
  engine.checkNaturalDisaster = () => null;
  engine.triggerMicroAccident = () => ({ isFatal: false });
  engine.calculateAnnualMortalityRate = () => 0;
  engine.findEligibleEvents = () => [];
  engine.checkLifeMilestone = () => null;
}

function firstCityOf(engine, provinceId) {
  return engine.cities.find(c => c.provinceId === provinceId) || engine.cities[0];
}

const tests = [];
function test(name, fn) {
  tests.push({ name, fn });
}

// ---------------------------------------------------------------------------
// P0-1 义务教育自动入学年龄上限
// ---------------------------------------------------------------------------
test('P0-1 46岁文盲农民不会被自动改成初中在读', async () => {
  const e = await freshEngine(11);
  makeCharacter(e, { birthYear: 1940, educationLevel: '未入学' });
  e.character.tags.delete('primary');
  e.character.tags.delete('junior_high');
  e.currentYear = 1986;
  e.currentAge = 46;
  stubHazards(e);
  e.advanceYear();
  assert.ok(!['小学在读', '初中在读'].includes(e.character.educationLevel),
    `46岁角色被改成 ${e.character.educationLevel}`);
});

test('P0-1 7岁儿童正常入学并记录“步入校门”里程碑', async () => {
  const e = await freshEngine(12);
  makeCharacter(e, { birthYear: 1990, educationLevel: '未入学' });
  e.character.tags.delete('primary');
  e.character.tags.delete('junior_high');
  e.currentYear = 1997;
  e.currentAge = 7;
  stubHazards(e);
  e.advanceYear();
  assert.strictEqual(e.character.educationLevel, '小学在读');
  assert.ok(e.character.milestones.some(m => m.title.includes('步入校门')),
    '缺少“步入校门”里程碑');
});

test('P0-1 12岁小学生正常升入初中并记录里程碑', async () => {
  const e = await freshEngine(13);
  makeCharacter(e, { birthYear: 1985, educationLevel: '小学在读' });
  e.character.tags.add('primary');
  e.character.tags.delete('junior_high');
  e.currentYear = 1997;
  e.currentAge = 12;
  stubHazards(e);
  e.advanceYear();
  assert.strictEqual(e.character.educationLevel, '初中在读');
  assert.ok(e.character.milestones.some(m => m.title.includes('升入初中')),
    '缺少“升入初中”里程碑');
});

// ---------------------------------------------------------------------------
// P0-2 传承模式崩溃
// ---------------------------------------------------------------------------
test('P0-2 传承角色具备 tags 与 causalityReview，能连续推进 20 年', async () => {
  const e = await freshEngine(21);
  const provinceId = e.provinces[0].id;
  const city = firstCityOf(e, provinceId);
  e.createCharacterFromParent({
    birthYear: 1978,
    provinceId,
    cityId: city.id,
    urbanRural: 'urban',
    sex: '男',
    ethnicity: '汉族',
    name: '测试父辈',
    childName: '测试子代'
  });
  assert.ok(e.character.tags instanceof sandbox.Set, '传承角色缺少 tags');
  assert.ok(Array.isArray(e.character.causalityReview), '传承角色缺少 causalityReview');
  stubHazards(e);
  for (let i = 0; i < 20 && !e.isGameOver; i++) e.advanceYear();
  assert.ok(e.currentYear >= 1998, `推进中断于 ${e.currentYear}`);
});

// ---------------------------------------------------------------------------
// P0-3 2026 年死亡不得判为在世
// ---------------------------------------------------------------------------
test('P0-3 2026 年死亡角色走死亡分支，不走在世固定百分位', async () => {
  const e = await freshEngine(31);
  makeCharacter(e, { educationLevel: '未入学' });
  e.character.tags.delete('higher_ed_degree');
  e.currentYear = 2026;
  e.currentAge = 50;
  e.deathInfo = { age: 50, year: 2026, cause: '测试死亡', isAliveIn2026: false };
  const comp = e.calculatePeerComparisons();
  assert.strictEqual(comp.education.percentile, 15,
    '2026 年死亡被当成在世，返回了在世固定百分位');
});

test('P0-3 UI 不再用 death.year >= 2026 判断在世', async () => {
  assert.ok(!uiCode.includes('death.year >= 2026'),
    'js/ui.js 仍存在 death.year >= 2026 的在世误判');
});

test('P0-3 引擎不再用 currentYear >= 2026 兜底判在世', async () => {
  assert.ok(!engineCode.includes('this.currentYear >= 2026'),
    'js/engine.js 仍存在 currentYear >= 2026 的在世误判');
});

// ---------------------------------------------------------------------------
// P0-4 高考结果接通学历/职业
// ---------------------------------------------------------------------------
test('P0-4 高考本科结果在毕业年结算为本科学历并标记 college_graduate', async () => {
  const e = await freshEngine(41);
  makeCharacter(e, { educationLevel: '普通高中' });
  e.character.tags.add('high_school_student');
  e.currentYear = 2020;
  e.currentAge = 18;
  e.statusFlags.clear();
  e.currentPendingDecision = {
    id: 'node_gaokao_jueze',
    title: '测试高考',
    choices: [{
      text: '本科',
      outcomes: [{ type: 'safe', weight: 100, status: 'college_degree', log: '本科录取' }]
    }]
  };
  e.resolveDecision('node_gaokao_jueze', 0);
  assert.ok(e.statusFlags.has('attended_gaokao'), '高考后未记录 attended_gaokao');
  assert.ok(e.character.collegeGraduationYear === 2024,
    `毕业年应为 2024，实际 ${e.character.collegeGraduationYear}`);
  e.currentYear = 2024;
  e.currentAge = 22;
  e.updateCareerStage();
  assert.strictEqual(e.character.educationLevel, '大学本科');
  assert.ok(e.statusFlags.has('college_graduate'), '毕业年未标记 college_graduate');
});

test('P0-4 复读生第二年可以再次参加高考', async () => {
  const e = await freshEngine(42);
  makeCharacter(e, { educationLevel: '普通高中' });
  e.character.tags.add('high_school_student');
  e.currentYear = 2020;
  e.currentAge = 18;
  e.statusFlags.clear();
  e.statusFlags.add('decision_gaokao_jueze');
  e.statusFlags.add('repeating_gaokao');
  e.currentAge = 19;
  e.currentYear = 2021;
  const dec = e.checkLifeMilestone();
  assert.ok(dec && (dec.id === 'node_gaokao_retry' || dec.id === 'node_gaokao_jueze'),
    '复读生第二年没有再次触发高考');
});

// ---------------------------------------------------------------------------
// P0-5 选项门槛强制执行 + 角色匹配
// ---------------------------------------------------------------------------
test('P0-5 年龄标签会过滤掉不符合年龄的选项', async () => {
  const e = await freshEngine(51);
  makeCharacter(e, {});
  e.currentYear = 2000;
  e.currentAge = 20;
  const out = e.filterAndPolishChoices({
    id: 'test_age',
    title: '年龄门槛',
    choices: [
      { text: '青年选项', choiceTags: ['年龄：18–30'] },
      { text: '老年选项', choiceTags: ['年龄：60–70'] }
    ]
  });
  assert.strictEqual(out.choices.length, 1, `过滤后应剩 1 项，实际 ${out.choices.length}`);
  assert.strictEqual(out.choices[0].text, '青年选项');
});

test('P0-5 时代/地域标签会过滤掉不符合条件的选择', async () => {
  const e = await freshEngine(52);
  makeCharacter(e, {});
  e.currentYear = 2000;
  e.currentAge = 30;
  e.character.provinceId = 'shandong';
  const out = e.filterAndPolishChoices({
    id: 'test_era_region',
    title: '时代地域门槛',
    choices: [
      { text: '抗战选项', choiceTags: ['时代：1937–1949', '地域：全国'] },
      { text: '湖北选项', choiceTags: ['时代：通用时代', '地域：湖北武汉'] },
      { text: '当代山东选项', choiceTags: ['时代：2000–2015', '地域：全国'] }
    ]
  });
  assert.strictEqual(out.choices.length, 1, `过滤后应剩 1 项，实际 ${out.choices.length}`);
  assert.strictEqual(out.choices[0].text, '当代山东选项');
});

test('P0-5 全部选项被过滤时返回可执行的兜底选项，而不是空弹窗', async () => {
  const e = await freshEngine(53);
  makeCharacter(e, {});
  e.currentYear = 2000;
  e.currentAge = 20;
  const out = e.filterAndPolishChoices({
    id: 'test_empty',
    title: '全部过滤',
    choices: [
      { text: '老年选项', choiceTags: ['年龄：60–70'] },
      { text: '医护选项', choiceTags: ['门槛：医护'] }
    ]
  });
  assert.ok(out.choices && out.choices.length > 0, '过滤后没有兜底选项');
});

test('P0-5 普通工人不匹配八路军战士/华野战将/涉台侨属', async () => {
  const e = await freshEngine(54);
  makeCharacter(e, {});
  const city = firstCityOf(e, 'beijing');
  e.character.provinceId = 'beijing';
  e.character.cityId = city.id;
  e.character.cityName = city.name;
  e.character.careerTrack = 'worker';
  e.character.occupation = '国营机械厂车工';
  e.character.educationLevel = '初中';
  e.character.tags = new sandbox.Set(['urban', 'male', 'beijing', 'worker', '温饱']);
  e.currentYear = 1980;
  e.currentAge = 35;
  assert.strictEqual(e.characterMatchesPersonaRole('热血八路军战士'), false);
  assert.strictEqual(e.characterMatchesPersonaRole('华野主力战将'), false);
  assert.strictEqual(e.characterMatchesPersonaRole('涉台侨属亲友'), false);
});

test('P0-5 地理位置门槛不会对异地角色放行', async () => {
  const e = await freshEngine(55);
  makeCharacter(e, {});
  const city = firstCityOf(e, 'beijing');
  e.character.provinceId = 'beijing';
  e.character.cityId = city.id;
  e.character.cityName = city.name;
  e.currentYear = 2020;
  e.currentAge = 35;
  assert.strictEqual(e.characterMatchesPersonaRole('身处重庆市区'), false);
});

test('P0-5 1980 年不会把普通角色识别为智能手机用户', async () => {
  const e = await freshEngine(56);
  makeCharacter(e, {});
  e.character.careerTrack = 'worker';
  e.character.occupation = '国营机械厂车工';
  e.currentYear = 1980;
  e.currentAge = 35;
  assert.strictEqual(e.characterMatchesPersonaRole('智能手机用户'), false);
});

// ---------------------------------------------------------------------------
// P0-5c 2020/2022 硬编码人群分支不得错配
// ---------------------------------------------------------------------------
test('P0-5c 2022 年 22 岁农民不会被套用高校考研剧情', async () => {
  const e = await freshEngine(57);
  makeCharacter(e, { birthYear: 2000, educationLevel: '初中文化', careerTrack: 'farmer', occupation: '种粮农民' });
  e.currentYear = 2022;
  e.currentAge = 22;
  const d = e.adaptDecisionToPersona({
    id: 'evt_2022_covid_lockdown', title: '疫情', historicalFact: '疫情', choices: []
  });
  const text = `${d.title} ${d.narrative}`;
  assert.ok(!/高校|考研|答辩|春招/.test(text), `农民被套用高校剧情: ${text}`);
  assert.ok(/春耕|农资|保供|农产品/.test(text), `农民未获得务农分支: ${text}`);
});

test('P0-5c 2022 年 12 岁儿童获得居家网课分支而不是考研就业', async () => {
  const e = await freshEngine(58);
  makeCharacter(e, { birthYear: 2010, educationLevel: '小学在读' });
  e.currentYear = 2022;
  e.currentAge = 12;
  const d = e.adaptDecisionToPersona({
    id: 'evt_2022_covid_lockdown', title: '疫情', historicalFact: '疫情', choices: []
  });
  const text = `${d.title} ${d.narrative}`;
  assert.ok(/网课|居家|线上/.test(text), `儿童未获得网课分支: ${text}`);
  assert.ok(!/考研|考公|就业大盘/.test(text), `儿童被套用成人就业剧情: ${text}`);
});

test('P0-5c 2020 年普通教师不会被误判为医护', async () => {
  const e = await freshEngine(59);
  makeCharacter(e, {
    birthYear: 1980,
    occupation: '公办学校青年教师',
    educationLevel: '大学本科',
    careerTrack: 'cadre_teacher'
  });
  e.character.tags.delete('doctor');
  e.character.tags.delete('nurse');
  e.currentYear = 2020;
  e.currentAge = 40;
  const d = e.adaptDecisionToPersona({
    id: 'evt_2020_covid_chuxi', title: '疫情', historicalFact: '疫情', choices: []
  });
  assert.ok(!/白衣执甲|援鄂|医护/.test(d.title), `普通教师被误判为医护: ${d.title}`);
  assert.ok(/全民抗疫|举国同心/.test(d.title), `普通教师未获得居民分支: ${d.title}`);
});

test('P0-5c 2020 年湖北儿童不会拿到志愿者/请战成人选项', async () => {
  const e = await freshEngine(60);
  const city = firstCityOf(e, 'hubei');
  makeCharacter(e, {
    birthYear: 2008,
    provinceId: 'hubei',
    cityId: city.id,
    cityName: city.name,
    educationLevel: '小学在读'
  });
  e.currentYear = 2020;
  e.currentAge = 12;
  const d = e.adaptDecisionToPersona({
    id: 'evt_2020_covid_chuxi', title: '疫情', historicalFact: '疫情', choices: []
  });
  const filtered = e.filterAndPolishChoices(d);
  const text = filtered.choices.map(c => c.text).join('|');
  assert.ok(!/志愿者|请战|医疗队|红袖标/.test(text), `儿童拿到成人选项: ${text}`);
  assert.ok(/作业|家务|锻炼|父母/.test(text), `儿童分支缺少适龄选项: ${text}`);
});

// ---------------------------------------------------------------------------
// P1-6 标签子串碰撞
// ---------------------------------------------------------------------------
test('P1-6 “数控技师”不会被识别为教师/干部', async () => {
  const e = await freshEngine(61);
  makeCharacter(e, {});
  e.character.occupation = '现代制造车间数控技师';
  e.character.careerTrack = 'worker';
  assert.strictEqual(e.characterHasTag('cadre_teacher'), false);
});

test('P1-6 “普通高中”不会被识别为初中学历', async () => {
  const e = await freshEngine(62);
  makeCharacter(e, { educationLevel: '普通高中' });
  assert.strictEqual(e.characterHasTag('junior_high'), false);
  assert.strictEqual(e.characterHasTag('high_school'), true);
});

test('P1-6 “高等院校在读”不会被识别为高中学历', async () => {
  const e = await freshEngine(63);
  makeCharacter(e, { educationLevel: '高等院校在读' });
  assert.strictEqual(e.characterHasTag('high_school'), false);
});

// ---------------------------------------------------------------------------
// P1-3 2026 年出生角色结局与传承文案
// ---------------------------------------------------------------------------
test('P1-3 2026 年出生角色结局不称“少年求学”', async () => {
  const e = await freshEngine(71);
  makeCharacter(e, { birthYear: 2026 });
  e.triggerNaturalEnding();
  const last = e.character.milestones[e.character.milestones.length - 1];
  const text = `${last.title} ${e.deathInfo.cause} ${last.detail}`;
  assert.ok(!/少年|求学/.test(text), `2026 年出生角色结局出现少年/求学文案: ${text}`);
});

test('P1-3 2026 年出生角色的传承时间线不倒序、不虚构出生前经历', async () => {
  const e = await freshEngine(72);
  makeCharacter(e, {
    birthYear: 2026,
    urbanRural: 'urban',
    parentJob: '下岗待业'
  });
  const lineage = e.generateLineageHistory(e.character);
  const text = JSON.stringify(lineage);
  assert.ok(!text.includes('2032 — 2026'), '传承时间线出现 2032 — 2026 倒序');
  assert.ok(!lineage.child.timeline.some(x => x.detail.includes('疫情')),
    '2026 年出生角色被写入疫情网课经历');
  for (const item of lineage.child.timeline) {
    const m = item.period.match(/^(\d{4}) — (\d{4})/);
    if (m) assert.ok(Number(m[1]) <= Number(m[2]), `时间线倒序: ${item.period}`);
  }
});

test('P1-5 祖辈时间线不再给 1961 年后出生者写“三年困难时期”', async () => {
  const e = await freshEngine(73);
  makeCharacter(e, { birthYear: 2026, urbanRural: 'urban', parentJob: '国营厂工人' });
  const lineage = e.generateLineageHistory(e.character);
  if (lineage.grandparent.birthYear > 1961) {
    const text = JSON.stringify(lineage.grandparent);
    assert.ok(!text.includes('三年困难时期'), '祖辈出生晚于 1961 却仍写童年亲历三年困难时期');
  }
});

test('P1-5 父辈职业为下岗待业时不虚构“知识白领”', async () => {
  const e = await freshEngine(74);
  makeCharacter(e, { birthYear: 2026, urbanRural: 'urban', parentJob: '下岗待业' });
  const lineage = e.generateLineageHistory(e.character);
  const text = JSON.stringify(lineage.parent.timeline);
  assert.ok(!text.includes('知识白领'), '父辈职业为下岗待业却写成了知识白领');
});

// ---------------------------------------------------------------------------
// P1-7 退休金/养老金时代错位
// ---------------------------------------------------------------------------
test('P1-7 1980 年农村老人不会被写成“领着基础养老金”', async () => {
  const e = await freshEngine(81);
  makeCharacter(e, { birthYear: 1910, urbanRural: 'rural', careerTrack: 'farmer', occupation: '乡村退养农户' });
  e.currentYear = 1980;
  e.currentAge = 70;
  const s = e.getLaborSensorySnippet(e.character, 70, 1980, { displayName: '某村' });
  assert.ok(!s.includes('基础养老金'), `1980 年出现基础养老金: ${s}`);
});

test('P1-7 1965 年城市老人不会被写成“每月按时领退休金”', async () => {
  const e = await freshEngine(82);
  makeCharacter(e, { birthYear: 1900, urbanRural: 'urban', careerTrack: 'worker', occupation: '国营厂老工人' });
  e.currentYear = 1965;
  e.currentAge = 65;
  const s = e.getLaborSensorySnippet(e.character, 65, 1965, { displayName: '某市' });
  assert.ok(!s.includes('每月按时领退休金'), `1965 年出现每月退休金: ${s}`);
});

// ---------------------------------------------------------------------------
// P1-9 产妇死亡不得只凭“已婚”判定
// ---------------------------------------------------------------------------
test('P1-9 无怀孕/生育事件时不会随机判为产妇死亡', async () => {
  const e = await freshEngine(91);
  makeCharacter(e, { sex: '女', maritalStatus: '已婚' });
  e.character.tags = new sandbox.Set(['female', 'married']);
  e.character.hasChildren = false;
  e.currentYear = 2000;
  e.currentAge = 25;
  const era = e.getEraForYear(2000);
  for (let i = 0; i < 100; i++) {
    const cause = e.getAuthenticCauseOfDeath(era, 25, '女', e.character.attributes, e.character.tags, null);
    assert.ok(!/难产|羊水栓塞|分娩|产后大出血/.test(cause),
      `无怀孕事件却出现产妇死因: ${cause}`);
  }
});

// ---------------------------------------------------------------------------
// P2-1 出生队列权重
// ---------------------------------------------------------------------------
test('P2-1 出生年份分布与 avgAnnualBirthM × 年数 的误差小于 2 个百分点', async () => {
  const e = await freshEngine(101);
  const cohorts = e.stats.birthCohorts;
  const masses = cohorts.map(c => {
    const years = c.range[1] - c.range[0] + 1;
    return (c.avgAnnualBirthM || 1) * years;
  });
  const total = masses.reduce((a, b) => a + b, 0);
  const n = 20000;
  const counts = new Array(cohorts.length).fill(0);
  for (let i = 0; i < n; i++) {
    const y = e.sampleBirthYear();
    const idx = cohorts.findIndex(c => y >= c.range[0] && y <= c.range[1]);
    if (idx >= 0) counts[idx]++;
  }
  const failures = [];
  cohorts.forEach((c, i) => {
    const observed = counts[i] / n;
    const expected = masses[i] / total;
    if (Math.abs(observed - expected) > 0.02) {
      failures.push(`${c.name}: 观测 ${(observed * 100).toFixed(1)}% / 期望 ${(expected * 100).toFixed(1)}%`);
    }
  });
  assert.deepStrictEqual(failures, [], failures.join('; '));
});

// ---------------------------------------------------------------------------
// 运行器
// ---------------------------------------------------------------------------
(async () => {
  let passed = 0;
  const failed = [];
  for (const t of tests) {
    try {
      await t.fn();
      passed++;
      console.log(`✅ ${t.name}`);
    } catch (err) {
      failed.push({ name: t.name, error: err.message });
      console.log(`❌ ${t.name}\n   ${err.message}`);
    }
  }
  console.log(`\n=== 回归测试: ${passed}/${tests.length} 通过, ${failed.length} 失败 ===`);
  if (failed.length > 0) process.exit(1);
})();
