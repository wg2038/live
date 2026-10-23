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
    this.transitions = null;
    this.details = null;
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

    // 状态标记与历史事件冷却表
    this.statusFlags = new Set();
    this.eventCooldowns = {};
    this.usedDetailSnippets = new Set();
    this.detailUsage = {};
    this.lastDetailSnippet = '';
    this.lastCitySnippetDecade = null;
    this.lastSentenceOpener = '';
    this.currentPendingDecision = null;
    this.lastEraDecisionYear = -999;
  }

  /**
   * 初始化并加载全部数据（支持本地 fetch，并在跨域限制时平滑采用 embedded 回退）
   */
  async init() {
    try {
      const [provRes, statRes, evtRes, cityRes, disRes, nameRes, transRes, detRes] = await Promise.all([
        fetch('data/province.json'),
        fetch('data/stats.json'),
        fetch('data/events.json'),
        fetch('data/cities.json'),
        fetch('data/disasters.json'),
        fetch('data/naming.json'),
        fetch('data/transitions.json'),
        fetch('data/details.json')
      ]);
      this.provinces = await provRes.json();
      this.stats = await statRes.json();
      this.events = await evtRes.json();
      this.cities = await cityRes.json();
      this.disasters = await disRes.json();
      this.naming = await nameRes.json();
      this.transitions = await transRes.json();
      this.details = await detRes.json();
      this.isLoaded = true;
    } catch (err) {
      console.warn('Fetch 失败（可能由于本地 file:// 协议），采用内置回退数据', err);
      const embedded = (typeof window !== 'undefined' && window.EMBEDDED_DATA) ? window.EMBEDDED_DATA : null;
      if (embedded) {
        this.provinces = embedded.provinces || [];
        this.stats = embedded.stats || null;
        // 事件会在 prepareEventPerspectives 中被改写，必须深拷贝，
        // 否则同一个页面里多次 new SimulationEngine() 会叠加改写内置数据。
        this.events = JSON.parse(JSON.stringify(embedded.events || []));
        this.cities = embedded.cities || [];
        this.disasters = embedded.disasters || [];
        this.naming = embedded.naming || null;
        this.transitions = embedded.transitions || null;
        this.details = embedded.details || null;
        this.isLoaded = true;
      } else {
        throw new Error('无法加载历史与城市数据库');
      }
    }
    this.prepareEventPerspectives();
  }

  /**
   * 判断某个事件是否被同年的灾害系统完全遮蔽。
   * advanceYear 在灾害命中时会提前返回，不再处理事件；如果事件的省份窗口
   * 与灾害灾区完全重合，该事件就永远不会触发（1954 洪水、1976 唐山、2021 郑州）。
   */
  findShadowingDisaster(evt) {
    if (!Array.isArray(this.disasters) || !evt.exposureConditions) return null;
    const provinces = evt.exposureConditions.provinces;
    if (!Array.isArray(provinces) || provinces.length === 0) return null;
    const regions = evt.applicableRegions || ['ALL'];
    const eligibleProvinces = provinces.filter(id => {
      if (regions.includes('ALL')) return true;
      const province = (this.provinces || []).find(p => p.id === id);
      return province && regions.includes(province.region);
    });
    if (eligibleProvinces.length === 0) return null;
    for (const dis of this.disasters) {
      if (dis.year < evt.yearRange[0] || dis.year > evt.yearRange[1]) continue;
      const hit = new Set(dis.targetProvinces || []);
      if (eligibleProvinces.every(id => hit.has(id))) return dis;
    }
    return null;
  }

  /**
   * 1937 年出生起点意味着任何角色在 1937–1949 年都不可能是成年人。
   * 对“目标年龄下限超过该年份窗口内最大可能年龄”的事件，转为父辈口述的被动历史，
   * 不再把成年人的选择硬塞给儿童，也不再让这些事件永远无法触发。
   */
  prepareEventPerspectives() {
    if (!Array.isArray(this.events)) return;
    for (const evt of this.events) {
      if (!evt || !evt.targetAge || !evt.yearRange) continue;
      // 灾害年份由灾害引擎独占：把同题材事件改为灾后数年的集体记忆，
      // 否则它会被灾害分支永久遮蔽，成为死数据。
      if (this.findShadowingDisaster(evt)) {
        evt.isDecision = false;
        evt.perspective = 'disaster_aftermath';
        evt.yearRange = [evt.yearRange[0], Math.min(2026, evt.yearRange[1] + 3)];
        evt.targetAge = [0, 90];
        evt.oralHistoryNarrative = `灾后多年，亲历者仍常说起${evt.title}：${evt.historicalFact || evt.narrative || ''}`;
        evt.passiveImpact = evt.passiveImpact || { mentality: 3 };
        continue;
      }
      const latestPossibleAge = evt.yearRange[1] - 1937;
      // 只要事件窗口内所有角色都还是幼童/少年（最大可能年龄 < 14），
      // 事件里的“参军、变卖家产、主持减租”等成年人选项就不该由孩子决定；
      // 统一改为长辈口述的被动历史，让儿童以耳濡目染的方式经历时代。
      const onlyChildrenCanReach = latestPossibleAge < 14;
      if (!onlyChildrenCanReach && evt.targetAge[0] <= latestPossibleAge) continue;
      evt.isDecision = false;
      evt.perspective = 'oral_history';
      // 口述历史可以晚几年由长辈讲给孩子听，但不应把成年人的角色门槛
      // （工人/干部/商人/军人）强加给一个孩子。
      const witnessAge = Math.min(16, Math.max(0, latestPossibleAge) + 6);
      evt.targetAge = [0, witnessAge];
      evt.yearRange = [evt.yearRange[0], Math.min(2026, evt.yearRange[1] + 6)];
      evt.preTags = [];
      evt.oralHistoryNarrative = `长辈们后来常讲起${evt.title}：${evt.historicalFact || evt.narrative || ''}`;
      evt.passiveImpact = evt.passiveImpact || { mentality: 2 };
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
    // 每个队列的总出生规模 = 年均出生人口 × 队列年数，避免宽队列被窄队列压低概率。
    const cohortMass = c => (c.avgAnnualBirthM || 1) * (c.range[1] - c.range[0] + 1);
    const totalWeight = cohorts.reduce((acc, c) => acc + cohortMass(c), 0);
    let rand = Math.random() * totalWeight;
    let selectedCohort = cohorts[0];

    for (const c of cohorts) {
      const mass = cohortMass(c);
      if (rand < mass) {
        selectedCohort = c;
        break;
      }
      rand -= mass;
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
    const clean = (s) => (s || '').replace(/[（(][^）)]*[）)]/g, '').trim();
    const cleanName = clean(city.name);
    // 自治州名过长，使用“阿坝州/红河州”这类简称；普通市保留“市”字。
    const official = cleanName.includes('自治州')
      ? (city.shortName || cleanName)
      : cleanName;
    if (year < city.foundingYear && city.historicalNamePre) {
      // 民国年间不应出现“XX族自治州”这类新中国区划名，退称“XX地区”。
      let preName = clean(city.historicalNamePre);
      if (preName.includes('自治州')) {
        const base = (city.shortName || preName).replace(/自治州|州$/, '').trim();
        if (base) preName = base + '地区';
      }
      return {
        displayName: preName || official,
        isPre: true,
        officialName: city.name,
        foundingYear: city.foundingYear
      };
    }
    return {
      displayName: official,
      isPre: false,
      officialName: city.name,
      foundingYear: city.foundingYear
    };
  }

  /**
   * 随年份滚动更新城市称谓与当期主导产业。
   * 例如 1980 年出生的深圳人，出生时是宝安县，1990 年应显示深圳市；
   * 其“当地产业底色”也应从三来一补逐步切换到高新科技，而不是一生停在出生年。
   */
  refreshCityContext() {
    if (!this.character || !Array.isArray(this.cities)) return;
    const city = this.cities.find(c => c.id === this.character.cityId);
    if (!city) return;

    const cityDisp = this.resolveCityDisplay(city, this.currentYear);
    const indEraKey = this.getIndustryEraKey(this.currentYear);
    const indProfile = (city.eraIndustries && (city.eraIndustries[indEraKey] || city.eraIndustries['era_1950_1978'])) || {};

    this.character.cityHistoricalName = cityDisp.displayName;
    this.character.cityShortName = city.shortName || cityDisp.displayName;
    this.character.cityOfficialName = city.name;
    this.character.industryPillar = indProfile.pillar || this.character.industryPillar;
    this.character.industryNature = indProfile.nature || this.character.industryNature || '';
  }

  /**
   * 按照年代抽选符合史实的农村户籍生计方式（务农、集体工、手艺人、务工、基层干事等）
   */
  sampleRuralJob(indEraKey) {
    const ruralJobsByEra = {
      era_1937_1949: [
        '自耕农田劳作农户',
        '乡村租田佃农',
        '乡间走村木匠手艺人',
        '农闲车马长途脚夫',
        '村头杂粮作坊磨房工'
      ],
      era_1950_1978: [
        '人民公社生产队农田社员',
        '大队农机站拖拉机手',
        '生产大队林果副业组员',
        '公社铁木农具修配组匠人',
        '大队赤脚卫生员',
        '生产队粮秣记工员'
      ],
      era_1979_2000: [
        '包产到户承包农户',
        '乡镇企业五金装配工人',
        '第一代进城务工建筑工人',
        '乡村个体木工装潢匠人',
        '大棚温室果蔬种植户',
        '村集体副业代销点掌柜'
      ],
      era_2001_2026: [
        '外出务工建筑装饰技工',
        '现代家庭农场农机种植户',
        '乡镇快递网点配送揽收员',
        '工厂跨省务工流水线班长',
        '乡村生态果林专业户',
        '村委会基层综合办事员'
      ]
    };
    const pool = ruralJobsByEra[indEraKey] || ruralJobsByEra['era_1950_1978'];
    return pool[Math.floor(Math.random() * pool.length)];
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
    this.lastEraDecisionYear = -999;
    this.isGameOver = false;
    this.deathInfo = null;
    this.narrativeTension = 35 + Math.floor(Math.random() * 25);
    this.nextDecisionCooldownUntil = 0;

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
      const countyPool = this.cities.filter(c => c.level === 'county');
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

    // 5. 抓取该城市当期的具体产业结构与父母职业（城镇/农村户籍深度适配）
    const indProfile = city.eraIndustries[indEraKey] || city.eraIndustries['era_1950_1978'];
    let parentJob;
    if (isUrban) {
      const typicalJobs = indProfile.typicalJobs && indProfile.typicalJobs.length > 0 ? indProfile.typicalJobs : ['国营工厂职工'];
      parentJob = typicalJobs[Math.floor(Math.random() * typicalJobs.length)];
    } else {
      parentJob = this.sampleRuralJob(indEraKey);
    }
    const familyClass = this.classifyFamilyClass(parentJob, isUrban);
    const familyDetail = `${urbanRural === 'urban' ? city.type : '乡村农户'} · ${parentJob}`;

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

    const initCareerTrack = this.determineInitialCareerTrack(isUrban, city, familyClass, parentJob);
    const initialTags = new Set([
      urbanRural,
      sex === '男' ? 'male' : 'female',
      province.id,
      initCareerTrack,
      economicLevel
    ]);

    // 根据年代、地域与性别初始化生活习惯/爱好倾向
    const smokerRate = (sex === '男' ? 0.35 : 0.05) * (birthYear < 1980 ? 1.2 : 0.8);
    if (Math.random() < smokerRate) initialTags.add('smoker');
    const drinkerRate = (sex === '男' ? 0.30 : 0.08);
    if (Math.random() < drinkerRate) initialTags.add('drinker');
    if (['hubei', 'hunan', 'jiangsu', 'zhejiang', 'guangdong', 'fujian', 'jiangxi', 'anhui'].includes(province.id) && Math.random() < 0.35) {
      initialTags.add('swimmer');
    }
    if (['sichuan', 'guizhou', 'yunnan', 'shaanxi', 'gansu', 'chongqing'].includes(province.id) && Math.random() < 0.30) {
      initialTags.add('hiker');
    }
    if (birthYear >= 1980 && Math.random() < 0.25) {
      initialTags.add('stay_up_late');
    }

    this.character = {
      name,
      sex,
      ethnicity,
      birthYear,
      birthPlace: province.name,
      provinceId: province.id,
      cityId: city.id,
      cityName: city.name,
      cityShortName: city.shortName || cityDisplay.displayName,
      cityHistoricalName: cityDisplay.displayName,
      birthCityName: cityDisplay.displayName,
      cityOfficialName: city.name,
      cityType: city.type,
      cityFoundingYear: city.foundingYear,
      region: province.region,
      urbanRural,
      familyClass,
      familyDetail,
      parentJob,
      industryPillar: indProfile.pillar,
      industryNature: indProfile.nature || '',
      economicLevel,
      siblingsCount,
      attributes,
      lifeRhythm: {
        marriageBaseAge: (urbanRural === 'rural' || birthYear < 1980)
          ? 20 + Math.floor(Math.random() * 5)
          : 21 + Math.floor(Math.random() * 6),
        careerPromoteAges: [
          22 + Math.floor(Math.random() * 3),
          33 + Math.floor(Math.random() * 5),
          46 + Math.floor(Math.random() * 5)
        ]
      },
      educationLevel: '未入学',
      careerTrack: initCareerTrack,
      careerRank: '初生幼年',
      occupation: isUrban ? '城镇孩童' : '乡野幼童',
      tags: initialTags,
      causalityReview: [],
      maritalStatus: '未婚',
      hasChildren: false,
      lastChildbirthYear: null,
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

    this.eventCooldowns = {};
    this.usedDetailSnippets = new Set();
    this.detailUsage = {};
    this.lastDetailSnippet = '';
    this.lastCitySnippetDecade = null;
    this.lastSentenceOpener = '';
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
    const birthIntro = `降生于${province.name}${cityDisplay.displayName}。彼时当地正值【${city.type}】定位，以【${indProfile.pillar}】为时代重心。长辈靠【${parentJob}】维持生计，家中同辈兄弟姐妹共${siblingsCount}人。`;
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

        // 核心受灾城市（震中/直溃口）按完整灾难伤亡概率判定
        // 外围波及省份城市主要承受震感、物价冲击与后方救助，伤亡率大幅衰减至写实区间，避免百万非灾区人口异常灭绝
        const deathMult = hitCity ? 1.0 : 0.015;
        const injuryMult = hitCity ? 1.0 : 0.08;
        const familyLossMult = hitCity ? 1.0 : 0.06;
        const wealthWipeMult = hitCity ? 1.0 : 0.10;
        const rolls = dis.casualtyRoll;

        const isKilled = Math.random() < (rolls.deathProb * deathMult);
        const isInjured = !isKilled && (Math.random() < (rolls.injuryProb * injuryMult));
        const isFamilyLost = Math.random() < (rolls.familyLossProb * familyLossMult);
        const isWealthWiped = Math.random() < (rolls.wealthWipeProb * wealthWipeMult);

        return {
          disaster: dis,
          isKilled,
          isInjured,
          isFamilyLost,
          isWealthWiped,
          isHit: true,
          isPeripheral: !hitCity
        };
      }
    }
    return null;
  }

  /**
   * 检验角色是否具备指定状态标签（支持Set、statusFlags、基础属性、婚姻学历与职业别名）
   */
  characterHasTag(tag) {
    if (!tag) return true;
    // 职业轨道标签以当前 careerTrack 为准。角色转轨后旧标签仍可能留在 tags 里，
    // 不能让“曾经的教师”在转任技工多年后仍被当成教师。
    const careerTags = ['worker', 'farmer', 'cadre_teacher', 'tech_whitecollar', 'merchant', 'flexible_labor'];
    const occ = this.character.occupation || '';
    if (careerTags.includes(tag)) {
      if (this.character.careerTrack === tag) return true;
      if (tag === 'worker' && /工人|技工|车工|钳工|焊工|电工|矿工|操作工|装配|流水线|技师|机修|施工|搬运|司机|骑手/.test(occ)) return true;
      if (tag === 'farmer' && /农民|农户|社员|农耕|养殖|种植|生产队/.test(occ)) return true;
      if (tag === 'cadre_teacher' && /教师|老师|教授|讲师|校长|园长|教研|干部|公务员|科员|主任|书记|局长|科长|干事|医师|医生|护士/.test(occ)) return true;
      if (tag === 'tech_whitecollar' && /软件|程序|研发|工程师|技术员|设计师|分析师|白领/.test(occ)) return true;
      if (tag === 'merchant' && /商人|商户|店主|老板|摊|商贸|个体户|经营/.test(occ)) return true;
      return false;
    }
    // 性别与婚姻标签以当前属性为准，防止 overrides 变更后 tags 残留旧值
    if (tag === 'female' || tag === '女') return this.character.sex === '女';
    if (tag === 'male' || tag === '男') return this.character.sex === '男';
    if (tag === 'married') return this.character.maritalStatus === '已婚';
    if (tag === 'single') return this.character.maritalStatus !== '已婚';
    if (tag === 'has_children') return Boolean(this.character.hasChildren);

    if (this.character.tags && this.character.tags.has(tag)) return true;
    if (this.statusFlags.has(tag)) return true;
    if (this.character.careerTrack === tag) return true;
    if (this.character.urbanRural === tag) return true;
    if (this.character.provinceId === tag) return true;
    if (this.character.economicLevel === tag) return true;
    if (tag === 'uneducated') {
      const edu = this.character.educationLevel;
      const isNone = !edu || edu === '未入学' || edu === '文盲';
      const hasDiploma = this.character.tags && (this.character.tags.has('status_literate') || this.character.tags.has('status_high_school_diploma') || this.character.tags.has('status_college_diploma') || this.character.tags.has('primary') || this.character.tags.has('junior_high') || this.character.tags.has('high_school'));
      if (isNone && !hasDiploma) return true;
    }
    const eduLevel = this.character.educationLevel || '';
    const isDegree = /大学本科|大专学历|本科|硕士|博士|研究生/.test(eduLevel) && !/在读/.test(eduLevel);
    if (tag === 'primary' && /小学|初小|高小|识字班/.test(eduLevel) && !/初中/.test(eduLevel)) return true;
    if (tag === 'junior_high' && /初中|初级中学/.test(eduLevel)) return true;
    if (tag === 'high_school' && /高中|普通高中|完中|中专|中职|技校|中等专业/.test(eduLevel) && !/高等院校|大学|大专/.test(eduLevel)) return true;
    if (tag === 'college' && /大学|本科|大专|专科|研究生|硕士|博士|高等院校/.test(eduLevel)) return true;
    if (tag === 'higher_ed_degree' && isDegree) return true;
    return false;
  }

  /**
   * 检验角色是否满足事件的曝光条件 (exposureConditions)
   */
  characterMeetsExposure(exposure) {
    if (!exposure || Object.keys(exposure).length === 0) return true;
    if (exposure.provinces && exposure.provinces.length > 0) {
      if (!exposure.provinces.includes(this.character.provinceId) && !exposure.provinces.includes('ALL')) {
        return false;
      }
    }
    if (exposure.urbanRural && exposure.urbanRural !== 'all') {
      if (exposure.urbanRural !== this.character.urbanRural) return false;
    }
    if (exposure.economicLevels && exposure.economicLevels.length > 0) {
      if (!exposure.economicLevels.includes(this.character.economicLevel)) return false;
    }
    if (exposure.minYear && this.currentYear < exposure.minYear) return false;
    if (exposure.maxYear && this.currentYear > exposure.maxYear) return false;
    return true;
  }

  /**
   * 子职业精准锚定（Sub-Occupation Guard）：校验 trajectory 职业事件是否与当前具体工种相符
   */
  characterMatchesTrajectoryEvent(evt) {
    if (!evt || evt.tier !== 'trajectory') return true;
    const char = this.character;
    if (!char) return false;
    const occ = char.occupation || '';
    const track = char.careerTrack || '';
    const provId = char.provinceId || '';
    const city = this.cities ? this.cities.find(c => c.id === char.cityId) : null;
    const isHeavyIndustryCity = (city && city.type === '重工业资源型') || (char.cityType === '重工业资源型');

    switch (evt.id) {
      case 'evt_traj_yihu_jizhen':
        // 医院急诊：仅限 occupation 含 医|护|卫|大夫 或拥有 doctor/nurse/barefoot_doctor 标签者触发（禁止普通中小学教师/校长触发）
        if (/医|护|卫|大夫/.test(occ)) return true;
        if (this.characterHasTag('doctor') || this.characterHasTag('nurse') || this.characterHasTag('barefoot_doctor')) return true;
        return false;

      case 'evt_traj_jiaoshi_yanyan':
        // 乡村讲台：仅限 occupation 含 教|师|校|督学 者触发
        if (/教|师|校|督学/.test(occ)) return true;
        return false;

      case 'evt_traj_xiaofang_jiuyuan':
        // 火场逆行：仅限拥有 military/firefighter 标签或 occupation 含 消防|救援|武警|安全 者触发（禁止普通车工/教师触发）
        if (this.characterHasTag('military') || this.characterHasTag('firefighter')) return true;
        if (/消防|救援|武警|安全/.test(occ)) return true;
        return false;

      case 'evt_traj_kuangong_fengxian':
        // 地下采掘：仅限 occupation 含 矿|采掘|井 或重工业资源型城市工矿工人触发
        if (/矿|采掘|井/.test(occ)) return true;
        if (isHeavyIndustryCity && (track === 'worker' || /工/.test(occ))) return true;
        return false;

      case 'evt_traj_qishou_fengyu':
        // 配送骑手：仅限 careerTrack === 'flexible_labor' 或 occupation 含 骑手|配送|快递|外卖 者触发
        if (track === 'flexible_labor') return true;
        if (/骑手|配送|快递|外卖/.test(occ)) return true;
        return false;

      case 'evt_traj_huoche_pilao':
        // 长途货运：仅限 careerTrack === 'flexible_labor' 或 occupation 含 司机|货运|跟车|车队 者触发
        if (track === 'flexible_labor') return true;
        if (/司机|货运|跟车|车队/.test(occ)) return true;
        return false;

      case 'evt_traj_yumin_fenglang':
        // 远洋捕捞：仅限沿海省份（广东、福建、浙江、山东、辽宁、海南、广西、江苏）的农村/渔民/工人触发，内陆省份农民严禁出海捕鱼
        const coastalProvinces = ['guangdong', 'fujian', 'zhejiang', 'shandong', 'liaoning', 'hainan', 'guangxi', 'jiangsu'];
        if (!coastalProvinces.includes(provId)) return false;
        if (char.urbanRural === 'rural' || track === 'farmer' || track === 'worker' || /渔|船|水产|工|海/.test(occ)) return true;
        return false;

      case 'evt_traj_chengxuyuan_996':
        if (track === 'tech_whitecollar' || /软件|程序|研发|算法|IT|科技|代码/.test(occ)) return true;
        return false;

      case 'evt_traj_getihu_jingying':
        if (track === 'merchant' || /商|店|摊|贸|个体/.test(occ)) return true;
        return false;

      case 'evt_traj_jianzhu_gaokong':
        if (track === 'worker' || /工|建筑|瓦|架|吊/.test(occ)) return true;
        return false;

      case 'evt_traj_nongye_laoshun':
        if (track === 'farmer' || char.urbanRural === 'rural' || /农|田|社|耕/.test(occ)) return true;
        return false;

      default:
        return true;
    }
  }

  /**
   * 判定某时代事件是否与当前角色身份/地域构成“核心碰撞”
   */
  isEraCoreCollision(evt) {
    if (!evt || evt.tier !== 'era') return false;
    const char = this.character;
    if (!char) return false;
    const occ = char.occupation || '';
    const track = char.careerTrack || '';
    const provId = char.provinceId || '';
    const cityName = char.cityName || '';
    const year = this.currentYear;

    // 1978 小岗村之于安徽农民
    if (evt.id === 'evt_1978_xiaogang_dabaogan' || (year >= 1978 && year <= 1982 && /小岗|包产到户|大包干/.test(evt.title))) {
      if (provId === 'anhui' && (char.urbanRural === 'rural' || track === 'farmer')) return true;
    }

    // 1990/1992 认购证/证券之于沪深市民
    if (evt.id === 'evt_1990_shanghai_zhengquan' || evt.id === 'evt_1992_shenzhen_rengouzheng' || evt.id === 'evt_1978_1999_d1_rengouzheng' || /认购证|上海证券交易所/.test(evt.title)) {
      if ((provId === 'shanghai' || provId === 'guangdong' || cityName.includes('上海') || cityName.includes('深圳')) && char.urbanRural === 'urban') {
        return true;
      }
    }

    // 1998 下岗潮之于东北国企工人
    if (evt.id === 'evt_1998_xiagangchao' || (/下岗/.test(evt.id) && evt.tier === 'era')) {
      if (char.region === '东北' && (track === 'worker' || /工/.test(occ))) return true;
    }

    // 专属特定省市事件碰撞 (非 ALL)
    if (evt.applicableRegions && !evt.applicableRegions.includes('ALL')) {
      const hitsProv = evt.applicableRegions.includes(provId) || evt.applicableRegions.includes(char.region);
      const hitsUrban = (evt.applicableRegions.includes('URBAN') && char.urbanRural === 'urban') ||
                        (evt.applicableRegions.includes('RURAL') && char.urbanRural === 'rural');
      if (hitsProv && hitsUrban) return true;
    }

    return false;
  }

  /**
   * 检查当年是否有待触发的历史大事件（严格遵循曝光条件、冷却期、前置与排除标签）
   */
  findEligibleEvents() {
    const list = [];
    for (const evt of this.events) {
      // 冷却期检查
      if (this.eventCooldowns[evt.id] && this.currentYear < this.eventCooldowns[evt.id]) {
        continue;
      }
      if (this.statusFlags.has(`done_${evt.id}`)) {
        continue;
      }

      // 年份窗口
      const [start, end] = evt.yearRange;
      if (this.currentYear < start || this.currentYear > end) continue;

      // 适用年龄
      if (evt.targetAge) {
        const [minAge, maxAge] = evt.targetAge;
        if (this.currentAge < minAge || this.currentAge > maxAge) continue;
      }

      // 地域覆盖
      if (evt.applicableRegions && !evt.applicableRegions.includes('ALL')) {
        let regionMatch = false;
        if (evt.applicableRegions.includes(this.character.region)) regionMatch = true;
        if (evt.applicableRegions.includes('URBAN') && this.character.urbanRural === 'urban') regionMatch = true;
        if (evt.applicableRegions.includes('RURAL') && this.character.urbanRural === 'rural') regionMatch = true;
        if (!regionMatch) continue;
      }

      // 曝光条件
      if (!this.characterMeetsExposure(evt.exposureConditions)) continue;

      // 职业专属 trajectory 精准校验 (子职业精准锚定，根治跨行串戏)
      if (evt.tier === 'trajectory') {
        if (!this.characterMatchesTrajectoryEvent(evt)) continue;
      }

      // 特殊生育事件校验：全面二孩与三孩政策必须已婚已育
      if (evt.id === 'evt_2016_quanmian_erhai') {
        const isMarried = this.characterHasTag('married');
        const hasChild = this.characterHasTag('has_children') || (this.character && this.character.hasChildren);
        if (!isMarried || !hasChild) continue;
      }
      if (evt.id === 'evt_2021_san_hai_zhengce') {
        const isMarried = this.characterHasTag('married');
        const hasChild = this.characterHasTag('has_children') || this.characterHasTag('two_children_family') || (this.character && this.character.hasChildren);
        if (!isMarried || !hasChild) continue;
      }

      // 前置标签默认表示“符合任一身份即可”（工人或教师或商户）。
      // 带性别标签或婚育复合标签的组合才要求全部满足。
      // 旧逻辑把所有列表都当 AND，导致 ["worker","cadre_teacher"] 这类事件永远不可达。
      if (evt.preTags && evt.preTags.length > 0) {
        const requiresAll = evt.preTags.includes('female') || evt.preTags.includes('male') ||
          (evt.preTags.includes('married') && evt.preTags.includes('has_children'));
        const match = requiresAll
          ? evt.preTags.every(t => this.characterHasTag(t))
          : evt.preTags.some(t => this.characterHasTag(t));
        if (!match) continue;
      }

      // 互斥排除标签 (任一命中即排除)
      if (evt.excludeTags && evt.excludeTags.length > 0) {
        let anyMatch = false;
        for (const t of evt.excludeTags) {
          if (this.characterHasTag(t)) {
            anyMatch = true;
            break;
          }
        }
        if (anyMatch) continue;
      }

      list.push(evt);
    }
    return list;
  }

  /**
   * 从已通过触发概率筛选的候选中按事件权重抽取一个。
   * 旧逻辑永远取数组第一个，排在低概率“时代切片”事件前面的高概率事件
   * 会年复一年把后者饿死，导致事件库覆盖长期停滞。
   */
  pickEventCandidate(candidates) {
    if (!candidates || candidates.length === 0) return null;
    if (candidates.length === 1) return candidates[0];
    // triggerProbability 已经在这一步之前决定“今年是否发生”，
    // 这里若再按概率加权，低概率事件会被重复惩罚而永不触发。
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  /**
   * 刚性学业节点检测（小升初/中考分流、高考、启蒙入学）：不受张力门控
   */
  checkRigidSchoolMilestone() {
    const age = this.currentAge;
    const isLateBorn = this.character && this.character.birthYear >= 2010;

    // 针对 2010 年及以后出生的新时代少儿：中考分流关口
    if (isLateBorn) {
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
              choiceTags: ['时代：普职分流', '年龄：14–16', '地域：全国', '门槛：应试奋进学子'],
              effect: { "knowledge": 30, "health": -10, "mentality": -5 },
              log: '挑灯夜战刷完几十套模拟卷，顺利拿到重点高中录取通知书，迈入人生新起点。'
            },
            {
              text: '报考艺术特长或特色职业技术院校',
              choiceTags: ['时代：多元成才', '年龄：14–16', '地域：全国', '门槛：特长与职教路线'],
              effect: { "mentality": 15, "wealth": 10, "knowledge": 10 },
              log: '结合自身爱好走向特色技能赛道，卸下过重考学包袱，走上一条踏实务实之路。'
            }
          ]
        };
      }
      return null;
    }

    const isCompulsoryEra = this.character.birthYear >= 1980 || this.currentYear >= 1986;

    if (isCompulsoryEra) {
      // 15–16岁：中考分流关口
      if (age >= 15 && age <= 16 && (this.character.educationLevel === '初中在读' || this.character.tags.has('junior_high')) && !this.statusFlags.has('decision_zhongkao_fenliu')) {
        this.statusFlags.add('decision_zhongkao_fenliu');
        return {
          id: 'node_zhongkao_fenliu',
          title: '中考分流：普高与职教技校十字路口',
          isDecision: true,
          narrative: `初三中考放榜在即，面对普职分流的现实分水岭，教室里的空气格外凝重。摆在面前的是两条迥然不同的人生赛道。`,
          choices: [
            {
              text: '全力冲刺重点普高，志在三年后参加高考',
              choiceTags: ['时代：现代教育', '年龄：15–16', '地域：全国', '门槛：学术考学追求者'],
              outcomes: [
                { type: 'safe', weight: 80, log: '中考成绩优异被重点示范性普通高中录取，进入高强度题海冲刺高考。', effect: { knowledge: 25, mentality: 10, health: -5 }, status: 'high_school_student', hiddenRiskLog: '顺利考入重点高中，叩开通往全日制高等学府的大门。' },
                { type: 'safe', weight: 20, log: '压线被普通高中普通班录取，虽然底子偏弱但依然保留高考冲刺机会。', effect: { knowledge: 15, mentality: 5 }, status: 'high_school_student', hiddenRiskLog: '勉强踏入普通高中门槛，需在高中三年加倍发奋苦读。' }
              ]
            },
            {
              text: '报考特色职业技术学校或中专，专攻实用立身技能',
              choiceTags: ['时代：现代教育', '年龄：15–16', '地域：全国', '门槛：技能实践导向者'],
              outcomes: [
                { type: 'safe', weight: 90, log: '入读中专职校王牌专业，扎实掌握一门过硬实操手艺，毕业后直通对口单位。', effect: { wealth: 15, mentality: 15, knowledge: 10 }, status: 'vocational_student', hiddenRiskLog: '早学一技之长立足社会，避开高考内卷走出务实道路。' },
                { type: 'safe', weight: 10, log: '在职校期间表现突出，代表学校参加全省技能大赛获二等奖。', effect: { knowledge: 20, wealth: 10 }, status: 'vocational_student', hiddenRiskLog: '职校磨砺出精湛技能，成为行业骨干后备力量。' }
              ]
            }
          ]
        };
      }

      // 18–19岁：高考关口；复读生 19–20 岁可再考一次
      const isGaokaoRetry = age >= 19 && age <= 20 &&
        this.statusFlags.has('repeating_gaokao') &&
        !this.statusFlags.has('decision_gaokao_retry');
      if ((age >= 18 && age <= 19 && (this.character.tags.has('high_school_student') || this.character.educationLevel === '普通高中') && !this.statusFlags.has('decision_gaokao_jueze')) || isGaokaoRetry) {
        if (isGaokaoRetry) this.statusFlags.add('decision_gaokao_retry');
        else this.statusFlags.add('decision_gaokao_jueze');
        return {
          id: isGaokaoRetry ? 'node_gaokao_retry' : 'node_gaokao_jueze',
          title: isGaokaoRetry ? '高四复读：再战六月考场' : '六月高考：千军万马过独木桥',
          isDecision: true,
          narrative: `蝉鸣夏日的考场外围满了焦急翘首的家长。十二载寒窗苦读换来黑板上的倒计时归零，考卷翻动的沙沙声叩响人生转折大门。`,
          choices: [
            {
              text: '冲击全日制本科院校（若失利则调剂专科）',
              choiceTags: ['时代：高考时代', '年龄：18–19', '地域：全国', '门槛：普高应届毕业生'],
              outcomes: [
                { type: 'safe', weight: 55, log: '发挥沉稳超常发挥，顺利被全日制本科大学录取，跨入高等学府象牙塔。', effect: { knowledge: 35, mentality: 20, wealth: -15 }, status: 'college_degree', hiddenRiskLog: '金榜题名迈入本科高校，为一生学术与职业奠定最高底色。' },
                { type: 'safe', weight: 35, log: '考分略有遗憾但被省属公办高等专科学校王牌专业录取，学制三年。', effect: { knowledge: 20, mentality: 10, wealth: -10 }, status: 'junior_college_degree', hiddenRiskLog: '入读高职大专踏实修习，为后续专升本或高薪就业铺路。' },
                { type: 'redirected', weight: 10, log: '发挥失常痛定思痛决定在县一中复读高四再战一年。', effect: { knowledge: 10, mentality: -10, health: -5 }, status: 'repeating_gaokao', hiddenRiskLog: '背水一战选择复读高四，经历常人难忍的精神洗礼。' }
              ]
            },
            {
              text: '放弃升学直接进入社会就业创业，早日自立减轻家庭负担',
              choiceTags: ['时代：通用时代', '年龄：18–20', '地域：全国', '门槛：自立打拼者'],
              outcomes: [
                { type: 'safe', weight: 85, log: '脱离书卷投身社会大熔炉，在同乡引荐下入职当地骨干企业或商贸实体。', effect: { wealth: 25, mentality: 15, family: 15 }, status: 'early_employment', hiddenRiskLog: '早早步入社会自食其力，在摸爬滚打中积累人情世故与第一桶金。' },
                { type: 'safe', weight: 15, log: '敏锐捕捉商机在批发市场支起摊位自力更生，当月实现盈利扭亏。', effect: { wealth: 35, mentality: 20 }, status: 'early_merchant', hiddenRiskLog: '青年下海敢为人先，自主创业走出一番天地。' }
              ]
            }
          ]
        };
      }
    } else {
      // 1980年前出生者：适龄读书与做工抉择 (6-8岁)
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
              choiceTags: ['时代：前义务教育', '年龄：6–8', '地域：全国', '门槛：求学向进者'],
              outcomes: [
                { type: 'safe', weight: 100, log: '在贫瘠与困顿中坚持念书，背着用粗布缝合的书包迈进学堂。', effect: { knowledge: 25, wealth: -10, health: 5 }, status: 'primary', hiddenRiskLog: '启蒙读书识字明理，彻底摆脱文盲困境。' }
              ]
            },
            {
              text: '早早辍学务农或当学徒做工',
              choiceTags: ['时代：前义务教育', '年龄：6–8', '地域：全国', '门槛：生计所迫者'],
              outcomes: [
                { type: 'redirected', weight: 100, log: `懂事地辍学帮衬家门，在${this.character.industryPillar}的尘土中流下第一滴汗水。`, effect: { wealth: 15, family: 15, knowledge: -10 }, status: 'status_dropped_out', hiddenRiskLog: '年幼失学过早步入劳作，文化水平受限成为一生憾事。' }
              ]
            }
          ]
        };
      }
    }

    return null;
  }

  createMarriageDecisionNode() {
    return {
      id: 'node_marriage',
      tier: 'life_chain',
      title: '成家立业关口',
      isDecision: true,
      narrative: `行至青年成家关口，媒人提亲或与心仪之人相知提上了日程。需置办聘礼家具，这是人生的一大转折点。`,
      choices: [
        {
          text: '依照习俗顺理成章成家完婚',
          choiceTags: ['时代：传统婚恋', '年龄：20–38', '地域：全国', '门槛：适龄青年'],
          outcomes: [
            { type: 'safe', weight: 90, log: '按当年规制办了喜酒成家立业，夫妻相濡以沫操持生计。', effect: { family: 25, wealth: -15, mentality: 10 }, status: 'married', hiddenRiskLog: '寻得终身伴侣喜结连理，携手抵御人间风雨。' },
            { type: 'safe', weight: 10, log: '喜结良缘且夫妻双方勤俭持家，小家庭积蓄蒸蒸日上。', effect: { family: 35, wealth: 10, mentality: 15 }, status: 'married', hiddenRiskLog: '得遇贤能良偶，齐心协力改善家境。' }
          ]
        },
        {
          text: '推迟婚期，专心打拼本职或求学',
          choiceTags: ['时代：事业优先', '年龄：20–38', '地域：全国', '门槛：打拼奋斗者'],
          outcomes: [
            { type: 'safe', weight: 100, log: '暂缓个人婚事，把满腔热忱投入到本职工作与打拼当中。', effect: { knowledge: 15, wealth: 15, family: -10 }, hiddenRiskLog: '暂缓成家立业，积蓄个人实力等待更佳良缘。' }
          ]
        }
      ]
    };
  }

  createMedicalDecisionNode() {
    return {
      id: 'node_medical',
      tier: 'contingency',
      title: '顽疾缠身与就医抉择',
      isDecision: true,
      narrative: `常年劳累积下重病，近来胸闷咳喘剧烈。大夫建议住院系统检查治疗，但这需要动用家中全部积蓄。`,
      choices: [
        {
          text: '动用全部积蓄积极住院治疗',
          choiceTags: ['时代：医疗救治', '年龄：48–65', '地域：全国', '门槛：重病患者'],
          outcomes: [
            { type: 'safe', weight: 85, log: '四处借钱并动用积蓄积极就医，病情得以控制稳定。', effect: { health: 25, wealth: -30, mentality: 10 }, hiddenRiskLog: '倾尽积蓄治愈恶疾，虽耗光钱财但保住宝贵生命。' },
            { type: 'injured', weight: 15, log: '住院手术历经凶险虽保住性命，但需常年服药调养。', effect: { health: 15, wealth: -40 }, hiddenRiskLog: '大病初愈落下慢性病根，需谨遵医嘱长期调理。' }
          ]
        },
        {
          text: '抓草药硬扛，把钱留给儿女开销',
          choiceTags: ['时代：保守求生', '年龄：48–65', '地域：全国', '门槛：省吃俭用者'],
          outcomes: [
            { type: 'injured', weight: 80, log: '不忍拖累家人选择硬撑苦挨，身体逐渐落下严重宿疾。', effect: { health: -20, family: 15, wealth: 5 }, hiddenRiskLog: '舍身顾念家庭延误医治，身体机能不可逆衰退。' },
            { type: 'fatal', weight: 20, log: '病情迅速恶化引发全身感染多器官衰竭，抢救无效溘然长逝。', isFatal: true, hiddenRiskLog: '重病延误医治不幸早逝。' }
          ]
        }
      ]
    };
  }

  createDarkestHourDecisionNode() {
    return {
      id: 'node_darkest_hour',
      tier: 'contingency',
      title: '人生至暗时刻：深渊边缘的寒夜',
      isDecision: true,
      historicalFact: '生活中总有些绝境，万念俱灰的重压几乎要将人彻底碾碎。这是人性的深渊，也是尊严、责任与执念的最后拷问。',
      narrative: '催债的电话在静音震动中闪烁不休，门缝里塞满了红色的律师函与催缴单。深冬的寒风呼呼灌进毛坯房的窗洞，你在桥头长椅上枯坐了整整一夜，烟头散落一地。前半生的心血与尊严碎成齑粉，桥下冰冷的黑水在夜色中泛着刺骨幽光。',
      choices: [
        {
          text: '万念俱灰，松开栏杆走入冰冷黑夜（绝境弃生）',
          choiceTags: ['时代：深渊时刻', '门槛：极度绝望者'],
          outcomes: [
            { type: 'fatal', weight: 100, isFatal: true, log: '心力枯竭，在无尽的黑暗与深渊面前永远闭上了双眼。', hiddenRiskLog: '在人生的至暗绝境中走完了一生。' }
          ]
        },
        {
          text: '嚼碎屈辱，哪怕出尽苦力也要替家人还债（负重苟活）',
          choiceTags: ['时代：深渊时刻', '门槛：坚韧求生者'],
          outcomes: [
            { type: 'safe', weight: 100, log: '在桥头痛哭一场后咬碎牙关擦干眼泪，哪怕脱掉长衫出尽苦力，也要替家门把债还清。', effect: { health: -25, wealth: 10, mentality: 25 }, hiddenRiskLog: '嚼碎绝望重新站起，在最苦最累的生计中重塑尊严。' }
          ]
        },
        {
          text: '推开破旧老屋柴门，父母的一碗热汤将自己从悬崖边缘拉回（至亲救赎）',
          choiceTags: ['时代：深渊时刻', '门槛：亲情羁绊者'],
          outcomes: [
            { type: 'safe', weight: 100, log: '在老母亲颤抖递来的一碗热汤面面前抱头痛哭，认栽还乡，在亲情庇护下捡回一条命。', effect: { family: 20, mentality: 35 }, hiddenRiskLog: '在血脉至亲的包容与温暖中重拾活下去的勇气。' }
          ]
        }
      ]
    };
  }

  /**
   * 人生重要抉择节点（向下兼容单测 direct call）
   */
  checkLifeMilestone() {
    const rigid = this.checkRigidSchoolMilestone();
    if (rigid) return rigid;

    const age = this.currentAge;
    const isLateBorn = this.character && this.character.birthYear >= 2010;

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
              choiceTags: ['时代：新时代少儿', '年龄：6–8', '地域：全国', '门槛：重视素质启蒙家庭'],
              effect: { "knowledge": 20, "wealth": -15, "health": -5 },
              log: '周末穿梭于各个校外培训班，虽略显疲累，但眼界与思维打下了扎实基础。'
            },
            {
              text: '坚持快乐童年，多跑跳户外运动',
              choiceTags: ['时代：新时代少儿', '年龄：6–8', '地域：全国', '门槛：崇尚天性自然家庭'],
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
              choiceTags: ['时代：数字时代', '年龄：10–12', '地域：全国', '门槛：自律求知学童'],
              effect: { "knowledge": 25, "mentality": 10, "health": -5 },
              log: '抵制住了游戏短视频诱惑，利用数字终端汲取海量知识，成绩名列前茅。'
            },
            {
              text: '沉迷手机游戏与短视频，熬夜摸鱼',
              choiceTags: ['时代：数字时代', '年龄：10–12', '地域：全国', '门槛：数字娱乐沉浸者'],
              effect: { "mentality": 15, "health": -10, "knowledge": -10 },
              log: '在虚拟网络世界中获得极高满足感，但也让视力下降，课业偶有落伍。'
            }
          ]
        };
      }
    }

    const rhythm = this.character && this.character.lifeRhythm;
    const marriageBaseAge = (rhythm && rhythm.marriageBaseAge) ? rhythm.marriageBaseAge : 22;
    const gradYear = (this.character && this.character.collegeGraduationYear) || 0;
    const inHigherEd = (gradYear && this.currentYear <= gradYear) || (this.character && this.character.educationLevel === '高等院校在读');
    const gradAge = gradYear ? (gradYear - this.character.birthYear) : 0;
    const effectiveMarriageAge = Math.max(marriageBaseAge, gradAge ? (gradAge + 1) : 0);

    if (!inHigherEd && age >= effectiveMarriageAge && age <= 38 && this.character.maritalStatus !== '已婚') {
      const isMarriageCooling = (this.eventCooldowns['node_marriage'] && this.currentYear < this.eventCooldowns['node_marriage']) ||
                                (this.eventCooldowns['evt_life_xiangqin_jiehun'] && this.currentYear < this.eventCooldowns['evt_life_xiangqin_jiehun']);
      if (!isMarriageCooling) {
        return this.createMarriageDecisionNode();
      }
    }

    if (age >= 48 && age <= 65 && this.character.attributes.health < 45 && !this.statusFlags.has('decision_medical')) {
      return this.createMedicalDecisionNode();
    }

    if (age >= 20 && this.character.attributes.mentality < 22 && this.character.attributes.wealth < 20 && !this.statusFlags.has('decision_darkest_hour')) {
      return this.createDarkestHourDecisionNode();
    }

    return null;
  }

  /**
   * 计算角色当年的真实死亡概率（真实时代基准 + 产业职业病风险 + 精力护体）
   */
  calculateAnnualMortalityRate(era) {
    const age = this.currentAge;

    // 时代宏观生命表换算（以中国现代化时期1990-2000预期寿命约69岁为锚点 1.0）
    // 1937年(抗战，预期寿命35) -> eraFactor ≈ 2.85
    // 1950年(建国初，预期寿命46.5) -> eraFactor ≈ 1.85
    // 1970年(文革后期，预期寿命63.5) -> eraFactor ≈ 1.15
    // 2014年(新时代，预期寿命77.3) -> eraFactor ≈ 0.70
    // 2026年(现代，预期寿命78.6) -> eraFactor ≈ 0.65
    const eraLifeExp = era.lifeExpectancy || 68;
    const eraFactor = Math.max(0.55, Math.min(3.2, Math.pow(69 / eraLifeExp, 1.6)));

    let baseRate = 0.001;

    // 分年龄段真实生命表基准率（参考国家统计局分年龄死亡率生命表，乘以时代修正系数）
    if (age === 0) {
      // 婴儿死亡率（0岁至1周岁前）
      baseRate = (era.infantMortality || 50) / 1000.0;
    } else if (age < 5) {
      // 1-4岁幼儿期（死亡率回归幼儿正常生命表基准）
      baseRate = 0.0012 * eraFactor;
    } else if (age < 15) {
      baseRate = 0.0005 * eraFactor;
    } else if (age < 30) {
      baseRate = 0.0008 * eraFactor;
    } else if (age < 45) {
      baseRate = 0.0015 * eraFactor;
    } else if (age < 60) {
      baseRate = 0.0055 * eraFactor;
    } else if (age < 70) {
      baseRate = 0.0160 * eraFactor;
    } else if (age < 80) {
      baseRate = 0.0450 * eraFactor;
    } else if (age < 90) {
      baseRate = 0.1200 * eraFactor;
    } else {
      baseRate = 0.2600 * eraFactor;
    }

    // 2. 健康属性指数调节
    const health = this.character.attributes.health;
    let healthFactor = 1.0;
    if (health <= 0) return 1.0;
    if (health < 20) healthFactor = 5.0;
    else if (health < 40) healthFactor = 2.5;
    else if (health < 60) healthFactor = 1.3;
    else if (health > 80) healthFactor = 0.6;

    // 3. 玩家“健康/休养”精力分配抵御调节
    const healthEnergyBonus = 1.0 - (this.energy.health / 100) * 0.45;

    // 4. 城市产业特定职业病与污染风险 (如石棉、煤矿尘肺)
    let industryRiskBonus = 1.0;
    const city = this.cities.find(c => c.id === this.character.cityId);
    if (city && city.riskModifiers) {
      if (city.riskModifiers.dustDisease && age >= 35 && (this.character.tags.has('worker') || this.character.tags.has('heavy_industry'))) {
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
    const city = this.cities.find(c => c.id === this.character.cityId);
    const cityRisk = (city && city.riskModifiers) || {};

    if (this.currentYear >= 1998 && this.currentYear <= 2000 && this.currentAge >= 28 && this.currentAge <= 55) {
      const shock = cityRisk.xiagang1998 || 1;
      if (shock > 1) {
        attr.wealth = Math.max(10, attr.wealth - Math.round(3 * shock * stepYears));
        attr.mentality = Math.max(10, attr.mentality - Math.round(2 * shock * stepYears));
      }
    }

    // 2001 入世红利：沿海外贸与民营轻工城市获得订单与就业扩张，农业主产区则承受进口冲击
    if (this.currentYear >= 2001 && this.currentYear <= 2007 && this.currentAge >= 20 && this.currentAge <= 60) {
      // wtoBoom2001 越高代表当地外贸/轻工订单扩张越强；越低代表受进口冲击越重。
      const wto = cityRisk.wtoBoom2001 || 1;
      if (wto >= 1.4) {
        attr.wealth += Math.round(2 * stepYears);
        attr.mentality += Math.round(1 * stepYears);
      } else if (wto <= 0.8) {
        attr.wealth = Math.max(10, attr.wealth - Math.round(1 * stepYears));
        attr.mentality = Math.max(10, attr.mentality - Math.round(1 * stepYears));
      }
    }

    // 2020-2022 疫情静默与供应链受阻对实体商贸、外贸民营及务工的冲击
    if (this.currentYear >= 2020 && this.currentYear <= 2022 && this.currentAge >= 20 && this.currentAge <= 65) {
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
   * 按当前家产刷新经济水平。
   * economicLevel 原先只在出生时按一次随机数写死，之后无论贫富都不再变化，
   * 导致“贫困”标签和结局面板与角色一生的实际财富脱节。
   */
  updateEconomicLevel() {
    if (!this.character || !this.character.attributes) return;
    const wealth = this.character.attributes.wealth;
    const next = wealth < 25 ? '贫困' : wealth < 50 ? '温饱' : wealth < 70 ? '小康' : '富裕';
    if (next === this.character.economicLevel) return;
    if (this.character.tags) {
      for (const level of ['贫困', '温饱', '小康', '富裕']) this.character.tags.delete(level);
      this.character.tags.add(next);
    }
    this.character.economicLevel = next;
  }

  /**
   * 把父母的具体职业归入家庭成分。
   * familyClass 曾经被写成“城市类型 · 职业”的展示串，导致
   * `familyClass === '干部'/'知识分子'/'商人'/'工人'` 四个判断永远是 false，
   * 教师、医生、机关干部的孩子会被随机归入工人轨道。
   */
  classifyFamilyClass(parentJob, isUrban) {
    if (!isUrban) return '农民';
    const job = parentJob || '';
    if (/教师|教授|讲师|教员|研究员|科研|学者|医生|医师|护士|律师|记者|编辑|作家|工程师|技术员|设计师|会计/.test(job)) {
      return '知识分子';
    }
    if (/干部|公务|机关|书记|主任|科长|局长|干事|督导|代表|党员|军人|警察|社区/.test(job)) {
      return '干部';
    }
    if (/商|贩|铺|老板|掌柜|倒爷|个体|店主|贸|销售|运营|主播|货代|报关|批发|电商|客栈|金融|投资|经理|总监/.test(job)) {
      return '商人';
    }
    return '工人';
  }

  /**
   * 初生职业轨道推演判定
   */
  determineInitialCareerTrack(isUrban, city, familyClass, parentJob) {
    if (!isUrban) return 'farmer';
    const family = ['干部', '知识分子', '商人', '工人'].includes(familyClass)
      ? familyClass
      : this.classifyFamilyClass(parentJob, isUrban);
    if (family === '干部' || family === '知识分子') return 'cadre_teacher';
    if (family === '商人') return 'merchant';
    return 'worker';
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

    // 1. 学历毕业结算与动态轨道迁跃
    // 高考录取只记录“入学与毕业年份”，到毕业年才结算学位；在读期间不得提前写成大学本科。
    if (char.collegeGraduationYear && year >= char.collegeGraduationYear && !flags.has('college_graduate')) {
      flags.add('college_graduate');
      char.educationLevel = char.degreeType === '大专' ? '大专学历' : '大学本科';
      char.tags.add('higher_ed_degree');
    }
    if (flags.has('college_graduate')) {
      if (year >= 2000 && (char.cityType === '综合科教中心' || energy.study >= 30)) {
        char.careerTrack = 'tech_whitecollar';
      } else {
        char.careerTrack = 'cadre_teacher';
      }
      if (!char.educationLevel || char.educationLevel === '高等院校在读') {
        char.educationLevel = char.degreeType === '大专' ? '大专学历' : '大学本科';
      }
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
    // 1986 年义务教育法实施后（或 1980 年后出生）才有稳定的直升初中路径。
    const isCompulsoryEra = char.birthYear >= 1980 || year >= 1986;

    // 读取个性化生命节律晋升年龄与属性门槛
    const promoteAges = (char.lifeRhythm && Array.isArray(char.lifeRhythm.careerPromoteAges))
      ? char.lifeRhythm.careerPromoteAges
      : [22, 35, 48];
    const p1 = promoteAges[0] || 22;
    const p2 = promoteAges[1] || 35;
    const p3 = promoteAges[2] || 48;
    const meetsHighThreshold = Boolean(attr && ((attr.knowledge >= 55) || (attr.wealth >= 55)));

    // (A) 幼年期 (0-5岁)
    if (age <= 2) {
      title = isUrban ? '城镇乳儿' : '乡野乳儿';
    } else if (age <= 5) {
      title = isUrban ? '城镇幼童' : '乡野幼童';
    }
    // (B) 少年求学与帮工期 (6-14岁)
    else if (age <= 14) {
      const isEnrolled = char.tags.has('primary') || char.tags.has('junior_high') || char.educationLevel === '小学在读' || char.educationLevel === '初中在读';

      if (flags.has('status_dropped_out') || !isEnrolled) {
        if (!char.educationLevel || char.educationLevel === '未入学') {
          char.educationLevel = '未入学';
        }
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
          // 读完小学且已按学制升入初中，才进入初中阶段；12 岁才补录入学的孩子先读小学。
          if (char.tags.has('junior_high') || (isCompulsoryEra && char.tags.has('primary') && age > 12)) {
            char.educationLevel = '初中在读';
            if (year < 1950) title = '新制初中学校生';
            else if (year < 1978) title = '初中学校红卫兵';
            else title = '初级中学在读生';
          } else {
            char.educationLevel = '小学文化';
            title = isUrban ? '作坊初级小工' : '生产队半劳力社员';
          }
        }
      }
    }
    // (C) 青年起步与深造期 (15-p1岁)
    else if (age <= p1) {
      const hasDroppedOut = flags.has('status_dropped_out');
      const isHigherEd = flags.has('college_graduate') || 
                         char.tags.has('higher_ed_degree') ||
                         char.tags.has('college_degree') ||
                         char.tags.has('class_of_77_elite') ||
                         char.educationLevel === '大学本科' || 
                         char.educationLevel === '大专学历' ||
                         char.educationLevel === '高等院校在读';
      const isHighSchool = char.tags.has('high_school_student') ||
                           char.educationLevel === '普通高中' ||
                           char.educationLevel === '高中在读';
      const isVocational = char.tags.has('vocational_student') ||
                           char.educationLevel === '中专技校' ||
                           char.educationLevel === '中等专业';

      if (!hasDroppedOut && isHighSchool && age <= 18) {
        char.educationLevel = '高中在读';
        title = year < 1977 ? '完高学生/学农青年' : '示范高中学子';
      } else if (!hasDroppedOut && isHigherEd && age <= 22 && !flags.has('college_graduate')) {
        char.educationLevel = '高等院校在读';
        if (year < 1977) title = '工农兵推荐学员';
        else if (year < 1999) title = '全日制公费大学生';
        else title = '全日制大学本科生';
      } else if (!hasDroppedOut && (isVocational || flags.has('chose_iron_bowl'))) {
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
    // (D) 壮年立业与黄金期 ((p1+1)-59岁)
    else if (age <= 59) {
      const isJunior = age <= p2;
      const isMid = age > p2 && age <= p3;

      switch (char.careerTrack) {
        case 'worker':
          if (isJunior) {
            if (year < 1998) title = '国营机械厂四级钳工';
            else if (year < 2005) title = flags.has('xiagang_self_employed') ? '下岗再就业模具骨干' : '国企技改车间技术员';
            else title = '现代制造车间数控技师';
          } else if (isMid) {
            if (meetsHighThreshold) {
              if (year < 1998) title = '机械制造车间副主任';
              else if (year < 2008) title = '民营五金模具厂车间主任';
              else title = '现代化总装车间主任/技师';
            } else {
              title = '车间资深骨干钳工';
            }
          } else {
            title = meetsHighThreshold ? '资深机电总装大师傅/八级工' : '资深机电熟练操作工';
          }
          break;

        case 'farmer':
          if (isJunior) {
            if (year < 1980) title = '公社大队农机手/副队长';
            else if (year < 2000) title = '责任田科技示范种粮能手';
            else title = '现代特色家庭农场主';
          } else if (isMid) {
            if (meetsHighThreshold) {
              if (year < 1980) title = '人民公社生产大队长';
              else if (year < 2000) title = '乡镇农资总经销/种粮大户';
              else title = '农机专业合作社理事长';
            } else {
              title = '公社熟练种田老社员';
            }
          } else {
            title = meetsHighThreshold ? '乡村资深农艺师/种田名家' : '乡村经验丰富老农';
          }
          break;

        case 'cadre_teacher':
          if (isJunior) {
            if (year < 1980) title = '公社中心校教导主任';
            else if (year < 2000) title = '县属中学公办骨干教师';
            else title = '实验中学高级教研组长';
          } else if (isMid) {
            title = meetsHighThreshold ? '重点中学校长/高级教师' : '资深骨干教师';
          } else {
            title = meetsHighThreshold ? '教育系统资深督学/高级教师' : '资深骨干教师';
          }
          break;

        case 'merchant':
          if (isJunior) {
            if (year < 1980) title = '供销社百货柜组组长';
            else if (year < 2000) title = '沿海商贸五金批发商行主';
            else title = '跨境商贸供应链合伙人';
          } else if (isMid) {
            title = meetsHighThreshold ? '建材五金城总批发商/总经理' : '商贸店东';
          } else {
            title = meetsHighThreshold ? '民营商贸企业董事长/商会理事' : '商贸店东';
          }
          break;

        case 'tech_whitecollar':
          if (isJunior) {
            if (year < 2005) title = '跨国实业外贸部经理';
            else if (year < 2018) title = '互联网资深软件架构师';
            else title = '人工智能算法研发总监';
          } else if (isMid) {
            title = meetsHighThreshold ? '高新科技公司技术总监/合伙人' : '高级工程师';
          } else {
            title = meetsHighThreshold ? '数字化转型首席行业顾问' : '高级工程师';
          }
          break;

        case 'flexible_labor':
          if (isJunior) {
            if (year < 2005) title = '长途货运重卡车队司机';
            else if (year < 2018) title = '物流干线冷链调度组长';
            else title = '平台金牌车队长/专送主管';
          } else if (isMid) {
            title = meetsHighThreshold ? '区域冷链货运车队长' : '资深干线货车司机';
          } else {
            title = meetsHighThreshold ? '产业园区设备安全运行主管' : '资深干线货车司机';
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
          title = year >= 2009 ? '乡村退养农户/享基础养老金' : '乡村退养农户/靠儿女赡养';
        } else if (char.careerTrack === 'merchant') {
          title = '退养商界名宿/老街坊';
        } else {
          if (isUrban) title = year >= 1991 ? '城镇退休居民/享社保' : '城镇退养居民/靠单位劳保';
          else title = year >= 2009 ? '乡村退养长者/享养老金' : '乡村退养长者/靠儿女赡养';
        }
      }
    }

    // 学籍结算：超过义务教育年龄仍未升学者，不能终身停留在“小学在读/初中在读”。
    if (age > 16) {
      if (char.educationLevel === '小学在读') char.educationLevel = '小学文化';
      else if (char.educationLevel === '初中在读') char.educationLevel = '初中文化';
      else if (char.educationLevel === '高中在读') char.educationLevel = '普通高中';
    }
    // 高等院校在读：有明确毕业年份的保留到毕业年；无学籍凭据的按高中/中专结算。
    if (age > 22 && char.educationLevel === '高等院校在读' && !char.collegeGraduationYear && !flags.has('college_graduate')) {
      char.educationLevel = '普通高中';
    }

    char.occupation = title;
    // 保持 tags 中的职业轨道与当前轨道一致，避免转轨后旧职业标签继续触发
    // 职业病、身份门槛等规则。
    for (const t of ['worker', 'farmer', 'cadre_teacher', 'tech_whitecollar', 'merchant', 'flexible_labor']) {
      char.tags.delete(t);
    }
    if (char.careerTrack) char.tags.add(char.careerTrack);
  }

  /**
   * 从文本中解析出明确的地理省份，用于选项级地域门槛和身份门槛。
   * 只识别具体地名；"城市社区""沿江码头"等场景描述返回空数组，不做误杀。
   */
  getPlaceRuleIds(text) {
    if (!text) return [];
    const placeRules = [
      { id: 'hubei', re: /湖北|武汉|鄂东|鄂北|鄂西/ },
      { id: 'henan', re: /河南|郑州|豫东|豫南|豫北|豫西|驻马店|黄泛区/ },
      { id: 'beijing', re: /北京|北平|京郊|京城/ },
      { id: 'shanghai', re: /上海|沪上|淞沪/ },
      { id: 'tianjin', re: /天津|津门|滨海/ },
      { id: 'chongqing', re: /重庆|陪都|山城/ },
      { id: 'hebei', re: /河北|唐山|邢台|石家庄|冀中|冀东|冀南/ },
      { id: 'shanxi', re: /山西|太原|晋察冀|晋东北|晋东南|晋西北|正太路/ },
      { id: 'shaanxi', re: /陕西|西安|延安|陕北|关中|陕南/ },
      { id: 'shandong', re: /山东|济南|鲁南|鲁中|鲁西|沂蒙/ },
      { id: 'jiangsu', re: /江苏|南京|苏州|苏北|苏南|江淮/ },
      { id: 'zhejiang', re: /浙江|杭州|浙北|浙南/ },
      { id: 'anhui', re: /安徽|合肥|皖北|皖南/ },
      { id: 'fujian', re: /福建|福州|厦门|闽南|闽北/ },
      { id: 'jiangxi', re: /江西|南昌|赣北|赣南|赣东/ },
      { id: 'hunan', re: /湖南|长沙|湘西|湘南|湘北/ },
      { id: 'guangdong', re: /广东|广州|深圳|珠三角|粤东|粤西|粤北/ },
      { id: 'guangxi', re: /广西|南宁|桂林/ },
      { id: 'hainan', re: /海南/ },
      { id: 'sichuan', re: /四川|成都|雅安|汶川|芦山|川西|川北|川南|川陕甘/ },
      { id: 'guizhou', re: /贵州|贵阳/ },
      { id: 'yunnan', re: /云南|昆明|滇西|滇南|滇东/ },
      { id: 'gansu', re: /甘肃|兰州|陇南|陇东/ },
      { id: 'qinghai', re: /青海|玉树|西宁/ },
      { id: 'ningxia', re: /宁夏|银川/ },
      { id: 'xinjiang', re: /新疆|乌鲁木齐|南疆|北疆/ },
      { id: 'xizang', re: /西藏|拉萨|藏北|藏南/ },
      { id: 'liaoning', re: /辽宁|沈阳|大连|辽南|辽东/ },
      { id: 'jilin', re: /吉林|长春/ },
      { id: 'heilongjiang', re: /黑龙江|哈尔滨|北大荒/ },
      { id: 'neimenggu', re: /内蒙古|呼和浩特|塞北/ },
      { id: 'taiwan', re: /台湾|台北|台南/ },
      { id: 'hongkong', re: /香港/ },
      { id: 'macau', re: /澳门/ }
    ];
    return placeRules.filter(rule => rule.re.test(text)).map(rule => rule.id);
  }

  /**
   * 校验 choiceTags 中的时代门槛。
   * 支持 1937 / 1937–1949 / 1937-1949 以及少量语义化时代名。
   */
  choiceMatchesEraTag(value) {
    const v = (value || '').trim();
    if (!v || v === '通用时代' || v === '深渊时刻') return true;
    if (v === '前义务教育') return this.currentYear < 1986;
    if (v === '现代教育') return this.currentYear >= 1986;
    if (v === '高考时代') return this.currentYear >= 1977;
    const m = v.match(/^(\d{4})(?:\s*[-–—~至]\s*(\d{4}))?$/);
    if (!m) return true; // 未知写法不误杀
    const start = parseInt(m[1], 10);
    const end = m[2] ? parseInt(m[2], 10) : start;
    return this.currentYear >= start && this.currentYear <= end;
  }

  /**
   * 校验 choiceTags 中的年龄门槛。
   */
  choiceMatchesAgeTag(value) {
    const m = (value || '').trim().match(/^(\d+)(?:\s*[-–—~至]\s*(\d+))?$/);
    if (!m) return true;
    const start = parseInt(m[1], 10);
    const end = m[2] ? parseInt(m[2], 10) : start;
    return this.currentAge >= start && this.currentAge <= end;
  }

  /**
   * 校验 choiceTags 中的地域门槛。全国性标签直接放行；只对明确地名做本地校验。
   */
  choiceMatchesRegionTag(value) {
    const v = (value || '').trim();
    if (!v || v === '全国' || v.startsWith('全国')) return true;
    if (/其他省份|其他省市|其他地区|非灾区/.test(v)) return true;
    const ids = this.getPlaceRuleIds(v);
    if (ids.length === 0) return true; // 场景描述，不是可校验的行政地域
    return ids.includes(this.character.provinceId);
  }

  /**
   * 检验角色是否符合特定职业/社会身份门槛（用于选项级身份准入鉴权）
   */
  characterMatchesPersonaRole(roleKey) {
    if (!roleKey) return true;
    const r = roleKey.trim();
    const char = this.character;
    const age = this.currentAge;
    const occ = (char && char.occupation) || '';
    const track = (char && char.careerTrack) || '';

    // 0. 地理地域/震中/疫区门槛 (如: 身处湖北/武汉, 身处郑州, 身处玉树, 身处唐山)
    const city = (this.cities && char && char.cityId) ? this.cities.find(c => c.id === char.cityId) : null;
    const cityName = (city && city.name) || '';
    const cityShort = (city && city.shortName) || '';
    const provId = (char && char.provinceId) || '';
    const provinceObj = (this.provinces && this.provinces.find(p => p.id === provId)) || null;
    const provName = (provinceObj && (provinceObj.name || provinceObj.shortName)) || '';

    if (/身处|处于|居于/.test(r)) {
      // 明确点名“非灾区/全国其他省份”的，不做本地匹配。
      if (/非灾区|其他省份|其他省市|其他地区/.test(r)) return true;
      const hits = this.getPlaceRuleIds(r);
      if (hits.length > 0) {
        return hits.includes(provId);
      }
      // “沿江/南方/北方/边区”等区域描述：方向性判断，无法精确到省时放行。
      return true;
    }

    // 全国其他省份 / 其他省市 / 广大同胞 (若当前角色身处核心疫区/震中，则不作为“其他省份同胞”)
    if (/其他省份|其他省市|其他地区/.test(r)) {
      if (/湖北|武汉/.test(r) && (provId === 'hubei' || cityName.includes('武汉'))) return false;
      if (/郑州|河南/.test(r) && (provId === 'henan' || cityName.includes('郑州'))) return false;
      return true;
    }

    // 海外/港澳台亲属关系门槛
    if (/侨属|侨眷|台属|涉台|台胞|华侨|港澳台亲属|海外亲属/.test(r)) {
      return this.characterHasTag('overseas_chinese_relative') ||
             this.characterHasTag('taiwan_relative') ||
             this.characterHasTag('华侨') ||
             this.characterHasTag('侨属') ||
             this.characterHasTag('台属') ||
             /侨|台属|台胞/.test(occ);
    }

    // 智能终端/网民门槛（1980 年代不可能拥有智能手机）
    if (/智能手机|手机用户|网民|微信|短视频|数字原住民/.test(r)) {
      return this.currentYear >= 2010;
    }

    // 支前/民工/百姓等群众角色：不要求军人身份
    if (/支前|民工|担架|老乡|船工|艄公|百姓|群众|军民|妇孺/.test(r)) {
      return age >= 12;
    }

    // 军队/战争身份：普通工人、农民不得被误认作八路军/野战军将士
    if (/八路军|新四军|解放军|志愿军|红军|华野|东野|野战军|战将|将士|战士|官兵|军人|老兵|民兵|游击|武工队|军属|烈属|敢死队|守军|远征军|飞虎队/.test(r)) {
      if (this.characterHasTag('military') || this.characterHasTag('pilot')) return true;
      if (/军|兵|警|战|部队|飞行|空勤/.test(occ)) return true;
      // 抗战/解放战争时期的支前民兵与地方武装，另由上面的群众分支处理。
      return false;
    }

    // 1. 医护与公卫专业人员
    if (/医护|公卫|医生|护士|卫生员|大夫|野战医疗|防疫|医疗/.test(r)) {
      if (this.characterHasTag('doctor') || this.characterHasTag('nurse') || this.characterHasTag('barefoot_doctor')) return true;
      if (/医|护|卫|公卫|诊所|病房/.test(occ)) return true;
      return false;
    }

    // 2. 在读学生 / 青少年学子 / 少儿
    if (/在读|学生|学子|学童|少儿|中小学生/.test(r)) {
      if (age <= 18) return true;
      if (age <= 25 && char && char.educationLevel && (char.educationLevel.includes('在读') || char.educationLevel.includes('大学') || char.educationLevel.includes('高中') || char.educationLevel.includes('中专'))) return true;
      return false;
    }

    // 3. 青年群体 (在京青年、长三角青年、爱国青年)
    if (/青年/.test(r)) {
      if (age < 15 || age > 38) return false;
      if (/在京/.test(r) && provId !== 'beijing' && !cityName.includes('北京')) return false;
      if (/上海|长三角/.test(r) && provId !== 'shanghai' && !['上海', '江苏', '浙江'].some(p => cityName.includes(p) || provName.includes(p))) return false;
      return true;
    }

    // 4. 教师 / 教培 / 文教科研人员 / 学者
    if (/教师|教培|文教|学者|知识分子|科研|工程人员|工程师/.test(r)) {
      if (track === 'cadre_teacher') return true;
      if (/教|师|校|院|研|工程|技术员|学者/.test(occ)) return true;
      return false;
    }

    // 5. 工业工矿 / 技工 / 产业工人 / 铁道 / 建筑 / 机务
    if (/工矿|技工|工人|机修|地勤|铁道|铁路|桥梁|采掘|矿工|机务|车间|五金/.test(r)) {
      if (track === 'worker') return true;
      if (/工|铁|桥|车间|技|矿|机械|焊|钳|模具/.test(occ)) return true;
      return false;
    }

    // 6. 军警 / 消防 / 特警 / 防化 / 官兵 / 士兵 / 飞行员
    if (/消防|军警|特警|防化|官兵|机工|汽车兵|士兵|部队|空勤|飞行员/.test(r)) {
      if (this.characterHasTag('military') || this.characterHasTag('pilot')) return true;
      if (/军|警|消|兵|飞行|空勤/.test(occ)) return true;
      return false;
    }

    // 7. 商业 / 餐饮 / 实体店主 / 摊贩 / 企业财务
    if (/商户|餐饮|店主|小微|手工业|酒楼|企业财务|商铺|个体/.test(r)) {
      if (track === 'merchant') return true;
      if (/商|店|餐|板|摊|贸|财|会计/.test(occ)) return true;
      return false;
    }

    // 8. 农村社员 / 农民 / 老农 / 养殖户
    if (/农户|社员|老农|农民|养殖户|贫困建档|石匠|老农/.test(r)) {
      if ((char && char.urbanRural === 'rural') || track === 'farmer') return true;
      if (/农|社|耕|养/.test(occ)) return true;
      return false;
    }

    // 9. 家长 / 父母
    if (/家长|父母/.test(r)) {
      if ((char && (char.hasChildren || char.maritalStatus === '已婚')) || age >= 28) return true;
      return false;
    }

    // 10. 子女
    if (/子女/.test(r)) {
      if (age >= 16 && age <= 65) return true;
      return false;
    }

    // 11. 白领 / 职场
    if (/白领|职场|务工|自由职业/.test(r)) {
      if (age >= 18 && age <= 65) return true;
      return false;
    }

    // 12. 重体力劳动工种
    if (/重体力/.test(r)) {
      if (track === 'worker' || track === 'farmer') return true;
      if (/工|矿|装卸|力|铁|机/.test(occ)) return true;
      return false;
    }

    // 13. 发病患者本人
    if (/患者本人/.test(r)) {
      if (age >= 45 || (char && char.attributes && char.attributes.health <= 60) || this.characterHasTag('status_chronic_heart')) return true;
      return false;
    }

    // 14. 公职人员 / 干部 / 党员
    if (/公职|干部|党员|机关/.test(r)) {
      if (track === 'cadre_teacher') return true;
      if (/干|委|局|政|办|公/.test(occ)) return true;
      return false;
    }

    // 15. 大众 / 普通居民 / 同胞 / 全国人民
    if (/普通|国民|居民|同胞|大众|市民|群众/.test(r)) {
      return true;
    }

    return true;
  }

  /**
   * 选项级身份准入过滤与文案自然去前缀清洗
   */
  filterAndPolishChoices(decision) {
    if (!decision || !decision.choices || decision.choices.length === 0) return decision;
    const cloned = JSON.parse(JSON.stringify(decision));
    const matched = [];
    let hadPersonaChoices = false;

    for (const c of cloned.choices) {
      const origText = c.text || '';
      let isEligible = true;

      // 1. 匹配开头的 "若为...，" 或 "若身处...，"
      const m = origText.match(/^若(?:为|身处)([^，,：:]{2,25})[，,：:]\s*(.*)/);
      if (m) {
        hadPersonaChoices = true;
        const role = (origText.startsWith('若身处') ? '身处' : '') + m[1];
        const action = m[2];
        if (this.characterMatchesPersonaRole(role)) {
          c.text = action;
          isEligible = true;
        } else {
          isEligible = false;
        }
      }

      // 2. 校验 choiceTags 中的全部可执行门槛：时代 / 年龄 / 地域 / 身份
      if (isEligible && c.choiceTags && Array.isArray(c.choiceTags)) {
        for (const t of c.choiceTags) {
          if (typeof t !== 'string') continue;
          if (t.startsWith('门槛：')) {
            if (!this.characterMatchesPersonaRole(t.slice(3))) {
              isEligible = false;
              break;
            }
          } else if (t.startsWith('时代：')) {
            if (!this.choiceMatchesEraTag(t.slice(3))) {
              isEligible = false;
              break;
            }
          } else if (t.startsWith('年龄：')) {
            if (!this.choiceMatchesAgeTag(t.slice(3))) {
              isEligible = false;
              break;
            }
          } else if (t.startsWith('地域：')) {
            if (!this.choiceMatchesRegionTag(t.slice(3))) {
              isEligible = false;
              break;
            }
          }
        }
      }

      if (isEligible) {
        matched.push(c);
      }
    }

    // 若原事件存在特定人群分支且过滤后留下了合规选项
    if (matched.length > 0) {
      if (hadPersonaChoices && matched.length === 1) {
        matched.push({
          text: '立足自身当下岗位与家庭实际，遵从公共指引，平稳理性应对外部变局',
          choiceTags: [`时代：${this.currentYear}`, `年龄：${this.currentAge}`, '地域：全国', '门槛：理性国民'],
          outcomes: [
            {
              type: 'safe',
              weight: 100,
              log: '保持理智与清醒，不随波逐流也不盲目涉险，守护个人与小家安宁。',
              effect: { mentality: 10, family: 10 },
              isFatal: false,
              hiddenRiskLog: '在外部时代动荡中坚守理智与从容。'
            }
          ]
        });
      }
      cloned.choices = matched;
      return cloned;
    }

    // 若过滤后完全没有剩下选项（例如全是飞行员/核专家的极端选项），
    // 必须生成任何普通角色都能执行的兜底选项，避免空弹窗卡死流程。
    cloned.choices = [
      {
        text: '冷静评估自身年龄、职业与家庭处境，选择最稳妥的应对方式',
        choiceTags: [`时代：${this.currentYear}`, `年龄：${this.currentAge}`, '地域：全国', '门槛：普通国民'],
        outcomes: [
          {
            type: 'safe',
            weight: 100,
            log: '权衡利弊后采取稳妥做法，避免因一时冲动造成不可逆的损失。',
            effect: { mentality: 10, family: 10 },
            isFatal: false,
            hiddenRiskLog: '在不确定的处境中保持克制与理性。'
          }
        ]
      },
      {
        text: '以家庭生计与健康为重，先守住眼前的生活基本盘',
        choiceTags: [`时代：${this.currentYear}`, `年龄：${this.currentAge}`, '地域：全国', '门槛：普通国民'],
        outcomes: [
          {
            type: 'safe',
            weight: 100,
            log: '把有限的时间与资源先用于家人和生计，平稳度过这段时期。',
            effect: { family: 20, mentality: 10 },
            isFatal: false,
            hiddenRiskLog: '在变局中优先守护家庭的基本安稳。'
          }
        ]
      }
    ];
    return cloned;
  }

  /**
   * 将重大历史抉择动态匹配到角色的年龄与社会圈层 (千人千面)
   */
  adaptDecisionToPersona(decision) {
    if (!decision) return decision;
    if (decision.id === 'evt_2022_covid_lockdown' || decision.id === 'evt_2022_covid_lockdown_6strata') {
      const age = this.currentAge;
      const track = this.character ? this.character.careerTrack : 'worker';
      const edu = this.character ? (this.character.educationLevel || '') : '';
      const eventId = decision.id;

      // 1. 高龄退养群体 (>=60岁)
      if (age >= 60) {
        return {
          id: eventId,
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

      // 2. 学龄儿童与中小学生 (<16岁)：居家网课，而不是考研/就业话题
      if (age < 16) {
        return {
          id: eventId,
          title: '居家网课、核酸打卡与特殊学期',
          isDecision: true,
          historicalFact: '2022年多地中小学阶段性转入线上教学，校园实行闭环管理，家庭成为学习与防疫的最小单元。',
          narrative: '书包里除了课本，还多了一沓核酸抗原试剂和备用口罩。课堂搬进了平板电脑的直播间，体育课变成客厅里的跳绳打卡。父母一边远程办公，一边盯着你按时上传作业，窗外的街道安静得能听见风声。',
          choices: [
            {
              text: '按学校课表认真上网课，课后主动帮家里分担家务',
              effect: { "knowledge": 15, "mentality": 10, "family": 15 },
              status: "covid_child_online",
              log: '在特殊学期里守住了学习节奏，也体会到父母操持家务的不易。'
            },
            {
              text: '利用居家时间多读课外书，坚持室内锻炼保护视力',
              effect: { "knowledge": 10, "health": 15, "mentality": 10 },
              status: "covid_child_reading",
              log: '把居家的日子过成了充实的阅读与锻炼时光，身心都得到舒展。'
            }
          ]
        };
      }

      // 3. 高校在读学子 (18-22岁)：闭环管理、线上答辩与考公考研
      const isHigherEdStudent = age >= 18 && (
        /大学|大专|本科|专科|高等院校/.test(edu) ||
        this.characterHasTag('college_degree') ||
        this.characterHasTag('junior_college_degree')
      );
      if (isHigherEdStudent && age < 23) {
        return {
          id: eventId,
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

      // 4. 高中/中职在读学子 (16-22岁)：网课、考试调整与升学选择
      if (age < 23 && (/高中|中专|技校|中职/.test(edu) || this.characterHasTag('high_school_student') || this.characterHasTag('vocational_student'))) {
        return {
          id: eventId,
          title: '高中网课、考试调整与升学关口',
          isDecision: true,
          historicalFact: '2022年部分高中与中职学校阶段性开展线上教学，各类考试安排随防疫形势动态调整。',
          narrative: '黑板换成了屏幕，早读改在云端打卡。老师反复提醒注意考试时间调整，家长在群里接力打印复习资料。面对不确定的升学节奏，你只能把书桌收拾得更整齐，把每一天的计划排得更满。',
          choices: [
            {
              text: '紧跟学校网课节奏，按计划复习备考',
              effect: { "knowledge": 20, "mentality": -5, "health": -5 },
              status: "covid_secondary_study",
              log: '在反复调整的考试安排中稳住复习节奏，把不确定性降到最低。'
            },
            {
              text: '文化课之外学一门实用技能，为升学与就业留后路',
              effect: { "knowledge": 10, "wealth": 10, "mentality": 10 },
              status: "covid_secondary_skill",
              log: '利用居家时间掌握了实用技能，为未来多留了一条踏实的出路。'
            }
          ]
        };
      }

      // 5. 医护与公卫人员：核酸采样、发热门诊与院感防控
      if (this.characterHasTag('doctor') || this.characterHasTag('nurse') || this.characterHasTag('barefoot_doctor') ||
          (this.character.occupation && /医|护|卫生|防疫|疾控|药剂/.test(this.character.occupation))) {
        return {
          id: eventId,
          title: '发热门诊、核酸采样与院感防线',
          isDecision: true,
          historicalFact: '2022年医疗机构承担大规模核酸筛查、发热门诊值守与院感防控任务，医护与公卫人员长期处于高负荷状态。',
          narrative: '防护服一穿就是六七个小时，面屏上的水汽模糊了视线。发热门诊、核酸采样点和病房三头轮转，手机里家人的未接来电越积越多。面对不断变化的防控方案，你必须在疲惫中保持专业与冷静。',
          choices: [
            {
              text: '坚守发热门诊与采样一线，严格执行院感防护流程',
              effect: { "knowledge": 20, "mentality": 15, "health": -20 },
              status: "covid_medic_frontline",
              log: '在高负荷轮转中守住了院感底线，也赢得了同事与患者的敬重。'
            },
            {
              text: '主动申请轮休调整，利用间隙学习最新诊疗方案',
              effect: { "health": 15, "knowledge": 15, "mentality": 10 },
              status: "covid_medic_rest",
              log: '在连轴转之后及时调整状态，以更稳妥的方式继续守住岗位。'
            }
          ]
        };
      }

      // 6. 体制内/教师/公职人员群组
      if (track === 'cadre_teacher') {
        return {
          id: eventId,
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
          id: eventId,
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
          id: eventId,
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

      // 7. 农业劳动者：春耕备耕、农资运输与农产品保供
      if (track === 'farmer') {
        return {
          id: eventId,
          title: '春耕备耕、农资下摆与农产品保供',
          isDecision: true,
          historicalFact: '2022年各地在防控同时统筹春耕备耕与农产品保供，农资运输、返乡务农与产销对接面临阶段性困难。',
          narrative: '化肥和种子还堵在县城的卡口，田里的秧苗却等不得。村干部一遍遍核对返乡人员名单，收购商的大车进不了村。你蹲在田埂上盘算着农时，手机里是不断跳动的农资价格和收购信息。',
          choices: [
            {
              text: '主动对接村里与供销社，想办法把农资运进田、把农产品卖出去',
              effect: { "wealth": 15, "mentality": 10, "health": -10 },
              status: "covid_farmer_supply",
              log: '跑前跑后打通农资与销路，在特殊年份里保住了地里的收成。'
            },
            {
              text: '稳扎稳打先保口粮与基本生活，缩减高风险的经济作物',
              effect: { "family": 20, "mentality": 10, "wealth": -5 },
              status: "covid_farmer_subsistence",
              log: '把风险降到最低，先守住一家人的口粮与基本生计。'
            }
          ]
        };
      }

      // 8. 灵活就业与物流配送人员：保供链条上的奔波
      if (track === 'flexible_labor') {
        return {
          id: eventId,
          title: '保供配送、卡口通行与平台订单波动',
          isDecision: true,
          historicalFact: '2022年保供物流与同城配送承担重要民生通道作用，骑手、司机与灵活就业者面临通行、隔离与订单波动的多重压力。',
          narrative: '手机里的订单提示音和核酸倒计时交替响起。封控小区门口堆满待送的米面蔬菜，通行证、健康码与行程卡缺一不可。你一边盘算今天的油钱和单量，一边担心回不了家。',
          choices: [
            {
              text: '办好通行手续，优先接下社区保供与老人药品的急单',
              effect: { "wealth": 15, "mentality": 15, "health": -20 },
              status: "covid_delivery_supply",
              log: '在保供链条上跑出了最忙的一段路，也收获了街坊邻里的真心感谢。'
            },
            {
              text: '减少跨区流动，转做就近零单与线上兼职，先保住安全',
              effect: { "health": 15, "wealth": -10, "family": 15 },
              status: "covid_delivery_safe",
              log: '主动收缩活动范围，宁可少赚一点也要守住自身与家人的安全。'
            }
          ]
        };
      }

      // 9. 商户、个体经营者
      if (track !== 'merchant') {
        return {
          id: eventId,
          title: '特殊时期的日常生计与家庭守护',
          isDecision: true,
          historicalFact: '2022年不同行业与家庭都在防控调整中重新安排工作与生活节奏。',
          narrative: '出入小区要扫码，上班与买菜都要掐着核酸时间。工作节奏被打乱，家里的老人孩子需要照顾，收入与开支却一样不能少。你在不确定的日子里反复权衡，寻找最稳妥的安排。',
          choices: [
            {
              text: '服从社区安排，稳住现有工作与收入，减少不必要流动',
              effect: { "wealth": 10, "health": 10, "mentality": 5 },
              status: "covid_general_work",
              log: '在特殊时期守住了工作与生活的基本盘。'
            },
            {
              text: '把更多时间留给家人，照顾老人孩子并料理好家中储备',
              effect: { "family": 20, "mentality": 10, "wealth": -5 },
              status: "covid_general_family",
              log: '在不确定的日子里，家人的平安与陪伴成了最踏实的依靠。'
            }
          ]
        };
      }

      return {
        id: eventId,
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

    // 2020 武汉保卫战与举国抗疫千人千面适配
    if (decision.id === 'evt_2020_covid_chuxi') {
      const isHubei = this.character && (
        this.character.provinceId === 'hubei' ||
        (this.character.birthPlace && this.character.birthPlace.includes('湖北')) ||
        (this.character.cityHistoricalName && this.character.cityHistoricalName.includes('武汉'))
      );
      const isMedic = this.character && (
        this.characterHasTag('doctor') ||
        this.characterHasTag('nurse') ||
        this.characterHasTag('barefoot_doctor') ||
        (this.character.occupation && /医|护|卫生|防疫|疾控|药剂/.test(this.character.occupation))
      );

      // 1. 湖北及武汉封控核心区居民
      if (isHubei) {
        if (this.currentAge < 16) {
          return {
            id: decision.id,
            title: '庚子寒假：封城之下的居家童年',
            isDecision: true,
            historicalFact: decision.historicalFact,
            narrative: '寒假被无限拉长，开学日期一再推迟。窗外的小区安静下来，电视里反复播放着戴口罩、勤洗手的提醒。你趴在窗边看楼下穿防护服的叔叔阿姨送菜，第一次知道“封城”两个字有多重。',
            choices: [
              {
                text: '听父母的话乖乖待在家里，按老师要求完成线上作业',
                effect: { "knowledge": 15, "family": 15, "health": 10 },
                status: "wuhan_child_home",
                log: '在漫长的封城寒假里守住了学习和健康，也记住了那段特殊的日子。'
              },
              {
                text: '帮父母分担家务，给楼上的独居老人送菜递药',
                effect: { "family": 20, "mentality": 15, "health": -5 },
                status: "wuhan_child_helper",
                log: '在力所能及的互助中体会到邻里守望的温暖。'
              }
            ]
          };
        }
        return {
          id: decision.id,
          title: '庚子新春突发新冠疫情与武汉保卫战',
          isDecision: true,
          historicalFact: decision.historicalFact,
          narrative: '大年三十的江城街头空无一人，黄鹤楼下长江静卧，只有红绿灯在冬夜里孤独交替。电视里滚动播报着封城通告与前线告急。口罩被洗劫一空，千家万户围坐取暖，在空前的磨难中守望相助。',
          choices: [
            {
              text: '严格遵从居家静默指令，守望相助，在阳台高唱国歌相互打气鼓励',
              choiceTags: ['时代：2020', '年龄：10–75', '地域：湖北武汉及周边', '门槛：封控核心区居民'],
              outcomes: [
                {
                  type: 'safe',
                  weight: 70,
                  log: '坚忍熬过七十六个日夜封控，全家人零感染平安等到4月8日武汉解封，历经浩劫内心坚如磐石。',
                  effect: { family: 30, mentality: 30 },
                  isFatal: false,
                  hiddenRiskLog: '在武汉封城76天严苛考验中生死守望幸存，成为坚韧抗疫英雄城市见证人。',
                  status: 'wuhan_lockdown_survivor'
                },
                {
                  type: 'injured',
                  weight: 27,
                  log: '初期不幸感染轻型新冠送入方舱医院隔离救治，在医护悉心照料下顺利康复转阴出舱。',
                  effect: { health: -25, mentality: 25 },
                  isFatal: false,
                  hiddenRiskLog: '方舱医院亲历人间真情痊愈，更加珍惜生命寻常可贵。',
                  status: 'fangcang_recovered'
                },
                {
                  type: 'fatal',
                  weight: 3,
                  log: '在早期医疗资源挤兑极度紧缺阶段不幸感染重症肺炎未能抢救脱险罹难。',
                  effect: {},
                  isFatal: true,
                  hiddenRiskLog: '在2020年初武汉早期医疗挤兑阶段不幸染疫罹难。'
                }
              ]
            },
            {
              text: '报名社区网格化志愿者，佩戴红袖标协助挨家挨户敲门排查体温与配送爱心蔬菜',
              choiceTags: ['时代：2020', '年龄：18–65', '地域：湖北武汉核心区', '门槛：社区青年志愿者'],
              outcomes: [
                {
                  type: 'safe',
                  weight: 85,
                  log: '在社区最艰难的日子里顶风冒雨搬运蔬菜粮油百余吨，赢得街坊交口赞誉，自身严密防护零感染。',
                  effect: { mentality: 35, family: 25, wealth: 10 },
                  isFatal: false,
                  hiddenRiskLog: '战疫最困难时期挺身而出担当社区顶梁柱，荣获优秀抗疫志愿者表彰。',
                  status: 'wuhan_community_volunteer'
                },
                {
                  type: 'injured',
                  weight: 15,
                  log: '高强度志愿服务导致体力严重透支急性受凉发热，核酸排除后卧床休养两周。',
                  effect: { health: -20, mentality: 25 },
                  isFatal: false,
                  hiddenRiskLog: '社区抗疫一线拼搏劳累受寒，因公奉献问心无愧。'
                }
              ]
            }
          ]
        };
      }

      // 2. 医护与公卫骨干
      if (isMedic) {
        return {
          id: decision.id,
          title: '庚子新春突发新冠疫情：白衣执甲与逆行出征',
          isDecision: true,
          historicalFact: decision.historicalFact,
          narrative: '除夕之夜科室电话骤然铃声大作，国家紧急抽调精锐跨省驰援武汉。微信群里‘我报名’的请战申请瞬间刷屏。明知前方是未知的致命烈性传染病，救死扶伤的职责却重于泰山。',
          choices: [
            {
              text: '除夕夜按红手印写下‘不计报酬、无论生死’请战书，连夜随医疗队直飞武汉一线',
              choiceTags: ['时代：2020', '年龄：20–55', '地域：全国各省公立医院', '门槛：援鄂医护骨干'],
              outcomes: [
                {
                  type: 'safe',
                  weight: 75,
                  log: '在金银潭或重症ICU穿三层防护服连轴奋战两月抢救数十名危重患者，全队零感染凯旋荣归。',
                  effect: { mentality: 40, knowledge: 30, wealth: 25 },
                  isFatal: false,
                  hiddenRiskLog: '援鄂医疗英雄，以生命护佑生命，荣膺国家功臣终身尊荣。',
                  status: 'anti_covid_national_hero'
                },
                {
                  type: 'injured',
                  weight: 25,
                  log: '密闭护目镜面颊压疮重度破溃感染留疤，并在撤离后患上创伤后应激失眠，休养半年。',
                  effect: { health: -30, mentality: 25 },
                  isFatal: false,
                  hiddenRiskLog: '战疫压疮留痕心力透支，深受全社会崇高致敬。',
                  status: 'injured_medic_hero'
                }
              ]
            },
            {
              text: '坚守本地医院发热门诊与预检分诊通道，严防输入病例扩散，筑牢家乡第一道防火墙',
              choiceTags: ['时代：2020', '年龄：20–60', '地域：本地医院', '门槛：在岗医护'],
              outcomes: [
                {
                  type: 'safe',
                  weight: 85,
                  log: '严格执行院感防控流程，连续数月坚守哨点门诊，实现本地医院零交叉感染。',
                  effect: { knowledge: 25, mentality: 25, wealth: 15 },
                  isFatal: false,
                  hiddenRiskLog: '坚守本地发热门诊筑牢疫情防护网，保全一方平安。',
                  status: 'fever_clinic_guardian'
                },
                {
                  type: 'injured',
                  weight: 15,
                  log: '长期高负荷穿脱防护服导致腰肌劳损与慢性皮炎，调养数月。',
                  effect: { health: -15, mentality: 20 },
                  isFatal: false,
                  hiddenRiskLog: '本土防线坚韧值守，默默奉献守护市民安宁。'
                }
              ]
            }
          ]
        };
      }

      // 3. 全国其他省市未成年学生
      if (this.currentAge < 16) {
        return {
          id: decision.id,
          title: '庚子寒假：居家防疫与线上课堂',
          isDecision: true,
          historicalFact: decision.historicalFact,
          narrative: '春节的串门拜年被取消，开学日期一推再推。老师第一次在屏幕那头布置作业，父母每天出门前都要检查口罩。你待在家里，透过窗户看着空荡荡的街道，盼着能早点回到学校和同学见面。',
          choices: [
            {
              text: '认真完成线上作业，坚持在家锻炼身体',
              effect: { "knowledge": 15, "health": 10, "mentality": 5 },
              status: "covid_child_homework",
              log: '在特殊假期里保持了学习与锻炼的习惯。'
            },
            {
              text: '帮父母做力所能及的家务，提醒家人勤洗手戴口罩',
              effect: { "family": 20, "mentality": 10, "knowledge": 5 },
              status: "covid_child_family",
              log: '在居家防疫中学会了照顾家人，也懂得了健康的重要。'
            }
          ]
        };
      }

      // 4. 全国其他省市普通居民
      return {
        id: decision.id,
        title: '庚子新春突发新冠疫情：举国同心与全民抗疫',
        isDecision: true,
        historicalFact: decision.historicalFact,
        narrative: '除夕夜的春晚播放着白衣天使集结出征的特别节目。手机屏幕上跳动着封城通报与各地响应。全国多地迅速启动重大突发公共卫生事件一级响应，取消大型聚会，倡导居家静默阻断病毒。',
        choices: [
          {
            text: '坚决响应国家号召退掉春节探亲旅游车票，取消聚餐，戴好口罩居家静默',
            choiceTags: ['时代：2020', '年龄：10–75', '地域：全国各省市', '门槛：普通国民'],
            outcomes: [
              {
                type: 'safe',
                weight: 88,
                log: '退掉车票闭门谢客，全家人在家做面食、看书、守望相助，平安健康度过疫情初期风暴。',
                effect: { family: 25, health: 20, mentality: 20 },
                isFatal: false,
                hiddenRiskLog: '在全民战疫初期严格自律阻断传播链，守护全家平安健康。',
                status: 'disciplined_citizen'
              },
              {
                type: 'injured',
                weight: 12,
                log: '抢购口罩消毒液遭遇阶段性断货，因恐慌焦虑失眠数日，后经社区平价调拨物资恢复安心。',
                effect: { wealth: -10, mentality: -15 },
                isFatal: false,
                hiddenRiskLog: '战疫初期经历物资短暂紧缺焦虑，后在有序保供中恢复平常心。'
              }
            ]
          },
          {
            text: '向红十字会或医疗一线捐赠款物，在业主群与朋友圈积极普及科学防护知识，抵制谣言',
            choiceTags: ['时代：2020', '年龄：14–70', '地域：全国各省市', '门槛：热心公益公民'],
            outcomes: [
              {
                type: 'safe',
                weight: 92,
                log: '捐出部分积蓄用于采购一线抗疫护目镜，并在邻里群协助独居老人代购生活物资，赢得赞许。',
                effect: { mentality: 30, family: 15, wealth: -15 },
                isFatal: false,
                hiddenRiskLog: '在大灾大难面前倾力奉献爱心，传递人间温情。',
                status: 'caring_citizen_2020'
              },
              {
                type: 'safe',
                weight: 8,
                log: '协助社区辟谣伪科学偏方，普及科学七步洗手法与戴口罩规范，获得街道表扬。',
                effect: { knowledge: 20, mentality: 20 },
                isFatal: false,
                hiddenRiskLog: '以科学理性之光驱散疫情恐慌阴霾。'
              }
            ]
          }
        ]
      };
    }
    return this.filterAndPolishChoices(decision);
  }

  /**
   * 自动生成当年纪实叙事 (严格 80-150 字，千人千面四重线索交织：起承转合 + 宏观切片/被动历史 + 时代生活细节 + 职业感官 + 家境温饱)
   */
  generateNarrative(era, triggeredEvent, disasterStrike, passiveNarratives = []) {
    const age = this.currentAge;
    const year = this.currentYear;
    const char = this.character;
    const city = this.cities.find(c => c.id === char.cityId) || {};
    const cityDisp = this.resolveCityDisplay(city, year);

    // 1. 若当年遭遇特大自然灾害袭击
    if (disasterStrike && disasterStrike.isHit) {
      return disasterStrike.disaster.hitNarrative;
    }

    // 2. 句首起承转合 (句式多样，禁止连续两年相同开头)
    let opener = '';
    if (this.details && this.details.sentenceOpeners && this.details.sentenceOpeners.length > 0) {
      const candidates = this.details.sentenceOpeners.filter(op => op !== this.lastSentenceOpener);
      opener = candidates[Math.floor(Math.random() * candidates.length)] || this.details.sentenceOpeners[0];
      this.lastSentenceOpener = opener;
    } else {
      opener = `${year}年，`;
    }

    // 3. 线程一：宏观时代脉搏与被动历史大事件
    let macro = '';
    if (passiveNarratives && passiveNarratives.length > 0) {
      macro = `${passiveNarratives[0]}。`;
    } else if (triggeredEvent && triggeredEvent.narrative) {
      macro = triggeredEvent.narrative.slice(0, 50);
    } else {
      macro = this.getYearMacroSnippet(year, era);
    }

    // 4. 线程二：时代生活细节库 (饮食、居住、交通、通讯、娱乐)
    //    不再只抽一个维度撞运气：遍历全部维度，优先使用未出现过的句子，
    //    全部用尽后允许每个句子最多复用 2 次，避免长人生后半程全是通用家境句。
    let lifeDetail = '';
    if (this.details && this.details.eras) {
      let eraKey = '1937_1949';
      if (year >= 1950 && year <= 1965) eraKey = '1950_1965';
      else if (year >= 1966 && year <= 1977) eraKey = '1966_1977';
      else if (year >= 1978 && year <= 1992) eraKey = '1978_1992';
      else if (year >= 1993 && year <= 2009) eraKey = '1993_2009';
      else if (year >= 2010) eraKey = '2010_2026';

      const eraDetails = this.details.eras[eraKey];
      if (eraDetails) {
        const classKey = (char.urbanRural === 'rural')
          ? 'rural'
          : (char.careerTrack === 'cadre_teacher' ? 'cadre_intellectual' : 'urban_worker');

        const dims = ['diet', 'housing', 'transport', 'communication', 'entertainment'];
        const allSnippets = [];
        const freshSnippets = [];
        for (const dim of dims) {
          const pool = (eraDetails[dim] && eraDetails[dim][classKey]) ? eraDetails[dim][classKey] : [];
          for (const item of pool) {
            if (!item || allSnippets.includes(item)) continue;
            allSnippets.push(item);
            const usedCount = this.detailUsage[item] || 0;
            if (item !== this.lastDetailSnippet && usedCount < 2) freshSnippets.push(item);
          }
        }

        let pool = freshSnippets;
        if (pool.length === 0) pool = allSnippets.filter(item => item !== this.lastDetailSnippet);
        if (pool.length === 0) pool = allSnippets;

        if (pool.length > 0) {
          lifeDetail = pool[Math.floor(Math.random() * pool.length)];
          this.detailUsage[lifeDetail] = (this.detailUsage[lifeDetail] || 0) + 1;
          this.lastDetailSnippet = lifeDetail;
          this.usedDetailSnippets.add(lifeDetail);
        }
      }
    }

    // 5. 线程三：职业工种感官与劳作细节
    const labor = this.getLaborSensorySnippet(char, age, year, cityDisp);

    // 6. 线程四：家境温饱与身心承载
    const household = this.getHouseholdSensorySnippet(char, age);
    const energyLine = this.getEnergySensorySnippet(this.energy || {});

    // 7. 线程五：城市纪事。每个十年只出现一次，让 700+ 城市的产业与地名真正进入叙事。
    let cityLine = '';
    const currentDecade = Math.floor(year / 10);
    if (this.lastCitySnippetDecade !== currentDecade) {
      cityLine = this.getCitySensorySnippet(city, cityDisp, year);
      this.lastCitySnippetDecade = currentDecade;
    }

    // 综合编织
    let full = '';
    if (lifeDetail) {
      full = `${opener}${macro} ${labor} ${lifeDetail}`.trim();
    } else {
      full = `${opener}${macro} ${labor} ${Math.random() < 0.5 ? energyLine : household}`.trim();
    }

    if (cityLine && full.length < 120) full += ` ${cityLine}`;
    if (energyLine && full.length < 110 && Math.random() < 0.45) full += ` ${energyLine}`;

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
    if (year >= 1937 && year <= 1938) return `卢沟桥烽火骤起，沿海高校与工矿仓促西撤，流民车马塞满官道。`;
    if (year >= 1939 && year <= 1941) return `大后方警报声不绝于耳，黑烟滚滚，街市在空袭与物价飞涨中勉力维系。`;
    if (year >= 1942 && year <= 1943) return `中原旱蝗成灾与战事胶着，粮盐定量紧缩，家家在煤油灯下苦苦捱过饥馑。`;
    if (year === 1944) return `豫湘桂战事吃紧，难民潮沿铁路线涌动，后方城市在警报与物价飞涨中勉力支撑。`;
    if (year === 1945) return `抗战胜利号外传遍大街小巷，爆竹碎屑染红青石板，百废待兴复员还乡。`;
    if (year >= 1946 && year <= 1948) return `法币金圆券如废纸般贬值，商铺关门物价如脱缰野马，局势急剧动荡。`;
    if (year >= 1949 && year <= 1950) return `开国礼炮响彻神州，城乡秧歌腰鼓震天，扫盲夜校与分田界碑遍布乡野。`;
    if (year >= 1951 && year <= 1953) return `抗美援朝保家卫国动员如火如荼，大后方工厂夜以继日赶制支前被服弹药。`;
    if (year >= 1954 && year <= 1956) return `“一五”重工奠基与三大改造高潮涌动，公私合营与手工业入社红榜挂满街头。`;
    if (year === 1957) return `“一五”计划收官，工厂与机关展开整风辩论，报刊上的批判文章一天比一天密集。`;
    if (year >= 1958 && year <= 1959) return `土高炉火光映红夜空，大炼钢铁与公社大食堂号角齐鸣，标语刷满白灰墙。`;
    if (year >= 1960 && year <= 1962) return `粮票布票按两称重，稀粥照出人影，工矿精简职工退粮还乡共克时艰。`;
    if (year >= 1963 && year <= 1965) return `第一颗原子弹在戈壁升空，“备战备荒”三线建设号召大批骨干扎入深山。`;
    if (year >= 1966 && year <= 1970) return `红色浪潮席卷城乡，语录歌在大喇叭里终日回响，知青打起背包上山下乡。`;
    if (year >= 1971 && year <= 1975) return `街道地下防空工事叮当作响，乒乓外交叩开国门，车间里悄然抓紧规章整顿。`;
    if (year === 1976) return `唐山大地震的余震波及华北，广播里哀乐低回，街巷人家在悲痛与不安中守望相助。`;
    if (year === 1977) return `高考之门重新开启，尘封多年的课本被翻出来，数十万学子挑灯夜战奔赴考场。`;
    if (year >= 1978 && year <= 1981) return `改革春风拂面，小岗村承包红手印传开，街头巷尾探讨着实践真理与按劳分配。`;
    if (year >= 1982 && year <= 1985) return `女排夺冠万人空巷，黑白电视机围满邻里，特区蛇口开山炮声震动南国。`;
    if (year >= 1986 && year <= 1989) return `港台卡带情歌回响街头，物价闯关牵动人心，孔雀东南飞与进厂学徒潮并起。`;
    if (year >= 1990 && year <= 1992) return `亚运盼盼走红，邓小平南巡讲话掀起新一轮热潮，股市认购证排起长龙。`;
    if (year >= 1993 && year <= 1996) return `商品经济狂飙，三角债与下海大潮激荡，腰间寻呼机BP机的嘀嘀声不绝于耳。`;
    if (year >= 1997 && year <= 1999) return `维港焰火映照香港回归，国企三年脱困下岗阵痛袭来，高校大扩招带来新希望。`;
    if (year >= 2000 && year <= 2003) return `千禧钟声长鸣，入世集装箱货轮扬帆起航，非典突袭与收容遣送废止铭刻历史。`;
    if (year >= 2004 && year <= 2007) return `沿海世界工厂机器昼夜轰鸣，春运列车满载务工老乡，延续两千余年的农业税彻底废除。`;
    if (year >= 2008 && year <= 2009) return `汶川浩劫举国大救援，奥运五环点亮北京夜空，四万亿基建列车高速启动。`;
    if (year >= 2010 && year <= 2014) return `白色高铁银龙飞驰成网，智能手机与扫码支付融入市井，电商快递堆满驿站。`;
    if (year >= 2015 && year <= 2019) return `棚改货币化拆平老街旧巷，脱贫攻坚建档立卡，新能源汽车开始驶入寻常巷陌。`;
    if (year >= 2020 && year <= 2022) return `场所码与24小时核酸成为通行日常，多轮网格化筛查与供应链考验着万千生计。`;
    if (year >= 2023 && year <= 2026) return `生成式AI狂飙迭代，绿牌电车无声流过街头，延迟退休与银发时代悄然落地。`;
    return `时代车轮滚滚向前，千家万户的喜怒哀乐交织成奔涌的历史长河。`;
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
      if (this.statusFlags.has('status_dropped_out') && age <= 14) {
        return char.urbanRural === 'urban'
          ? '在手工作坊当小工学徒，搬运原料打磨粗坯，掌心沾满污迹，早早尝到谋生艰辛。'
          : '在生产队和家中田头放牛割草帮工，脚踩泥泞面朝黄土，过早挑起家门半副生计。';
      }
      if (char.birthYear >= 2010) {
        if (age <= 11) return `书包沉沉压在肩上，教室里齐刷刷朗读课文，放学路队穿行于车流，盼着路边一串热烤肠。`;
        return `教室顶上日光灯嗡嗡作响，模拟题与错题本堆满课桌，指关节磨出薄茧，课间讨论着新网络话题。`;
      }
      if (age <= 11) {
        return `在简易木课桌前翻读磨出毛边的旧课本，墨水蹭脏了粗布袖口，晨读声穿透薄雾回荡在土墙校舍。`;
      }
      return `挑灯自习到深夜，算草纸写满密密麻麻的公式，煤油灯或日光灯照亮年轻求知的眼睛。`;
    }

    // 3. 退休与退养老者 (60+)：退休金/养老金制度必须与年代匹配
    if (age >= 60) {
      const isSystemRetiree = track === 'cadre_teacher' || track === 'worker' || track === 'tech_whitecollar' || char.urbanRural === 'urban';
      if (isSystemRetiree) {
        if (year < 1951) {
          return `身为【${occ}】，年老后失去固定俸禄，靠儿女赡养与街坊接济度日，常坐在门槛上晒着太阳回忆旧事。`;
        }
        if (year < 1978) {
          return `身为【${occ}】，按单位劳动保险领取退休补助，晨起拎着茶缸在公园看人杀棋，戴着老花镜翻阅旧报纸。`;
        }
        if (year < 1991) {
          return `身为【${occ}】，按单位劳保领取退休金，晨起拎着茶缸在公园看人杀棋，戴着老花镜在阳台翻阅晚报。`;
        }
        return `身为【${occ}】，每月按时领取退休金/养老金，晨起在公园散步看人下棋，戴着老花镜翻阅报刊。`;
      }
      if (year < 2009) {
        return `身为【${occ}】，在自留菜园给水葱青菜浇水除草，晚年主要靠儿女赡养，傍晚守在村口看着儿孙归家。`;
      }
      return `身为【${occ}】，在自留菜园给水葱青菜浇水除草，按月领取城乡居民基础养老金，傍晚守在村口看着儿孙。`;
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
      if (age <= 5) {
        return `自幼体质孱弱易患风寒夜咳，长辈彻夜守在摇篮边悉心照料。`;
      }
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

  /**
   * 城市纪事：让城市类型、历史称谓与当期产业进入日常叙事，而不只是面板上的标签。
   */
  getCitySensorySnippet(city, cityDisp, year) {
    const name = (cityDisp && cityDisp.displayName) || this.character.cityHistoricalName || '家乡';
    const pillar = (this.character && this.character.industryPillar) || '';
    const type = (city && city.type) || (this.character && this.character.cityType) || '';

    switch (type) {
      case '重工业资源型':
        return `厂区汽笛与${pillar || '工矿生产'}，仍是${name}街巷里绕不开的生计底色。`;
      case '三线军工型':
        return `山沟里的代号厂与${pillar || '军工生产'}，仍在${name}许多家庭的记忆里回响。`;
      case '传统农业劳务型':
        return `${name}四乡的田畴与外出务工的汇款单，撑起寻常人家的柴米油盐。`;
      case '沿海商贸外贸型':
        return `${name}的码头汽笛与外贸订单，牵动着街市上每一家铺面的心跳。`;
      case '民营轻工集群型':
        return `${name}的作坊、厂房与专业市场灯火通明，家家户户在订单里讨生活。`;
      case '综合科教中心':
        return `${name}的校园、研究所与机关大院，塑造着这座城市不紧不慢的节奏。`;
      case '边陲农牧林业型':
        return `${name}的草场、林场与边境集市，风声里夹杂着各族乡音。`;
      case '贫瘠特困型':
        return `${name}的瘠薄山地与外出谋生的行囊，仍是许多家庭绕不开的现实。`;
      default:
        return `${name}的街巷在${year}年的风里照常醒转，家家有本难念的经。`;
    }
  }

  getEnergySensorySnippet(energy) {
    const entries = [
      ['study', energy.study || 0, `夜灯下翻卷深研，眼界见识日益开阔。`],
      ['work', energy.work || 0, `抢抓工时全力打拼，掌心磨出厚实老茧。`],
      ['family', energy.family || 0, `用心照看老小起居，屋檐下满是烟火人情。`],
      ['health', energy.health || 0, `起居有节清淡进补，精神矍铄身骨结实。`]
    ];
    entries.sort((a, b) => b[1] - a[1]);
    if (entries[0][1] >= 25) return entries[0][2];
    return `脚踏实地，在岁序更替中守住内心的踏实与平静。`;
  }

  /**
   * 前进一年（或步长指定年数）
   */
  advanceYear() {
    if (this.isGameOver) return null;

    this.refreshCityContext();
    let stepYears = this.getStepYears();
    if (this.currentYear < 2026 && this.currentYear + stepYears > 2026) {
      stepYears = 2026 - this.currentYear;
    }
    const era = this.getEraForYear(this.currentYear);

    // 0. 义务教育默认路径自动推进 (1980年后出生或1986年后，不再跳弹出工/辍学弹窗，仅在分流节点弹出)
    // 仅对适龄少年生效：超过 16 岁仍未入学的成年人不再被“补录”为小学/初中在读。
    const isCompulsoryEra = this.character.birthYear >= 1980 || this.currentYear >= 1986;
    if (isCompulsoryEra && this.currentAge >= 7 && this.currentAge <= 16) {
      const wasPrimaryBefore = this.character.educationLevel === '小学在读' || this.character.tags.has('primary');
      if (this.character.educationLevel === '未入学') {
        this.character.educationLevel = '小学在读';
        this.character.tags.add('primary');
        this.character.milestones.push({
          year: this.currentYear,
          age: this.currentAge,
          title: '步入校门：九年义务教育启蒙',
          detail: '依照义务教育法按时免试就近入学，背上书包领到崭新的语文算术课本。'
        });
      }
      if (this.currentAge >= 12 && wasPrimaryBefore && !this.character.tags.has('junior_high') && this.character.educationLevel === '小学在读') {
        this.character.educationLevel = '初中在读';
        this.character.tags.add('junior_high');
        this.character.milestones.push({
          year: this.currentYear,
          age: this.currentAge,
          title: '升入初中：迈入少年求知新阶段',
          detail: '小学毕业直升划片初级中学，开设代数几何与物理历史，眼界更加开阔。'
        });
      }
    }

    // 0.1 更新角色职业状态与生涯阶段 (0-80岁职业进阶树)
    this.updateCareerStage();
    this.updateEconomicLevel();

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

      let baseNarrative = dis.hitNarrative;
      if (disasterStrike.isPeripheral) {
        baseNarrative = `虽非震中或决口核心区，但【${dis.name}】强烈波及全省，地动山摇，万千军民同胞投入生死大救援。`;
      }
      const disasterNarrative = `${baseNarrative} 经此大难，你虽侥幸脱险，但【${disasterEffectsDesc.join('、') || '惊魂未定，守望相助共渡难关'}】。`;
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
      this.refreshCityContext();

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

    // 2. 检查当年所有合格事件（时代层、轨迹层、人生链条、偶发层）
    const eligibleEvents = this.findEligibleEvents();

    // 2.1 分离并立即结算被动时代宏观大事件 (isDecision === false)
    const passiveEvents = eligibleEvents.filter(e => !e.isDecision);
    const passiveNarrativeAdditions = [];
    for (const pevt of passiveEvents) {
      this.statusFlags.add(`done_${pevt.id}`);
      if (pevt.passiveImpact) {
        for (const [k, v] of Object.entries(pevt.passiveImpact)) {
          if (this.character.attributes[k] !== undefined) {
            this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
          }
        }
      }
      this.character.milestones.push({
        year: this.currentYear,
        age: this.currentAge,
        title: pevt.title,
        detail: pevt.historicalFact ? pevt.historicalFact.slice(0, 50) : pevt.title
      });
      passiveNarrativeAdditions.push(pevt.oralHistoryNarrative || pevt.title);
    }

    // 2.2 筛选主动决策候选事件 (isDecision === true)
    // 幼童与婴儿阶段（0-5岁）完全由长辈监护抚育，缺乏独立社会行为能力，不触发成年人主动决策
    const decisionCandidates = this.currentAge < 6
      ? []
      : eligibleEvents.filter(e => e.isDecision);

    // 3. 检查人生里程碑节点（刚性学制节点豁免门控，弹性节点受张力门控）
    const pendingMilestone = this.checkLifeMilestone();
    const isRigidMilestone = pendingMilestone && [
      'node_zhongkao_fenliu', 'node_gaokao_jueze', 'node_gaokao_retry', 'node_school', 'node_child_exam'
    ].includes(pendingMilestone.id);

    let activeDecision = null;

    if (isRigidMilestone) {
      // 硬性学业节点豁免，不受张力阈值限制，触发后重置张力为 20
      activeDecision = pendingMilestone;
      this.narrativeTension = 20;
    } else {
      // 普通决策受张力门控
      if (this.narrativeTension === undefined) {
        this.narrativeTension = 35 + Math.floor(Math.random() * 25);
      }
      if (this.nextDecisionCooldownUntil === undefined) {
        this.nextDecisionCooldownUntil = 0;
      }

      const isTensionReady = (this.narrativeTension >= 85) && (this.currentYear >= this.nextDecisionCooldownUntil);

      if (isTensionReady && this.currentAge >= 6) {
        const eraCandidates = decisionCandidates.filter(e => e.tier === 'era');
        const lifeChainCandidates = decisionCandidates.filter(e => e.tier === 'life_chain');
        const trajCandidates = decisionCandidates.filter(e => e.tier === 'trajectory');
        const contCandidates = decisionCandidates.filter(e => e.tier === 'contingency');

        if (pendingMilestone && !isRigidMilestone) {
          if (pendingMilestone.id === 'node_marriage') {
            lifeChainCandidates.push(pendingMilestone);
            lifeChainCandidates.push(pendingMilestone);
          } else if (pendingMilestone.id === 'node_medical' || pendingMilestone.id === 'node_darkest_hour') {
            contCandidates.push(pendingMilestone);
          } else {
            lifeChainCandidates.push(pendingMilestone);
          }
        }

        const validEraDecisions = [];
        for (const eraEvt of eraCandidates) {
          const isCore = this.isEraCoreCollision(eraEvt);
          const adapted = this.adaptDecisionToPersona(eraEvt);
          const polished = this.filterAndPolishChoices(adapted);
          if (!polished.choices || polished.choices.length <= 1) {
            this.statusFlags.add(`done_${eraEvt.id}`);
            const singleChoice = (polished.choices && polished.choices[0]);
            if (singleChoice) {
              const eff = (singleChoice.outcomes && singleChoice.outcomes[0] && singleChoice.outcomes[0].effect) || singleChoice.effect || {};
              for (const [k, v] of Object.entries(eff)) {
                if (this.character.attributes[k] !== undefined) {
                  this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
                }
              }
              this.character.milestones.push({
                year: this.currentYear,
                age: this.currentAge,
                title: eraEvt.title,
                detail: (singleChoice.outcomes && singleChoice.outcomes[0] && singleChoice.outcomes[0].log) || singleChoice.log || singleChoice.text || eraEvt.title
              });
            }
            passiveNarrativeAdditions.push(eraEvt.oralHistoryNarrative || eraEvt.title);
          } else {
            validEraDecisions.push({ raw: eraEvt, isCore });
          }
        }

        const coreCollisionEra = validEraDecisions.find(e => e.isCore);
        if (coreCollisionEra) {
          activeDecision = coreCollisionEra.raw;
          this.lastEraDecisionYear = this.currentYear;
        } else {
          const hasPersonalHook = (this.character.maritalStatus === '已婚' && !this.character.hasChildren) ||
                                  this.characterHasTag('xiagang') ||
                                  this.characterHasTag('xiagang_self_employed') ||
                                  ['worker', 'farmer', 'cadre_teacher', 'tech_whitecollar', 'merchant', 'flexible_labor'].includes(this.character.careerTrack) ||
                                  ['smoker', 'drinker', 'swimmer', 'hiker', 'stay_up_late'].some(t => this.characterHasTag(t));

          const inEraFatigue = this.lastEraDecisionYear && (this.currentYear - this.lastEraDecisionYear <= 2);

          let wLife = hasPersonalHook ? 40 : 30;
          let wTraj = hasPersonalHook ? 30 : 20;
          let wEra = inEraFatigue ? 5 : (hasPersonalHook ? 25 : 40);
          let wCont = hasPersonalHook ? 5 : 10;

          const availableTiers = [];
          if (lifeChainCandidates.length > 0) availableTiers.push({ tier: 'life_chain', weight: wLife, list: lifeChainCandidates });
          if (trajCandidates.length > 0) availableTiers.push({ tier: 'trajectory', weight: wTraj, list: trajCandidates });
          if (validEraDecisions.length > 0) availableTiers.push({ tier: 'era', weight: wEra, list: validEraDecisions.map(d => d.raw) });
          if (contCandidates.length > 0) availableTiers.push({ tier: 'contingency', weight: wCont, list: contCandidates });

          while (availableTiers.length > 0 && !activeDecision) {
            const totalWeight = availableTiers.reduce((acc, t) => acc + t.weight, 0);
            let roll = Math.random() * totalWeight;
            let chosenTierIndex = 0;
            for (let i = 0; i < availableTiers.length; i++) {
              if (roll <= availableTiers[i].weight) {
                chosenTierIndex = i;
                break;
              }
              roll -= availableTiers[i].weight;
            }
            const chosenTier = availableTiers[chosenTierIndex];
            const candidate = this.pickEventCandidate(chosenTier.list);
            const adapted = this.adaptDecisionToPersona(candidate);
            const polished = this.filterAndPolishChoices(adapted);
            if (polished.choices && polished.choices.length > 1) {
              activeDecision = candidate;
              if (chosenTier.tier === 'era') {
                this.lastEraDecisionYear = this.currentYear;
              }
            } else {
              this.statusFlags.add(`done_${candidate.id}`);
              if (polished.choices && polished.choices.length === 1) {
                const c = polished.choices[0];
                const eff = (c.outcomes && c.outcomes[0] && c.outcomes[0].effect) || c.effect || {};
                for (const [k, v] of Object.entries(eff)) {
                  if (this.character.attributes[k] !== undefined) {
                    this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
                  }
                }
                this.character.milestones.push({
                  year: this.currentYear,
                  age: this.currentAge,
                  title: candidate.title,
                  detail: (c.outcomes && c.outcomes[0] && c.outcomes[0].log) || c.log || c.text || candidate.title
                });
                passiveNarrativeAdditions.push(candidate.oralHistoryNarrative || candidate.title);
              }
              chosenTier.list = chosenTier.list.filter(e => e.id !== candidate.id);
              if (chosenTier.list.length === 0) {
                availableTiers.splice(chosenTierIndex, 1);
              }
            }
          }
        }
      }
    }

// 5. 正常年度死亡检测
    const deathRate = this.calculateAnnualMortalityRate(era);
    const deathRoll = Math.random();
    const hasDied = deathRoll < deathRate || this.character.attributes.health <= 0;

    if (hasDied) {
      this.triggerDeath(era, activeDecision);
      return {
        isGameOver: true,
        deathInfo: this.deathInfo,
        character: this.character,
        history: this.history
      };
    }

    // 6. 若有主动决策触发，暂停推进等待玩家选择 (千人千面适配)
    if (activeDecision && activeDecision.isDecision) {
      // 适配后的千人千面分支同样要经过时代/年龄/地域/身份门槛过滤，
      // 避免儿童拿到成人选项、普通职工被套上医护/商户剧情。
      activeDecision = this.filterAndPolishChoices(this.adaptDecisionToPersona(activeDecision));
      // 兜底防御：若过滤后选项仍小于等于 1 且不是硬性学制节点，自动转为被动记录，不弹出单按钮伪弹窗
      if (activeDecision.choices && activeDecision.choices.length <= 1 && !['node_zhongkao_fenliu', 'node_gaokao_jueze', 'node_gaokao_retry', 'node_school', 'node_child_exam'].includes(activeDecision.id)) {
        this.statusFlags.add(`done_${activeDecision.id}`);
        const c = activeDecision.choices[0];
        if (c) {
          const eff = (c.outcomes && c.outcomes[0] && c.outcomes[0].effect) || c.effect || {};
          for (const [k, v] of Object.entries(eff)) {
            if (this.character.attributes[k] !== undefined) {
              this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
            }
          }
          this.character.milestones.push({
            year: this.currentYear,
            age: this.currentAge,
            title: activeDecision.title,
            detail: (c.outcomes && c.outcomes[0] && c.outcomes[0].log) || c.log || c.text || activeDecision.title
          });
        }
        passiveNarrativeAdditions.push(activeDecision.oralHistoryNarrative || activeDecision.title);
        activeDecision = null;
      } else {
        this.currentPendingDecision = activeDecision;
        return {
          isDecision: true,
          decisionData: activeDecision,
          currentYear: this.currentYear,
          currentAge: this.currentAge
        };
      }
    }

    // 7. 若当年为平静岁月 (无决策)，应用精力结算并自然推进，累加张力
    this.applyEnergyEffects(stepYears);
    this.narrativeTension = (this.narrativeTension || 0) + (28 + Math.floor(Math.random() * 12));

    // 8. 生成当年纪实叙事 (融合宏观背景与生活细节)
    const narrativeText = this.generateNarrative(era, null, null, passiveNarrativeAdditions);

    // 9. 记录历史轨迹
    const turnRecord = {
      year: this.currentYear,
      age: this.currentAge,
      eraName: era.name,
      narrative: narrativeText,
      attributes: { ...this.character.attributes },
      eventTitle: passiveNarrativeAdditions.length > 0 ? passiveNarrativeAdditions[0] : '平静岁月'
    };
    this.history.push(turnRecord);

    // 10. 年份递增
    this.currentYear += stepYears;
    this.currentAge += stepYears;
    this.recordLifeline();
    this.refreshCityContext();

    // 11. 到达 2026 年或百岁圆满
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
   * 检验职业状态机跃迁合法性 (根据 data/transitions.json 规则库)
   */
  validateCareerTransition(currentTrack, targetTrack, year, age, tags, wealth) {
    if (!currentTrack || !targetTrack) return true;
    if (currentTrack === targetTrack) return true;
    if (!this.transitions || !this.transitions.careerTracks) return true;

    const trackConfig = this.transitions.careerTracks[currentTrack];
    if (!trackConfig || !trackConfig.allowedNext) return true;

    // 检查 allowedNext 列表
    const rule = trackConfig.allowedNext.find(r => r.target === targetTrack);
    if (rule) {
      if (rule.minYear && year < rule.minYear) return false;
      if (rule.maxYear && year > rule.maxYear) return false;
      if (rule.minAge && age < rule.minAge) return false;
      if (rule.maxAge && age > rule.maxAge) return false;
      if (rule.requiresWealth && wealth < rule.requiresWealth) return false;
      if (rule.requiresTags && rule.requiresTags.length > 0) {
        for (const t of rule.requiresTags) {
          if (!this.characterHasTag(t)) return false;
        }
      }
      return true;
    }

    // 若未在直接转移列表中，检查高阶门槛
    if (targetTrack === 'cadre_teacher' || targetTrack === 'tech_whitecollar') {
      return this.characterHasTag('higher_ed_degree') || this.characterHasTag('college');
    }

    return true;
  }

  /**
   * 玩家确认抉择后的结算处理（支持加权分支 outcomes、因果回顾 hiddenRiskLog、职业跃迁与致命分支）
   */
  resolveDecision(decisionId, choiceIndex) {
    let evt = (this.currentPendingDecision && this.currentPendingDecision.id === decisionId)
      ? this.currentPendingDecision
      : this.events.find(e => e.id === decisionId);

    if (!evt) {
      if (decisionId === 'node_zhongkao_fenliu') {
        evt = {
          title: '中考分流：普高与职教技校十字路口',
          choices: [
            {
              text: '全力冲刺重点普高，志在三年后参加高考',
              choiceTags: ['时代：现代教育', '年龄：15–16', '地域：全国', '门槛：学术考学追求者'],
              outcomes: [
                { type: 'safe', weight: 80, log: '中考成绩优异被重点示范性普通高中录取，进入高强度题海冲刺高考。', effect: { knowledge: 25, mentality: 10, health: -5 }, status: 'high_school_student', hiddenRiskLog: '顺利考入重点高中，叩开通往全日制高等学府的大门。' },
                { type: 'safe', weight: 20, log: '压线被普通高中普通班录取，虽然底子偏弱但依然保留高考冲刺机会。', effect: { knowledge: 15, mentality: 5 }, status: 'high_school_student', hiddenRiskLog: '勉强踏入普通高中门槛，需在高中三年加倍发奋苦读。' }
              ]
            },
            {
              text: '报考特色职业技术学校或中专，专攻实用立身技能',
              choiceTags: ['时代：现代教育', '年龄：15–16', '地域：全国', '门槛：技能实践导向者'],
              outcomes: [
                { type: 'safe', weight: 90, log: '入读中专职校王牌专业，扎实掌握一门过硬实操手艺，毕业后直通对口单位。', effect: { wealth: 15, mentality: 15, knowledge: 10 }, status: 'vocational_student', hiddenRiskLog: '早学一技之长立足社会，避开高考内卷走出务实道路。' },
                { type: 'safe', weight: 10, log: '在职校期间表现突出，代表学校参加全省技能大赛获二等奖。', effect: { knowledge: 20, wealth: 10 }, status: 'vocational_student', hiddenRiskLog: '职校磨砺出精湛技能，成为行业骨干后备力量。' }
              ]
            }
          ]
        };
      } else if (decisionId === 'node_gaokao_jueze' || decisionId === 'node_gaokao_retry') {
        evt = {
          title: '六月高考：千军万马过独木桥',
          choices: [
            {
              text: '冲击全日制本科院校（若失利则调剂专科）',
              choiceTags: ['时代：高考时代', '年龄：18–19', '地域：全国', '门槛：普高应届毕业生'],
              outcomes: [
                { type: 'safe', weight: 55, log: '发挥沉稳超常发挥，顺利被全日制本科大学录取，跨入高等学府象牙塔。', effect: { knowledge: 35, mentality: 20, wealth: -15 }, status: 'college_degree', hiddenRiskLog: '金榜题名迈入本科高校，为一生学术与职业奠定最高底色。' },
                { type: 'safe', weight: 35, log: '考分略有遗憾但被省属公办高等专科学校王牌专业录取，学制三年。', effect: { knowledge: 20, mentality: 10, wealth: -10 }, status: 'junior_college_degree', hiddenRiskLog: '入读高职大专踏实修习，为后续专升本或高薪就业铺路。' },
                { type: 'redirected', weight: 10, log: '发挥失常痛定思痛决定在县一中复读高四再战一年。', effect: { knowledge: 10, mentality: -10, health: -5 }, status: 'repeating_gaokao', hiddenRiskLog: '背水一战选择复读高四，经历常人难忍的精神洗礼。' }
              ]
            },
            {
              text: '放弃升学直接进入社会就业创业，早日自立减轻家庭负担',
              choiceTags: ['时代：通用时代', '年龄：18–20', '地域：全国', '门槛：自立打拼者'],
              outcomes: [
                { type: 'safe', weight: 85, log: '脱离书卷投身社会大熔炉，在同乡引荐下入职当地骨干企业或商贸实体。', effect: { wealth: 25, mentality: 15, family: 15 }, status: 'early_employment', hiddenRiskLog: '早早步入社会自食其力，在摸爬滚打中积累人情世故与第一桶金。' },
                { type: 'safe', weight: 15, log: '敏锐捕捉商机在批发市场支起摊位自力更生，当月实现盈利扭亏。', effect: { wealth: 35, mentality: 20 }, status: 'early_merchant', hiddenRiskLog: '青年下海敢为人先，自主创业走出一番天地。' }
              ]
            }
          ]
        };
      } else if (decisionId === 'node_school') {
        evt = {
          title: '适龄读书与做工抉择',
          choices: [
            {
              text: '克服困难坚持上学读书',
              choiceTags: ['时代：前义务教育', '年龄：6–8', '地域：全国', '门槛：求学向进者'],
              outcomes: [
                { type: 'safe', weight: 100, log: '在贫瘠与困顿中坚持念书，背着用粗布缝合的书包迈进学堂。', effect: { knowledge: 25, wealth: -10, health: 5 }, status: 'primary', hiddenRiskLog: '启蒙读书识字明理，彻底摆脱文盲困境。' }
              ]
            },
            {
              text: '早早辍学务农或当学徒做工',
              choiceTags: ['时代：前义务教育', '年龄：6–8', '地域：全国', '门槛：生计所迫者'],
              outcomes: [
                { type: 'redirected', weight: 100, log: '懂事地辍学帮衬家门，在尘土与汗水中挑起家庭生计重担。', effect: { wealth: 15, family: 15, knowledge: -10 }, status: 'status_dropped_out', hiddenRiskLog: '年幼失学过早步入劳作，文化水平受限成为一生憾事。' }
              ]
            }
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
          title: '成家立业关口',
          choices: [
            {
              text: '依照习俗顺理成章成家完婚',
              choiceTags: ['时代：传统婚恋', '年龄：21–35', '地域：全国', '门槛：适龄青年'],
              outcomes: [
                { type: 'safe', weight: 90, log: '按当年规制办了喜酒成家立业，夫妻相濡以沫操持生计。', effect: { family: 25, wealth: -15, mentality: 10 }, status: 'married', hiddenRiskLog: '寻得终身伴侣喜结连理，携手抵御人间风雨。' },
                { type: 'safe', weight: 10, log: '喜结良缘且夫妻双方勤俭持家，小家庭积蓄蒸蒸日上。', effect: { family: 35, wealth: 10, mentality: 15 }, status: 'married', hiddenRiskLog: '得遇贤能良偶，齐心协力改善家境。' }
              ]
            },
            {
              text: '推迟婚期，专心打拼本职或求学',
              choiceTags: ['时代：事业优先', '年龄：21–35', '地域：全国', '门槛：打拼奋斗者'],
              outcomes: [
                { type: 'safe', weight: 100, log: '暂缓个人婚事，把满腔热忱投入到本职工作与打拼当中。', effect: { knowledge: 15, wealth: 15, family: -10 }, hiddenRiskLog: '暂缓成家立业，积蓄个人实力等待更佳良缘。' }
              ]
            }
          ]
        };
      } else if (decisionId === 'node_medical') {
        evt = {
          title: '顽疾缠身与就医抉择',
          choices: [
            {
              text: '动用全部积蓄积极住院治疗',
              choiceTags: ['时代：医疗救治', '年龄：48–65', '地域：全国', '门槛：重病患者'],
              outcomes: [
                { type: 'safe', weight: 85, log: '四处借钱并动用积蓄积极就医，病情得以控制稳定。', effect: { health: 25, wealth: -30, mentality: 10 }, hiddenRiskLog: '倾尽积蓄治愈恶疾，虽耗光钱财但保住宝贵生命。' },
                { type: 'injured', weight: 15, log: '住院手术历经凶险虽保住性命，但需常年服药调养。', effect: { health: 15, wealth: -40 }, hiddenRiskLog: '大病初愈落下慢性病根，需谨遵医嘱长期调理。' }
              ]
            },
            {
              text: '抓草药硬扛，把钱留给儿女开销',
              choiceTags: ['时代：保守求生', '年龄：48–65', '地域：全国', '门槛：省吃俭用者'],
              outcomes: [
                { type: 'injured', weight: 80, log: '不忍拖累家人选择硬撑苦挨，身体逐渐落下严重宿疾。', effect: { health: -20, family: 15, wealth: 5 }, hiddenRiskLog: '舍身顾念家庭延误医治，身体机能不可逆衰退。' },
                { type: 'fatal', weight: 20, log: '病情迅速恶化引发全身感染多器官衰竭，抢救无效溘然长逝。', isFatal: true, hiddenRiskLog: '重病延误医治不幸早逝。' }
              ]
            }
          ]
        };
      } else if (decisionId === 'node_darkest_hour') {
        evt = {
          title: '人生至暗时刻：深渊边缘的寒夜',
          choices: [
            {
              text: '万念俱灰，松开栏杆走入冰冷黑夜（绝境弃生）',
              choiceTags: ['时代：深渊时刻', '门槛：极度绝望者'],
              outcomes: [
                { type: 'fatal', weight: 100, isFatal: true, log: '心力枯竭，在无尽的黑暗与深渊面前永远闭上了双眼。', hiddenRiskLog: '在人生的至暗绝境中走完了一生。' }
              ]
            },
            {
              text: '嚼碎屈辱，哪怕出尽苦力也要替家人还债（负重苟活）',
              choiceTags: ['时代：深渊时刻', '门槛：坚韧求生者'],
              outcomes: [
                { type: 'safe', weight: 100, log: '在桥头痛哭一场后咬碎牙关擦干眼泪，哪怕脱掉长衫出尽苦力，也要替家门把债还清。', effect: { health: -25, wealth: 10, mentality: 25 }, hiddenRiskLog: '嚼碎绝望重新站起，在最苦最累的生计中重塑尊严。' }
              ]
            },
            {
              text: '推开破旧老屋柴门，父母的一碗热汤将自己从悬崖边缘拉回（至亲救赎）',
              choiceTags: ['时代：深渊时刻', '门槛：亲情羁绊者'],
              outcomes: [
                { type: 'safe', weight: 100, log: '在老母亲颤抖递来的一碗热汤面面前抱头痛哭，认栽还乡，在亲情庇护下捡回一条命。', effect: { family: 20, mentality: 35 }, hiddenRiskLog: '在血脉至亲的包容与温暖中重拾活下去的勇气。' }
              ]
            }
          ]
        };
      }
    }

    if (!evt || !evt.choices || !evt.choices[choiceIndex]) return;

    const choice = evt.choices[choiceIndex];
    let selectedOutcome = null;

    // 检查 outcomes 加权分支
    if (choice.outcomes && choice.outcomes.length > 0) {
      const totalWeight = choice.outcomes.reduce((acc, o) => acc + (o.weight || 0), 0);
      let roll = Math.random() * (totalWeight || 1);
      for (const o of choice.outcomes) {
        if (roll <= (o.weight || 0)) {
          selectedOutcome = o;
          break;
        }
        roll -= (o.weight || 0);
      }
      if (!selectedOutcome) selectedOutcome = choice.outcomes[choice.outcomes.length - 1];
    }

    // 致命分支结算
    if (selectedOutcome && selectedOutcome.isFatal) {
      this.isGameOver = true;
      const deathCause = selectedOutcome.log || `${evt.title}：不幸身亡`;
      this.deathInfo = {
        age: this.currentAge,
        year: this.currentYear,
        cause: deathCause,
        isNatural: false,
        isEventFatal: true,
        eventTitle: evt.title
      };
      this.character.causalityReview.push({
        year: this.currentYear,
        age: this.currentAge,
        eventTitle: evt.title || '突发变故',
        choiceText: choice.text,
        outcomeType: 'fatal',
        hiddenRisk: selectedOutcome.hiddenRiskLog || deathCause
      });
      this.character.milestones.push({
        year: this.currentYear,
        age: this.currentAge,
        title: evt.title,
        detail: selectedOutcome.log
      });

      const era = this.getEraForYear(this.currentYear);
      const outcomeLog = selectedOutcome.log || deathCause;
      const narrativeText = `${evt.narrative || ''} 面对命运关口，你选择了【${choice.text}】。${outcomeLog}`;
      let trimmedNarrative = narrativeText.trim();
      if (trimmedNarrative.length > 150) trimmedNarrative = trimmedNarrative.slice(0, 146) + '……';

      const turnRecord = {
        year: this.currentYear,
        age: this.currentAge,
        eraName: era.name,
        narrative: trimmedNarrative,
        attributes: { ...this.character.attributes },
        eventTitle: evt.title || '关键抉择',
        isDecision: true
      };
      this.history.push(turnRecord);
      this.recordLifeline();
      this.refreshCityContext();

      this.currentPendingDecision = null;
      return;
    }

    // 属性影响处理
    const effect = (selectedOutcome && selectedOutcome.effect) ? selectedOutcome.effect : (choice.effect || {});
    for (const [k, v] of Object.entries(effect)) {
      if (this.character.attributes[k] !== undefined) {
        this.character.attributes[k] = Math.max(0, Math.min(100, this.character.attributes[k] + v));
      }
    }

    // 状态标签与人生状态处理
    this.updateEconomicLevel();
    const outcomeStatus = (selectedOutcome && selectedOutcome.status) ? selectedOutcome.status : choice.status;
    if (outcomeStatus) {
      this.character.tags.add(outcomeStatus);
      this.statusFlags.add(outcomeStatus);

      const isGaokaoDecision = decisionId === 'node_gaokao_jueze' || decisionId === 'node_gaokao_retry';

      if (outcomeStatus === 'married') {
        this.character.maritalStatus = '已婚';
      }
      if (outcomeStatus === 'has_children') {
        this.character.hasChildren = true;
      }
      // 只有真正发生生育的结局才记录产育年份，供产妇死亡风险使用。
      const birthStatuses = new Set([
        'has_children', 'multi_children', 'millennium_baby_parent',
        'two_children_family', 'three_children_family',
        'safe_cesarean_mother', 'resilient_brave_mother'
      ]);
      if (birthStatuses.has(outcomeStatus)) {
        this.character.lastChildbirthYear = this.currentYear;
        this.character.hasChildren = true;
      }
      if (isGaokaoDecision && (outcomeStatus === 'college_degree' || outcomeStatus === 'junior_college_degree')) {
        // 录取不等于毕业：记录学制，到毕业年份再由 updateCareerStage 结算学位。
        this.statusFlags.add('attended_gaokao');
        this.character.degreeType = outcomeStatus === 'junior_college_degree' ? '大专' : '本科';
        this.character.collegeGraduationYear = this.currentYear + (outcomeStatus === 'junior_college_degree' ? 3 : 4);
        this.character.educationLevel = '高等院校在读';
      } else if (isGaokaoDecision && outcomeStatus === 'repeating_gaokao') {
        this.statusFlags.add('attended_gaokao');
        this.character.educationLevel = '普通高中';
      } else if (outcomeStatus === 'college_degree' || outcomeStatus === 'class_of_77_elite' || outcomeStatus === 'expanded_college_student' || outcomeStatus === 'lianda_scholar_elite' || outcomeStatus === 'overseas_scholar' || outcomeStatus === 'overseas_phd_scholar') {
        this.character.educationLevel = '大学本科';
        this.character.tags.add('higher_ed_degree');
        this.character.tags.add('college_graduate');
        this.statusFlags.add('college_graduate');
        if (!this.character.collegeGraduationYear) {
          this.character.collegeGraduationYear = this.currentYear + 4;
        }
      } else if (outcomeStatus === 'junior_college_degree' || outcomeStatus === 'highschool_to_college' || outcomeStatus === 'self_made_scholar_1977') {
        this.character.educationLevel = '大专学历';
        this.character.tags.add('higher_ed_degree');
      } else if (outcomeStatus === 'high_school_student') {
        this.character.educationLevel = '普通高中';
      } else if (outcomeStatus === 'vocational_student') {
        this.character.educationLevel = '中专技校';
      } else if (outcomeStatus === 'primary') {
        this.character.educationLevel = '小学文化';
      }
    }

    // 职业赛道跃迁（接入 transitions 状态机合法性检验）
    if (selectedOutcome && selectedOutcome.newCareerTrack) {
      const target = selectedOutcome.newCareerTrack;
      if (this.validateCareerTransition(this.character.careerTrack, target, this.currentYear, this.currentAge, this.character.tags, this.character.attributes.wealth)) {
        this.character.careerTrack = target;
        this.character.tags.add(target);
      }
    }

    // 记录因果回顾 (hiddenRiskLog)
    const hiddenRiskLog = (selectedOutcome && selectedOutcome.hiddenRiskLog)
      ? selectedOutcome.hiddenRiskLog
      : (choice.log || choice.text);
    this.character.causalityReview.push({
      year: this.currentYear,
      age: this.currentAge,
      eventTitle: evt.title || '人生抉择',
      choiceText: choice.text,
      outcomeType: (selectedOutcome && selectedOutcome.type) ? selectedOutcome.type : 'safe',
      hiddenRisk: hiddenRiskLog
    });

    // 记录里程碑
    const outcomeLog = (selectedOutcome && selectedOutcome.log) ? selectedOutcome.log : (choice.log || choice.text);
    this.character.milestones.push({
      year: this.currentYear,
      age: this.currentAge,
      title: evt.title || '关键抉择',
      detail: outcomeLog
    });

    // 设置冷却时间与完成标记
    if (evt.id) {
      this.eventCooldowns[evt.id] = this.currentYear + (evt.coolingPeriod || 999);
      this.statusFlags.add(`done_${evt.id}`);

      // 婚育关卡冷却联动
      if (evt.id === 'node_marriage' || evt.id === 'evt_life_xiangqin_jiehun') {
        this.eventCooldowns['node_marriage'] = this.currentYear + 4;
        this.eventCooldowns['evt_life_xiangqin_jiehun'] = this.currentYear + 4;
      }
    }

    // 扣减张力并设置呼吸期冷却
    const isRigidDecision = (decisionId === 'node_zhongkao_fenliu' || decisionId === 'node_gaokao_jueze' || decisionId === 'node_gaokao_retry' || decisionId === 'node_school' || decisionId === 'node_child_exam');
    this.narrativeTension = isRigidDecision ? 20 : Math.floor(Math.random() * 18);
    this.nextDecisionCooldownUntil = this.currentYear + (1 + Math.floor(Math.random() * 2));

    this.currentPendingDecision = null;
    this.updateCareerStage();

    let stepYears = this.getStepYears();
    if (this.currentYear < 2026 && this.currentYear + stepYears > 2026) {
      stepYears = 2026 - this.currentYear;
    }
    const era = this.getEraForYear(this.currentYear);

    this.applyEnergyEffects(stepYears);

    const narrativeText = `${evt.narrative || ''} 面对命运关口，你选择了【${choice.text}】。${outcomeLog}`;
    let trimmedNarrative = narrativeText.trim();
    if (trimmedNarrative.length > 150) trimmedNarrative = trimmedNarrative.slice(0, 146) + '……';

    const turnRecord = {
      year: this.currentYear,
      age: this.currentAge,
      eraName: era.name,
      narrative: trimmedNarrative,
      attributes: { ...this.character.attributes },
      eventTitle: evt.title || '关键抉择',
      isDecision: true
    };
    this.history.push(turnRecord);

    this.currentYear += stepYears;
    this.currentAge += stepYears;
    this.recordLifeline();
    this.refreshCityContext();

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

    if (isHeavy && this.currentAge >= 18 && this.currentAge <= 65 && (this.character.tags.has('worker') || this.character.tags.has('heavy_industry') || this.character.tags.has('miner'))) {
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
      let fatalMilestoneTitle = '天降横祸';
      if (this.currentAge < 16) fatalMilestoneTitle = '飞来横祸';
      else if (this.currentAge < 45) fatalMilestoneTitle = '英年横祸';
      else if (this.currentAge >= 70) fatalMilestoneTitle = '暮年意外';

      this.character.milestones.push({
        year: this.currentYear,
        age: this.currentAge,
        title: fatalMilestoneTitle,
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
   * 严密按年龄、时代、性别、习惯标签分层的真实死因生成器（彻底消除32岁死于“老年多器官衰竭”等严重倒挂）
   */
  getAuthenticCauseOfDeath(era, age, sex, attributes, tags, fatalEvent) {
    if (fatalEvent) {
      if (fatalEvent.cause) return fatalEvent.cause;
      if (fatalEvent.title && fatalEvent.title.includes('饥荒')) return '遭遇严重饥荒营养枯竭衰竭离世';
      if (fatalEvent.title && fatalEvent.title.includes('抗战')) return '战火流弹波及与战地疫病离世';
    }

    const year = this.currentYear;

    // 1. 婴儿期 (0 岁)
    if (age === 0) {
      if (year < 1950) {
        const pool = [
          '因当年严峻的新生儿破伤风与脐带感染夭折',
          '因母乳匮乏与严冬受冻重症肺炎夭折',
          '因急性小儿百日咳与严重腹泻脱水夭折'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 1980) {
        const pool = [
          '因当年医疗匮乏突发新生儿急腹症未能及时送医夭折',
          '因重症小儿麻疹并发急性肺炎夭折',
          '因急性百日咳并发呼吸衰竭夭折'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 2000) {
        const pool = [
          '因新生儿重症急性呼吸窘迫综合征未能挽回',
          '因先天性重症复杂畸形多器官衰竭夭折',
          '因新生儿重度溶血与脑病并发症夭折'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else {
        const pool = [
          '因极低出生体重超早产合并多器官发育不全夭折',
          '因严重复杂先天性心血管畸形抢救无效夭折',
          '因新生儿急性重症坏死性小肠结肠炎夭折'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      }
    }

    // 2. 幼童与少儿期 (1–14 岁)
    if (age <= 14) {
      if (year < 1950) {
        const pool = [
          '因霍乱与中毒性急性痢疾高热衰竭离世',
          '因恶性疟疾（打摆子）高热抽搐未能送医离世',
          '因白喉喉梗阻窒息不幸夭折',
          '在战乱流亡逃荒途中因恶疾暴发夭折'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 1980) {
        const pool = [
          '因流行性乙型脑炎高热未能挽回离世',
          '因暴发性流脑高热昏迷不幸离世',
          '因急性重症细菌性肺炎未能及时用上抗生素离世',
          '夏日野外水塘戏水不幸溺水身亡'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 2000) {
        const pool = [
          '因暴发性病毒性心肌炎急性发作抢救无效离世',
          '因急性淋巴细胞白血病多方救治无效离世',
          '因野外水域游泳溺水意外不幸溺亡',
          '在放学途中遭遇严重公路交通事故意外离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else {
        const pool = [
          '因急性恶性血液系统疾病多方救治无效离世',
          '因暴发性急性重症病毒性心肌炎不治离世',
          '在校外突发严重道路交通意外创伤不治',
          '因急性重症脑干脑炎抢救无效离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      }
    }

    // 3. 青年与年轻壮年期 (15–35 岁)
    if (age <= 35) {
      // 习惯与生活标签响应
      if (tags && (tags.has('stay_up_late') || tags.has('exhaustion')) && Math.random() < 0.28) {
        return '因长期高强度通宵熬夜与极度过劳，突发急性心源性猝死';
      }
      if (tags && tags.has('drinker') && Math.random() < 0.6) {
        return '在连续过量烈酒应酬后突发暴发性急性重症胰腺炎离世';
      }
      if (tags && tags.has('smoker') && Math.random() < 0.5) {
        return '因长期吸烟诱发突发自发性张力性气胸急性衰竭离世';
      }

      // 性别特定死因：只有近一年内真实发生过生育的女性，才进入产妇死亡风险。
      const recentBirth = this.character && this.character.lastChildbirthYear &&
        this.currentYear - this.character.lastChildbirthYear <= 1;
      if (sex === '女' && tags && tags.has('married') && recentBirth && Math.random() < 0.25) {
        if (year < 1978) {
          return '在农村土法接生中遭遇严重难产与产后大出血感染不幸离世';
        } else {
          return '在分娩过程中突发极为凶险的暴发性羊水栓塞大出血不幸离世';
        }
      }

      // 时代青年死因池
      if (year < 1950) {
        const pool = [
          '因浸润型肺结核空洞破裂大咯血未能救治离世',
          '因暴发性伤寒高热不退与消化道穿孔离世',
          '因霍乱急性重度脱水休克未能抢救离世',
          sex === '男' ? '在战火动荡中被拉壮丁或前线流弹创伤感染离世' : '在战火流离颠沛中染上恶性痢疾未能救治离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 1980) {
        const pool = [
          '因暴发性病毒性肝炎诱发急性重度肝坏死衰竭离世',
          '因重度肺结核反复大咯血在隔离病房不幸离世',
          '因急性重症心肌炎未能有效复苏不幸离世',
          '在水利工程与高强度农耕中遭遇塌方工伤意外离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 2000) {
        const pool = [
          '因暴发性重症心肌炎猝发导致急性心力衰竭离世',
          '因急性坏死性重度胰腺炎多器官抢救无效离世',
          '在长途公路出行业务途中遭遇特大交通事故创伤不治',
          '因恶性淋巴瘤晚期多发转移多方求医不治离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else {
        // 2000–2026年现代青年死因 (绝对排除了“老年”、“衰老”等一切老年词汇)
        const pool = [
          '突发急性心源性猝死，经医院多方抢救无效不幸英年早逝',
          '因青年期高发恶性肿瘤晚期恶病质，多方化疗救治不治离世',
          '因暴发性急性重症病毒性心肌炎并发恶性心律失常离世',
          '因急性坏死性胰腺炎合并全身重度感染性休克离世',
          '在深夜国道公路长途行程中遭遇严重机动车碰撞意外创伤不治'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      }
    }

    // 4. 中青年与中年期 (36–59 岁)
    if (age <= 59) {
      if (tags && (tags.has('stay_up_late') || tags.has('exhaustion')) && Math.random() < 0.28) {
        return '中年肩负家庭与工作双重重压，长期严重透支引发突发急性心梗猝死';
      }
      if (tags && tags.has('smoker') && Math.random() < 0.6) {
        return '因数十载烟龄诱发中晚期中央型肺癌广泛转移衰竭离世';
      }
      if (tags && tags.has('drinker') && Math.random() < 0.6) {
        return '因长期大量饮酒诱发重度肝硬化失代偿期腹水并上消化道大出血离世';
      }

      if (year < 1980) {
        const pool = [
          '因长期过度劳累与营养不良诱发重度肺源性心脏病衰竭离世',
          '因中晚期胃部恶性肿瘤恶竭衰竭离世',
          '因突发大面积重度脑溢血偏瘫昏迷未能醒来',
          '因重度化脓性腹膜炎送医不及时不幸离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 2000) {
        const pool = [
          '因突发急性大面积前壁心肌梗死抢救无效离世',
          '因原发性晚期肝癌竭力多方保守治疗无效离世',
          '因高血压性基底节区重度脑出血不治离世',
          '因中晚期消化系统恶性肿瘤广泛浸润衰竭离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else {
        const pool = [
          '因急性广泛前壁心肌梗死伴心源性休克抢救无效离世',
          '因中晚期恶性肿瘤（肺癌/消化道肿瘤）全身多发转移衰竭离世',
          '因脑基底节区突发重度出血破入脑室中枢衰竭离世',
          '因原发性肝脏恶性肿瘤晚期失代偿衰竭离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      }
    }

    // 5. 初老与老年期 (60–74 岁)
    if (age <= 74) {
      if (year < 1980) {
        const pool = [
          '因慢性支气管炎合并重度肺气肿与感染呼吸衰竭离世',
          '因重度脑卒中后遗症昏迷长期卧床肺部感染离世',
          '因慢性肾功能衰竭尿毒症终末期离世',
          '因晚期消化道恶疾恶病质离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else if (year < 2000) {
        const pool = [
          '因冠状动脉粥样硬化性心脏病急性加重合并心衰离世',
          '因慢性阻塞性肺疾病(COPD)急性加重呼吸衰竭离世',
          '因大面积缺血性脑卒中并中枢性呼吸衰竭离世',
          '因晚期恶性肿瘤全身消耗衰竭离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      } else {
        const pool = [
          '因冠状动脉粥样硬化性心脏病合并慢性心力衰竭急性加重离世',
          '因重度慢性阻塞性肺疾病合并重症肺部感染衰竭离世',
          '因各类中晚期恶性肿瘤终末期恶竭离世',
          '因重度脑梗死大面积软化并中枢神经衰竭离世'
        ];
        return pool[Math.floor(Math.random() * pool.length)];
      }
    }

    // 6. 高龄老人期 (75 岁及以上 - 唯有此处才允许出现“老年多器官衰退”与“高龄自然终老”)
    if (age >= 85) {
      const pool = [
        '一生历经近一个世纪家国风雨，于耄耋之年寿终正寝自然终老',
        '因高龄体衰，多器官功能自然衰退，安详长眠离世',
        '因极高龄重症肺部感染合并多系统循环功能自然衰竭终老'
      ];
      return pool[Math.floor(Math.random() * pool.length)];
    } else {
      // 75–84 岁
      const pool = [
        '因老年多器官功能退化衰退，在亲人守候中平静离世',
        '因高龄慢性基础疾病终末期合并肺部感染衰竭离世',
        '因重度脑血管病后遗症致中枢系统与循环功能渐进性衰退离世',
        '因高龄体弱心肺功能衰竭安详离世'
      ];
      return pool[Math.floor(Math.random() * pool.length)];
    }
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
    const cause = this.getAuthenticCauseOfDeath(
      era,
      this.currentAge,
      this.character.sex,
      this.character.attributes,
      this.character.tags,
      fatalEvent
    );

    this.deathInfo = {
      age: this.currentAge,
      year: this.currentYear,
      cause,
      isNatural: false,
      isDisaster: false
    };

    let milestoneTitle = '魂归故土';
    if (this.currentAge < 15) milestoneTitle = '幼年夭折';
    else if (this.currentAge < 45) milestoneTitle = '英年早逝';
    else if (this.currentAge < 65) milestoneTitle = '中途陨落';
    else if (this.currentAge >= 80) milestoneTitle = '寿终正寝';

    this.character.milestones.push({
      year: this.currentYear,
      age: this.currentAge,
      title: milestoneTitle,
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
    this.refreshCityContext();

    let cause = '见证近百年家国沧桑，于当今盛世安享晚年';
    let title = '见证盛世';
    let detail = `从${this.character.birthYear}年风雨中一路走来，终在2026年与时代相拥，一生平凡而丰厚。`;

    if (finalAge <= 2) {
      cause = '于2026年平安降生，在家人日夜守护下初识这个世界';
      title = '襁褓新生';
      detail = `于${this.character.birthYear}年降生，尚在襁褓之中，在家人的呵护下开始打量这个崭新的世界。`;
    } else if (finalAge <= 5) {
      cause = '在当今时代家庭的悉心照护下平稳成长，正是牙牙学语的幼年';
      title = '稚子幼年';
      detail = `于${this.character.birthYear}年降生，在祖辈与父辈的照护下蹒跚学步，于2026年长成稚嫩幼童。`;
    } else if (finalAge <= 11) {
      cause = '在当今时代家庭的倾力托举与照护中平稳成长，正值童年求学之时';
      title = '童年学子';
      detail = `于${this.character.birthYear}年降生，在祖辈与父辈的倾力托举下，于2026年成长为求学少年。`;
    } else if (finalAge < 18) {
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

    // 统计学预期余命区间（基于国家统计局分年龄分性别生命表，严禁预测2026年后的具体事件）
    let remainingRange = '45–52 年';
    let totalExpectedAgeRange = '78–85 岁';
    if (finalAge <= 16) {
      remainingRange = '65–72 年';
      totalExpectedAgeRange = '79–86 岁';
    } else if (finalAge <= 30) {
      remainingRange = '50–57 年';
      totalExpectedAgeRange = '78–85 岁';
    } else if (finalAge <= 50) {
      remainingRange = '32–38 年';
      totalExpectedAgeRange = '79–85 岁';
    } else if (finalAge <= 70) {
      remainingRange = '15–20 年';
      totalExpectedAgeRange = '80–86 岁';
    } else {
      remainingRange = '7–12 年';
      totalExpectedAgeRange = '83–89 岁';
    }

    this.character.actuarialExpectancy = {
      currentAge: finalAge,
      remainingRange,
      totalExpectedAgeRange,
      disclaimer: '基于统计规律的典型轨迹推演，非真实个人经历；2026年之后的人生充满无限可能。'
    };

    // 若为 2010 年及以后出生角色，解锁传承视角（推演父辈与祖辈典型轨迹）
    if (this.character.birthYear >= 2010) {
      this.character.lineageHistory = this.generateLineageHistory(this.character);
    }

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

    const isAlive2026 = !!(this.deathInfo && this.deathInfo.isAliveIn2026 === true);

    // 针对 2026 年依然在世的角色（未完待续，根据生命表展现健康余命）
    if (isAlive2026) {
      let eduLevel = this.character.educationLevel || '初级中等教育在读';
      if (this.character.birthYear >= 2010) {
        eduLevel = age <= 6 ? '学前幼儿阶段' : (age <= 12 ? '小学义务教育阶段' : '初级中等教育在读');
      }
      const lifePct = Math.min(96, Math.max(50, Math.round(50 + (age / (expectedLife || 75)) * 45)));

      return {
        lifespan: {
          val: age,
          expected: expectedLife,
          percentile: lifePct,
          desc: `健康平稳行至2026新时代，继续见证日新月异的神州大地（当年新生儿预期寿命约 ${expectedLife} 岁）`
        },
        education: {
          level: eduLevel,
          percentile: 85,
          desc: `顺应国家教育普及发展浪潮，知识技能基础良好`
        },
        wealth: {
          tier: this.character.economicLevel || '寻常温饱',
          percentile: 70,
          desc: `依托两代人的汗水积累，享有稳定的现代物质生活与家庭托举`
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

    const edu = this.character.educationLevel || '未入学';
    let eduLevel = edu;
    let eduPercentile = 40;

    if (edu.includes('大') || edu.includes('本') || edu.includes('研') || this.character.tags.has('higher_ed_degree')) {
      eduLevel = edu.includes('大专') ? '大专学历' : '大学本科及以上';
      eduPercentile = 96;
    } else if (edu.includes('高') || edu.includes('中专') || this.character.tags.has('high_school_student') || this.character.tags.has('vocational_student')) {
      eduLevel = (edu.includes('中专') || this.character.tags.has('vocational_student')) ? '中专 / 职校技校' : '普通高中学历';
      eduPercentile = 80;
    } else if (edu.includes('初') || this.character.tags.has('junior_high')) {
      eduLevel = '初中文化程度';
      eduPercentile = 60;
    } else if (edu.includes('小') || this.character.tags.has('primary')) {
      eduLevel = '小学文化程度';
      eduPercentile = 35;
    } else {
      eduLevel = this.character.attributes.knowledge >= 30 ? '识字水平（扫盲/自学）' : '未入学（文化底子薄）';
      eduPercentile = 15;
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
        desc: `在同年代出生人群中寿命排前 ${Math.max(1, 100 - lifePercentile)}% 左右（当年新生儿平均预期寿命约为 ${expectedLife} 岁）`
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

    const clampYear = y => Math.min(y, 2026);
    const pushStage = (timeline, start, end, stage, detail) => {
      if (start > 2026) return;
      timeline.push({ period: `${start} — ${clampYear(Math.max(start, end))} 年`, stage, detail });
    };

    // 1. 祖辈轨迹：按实际出生年份生成，不能把 1961 年后出生者写成亲历三年困难时期
    const grandTimeline = [];
    let grandChildhood;
    if (grandBirthYear <= 1958) {
      grandChildhood = `生于新中国初建时期，童年亲历三年困难时期（1959–1961），靠红薯干与国家定粮度日，在朴素清贫中扎下勤俭家风。`;
    } else if (grandBirthYear <= 1961) {
      grandChildhood = `出生于困难时期前后，幼年在票证与定量供应中度过，靠粗粮和邻里互助熬过清苦岁月。`;
    } else if (grandBirthYear <= 1977) {
      grandChildhood = `在集体化与票证岁月中度过童年，穿着补丁衣服上学，放学后帮家里割草、拾柴、照看弟妹。`;
    } else {
      grandChildhood = `在改革开放初期度过童年，物质仍不宽裕，但街市渐渐热闹，家里第一次添置了收音机或黑白电视。`;
    }
    pushStage(grandTimeline, grandBirthYear, grandBirthYear + 15,
      grandBirthYear <= 1961 ? '童年与困难时期记忆' : '童年与集体岁月', grandChildhood);

    if (grandBirthYear + 16 <= 2026) {
      const youthDetail = isUrban
        ? `青年期按政策招工进入${char.cityName}国营厂矿或街道单位做工，历经工业建设岁月，按工龄与级别领取粮票工资。`
        : `在公社生产大队挣工分、修筑水库水利设施，参加农业集体劳动，打下吃苦耐劳的体力底子。`;
      pushStage(grandTimeline, grandBirthYear + 16, grandBirthYear + 25, '青年劳作与集体建设', youthDetail);
    }

    if (grandBirthYear + 28 <= 2026) {
      const reformDetail = isUrban
        ? `迎来改革开放与国企转轨浪潮，经历单位福利分房或房改购房，操持一家温饱，抚育下一代成长。`
        : `赶上家庭联产承包责任制，大包干解决一家温饱，农闲兼做零工运输，支撑儿女学杂开支。`;
      pushStage(grandTimeline, grandBirthYear + 28, grandBirthYear + 40, '改革开放与家门立业', reformDetail);
    }

    const grandLateStart = Math.max(grandBirthYear + 41, 2000);
    if (grandLateStart <= 2026) {
      const grandAge2026 = 2026 - grandBirthYear;
      const lateStage = grandAge2026 >= 60 ? '晚年桑榆与照看幼孙' : '中年操持与照看孙辈';
      const pensionLine = grandAge2026 >= 60
        ? (grandBirthYear <= 1949 ? '领取退休金' : '领取基础养老金')
        : '仍在操持家务或打零工';
      pushStage(grandTimeline, grandLateStart, 2026, lateStage,
        `${grandAge2026 >= 60 ? '步入晚年' : '步入中年'}，${pensionLine}，常在老家小院侍弄菜圃，或进城帮衬照护孙辈（即你），在安宁中守望家族生生不息。`);
    }

    // 2. 父辈轨迹：教育、就业与住房文案由 parentJob 驱动，避免“下岗待业”被写成知识白领
    const parentJob = char.parentJob || '';
    const parentIsLaidOff = /下岗|待业|失业|无业|裁员/.test(parentJob);
    const parentIsKnowledge = /教师|医生|医护|工程师|科研|干部|公务员|会计|律师|白领|知识分子/.test(parentJob);
    const parentIsFarmer = /农|种植|养殖|社员|生产队/.test(parentJob);
    const parentIsMerchant = /商|店|摊|个体|买卖|生意/.test(parentJob);

    const parentTimeline = [];
    let parentEducation;
    if (!isUrban || parentIsFarmer) {
      parentEducation = `完成乡村初中学业后就读中专技校或拜师学手艺，立志通过技术走出土地。`;
    } else if (parentIsLaidOff) {
      parentEducation = `在国企子弟学校读完初高中，毕业后按政策进入国营企业当工人，捧过几年“铁饭碗”。`;
    } else if (parentIsKnowledge) {
      parentEducation = `在九年义务教育普惠中读完初高中，适逢高校大扩招浪潮，考入大专院校就读，成为家族首代知识白领。`;
    } else {
      parentEducation = `在九年义务教育中读完初高中，毕业后进入工厂、商店或服务行业谋生，靠勤恳踏实站稳脚跟。`;
    }
    pushStage(parentTimeline, parentBirthYear, parentBirthYear + 18, '求学与升学改制', parentEducation);

    let parentEmployment;
    if (!isUrban || parentIsFarmer) {
      parentEmployment = `搭上南下民工大潮的绿皮火车，在沿海制造业车间、建筑工地或物流网点奔波，凭辛勤汗水汇款安家。`;
    } else if (parentIsLaidOff) {
      parentEmployment = `遭遇国企改制与下岗分流，靠摆摊、蹬三轮、做保安等零工维持一家生计，在市场化浪潮中咬牙支撑。`;
    } else if (parentIsKnowledge) {
      parentEmployment = `步入社会直面国企重组与外资民企蓬勃期，进入学校、医院、机关或现代企业打拼，经历市场风浪与行业周期。`;
    } else if (parentIsMerchant) {
      parentEmployment = `在街边开店、跑批发或做小生意，起早贪黑核算进销差价，在市场竞争中一点点攒下家底。`;
    } else {
      parentEmployment = `进入国营或民营工厂、物流仓储与城市服务行业，靠加班和手艺支撑家庭开支。`;
    }
    pushStage(parentTimeline, parentBirthYear + 19, parentBirthYear + 26, '就业打拼与经济转轨', parentEmployment);

    if (parentBirthYear + 27 < childBirthYear) {
      const familyDetail = !isUrban || parentIsFarmer
        ? `在老家宅基地翻建二层红砖楼房，或在务工城市租房栖身，省吃俭用为新生命到来做好准备。`
        : parentIsLaidOff
          ? `在国企改制后靠积蓄与亲友帮衬成家，租住或购买小户型住房，精打细算迎接新生命。`
          : `适逢福利分房终结与商品房市场化，倾注两代人积蓄背负按揭贷款在城市购置首套住房，建立家庭。`;
      pushStage(parentTimeline, parentBirthYear + 27, childBirthYear - 1, '房改安家与成家立业', familyDetail);
    }

    const parentAge2026 = 2026 - parentBirthYear;
    const childcareEra = childBirthYear <= 2019
      ? '经历校外辅导班热潮、疫情三年陪读与生活转段'
      : '经历疫情后的生活转段、育儿成本上升与教育政策调整';
    const parentStage = parentAge2026 >= 40 ? '托举子女与中年重任' : '初为人父母与事业爬坡';
    pushStage(parentTimeline, childBirthYear, 2026, parentStage,
      `迎来你的出生。${parentAge2026 >= 40 ? '人到中年承担上有老下有小的重担' : '初为人父母，在事业与家庭之间来回奔忙'}，${childcareEra}，倾尽所能护佑你平安成长。`);

    // 3. 角色自身（2010-2026 童年）：只描述出生后真实经历过的年份，禁止倒序与出生前记忆
    const childTimeline = [];
    const childAge2026 = 2026 - childBirthYear;
    const earlyEnd = clampYear(childBirthYear + 5);
    let earlyDetail;
    if (childAge2026 <= 2) {
      earlyDetail = `于${childBirthYear}年降生，尚在襁褓之中，在家人日夜守护下认识这个崭新的世界。`;
    } else if (childBirthYear >= 2016) {
      earlyDetail = `降生于移动互联网与智能终端普及的时代，在家庭的照拂、早教绘本与亲子陪伴中度过学前时光。`;
    } else {
      earlyDetail = `降生于中国综合国力腾飞与移动互联网兴起的年代，在家庭的照拂、早教绘本与智能终端的陪伴中步入童年。`;
    }
    pushStage(childTimeline, childBirthYear, earlyEnd, '数字时代的学前生活', earlyDetail);

    if (childBirthYear + 6 <= 2026) {
      let schoolDetail;
      if (childBirthYear <= 2014) {
        schoolDetail = `背上书包走进校园，亲历了三年疫情网课居家打卡、校外“双减”落地与中考改革，在飞速演进的时代中成长。`;
      } else if (childBirthYear <= 2019) {
        schoolDetail = `背上书包走进校园，在疫情后的校园生活中适应线上线下混合教学，经历“双减”与素质教育改革。`;
      } else {
        schoolDetail = `背上书包走进校园，在移动互联网与素质教育改革的环境中开始求学岁月。`;
      }
      pushStage(childTimeline, childBirthYear + 6, 2026, '求学岁月与同龄记忆', schoolDetail);
    }

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
    this.lastEraDecisionYear = -999;
    this.isGameOver = false;
    this.deathInfo = null;
    this.narrativeTension = 35 + Math.floor(Math.random() * 25);
    this.nextDecisionCooldownUntil = 0;

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
    let parentJob;
    if (isUrban) {
      const typicalJobs = indProfile.typicalJobs || ['国营厂技术员', '普通工人'];
      parentJob = typicalJobs[Math.floor(Math.random() * typicalJobs.length)];
    } else {
      parentJob = this.sampleRuralJob(indEraKey);
    }
    const familyClass = this.classifyFamilyClass(parentJob, isUrban);
    const familyDetail = `${urbanRural === 'urban' ? city.type : '乡村农户'} · ${parentJob}`;
    const initCareerTrack = this.determineInitialCareerTrack(isUrban, city, familyClass, parentJob);

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
      cityShortName: city.shortName || cityDisplay.displayName,
      cityHistoricalName: cityDisplay.displayName,
      birthCityName: cityDisplay.displayName,
      cityOfficialName: city.name,
      cityType: city.type,
      cityFoundingYear: city.foundingYear,
      region: province.region,
      urbanRural,
      familyClass,
      familyDetail,
      parentJob,
      industryPillar: indProfile.pillar,
      industryNature: indProfile.nature || '',
      economicLevel: '温饱',
      siblingsCount: 2,
      attributes,
      lifeRhythm: {
        marriageBaseAge: (urbanRural === 'rural' || birthYear < 1980)
          ? 20 + Math.floor(Math.random() * 5)
          : 21 + Math.floor(Math.random() * 6),
        careerPromoteAges: [
          22 + Math.floor(Math.random() * 3),
          33 + Math.floor(Math.random() * 5),
          46 + Math.floor(Math.random() * 5)
        ]
      },
      educationLevel: '未入学',
      careerTrack: initCareerTrack,
      careerRank: '初生幼年',
      occupation: isUrban ? '城镇孩童' : '乡野幼童',
      tags: new Set([
        urbanRural,
        sex === '男' ? 'male' : 'female',
        province.id,
        initCareerTrack,
        '温饱'
      ]),
      causalityReview: [],
      maritalStatus: '未婚',
      hasChildren: false,
      lastChildbirthYear: null,
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
    this.usedDetailSnippets = new Set();
    this.detailUsage = {};
    this.lastDetailSnippet = '';
    this.lastCitySnippetDecade = null;
    this.lastSentenceOpener = '';
    this.eventCooldowns = {};
    this.currentPendingDecision = null;
    this.lastEraDecisionYear = -999;
    this.isGameOver = false;
    this.deathInfo = null;
    this.narrativeTension = 35 + Math.floor(Math.random() * 25);
    this.nextDecisionCooldownUntil = 0;
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

// 挂载至全局与 Node 模块导出
if (typeof window !== 'undefined') {
  window.SimulationEngine = SimulationEngine;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SimulationEngine;
}
