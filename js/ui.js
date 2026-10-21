/**
 * 中国出生模拟器 (China Birth Simulator) - UI 界面交互与视图渲染
 * 强化：区县级地名沿革显示、产业生计标签、自然灾难遇险告警、Canvas 分享卡
 */

document.addEventListener('DOMContentLoaded', async () => {
  const engine = new window.SimulationEngine();

  // DOM 元素引用
  const viewStart = document.getElementById('view-start');
  const viewGame = document.getElementById('view-game');
  const viewEnding = document.getElementById('view-ending');

  // 开局配置
  const paceButtons = document.querySelectorAll('.pace-btn');
  const paceDesc = document.getElementById('paceDesc');
  const btnStart = document.getElementById('btnStart');
  let selectedPace = 'medium';

  const paceDescriptions = {
    short: '极速一生：按童年、求学、择业、中年、晚年等 5-7 年大跨步跳跃，约 10-15 回合。',
    medium: '标准速读：每次前进 2-3 年，重点经历重大历史关卡与天灾转折，约 25-35 回合。',
    long: '沉浸逐年：按年步进（每次 1 年），详尽体验一生近百年的历史风霜，约 50-80 回合。'
  };

  // 角色档案卡
  const dossierName = document.getElementById('dossierName');
  const dossierBirth = document.getElementById('dossierBirth');
  const dossierPlace = document.getElementById('dossierPlace');
  const dossierClass = document.getElementById('dossierClass');
  const dossierSiblings = document.getElementById('dossierSiblings');

  const eraTickerName = document.getElementById('eraTickerName');
  const eraTickerYear = document.getElementById('eraTickerYear');

  const statHealth = document.getElementById('statHealth');
  const statWealth = document.getElementById('statWealth');
  const statKnowledge = document.getElementById('statKnowledge');
  const statFamily = document.getElementById('statFamily');
  const statMentality = document.getElementById('statMentality');

  const barHealth = document.getElementById('barHealth');
  const barWealth = document.getElementById('barWealth');
  const barKnowledge = document.getElementById('barKnowledge');
  const barFamily = document.getElementById('barFamily');
  const barMentality = document.getElementById('barMentality');

  const narrativeStream = document.getElementById('narrativeStream');

  // 精力滑块
  const sliderStudy = document.getElementById('sliderStudy');
  const sliderWork = document.getElementById('sliderWork');
  const sliderFamily = document.getElementById('sliderFamily');
  const sliderHealth = document.getElementById('sliderHealth');

  const valStudy = document.getElementById('valStudy');
  const valWork = document.getElementById('valWork');
  const valFamily = document.getElementById('valFamily');
  const valHealth = document.getElementById('valHealth');

  const btnResetEnergy = document.getElementById('btnResetEnergy');
  const btnAdvance = document.getElementById('btnAdvance');

  // 抉择弹窗
  const decisionModal = document.getElementById('decisionModal');
  const modalTitle = document.getElementById('modalTitle');
  const modalFact = document.getElementById('modalFact');
  const modalNarrative = document.getElementById('modalNarrative');
  const modalChoices = document.getElementById('modalChoices');

  // 结局界面
  const epitaphName = document.getElementById('epitaphName');
  const epitaphLifespan = document.getElementById('epitaphLifespan');
  const epitaphCause = document.getElementById('epitaphCause');

  const peerLifespanDesc = document.getElementById('peerLifespanDesc');
  const peerLifespanBar = document.getElementById('peerLifespanBar');
  const peerEduDesc = document.getElementById('peerEduDesc');
  const peerEduBar = document.getElementById('peerEduBar');
  const peerWealthDesc = document.getElementById('peerWealthDesc');
  const peerWealthBar = document.getElementById('peerWealthBar');

  const milestoneTimeline = document.getElementById('milestoneTimeline');

  // 追思馆
  const memorialInput = document.getElementById('memorialInput');
  const btnSubmitMemorial = document.getElementById('btnSubmitMemorial');
  const memorialList = document.getElementById('memorialList');

  // 分享卡片
  const shareModal = document.getElementById('shareModal');
  const btnOpenShare = document.getElementById('btnOpenShare');
  const btnCloseShare = document.getElementById('btnCloseShare');
  const btnDownloadShare = document.getElementById('btnDownloadShare');
  const shareCanvas = document.getElementById('shareCanvas');

  const btnRestart = document.getElementById('btnRestart');

  // 1. 初始化引擎加载多源数据库
  try {
    await engine.init();
    console.log('全国31省份、149地级市与特大自然灾害全息数据库加载完成！');
  } catch (err) {
    alert('历史数据初始化失败，请检查数据文件');
    return;
  }

  // 步长选项切换
  paceButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      paceButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedPace = btn.dataset.pace;
      paceDesc.textContent = paceDescriptions[selectedPace];
    });
  });

  // 开始新人生
  btnStart.addEventListener('click', () => {
    const char = engine.createCharacter(selectedPace);
    setupGameView(char);
    switchView('game');
  });

  function switchView(viewName) {
    viewStart.classList.remove('active');
    viewGame.classList.remove('active');
    viewEnding.classList.remove('active');

    if (viewName === 'start') viewStart.classList.add('active');
    if (viewName === 'game') viewGame.classList.add('active');
    if (viewName === 'ending') viewEnding.classList.add('active');
  }

  // 初始化游戏主面板信息
  function setupGameView(char) {
    dossierName.textContent = char.name;
    dossierBirth.textContent = `${char.birthYear}年 (${char.sex}·${char.ethnicity})`;
    
    // 显示省份 + 真实市县（若为设市前则带旧县名标注）
    const locationStr = `${char.birthPlace} · ${char.cityHistoricalName} (${char.urbanRural === 'urban' ? '城镇' : '乡村'})`;
    dossierPlace.textContent = locationStr;
    dossierClass.textContent = `${char.familyClass}`;
    dossierSiblings.textContent = `${char.siblingsCount} 人`;

    narrativeStream.innerHTML = '';
    const initialNarrative = document.createElement('div');
    initialNarrative.className = 'narrative-item latest';
    initialNarrative.innerHTML = `
      <div class="narrative-meta">
        <span>${char.birthYear} 年 (0 岁)</span>
        <span>诞生 · ${char.cityType}</span>
      </div>
      <div>你呱呱坠地于【${char.birthPlace} ${char.cityHistoricalName}】。当地产业底色为【${char.industryPillar}】，长辈靠【${char.parentJob}】勉强维持一家温饱。家中同辈兄弟姐妹${char.siblingsCount}人。人间的风雨与晴空，就此徐徐展开……</div>
    `;
    narrativeStream.appendChild(initialNarrative);

    resetEnergySliders();
    updateDashboard();
  }

  // 更新数值面板
  function updateDashboard() {
    const char = engine.character;
    const era = engine.getEraForYear(engine.currentYear);

    eraTickerName.textContent = era.name;
    eraTickerYear.textContent = `${engine.currentYear} 年 (${engine.currentAge} 岁)`;

    const attr = char.attributes;
    statHealth.textContent = attr.health;
    statWealth.textContent = attr.wealth;
    statKnowledge.textContent = attr.knowledge;
    statFamily.textContent = attr.family;
    statMentality.textContent = attr.mentality;

    barHealth.style.width = `${attr.health}%`;
    barHealth.style.backgroundColor = attr.health < 25 ? '#a33826' : '#8c3b31';
    barWealth.style.width = `${attr.wealth}%`;
    barKnowledge.style.width = `${attr.knowledge}%`;
    barFamily.style.width = `${attr.family}%`;
    barMentality.style.width = `${attr.mentality}%`;
  }

  // 精力滑块联动处理 (总和必须等于 100)
  function handleSliderChange(changedSource) {
    let s = parseInt(sliderStudy.value) || 0;
    let w = parseInt(sliderWork.value) || 0;
    let f = parseInt(sliderFamily.value) || 0;
    let h = parseInt(sliderHealth.value) || 0;

    let total = s + w + f + h;
    let diff = total - 100;

    if (diff !== 0) {
      const others = [
        { key: 's', val: s, set: v => { s = v; sliderStudy.value = v; } },
        { key: 'w', val: w, set: v => { w = v; sliderWork.value = v; } },
        { key: 'f', val: f, set: v => { f = v; sliderFamily.value = v; } },
        { key: 'h', val: h, set: v => { h = v; sliderHealth.value = v; } }
      ].filter(item => item.key !== changedSource);

      const otherSum = others.reduce((sum, item) => sum + item.val, 0);
      if (otherSum > 0) {
        others.forEach(item => {
          const deduction = Math.round((item.val / otherSum) * diff);
          item.set(Math.max(0, Math.min(100, item.val - deduction)));
        });
      }
    }

    valStudy.textContent = `${sliderStudy.value}%`;
    valWork.textContent = `${sliderWork.value}%`;
    valFamily.textContent = `${sliderFamily.value}%`;
    valHealth.textContent = `${sliderHealth.value}%`;

    engine.setEnergy(
      parseInt(sliderStudy.value),
      parseInt(sliderWork.value),
      parseInt(sliderFamily.value),
      parseInt(sliderHealth.value)
    );
  }

  sliderStudy.addEventListener('input', () => handleSliderChange('s'));
  sliderWork.addEventListener('input', () => handleSliderChange('w'));
  sliderFamily.addEventListener('input', () => handleSliderChange('f'));
  sliderHealth.addEventListener('input', () => handleSliderChange('h'));

  function resetEnergySliders() {
    sliderStudy.value = 25;
    sliderWork.value = 25;
    sliderFamily.value = 25;
    sliderHealth.value = 25;
    valStudy.textContent = '25%';
    valWork.textContent = '25%';
    valFamily.textContent = '25%';
    valHealth.textContent = '25%';
    engine.setEnergy(25, 25, 25, 25);
  }

  btnResetEnergy.addEventListener('click', resetEnergySliders);

  // 推进岁月按钮
  btnAdvance.addEventListener('click', () => {
    btnAdvance.disabled = true;
    const result = engine.advanceYear();
    btnAdvance.disabled = false;

    if (!result) return;

    if (result.isGameOver) {
      showEndingView();
      return;
    }

    if (result.isDecision) {
      showDecisionModal(result.decisionData);
      return;
    }

    // 正常或遭遇天灾警报回合
    if (result.turnRecord) {
      appendNarrativeRecord(result.turnRecord, result.isDisasterAlert);
      updateDashboard();
    }
  });

  // 在界面追加叙事段落 (支持天灾特别警示卡片)
  function appendNarrativeRecord(rec, isDisaster) {
    const prev = narrativeStream.querySelectorAll('.narrative-item');
    prev.forEach(p => p.classList.remove('latest'));

    const item = document.createElement('div');
    item.className = isDisaster ? 'narrative-item latest disaster-hit' : 'narrative-item latest';
    
    const tagColor = isDisaster ? '#b3241b' : 'var(--highlight-gold)';
    item.innerHTML = `
      <div class="narrative-meta" style="color:${tagColor};">
        <span>${rec.year} 年 (${rec.age} 岁)</span>
        <span>${rec.eventTitle || rec.eraName}</span>
      </div>
      <div>${rec.narrative}</div>
    `;
    narrativeStream.appendChild(item);
    narrativeStream.scrollTop = narrativeStream.scrollHeight;
  }

  // 弹出关键抉择对话框
  function showDecisionModal(decision) {
    decisionModal.classList.add('active');
    modalTitle.textContent = decision.title;
    
    if (decision.historicalFact) {
      modalFact.style.display = 'block';
      modalFact.textContent = `【史料背景】${decision.historicalFact}`;
    } else {
      modalFact.style.display = 'none';
    }

    modalNarrative.textContent = decision.narrative;
    modalChoices.innerHTML = '';

    decision.choices.forEach((c, idx) => {
      const btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.textContent = `${idx + 1}. ${c.text}`;
      btn.addEventListener('click', () => {
        decisionModal.classList.remove('active');
        engine.resolveDecision(decision.id, idx);
        
        const lastTurn = engine.history[engine.history.length - 1];
        if (lastTurn) {
          appendNarrativeRecord(lastTurn, false);
        }
        updateDashboard();

        if (engine.isGameOver) {
          showEndingView();
        }
      });
      modalChoices.appendChild(btn);
    });
  }

  // 结局页渲染
  function showEndingView() {
    switchView('ending');
    const char = engine.character;
    const death = engine.deathInfo;

    epitaphName.textContent = char.name;
    epitaphLifespan.textContent = `（${char.birthYear} — ${death.year}，享年 ${death.age} 岁）`;
    epitaphCause.textContent = death.cause;

    if (death.isDisaster) {
      epitaphCause.style.color = '#b3241b';
      epitaphCause.style.fontWeight = 'bold';
    } else {
      epitaphCause.style.color = 'var(--text-muted)';
      epitaphCause.style.fontWeight = 'normal';
    }

    // 同龄人对比
    const comparisons = engine.calculatePeerComparisons();
    peerLifespanDesc.textContent = `寿命：${comparisons.lifespan.desc}`;
    peerLifespanBar.style.width = `${comparisons.lifespan.percentile}%`;

    peerEduDesc.textContent = `文化：${comparisons.education.desc} (${comparisons.education.level})`;
    peerEduBar.style.width = `${comparisons.education.percentile}%`;

    peerWealthDesc.textContent = `家境：${comparisons.wealth.desc} (${comparisons.wealth.tier})`;
    peerWealthBar.style.width = `${comparisons.wealth.percentile}%`;

    // 渲染一生里程碑时间轴
    milestoneTimeline.innerHTML = '';
    char.milestones.forEach(m => {
      const div = document.createElement('div');
      div.className = 'timeline-item';
      div.innerHTML = `
        <div class="timeline-time">${m.year} 年 (${m.age} 岁) · ${m.title}</div>
        <div class="timeline-content">${m.detail}</div>
      `;
      milestoneTimeline.appendChild(div);
    });

    renderMemorialList();
  }

  // 追思馆交互
  btnSubmitMemorial.addEventListener('click', () => {
    const text = memorialInput.value.trim();
    if (!text) return;

    const char = engine.character;
    const item = {
      name: char.name,
      birthYear: char.birthYear,
      deathYear: engine.deathInfo.year,
      place: `${char.birthPlace}·${char.cityHistoricalName}`,
      text: text,
      date: new Date().toLocaleDateString('zh-CN')
    };

    const stored = JSON.parse(localStorage.getItem('china_sim_memorials') || '[]');
    stored.unshift(item);
    localStorage.setItem('china_sim_memorials', JSON.stringify(stored.slice(0, 50)));

    memorialInput.value = '';
    renderMemorialList();
  });

  function renderMemorialList() {
    const stored = JSON.parse(localStorage.getItem('china_sim_memorials') || '[]');
    memorialList.innerHTML = '';
    if (stored.length === 0) {
      memorialList.innerHTML = '<div style="color:#888; font-size:0.75rem;">暂无追思留言，写下第一句悼词吧。</div>';
      return;
    }

    stored.forEach(item => {
      const div = document.createElement('div');
      div.className = 'memorial-item';
      div.innerHTML = `
        <div><strong>悼念 ${item.name}</strong> (${item.place}，${item.birthYear}–${item.deathYear})：${item.text}</div>
        <div style="font-size:0.7rem; color:#888; text-align:right;">${item.date}</div>
      `;
      memorialList.appendChild(div);
    });
  }

  // 生成分享卡片 Canvas 绘制（含市县生平与天灾亲历）
  function generateShareCard() {
    const ctx = shareCanvas.getContext('2d');
    const char = engine.character;
    const death = engine.deathInfo;
    const comp = engine.calculatePeerComparisons();

    const w = 600;
    const h = 880;
    shareCanvas.width = w;
    shareCanvas.height = h;

    // 1. 复古宣纸底色
    ctx.fillStyle = '#f5ede0';
    ctx.fillRect(0, 0, w, h);

    // 2. 双重古典边框
    ctx.strokeStyle = '#8a7764';
    ctx.lineWidth = 3;
    ctx.strokeRect(18, 18, w - 36, h - 36);
    ctx.strokeStyle = '#bbaea0';
    ctx.lineWidth = 1;
    ctx.strokeRect(24, 24, w - 48, h - 48);

    // 3. 顶部印章与报头
    ctx.fillStyle = '#a33826';
    ctx.font = 'bold 15px "Noto Serif SC", serif';
    ctx.fillText('【 中 华 纪 事 档 案 】', 215, 65);

    ctx.fillStyle = '#2b2520';
    ctx.font = 'bold 30px "Noto Serif SC", serif';
    ctx.textAlign = 'center';
    ctx.fillText('live · 人 间 一 瞬', w / 2, 108);

    ctx.font = '13.5px "Noto Serif SC", serif';
    ctx.fillStyle = '#6e6459';
    ctx.fillText('中国出生模拟器（1937 — 2026）· 致敬在时代巨浪中生息跋涉的平凡个体', w / 2, 138);

    ctx.strokeStyle = '#8a7764';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(40, 155);
    ctx.lineTo(w - 40, 155);
    ctx.stroke();

    // 4. 人物核心生平
    ctx.textAlign = 'left';
    ctx.font = 'bold 21px "Noto Serif SC", serif';
    ctx.fillStyle = '#2b2520';
    ctx.fillText(`人物生平：${char.name}（${char.sex}·${char.ethnicity}）`, 50, 195);

    ctx.font = '14.5px "Noto Serif SC", serif';
    ctx.fillStyle = '#443b34';
    ctx.fillText(`生卒年岁：${char.birthYear} 年 — ${death.year} 年（享年 ${death.age} 岁）`, 50, 226);
    ctx.fillText(`出生籍贯：${char.birthPlace} · ${char.cityHistoricalName}（${char.cityType}）`, 50, 254);
    ctx.fillText(`家门生计：${char.parentJob}（${char.industryPillar}）`, 50, 282);
    
    // 若死于天灾，高亮提示
    if (death.isDisaster) {
      ctx.fillStyle = '#a33826';
      ctx.fillText(`人生终局：${death.cause} ⚠️`, 50, 310);
    } else {
      ctx.fillStyle = '#443b34';
      ctx.fillText(`人生终局：${death.cause}`, 50, 310);
    }

    // 5. 亲历天灾印记 (若有)
    if (char.survivedDisasters && char.survivedDisasters.length > 0) {
      ctx.fillStyle = '#8c3b31';
      ctx.font = 'italic 13px "Noto Serif SC", serif';
      ctx.fillText(`历劫烙印：一生曾亲历 ${char.survivedDisasters.join('、')} 等特大天灾并顽强幸存`, 50, 338);
    }

    // 6. 同龄人宏观位置对比框
    ctx.fillStyle = '#ede3d1';
    ctx.fillRect(45, 360, w - 90, 130);
    ctx.strokeStyle = '#d0c3b0';
    ctx.strokeRect(45, 360, w - 90, 130);

    ctx.font = 'bold 15px "Noto Serif SC", serif';
    ctx.fillStyle = '#2c4953';
    ctx.fillText('【 同 代 人 群 统 计 估 算 对 比 】', 60, 388);

    ctx.font = '13px "Noto Serif SC", serif';
    ctx.fillStyle = '#3a332d';
    ctx.fillText(`• ${comp.lifespan.desc}`, 60, 416);
    ctx.fillText(`• ${comp.education.desc}`, 60, 444);
    ctx.fillText(`• ${comp.wealth.desc}`, 60, 471);

    // 7. 一生关键历史里程碑摘要 (精选 5 条)
    ctx.font = 'bold 16px "Noto Serif SC", serif';
    ctx.fillStyle = '#2b2520';
    ctx.fillText('【 一 生 关 键 烙 印 】', 50, 525);

    ctx.font = '13.5px "Noto Serif SC", serif';
    let yOffset = 558;
    const displayMilestones = char.milestones.slice(0, 5);
    displayMilestones.forEach(m => {
      ctx.fillStyle = '#967039';
      ctx.fillText(`[${m.year}年 / ${m.age}岁]`, 50, yOffset);
      ctx.fillStyle = '#2b2520';
      const detailStr = `${m.title}：${m.detail}`.slice(0, 31);
      ctx.fillText(detailStr, 160, yOffset);
      yOffset += 31;
    });

    // 8. 仿真印章
    ctx.save();
    ctx.translate(480, 770);
    ctx.rotate(-0.08);
    ctx.strokeStyle = '#a33826';
    ctx.lineWidth = 2.5;
    ctx.strokeRect(-40, -25, 80, 50);
    ctx.font = 'bold 14px "Noto Serif SC", serif';
    ctx.fillStyle = '#a33826';
    ctx.textAlign = 'center';
    ctx.fillText('人间一瞬', 0, -2);
    ctx.fillText('如实纪存', 0, 18);
    ctx.restore();

    // 9. 免责与时代水印
    ctx.textAlign = 'center';
    ctx.font = '11px "Noto Serif SC", serif';
    ctx.fillStyle = '#8c7e70';
    ctx.fillText('本数据为基于国家历史统计年鉴与方志资料的简化模拟，仅供体味人生，不代表真实个体。', w / 2, 835);
  }

  btnOpenShare.addEventListener('click', () => {
    generateShareCard();
    shareModal.classList.add('active');
  });

  btnCloseShare.addEventListener('click', () => {
    shareModal.classList.remove('active');
  });

  btnDownloadShare.addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = `live_人间一瞬_${engine.character.name}_生平档案.png`;
    link.href = shareCanvas.toDataURL('image/png');
    link.click();
  });

  btnRestart.addEventListener('click', () => {
    switchView('start');
  });
});
