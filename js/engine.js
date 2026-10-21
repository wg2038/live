/**
 * 中国出生模拟器 (China Birth Simulator) - 全息历史与灾难城市级引擎
 * 模拟 1937-2026 年全国 31 省区市、333个地级市与特色县级市演变、特大自然灾害命中与年代人名体系
 */

class SimulationEngine {
  constructor() {
    this.provinces = [];
    this.stats = null;
    this.events = [];
    this.cities = [];
    this.disasters = [];
    this.naming = null;
    this.isLoaded = false;

    // 当前角色状态
    this.character = null;
    this.history = [];
    this.currentYear = 1937;
    this.currentAge = 0;
    this.paceMode = 'medium'; // 'short', 'medium', 'long'
    this.isGameOver = false;
    this.deathInfo = null;

    // 当年精力分配 (总和 100)
    this.energy = {
      study: 25,
      work: 25,
      family: 25,
      health: 25
    };

    // 状态标记
    this.statusFlags = new Set();
  }

  /**
   * 初始化并加载全部数据（支持本地 fetch，并在跨域限制时平滑采用 embedded 回退）
   */
  async init() {
    try {
      const [provRes, statRes, evtRes, cityRes, disRes, nameRes] = await Promise.all([
        fetch('data/province.json'),
        fetch('data/stats.json'),
        fetch('data/events.json'),
        fetch('data/cities.json'),
        fetch('data/disasters.json'),
        fetch('data/naming.json')
      ]);
      this.provinces = await provRes.json();
      this.stats = await statRes.json();
      this.events = await evtRes.json();
      this.cities = await cityRes.json();
      this.disasters = await disRes.json();
      this.naming = await nameRes.json();
      this.isLoaded = true;
    } catch (err) {
      console.warn('Fetch 失败（可能由于本地 file:// 协议），采用内置回退数据', err);
      if (window.EMBEDDED_DATA) {
        this.provinces = window.EMBEDDED_DATA.provinces;
        this.stats = window.EMBEDDED_DATA.stats;
        this.events = window.EMBEDDED_DATA.events;
        this.cities = window.EMBEDDED_DATA.cities;
        this.disasters = window.EMBEDDED_DATA.disasters;
        this.naming = window.EMBEDDED_DATA.naming;
        this.isLoaded = true;
      } else {
        throw new Error('无法加载历史与城市数据库');
      }
    }
  }

  /**
   * 根据年份获取对应的宏观历史时期配置
   */
  getEraForYear(year) {
    const found = this.stats.eras.find(e => year >= e.startYear && year <= e.endYear);
    return found || this.stats.eras[this.stats.eras.length - 1];
  }

  /**
   * 获取工业演变时期 Key (四大时期)
   */
  getIndustryEraKey(year) {
    if (year <= 1949) return 'era_1937_1949';
    if (year <= 1978) return 'era_1950_1978';
    if (year <= 2000) return 'era_1979_2000';
    return 'era_2001_2026';
  }

  /**
   * 按出生年代与地域族群生成血肉人名
   */
  generateAuthenticName(birthYear, sex, provinceId, ethnicity) {
    // 1. 抽取姓氏（人口加权）
    const surnames = this.naming.surnames;
    const totalSWeight = surnames.reduce((sum, s) => sum + s.weight, 0);
    let sRand = Math.random() * totalSWeight;
    let surname = surnames[0].name;
    for (const s of surnames) {
      if (sRand < s.weight) {
        surname = s.name;
        break;
      }
      sRand -= s.weight;
    }

    // 2. 特殊少数民族命名覆盖
    if (ethnicity && ethnicity !== '汉族') {
      const ethMap = {
        '藏族': 'tibetan',
        '维吾尔族': 'uyghur',
        '蒙古族': 'mongolian'
      };
      const ethKey = ethMap[ethnicity];
      if (ethKey && this.naming.regionalNuances.ethnic[ethKey]) {
        const pool = sex === '男' ? this.naming.regionalNuances.ethnic[ethKey].male : this.naming.regionalNuances.ethnic[ethKey].female;
        return pool[Math.floor(Math.random() * pool.length)];
      }
    }

    // 3. 岭南特色姓名加权（广东/广西）
    if ((provinceId === 'guangdong' || provinceId === 'guangxi') && Math.random() < 0.35) {
      const pool = sex === '男' ? this.naming.regionalNuances.guangdong.male : this.naming.regionalNuances.guangdong.female;
      return `${surname}${pool[Math.floor(Math.random() * pool.length)]}`;
    }

    // 4. 东北特色质朴姓名加权
    if (['liaoning', 'jilin', 'heilongjiang'].includes(provinceId) && birthYear <= 1980 && Math.random() < 0.25) {
      const pool = sex === '男' ? this.naming.regionalNuances.northeast.male : this.naming.regionalNuances.northeast.female;
      return `${surname}${pool[Math.floor(Math.random() * pool.length)]}`;
    }

    // 5. 按五大历史代际精准取名
    let eraKey = '1937_1949';
    if (birthYear >= 1950 && birthYear <= 1965) eraKey = '1950_1965';
    else if (birthYear >= 1966 && birthYear <= 1976) eraKey = '1966_1976';
    else if (birthYear >= 1977 && birthYear <= 1999) eraKey = '1977_1999';
    else if (birthYear >= 2000) eraKey = '2000_2026';

    const eraNaming = this.naming.eras[eraKey];
    const givenPool = sex === '男' ? eraNaming.male : eraNaming.female;
    const givenName = givenPool[Math.floor(Math.random() * givenPool.length)];

    return `${surname}${givenName}`;
  }

  /**
   * 按照历史真实出生人口加权抽取出生年份
   */
  sampleBirthYear() {
    const cohorts = this.stats.birthCohorts;
    const totalWeight = cohorts.reduce((acc, c) => acc + c.weight, 0);
    let rand = Math.random() * totalWeight;
    let selectedCohort = cohorts[0];

    for (const c of cohorts) {
      if (rand < c.weight) {
        selectedCohort = c;
        break;
      }
      rand -= c.weight;
    }

    const [start, end] = selectedCohort.range;
    return Math.floor(start + Math.random() * (end - start + 1));
  }

