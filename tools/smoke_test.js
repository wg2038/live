// tools/smoke_test.js
// 快速轻量冒烟测试：运行 50 个随机角色，验证逻辑闭环、无报错、无路径矛盾

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

async function runSmokeTest(count = 50) {
  const engine = new sandbox.SimulationEngine();
  await engine.init();

  console.log(`\n=== 🚀 启动轻量开发阶段冒烟测试 (${count} 个随机角色) ===`);
  const startTime = Date.now();

  let errors = [];
  let warnings = [];
  let totalDecisions = 0;
  let triggeredEventsSet = new Set();
  let survivedCount = 0;
  let deceasedCount = 0;

  for (let i = 0; i < count; i++) {
    const char = engine.createCharacter({ paceMode: 'step', eraFilter: 'all' });
    let safetyLoop = 0;
    let charDecisions = 0;

    while (!engine.isGameOver && engine.currentYear <= 2026 && safetyLoop < 120) {
      safetyLoop++;
      const curYear = engine.currentYear;
      const curAge = engine.currentAge;

      try {
        engine.advanceYear();
      } catch (err) {
        errors.push(`[角色 #${i+1} ${curYear}年/${curAge}岁] advanceYear 抛出异常: ${err.message}`);
        break;
      }

      if (engine.currentPendingDecision) {
        charDecisions++;
        totalDecisions++;
        const dec = engine.currentPendingDecision;
        const decId = dec.id || dec.title;
        triggeredEventsSet.add(decId);

        // 校验 1: 幼童阻断 (<6 岁不可出现决策)
        if (curAge < 6) {
          errors.push(`[逻辑矛盾] 角色 #${i+1} 在 ${curAge} 岁（襁褓期）触发了决策: ${dec.title}`);
        }

        // 校验 2: 路径一致性约束
        if (decId.includes('gaokao') || decId.includes('gaodeng')) {
          const tags = engine.character.tags || new Set();
          const edu = engine.character.educationLevel || '';
          const hasRemedial = tags.has('status_high_school_diploma') || tags.has('status_literate') || tags.has('status_college_diploma');
          const isHighSchool = edu.includes('高中') || edu.includes('中专') || edu.includes('大专');
          if (!isHighSchool && !hasRemedial && edu === '未入学') {
            errors.push(`[路径矛盾] 角色 #${i+1} 既往未入学且无补救学历，却触发高考: ${decId}`);
          }
        }

        // 校验 3: 身份准入一致性 (学生在非典中绝不可看到或选择医护一线重症选项)
        if (decId === 'evt_2003_sars_feidian') {
          const occ = engine.character.occupation || '';
          const isMedic = engine.characterHasTag('doctor') || engine.characterHasTag('nurse') || /医|护|卫/.test(occ);
          const hasMedicChoice = (dec.choices || []).some(c => c.text && c.text.includes('小汤山一线隔离区'));
          if (!isMedic && hasMedicChoice) {
            errors.push(`[身份越位] 非医护角色 #${i+1} (${engine.character.age}岁, 职业: ${occ}) 在非典中被展示了一线ICU抢救选项`);
          }
        }

        const choices = dec.choices || [];
        if (!choices || choices.length === 0) {
          errors.push(`[数据缺陷] 决策事件 ${decId} 缺少选项 choices`);
          engine.currentPendingDecision = null;
        } else {
          // 随机挑选选项模拟
          const choiceIdx = Math.floor(Math.random() * choices.length);
          try {
            engine.resolveDecision(dec.id, choiceIdx);
          } catch (err) {
            errors.push(`[决断异常] 解决决策 ${decId} 时出错: ${err.message}`);
          }
        }
      }
    }

    const isAlive = engine.deathInfo && engine.deathInfo.isAliveIn2026;
    if (isAlive) {
      survivedCount++;
    } else {
      deceasedCount++;
    }
  }

  const duration = ((Date.now() - startTime) / 1000).toFixed(2);
  console.log(`\n=== 📊 冒烟测试完成 (耗时: ${duration}s) ===`);
  console.log(`- 模拟角色总数: ${count} 人`);
  console.log(`- 存活至2026在世: ${survivedCount} 人 (${((survivedCount/count)*100).toFixed(1)}%)`);
  console.log(`- 离世角色: ${deceasedCount} 人 (${((deceasedCount/count)*100).toFixed(1)}%)`);
  console.log(`- 触发总决策次数: ${totalDecisions} 次 (人均 ${(totalDecisions/count).toFixed(1)} 次)`);
  console.log(`- 触发独特事件种数: ${triggeredEventsSet.size} 个`);

  if (errors.length > 0) {
    console.error(`\n❌ 发现 ${errors.length} 个逻辑与运行错误:`);
    errors.slice(0, 10).forEach((err, idx) => console.error(`  ${idx+1}. ${err}`));
    process.exit(1);
  } else {
    console.log(`\n✅ 冒烟测试全部通过！0 报错、0 路径逻辑矛盾、0 崩溃！`);
  }
}

runSmokeTest(parseInt(process.argv[2], 10) || 50).catch(err => {
  console.error("Fatal error:", err);
  process.exit(1);
});
