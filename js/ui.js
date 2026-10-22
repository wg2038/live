/**
 * live · 14亿分之1 (中国历史人生模拟 1937–2026)
 * 1:1 Modern Editorial Controller & Canvas Renderer based on 1in8b.life
 */

document.addEventListener('DOMContentLoaded', async () => {
  const engine = new window.SimulationEngine();

  // 1. 初始化引擎多源历史数据库
  try {
    await engine.init();
    console.log('历史与城市数据库加载完毕');
  } catch (err) {
    console.error('引擎数据初始化失败:', err);
  }

  // =========================================================================
  // 主题切换管理 (Theme Manager)
  // =========================================================================
  const themeBtn = document.getElementById('themeBtn');
  const themeBtn2 = document.getElementById('themeBtn2');

  function initTheme() {
    const saved = localStorage.getItem('live_theme');
    if (saved) {
      document.documentElement.setAttribute('data-theme', saved);
    } else {
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }
  }

  function toggleTheme() {
    const cur = document.documentElement.getAttribute('data-theme') || 'light';
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('live_theme', next);
  }

  if (themeBtn) themeBtn.addEventListener('click', toggleTheme);
  if (themeBtn2) themeBtn2.addEventListener('click', toggleTheme);
  initTheme();

  // =========================================================================
  // 首页实时人口统计计数器 (Live Ticker)
  // =========================================================================
  const cBirthEl = document.getElementById('cBirth');
  const cDeathEl = document.getElementById('cDeath');
  const pageStartTime = Date.now();
  // 真实人口统计模型：当前中国年出生人口约 902 万人（约 0.2858 人/秒），年离世人口约 1041 万人（约 0.3299 人/秒）
  const BIRTH_RATE_PER_SEC = 9020000 / (365.25 * 86400);
  const DEATH_RATE_PER_SEC = 10410000 / (365.25 * 86400);

  function updateLiveTicker() {
    const elapsedSec = (Date.now() - pageStartTime) / 1000;
    const currentBirths = Math.floor(elapsedSec * BIRTH_RATE_PER_SEC);
    const currentDeaths = Math.floor(elapsedSec * DEATH_RATE_PER_SEC);
    if (cBirthEl) cBirthEl.textContent = currentBirths.toLocaleString('zh-CN');
    if (cDeathEl) cDeathEl.textContent = currentDeaths.toLocaleString('zh-CN');
  }
  setInterval(updateLiveTicker, 200);
  updateLiveTicker();

  // =========================================================================
  // 首页配置选项卡 (Segmented Controls)
  // =========================================================================
  let selectedEra = 'all';
  let selectedCity = 'weighted';
  let selectedPace = 'medium';

  function bindSegment(id, onChange) {
    const container = document.getElementById(id);
    if (!container) return;
    const buttons = container.querySelectorAll('button');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.setAttribute('aria-pressed', 'false'));
        btn.setAttribute('aria-pressed', 'true');
        onChange(btn.getAttribute('data-val'));
      });
    });
  }

  bindSegment('segEra', val => { selectedEra = val; });
  bindSegment('segCity', val => { selectedCity = val; });
  bindSegment('segPace', val => { selectedPace = val; });

  // 追思馆本地存储渲染
  const MEMORIAL_STORAGE_KEY = 'live_memorial_lives';
  function loadMemorialLives() {
    const grid = document.getElementById('pastLivesGrid');
    if (!grid) return;
    try {
      const stored = JSON.parse(localStorage.getItem(MEMORIAL_STORAGE_KEY) || '[]');
      if (stored.length > 0) {
        grid.innerHTML = stored.slice(-6).reverse().map(item => `
          <div class="memo-card">
            <div class="mc-head"><span>${item.birthYear} — ${item.deathYear} · 享年 ${item.age} 岁</span><span>${item.place}</span></div>
            <div class="mc-name">${escapeHtml(item.name)} (${item.job})</div>
            <div class="mc-note">“${escapeHtml(item.farewell || '平凡一生，踏实走过。')}”</div>
          </div>
        `).join('');
      }
    } catch (e) {
      console.warn('追思馆读取失败', e);
    }
  }
  loadMemorialLives();

  // =========================================================================
  // 视图切换与轮盘动画 (Views & Roulette Roll)
  // =========================================================================
  const secIntro = document.getElementById('intro');
  const secRoll = document.getElementById('roll');
  const secLifeview = document.getElementById('lifeview');
  const secDead = document.getElementById('dead');
  const modalEl = document.getElementById('modal');

  function showSection(targetSec) {
    [secIntro, secRoll, secLifeview, secDead].forEach(s => {
      if (s) s.hidden = (s !== targetSec);
    });
    window.scrollTo(0, 0);
  }

  const startBtn = document.getElementById('startBtn');
  const rollerEl = document.getElementById('roller');
  const rollNameEl = document.getElementById('rollName');
  const rollMetaEl = document.getElementById('rollMeta');
  const certEl = document.getElementById('cert');
  const reRollBtn = document.getElementById('reRollBtn');
  const beginBtn = document.getElementById('beginBtn');

  let isRolling = false;
  async function triggerRoulette() {
    if (isRolling) return;
    isRolling = true;

    try {
      showSection(secRoll);
      rollerEl.hidden = false;
      certEl.hidden = true;

      const rollProgressEl = document.getElementById('rollProgress');
      if (rollProgressEl) rollProgressEl.style.width = '0%';

      // 1. 预先创建角色，确保终点与出生登记证 100% 严丝合缝
      const char = engine.createCharacter({
        eraFilter: 'all',
        cityFilter: 'weighted',
        paceMode: 'medium'
      });

      const finalProv = (char.birthPlace || '').replace(/(特别行政区|维吾尔自治区|壮族自治区|回族自治区|自治区|省|市)/g, '');
      const finalCity = ['北京', '上海', '天津', '重庆'].includes(finalProv)
        ? `${finalProv}市`
        : (finalProv ? `${finalProv} · ` : '') + (char.cityHistoricalName || '');
      const lunar = getLunarYearName(char.birthYear);
      const finalMeta = `${char.birthYear}年 · ${lunar} · ${char.cityType || '普通家庭'}`;

      // 2. 规范化候选城市库：去除长后缀及括号历史说明，将单行字符长度严格控制在规范以内，彻底避免多行高度跳动
      const rawCities = (engine.cities && engine.cities.length > 0) ? engine.cities : [];
      const candidateList = rawCities.map(c => {
        const prov = engine.provinces ? engine.provinces.find(p => p.id === c.provinceId) : null;
        const pName = (prov ? prov.name : '').replace(/(特别行政区|维吾尔自治区|壮族自治区|回族自治区|自治区|省|市)/g, '');
        let cName = (c.name || '').replace(/[（\(][^）\)]*[）\)]/g, '').trim();
        if (['北京', '上海', '天津', '重庆'].includes(pName)) {
          return { displayName: `${pName}市`, type: c.type || '直辖市' };
        }
        cName = cName.replace(/(藏族羌族|朝鲜族|哈萨克|蒙古|藏族|傣族|白族|柯尔克孜|回族|布依族苗族|苗族侗族)自治州$/, '州');
        const displayName = pName ? `${pName} · ${cName}` : cName;
        return {
          displayName,
          type: c.type || '城市'
        };
      });

      // 3. 严格跳动 5 秒整，采用平滑物理拟真减速曲线（前 3 秒极速抓取，3~4.6 秒递进减速，4.6~5 秒精准停靠）
      const totalDuration = 5000;
      const startTime = Date.now();

      await new Promise(resolve => {
        function tick() {
          const elapsed = Date.now() - startTime;
          const progress = Math.min(100, Math.round((elapsed / totalDuration) * 100));
          if (rollProgressEl) rollProgressEl.style.width = `${progress}%`;

          if (elapsed >= totalDuration) {
            rollNameEl.textContent = finalCity;
            rollMetaEl.textContent = finalMeta;
            if (rollProgressEl) rollProgressEl.style.width = '100%';
            resolve();
            return;
          }

          if (elapsed >= 4600) {
            rollNameEl.textContent = finalCity;
            rollMetaEl.textContent = finalMeta;
            setTimeout(tick, totalDuration - elapsed);
            return;
          }

          if (candidateList.length > 0) {
            const rnd = candidateList[Math.floor(Math.random() * candidateList.length)];
            const rndYear = Math.floor(1937 + Math.random() * 89);
            rollNameEl.textContent = rnd.displayName;
            rollMetaEl.textContent = `${rndYear}年 · ${rnd.type}`;
          }

          let nextDelay = 65;
          if (elapsed > 3000) {
            const p = (elapsed - 3000) / 1600;
            nextDelay = Math.round(65 + Math.pow(p, 2) * 320);
          }
          setTimeout(tick, nextDelay);
        }
        tick();
      });

      // 4. 填充出生登记证并无缝展示
      renderBirthCertificate(char);
      rollerEl.hidden = true;
      certEl.hidden = false;
    } finally {
      isRolling = false;
    }
  }

  function renderBirthCertificate(char) {
    const era = engine.getEraForYear(char.birthYear);
    const serial = `NO. 1937-2026-${Math.floor(1000 + Math.random() * 9000)}`;

    document.getElementById('certNo').textContent = serial;
    document.getElementById('certName').textContent = char.name;

    const isUrban = char.urbanRural === 'urban';
    const urbanLabel = isUrban ? '城镇户籍' : '农村户籍';
    const tagEl = document.getElementById('certUrbanTag');
    if (tagEl) {
      tagEl.textContent = urbanLabel;
      tagEl.className = `cert-status-badge ${isUrban ? 'badge-urban' : 'badge-rural'}`;
    }

    const lunar = getLunarYearName(char.birthYear);
    const provName = (char.birthPlace || '').replace(/(特别行政区|维吾尔自治区|壮族自治区|回族自治区|自治区|省|市)/g, '');
    const placeName = ['北京', '上海', '天津', '重庆'].includes(provName)
      ? `${provName}市`
      : (provName ? `${provName} · ` : '') + (char.cityHistoricalName || '');

    const story = `你出生在 ${char.birthYear} 年（${lunar}）的 ${placeName}。彼时当地正值【${char.cityType}】定位，以【${char.industryPillar}】为时代重心。家中长辈靠【${char.parentJob}】维持生计，撑起一门烟火，同胞兄弟姐妹共 ${char.siblingsCount} 人。`;
    document.getElementById('certStory').textContent = story;

    document.getElementById('cfYear').textContent = `${char.birthYear}年 (${lunar})`;
    document.getElementById('cfPlace').textContent = `${char.birthPlace} · ${char.cityHistoricalName}`;
    document.getElementById('cfUrban').textContent = urbanLabel;
    document.getElementById('cfLife').textContent = `${era.lifeExpectancy} 岁`;
    document.getElementById('cfInd').textContent = char.industryPillar;
    document.getElementById('cfSiblings').textContent = `${char.siblingsCount} 人`;

    const urbanPct = Math.round(era.urbanRatio);
    const ruralPct = 100 - urbanPct;
    if (isUrban) {
      document.getElementById('certOdds').textContent = `在 ${char.birthYear} 年出生的中国人中，约有 ${urbanPct}% 像你一样生于城镇，其余 ${ruralPct}% 则生于乡村。当年全国人均期望寿命约为 ${era.lifeExpectancy} 岁。`;
    } else {
      document.getElementById('certOdds').textContent = `在 ${char.birthYear} 年出生的中国人中，约有 ${ruralPct}% 像你一样生于乡村，仅 ${urbanPct}% 生于城镇。当年全国人均期望寿命约为 ${era.lifeExpectancy} 岁。`;
    }
  }

  if (startBtn) startBtn.addEventListener('click', triggerRoulette);
  if (reRollBtn) reRollBtn.addEventListener('click', triggerRoulette);

  // =========================================================================
  // 人生推演主循环与时间控制器 (Life Simulation Game Loop)
  // =========================================================================
  let gameTimer = null;
  let isPaused = false;
  let currentSpeedMs = 1100; // 1× 初始速度

  const pauseBtn = document.getElementById('pauseBtn');
  const stepBtn = document.getElementById('stepBtn');
  const spButtons = document.querySelectorAll('#spSet button');

  function setSpeed(multiplier) {
    spButtons.forEach(btn => {
      const m = parseInt(btn.getAttribute('data-speed'), 10);
      btn.setAttribute('aria-pressed', m === multiplier ? 'true' : 'false');
    });
    if (multiplier === 1) currentSpeedMs = 1100;
    else if (multiplier === 2) currentSpeedMs = 550;
    else if (multiplier === 4) currentSpeedMs = 240;

    if (!isPaused && gameTimer) {
      clearInterval(gameTimer);
      gameTimer = setInterval(tickTurn, currentSpeedMs);
    }
  }

  spButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const m = parseInt(btn.getAttribute('data-speed'), 10);
      setSpeed(m);
    });
  });

  function pauseGame() {
    isPaused = true;
    if (gameTimer) {
      clearInterval(gameTimer);
      gameTimer = null;
    }
    if (pauseBtn) {
      pauseBtn.setAttribute('aria-pressed', 'true');
      pauseBtn.textContent = '▶ 继续';
    }
  }

  function resumeGame() {
    isPaused = false;
    if (pauseBtn) {
      pauseBtn.setAttribute('aria-pressed', 'false');
      pauseBtn.textContent = '❚❚ 暂停';
    }
    if (!gameTimer) {
      gameTimer = setInterval(tickTurn, currentSpeedMs);
    }
  }

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      if (isPaused) resumeGame();
      else pauseGame();
    });
  }

  if (stepBtn) {
    stepBtn.addEventListener('click', () => {
      pauseGame();
      tickTurn();
    });
  }

  // 开始人生按钮
  if (beginBtn) {
    beginBtn.addEventListener('click', () => {
      showSection(secLifeview);
      initLifeviewUI();
      resumeGame();
    });
  }

  function initLifeviewUI() {
    const char = engine.character;
    // 身份证面板
    document.getElementById('idName').textContent = char.name;
    document.getElementById('idPlace').textContent = `${char.birthPlace} · ${char.cityHistoricalName}`;
    document.getElementById('idClass').textContent = `${char.urbanRural === 'urban' ? '城镇职工' : '农村户籍'} · ${char.economicLevel}`;
    document.getElementById('idJob').textContent = char.occupation || '孩童';

    // 清空纪事流
    const feed = document.getElementById('lifeFeed');
    if (feed) feed.innerHTML = '';

    // 重置精力分配按钮
    setFocusChip('work');

    // 记录出生首条
    appendFeedItem({
      age: 0,
      year: char.birthYear,
      tag: '诞生于世',
      tagClass: 'tag-era',
      narrative: `你降生在${char.birthPlace}${char.cityHistoricalName}。其时地属【${char.cityType}】，当地主导生计为【${char.industryPillar}】，父亲/长辈靠【${char.parentJob}】养家。家中有同辈兄弟姐妹${char.siblingsCount}人。`
    });

    updateVitalsUI();
  }

  // 精力重心调节器
  const focusChips = document.querySelectorAll('#focusChips .chip');
  const focusHint = document.getElementById('focusHint');

  const focusProfiles = {
    study: {
      energy: [45, 15, 15, 25],
      hint: '当前重心：读书求学。心系笔墨知识，大幅提升文化与技能，为升学与时代转折打下根基。'
    },
    work: {
      energy: [10, 55, 15, 20],
      hint: '当前重心：勤奋搞钱。投入大量汗水赚取年入与积蓄，家门殷实，但略耗损体魄健康。'
    },
    family: {
      energy: [10, 15, 55, 20],
      hint: '当前重心：顾家陪伴。悉心照看老幼亲族，家门融洽温存，滋养内心志气与抗挫韧劲。'
    },
    health: {
      energy: [10, 15, 20, 55],
      hint: '当前重心：养生疗愈。注重饮食歇息与防病强身，加速恢复体力，极大降低恶疾与暴毙风险。'
    }
  };

  function setFocusChip(key) {
    focusChips.forEach(c => {
      c.setAttribute('aria-pressed', c.getAttribute('data-focus') === key ? 'true' : 'false');
    });
    const profile = focusProfiles[key] || focusProfiles.work;
    engine.setEnergy(...profile.energy);
    if (focusHint) focusHint.textContent = profile.hint;
  }

  focusChips.forEach(c => {
    c.addEventListener('click', () => {
      setFocusChip(c.getAttribute('data-focus'));
    });
  });

  // 更新左栏属性与仪表盘
  function updateVitalsUI() {
    const char = engine.character;
    if (!char) return;

    const age = engine.currentAge;
    const year = engine.currentYear;
    const attr = char.attributes;
    const era = engine.getEraForYear(year);

    // 顶部年岁与进度条
    document.getElementById('ageNum').innerHTML = `${age}<small>岁</small>`;
    const lunar = getLunarYearName(year);
    document.getElementById('ageYear').textContent = `${year} 年 (${lunar}) · ${era.name}`;

    const progPercent = Math.min(100, Math.max(0, (age / 85) * 100));
    const progBar = document.getElementById('prog');
    if (progBar) progBar.style.transform = `scaleX(${progPercent / 100})`;

    // 四维状态进度条
    setBarVal('barHealth', 'valHealth', attr.health, getHealthColor(attr.health));
    setBarVal('barMentality', 'valMentality', attr.mentality, 'var(--stamp)');
    setBarVal('barKnowledge', 'valKnowledge', attr.knowledge, 'var(--gold)');
    setBarVal('barFamily', 'valFamily', attr.family, 'var(--good)');

    // 资产与购买力换算
    const purchasing = calculatePurchasingPower(year, attr.wealth, age);
    document.getElementById('txtIncome').textContent = purchasing.annualIncome;
    document.getElementById('txtWealth').textContent = purchasing.netWorth;
    document.getElementById('txtPurchasing').textContent = purchasing.description;

    // 当地产业与时代信息
    const indProfile = char.industryPillar || '传统农业手工业';
    document.getElementById('macroIndustry').textContent = indProfile;
    document.getElementById('macroEra').textContent = `${era.name}（预期寿命基准 ${era.lifeExpectancy} 岁）`;
    document.getElementById('idJob').textContent = char.occupation || '平民';
  }

  function setBarVal(barId, txtId, val, color) {
    const bar = document.getElementById(barId);
    const txt = document.getElementById(txtId);
    const clampVal = Math.min(100, Math.max(0, Math.round(val)));
    if (bar) {
      bar.style.width = `${clampVal}%`;
      if (color) bar.style.background = color;
    }
    if (txt) txt.textContent = clampVal;
  }

  function getHealthColor(health) {
    if (health >= 55) return 'var(--good)';
    if (health >= 30) return 'var(--warn)';
    return 'var(--bad)';
  }

  // 纪事流渲染
  function appendFeedItem({ age, year, tag, tagClass, narrative }) {
    const feed = document.getElementById('lifeFeed');
    if (!feed) return;

    const li = document.createElement('li');
    li.innerHTML = `
      <div class="a">${age}岁<br><small style="color:var(--ink3)">${year}</small></div>
      <div class="x">
        ${tag ? `<span class="feed-tag ${tagClass || 'tag-era'}">${escapeHtml(tag)}</span>` : ''}
        <span>${escapeHtml(narrative)}</span>
      </div>
    `;

    feed.insertBefore(li, feed.firstChild);
  }

  // 单次回合演进
  function tickTurn() {
    if (engine.isGameOver) {
      handleGameOver();
      return;
    }

    const res = engine.advanceYear();
    if (!res) return;

    // 1. 死亡或圆满结束
    if (res.isGameOver) {
      updateVitalsUI();
      handleGameOver();
      return;
    }

    // 2. 触发人生关键抉择或至暗时刻 (暂停演进，呼出弹窗)
    if (res.isDecision) {
      pauseGame();
      updateVitalsUI();
      showDecisionModal(res);
      return;
    }

    // 3. 常规年份或自然灾害幸存
    const turn = res.turnRecord;
    let tag = null;
    let tagClass = 'tag-era';

    if (res.isDisasterAlert && res.disaster) {
      tag = `天灾浩劫 · ${res.disaster.name}`;
      tagClass = 'tag-disaster';
    } else if (turn.eventTitle) {
      tag = turn.eventTitle;
      tagClass = 'tag-choice';
    }

    appendFeedItem({
      age: turn.age,
      year: turn.year,
      tag,
      tagClass,
      narrative: turn.narrative
    });

    updateVitalsUI();
  }

  // =========================================================================
  // 抉择弹窗处理 (Decision Modal)
  // =========================================================================
  function showDecisionModal(res) {
    const evt = res.decisionData || res.event || res.decisionNode;
    if (!evt) return;

    const isDark = (evt.id === 'node_darkest_hour') || res.isDarkestHour;
    document.getElementById('decType').textContent = isDark ? '至暗时刻 · 精神救赎' : '关键人生抉择';
    document.getElementById('decMeta').textContent = `${engine.currentAge}岁 · ${engine.currentYear}年`;
    document.getElementById('decTitle').textContent = evt.title || '命运关卡';
    document.getElementById('decNarrative').textContent = evt.narrative || evt.description || '面临人生重大关口，你的决定将影响未来的轨迹。';

    const factEl = document.getElementById('decFact');
    const factText = evt.historicalFact || evt.fact;
    if (factText) {
      factEl.hidden = false;
      factEl.textContent = `历史背景：${factText}`;
    } else {
      factEl.hidden = true;
    }

    const choicesContainer = document.getElementById('decChoices');
    choicesContainer.innerHTML = '';

    const choices = evt.choices || [];
    choices.forEach((c, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      let tagsHtml = '';
      if (c.choiceTags && Array.isArray(c.choiceTags) && c.choiceTags.length > 0) {
        tagsHtml = `<div class="choice-tags-container">` +
          c.choiceTags.map(t => `<span class="choice-tag-pill">${escapeHtml(t)}</span>`).join('') +
          `</div>`;
      }
      btn.innerHTML = `<b>${escapeHtml(c.text)}</b>${c.desc ? `<small style="display:block;color:var(--ink3);margin-top:2px;">${escapeHtml(c.desc)}</small>` : ''}${tagsHtml}`;
      btn.addEventListener('click', () => {
        resolveChoice(evt.id, idx);
      });
      choicesContainer.appendChild(btn);
    });

    modalEl.hidden = false;
  }

  function resolveChoice(decisionId, choiceIndex) {
    modalEl.hidden = true;
    engine.resolveDecision(decisionId, choiceIndex);

    const lastHistory = engine.history[engine.history.length - 1];
    if (lastHistory) {
      appendFeedItem({
        age: lastHistory.age,
        year: lastHistory.year,
        tag: '抉择',
        tagClass: 'tag-choice',
        narrative: lastHistory.narrative
      });
    }

    updateVitalsUI();

    if (engine.isGameOver) {
      handleGameOver();
    } else if (!isPaused) {
      resumeGame();
    }
  }

  // =========================================================================
  // 终局死亡结算与生平全纪档案 (#dead)
  // =========================================================================
  function handleGameOver() {
    pauseGame();
    showSection(secDead);

    const char = engine.character;
    const death = engine.deathInfo || { age: engine.currentAge, year: engine.currentYear, cause: '安详离世' };
    const comp = engine.evaluateLifeResults();
    const era = engine.getEraForYear(char.birthYear);

    const isAlive2026 = death.isAliveIn2026 || death.year >= 2026;

    // 1. 证书核心信息 (严格区分在世与离世)
    if (isAlive2026) {
      document.getElementById('deadCertNo').textContent = `NO. 1937-2026-LIVE-${Math.floor(1000 + Math.random() * 9000)}`;
      document.getElementById('deadName').textContent = `${char.name} (${char.birthYear} — 2026 · 现年 ${death.age} 岁 · 在世)`;
      document.getElementById('deadCause').textContent = `当前状态：${death.cause}`;
      document.getElementById('deadCtx').textContent = `在 ${char.birthYear} 年同一年出生的中国人中，你健康平稳地行至2026年，继续见证日新月异的神州大地。当年同代人的平均预期寿命约为 ${era.lifeExpectancy} 岁。`;
      document.getElementById('dSumYears').textContent = `生于${char.birthPlace}${char.cityHistoricalName}，在时代洪流中奋进成长`;
    } else {
      document.getElementById('deadCertNo').textContent = `NO. 1937-2026-RIP-${Math.floor(1000 + Math.random() * 9000)}`;
      document.getElementById('deadName').textContent = `${char.name} (${char.birthYear} — ${death.year} · 享年 ${death.age} 岁)`;
      document.getElementById('deadCause').textContent = `死因：${death.cause}`;

      const diff = death.age - era.lifeExpectancy;
      const diffText = diff >= 0 ? `多活了 ${diff.toFixed(1)} 年` : `少活了 ${Math.abs(diff).toFixed(1)} 年`;
      document.getElementById('deadCtx').textContent = `在 ${char.birthYear} 年同一年出生的中国人中，约有 ${Math.max(1, 100 - comp.lifespan.percentile)}% 活得比你久。你比当年同代人的平均预期寿命（${era.lifeExpectancy} 岁）${diffText}。`;
      document.getElementById('dSumYears').textContent = `生于${char.birthPlace}${char.cityHistoricalName}，在近一个世纪的风云变迁中走完一生`;
    }

    // 2. 一生履历摘要
    document.getElementById('dSumEdu').textContent = comp.education.level;
    document.getElementById('dSumJob').textContent = char.occupation || '平民';
    document.getElementById('dSumFamily').textContent = `家庭亲缘指数 ${char.attributes.family} · 同胞兄弟姐妹 ${char.siblingsCount} 人`;
    document.getElementById('dSumWealth').textContent = comp.wealth.tier;

    const disasterStr = char.survivedDisasters && char.survivedDisasters.length > 0 ? char.survivedDisasters.join('、') : '一生未逢特大毁灭性浩劫';
    document.getElementById('dSumDisaster').textContent = disasterStr;

    // 3. 同代人排名
    document.getElementById('cmpLife').textContent = comp.lifespan.desc;
    document.getElementById('cmpEdu').textContent = comp.education.desc;
    document.getElementById('cmpWealth').textContent = comp.wealth.desc;

    // 4. 绘制 Canvas 生命轨迹图 (Lifeline Chart)
    drawLifelineChart(char.lifelineHistory, death.age);

    // 4.5 2026在世未完待续专栏渲染
    const continueSection = document.getElementById('continueSection');
    if (continueSection) {
      if (isAlive2026) {
        continueSection.hidden = false;
        const act = char.actuarialExpectancy || {};
        const ageEl = document.getElementById('contCurrentAge');
        const remEl = document.getElementById('contRemaining');
        const totEl = document.getElementById('contTotalAge');
        if (ageEl) ageEl.textContent = `${death.age} 岁`;
        if (remEl) remEl.textContent = act.remainingRange || '45–52 年';
        if (totEl) totEl.textContent = act.totalExpectedAgeRange || '78–85 岁';
      } else {
        continueSection.hidden = true;
      }
    }

    // 4.6 因果回顾专栏渲染 (蝴蝶效应)
    const causalitySection = document.getElementById('causalitySection');
    const causalityList = document.getElementById('causalityList');
    if (causalitySection && causalityList) {
      const reviews = char.causalityReview || [];
      if (reviews.length > 0) {
        causalitySection.hidden = false;
        causalityList.innerHTML = reviews.map(r => {
          let badgeClass = 'safe';
          let badgeLabel = '安然无恙';
          if (r.outcomeType === 'injured') { badgeClass = 'injured'; badgeLabel = '负伤受创'; }
          else if (r.outcomeType === 'entangled') { badgeClass = 'entangled'; badgeLabel = '受到牵连'; }
          else if (r.outcomeType === 'redirected') { badgeClass = 'redirected'; badgeLabel = '人生转向'; }
          else if (r.outcomeType === 'fatal') { badgeClass = 'fatal'; badgeLabel = '不幸罹难'; }

          return `
            <div class="causality-item">
              <div class="causality-meta">
                <span>${r.age}岁 · ${r.year}年 · ${escapeHtml(r.eventTitle || '关键关卡')}</span>
                <span class="badge-outcome ${badgeClass}">${badgeLabel}</span>
              </div>
              <div class="causality-choice">选择：${escapeHtml(r.choiceText || '')}</div>
              <div class="causality-risk">因果注脚：${escapeHtml(r.hiddenRisk || '')}</div>
            </div>
          `;
        }).join('');
      } else {
        causalitySection.hidden = true;
      }
    }

    // 5. 晚出生角色“传承视角”检测与渲染 (出生>=2010且2026年存活)
    const lineageSection = document.getElementById('lineageSection');
    const isLateBornSurvivor = char.birthYear >= 2010 && (death.isAliveIn2026 || death.year >= 2026);

    if (lineageSection) {
      if (isLateBornSurvivor) {
        const lineage = engine.generateLineageHistory(char);
        renderLineageView(lineage);
        lineageSection.hidden = false;
      } else {
        lineageSection.hidden = true;
      }
    }

    // 6. 渲染分享卡与文字总结
    let summaryText = '';
    if (isLateBornSurvivor) {
      summaryText = `【live · 14亿分之1】我在 1937–2026 中国历史模拟中化身为新时代少年「${char.name}」（${char.birthYear}年出生，现年 ${death.age} 岁）。出生于 ${char.birthPlace} · ${char.cityHistoricalName}，在父祖两代人近半个世纪的接力托举中平稳成长。来体验属于中国人真实历史的一生：https://wg2038.github.io/live/`;
    } else {
      summaryText = `【live · 14亿分之1】我在 1937–2026 中国历史模拟中化身为「${char.name}」（${char.birthYear}–${death.year}），享年 ${death.age} 岁。出生于 ${char.birthPlace} · ${char.cityHistoricalName}，因 ${death.cause} 离世。寿数超越同代 ${comp.lifespan.percentile}% 的人！来体验属于中国人真实历史的一生：https://wg2038.github.io/live/`;
    }
    document.getElementById('shareText').textContent = summaryText;

    renderShareCardPreview(char, death, comp, '');
  }

  // 渲染晚出生角色“传承视角”三代人对照
  function renderLineageView(lineage) {
    if (!lineage) return;
    const container = document.getElementById('lineageCards');
    if (!container) return;

    const gp = lineage.grandparent;
    const p = lineage.parent;
    const c = lineage.child;

    container.innerHTML = `
      <!-- 祖辈一代 -->
      <div class="gen-card">
        <div class="gen-title">
          <span>祖辈一代 · ${escapeHtml(gp.name)}（约 ${gp.birthYear} 年生）</span>
          <span class="tag">建国初与集体化一代</span>
        </div>
        <ul class="gen-timeline">
          ${gp.timeline.map(item => `
            <li class="gen-step">
              <span class="period">${escapeHtml(item.period)}</span>
              <b>${escapeHtml(item.stage)}</b>
              <span>${escapeHtml(item.detail)}</span>
            </li>
          `).join('')}
        </ul>
      </div>

      <!-- 父辈一代 -->
      <div class="gen-card">
        <div class="gen-title">
          <span>父辈一代 · ${escapeHtml(p.name)}（约 ${p.birthYear} 年生 · ${escapeHtml(p.job)}）</span>
          <span class="tag">改革开放与市场转轨托举一代</span>
        </div>
        <ul class="gen-timeline">
          ${p.timeline.map(item => `
            <li class="gen-step">
              <span class="period">${escapeHtml(item.period)}</span>
              <b>${escapeHtml(item.stage)}</b>
              <span>${escapeHtml(item.detail)}</span>
            </li>
          `).join('')}
        </ul>
      </div>

      <!-- 角色当代 -->
      <div class="gen-card" style="border-color: var(--stamp);">
        <div class="gen-title" style="color: var(--stamp);">
          <span>当代少年 · ${escapeHtml(c.name)}（${c.birthYear} 年生 · 现年 ${c.ageIn2026} 岁）</span>
          <span class="tag" style="background: var(--stamp); color: var(--paper);">移动互联与新时代一代</span>
        </div>
        <ul class="gen-timeline">
          ${c.timeline.map(item => `
            <li class="gen-step child-step">
              <span class="period">${escapeHtml(item.period)}</span>
              <b>${escapeHtml(item.stage)}</b>
              <span>${escapeHtml(item.detail)}</span>
            </li>
          `).join('')}
        </ul>
      </div>
    `;

    const btnReplayParent = document.getElementById('btnReplayParent');
    if (btnReplayParent && p && p.profile) {
      btnReplayParent.onclick = () => {
        engine.createCharacterFromParent(p.profile);
        showSection(secLifeview);
        initLifeviewUI();
        resumeGame();
      };
    }
  }

  // 绘制生命轨迹线图
  function drawLifelineChart(history, deathAge) {
    const canvas = document.getElementById('lifeMap');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    const w = 640;
    const h = 180;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = '100%';
    canvas.style.maxWidth = '640px';
    canvas.style.height = 'auto';
    ctx.scale(dpr, dpr);

    ctx.clearRect(0, 0, w, h);

    if (!history || history.length === 0) return;
    const pts = history.length === 1 ? [history[0], { ...history[0], age: Math.max(1, deathAge) }] : history;

    const padding = { top: 20, right: 30, bottom: 25, left: 35 };
    const chartW = w - padding.left - padding.right;
    const chartH = h - padding.top - padding.bottom;

    // 背景网格线
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--rule2').trim() || '#DCE4E1';
    ctx.lineWidth = 1;

    for (let r = 0; r <= 4; r++) {
      const y = padding.top + (chartH / 4) * r;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(w - padding.right, y);
      ctx.stroke();
    }

    // 坐标映射
    const maxAge = Math.max(80, deathAge);
    const getX = a => padding.left + (a / maxAge) * chartW;
    const getY = v => padding.top + chartH - (Math.min(100, Math.max(0, v)) / 100) * chartH;

    // 绘制健康曲线 (翡翠绿实线)
    ctx.beginPath();
    ctx.strokeStyle = '#0F6E68';
    ctx.lineWidth = 2.5;
    pts.forEach((pt, idx) => {
      const x = getX(pt.age);
      const y = getY(pt.health);
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // 绘制财富/生计曲线 (琥珀金虚线)
    ctx.beginPath();
    ctx.strokeStyle = '#9C7020';
    ctx.lineWidth = 1.8;
    ctx.setLineDash([4, 4]);
    pts.forEach((pt, idx) => {
      const x = getX(pt.age);
      const y = getY(pt.wealth);
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.setLineDash([]); // 还原实线

    // 横轴年龄刻度文字
    ctx.font = '11px "IBM Plex Mono", monospace';
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--ink3').trim() || '#5F6E72';
    ctx.textAlign = 'center';
    [0, 20, 40, 60, 80].forEach(a => {
      if (a <= maxAge) {
        ctx.fillText(`${a}岁`, getX(a), h - 8);
      }
    });
    ctx.fillText(`${deathAge}岁(终)`, getX(deathAge), h - 8);
  }

  // =========================================================================
  // Canvas 高清生平卡生成 (1:1 1in8b.life Editorial Share Card)
  // =========================================================================
  function renderShareCardPreview(char, death, comp, farewell) {
    const cardImg = document.getElementById('cardImg');
    const cardWait = document.getElementById('cardWait');
    if (!cardImg) return;

    const canvas = document.createElement('canvas');
    const w = 720;
    const h = 960;
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');

    // 1. 卡片底色 (Paper)
    ctx.fillStyle = '#F7FAF8';
    ctx.fillRect(0, 0, w, h);

    // 边框
    ctx.strokeStyle = '#C7D2CE';
    ctx.lineWidth = 2;
    ctx.strokeRect(16, 16, w - 32, h - 32);

    // 2. 顶部 Crimson 红色条标
    ctx.fillStyle = '#8C1D3C';
    ctx.fillRect(16, 16, w - 32, 56);

    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 20px "Noto Serif SC", serif';
    ctx.textAlign = 'left';
    ctx.fillText('live · 14亿分之1', 36, 52);

    ctx.font = '13px "IBM Plex Mono", monospace';
    ctx.textAlign = 'right';
    ctx.fillText(`NO. 1937-2026-CHRONICLE`, w - 36, 51);

    // 3. 人物大标题
    ctx.textAlign = 'left';
    ctx.fillStyle = '#13212A';
    ctx.font = 'bold 36px "Noto Serif SC", serif';
    ctx.fillText(char.name, 40, 126);

    const isSurvivor = death.isAliveIn2026 || death.year >= 2026;
    let subTitle;
    if (isSurvivor) {
      const ageLabel = death.age < 18 ? '岁少年' : '岁';
      subTitle = `${char.birthYear} — 2026 · 现年 ${death.age} ${ageLabel} (${char.sex} · ${char.ethnicity} · 在世)`;
    } else {
      subTitle = `${char.birthYear} — ${death.year} · 享年 ${death.age} 岁 (${char.sex} · ${char.ethnicity})`;
    }

    ctx.font = '16px "IBM Plex Mono", monospace';
    ctx.fillStyle = '#4A5A61';
    ctx.fillText(subTitle, 40, 156);

    // 4. 死因与生卒条框
    ctx.fillStyle = '#DCEDEA';
    ctx.fillRect(40, 180, w - 80, 48);
    ctx.fillStyle = '#0F6E68';
    ctx.font = 'bold 16px "Noto Serif SC", serif';
    const causeText = isSurvivor ? `当前状态：${death.cause}` : `死因：${death.cause}`;
    ctx.fillText(causeText, 56, 210);

    // 5. 出生与家门基准
    ctx.fillStyle = '#13212A';
    ctx.font = 'bold 16px "Noto Serif SC", serif';
    ctx.fillText('【 籍 贯 与 家 门 】', 40, 268);

    ctx.font = '15px "Noto Serif SC", serif';
    ctx.fillStyle = '#4A5A61';
    ctx.fillText(`出生地：${char.birthPlace} · ${char.cityHistoricalName}（${char.cityType}）`, 40, 300);
    ctx.fillText(`门第生计：${char.parentJob}（主导产业：${char.industryPillar}）`, 40, 328);
    ctx.fillText(`同胞兄弟姐妹：${char.siblingsCount} 人 · 最终文化水平：${comp.education.level}`, 40, 356);

    // 6. 统计百分位排名表格
    ctx.fillStyle = '#F0F4F2';
    ctx.fillRect(40, 388, w - 80, 136);
    ctx.strokeStyle = '#DCE4E1';
    ctx.strokeRect(40, 388, w - 80, 136);

    ctx.font = 'bold 15px "Noto Serif SC", serif';
    ctx.fillStyle = '#13212A';
    ctx.fillText('【 同 代 人 群 历 史 统 计 对 比 】', 56, 420);

    ctx.font = '14px "Noto Serif SC", serif';
    ctx.fillStyle = '#4A5A61';
    ctx.fillText(`• 寿命排位：${comp.lifespan.desc}`, 56, 450);
    ctx.fillText(`• 文化程度：${comp.education.desc}`, 56, 478);
    ctx.fillText(`• 家门财富：${comp.wealth.desc}`, 56, 506);

    // 7. 一生关键烙印与灾害
    ctx.fillStyle = '#13212A';
    ctx.font = 'bold 16px "Noto Serif SC", serif';
    ctx.fillText('【 一 生 关 键 烙 印 】', 40, 564);

    ctx.font = '14px "Noto Serif SC", serif';
    let my = 598;
    const topMilestones = char.milestones.slice(0, 4);
    topMilestones.forEach(m => {
      ctx.fillStyle = '#9C7020';
      ctx.fillText(`[${m.year}年 / ${m.age}岁]`, 40, my);
      ctx.fillStyle = '#13212A';
      const str = `${m.title}：${m.detail}`.slice(0, 34);
      ctx.fillText(str, 160, my);
      my += 30;
    });

    if (char.survivedDisasters && char.survivedDisasters.length > 0) {
      ctx.fillStyle = '#B0362B';
      ctx.fillText(`亲历天灾：曾九死一生幸存自 ${char.survivedDisasters.join('、')}`, 40, my);
      my += 30;
    }

    // 8. 留给这一生的话
    const defaultQuote = isSurvivor
      ? '三代人八十载寒暑接力，终见人间安宁与繁盛。'
      : '辛苦操劳了一生，在人间风雨里平平淡淡走过，无悔于世。';
    const quote = farewell || defaultQuote;
    ctx.fillStyle = '#DCEDEA';
    ctx.fillRect(40, 755, w - 80, 68);
    ctx.font = 'italic 15px "Noto Serif SC", serif';
    ctx.fillStyle = '#0F6E68';
    ctx.fillText(`“${quote}”`, 56, 796);

    // 9. 底部标识与水印
    ctx.textAlign = 'center';
    ctx.font = '12px "IBM Plex Mono", monospace';
    ctx.fillStyle = '#5F6E72';
    ctx.fillText('中国历史人生模拟器 · 基于全国31省149城真实统计与方志档案 · live.1in8b.life', w / 2, 876);
    ctx.fillText('https://wg2038.github.io/live/', w / 2, 898);

    const dataUrl = canvas.toDataURL('image/png');
    cardImg.src = dataUrl;
    cardImg.hidden = false;
    if (cardWait) cardWait.hidden = true;
  }

  // 追思馆留念提交
  const farewellBtn = document.getElementById('farewellBtn');
  const farewellInput = document.getElementById('farewellInput');

  if (farewellBtn && farewellInput) {
    farewellBtn.addEventListener('click', () => {
      const text = farewellInput.value.trim();
      const char = engine.character;
      const death = engine.deathInfo || { age: engine.currentAge, year: engine.currentYear, cause: '安详离世' };
      const comp = engine.evaluateLifeResults();

      // 保存至本地存储
      try {
        const list = JSON.parse(localStorage.getItem(MEMORIAL_STORAGE_KEY) || '[]');
        list.push({
          name: char.name,
          birthYear: char.birthYear,
          deathYear: death.year,
          age: death.age,
          place: `${char.birthPlace} ${char.cityHistoricalName}`,
          job: char.occupation || '平民',
          farewell: text || '平凡一生，踏实走过。'
        });
        localStorage.setItem(MEMORIAL_STORAGE_KEY, JSON.stringify(list));
        loadMemorialLives();
      } catch (e) {
        console.warn(e);
      }

      // 更新生平卡
      renderShareCardPreview(char, death, comp, text);
      alert('已成功留念在追思馆，并更新至生平档案卡！');
    });
  }

  // 下载生平卡片
  const cardDownloadBtn = document.getElementById('cardDownloadBtn');
  const cardPrevBtn = document.getElementById('cardPrevBtn');

  function downloadShareCard() {
    const cardImg = document.getElementById('cardImg');
    if (!cardImg || !cardImg.src) return;
    const a = document.createElement('a');
    a.download = `live_14亿分之1_${engine.character.name}_生平档案.png`;
    a.href = cardImg.src;
    a.click();
  }

  if (cardDownloadBtn) cardDownloadBtn.addEventListener('click', downloadShareCard);
  if (cardPrevBtn) cardPrevBtn.addEventListener('click', downloadShareCard);

  // 复制生平文字
  const copyShareBtn = document.getElementById('copyShareBtn');
  if (copyShareBtn) {
    copyShareBtn.addEventListener('click', () => {
      const text = document.getElementById('shareText').textContent;
      navigator.clipboard.writeText(text).then(() => {
        alert('生平总结文字已复制到剪贴板！');
      }).catch(() => {
        alert('复制失败，请手动长按文字复制。');
      });
    });
  }

  // 重开新人生
  const restartBtn = document.getElementById('restartBtn');
  if (restartBtn) {
    restartBtn.addEventListener('click', () => {
      showSection(secIntro);
    });
  }

  // =========================================================================
  // 辅助函数 (Helpers)
  // =========================================================================
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function getLunarYearName(year) {
    const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
    const branches = ['子鼠', '丑牛', '寅虎', '卯兔', '辰龙', '巳蛇', '午马', '未羊', '申猴', '酉鸡', '戌狗', '亥猪'];
    const offset = year - 4;
    const s = stems[(offset % 10 + 10) % 10];
    const b = branches[(offset % 12 + 12) % 12];
    return `${s}${b}年`;
  }

  function calculatePurchasingPower(year, wealthScore, age) {
    if (age < 15) {
      if (year <= 1949) {
        const silverYuan = Math.max(1, Math.round((wealthScore / 10) * 0.8));
        return {
          annualIncome: '无独立收入 (长辈供养)',
          netWorth: `家底约折合 ${silverYuan} 块大洋`,
          description: '未成年阶段，靠父母长辈劳作口粮抚育度日。'
        };
      }
      if (year <= 1978) {
        return {
          annualIncome: '¥ 0 (由长辈抚养)',
          netWorth: `家存储蓄约 ¥ ${Math.round(wealthScore * 6)} 元`,
          description: '未成年阶段，全凭父母工分粮票与微薄工资供给衣食。'
        };
      }
      if (year <= 1999) {
        return {
          annualIncome: '¥ 0 (由长辈抚养)',
          netWorth: `家境资产约 ¥ ${(wealthScore * 90).toLocaleString()} 元`,
          description: '求学成长期，衣食起居主要依赖家庭工薪与结余。'
        };
      }
      return {
        annualIncome: '¥ 0 (在读/抚养中)',
        netWorth: `家庭资产支持约 ¥ ${(wealthScore * 6000).toLocaleString()} 元`,
        description: '求学成长阶段，衣食学费由父母长辈全力支持。'
      };
    }

    if (year <= 1949) {
      const silverYuan = Math.round((wealthScore / 10) * 1.5);
      return {
        annualIncome: `约 ${Math.round(wealthScore * 0.8)} 银元/法币`,
        netWorth: `折合 ${silverYuan} 块大洋`,
        description: '战火与民国法币贬值，靠银元面粉或硬通货度日。'
      };
    }

    if (year <= 1978) {
      const wage = Math.round(28 + (wealthScore / 100) * 45);
      return {
        annualIncome: `¥ ${wage * 12} 元/年`,
        netWorth: `储蓄约 ¥ ${Math.round(wealthScore * 12)} 元`,
        description: '计划经济凭票购粮，国营八级工资制，猪肉约0.7元/斤。'
      };
    }

    if (year <= 1999) {
      const wage = Math.round(150 + (wealthScore / 100) * 850);
      return {
        annualIncome: `¥ ${(wage * 12).toLocaleString()} 元/年`,
        netWorth: `净资产 ¥ ${(wealthScore * 180).toLocaleString()} 元`,
        description: '市场经济转轨，万元户涌现，通胀与外贸浪潮并存。'
      };
    }

    // 2000-2026
    const wage = Math.round(2200 + (wealthScore / 100) * 14000);
    const asset = Math.round(wealthScore * 12000);
    return {
      annualIncome: `¥ ${(wage * 12).toLocaleString()} 元/年`,
      netWorth: `资产约 ¥ ${asset.toLocaleString()} 元`,
      description: '现代货币物价体系，覆盖房产、公积金与现代消费支出。'
    };
  }
});
