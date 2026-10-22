// tools/audit_metrics.js
// 审计统计：批量跑完整人生，输出出生分布、学历/职业矛盾、事件覆盖率、死亡结构等指标。
// 用法: node tools/audit_metrics.js [局数]

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

function pct(a, b) { return b > 0 ? ((a / b) * 100).toFixed(1) + '%' : '0%'; }

async function main() {
  const total = parseInt(process.argv[2], 10) || 1000;
  setSeed(20261023);
  const engine = new sandbox.SimulationEngine();
  await engine.init();

  const cohorts = engine.stats.birthCohorts;
  const expectedMass = cohorts.map(c => (c.avgAnnualBirthM || 1) * (c.range[1] - c.range[0] + 1));
  const expectedTotal = expectedMass.reduce((a, b) => a + b, 0);

  const stats = {
    total,
    cohortCounts: new Array(cohorts.length).fill(0),
    cohortNames: cohorts.map(c => c.name),
    adultEducationAnomaly: 0,
    adultEducationSamples: [],
    degreeCareer: {},
    collegeInProgress: 0,
    degreeGraduates: 0,
    deaths2026: 0,
    deaths2026PeerAlive: 0,
    fatalDecisionDeaths: 0,
    deceased: 0,
    alive2026: 0,
    married: 0,
    hasChildren: 0,
    totalDecisions: 0,
    decisionEventCounts: {},
    triggeredEventIds: new Set(),
    deathCauses: {},
    finalEducation: {},
    finalCareer: {},
    crashes: []
  };

  for (let i = 0; i < total; i++) {
    let char;
    try {
      char = engine.createCharacter({ paceMode: 'step', eraFilter: 'all' });
    } catch (err) {
      stats.crashes.push({ life: i, phase: 'create', error: err.message });
      continue;
    }

    const birthYear = char.birthYear;
    const idx = cohorts.findIndex(c => birthYear >= c.range[0] && birthYear <= c.range[1]);
    if (idx >= 0) stats.cohortCounts[idx]++;

    let years = 0;
    try {
      while (!engine.isGameOver && engine.currentYear <= 2026 && years < 130) {
        years++;
        engine.advanceYear();
        if (engine.currentPendingDecision) {
          const dec = engine.currentPendingDecision;
          const decId = dec.id || dec.title;
          stats.totalDecisions++;
          stats.decisionEventCounts[decId] = (stats.decisionEventCounts[decId] || 0) + 1;
          const choices = dec.choices || [];
          if (choices.length > 0) {
            engine.resolveDecision(dec.id, Math.floor(Math.random() * choices.length));
          } else {
            engine.currentPendingDecision = null;
          }
        }
      }
    } catch (err) {
      stats.crashes.push({ life: i, phase: 'advance', year: engine.currentYear, age: engine.currentAge, error: err.message });
      continue;
    }

    for (const flag of engine.statusFlags) {
      if (flag.startsWith('done_')) stats.triggeredEventIds.add(flag.slice(5));
    }

    const death = engine.deathInfo || {};
    const isAlive = death.isAliveIn2026 === true;
    const finalAge = death.age !== undefined ? death.age : engine.currentAge;
    const edu = char.educationLevel || '未入学';
    const career = char.careerTrack || 'unknown';

    stats.finalEducation[edu] = (stats.finalEducation[edu] || 0) + 1;
    stats.finalCareer[career] = (stats.finalCareer[career] || 0) + 1;

    if (isAlive) {
      stats.alive2026++;
    } else {
      stats.deceased++;
      stats.deathCauses[death.cause || '未知'] = (stats.deathCauses[death.cause || '未知'] || 0) + 1;
      if (death.year === 2026) {
        stats.deaths2026++;
        const comp = engine.calculatePeerComparisons();
        if (comp && comp.education && comp.education.percentile === 85) {
          stats.deaths2026PeerAlive++;
        }
      }
      if (death.isEventFatal) stats.fatalDecisionDeaths++;
    }

    if (char.maritalStatus === '已婚' || (char.tags && char.tags.has('married'))) stats.married++;
    if (char.hasChildren) stats.hasChildren++;

    if (finalAge > 16 && /小学在读|初中在读/.test(edu)) {
      stats.adultEducationAnomaly++;
      if (stats.adultEducationSamples.length < 10) {
        stats.adultEducationSamples.push({
          name: char.name, birthYear, finalAge, edu, career, occupation: char.occupation
        });
      }
    }

    if (edu.includes('高等院校在读')) stats.collegeInProgress++;
    if (edu === '大学本科' || edu === '大专学历') stats.degreeGraduates++;

    if (edu.includes('高等院校在读') || edu === '大学本科' || edu === '大专学历') {
      const key = `${career}|${edu}`;
      stats.degreeCareer[key] = (stats.degreeCareer[key] || 0) + 1;
    }
  }

  const unreachableStatic = [];
  for (const evt of engine.events) {
    const yr = evt.yearRange || [1937, 2026];
    const ta = evt.targetAge;
    if (!ta) continue;
    const maxAge = yr[1] - 1937;
    if (ta[0] > maxAge) unreachableStatic.push(evt.id);
  }

  const allEventIds = new Set(engine.events.map(e => e.id));
  const untriggered = [...allEventIds].filter(id => !stats.triggeredEventIds.has(id));
  const reachableUntriggered = untriggered.filter(id => !unreachableStatic.includes(id));

  const report = {
    total,
    cohortObserved: cohorts.map((c, i) => ({
      name: c.name,
      range: c.range,
      observed: stats.cohortCounts[i],
      observedPct: +(stats.cohortCounts[i] / total * 100).toFixed(2),
      expectedPct: +(expectedMass[i] / expectedTotal * 100).toFixed(2)
    })),
    adultEducationAnomaly: stats.adultEducationAnomaly,
    adultEducationAnomalyPct: +(stats.adultEducationAnomaly / total * 100).toFixed(2),
    adultEducationSamples: stats.adultEducationSamples,
    degreeCareer: Object.entries(stats.degreeCareer).sort((a, b) => b[1] - a[1]),
    collegeInProgress: stats.collegeInProgress,
    degreeGraduates: stats.degreeGraduates,
    deaths2026: stats.deaths2026,
    deaths2026PeerAlive: stats.deaths2026PeerAlive,
    fatalDecisionDeaths: stats.fatalDecisionDeaths,
    fatalDecisionDeathPct: +(stats.fatalDecisionDeaths / Math.max(1, stats.deceased) * 100).toFixed(2),
    alive2026: stats.alive2026,
    deceased: stats.deceased,
    marriagePct: +(stats.married / total * 100).toFixed(2),
    childrenPct: +(stats.hasChildren / total * 100).toFixed(2),
    avgDecisions: +(stats.totalDecisions / total).toFixed(2),
    eventCoverage: {
      total: allEventIds.size,
      triggered: stats.triggeredEventIds.size,
      untriggered: untriggered.length,
      staticUnreachable: unreachableStatic.length,
      reachableUntriggered: reachableUntriggered.length,
      reachableUntriggeredIds: reachableUntriggered.slice(0, 40),
      staticUnreachableIds: unreachableStatic
    },
    finalEducation: Object.entries(stats.finalEducation).sort((a, b) => b[1] - a[1]),
    finalCareer: Object.entries(stats.finalCareer).sort((a, b) => b[1] - a[1]),
    crashes: stats.crashes.slice(0, 20),
    crashCount: stats.crashes.length,
    topDeathCauses: Object.entries(stats.deathCauses).sort((a, b) => b[1] - a[1]).slice(0, 15),
    topDecisionEvents: Object.entries(stats.decisionEventCounts).sort((a, b) => b[1] - a[1]).slice(0, 20)
  };

  fs.writeFileSync(path.join(ROOT, 'tools/audit_metrics.json'), JSON.stringify(report, null, 2), 'utf8');

  console.log(`\n=== 审计统计 (${total} 局) ===`);
  console.log(`崩溃: ${report.crashCount}`);
  console.log(`成年仍显示小学/初中在读: ${report.adultEducationAnomaly} (${report.adultEducationAnomalyPct}%)`);
  console.log(`最终“高等院校在读”: ${report.collegeInProgress}, 本科/大专毕业: ${report.degreeGraduates}`);
  console.log(`2026 年死亡: ${report.deaths2026}, 其中仍走“在世”百分位: ${report.deaths2026PeerAlive}`);
  console.log(`致命决策死亡 / 全部死亡: ${report.fatalDecisionDeaths}/${report.deceased} (${report.fatalDecisionDeathPct}%)`);
  console.log(`结婚率: ${report.marriagePct}%, 有子女率: ${report.childrenPct}%`);
  console.log(`人均决策: ${report.avgDecisions}`);
  console.log(`事件覆盖: ${report.eventCoverage.triggered}/${report.eventCoverage.total}, 静态不可达 ${report.eventCoverage.staticUnreachable}, 可达但未触发 ${report.eventCoverage.reachableUntriggered}`);
  console.log('\n出生队列观测 vs 期望:');
  for (const c of report.cohortObserved) {
    console.log(`  ${c.name} ${c.range[0]}–${c.range[1]}: ${c.observedPct}% vs ${c.expectedPct}%`);
  }
  console.log('\n学历/职业矛盾 Top:');
  for (const [k, v] of report.degreeCareer.slice(0, 10)) console.log(`  ${k}: ${v}`);
  if (report.adultEducationSamples.length) {
    console.log('\n成年在读样例:');
    for (const s of report.adultEducationSamples) console.log(`  ${s.name} ${s.birthYear}年生 ${s.finalAge}岁 ${s.edu} ${s.career} ${s.occupation}`);
  }
  console.log('\n报告已写入 tools/audit_metrics.json');
}

main().catch(err => { console.error(err); process.exit(1); });