  /**
   * 加权抽取省份
   */
  sampleProvince() {
    const total = this.provinces.reduce((sum, p) => sum + p.popWeight, 0);
    let rand = Math.random() * total;
    for (const p of this.provinces) {
      if (rand < p.popWeight) return p;
      rand -= p.popWeight;
    }
    return this.provinces[0];
  }

  /**
   * 在省内加权抽取地级市或特色县级市
   */
  sampleCityInProvince(provinceId) {
    const provinceCities = this.cities.filter(c => c.provinceId === provinceId);
    if (!provinceCities || provinceCities.length === 0) {
      return this.cities[0];
    }
    const totalWeight = provinceCities.reduce((sum, c) => sum + (c.popWeight || 1), 0);
    let rand = Math.random() * totalWeight;
    for (const c of provinceCities) {
      if (rand < (c.popWeight || 1)) return c;
      rand -= (c.popWeight || 1);
    }
    return provinceCities[0];
  }

  /**
   * 动态解析城市在当年的历史称谓（如1940年深圳显示为宝安县）
   */
  resolveCityDisplay(city, year) {
    if (year < city.foundingYear && city.historicalNamePre) {
      return {
        displayName: city.historicalNamePre,
        isPre: true,
        officialName: city.name,
        foundingYear: city.foundingYear
      };
    }
    return {
      displayName: city.name,
      isPre: false,
      officialName: city.name,
      foundingYear: city.foundingYear
    };
  }

  /**
   * 创建新角色（开局玩家无法选择出身）
   */
  createCharacter(paceMode = 'medium') {
    this.paceMode = paceMode;
    this.history = [];
    this.statusFlags.clear();
    this.isGameOver = false;
    this.deathInfo = null;

    // 1. 出生年份
    const birthYear = this.sampleBirthYear();
    const era = this.getEraForYear(birthYear);
    const indEraKey = this.getIndustryEraKey(birthYear);

    // 2. 出生省份与城市/区县
    const province = this.sampleProvince();
    const city = this.sampleCityInProvince(province.id);
    const cityDisplay = this.resolveCityDisplay(city, birthYear);

    // 3. 城乡判定（结合宏观时期与省份基准）
    const effectiveUrbanRatio = Math.min(95, Math.max(5, era.urbanRatio * (province.urbanRatioBaseline || 1.0)));
    const isUrban = (Math.random() * 100) < effectiveUrbanRatio;
    const urbanRural = isUrban ? 'urban' : 'rural';

    // 4. 性别与民族
    const sex = Math.random() < 0.515 ? '男' : '女';
    const isMinority = Math.random() < 0.085;
    const minorityNames = ['回族', '满族', '蒙古族', '藏族', '维吾尔族', '苗族', '彝族', '壮族', '土家族'];
    const ethnicity = isMinority ? minorityNames[Math.floor(Math.random() * minorityNames.length)] : '汉族';

    // 5. 抓取该城市当期的具体产业结构与父母职业！
    const indProfile = city.eraIndustries[indEraKey] || city.eraIndustries['era_1950_1978'];
    const typicalJobs = indProfile.typicalJobs || ['农田社员'];
    const parentJob = typicalJobs[Math.floor(Math.random() * typicalJobs.length)];
    const familyClass = `${city.type} · ${parentJob}`;

    // 6. 家庭经济水平
    const econRoll = Math.random() * 100;
    let economicLevel = '温饱';
    let initWealth = 40;
    if (city.type === '贫瘠特困型') {
      economicLevel = '贫困';
      initWealth = 15;
    } else if (econRoll < 28) {
      economicLevel = '贫困';
      initWealth = 20;
    } else if (econRoll < 80) {
      economicLevel = '温饱';
      initWealth = 40;
    } else if (econRoll < 96) {
      economicLevel = '小康';
      initWealth = 60;
    } else {
      economicLevel = '富裕';
      initWealth = 75;
    }

    // 7. 兄弟姐妹数
    const baseSiblings = era.avgSiblings;
    const siblingVariance = (Math.random() - 0.5) * 2;
    const siblingsCount = Math.max(0, Math.round(baseSiblings + siblingVariance));

    // 8. 角色核心五维属性 (0 - 100)
    const attributes = {
      health: Math.min(95, Math.max(40, Math.round(75 + (initWealth - 40) * 0.3 + (Math.random() * 10 - 5)))),
      wealth: initWealth,
      knowledge: Math.min(80, Math.max(10, Math.round(20 + (isUrban ? 10 : 0) + (Math.random() * 10)))),
      family: Math.round(70 + (Math.random() * 15 - 7)),
      mentality: Math.round(70 + (Math.random() * 10 - 5))
    };

    // 9. 智能历史人名生成
    const name = this.generateAuthenticName(birthYear, sex, province.id, ethnicity);

    this.character = {
      name,
      sex,
      ethnicity,
      birthYear,
      birthPlace: province.name,
      provinceId: province.id,
      cityId: city.id,
      cityName: city.name,
      cityHistoricalName: cityDisplay.displayName,
      cityType: city.type,
      cityFoundingYear: city.foundingYear,
      region: province.region,
      urbanRural,
      familyClass,
      parentJob,
      industryPillar: indProfile.pillar,
      economicLevel,
      siblingsCount,
      attributes,
      educationLevel: '未入学',
      occupation: isUrban ? '城镇孩童' : '乡野幼童',
      milestones: [],
      survivedDisasters: []
    };

    this.currentYear = birthYear;
    this.currentAge = 0;

    // 默认精力分配
    this.energy = {
      study: 20,
      work: 10,
      family: 35,
      health: 35
    };

    // 记录出生里程碑
    const birthIntro = `降生于${province.name}${cityDisplay.displayName}。其时地属【${city.type}】，当地主导生计为【${indProfile.pillar}】，父亲/长辈靠【${parentJob}】拉扯家门，家中有同辈兄弟姐妹${siblingsCount}人。`;
    this.character.milestones.push({
      year: birthYear,
      age: 0,
      title: '诞生于世',
      detail: birthIntro
    });

    return this.character;
  }

