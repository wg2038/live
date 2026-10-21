// tools/batch_simulate.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const embeddedCode = fs.readFileSync(path.join(ROOT, 'data/embedded.js'), 'utf8');
const engineCode = fs.readFileSync(path.join(ROOT, 'js/engine.js'), 'utf8');

const sandbox = {
  window: {},
  console: console,
  Math: Math,
  Set: Set,
  Map: Map,
  Array: Array,
  Object: Object,
  setTimeout: setTimeout,
  clearTimeout: clearTimeout
};
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(embeddedCode, sandbox);
vm.runInContext(engineCode, sandbox);

async function runSimulation(totalCharacters = 5000) {
  const engine = new sandbox.SimulationEngine();
  await engine.init();

  console.log(`Starting batch simulation of ${totalCharacters} characters...`);

  const stats = {
    total: totalCharacters,
    birthsByYear: {},
    birthsByEra: {},
    deathsByEra: {
      '1937_1949': { deaths: 0, totalPersonYears: 0 },
      '1950_1957': { deaths: 0, totalPersonYears: 0 },
      '1958_1961': { deaths: 0, totalPersonYears: 0 },
      '1962_1976': { deaths: 0, totalPersonYears: 0 },
      '1977_1999': { deaths: 0, totalPersonYears: 0 },
      '2000_2026': { deaths: 0, totalPersonYears: 0 }
    },
    infantDeaths: 0,
    deceasedCount: 0,
    aliveIn2026: 0,
    totalLifespanDeceased: 0,
    totalLifespanAll: 0,
    marriedCount: 0,
    literateCount: 0,
    collegeCount: 0,
    eventTriggerCounts: {},
    decisionTriggerCounts: {},
    decisionChoiceCounts: {},
    deathCauses: {},
    disasterDeaths: 0,
    historicalEventDeaths: 0,
    naturalOrIllnessDeaths: 0,
    sampledCharacters: []
  };

  function getEraBucket(year) {
    if (year <= 1949) return '1937_1949';
    if (year <= 1957) return '1950_1957';
    if (year <= 1961) return '1958_1961';
    if (year <= 1976) return '1962_1976';
    if (year <= 1999) return '1977_1999';
    return '2000_2026';
  }

  for (let i = 0; i < totalCharacters; i++) {
    const char = engine.createCharacter({ paceMode: 'step', eraFilter: 'all' });
    const birthYear = char.birthYear;
    stats.birthsByYear[birthYear] = (stats.birthsByYear[birthYear] || 0) + 1;
    const birthEra = getEraBucket(birthYear);
    stats.birthsByEra[birthEra] = (stats.birthsByEra[birthEra] || 0) + 1;

    let isMarried = false;
    let maxEdu = '未入学';
    let lifeEvents = [];
    lifeEvents.push({ year: char.birthYear, age: 0, text: `出生在 ${char.birthPlace} ${char.cityName}` });

    let safetyLoop = 0;
    let decisionsCount = 0;
    while (!engine.isGameOver && engine.currentYear <= 2026 && safetyLoop < 150) {
      safetyLoop++;
      const curYear = engine.currentYear;
      const curAge = engine.currentAge;
      const eraBucket = getEraBucket(curYear);
      stats.deathsByEra[eraBucket].totalPersonYears++;

      // Advance year
      const yearLog = engine.advanceYear();
      if (yearLog && !yearLog.isDecision) {
        lifeEvents.push({ year: curYear, age: curAge, text: yearLog.title || yearLog.narrative || JSON.stringify(yearLog) });
      }

      // If pending decision
      if (engine.currentPendingDecision) {
        decisionsCount++;
        const dec = engine.currentPendingDecision;
        const decId = dec.id || dec.title;
        stats.decisionTriggerCounts[decId] = (stats.decisionTriggerCounts[decId] || 0) + 1;
        const choices = dec.choices || [];
        if (choices.length > 0) {
          const choiceIdx = Math.floor(Math.random() * choices.length);
          const chosen = choices[choiceIdx];
          const choiceKey = `${decId} -> ${chosen.text}`;
          stats.decisionChoiceCounts[choiceKey] = (stats.decisionChoiceCounts[choiceKey] || 0) + 1;

          engine.resolveDecision(dec.id, choiceIdx);
          lifeEvents.push({ year: engine.currentYear, age: engine.currentAge, text: `[抉择] ${dec.title}: 选择了「${chosen.text}」` });
        } else {
          engine.currentPendingDecision = null;
        }
      }

      // Check education & marital status
      if (char.educationLevel && char.educationLevel !== '未入学') {
        maxEdu = char.educationLevel;
      }
      if (char.maritalStatus === '已婚' || (char.tags && char.tags.has('married'))) {
        isMarried = true;
      }
    }

    stats.totalDecisions = (stats.totalDecisions || 0) + decisionsCount;

    const finalAge = engine.currentAge;
    stats.totalLifespanAll += finalAge;

    if (isMarried) stats.marriedCount++;
    if (maxEdu !== '未入学' && maxEdu !== '文盲') stats.literateCount++;
    if (maxEdu.includes('大专') || maxEdu.includes('本') || maxEdu.includes('研') || maxEdu.includes('大学') || maxEdu.includes('高等院校')) {
      stats.collegeCount++;
    }

    const isSurvival = engine.deathInfo && engine.deathInfo.isAliveIn2026;

    if (isSurvival) {
      stats.aliveIn2026++;
    } else {
      stats.deceasedCount++;
      stats.totalLifespanDeceased += finalAge;
      if (finalAge === 0) stats.infantDeaths++;

      const deathYear = engine.currentYear;
      const deathEra = getEraBucket(deathYear);
      stats.deathsByEra[deathEra].deaths++;

      const cause = engine.deathInfo ? engine.deathInfo.cause : '自然/意外逝世';
      stats.deathCauses[cause] = (stats.deathCauses[cause] || 0) + 1;

      if (cause.includes('地震') || cause.includes('洪水') || cause.includes('自然灾害') || cause.includes('饥荒') || cause.includes('干旱')) {
        stats.disasterDeaths++;
      } else if (cause.includes('空袭') || cause.includes('战') || cause.includes('武斗') || cause.includes('火灾爆炸')) {
        stats.historicalEventDeaths++;
      } else {
        stats.naturalOrIllnessDeaths++;
      }
    }

    // Keep 15 samples
    if (i < 15) {
      stats.sampledCharacters.push({
        id: i + 1,
        name: char.name,
        sex: char.sex,
        ethnicity: char.ethnicity,
        birthYear: char.birthYear,
        birthPlace: `${char.birthPlace} ${char.cityName}`,
        urbanRural: char.urbanRural,
        familyClass: char.familyClass,
        finalAge: finalAge,
        status: isSurvival ? '在世(2026·未完待续)' : '离世',
        cause: isSurvival ? '活至2026年' : (engine.deathInfo ? engine.deathInfo.cause : '自然离世'),
        maxEdu: maxEdu,
        occupation: char.occupation,
        careerRank: char.careerRank,
        isMarried: isMarried,
        timelineLength: lifeEvents.length,
        timeline: lifeEvents
      });
    }

    // Count events in milestones
    if (char.milestones) {
      for (const m of char.milestones) {
        const title = m.title || '未知里程碑';
        stats.eventTriggerCounts[title] = (stats.eventTriggerCounts[title] || 0) + 1;
      }
    }
  }

  return stats;
}

