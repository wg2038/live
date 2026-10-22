// tools/lineage_test.js
// 传承模式全量验证：先完整跑完一世，再用该角色作为父辈重开一世，检查状态初始化与叙事闭环。
// 用法: node tools/lineage_test.js [局数]

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const embeddedCode = fs.readFileSync(path.join(ROOT, 'data/embedded.js'), 'utf8');
const engineCode = fs.readFileSync(path.join(ROOT, 'js/engine.js'), 'utf8');

let rngState = 20261023;
function setSeed(seed) { rngState = (seed >>> 0) || 1; }
function nextRandom() {
  rngState = (Math.imul(1664525, rngState) + 1013904223) >>> 0;
  return rngState / 4294967296;
}

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

async function runLife(engine, maxYears = 130) {
  let years = 0;
  let decisions = 0;
  while (!engine.isGameOver && engine.currentYear <= 2026 && years < maxYears) {
    years++;
    engine.advanceYear();
    if (engine.currentPendingDecision) {
      const dec = engine.currentPendingDecision;
      const choices = dec.choices || [];
      if (choices.length > 0) {
        engine.resolveDecision(dec.id, Math.floor(Math.random() * choices.length));
      } else {
        engine.currentPendingDecision = null;
      }
      decisions++;
    }
  }
  return { years, decisions };
}

function profileFromCharacter(char) {
  return {
    birthYear: char.birthYear,
    provinceId: char.provinceId,
    cityId: char.cityId,
    urbanRural: char.urbanRural,
    sex: char.sex,
    ethnicity: char.ethnicity,
    name: char.name,
    childName: `${char.name}之子女`
  };
}

async function main() {
  const total = parseInt(process.argv[2], 10) || 1000;
  setSeed(20261023);

  const engine = new sandbox.SimulationEngine();
  await engine.init();

  const report = {
    total,
    parentsCompleted: 0,
    lineageStarted: 0,
    lineageCompleted: 0,
    crashes: [],
    initErrors: [],
    logicErrors: [],
    parentDeaths: 0,
    lineageDeaths: 0,
    lineageAlive2026: 0,
    totalDecisions: 0,
    avgDecisions: 0,
    birthYears: {}
  };

  for (let i = 0; i < total; i++) {
    let parentProfile;
    try {
      const parent = engine.createCharacter({ paceMode: 'step', eraFilter: 'all' });
      await runLife(engine);
      parentProfile = profileFromCharacter(parent);
      report.parentsCompleted++;
    } catch (err) {
      report.crashes.push({ life: i, phase: 'parent', error: err.message });
      continue;
    }

    let child;
    try {
      child = engine.createCharacterFromParent(parentProfile);
      report.lineageStarted++;
    } catch (err) {
      report.crashes.push({ life: i, phase: 'lineage-init', error: err.message });
      continue;
    }

    // 初始化契约检查
    if (!(child.tags instanceof sandbox.Set)) {
      report.initErrors.push({ life: i, error: 'tags 不是 Set' });
    }
    if (!Array.isArray(child.causalityReview)) {
      report.initErrors.push({ life: i, error: 'causalityReview 不是数组' });
    }
    if (child.isInheritedParent !== true) {
      report.initErrors.push({ life: i, error: 'isInheritedParent 未标记' });
    }
    if (child.childName !== parentProfile.childName) {
      report.initErrors.push({ life: i, error: 'childName 未继承' });
    }
    if (engine.currentYear !== child.birthYear || engine.currentAge !== 0) {
      report.initErrors.push({ life: i, error: `起点年份/年龄错误: ${engine.currentYear}/${engine.currentAge}` });
    }
    if (!child.milestones.some(m => m.title === '血脉溯源')) {
      report.initErrors.push({ life: i, error: '缺少“血脉溯源”里程碑' });
    }
    if (child.birthYear < 1937 || child.birthYear > 2026) {
      report.initErrors.push({ life: i, error: `出生年份越界: ${child.birthYear}` });
    }

    try {
      const result = await runLife(engine);
      report.lineageCompleted++;
      report.totalDecisions += result.decisions;
      const birthYear = child.birthYear;
      report.birthYears[birthYear] = (report.birthYears[birthYear] || 0) + 1;

      const death = engine.deathInfo || {};
      if (death.isAliveIn2026 === true) {
        report.lineageAlive2026++;
      } else {
        report.lineageDeaths++;
      }

      const finalAge = death.age !== undefined ? death.age : engine.currentAge;
      if (finalAge > 16 && /小学在读|初中在读/.test(child.educationLevel || '')) {
        report.logicErrors.push({ life: i, error: `成年仍在读: ${finalAge}岁 ${child.educationLevel}` });
      }
      // 在世角色在 2026 年停笔时 deathInfo.year 也是 2026，这是正常状态；
      // 只有死亡年份早于 2026 却仍标记在世才矛盾。
      if (death.year < 2026 && death.isAliveIn2026 === true) {
        report.logicErrors.push({ life: i, error: `早于 2026（${death.year}）死亡却标记为在世` });
      }
      if (engine.currentYear > 2026) {
        report.logicErrors.push({ life: i, error: `掠过 2026: ${engine.currentYear}` });
      }
    } catch (err) {
      report.crashes.push({ life: i, phase: 'lineage-run', year: engine.currentYear, age: engine.currentAge, error: err.message });
    }
  }

  report.avgDecisions = +(report.totalDecisions / Math.max(1, report.lineageCompleted)).toFixed(2);
  report.crashCount = report.crashes.length;
  report.initErrorCount = report.initErrors.length;
  report.logicErrorCount = report.logicErrors.length;

  fs.writeFileSync(path.join(ROOT, 'tools/lineage_test.json'), JSON.stringify(report, null, 2), 'utf8');

  console.log(`\n=== 传承模式验证 (${total} 局) ===`);
  console.log(`父辈完整跑完: ${report.parentsCompleted}`);
  console.log(`传承成功启动: ${report.lineageStarted}, 完整跑完: ${report.lineageCompleted}`);
  console.log(`崩溃: ${report.crashCount}, 初始化错误: ${report.initErrorCount}, 逻辑错误: ${report.logicErrorCount}`);
  console.log(`传承世死亡: ${report.lineageDeaths}, 2026 在世: ${report.lineageAlive2026}`);
  console.log(`传承世人均决策: ${report.avgDecisions}`);
  if (report.crashes.length) {
    console.log('\n崩溃样例:');
    for (const c of report.crashes.slice(0, 10)) console.log(`  ${JSON.stringify(c)}`);
  }
  if (report.initErrors.length) {
    console.log('\n初始化错误样例:');
    for (const c of report.initErrors.slice(0, 10)) console.log(`  ${JSON.stringify(c)}`);
  }
  if (report.logicErrors.length) {
    console.log('\n逻辑错误样例:');
    for (const c of report.logicErrors.slice(0, 10)) console.log(`  ${JSON.stringify(c)}`);
  }
  console.log('\n报告已写入 tools/lineage_test.json');

  if (report.crashCount || report.initErrorCount || report.logicErrorCount) process.exitCode = 1;
}

main().catch(err => { console.error(err); process.exit(1); });