  /**
   * 设定精力分配（保证总和 100）
   */
  setEnergy(study, work, family, health) {
    let total = study + work + family + health;
    if (total <= 0) total = 100;
    this.energy = {
      study: Math.round((study / total) * 100),
      work: Math.round((work / total) * 100),
      family: Math.round((family / total) * 100),
      health: Math.round((health / total) * 100)
    };
  }

  /**
   * 计算步长（根据游戏时长选项）
   */
  getStepYears() {
    if (this.paceMode === 'long') return 1;
    if (this.paceMode === 'short') {
      if (this.currentAge < 16) return 4;
      if (this.currentAge < 55) return 6;
      return 5;
    }
    // medium
    if (this.currentAge < 18) return 2;
    if (this.currentAge < 60) return 3;
    return 2;
  }

  /**
   * 自然灾害碰撞命中引擎（当年 × 地域经纬匹配）
   */
  checkNaturalDisaster() {
    for (const dis of this.disasters) {
      if (this.statusFlags.has(`disaster_done_${dis.id}`)) continue;

      // 年份窗口吻合
      if (this.currentYear !== dis.year) continue;

      // 判定城市或省份是否命中震中/泛滥重灾区
      const hitCity = dis.targetCities && dis.targetCities.includes(this.character.cityId);
      const hitProvince = dis.targetProvinces && dis.targetProvinces.includes(this.character.provinceId);

      if (hitCity || hitProvince) {
        this.statusFlags.add(`disaster_done_${dis.id}`);

        // 城市直接在震中/溃坝名单中，遭击中概率倍增
        const severityMultiplier = hitCity ? 1.0 : 0.6;
        const rolls = dis.casualtyRoll;

        const isKilled = Math.random() < (rolls.deathProb * severityMultiplier);
        const isInjured = !isKilled && (Math.random() < (rolls.injuryProb * severityMultiplier));
        const isFamilyLost = Math.random() < (rolls.familyLossProb * severityMultiplier);
        const isWealthWiped = Math.random() < (rolls.wealthWipeProb * severityMultiplier);

        return {
          disaster: dis,
          isKilled,
          isInjured,
          isFamilyLost,
          isWealthWiped,
          isHit: true
        };
      }
    }
    return null;
  }

  /**
   * 检查当年是否有待触发的历史大事件
   */
  findEligibleEvents() {
    const list = [];
    for (const evt of this.events) {
      if (this.statusFlags.has(`done_${evt.id}`)) continue;

      const [start, end] = evt.yearRange;
      if (this.currentYear < start || this.currentYear > end) continue;

      if (evt.targetAge) {
        const [minAge, maxAge] = evt.targetAge;
        if (this.currentAge < minAge || this.currentAge > maxAge) continue;
      }

      if (evt.urbanRural && evt.urbanRural !== 'all' && evt.urbanRural !== this.character.urbanRural) {
        continue;
      }

      if (evt.applicableRegions && !evt.applicableRegions.includes('ALL')) {
        if (!evt.applicableRegions.includes(this.character.region)) continue;
      }

      list.push(evt);
    }
    return list;
  }

  /**
   * 人生固定重要抉择节点
   */
  checkLifeMilestone() {
    const age = this.currentAge;

    // 1. 启蒙上学 (6-8岁)
    if (age >= 6 && age <= 8 && !this.statusFlags.has('decision_school')) {
      this.statusFlags.add('decision_school');
      return {
        id: 'node_school',
        title: '适龄读书与做工抉择',
        isDecision: true,
        narrative: `你已到学龄，本地学堂传来朗朗书声。但家里${this.character.cityType}生计吃紧，长辈为书本与工分发愁，这决定了你一生的文化底子。`,
        choices: [
          {
            text: '克服困难坚持上学读书',
            effect: { "knowledge": 25, "wealth": -10, "health": 5 },
            log: '在贫瘠与困顿中坚持念书，背着用粗布缝合的书包迈进学堂。'
          },
          {
            text: '早早辍学务农或当学徒做工',
            effect: { "wealth": 15, "family": 15, "knowledge": -10 },
            log: `懂事地辍学帮衬家门，在${this.character.industryPillar}的尘土中流下第一滴汗水。`
          }
        ]
      };
    }

    // 2. 青年婚育抉择 (21-25岁)
    if (age >= 21 && age <= 25 && !this.statusFlags.has('decision_marriage')) {
      this.statusFlags.add('decision_marriage');
      return {
        id: 'node_marriage',
        title: '成家立业关口',
        isDecision: true,
        narrative: `行至青年成家关口，媒人提亲或与心仪之人相知提上了日程。需置办聘礼家具，这是人生的一大转折点。`,
        choices: [
          {
            text: '依照习俗顺理成章成家完婚',
            effect: { "family": 25, "wealth": -15, "mentality": 10 },
            log: '按当年规制办了喜酒成家立业，夫妻相濡以沫操持生计。'
          },
          {
            text: '推迟婚期，专心打拼本职或求学',
            effect: { "knowledge": 15, "wealth": 15, "family": -10 },
            log: '暂缓个人婚事，把满腔热忱投入到本职工作与打拼当中。'
          }
        ]
      };
    }

    // 3. 中年大病求医抉择 (45-65岁，若健康较低)
    if (age >= 48 && age <= 65 && this.character.attributes.health < 45 && !this.statusFlags.has('decision_medical')) {
      this.statusFlags.add('decision_medical');
      return {
        id: 'node_medical',
        title: '顽疾缠身与就医抉择',
        isDecision: true,
        narrative: `常年劳累积下重病，近来胸闷咳喘剧烈。大夫建议住院系统检查治疗，但这需要动用家中全部积蓄。`,
        choices: [
          {
            text: '动用全部积蓄积极住院治疗',
            effect: { "health": 25, "wealth": -30, "mentality": 10 },
            log: '四处借钱并动用积蓄积极就医，病情得以控制稳定。'
          },
          {
            text: '抓草药硬扛，把钱留给儿女开销',
            effect: { "health": -20, "family": 15, "wealth": 5 },
            log: '不忍拖累家人选择硬撑苦挨，身体逐渐落下严重宿疾。'
          }
        ]
      };
    }

    // 4. 人生至暗时刻抉择 (成年后心态极低且财富极低，处于破产与绝望边缘)
    if (age >= 20 && this.character.attributes.mentality < 22 && this.character.attributes.wealth < 20 && !this.statusFlags.has('decision_darkest_hour')) {
      this.statusFlags.add('decision_darkest_hour');
      return {
        id: 'node_darkest_hour',
        title: '人生至暗时刻：深渊边缘的寒夜',
        isDecision: true,
        historicalFact: '生活中总有些绝境，万念俱灰的重压几乎要将人彻底碾碎。这是人性的深渊，也是尊严、责任与执念的最后拷问。',
        narrative: '催债的电话在静音震动中闪烁不休，门缝里塞满了红色的律师函与催缴单。深冬的寒风呼呼灌进毛坯房的窗洞，你在桥头长椅上枯坐了整整一夜，烟头散落一地。前半生的心血与尊严碎成齑粉，桥下冰冷的黑水在夜色中泛着刺骨幽光。',
        choices: [
          {
            text: '万念俱灰，松开栏杆走入冰冷黑夜（绝境弃生）',
            effect: { "health": -100 },
            isSuicide: true,
            log: '心力枯竭，在无尽的黑暗与深渊面前永远闭上了双眼。'
          },
          {
            text: '嚼碎屈辱，哪怕去扛大包、跑夜班外卖也要替家人还债（负重苟活）',
            effect: { "health": -25, "wealth": 10 },
            isStoicSurvival: true,
            log: '在桥头痛哭一场后咬碎牙关擦干眼泪，哪怕脱掉长衫出尽苦力，也要替家门把债还清。'
          },
          {
            text: '推开破旧老屋柴门，父母的一碗热汤将自己从悬崖边缘硬生生拉回（至亲救赎）',
            effect: { "family": 20, "mentality": 35 },
            isFamilyRedeem: true,
            log: '在老母亲颤抖递来的一碗热汤面面前抱头痛哭，认栽还乡，在亲情庇护下捡回一条命。'
          }
        ]
      };
    }

    return null;
  }

