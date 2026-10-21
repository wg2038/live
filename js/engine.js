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
    this.currentPendingDecision = null;
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
   * 创建新角色（开局玩家无法选择出身，支持时代与抽选模式参数）
   */
  createCharacter(options = 'medium') {
    let paceMode = 'medium';
    let eraFilter = 'all';
    let cityFilter = 'weighted';

    if (typeof options === 'object' && options !== null) {
      paceMode = options.paceMode || 'medium';
      eraFilter = options.eraFilter || 'all';
      cityFilter = options.cityFilter || 'weighted';
    } else if (typeof options === 'string') {
      paceMode = options;
    }

    this.paceMode = paceMode;
    this.history = [];
    this.statusFlags.clear();
    this.currentPendingDecision = null;
    this.isGameOver = false;
    this.deathInfo = null;

    // 1. 出生年份 (支持年代段抽取)
    let birthYear;
    if (eraFilter === '1937_1949') {
      birthYear = Math.floor(1937 + Math.random() * (1949 - 1937 + 1));
    } else if (eraFilter === '1950_1977') {
      birthYear = Math.floor(1950 + Math.random() * (1977 - 1950 + 1));
    } else if (eraFilter === '1978_1999') {
      birthYear = Math.floor(1978 + Math.random() * (1999 - 1978 + 1));
    } else if (eraFilter === '2000_2026') {
      birthYear = Math.floor(2000 + Math.random() * (2026 - 2000 + 1));
    } else {
      birthYear = this.sampleBirthYear();
    }
    const era = this.getEraForYear(birthYear);
    const indEraKey = this.getIndustryEraKey(birthYear);

    // 2. 出生省份与城市/区县 (支持不同抽选机制)
    let province, city;
    if (cityFilter === 'county') {
      const countyPool = this.cities.filter(c => c.type.includes('县') || c.type.includes('资源') || c.type.includes('贫瘠') || c.type.includes('特色'));
      city = countyPool.length > 0 ? countyPool[Math.floor(Math.random() * countyPool.length)] : this.cities[0];
      province = this.provinces.find(p => p.id === city.provinceId) || this.provinces[0];
    } else if (cityFilter === 'random') {
      city = this.cities[Math.floor(Math.random() * this.cities.length)];
      province = this.provinces.find(p => p.id === city.provinceId) || this.provinces[0];
    } else {
      province = this.sampleProvince();
      city = this.sampleCityInProvince(province.id);
    }
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
      careerTrack: this.determineInitialCareerTrack(isUrban, city, familyClass, parentJob),
      careerRank: '初生幼年',
      occupation: isUrban ? '城镇孩童' : '乡野幼童',
      milestones: [],
      survivedDisasters: [],
      lifelineHistory: [
        {
          age: 0,
          year: birthYear,
          health: attributes.health,
          wealth: attributes.wealth,
          mentality: attributes.mentality,
          knowledge: attributes.knowledge
        }
      ]
    };

    this.currentYear = birthYear;
    this.currentAge = 0;
    this.updateCareerStage();

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
   * 记录生命轨迹点（用于绘制人生轨迹线图）
   */
  recordLifeline() {
    if (!this.character) return;
    this.character.lifelineHistory.push({
      age: this.currentAge,
      year: this.currentYear,
      health: this.character.attributes.health,
      wealth: this.character.attributes.wealth,
      mentality: this.character.attributes.mentality,
      knowledge: this.character.attributes.knowledge
    });
  }

  /**
   * 计算步长（根据游戏时长选项）
   */
  getStepYears() {
    if (this.paceMode === 'step' || this.paceMode === 'long' || this.paceMode === 'medium') return 1;
    if (this.paceMode === 'short') {
      if (this.currentAge < 16) return 2;
      return 3;
    }
    return 1;
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
    const isLateBorn = this.character && this.character.birthYear >= 2010;

    // 针对 2010 年及以后出生的新时代少儿专属成长关卡（绝不涉及成年虚构内容）
    if (isLateBorn) {
      if (age >= 6 && age <= 8 && !this.statusFlags.has('decision_child_interest')) {
        this.statusFlags.add('decision_child_interest');
        return {
          id: 'node_child_interest',
          title: '幼小衔接与兴趣班抉择',
          isDecision: true,
          narrative: `你已到学龄，周边家长纷纷给孩子报名少儿编程、英语口语与思维训练班。面对激烈的同龄竞争，家庭需权衡教育投入。`,
          choices: [
            {
              text: '报读少儿兴趣与思维启蒙班',
              effect: { "knowledge": 20, "wealth": -15, "health": -5 },
              log: '周末穿梭于各个校外培训班，虽略显疲累，但眼界与思维打下了扎实基础。'
            },
            {
              text: '坚持快乐童年，多跑跳户外运动',
              effect: { "health": 15, "family": 15, "wealth": 5 },
              log: '放学后与邻里小伙伴在小区楼下自由奔跑玩耍，享受无忧无虑的纯真童年。'
            }
          ]
        };
      }

      if (age >= 10 && age <= 12 && !this.statusFlags.has('decision_child_digital')) {
        this.statusFlags.add('decision_child_digital');
        return {
          id: 'node_child_digital',
          title: '网课居家与智能终端考量',
          isDecision: true,
          narrative: `疫情居家上网课期间，你拥有了属于自己的平板与智能手机。屏幕那头是老师的板书，后台则是精彩纷呈的短视频与手机游戏。`,
          choices: [
            {
              text: '高度自律专心网课，主动做拓展题',
              effect: { "knowledge": 25, "mentality": 10, "health": -5 },
              log: '抵制住了游戏短视频诱惑，利用数字终端汲取海量知识，成绩名列前茅。'
            },
            {
              text: '沉迷手机游戏与短视频，熬夜摸鱼',
              effect: { "mentality": 15, "health": -10, "knowledge": -10 },
              log: '在虚拟网络世界中获得极高满足感，但也让视力下降，课业偶有落伍。'
            }
          ]
        };
      }

      if (age >= 14 && age <= 16 && !this.statusFlags.has('decision_child_exam')) {
        this.statusFlags.add('decision_child_exam');
        return {
          id: 'node_child_exam',
          title: '中考分流与未来求学方向',
          isDecision: true,
          narrative: `初三中考倒计时，面对普职分流的现实分水岭，教室里的空气格外凝重。面对未来的求学路径，你与父母坐下来认真商量。`,
          choices: [
            {
              text: '开启题海战术冲刺重点示范普高',
              effect: { "knowledge": 30, "health": -10, "mentality": -5 },
              log: '挑灯夜战刷完几十套模拟卷，顺利拿到重点高中录取通知书，迈入人生新起点。'
            },
            {
              text: '报考艺术特长或特色职业技术院校',
              effect: { "mentality": 15, "wealth": 10, "knowledge": 10 },
              log: '结合自身爱好走向特色技能赛道，卸下过重考学包袱，走上一条踏实务实之路。'
            }
          ]
        };
      }

      return null;
    }

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
            status: 'status_dropped_out',
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
   * 初生职业轨道推演判定
   */
  determineInitialCareerTrack(isUrban, city, familyClass, parentJob) {
    if (familyClass === '干部' || familyClass === '知识分子') return 'cadre_teacher';
    if (familyClass === '商人' || (parentJob && (parentJob.includes('商') || parentJob.includes('贩') || parentJob.includes('铺')))) return 'merchant';
    if (familyClass === '工人' || (parentJob && (parentJob.includes('工') || parentJob.includes('匠')))) return 'worker';
    if (!isUrban || (familyClass && familyClass.includes('农'))) return 'farmer';
    if (city && city.type === '综合科教中心') return 'tech_whitecollar';
    return isUrban ? 'worker' : 'farmer';
  }

  /**
   * 角色生涯与职业进阶树动态推演引擎 (0-80+岁千人千面)
   */
  updateCareerStage() {
    if (!this.character) return;
    const char = this.character;
    const age = this.currentAge;
    const year = this.currentYear;
    const flags = this.statusFlags;
    const energy = this.energy;
    const attr = char.attributes;
    const isUrban = char.urbanRural === 'urban';

    if (!char.careerTrack) {
      char.careerTrack = this.determineInitialCareerTrack(isUrban, null, char.familyClass, char.parentJob);
    }

    // 1. 动态轨道迁跃校准 (基于重大历史抉择与玩家精力)
    if (flags.has('college_graduate') || flags.has('attended_gaokao')) {
      if (year >= 2000 && (char.cityType === '综合科教中心' || energy.study >= 30)) {
        char.careerTrack = 'tech_whitecollar';
      } else {
        char.careerTrack = 'cadre_teacher';
      }
      char.educationLevel = '大学本科';
    } else if (flags.has('chose_south_artisan') || flags.has('township_worker') || flags.has('certified_technician')) {
      char.careerTrack = 'worker';
    } else if (flags.has('chose_iron_bowl') || flags.has('vocational_talent')) {
      char.careerTrack = 'worker';
      char.educationLevel = '中等专业';
    } else if (flags.has('xiahai_entrepreneur') || flags.has('franchise_owner') || flags.has('regional_trader')) {
      char.careerTrack = 'merchant';
    } else if (flags.has('safe_driver') || flags.has('highspeed_commuter')) {
      char.careerTrack = 'flexible_labor';
    } else if (flags.has('expert_farmer') || flags.has('sober_peasant')) {
      char.careerTrack = 'farmer';
    }

    // 2. 年龄阶段进阶与身份定格
    let title = '平民';

    // (A) 幼年期 (0-5岁)
    if (age <= 2) {
      title = isUrban ? '城镇乳儿' : '乡野乳儿';
    } else if (age <= 5) {
      title = isUrban ? '城镇幼童' : '乡野幼童';
    }
    // (B) 少年求学与帮工期 (6-14岁)
    else if (age <= 14) {
      if (flags.has('status_dropped_out')) {
        if (isUrban) {
          title = year < 1980 ? '手工作坊学徒' : '市井跑腿杂工';
        } else {
          title = year < 1980 ? '生产队放牛娃' : '农家田头帮工';
        }
      } else {
        if (age <= 11) {
          char.educationLevel = '小学在读';
          if (year < 1950) title = '私塾/新制小学童';
          else if (year < 1978) title = '完小少先队员';
          else if (year < 2000) title = '小学少先队员';
          else title = '小学学生';
        } else {
          char.educationLevel = '初中在读';
          if (year < 1950) title = '新制初中学校生';
          else if (year < 1978) title = '初中学校红卫兵';
          else title = '初级中学在读生';
        }
      }
    }
    // (C) 青年起步与深造期 (15-22岁)
    else if (age <= 22) {
      const isStudying = flags.has('college_graduate') || 
                         char.educationLevel === '大学本科' || 
                         char.educationLevel === '高等院校在读' ||
                         (age <= 18 && (energy.study >= 25 || attr.knowledge >= 45));

      if (isStudying && age <= 18) {
        char.educationLevel = '高中在读';
        title = year < 1977 ? '完高学生/学农青年' : '示范高中学子';
      } else if (isStudying && age <= 22) {
        char.educationLevel = '高等院校在读';
        if (year < 1977) title = '工农兵推荐学员';
        else if (year < 1999) title = '全日制公费大学生';
        else title = '全日制大学本科生';
      } else if (char.educationLevel === '中等专业' || flags.has('chose_iron_bowl')) {
        title = age <= 18 ? '省属中专技校实习生' : '国营大厂分配青年技工';
      } else {
        switch (char.careerTrack) {
          case 'worker':
            if (year < 1978) title = isUrban ? '国营机修厂二级学徒' : '公社修配站青工';
            else if (year < 1998) title = flags.has('chose_south_artisan') ? '特区外资模具厂冲压工' : '国营机械厂车工';
            else if (year < 2012) title = '沿海五金装配流水线工';
            else title = '现代装备数控操作工';
            break;
          case 'farmer':
            if (year < 1980) title = '人民公社生产队整劳力';
            else if (year < 2000) title = '承包责任田种粮青年';
            else title = '现代农业合作社青年农户';
            break;
          case 'cadre_teacher':
            if (year < 1980) title = '公社完小民办代课教师';
            else if (year < 2000) title = '乡镇公办小学青年教师';
            else title = '公办学校青年教师/科员';
            break;
          case 'merchant':
            if (year < 1980) title = '街道便民组修补匠';
            else if (year < 2000) title = '农贸市场摊位年轻店主';
            else title = '连锁商超店长/电商合伙人';
            break;
          case 'tech_whitecollar':
            if (year < 2005) title = '外贸公司跟单助理';
            else if (year < 2015) title = '软件研发初级程序员';
            else title = '科技公司全栈研发工程师';
            break;
          case 'flexible_labor':
            if (year < 2005) title = '城市货运长途跟车员';
            else if (year < 2015) title = '干线重卡长途货车司机';
            else title = '平台同城专送金牌骑手';
            break;
          default:
            title = isUrban ? '工厂装配初级工' : '生产队青年劳力';
        }
      }
    }
    // (D) 壮年立业与黄金期 (23-59岁)
    else if (age <= 59) {
      const isJunior = age <= 35;
      const isMid = age > 35 && age <= 48;

      switch (char.careerTrack) {
        case 'worker':
          if (isJunior) {
            if (year < 1998) title = '国营机械厂四级钳工';
            else if (year < 2005) title = flags.has('xiagang_self_employed') ? '下岗再就业模具骨干' : '国企技改车间技术员';
            else title = '现代制造车间数控技师';
          } else if (isMid) {
            if (year < 1998) title = '机械制造车间副主任';
            else if (year < 2008) title = '民营五金模具厂车间主任';
            else title = '现代化总装车间主任/技师';
          } else {
            title = '资深机电总装大师傅/八级工';
          }
          break;

        case 'farmer':
          if (isJunior) {
            if (year < 1980) title = '公社大队农机手/副队长';
            else if (year < 2000) title = '责任田科技示范种粮能手';
            else title = '现代特色家庭农场主';
          } else if (isMid) {
            if (year < 1980) title = '人民公社生产大队长';
            else if (year < 2000) title = '乡镇农资总经销/种粮大户';
            else title = '农机专业合作社理事长';
          } else {
            title = '乡村资深农艺师/种田名家';
          }
          break;

        case 'cadre_teacher':
          if (isJunior) {
            if (year < 1980) title = '公社中心校教导主任';
            else if (year < 2000) title = '县属中学公办骨干教师';
            else title = '实验中学高级教研组长';
          } else if (isMid) {
            title = '重点中学校长/高级教师';
          } else {
            title = '教育系统资深督学/高级教师';
          }
          break;

        case 'merchant':
          if (isJunior) {
            if (year < 1980) title = '供销社百货柜组组长';
            else if (year < 2000) title = '沿海商贸五金批发商行主';
            else title = '跨境商贸供应链合伙人';
          } else if (isMid) {
            title = '建材五金城总批发商/总经理';
          } else {
            title = '民营商贸企业董事长/商会理事';
          }
          break;

        case 'tech_whitecollar':
          if (isJunior) {
            if (year < 2005) title = '跨国实业外贸部经理';
            else if (year < 2018) title = '互联网资深软件架构师';
            else title = '人工智能算法研发总监';
          } else if (isMid) {
            title = '高新科技公司技术总监/合伙人';
          } else {
            title = '数字化转型首席行业顾问';
          }
          break;

        case 'flexible_labor':
          if (isJunior) {
            if (year < 2005) title = '长途货运重卡车队司机';
            else if (year < 2018) title = '物流干线冷链调度组长';
            else title = '平台金牌车队长/专送主管';
          } else if (isMid) {
            title = '区域冷链货运车队长';
          } else {
            title = '产业园区设备安全运行主管';
          }
          break;

        default:
          title = isUrban ? '工厂技术骨干' : '乡村骨干农户';
      }
    }
    // (E) 退休退养与期颐期 (60岁及以上)
    else {
      const isOld = age >= 75;
      const isCentenarian = age >= 85;

      const isSystemRetiree = char.careerTrack === 'cadre_teacher' || 
                              char.careerTrack === 'worker' || 
                              char.careerTrack === 'tech_whitecollar' || 
                              char.urbanRural === 'urban';

      if (isCentenarian) {
        title = isSystemRetiree ? '期颐之年离休老同志' : '九旬期颐老寿星';
      } else if (isOld) {
        title = isSystemRetiree ? '八旬高龄退休老职工' : '八旬耄耋乡村长者';
      } else {
        if (char.careerTrack === 'cadre_teacher') {
          title = '教育系统退休高级教师';
        } else if (char.careerTrack === 'worker') {
          title = '国企退休八级技师';
        } else if (char.careerTrack === 'tech_whitecollar') {
          title = '企业退休资深技术顾问';
        } else if (char.careerTrack === 'farmer') {
          title = '乡村退养农户/享基础养老金';
        } else if (char.careerTrack === 'merchant') {
          title = '退养商界名宿/老街坊';
        } else {
          title = isUrban ? '城镇退休居民/享社保' : '乡村退养长者/享养老金';
        }
      }
    }

    char.occupation = title;
  }

  /**
   * 将重大历史抉择动态匹配到角色的年龄与社会圈层 (千人千面)
   */
  adaptDecisionToPersona(decision) {
    if (!decision) return decision;
    if (decision.id === 'evt_2022_covid_lockdown') {
      const age = this.currentAge;
      const track = this.character ? this.character.careerTrack : 'worker';

      // 1. 高龄退养群体 (>=60岁)
      if (age >= 60) {
        return {
          id: 'evt_2022_covid_lockdown',
          title: '常态化防控、社区静默与慢病保供',
          isDecision: true,
          historicalFact: '2022年部分特大城市经历长时间静态管理与网格化多轮核酸筛查，社区成为老幼互助的最小单元，各级保障通道全力守护高龄慢病群体的生命线。',
          narrative: '绿色的健康码和场所码成了进出楼栋的硬通货。社区连日组织多轮网格化筛查，儿孙隔着手机屏幕反复叮嘱别受凉。家里的降压慢病常用药快要见底，楼道群里老街坊们互相通气匀药，在不确定的岁月里守望相助。',
          choices: [
            {
              text: '求助居委会与楼组长接力配药通道，闭门静心休养',
              effect: { "health": 15, "mentality": 10, "wealth": -5 },
              status: "covid_senior_rest",
              log: '靠社区爱心送药通道和邻里匀出的半盒降压药渡过断药危机，居家静待生机。'
            },
            {
              text: '戴好口罩与红袖标，在楼道单元协助分发蔬菜与抗原试剂',
              effect: { "mentality": 20, "family": 15, "health": -15 },
              status: "covid_senior_volunteer",
              log: '虽腿脚微有不便，但协助楼道分发爱心菜包，赢得街坊邻里由衷敬重。'
            }
          ]
        };
      }

      // 2. 青少年与在读学子 (<23岁)
      if (age < 23) {
        return {
          id: 'evt_2022_covid_lockdown',
          title: '高校闭环管理、线上答辩与考公考研大潮',
          isDecision: true,
          historicalFact: '2022年高校广泛推行闭环管理与线上双选会，应届毕业生规模创下历史新高，数以百万计的年轻人投入考研与公考大军。',
          narrative: '校园实行闭环管理，食堂提倡错峰打包，自习室拉起了透明隔板。毕业论文答辩转入腾讯会议云端，线下春招宣讲会纷纷延期。面对严峻的就业大盘，考研自习室与公考备考群里座无虚席。',
          choices: [
            {
              text: '扎进图书馆早出晚归，高强度刷题冲刺事业单位与公考',
              effect: { "knowledge": 25, "mentality": -10, "health": -10 },
              status: "covid_study_exam",
              log: '刷完上万道公考行测申论模拟题，在严峻就业大环境中力求搏得一份稳定保障。'
            },
            {
              text: '海投民营科技与外贸实习，先就业在实战一线积累经验',
              effect: { "wealth": 15, "mentality": 15, "knowledge": 10 },
              status: "covid_early_job",
              log: '放下身段先就业再择业，在实际业务摸爬滚打中迅速褪去学生的稚气。'
            }
          ]
        };
      }

      // 3. 体制内/教师/医护群组
      if (track === 'cadre_teacher') {
        return {
          id: 'evt_2022_covid_lockdown',
          title: '常态化防控、线上教学与下沉网格包保',
          isDecision: true,
          historicalFact: '2022年广大党员干部、教师和医护工作者践行初心使命，坚守讲台停课不停学，多轮下沉社区网格充实基层保供与流调排查一线。',
          narrative: '作为体制内与文教人员，单位要求除保供运转外全员居家备勤。不仅要熟练开展线上网课与云端办公，还要随时响应号召下沉网格协助维持核酸检测秩序与卡口值守。',
          choices: [
            {
              text: '一丝不苟备好每一堂线上网课，安抚屏幕那端求学的孩子',
              effect: { "knowledge": 15, "mentality": 10, "health": -5 },
              status: "covid_online_teaching",
              log: '调试好麦克风与课件，在特殊时期给求学的孩子们守住一张安定的书桌。'
            },
            {
              text: '佩戴红袖标连续数周下沉社区一线协助维持采样秩序与卡口值守',
              effect: { "mentality": 20, "family": 10, "health": -20 },
              status: "covid_cadre_volunteer",
              log: '顶着风雨在核酸卡口扫码值守，身心极度疲惫，但也切身体会到基层一线的不易。'
            }
          ]
        };
      }

      // 4. 工矿与制造技工
      if (track === 'worker') {
        return {
          id: 'evt_2022_covid_lockdown',
          title: '闭环泡泡生产、驻厂保产与供应链承压',
          isDecision: true,
          historicalFact: '2022年重点工业企业推行‘气泡式’闭环管理，广大产业工人和工程师吃住在厂、封闭连轴运转，全力保住关键产业链供应链稳定。',
          narrative: '为保障重点产业链与重大装备交付不中断，厂区实行‘气泡式’闭环管理。工人们背着被褥卷住进车间行军床，每天早晚做抗原核酸，机器轰鸣昼夜不歇，物流货车排队消杀等候通行证。',
          choices: [
            {
              text: '接受驻厂闭环封闭生产，睡车间行军床换取加班津贴',
              effect: { "wealth": 20, "health": -20, "mentality": -10 },
              status: "covid_factory_bubble",
              log: '在车间地铺上熬了整整一个月，靠满负荷加班保住交货期，领到一笔沉甸甸的闭环津贴。'
            },
            {
              text: '担忧家中老小生计，申请居家静默照料老小',
              effect: { "family": 25, "mentality": 10, "wealth": -15 },
              status: "covid_home_care",
              log: '放弃闭环津贴守在家人身边，虽只能拿基本保障工资，但一家人朝夕相伴心里踏实。'
            }
          ]
        };
      }

      // 5. 知识白领与科技人员
      if (track === 'tech_whitecollar') {
        return {
          id: 'evt_2022_covid_lockdown',
          title: '居家远程办公、腾讯会议与降本增效阴云',
          isDecision: true,
          historicalFact: '2022年现代科技与商务服务业全面推行远程办公，各平台会议日活激增，同时面临降本增效与组织架构调整带来的职场挑战。',
          narrative: '居家远程办公成了常态，日程表被密密麻麻的线上会议占满。屏幕右下角时不时跳出公司业务收缩与部门裁员降薪的传闻。窗外的大街空空荡荡，你在书桌前一边盯着线上周报，一边关注着生鲜App的清晨补货时段。',
          choices: [
            {
              text: '熬夜响应工作群消息保住KPI，利用深夜恶补新技术与考编知识',
              effect: { "knowledge": 20, "wealth": 10, "health": -20 },
              status: "covid_wfh_struggle",
              log: '顶住裁员阴影在工位上连轴转，用过硬的业务产出和技能储备稳住了职场阵脚。'
            },
            {
              text: '申请远程外包兼职并压缩一切日常非必要开销，囤粮求稳',
              effect: { "wealth": 10, "family": 15, "mentality": -10 },
              status: "covid_frugal_defense",
              log: '果断退订非必要消费，居家学做三餐，以极低的生存成本平稳度过风暴期。'
            }
          ]
        };
      }

      // 6. 商户、个体与灵活人员
      return {
        id: 'evt_2022_covid_lockdown',
        title: '实体客流冲击、社区保供团长与现金流生死线',
        isDecision: true,
        historicalFact: '2022年部分线下餐饮、文旅与小微商贸遭遇停业与现金流严峻考验，许多商户主动转型社区保供团购，在坚守与转型中搏击生机。',
        narrative: '堂食暂停、商场关门、物流受阻，卷帘门一关就是数月，但店铺租金、员工保底与货款账单依旧准时送达。街头行人寥寥，唯有身穿防护服的保供人员与骑手在疾驰。小微生计到了悬崖边上。',
        choices: [
          {
            text: '对接周边小区居民需求，改做无接触社区团购保供与自提配送',
            effect: { "wealth": 15, "health": -25, "mentality": -10 },
            status: "covid_group_leader",
            log: '每天起早摸黑对接蔬菜基地与小区团购，靠微薄跑腿利润和双脚硬扛过店铺断流难关。'
          },
          {
            text: '与房东坦诚协商减免部分租金，盘点退库果断止损休整',
            effect: { "wealth": -15, "mentality": 15, "family": 15 },
            status: "covid_store_close",
            log: '结清各方款项保住信誉，退回老家与家人静待市场生机复苏，虽折损本金但守住了底线。'
          }
        ]
      };
    }
    return decision;
  }

  /**
   * 自动生成当年纪实叙事 (严格 80-150 字，千人千面四重线索交织：宏观切片 + 职业工种感官 + 家底温饱 + 精力印记)
   */
  generateNarrative(era, triggeredEvent, disasterStrike) {
    const age = this.currentAge;
    const year = this.currentYear;
    const char = this.character;
    const city = this.cities.find(c => c.id === char.cityId) || {};
    const cityDisp = this.resolveCityDisplay(city, year);

    // 1. 若当年遭遇特大自然灾害袭击
    if (disasterStrike && disasterStrike.isHit) {
      return disasterStrike.disaster.hitNarrative;
    }

    // 2. 线程一：宏观时代脉搏 (约 30-55 字)
    let macro = '';
    if (triggeredEvent && triggeredEvent.narrative) {
      macro = triggeredEvent.narrative.slice(0, 55);
    } else {
      macro = this.getYearMacroSnippet(year, era);
    }

    // 3. 线程二：职业工种感官与劳作细节 (约 35-55 字)
    const labor = this.getLaborSensorySnippet(char, age, year, cityDisp);

    // 4. 线程三：家境温饱与身心承载 (约 20-35 字)
    const household = this.getHouseholdSensorySnippet(char, age);

    // 5. 线程四：精力灌注之印记 (约 15-25 字)
    const energyFocus = this.getEnergySensorySnippet(this.energy);

    // 综合编织
    let full = `${macro} ${labor} ${household} ${energyFocus}`.trim();

    // 长度与节奏严格钳制在 80 - 150 汉字
    if (full.length > 150) {
      full = full.slice(0, 146) + '……';
    } else if (full.length < 80) {
      full += `岁序常易，寻常岁月里唯有脚踏实地才是穿透风雨最坚固的依靠。`;
      if (full.length > 150) full = full.slice(0, 146) + '……';
    }

    return full;
  }

  getYearMacroSnippet(year, era) {
    if (year >= 1937 && year <= 1938) return `${year}年卢沟桥烽火骤起，沿海高校与工矿仓促西撤，流民车马塞满官道。`;
    if (year >= 1939 && year <= 1941) return `${year}年大后方警报声不绝于耳，黑烟滚滚，街市在空袭与物价飞涨中勉力维系。`;
    if (year >= 1942 && year <= 1943) return `${year}年中原旱蝗成灾与战事胶着，粮盐定量紧缩，家家在煤油灯下苦苦捱过饥馑。`;
    if (year >= 1944 && year <= 1945) return `${year}年抗战胜利号外传遍大街小巷，爆竹碎屑染红青石板，百废待兴复员还乡。`;
    if (year >= 1946 && year <= 1948) return `${year}年法币金圆券如废纸般贬值，商铺关门物价如脱缰野马，局势急剧动荡。`;
    if (year >= 1949 && year <= 1950) return `${year}年开国礼炮响彻神州，城乡秧歌腰鼓震天，扫盲夜校与分田界碑遍布乡野。`;
    if (year >= 1951 && year <= 1953) return `${year}年抗美援朝保家卫国动员如火如荼，大后方工厂夜以继日赶制支前被服弹药。`;
    if (year >= 1954 && year <= 1956) return `${year}年“一五”重工奠基与三大改造高潮涌动，公私合营与手工业入社红榜挂满街头。`;
    if (year >= 1957 && year <= 1959) return `${year}年土高炉火光映红夜空，大炼钢铁与公社大食堂号角齐鸣，标语刷满白灰墙。`;
    if (year >= 1960 && year <= 1962) return `${year}年粮票布票按两称重，稀粥照出人影，工矿精简职工退粮还乡共克时艰。`;
    if (year >= 1963 && year <= 1965) return `${year}年第一颗原子弹在戈壁升空，“备战备荒”三线建设号召大批骨干扎入深山。`;
    if (year >= 1966 && year <= 1970) return `${year}年红色浪潮席卷城乡，语录歌在大喇叭里终日回响，知青打起背包上山下乡。`;
    if (year >= 1971 && year <= 1975) return `${year}年街道地下防空工事叮当作响，乒乓外交叩开国门，车间里悄然抓紧规章整顿。`;
    if (year >= 1976 && year <= 1977) return `${year}年唐山余震未平，紧接着高考之门重新开启，数十万学子挑灯夜战奔赴考场。`;
    if (year >= 1978 && year <= 1981) return `${year}年改革春风拂面，小岗村承包红手印传开，街头巷尾探讨着实践真理与按劳分配。`;
    if (year >= 1982 && year <= 1985) return `${year}年女排夺冠万人空巷，黑白电视机围满邻里，特区蛇口开山炮声震动南国。`;
    if (year >= 1986 && year <= 1989) return `${year}年港台卡带情歌回响街头，物价闯关牵动人心，孔雀东南飞与进厂学徒潮并起。`;
    if (year >= 1990 && year <= 1992) return `${year}年亚运盼盼走红，邓小平南巡讲话掀起新一轮热潮，股市认购证排起长龙。`;
    if (year >= 1993 && year <= 1996) return `${year}年商品经济狂飙，三角债与下海大潮激荡，腰间寻呼机BP机的嘀嘀声不绝于耳。`;
    if (year >= 1997 && year <= 1999) return `${year}年维港焰火映照香港回归，国企三年脱困下岗阵痛袭来，高校大扩招带来新希望。`;
    if (year >= 2000 && year <= 2003) return `${year}年千禧钟声长鸣，入世集装箱货轮扬帆起航，非典突袭与收容遣送废止铭刻历史。`;
    if (year >= 2004 && year <= 2007) return `${year}年沿海世界工厂机器昼夜轰鸣，春运列车满载务工老乡，延续两千余年的农业税彻底废除。`;
    if (year >= 2008 && year <= 2009) return `${year}年汶川浩劫举国大救援，奥运五环点亮北京夜空，四万亿基建列车高速启动。`;
    if (year >= 2010 && year <= 2014) return `${year}年白色高铁银龙飞驰成网，智能手机与扫码支付融入市井，电商快递堆满驿站。`;
    if (year >= 2015 && year <= 2019) return `${year}年棚改货币化拆平老街旧巷，脱贫攻坚建档立卡，新能源汽车开始驶入寻常巷陌。`;
    if (year >= 2020 && year <= 2022) return `${year}年场所码与24小时核酸成为通行日常，多轮网格化筛查与供应链考验着万千生计。`;
    if (year >= 2023 && year <= 2026) return `${year}年生成式AI狂飙迭代，绿牌电车无声流过街头，延迟退休与银发时代悄然落地。`;
    return `${year}年时代车轮滚滚向前，千家万户的喜怒哀乐交织成奔涌的历史长河。`;
  }

  getLaborSensorySnippet(char, age, year, cityDisp) {
    const track = char.careerTrack || 'worker';
    const occ = char.occupation || '平民';

    // 1. 幼年 (0-5)
    if (age <= 5) {
      if (char.birthYear >= 2010) {
        return `你在${cityDisp.displayName}的长辈看护下玩耍，客厅播放着早教儿歌，城市在咿呀学语中日新月异。`;
      }
      return `你在${cityDisp.displayName}的简陋屋檐下蹒跚学步，常喝热米汤充饥，童年在清贫与泥土芬芳中一天天抽条。`;
    }

    // 2. 学童与青年求学 (6-14 或高等求学)
    if (age <= 14 || occ.includes('学生') || occ.includes('学员') || occ.includes('少先队')) {
      if (char.birthYear >= 2010) {
        if (age <= 11) return `书包沉沉压在肩上，教室里齐刷刷朗读课文，放学路队穿行于车流，盼着路边一串热烤肠。`;
        return `教室顶上日光灯嗡嗡作响，模拟题与错题本堆满课桌，指关节磨出薄茧，课间讨论着新网络话题。`;
      }
      if (age <= 11) {
        return `在简易木课桌前翻读磨出毛边的旧课本，墨水蹭脏了粗布袖口，晨读声穿透薄雾回荡在土墙校舍。`;
      }
      return `挑灯自习到深夜，算草纸写满密密麻麻的公式，煤油灯或日光灯照亮年轻求知的眼睛。`;
    }

    // 3. 退休与退养老者 (60+)
    if (age >= 60) {
      if (track === 'cadre_teacher' || track === 'worker' || track === 'tech_whitecollar' || char.urbanRural === 'urban') {
        return `身为【${occ}】，晨起拎着茶缸在公园看人杀棋，每月按时领退休金，戴着老花镜在阳台翻阅晚报。`;
      }
      return `身为【${occ}】，在自留菜园给水葱青菜浇水除草，傍晚守在村口看着儿孙，领着基础养老金颐养天年。`;
    }

    // 4. 各行业在岗劳动感官细节
    switch (track) {
      case 'worker':
        return `身为【${occ}】，工装上浸着深色机油与铁屑味，手握游标卡尺精确校准工件，机床轰鸣声震彻耳膜。`;
      case 'farmer':
        return `身为【${occ}】，卷起裤腿踩进微凉泥水田，农忙时秸秆粉尘扑得满身微痒，扶着突突作响的农机抢收抢种。`;
      case 'cadre_teacher':
        return `身为【${occ}】，讲台前飞扬着白色粉笔微尘，红墨水在教案本上留下端正批注，公文印章在桌角码放整齐。`;
      case 'merchant':
        return `身为【${occ}】，天未亮便哗啦拉开卷帘门，算盘与计算器噼啪作响，精细核算着每一笔进销差价与铺面流水。`;
      case 'tech_whitecollar':
        return `身为【${occ}】，液晶屏幕蓝光映在发酸的双眼，键盘敲击声不知疲倦，工作群红点闪烁，深夜工位放着凉透的外卖。`;
      case 'flexible_labor':
        return `身为【${occ}】，离合器踩到发木，雨夜反光雨披在车灯下闪烁，手机接单提示音在耳畔催促着分秒必争。`;
      default:
        return `身为【${occ}】，在${cityDisp.displayName}本分劳作，工装上落满岁月的痕迹，凭双手撑起门庭口粮。`;
    }
  }

  getHouseholdSensorySnippet(char, age) {
    const attr = char.attributes;
    if (attr.health < 30) {
      return `常年劳碌落下陈年腰腿疾，阴雨天隐隐酸痛，抽屉里常备膏药。`;
    }
    if (attr.wealth < 25) {
      return `手头紧巴捏着账本直叹气，粗茶淡饭精打细算度日。`;
    }
    if (attr.wealth >= 75) {
      return `家底渐趋厚实余粮宽裕，添置大件家什，日子过得分外踏实从容。`;
    }
    return `柴米油盐细水长流，日子虽不富裕倒也平稳温饱。`;
  }

  getEnergySensorySnippet(energy) {
    if (energy.study >= 40) return `夜灯下翻卷深研，眼界见识日益开阔。`;
    if (energy.work >= 45) return `抢抓工时全力打拼，掌心磨出厚实老茧。`;
    if (energy.family >= 45) return `用心照看老小起居，屋檐下满是烟火人情。`;
    if (energy.health >= 45) return `起居有节清淡进补，精神矍铄身骨结实。`;
    return `脚踏实地，在岁序更替中守住内心的踏实与平静。`;
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

    // 0. 更新角色职业状态与生涯阶段 (0-80岁职业进阶树)
    this.updateCareerStage();

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
      this.recordLifeline();

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

    let activeDecision = (pendingEvent && pendingEvent.isDecision) ? pendingEvent : pendingMilestone;

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

    // 5. 若有重大历史抉择，暂停推进等待玩家选择 (动态圈层千人千面适配)
    if (activeDecision && activeDecision.isDecision) {
      activeDecision = this.adaptDecisionToPersona(activeDecision);
      this.currentPendingDecision = activeDecision;
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
    this.recordLifeline();

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
    let evt = (this.currentPendingDecision && this.currentPendingDecision.id === decisionId)
      ? this.currentPendingDecision
      : this.events.find(e => e.id === decisionId);
    if (!evt) {
      if (decisionId === 'node_school') {
        evt = {
          choices: [
            { text: '坚持上学', effect: { "knowledge": 25, "wealth": -10 }, log: '在困境中坚持上学，打下了扎实的文化底子。' },
            { text: '辍学做工', effect: { "wealth": 15, "knowledge": -10 }, status: 'status_dropped_out', log: '早早挑起家庭生计重担，在劳动中磨砺手茧。' }
          ]
        };
      } else if (decisionId === 'node_child_interest') {
        evt = {
          title: '幼小衔接与兴趣班抉择',
          choices: [
            { text: '报读少儿兴趣与思维启蒙班', effect: { "knowledge": 20, "wealth": -15, "health": -5 }, log: '周末穿梭于各个校外培训班，虽略显疲累，但眼界与思维打下了扎实基础。' },
            { text: '坚持快乐童年多跑跳运动', effect: { "health": 15, "family": 15, "wealth": 5 }, log: '放学后与邻里小伙伴在小区楼下自由奔跑玩耍，享受无忧无虑的纯真童年。' }
          ]
        };
      } else if (decisionId === 'node_child_digital') {
        evt = {
          title: '网课居家与智能终端考量',
          choices: [
            { text: '高度自律专心网课打卡', effect: { "knowledge": 25, "mentality": 10, "health": -5 }, log: '抵制住了游戏短视频诱惑，利用数字终端汲取海量知识，成绩名列前茅。' },
            { text: '沉迷手机游戏与短视频', effect: { "mentality": 15, "health": -10, "knowledge": -10 }, log: '在虚拟网络世界中获得极高满足感，但也让视力下降，课业偶有落伍。' }
          ]
        };
      } else if (decisionId === 'node_child_exam') {
        evt = {
          title: '中考分流与求学走向',
          choices: [
            { text: '开启题海战术冲刺重点普高', effect: { "knowledge": 30, "health": -10, "mentality": -5 }, log: '挑灯夜战刷完几十套模拟卷，顺利拿到重点高中录取通知书，迈入人生新起点。' },
            { text: '报考艺术特长或职教院校', effect: { "mentality": 15, "wealth": 10, "knowledge": 10 }, log: '结合自身爱好走向特色技能赛道，卸下过重考学包袱，走上一条踏实务实之路。' }
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

    if (choice.status) {
      this.statusFlags.add(choice.status);
    }

    if (choice.effect) {
      for (const [k, v] of Object.entries(choice.effect)) {
        if (this.character.attributes[k] !== undefined) {
          this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
        }
      }
    }

    this.updateCareerStage();
    this.currentPendingDecision = null;

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

    // 0. 更新角色职业状态与生涯阶段 (0-80岁职业进阶树)
    this.updateCareerStage();

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
    this.recordLifeline();

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

    let cause = '见证近百年家国沧桑，于当今盛世安享晚年';
    let title = '见证盛世';
    let detail = `从${this.character.birthYear}年风雨中一路走来，终在2026年与时代相拥，一生平凡而丰厚。`;

    if (finalAge < 18) {
      cause = '在当今时代家庭的倾力托举与照护中平稳成长，正值少年求学之时';
      title = '风华少年';
      detail = `于${this.character.birthYear}年降生，在祖辈与父辈的倾力托举下，于2026年成长为风华少年。`;
    } else if (finalAge < 35) {
      cause = '沐浴新时代发展春风，作为时代青年正奋战于各行各业前沿';
      title = '青年立业';
      detail = `于${this.character.birthYear}年降生，历经求学与入职磨砺，在2026年昂首步入人生事业上升期。`;
    } else if (finalAge < 60) {
      cause = '历经时代风云洗礼，作为社会中流砥柱在当代继续奋斗前行';
      title = '中流砥柱';
      detail = `从${this.character.birthYear}年一路拼搏，承担家庭与事业重担，在2026年继续稳步前行。`;
    }

    this.deathInfo = {
      age: finalAge,
      year: finalYear,
      cause,
      isNatural: true,
      isDisaster: false,
      isAliveIn2026: true
    };

    this.character.milestones.push({
      year: finalYear,
      age: finalAge,
      title,
      detail
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

    // 针对 2010 年及以后出生且存活至 2026 年的少年
    if (this.character.birthYear >= 2010 && (this.deathInfo && this.deathInfo.isAliveIn2026)) {
      const eduLevel = age <= 6 ? '学前幼儿阶段' : (age <= 12 ? '小学义务教育阶段' : '初级中等教育在读');
      return {
        lifespan: {
          val: age,
          expected: expectedLife,
          percentile: 98,
          desc: `现代公共卫生条件下，该世代人均预期寿命已达 ${expectedLife} 岁，平稳健康成长中`
        },
        education: {
          level: eduLevel,
          percentile: 88,
          desc: `全面普及九年义务教育环境，知识技能基础良好`
        },
        wealth: {
          tier: this.character.economicLevel || '寻常温饱',
          percentile: 72,
          desc: `依托父辈两代人的积累，享有较完备的现代物质生活与家庭托举`
        }
      };
    }

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

  evaluateLifeResults() {
    return this.calculatePeerComparisons();
  }

  /**
   * 为 2010 年及以后出生且存活至 2026 年的角色生成“传承视角”三代人对照
   */
  generateLineageHistory(char) {
    if (!char || char.birthYear < 2010) return null;

    const childBirthYear = char.birthYear;
    // 父辈出生于 1975–1990 年
    const parentAgeAtBirth = 25 + (childBirthYear % 6);
    const parentBirthYear = childBirthYear - parentAgeAtBirth;
    // 祖辈出生于 1950–1965 年
    const grandAgeAtBirth = 24 + (parentBirthYear % 5);
    const grandBirthYear = parentBirthYear - grandAgeAtBirth;

    const isUrban = char.urbanRural === 'urban';

    const parentName = this.generateAuthenticName(parentBirthYear, '男', char.provinceId, char.ethnicity);
    const grandName = this.generateAuthenticName(grandBirthYear, '男', char.provinceId, char.ethnicity);

    // 1. 祖辈轨迹 (约 1950s-1970s 成长)
    const grandTimeline = [
      {
        period: `${grandBirthYear} — ${grandBirthYear + 15} 年`,
        stage: '童年与三年困难时期',
        detail: `生于新中国初建时期，童年亲历三年困难时期（1959–1961），靠红薯干与国家定粮度日，在朴素清贫中扎下勤俭家风。`
      },
      {
        period: `${grandBirthYear + 16} — ${grandBirthYear + 25} 年`,
        stage: '青年劳作与集体建设',
        detail: isUrban
          ? `青年期按政策招工进入${char.cityName}国营厂矿做工，历经工业建设岁月，按八级工规制领取粮票工资。`
          : `在公社生产大队挣工分、修筑水库水利设施，参加农业集体劳动，打下吃苦耐劳的体力底子。`
      },
      {
        period: `${grandBirthYear + 28} — ${grandBirthYear + 40} 年`,
        stage: '改革开放与家门立业',
        detail: isUrban
          ? `迎来改革开放与国企转轨浪潮，享受单位福利分房，操持一家温饱，抚育下一代成长。`
          : `赶上家庭联产承包责任制，大包干解决一家温饱，农闲兼做零工运输，支撑儿女学杂开支。`
      },
      {
        period: `2000 年代至今`,
        stage: '晚年桑榆与照看幼孙',
        detail: `迈入晚年领取基础养老退休金，常在老家小院侍弄菜圃，或进城帮衬照护孙辈（即你），在安宁中守望家族生生不息。`
      }
    ];

    // 2. 父辈轨迹 (约 1975-1990s 成长)
    const parentTimeline = [
      {
        period: `${parentBirthYear} — ${parentBirthYear + 18} 年`,
        stage: '求学与升学改制',
        detail: isUrban
          ? `在九年义务教育普惠中读完初高中，适逢高校大扩招浪潮，考入大专院校就读，成为家族首代知识白领。`
          : `完成乡村初中学业后就读中专技校或拜师学手艺，立志通过技术走出土地。`
      },
      {
        period: `${parentBirthYear + 19} — ${parentBirthYear + 26} 年`,
        stage: '就业打拼与经济转轨',
        detail: isUrban
          ? `步入社会直面国企重组与外资民企蓬勃期，进入现代企业竞争打拼，经历市场风浪与行业周期。`
          : `搭上南下民工大潮的绿皮火车，在沿海制造业车间、建筑工地或物流网点奔波，凭辛勤汗水汇款安家。`
      },
      {
        period: `${parentBirthYear + 26} — ${childBirthYear} 年`,
        stage: '房改安家与成家立业',
        detail: isUrban
          ? `适逢福利分房终结与商品房市场化，倾注两代人积蓄背负按揭贷款在城市购置首套住房，建立家庭。`
          : `在老家宅基地翻建二层红砖楼房，或在务工城市租房栖身，省吃俭用为新生命到来做好准备。`
      },
      {
        period: `${childBirthYear} — 2026 年`,
        stage: '托举子女与中年重任',
        detail: `迎来你的出生。人到中年承担上有老下有小的重担，经历校外辅导班热潮、疫情三年陪读与生活转段，倾尽所能护佑你平安成长。`
      }
    ];

    // 3. 角色自身（2010-2026 童年）
    const childTimeline = [
      {
        period: `${childBirthYear} — ${childBirthYear + 5} 年`,
        stage: '数字时代的学前生活',
        detail: `降生于中国综合国力腾飞与移动互联网时代，在家庭的照拂、早教绘本与智能终端的陪伴中步入童年。`
      },
      {
        period: `${childBirthYear + 6} — 2026 年`,
        stage: '求学岁月与同龄记忆',
        detail: `背上书包走进校园，亲历了三年疫情网课居家打卡、校外“双减”落地、中考素质教育改革，在飞速演进的时代中成长为风华少年。`
      }
    ];

    return {
      disclaimer: '基于统计规律的典型轨迹推演，非真实个人经历。不涉及 2026 年之后的任何预测。',
      child: {
        birthYear: childBirthYear,
        name: char.name,
        ageIn2026: 2026 - childBirthYear,
        timeline: childTimeline
      },
      parent: {
        birthYear: parentBirthYear,
        name: parentName,
        ageIn2026: 2026 - parentBirthYear,
        job: char.parentJob,
        timeline: parentTimeline,
        profile: {
          birthYear: parentBirthYear,
          name: parentName,
          provinceId: char.provinceId,
          cityId: char.cityId,
          urbanRural: char.urbanRural,
          sex: '男',
          ethnicity: char.ethnicity,
          childName: char.name
        }
      },
      grandparent: {
        birthYear: grandBirthYear,
        name: grandName,
        ageIn2026: 2026 - grandBirthYear,
        timeline: grandTimeline
      }
    };
  }

  /**
   * 以父母身份重新开始新一世人生（代际串联读档）
   */
  createCharacterFromParent(parentProfile) {
    this.paceMode = 'medium';
    this.history = [];
    this.statusFlags.clear();
    this.currentPendingDecision = null;
    this.isGameOver = false;
    this.deathInfo = null;

    const birthYear = parentProfile.birthYear;
    const era = this.getEraForYear(birthYear);
    const indEraKey = this.getIndustryEraKey(birthYear);

    const province = this.provinces.find(p => p.id === parentProfile.provinceId) || this.provinces[0];
    const city = this.cities.find(c => c.id === parentProfile.cityId) || this.cities[0];
    const cityDisplay = this.resolveCityDisplay(city, birthYear);

    const urbanRural = parentProfile.urbanRural || 'urban';
    const isUrban = urbanRural === 'urban';
    const sex = parentProfile.sex || '男';
    const ethnicity = parentProfile.ethnicity || '汉族';
    const name = parentProfile.name || this.generateAuthenticName(birthYear, sex, province.id, ethnicity);

    const indProfile = city.eraIndustries[indEraKey] || city.eraIndustries['era_1979_2000'];
    const typicalJobs = indProfile.typicalJobs || ['国营厂技术员', '农田社员'];
    const parentJob = typicalJobs[Math.floor(Math.random() * typicalJobs.length)];
    const familyClass = `${city.type} · ${parentJob}`;

    const attributes = {
      health: 82,
      wealth: 45,
      knowledge: isUrban ? 38 : 24,
      family: 75,
      mentality: 70
    };

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
      economicLevel: '温饱',
      siblingsCount: 2,
      attributes,
      educationLevel: '未入学',
      careerTrack: this.determineInitialCareerTrack(isUrban, city, familyClass, parentJob),
      careerRank: '初生幼年',
      occupation: isUrban ? '城镇孩童' : '乡野幼童',
      milestones: [],
      survivedDisasters: [],
      lifelineHistory: [
        {
          age: 0,
          year: birthYear,
          health: attributes.health,
          wealth: attributes.wealth,
          mentality: attributes.mentality,
          knowledge: attributes.knowledge
        }
      ],
      isInheritedParent: true,
      childName: parentProfile.childName
    };

    this.currentYear = birthYear;
    this.currentAge = 0;
    this.updateCareerStage();

    this.energy = {
      study: 25,
      work: 25,
      family: 25,
      health: 25
    };

    this.character.milestones.push({
      year: birthYear,
      age: 0,
      title: '血脉溯源',
      detail: `时光倒流回到 ${birthYear} 年。作为曾抚育【${parentProfile.childName || '子嗣'}】的父辈，你在${province.name}${cityDisplay.displayName}以【${name}】之名重新开启这充满时代激荡的一生。`
    });

    return this.character;
  }
}

// 挂载至全局
window.SimulationEngine = SimulationEngine;