const count = parseInt(process.argv[2], 10) || 5000;
runSimulation(count).then(stats => {
  fs.writeFileSync(path.join(ROOT, 'tools/simulation_report.json'), JSON.stringify(stats, null, 2), 'utf8');
  console.log('Batch simulation complete. Report saved to tools/simulation_report.json');
  
  console.log('\n================ BATCH SIMULATION SUMMARY ================');
  console.log(`Total Simulated: ${stats.total}`);
  console.log(`Deceased: ${stats.deceasedCount} (${((stats.deceasedCount / stats.total) * 100).toFixed(1)}%)`);
  console.log(`Alive in 2026 ("未完待续"): ${stats.aliveIn2026} (${((stats.aliveIn2026 / stats.total) * 100).toFixed(1)}%)`);
  console.log(`Average Lifespan (Deceased): ${(stats.totalLifespanDeceased / stats.deceasedCount).toFixed(1)} 岁`);
  console.log(`Average Age (All at End): ${(stats.totalLifespanAll / stats.total).toFixed(1)} 岁`);
  console.log(`Average Decisions per Lifetime: ${(stats.totalDecisions / stats.total).toFixed(1)} 次`);
  console.log(`Infant Mortality (Age 0): ${stats.infantDeaths} (${((stats.infantDeaths / stats.total) * 100).toFixed(2)}%)`);
  console.log(`Marriage Rate: ${stats.marriedCount} (${((stats.marriedCount / stats.total) * 100).toFixed(1)}%)`);
  console.log(`Literacy Rate: ${stats.literateCount} (${((stats.literateCount / stats.total) * 100).toFixed(1)}%)`);
  console.log(`Higher Ed Rate: ${stats.collegeCount} (${((stats.collegeCount / stats.total) * 100).toFixed(1)}%)`);
  console.log(`Higher Ed Rate: ${stats.collegeCount} (${((stats.collegeCount / stats.total) * 100).toFixed(1)}%)`);
  
  console.log('\n--- Mortality by Era (Deaths / Person-Years) ---');
  for (const [era, data] of Object.entries(stats.deathsByEra)) {
    const rate = data.totalPersonYears > 0 ? ((data.deaths / data.totalPersonYears) * 1000).toFixed(2) : '0';
    console.log(`${era}: ${data.deaths} deaths in ${data.totalPersonYears} person-years (${rate} ‰)`);
  }

  console.log('\n--- Top 20 Triggered Milestones/Events ---');
  const sortedEvents = Object.entries(stats.eventTriggerCounts).sort((a, b) => b[1] - a[1]).slice(0, 20);
  sortedEvents.forEach(([k, v], idx) => {
    console.log(`${idx + 1}. ${k}: ${v} (${((v / stats.total) * 100).toFixed(1)}%)`);
  });

  console.log('\n--- Top 15 Decision Nodes Triggered ---');
  const sortedDecisions = Object.entries(stats.decisionTriggerCounts).sort((a, b) => b[1] - a[1]).slice(0, 15);
  sortedDecisions.forEach(([k, v], idx) => {
    console.log(`${idx + 1}. ${k}: ${v} (${((v / stats.total) * 100).toFixed(1)}%)`);
  });

  console.log('\n--- Death Causes Breakdown ---');
  console.log(`Disaster Deaths: ${stats.disasterDeaths} (${((stats.disasterDeaths / stats.deceasedCount) * 100).toFixed(1)}%)`);
  console.log(`Historical Event Deaths: ${stats.historicalEventDeaths} (${((stats.historicalEventDeaths / stats.deceasedCount) * 100).toFixed(1)}%)`);
  console.log(`Natural/Illness/Accident: ${stats.naturalOrIllnessDeaths} (${((stats.naturalOrIllnessDeaths / stats.deceasedCount) * 100).toFixed(1)}%)`);
  const topCauses = Object.entries(stats.deathCauses).sort((a, b) => b[1] - a[1]).slice(0, 10);
  topCauses.forEach(([k, v], idx) => {
    console.log(`  ${idx + 1}. ${k}: ${v}`);
  });
}).catch(err => {
  console.error('Simulation error:', err);
});