  /**
   * 计算角色当年的真实死亡概率（真实时代基准 + 产业职业病风险 + 精力护体）
   */
  calculateAnnualMortalityRate(era) {
    const age = this.currentAge;
    let baseRate = 0.005;

    // 1. 婴儿脆弱期（基于各时期婴儿死亡率）
    if (age <= 1) {
      baseRate = era.infantMortality / 1000.0;
    } else if (age < 10) {
      baseRate = 0.015;
    } else if (age < 30) {
      baseRate = 0.006;
    } else if (age < 50) {
      baseRate = 0.015;
    } else if (age < 65) {
      baseRate = 0.035;
    } else if (age < 75) {
      baseRate = 0.07;
    } else if (age < 85) {
      baseRate = 0.15;
    } else {
      baseRate = 0.28;
    }

    // 2. 健康属性指数调节
    const health = this.character.attributes.health;
    let healthFactor = 1.0;
    if (health <= 0) return 1.0;
    if (health < 20) healthFactor = 4.5;
    else if (health < 40) healthFactor = 2.2;
    else if (health < 60) healthFactor = 1.2;
    else if (health > 80) healthFactor = 0.6;

    // 3. 玩家“健康/休养”精力分配抵御调节
    const healthEnergyBonus = 1.0 - (this.energy.health / 100) * 0.45;

    // 4. 城市产业特定职业病与污染风险 (如石棉、煤矿尘肺)
    let industryRiskBonus = 1.0;
    const city = this.cities.find(c => c.id === this.character.cityId);
    if (city && city.riskModifiers) {
      if (city.riskModifiers.dustDisease && age >= 35) {
        industryRiskBonus *= city.riskModifiers.dustDisease;
      }
      if (this.currentYear >= 1959 && this.currentYear <= 1961 && city.riskModifiers.famine1959) {
        industryRiskBonus *= city.riskModifiers.famine1959;
      }
      // 2022-2023 冬春转段对高龄基础病老人的考验
      if ((this.currentYear === 2022 || this.currentYear === 2023) && age >= 72 && health < 45) {
        industryRiskBonus *= 1.35;
      }
    }

    return Math.min(0.95, baseRate * healthFactor * healthEnergyBonus * industryRiskBonus);
  }

  /**
   * 应用精力分配对属性的年度修正
   */
  applyEnergyEffects(stepYears) {
    const attr = this.character.attributes;

    // 学业分配
    if (this.currentAge < 25) {
      attr.knowledge += Math.round((this.energy.study / 10) * stepYears * 1.2);
    } else {
      attr.knowledge += Math.round((this.energy.study / 20) * stepYears);
    }

    // 劳动/工作分配
    if (this.currentAge >= 14 && this.currentAge <= 70) {
      const wealthGain = Math.round((this.energy.work / 12) * stepYears);
      attr.wealth += wealthGain;
      if (this.energy.health < 20 && this.energy.work > 40) {
        attr.health -= Math.round((this.energy.work / 15) * stepYears);
      }
    }

    // 家庭分配
    attr.family += Math.round(((this.energy.family - 25) / 10) * stepYears);
    if (this.energy.family >= 35) {
      attr.mentality += Math.round(1 * stepYears);
    }

    // 健康分配
    if (this.energy.health >= 35) {
      attr.health += Math.round(2 * stepYears);
    } else if (this.energy.health < 15) {
      attr.health -= Math.round(2 * stepYears);
    }

    // 自然衰老对健康与心态的消耗
    if (this.currentAge > 50) {
      attr.health -= Math.round(((this.currentAge - 50) / 15) * stepYears);
    }

    // 产业特征对属性的影响（如重工业与下岗浪潮）
    if (this.currentYear >= 1998 && this.currentYear <= 2000 && this.currentAge >= 28 && this.currentAge <= 55) {
      const city = this.cities.find(c => c.id === this.character.cityId);
      if (city && city.type === '重工业资源型') {
        attr.wealth = Math.max(10, attr.wealth - 5 * stepYears);
        attr.mentality = Math.max(10, attr.mentality - 5 * stepYears);
      }
    }

    // 2020-2022 疫情静默与供应链受阻对实体商贸、外贸民营及务工的冲击
    if (this.currentYear >= 2020 && this.currentYear <= 2022 && this.currentAge >= 20 && this.currentAge <= 65) {
      const city = this.cities.find(c => c.id === this.character.cityId);
      if (city && (city.type === '沿海商贸外贸型' || city.type === '民营轻工集群型' || city.type === '传统农业劳务型')) {
        attr.wealth = Math.max(8, attr.wealth - 4 * stepYears);
        attr.mentality = Math.max(10, attr.mentality - 3 * stepYears);
      }
    }

    // 2022-2023 冬春转段高烧对高龄群体的健康消耗
    if ((this.currentYear === 2022 || this.currentYear === 2023) && this.currentAge >= 68) {
      attr.health = Math.max(5, attr.health - 6 * stepYears);
    }

    // 2023-2024 AI大模型狂飙对青年知识白领的降本增效竞争
    if (this.currentYear >= 2023 && this.currentYear <= 2024 && this.currentAge >= 20 && this.currentAge <= 35) {
      const city = this.cities.find(c => c.id === this.character.cityId);
      if (city && city.type === '综合科教中心') {
        if (this.energy.study >= 30) {
          attr.knowledge += 5 * stepYears;
        } else {
          attr.mentality = Math.max(10, attr.mentality - 4 * stepYears);
        }
      }
    }

    // 边界限制
    attr.health = Math.max(0, Math.min(100, attr.health));
    attr.wealth = Math.max(5, Math.min(100, attr.wealth));
    attr.knowledge = Math.max(5, Math.min(100, attr.knowledge));
    attr.family = Math.max(5, Math.min(100, attr.family));
    attr.mentality = Math.max(5, Math.min(100, attr.mentality));
  }

  /**
   * 自动生成当年纪实叙事 (严格 80-150 字，克制、具体、生活细节)
   */
  generateNarrative(era, triggeredEvent, disasterStrike) {
    const age = this.currentAge;
    const year = this.currentYear;
    const prov = this.character.birthPlace;
    const city = this.cities.find(c => c.id === this.character.cityId) || {};
    const cityDisp = this.resolveCityDisplay(city, year);
    const indEraKey = this.getIndustryEraKey(year);
    const ind = city.eraIndustries ? city.eraIndustries[indEraKey] : null;

    // 1. 若当年遭遇自然灾难袭击
    if (disasterStrike && disasterStrike.isHit) {
      return disasterStrike.disaster.hitNarrative;
    }

    // 2. 宏观背景切片 (约 40-60 字)
    let macro = '';
    if (triggeredEvent && triggeredEvent.narrative) {
      macro = triggeredEvent.narrative.slice(0, 70);
    } else {
      const snippets = era.macroSnippets || [];
      macro = snippets[Math.floor(Math.random() * snippets.length)] || `${year}年春风吹过神州大地，历史的滚滚车轮在每一个寻常巷陌刻下深印。`;
    }

    // 3. 个人处境切片 (结合具体城市产业与职业细节，约 40-70 字)
    let personal = '';
    const jobDetail = ind && ind.typicalJobs ? ind.typicalJobs[0] : '寻常劳作';

    if (age <= 5) {
      personal = `你在${cityDisp.displayName}的青瓦泥墙下由长辈拉扯着蹒跚学步，常喝米汤充饥，童年在清贫中一天天长大。`;
    } else if (age <= 15) {
      if (this.energy.study >= 30) {
        personal = `在昏暗的煤油灯下仔细翻读卷边的旧课本，课余帮家里料理碎柴，心底里悄悄盼望着多长些文化见识。`;
      } else {
        personal = `你早早跟着长辈学习【${jobDetail}】的粗浅活计，掌心磨出薄茧，在粗茶淡饭间体味着操持家门的不易。`;
      }
    } else if (age <= 55) {
      if (this.energy.work >= 35) {
        personal = `你在${cityDisp.displayName}从事【${jobDetail}】，工装上落满岁月的痕迹，凭勤恳踏实攒下每分汗水钱撑起全家口粮。`;
      } else if (this.energy.family >= 35) {
        personal = `你把更多心思放在照拂老少亲眷上，柴米油盐细水长流，简陋的屋檐下洋溢着互谅互勉的人间温情。`;
      } else {
        personal = `在生活的磕碰起伏中步履不停，既要顾全家中一日三餐，也在岁月更迭中竭力守住内心的安宁。`;
      }
    } else {
      personal = `青丝染雪，手脚渐慢。你坐在老屋竹椅上守望着儿孙的背影，往昔在${cityDisp.displayName}数十载风风雨雨皆化作案头平静的长叹。`;
    }

    let full = `${macro} ${personal}`.trim();
    if (full.length > 150) {
      full = full.slice(0, 146) + '……';
    } else if (full.length < 80) {
      full += `岁序常易，寻常岁月里唯有坚韧生活才是最踏实的依靠。`;
    }

    return full;
  }

  /**
   * 前进一年（或步长指定年数）
   */
  advanceYear() {
    if (this.isGameOver) return null;

    let stepYears = this.getStepYears();
    if (this.currentYear < 2026 && this.currentYear + stepYears > 2026) {
      stepYears = 2026 - this.currentYear;
    }
    const era = this.getEraForYear(this.currentYear);

    // 1. 自然灾害碰撞命中检验（这是人生的残酷天谴）
    const disasterStrike = this.checkNaturalDisaster();
    if (disasterStrike && disasterStrike.isHit) {
      const dis = disasterStrike.disaster;

      // 记录曾亲历的特大自然灾害
      this.character.survivedDisasters.push(dis.name);

      // (1) 若直接罹难
      if (disasterStrike.isKilled) {
        this.triggerDisasterDeath(dis);
        return {
          isGameOver: true,
          deathInfo: this.deathInfo,
          character: this.character,
          history: this.history,
          isDisaster: true,
          disaster: dis
        };
      }

      // (2) 幸存但承受灾害重创
      let disasterEffectsDesc = [];
      if (disasterStrike.isInjured) {
        this.character.attributes.health = Math.max(10, this.character.attributes.health - 40);
        disasterEffectsDesc.push('在灾难中遭受重伤致残');
      }
      if (disasterStrike.isFamilyLost) {
        this.character.attributes.family = Math.max(10, this.character.attributes.family - 45);
        this.character.attributes.mentality = Math.max(10, this.character.attributes.mentality - 35);
        disasterEffectsDesc.push('痛失至亲骨肉');
      }
      if (disasterStrike.isWealthWiped) {
        this.character.attributes.wealth = 5;
        disasterEffectsDesc.push('家产田宅尽数被毁');
      }

      const disasterNarrative = `${dis.hitNarrative} 经此大难，你虽侥幸捡回一条命，但【${disasterEffectsDesc.join('、') || '惊魂未定'}】。`;
      let trimmedNarrative = disasterNarrative.trim();
      if (trimmedNarrative.length > 150) trimmedNarrative = trimmedNarrative.slice(0, 146) + '……';

      this.character.milestones.push({
        year: this.currentYear,
        age: this.currentAge,
        title: `历劫幸存：${dis.name}`,
        detail: `在${dis.name}浩劫中九死一生，${disasterEffectsDesc.join('，') || '家园疮痍重振'}。`
      });

      const turnRecord = {
        year: this.currentYear,
        age: this.currentAge,
        eraName: dis.name,
        narrative: trimmedNarrative,
        attributes: { ...this.character.attributes },
        eventTitle: `天灾：${dis.name}`
      };
      this.history.push(turnRecord);

      this.currentYear += stepYears;
      this.currentAge += stepYears;

      if (this.currentYear > 2026 || this.currentAge >= 98) {
        this.triggerNaturalEnding();
        return {
          isGameOver: true,
          deathInfo: this.deathInfo,
          character: this.character,
          history: this.history
        };
      }

      return {
        isDecision: false,
        turnRecord,
        character: this.character,
        isDisasterAlert: true,
        disaster: dis
      };
    }

    // 1.5 微观生活意外与飞来横祸 (低概率突发黑天鹅，受地域与工种调节)
    if (!disasterStrike && this.currentAge >= 14 && Math.random() < 0.005) {
      const city = this.cities.find(c => c.id === this.character.cityId);
      const acc = this.triggerMicroAccident(city);
      if (acc.isFatal) {
        return {
          isGameOver: true,
          deathInfo: this.deathInfo,
          character: this.character,
          history: this.history
        };
      }
    }

    // 2. 检查是否有历史事件待触发
    const eligibleEvents = this.findEligibleEvents();
    let pendingEvent = null;
    if (eligibleEvents.length > 0) {
      pendingEvent = eligibleEvents[0];
      this.statusFlags.add(`done_${pendingEvent.id}`);
    }

    // 3. 检查人生重要节点抉择
    let pendingMilestone = null;
    if (!pendingEvent) {
      pendingMilestone = this.checkLifeMilestone();
    }

    const activeDecision = (pendingEvent && pendingEvent.isDecision) ? pendingEvent : pendingMilestone;

    // 4. 正常年度死亡检测
    const deathRate = this.calculateAnnualMortalityRate(era);
    const deathRoll = Math.random();
    const hasDied = deathRoll < deathRate || this.character.attributes.health <= 0;

    if (hasDied) {
      this.triggerDeath(era, pendingEvent);
      return {
        isGameOver: true,
        deathInfo: this.deathInfo,
        character: this.character,
        history: this.history
      };
    }

    // 5. 若有重大历史抉择，暂停推进等待玩家选择
    if (activeDecision && activeDecision.isDecision) {
      return {
        isDecision: true,
        decisionData: activeDecision,
        currentYear: this.currentYear,
        currentAge: this.currentAge
      };
    }

    // 6. 若为被动事件，直接应用属性影响
    if (pendingEvent && !pendingEvent.isDecision && pendingEvent.passiveImpact) {
      for (const [k, v] of Object.entries(pendingEvent.passiveImpact)) {
        if (this.character.attributes[k] !== undefined) {
          this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
        }
      }
      this.character.milestones.push({
        year: this.currentYear,
        age: this.currentAge,
        title: pendingEvent.title,
        detail: pendingEvent.log || pendingEvent.historicalFact.slice(0, 45)
      });
    }

    // 7. 应用精力结算
    this.applyEnergyEffects(stepYears);

    // 8. 生成当年纪实叙事 (80-150字)
    const narrativeText = this.generateNarrative(era, pendingEvent, null);

    // 9. 记录历史轨迹
    const turnRecord = {
      year: this.currentYear,
      age: this.currentAge,
      eraName: era.name,
      narrative: narrativeText,
      attributes: { ...this.character.attributes },
      eventTitle: pendingEvent ? pendingEvent.title : null
    };
    this.history.push(turnRecord);

    // 10. 年份递增
    this.currentYear += stepYears;
    this.currentAge += stepYears;

    // 11. 到达 2026 年或百岁正常圆满
    if (this.currentYear > 2026 || this.currentAge >= 98) {
      this.triggerNaturalEnding();
      return {
        isGameOver: true,
        deathInfo: this.deathInfo,
        character: this.character,
        history: this.history
      };
    }

    return {
      isDecision: false,
      turnRecord,
      character: this.character
    };
  }

  /**
   * 玩家确认抉择后的结算处理
   */
  resolveDecision(decisionId, choiceIndex) {
    let evt = this.events.find(e => e.id === decisionId);
    if (!evt) {
      if (decisionId === 'node_school') {
        evt = {
          choices: [
            { text: '坚持上学', effect: { "knowledge": 25, "wealth": -10 }, log: '在困境中坚持上学，打下了扎实的文化底子。' },
            { text: '辍学做工', effect: { "wealth": 15, "knowledge": -10 }, log: '早早挑起家庭生计重担，在劳动中磨砺手茧。' }
          ]
        };
      } else if (decisionId === 'node_marriage') {
        evt = {
          choices: [
            { text: '遵从习俗成家', effect: { "family": 25, "wealth": -15 }, log: '遵从风俗完婚成家，与伴侣合力撑起小家。' },
            { text: '推迟婚期拼事业', effect: { "knowledge": 15, "wealth": 15 }, log: '暂缓婚事，全副身心投入到工作打拼中。' }
          ]
        };
      } else if (decisionId === 'node_medical') {
        evt = {
          choices: [
            { text: '耗尽积蓄就医', effect: { "health": 25, "wealth": -30 }, log: '动用全部积蓄寻医问药，病情得以平稳控制。' },
            { text: '保守硬抗省钱', effect: { "health": -20, "wealth": 5 }, log: '为给家中儿女省钱硬扛病痛，身体每况愈下。' }
          ]
        };
      } else if (decisionId === 'node_darkest_hour') {
        evt = {
          title: '人生至暗时刻：深渊边缘的寒夜',
          choices: [
            { text: '万念俱灰绝境弃生', isSuicide: true, log: '心力枯竭，在无尽的黑暗与深渊面前永远闭上了双眼。' },
            { text: '嚼碎屈辱负重苟活还债', isStoicSurvival: true, log: '咬碎牙关擦干眼泪，哪怕脱掉长衫出尽苦力，也要替家门把债还清。' },
            { text: '推开柴门接受至亲救赎', isFamilyRedeem: true, log: '在老母亲颤抖递来的一碗热汤面面前抱头痛哭，认栽还乡，在亲情庇护下捡回一条命。' }
          ]
        };
      }
    }

    if (!evt || !evt.choices || !evt.choices[choiceIndex]) return;

    const choice = evt.choices[choiceIndex];

    // 针对“至暗时刻”的特殊命运走向
    if (decisionId === 'node_darkest_hour') {
      if (choiceIndex === 0) {
        this.isGameOver = true;
        const cause = '于人生至暗时刻心力枯竭，在绝境深渊面前永远闭上了双眼';
        this.deathInfo = {
          age: this.currentAge,
          year: this.currentYear,
          cause,
          isNatural: false,
          isDarkestHour: true
        };
        this.character.milestones.push({
          year: this.currentYear,
          age: this.currentAge,
          title: '魂断深渊',
          detail: `于${this.currentYear}年（享年${this.currentAge}岁）在人生至暗绝境中走完了一生。`
        });
        return;
      } else if (choiceIndex === 1) {
        this.character.attributes.mentality = 25;
        this.character.attributes.wealth = Math.max(10, this.character.attributes.wealth);
      } else if (choiceIndex === 2) {
        this.character.attributes.mentality = 45;
        this.character.attributes.family = Math.max(35, this.character.attributes.family);
      }
    }

    if (choice.effect) {
      for (const [k, v] of Object.entries(choice.effect)) {
        if (this.character.attributes[k] !== undefined) {
          this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
        }
      }
    }

    this.character.milestones.push({
      year: this.currentYear,
      age: this.currentAge,
      title: evt.title || '人生关键抉择',
      detail: choice.log || choice.text
    });

    let stepYears = this.getStepYears();
    if (this.currentYear < 2026 && this.currentYear + stepYears > 2026) {
      stepYears = 2026 - this.currentYear;
    }
    const era = this.getEraForYear(this.currentYear);

    this.applyEnergyEffects(stepYears);

    const narrativeText = `${evt.narrative || ''} 面对命运的十字路口，你选择了【${choice.text}】。${choice.log || ''}`;
    let trimmedNarrative = narrativeText.trim();
    if (trimmedNarrative.length > 150) trimmedNarrative = trimmedNarrative.slice(0, 146) + '……';

    const turnRecord = {
      year: this.currentYear,
      age: this.currentAge,
      eraName: era.name,
      narrative: trimmedNarrative,
      attributes: { ...this.character.attributes },
      eventTitle: evt.title || '关键抉择'
    };
    this.history.push(turnRecord);

    this.currentYear += stepYears;
    this.currentAge += stepYears;

    if (this.currentYear > 2026 || this.currentAge >= 98) {
      this.triggerNaturalEnding();
    }
  }

  /**
   * 微观生活意外与飞来横祸 (不可抗力黑天鹅事件)
   */
  triggerMicroAccident(city) {
    const isWestern = city && (city.region === '西南' || city.region === '西北');
    const isHeavy = city && city.type === '重工业资源型';

    const accidentPool = [];

    if (isWestern) {
      accidentPool.push({
        title: '偶遇高原山道突发落石',
        detail: '在深山悬崖公路行车突遇山体落石砸毁车身，车翻落浅滩，所幸被路过老乡破窗拉出，身负多处骨折。',
        cause: '在高原深山公路遭遇突发山体崩塌落石不幸罹难',
        healthDmg: 35,
        wealthDmg: 15,
        fatalProb: 0.16
      });
    }

    if (isHeavy) {
      accidentPool.push({
        title: '重工车间突发机械安全事故',
        detail: '老厂行车钢丝绳断裂掉落重载钢件，险些被当场砸中，右腿严重撕裂骨折住院大半年。',
        cause: '在重工业厂矿车间突发机械意外工伤罹难',
        healthDmg: 35,
        wealthDmg: 10,
        fatalProb: 0.15
      });
    }

    accidentPool.push(
      {
        title: '国道大货车恶性侧翻险情',
        detail: '深夜乘坐长途大巴遭遇对向满载大货车失控侧翻刮擦，满身玻璃划痕被甩出车厢捡回一条命。',
        cause: '在国道遭遇夜行重型货车失控交通事故不幸离世',
        healthDmg: 30,
        wealthDmg: 15,
        fatalProb: 0.18
      },
      {
        title: '老旧宅院电线短路起火',
        detail: '深夜老屋电线短路引燃柴垛房梁，浓烟中仓皇背出家中老少，多年积攒的衣物被褥化为灰烬。',
        cause: '在深夜老屋电线短路火灾中吸入大量毒烟窒息离世',
        healthDmg: 20,
        wealthDmg: 30,
        fatalProb: 0.12
      }
    );

    const accident = accidentPool[Math.floor(Math.random() * accidentPool.length)];
    const isFatal = Math.random() < accident.fatalProb;

    if (isFatal) {
      this.isGameOver = true;
      this.deathInfo = {
        age: this.currentAge,
        year: this.currentYear,
        cause: accident.cause,
        isNatural: false,
        isAccident: true
      };
      this.character.milestones.push({
        year: this.currentYear,
        age: this.currentAge,
        title: '天降横祸',
        detail: `于${this.currentYear}年（享年${this.currentAge}岁）因【${accident.cause}】骤然离世。`
      });
      return { isFatal: true };
    }

    this.character.attributes.health = Math.max(10, this.character.attributes.health - accident.healthDmg);
    this.character.attributes.wealth = Math.max(5, this.character.attributes.wealth - accident.wealthDmg);
    this.character.milestones.push({
      year: this.currentYear,
      age: this.currentAge,
      title: accident.title,
      detail: accident.detail
    });

    return {
      isFatal: false,
      title: accident.title,
      detail: accident.detail
    };
  }

  /**
   * 触发天灾罹难终局
   */
  triggerDisasterDeath(disaster) {
    this.isGameOver = true;
    const cause = `在【${disaster.name}】特大浩劫中不幸罹难`;

    this.deathInfo = {
      age: this.currentAge,
      year: this.currentYear,
      cause,
      isNatural: false,
      isDisaster: true,
      disasterName: disaster.name
    };

    this.character.milestones.push({
      year: this.currentYear,
      age: this.currentAge,
      title: '魂断天灾',
      detail: `于${this.currentYear}年遭遇${disaster.name}，生命永远定格在${this.currentAge}岁。`
    });
  }

  /**
   * 触发疾病或时代终老离世
   */
  triggerDeath(era, fatalEvent) {
    this.isGameOver = true;
    let cause = '因病恶化未能及时救治不幸离世';

    if (this.currentAge <= 2) {
      cause = '因当年严峻的新生儿急症与医疗条件匮乏夭折';
    } else if (fatalEvent && fatalEvent.title.includes('饥荒')) {
      cause = '遭遇严重饥荒营养枯竭衰竭离世';
    } else if (fatalEvent && fatalEvent.title.includes('抗战')) {
      cause = '战火流弹波及与战地疫病离世';
    } else {
      const causes = era.typicalCausesOfDeath || ['因高龄体衰自然终老'];
      cause = causes[Math.floor(Math.random() * causes.length)];
    }

    this.deathInfo = {
      age: this.currentAge,
      year: this.currentYear,
      cause,
      isNatural: false,
      isDisaster: false
    };

    this.character.milestones.push({
      year: this.currentYear,
      age: this.currentAge,
      title: '魂归故土',
      detail: `于${this.currentYear}年（享年${this.currentAge}岁）因【${cause}】走完了一生。`
    });
  }

  /**
   * 到达 2026 年依然在世的圆满结局
   */
  triggerNaturalEnding() {
    this.isGameOver = true;
    const finalYear = 2026;
    const finalAge = 2026 - this.character.birthYear;
    this.currentYear = finalYear;
    this.currentAge = finalAge;

    this.deathInfo = {
      age: finalAge,
      year: finalYear,
      cause: '见证近百年家国沧桑，于当今盛世安享晚年',
      isNatural: true,
      isDisaster: false
    };

    this.character.milestones.push({
      year: finalYear,
      age: finalAge,
      title: '见证盛世',
      detail: `从${this.character.birthYear}年风雨中一路走来，终在2026年与时代相拥，一生平凡而丰厚。`
    });
  }

  /**
   * 与同代出生人对比（生成同龄人分布排位）
   */
  calculatePeerComparisons() {
    const age = this.deathInfo ? this.deathInfo.age : this.currentAge;
    const birthYear = this.character.birthYear;
    const era = this.getEraForYear(birthYear);

    const expectedLife = era.lifeExpectancy;
    const diff = age - expectedLife;
    let lifePercentile = 50;
    if (diff > 25) lifePercentile = 95;
    else if (diff > 15) lifePercentile = 85;
    else if (diff > 5) lifePercentile = 70;
    else if (diff > -5) lifePercentile = 50;
    else if (diff > -15) lifePercentile = 30;
    else lifePercentile = 12;

    const knowledge = this.character.attributes.knowledge;
    let eduLevel = '小学及以下';
    let eduPercentile = 40;
    if (knowledge > 80) {
      eduLevel = '大专或大学本科以上';
      eduPercentile = 96;
    } else if (knowledge > 60) {
      eduLevel = '高中 / 技校中专';
      eduPercentile = 82;
    } else if (knowledge > 35) {
      eduLevel = '初中文化';
      eduPercentile = 60;
    } else {
      eduLevel = '小学或识字扫盲班水平';
      eduPercentile = 35;
    }

    const wealth = this.character.attributes.wealth;
    let wealthTier = '平稳小康';
    let wealthPercentile = 55;
    if (wealth > 80) {
      wealthTier = '优渥富裕';
      wealthPercentile = 90;
    } else if (wealth > 60) {
      wealthTier = '温饱有余（小康）';
      wealthPercentile = 72;
    } else if (wealth > 35) {
      wealthTier = '寻常温饱';
      wealthPercentile = 45;
    } else {
      wealthTier = '生计艰辛（困顿）';
      wealthPercentile = 18;
    }

    return {
      lifespan: {
        val: age,
        expected: expectedLife,
        percentile: lifePercentile,
        desc: `在同年代出生人群中排前 ${100 - lifePercentile}% 左右（当年新生儿平均预期寿命约为 ${expectedLife} 岁）`
      },
      education: {
        level: eduLevel,
        percentile: eduPercentile,
        desc: `超过了同代约 ${eduPercentile}% 的同龄人文化水平`
      },
      wealth: {
        tier: wealthTier,
        percentile: wealthPercentile,
        desc: `处在同代人中约前 ${100 - wealthPercentile}% 的生计水平区间`
      }
    };
  }
}

// 挂载至全局
window.SimulationEngine = SimulationEngine;
