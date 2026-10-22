# -*- coding: utf-8 -*-
"""
2000–2015 新世纪腾飞与数字时代：四大机制事件批次 (16条)
A. 路径补救 (IT培训班跨行转码、农民工考取高压焊工证、自学专升本、加盟连锁早点铺)
B. 渐进伤害 (长期久坐腰间盘突出、海鲜不洁急性肠胃炎、土三七偏方肝损伤、感冒熬夜病毒性心肌炎)
C. 经济诱惑 (跟风配资炒股遭遇股灾、磁疗床垫保健品骗局、快招网红奶茶加盟陷阱、掏空全家上车商品房)
D. 亲友离别 (非典隔离期隔窗守望、母亲ICU呼吸机自费陪护抉择、借钱买房借条成死账、汶川震后结对助学)
"""

def get_events():
    return [
        # --- A. 路径补救 ---
        {
            "id": "evt_2000_2015_a1_jisuanji_peixun",
            "tier": "era",
            "title": "数字浪潮：借钱报名软件培训班转行初级码农",
            "yearRange": [2002, 2015],
            "targetAge": [21, 35],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "入世后中国互联网与软件外包迅猛发展，北大青鸟、达内等IT职业培训班遍地开花，四到六个月集中脱产实训成为大批非计算机专业青年跨入高薪IT业的主要跳板。",
            "narrative": "普通文科大专毕业后在小商贸公司拿八百元底薪做文员。中关村与科技园的程序员起薪已开到四五千，你站在职业软件工程师脱产班门口，学费要一万两千元借贷。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "向亲戚借齐一万两千元学费并签下培训贷，脱产半年每天在机房苦练代码十四个小时",
                    "choiceTags": ["时代：2000–2015", "年龄：21–35", "地域：全国城市", "门槛：有学习意愿的大专青年"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "结业通过外包项目考核顺利入职软件园科技公司做初级前端开发，月薪跃升至四千元，半年内还清全部借款！",
                            "effect": {"wealth": 35, "mentality": 30, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "抓住PC互联网黄金时代红利成功转行软件工程师，踏入中产门槛。",
                            "status": "status_white_collar"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "长期通宵敲代码致重度干眼症与腱鞘炎，手腕红肿打封闭针，虽入职成功但体能消耗较大。",
                            "effect": {"health": -15, "wealth": 20, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "高强度转码集训引发轻微慢性劳损。"
                        }
                    ]
                },
                {
                    "text": "怀疑培训班是割韭菜骗局，拒绝借钱背贷，安守现状继续做商贸公司打字文员",
                    "choiceTags": ["时代：2000–2015", "年龄：21–35", "地域：全国城市", "门槛：规避借贷者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "虽然没有负债风险，但月薪在通胀下十年未见显著增长，逐渐被新一代年轻应届生边缘化。",
                            "effect": {"wealth": 5, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "错失IT黄金转型期，长期停留在基层低薪文员岗。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_a2_nongmingong_hanbing",
            "tier": "era",
            "title": "技术立足：进城力工自费考取压力容器高压焊工证",
            "yearRange": [2003, 2015],
            "targetAge": [20, 45],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "新世纪全国重大基建与造船、石化产业爆发，持质监局锅炉压力容器焊工特种作业证的熟练技术工人日薪达三四百元，成为农民工向高技术蓝领跃升的黄金通道。",
            "narrative": "在建筑工地拌了三年水泥、扛了三年钢筋，浑身是泥日薪才六十元。你看着造船厂车间里的高压焊工戴着防护面罩焊花飞溅，按日结算三百元且供不应求。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "拿出一年积蓄两千五百元报名安监焊工考证班，克服电弧强光刺眼，反复练习鱼鳞焊缝",
                    "choiceTags": ["时代：2000–2015", "年龄：20–45", "地域：工业园区", "门槛：吃苦耐劳打工者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "无损探伤拍片一次性全优通过！顺利拿到特种设备高压焊工证，被大型造船厂高薪录用为高级技工，月入过万。",
                            "effect": {"wealth": 40, "mentality": 35, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "从工地苦力成功升级为国家级特种高压焊工，收入与地位跃迁。",
                            "status": "status_skilled_welder"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "练习电焊时不慎电弧晃眼引发急性电光性眼炎，双眼剧烈眼痛流泪两日，点冷牛奶与眼药水后愈合。",
                            "effect": {"health": -15, "wealth": 25, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "考证电光晃眼轻微眼损无大碍。"
                        }
                    ]
                },
                {
                    "text": "害怕电焊有毒烟尘伤害身体，继续在工地上做小工搬砖推沙包",
                    "choiceTags": ["时代：2000–2015", "年龄：20–45", "地域：工业园区", "门槛：畏缩保守者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "年复一年在工地上出卖力气，随着年龄渐长腰腿劳损加重，逐渐在体力工市场失去竞争优势。",
                            "effect": {"health": -10, "wealth": 10, "mentality": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "未能实现技术晋级，长期受困于重体力劳务消耗。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_a3_zhuanshengben",
            "tier": "era",
            "title": "圆梦本科学位：在职自考攻克最后三门统考",
            "yearRange": [2001, 2014],
            "targetAge": [22, 38],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "高校扩招后大专文凭在职场迅速贬值，成人高等教育专升本与自考专升本成为在职员工晋升中层、参加公务员考试的必备硬性门槛。",
            "narrative": "单位进行中层竞聘，你的业务能力全处室第一，但人事处明确红头文件规定‘必须具备全日制或国家承认本科学历及学士学位’。你看着还剩最后三门攻坚的自考准考证。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "请掉全部年休假闭关苦读，聘请名师辅导攻克高数与学位英语，志在必得拿下学位",
                    "choiceTags": ["时代：2000–2015", "年龄：22–38", "地域：全国城市", "门槛：在职专科进修者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "三门统考全过，毕业论文答辩获评良好！顺利拿到省重点大学成人本科学历与学士学位证书，破格提拔为部门副经理。",
                            "effect": {"mentality": 35, "wealth": 30, "family": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "在职拿下自考本科与学位彻底补齐学历短板，晋升中层骨干。",
                            "status": "status_college_diploma"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "高压备考导致长期失眠与轻度偏头痛，好在学位顺利到手，身心逐步通过休假调整复原。",
                            "effect": {"health": -10, "wealth": 20, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "备考疲劳稍有神经衰弱无后遗症。"
                        }
                    ]
                },
                {
                    "text": "抱怨体制只认死文凭不看真本事，怒而放弃考试，寄希望于领导讲人情照顾",
                    "choiceTags": ["时代：2000–2015", "年龄：22–38", "地域：全国城市", "门槛：抱侥幸心理者"],
                    "outcomes": [
                        {
                            "type": "redirected",
                            "weight": 100,
                            "log": "竞聘硬性条件卡死无法上报，副经理职位被新来的名校本科生顶替，职场天花板彻底被焊死。",
                            "effect": {"mentality": -20, "wealth": 0},
                            "isFatal": False,
                            "hiddenRiskLog": "放弃学历补全机会，职场发展遭受硬性资格天花板制约。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_a4_kaidian_chuangye",
            "tier": "era",
            "title": "商海转型：加盟品牌连锁便利店自主创业",
            "yearRange": [2005, 2015],
            "targetAge": [28, 55],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "城市化进程中‘美宜佳’、‘全家’、‘红旗连锁’等品牌便利店深入社区街道，特许加盟模式成为许多失业转型人员与中小创业者稳健立足的选择。",
            "narrative": "原单位业务调整遭遇裁员，领到八万元补偿金。小区门口临街旺铺招租，知名品牌连锁便利店正在招募社区合伙加盟商，免加盟费提供统一配送系统。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "抵押积蓄投资加盟便利店，全家倒班轮流守店开通24小时营业，靠勤快与热诚服务打动街坊",
                    "choiceTags": ["时代：2000–2015", "年龄：28–55", "地域：城市社区", "门槛：有数万元启动资金者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "依托完善供应链与便民早餐快递服务，小店月营业额突破六万元，不仅实现自负盈亏更净赚全家丰厚收益！",
                            "effect": {"wealth": 40, "family": 25, "mentality": 30, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "成功切入城市连锁零售业态，靠家族协作实现小康创业。",
                            "status": "status_self_employed"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "长期值夜班熬夜导致下肢静脉曲张轻度水肿，后雇佣半天兼职店员倒班改善。",
                            "effect": {"health": -15, "wealth": 25, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "创业早期劳累引起轻微下肢静脉曲张。"
                        }
                    ]
                },
                {
                    "text": "觉得开小卖部成天看店太受罪，把补偿金全额存进银行理财继续四处投简历找清闲工作",
                    "choiceTags": ["时代：2000–2015", "年龄：28–55", "地域：城市社区", "门槛：求轻松规避实业者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "投出的简历大多石沉大海，中年求职屡屡碰壁，虽然生活安闲但存款逐年缩水。",
                            "effect": {"wealth": -5, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "错失实体商业创业良机，求职遇冷陷入中年危机。"
                        }
                    ]
                }
            ]
        },

        # --- B. 渐进伤害与可错选项 ---
        {
            "id": "evt_2000_2015_b1_996_yaozhui",
            "tier": "era",
            "title": "职场劳损：长期久坐伏案腰椎间盘突出硬挺",
            "yearRange": [2005, 2015],
            "targetAge": [22, 45],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "随着电脑普及与互联网加班文化盛行，办公室白领长期伏案久坐缺乏锻炼，腰椎间盘突出症发病年龄大幅提前，多因盲目推拿按摩加重病情。",
            "narrative": "连续熬夜加班两周赶项目上线，右侧腰臀部突然如触电般剧痛，一路放射麻木至右小腿肚和脚背，甚至走不完五十米就得蹲下缓解。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "嫌去大医院拍片排队繁琐，就近在路边盲人按摩店让师傅猛踩后腰大骨进行重力复位",
                    "choiceTags": ["时代：2000–2015", "年龄：22–45", "地域：全国城市", "门槛：盲目粗暴推拿者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 75,
                            "log": "暴力踩踏导致原本破损的纤维环彻底脱垂碎裂，马尾神经受压急性大小便障碍，急送三甲医院行急诊椎板减压手术才免于瘫痪！",
                            "effect": {"health": -45, "wealth": -35, "mentality": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "不当暴力推拿致腰椎间盘急性巨大脱垂急诊手术，落下神经麻木残留。",
                            "status": "sequelae_chronic_backpain"
                        },
                        {
                            "type": "safe",
                            "weight": 25,
                            "log": "运气好仅是单纯腰背筋膜炎，师傅推拿后肌肉放松大半，侥幸未伤及椎间盘核心。",
                            "effect": {"health": 5, "wealth": -5, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "侥幸避开神经根损伤。"
                        }
                    ]
                },
                {
                    "text": "立即请假前往三甲骨科行腰椎核磁共振检查，遵医嘱绝对硬板床平躺休息两周配合牵引与神经营养药",
                    "choiceTags": ["时代：2000–2015", "年龄：22–45", "地域：全国城市", "门槛：具备现代医学常识者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 92,
                            "log": "规范卧床使得神经根水肿完全消退，配合麦肯基疗法核心肌群锻炼，疼痛彻底根除自如返岗。",
                            "effect": {"health": 10, "wealth": -10, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "科学制动平卧与正规康复彻底治愈腰突，未遗留神经后遗症。"
                        },
                        {
                            "type": "injured",
                            "weight": 8,
                            "log": "虽避免了手术，但久坐后偶有腰部酸紧，需长期注意坐姿防范。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "偶有轻度腰酸但无神经根压迫。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_b2_haixian_changweiyan",
            "tier": "era",
            "title": "夏令不洁：夜市大排档海鲜死虾急性胃肠炎",
            "yearRange": [2003, 2015],
            "targetAge": [16, 65],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "城市夜市大排档冷链储存不规范，死海鲜变质滋生副溶血性弧菌与嗜水气单胞菌，极易引发伴随剧烈脐周绞痛、血便脱水的感染性腹泻。",
            "narrative": "夏天和朋友在夜市大排档喝冰啤酒吃麻辣小龙虾与生蚝。凌晨两点腹部剧烈绞痛，上吐下泻连续七次，吐尽苦胆水，全身冷汗淋漓四肢发软打颤。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "觉得只是普通吃坏肚子，翻出抽屉里过期的止泻药和牛黄解毒片吞服，喝口开水蒙头大睡硬熬",
                    "choiceTags": ["时代：2000–2015", "年龄：16–65", "地域：全国城乡", "门槛：滥用过期药硬扛者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 70,
                            "log": "强力止泻药阻碍肠道病菌排出致毒血症，诱发重度脱水休克与急性肾损伤，次日被同住人叫120抬进急诊重症监护室抢救三天！",
                            "effect": {"health": -40, "wealth": -20, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "急性细菌性肠胃炎盲目止泻致感染性休克伤及肾功能。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "fatal",
                            "weight": 2,
                            "log": "剧烈呕吐误吸入呼吸道引起窒息并发恶性心律失常不幸离世。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "重症呕吐误吸窒息意外身故。"
                        },
                        {
                            "type": "safe",
                            "weight": 28,
                            "log": "自身肠道自净力极强，狂吐狂拉排空毒素后，多喝温水熬过了危险期，虚脱两天康复。",
                            "effect": {"health": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "排尽毒素脱险但胃肠黏膜需调理。"
                        }
                    ]
                },
                {
                    "text": "果断叫出租车直奔附近三甲医院发热门诊，做血常规化验，接受正规盐水输液与抗生素治疗",
                    "choiceTags": ["时代：2000–2015", "年龄：16–65", "地域：全国城乡", "门槛：果断正规急诊者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "急诊静脉补充电解质与第三代头孢输液，呕吐腹痛两小时内完全平息，次日精神饱满出院无大碍。",
                            "effect": {"health": 5, "wealth": -10, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "科学急诊补液与抗菌治疗迅速掐灭严重感染。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "急诊开销数百元，但迅速保全了身体元气。",
                            "effect": {"wealth": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "轻微经济支出换来健康平安。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_b3_tusanqi_ganposun",
            "tier": "era",
            "title": "民间偏方祸端：盲信土三七泡酒致肝小静脉闭塞",
            "yearRange": [2006, 2015],
            "targetAge": [35, 70],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "民间常混淆中药‘熟三七’与含吡咯烷生物碱的‘土三七’（菊三七）。长期服用土三七泡酒极易引起不可逆的肝窦阻塞综合征（肝小静脉闭塞症），表现为腹水黄疸。",
            "narrative": "膝关节骨质增生酸痛，邻居老中医热情推荐山里挖来的‘野生土三七’泡高度白酒，宣称活血化瘀神效。你每天晚饭按时喝两小杯，一个月后腹部鼓胀如鼓、双眼金黄尿如浓茶。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "听信邻居‘这是体内湿热在向外排毒反应’的荒谬解释，继续加量饮用并配合拔罐硬顶",
                    "choiceTags": ["时代：2000–2015", "年龄：35–70", "地域：全国城乡", "门槛：深陷迷信偏方排毒说者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 78,
                            "log": "不可逆的吡咯烷毒素导致肝内广泛微小静脉闭塞纤维化，大量腹水形成顽固性肝硬化失代偿期，终身需服药并丧失重体力劳动能力！",
                            "effect": {"health": -45, "wealth": -35, "mentality": -30},
                            "isFatal": False,
                            "hiddenRiskLog": "盲信土三七偏方致药物性肝窦阻塞与不可逆肝损伤。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "突发肝性脑病深昏迷合并食管胃底静脉曲张大出血不治身亡。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "土三七重度肝衰竭并发消化道大出血罹难。"
                        },
                        {
                            "type": "safe",
                            "weight": 19,
                            "log": "家人发现不对强行倒掉药酒送医保肝治疗，所幸服用剂量尚小，经半年药物排毒肝功能指标部分逆转。",
                            "effect": {"health": -20, "wealth": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "强制停用偏方险死还生保全性命。"
                        }
                    ]
                },
                {
                    "text": "察觉腹水黄疸异常立即停药，带上药酒样本直奔大学附属医院消化肝病中心排毒做肝穿刺确诊",
                    "choiceTags": ["时代：2000–2015", "年龄：35–70", "地域：全国城乡", "门槛：具备科学用药警惕者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 92,
                            "log": "专家精准锁定菊三七中毒，早期给予低分子肝素抗凝、前列地尔改善微循环与大剂量还原型谷胱甘肽，腹水全消，肝功恢复正常指标！",
                            "effect": {"health": 5, "wealth": -15, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "及时科学抗凝保肝阻断肝小静脉闭塞进展，彻底化险为夷。"
                        },
                        {
                            "type": "injured",
                            "weight": 8,
                            "log": "肝脏纤维化早期轻微病变已受控，日常需杜绝饮酒保护肝脏。",
                            "effect": {"health": -5, "wealth": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "轻微肝纤维化早期受控需遵医嘱戒酒。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_b4_ganmao_xinjiyan",
            "tier": "era",
            "title": "重感硬撑：青年感冒通宵熬夜突发心肌炎",
            "yearRange": [2004, 2015],
            "targetAge": [16, 38],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "柯萨奇病毒、流感病毒引起的重感冒在青壮年群体中若得不到充分休息，病毒可直接侵犯心肌细胞诱发急性暴发性心肌炎，猝死率极高。",
            "narrative": "重感冒发烧三十八度五、咽痛咳嗽，恰逢年底考核冲刺。你吞下两粒泰诺后在办公室连轴转通宵两天，清晨突然胸闷如压巨石、呼吸急促、心跳失常频发早搏。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "自恃二十多岁身体底子好，以为只是通宵缺觉，喝下两罐红牛强行支撑继续外出跟客户谈判",
                    "choiceTags": ["时代：2000–2015", "年龄：16–38", "地域：全国城市", "门槛：盲目逞强拼命三郎"],
                    "outcomes": [
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "暴发性心肌炎诱发恶性心室颤动心源性猝死，在谈判桌旁倒下未能抢救成功。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "重感冒通宵过劳死于急性暴发性心肌炎猝死。"
                        },
                        {
                            "type": "injured",
                            "weight": 77,
                            "log": "晕倒在会议室被送医查肌钙蛋白高出百倍，确诊重症心肌炎，在心内科重症监护室卧床一个月，留下了频发室性早搏与心肌收缩力减弱后遗症。",
                            "effect": {"health": -45, "wealth": -30, "mentality": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "心肌炎严重损伤心脏收缩力，落下终身心脏早搏旧疾。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "safe",
                            "weight": 20,
                            "log": "强大的年轻免疫力险险挺过心肌损伤关口，自行代谢后逃过一劫，吓出一身冷汗。",
                            "effect": {"health": -15, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "过度劳累后心肌受惊吓侥幸保全未衰竭。"
                        }
                    ]
                },
                {
                    "text": "觉察胸闷心悸异常不对劲，立刻向主管请假退出现场，直奔医院做心电图与心肌酶谱化验并绝对卧床",
                    "choiceTags": ["时代：2000–2015", "年龄：16–38", "地域：全国城市", "门槛：具备健康红线意识者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "早期发现心肌炎及时使用磷酸肌酸钠与大剂量维生素C营养心肌，严格平卧静养三周，心肌完全再生康复无任何杂音！",
                            "effect": {"health": 10, "wealth": -10, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "及时卧床静养避免暴发性恶化，完美护卫心脏核心机能。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "请假扣除当月绩效奖金，但换来了心脏一辈子的健康与安全。",
                            "effect": {"wealth": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "短暂薪资折损换得全身健康平安。"
                        }
                    ]
                }
            ]
        },

        # --- C. 经济系统与诱惑 ---
        {
            "id": "evt_2000_2015_c1_gumin_guzai",
            "tier": "era",
            "title": "股市激流：2007/2015全民炒股高杠杆配资爆仓",
            "yearRange": [2007, 2015],
            "targetAge": [22, 60],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 6,
            "factLevel": "确证",
            "historicalFact": "2007年大牛市上证冲上6124点与2015年配资牛市冲上5178点期间，全民炒股狂热，大量散户通过场外1:4高杠杆配资借贷炒股，随后遭遇千股跌停断崖式强平爆仓。",
            "narrative": "交易所大厅绿化带连大妈都在讨论股票涨停，朋友圈天天晒几万元收益。配资中介拉拢你称提供四倍场外配资杠杆，只需押进二十万积蓄就能操盘百万大单直奔财务自由。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "抵押房产取出全部储蓄加满四倍配资杠杆，全仓杀入当时炒得最火热的题材妖股",
                    "choiceTags": ["时代：2000–2015", "年龄：22–60", "地域：全国城市", "门槛：贪恋资本暴利博徒"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 80,
                            "log": "遭遇连续三个跌停板毫无流动性无法挂单卖出！配资公司无情执行穿仓强平，本金瞬间归零并倒欠配资公司十几万元债务！",
                            "effect": {"wealth": -65, "mentality": -40, "family": -30},
                            "isFatal": False,
                            "hiddenRiskLog": "高杠杆炒股遭遇极端千股跌停穿仓爆仓，家庭财富遭毁灭性洗劫。",
                            "status": "status_debt_burdened"
                        },
                        {
                            "type": "safe",
                            "weight": 20,
                            "log": "在暴跌前夕嗅到监管清查异动，提前果断清仓离场，狂赚两倍利润全身而退买下大平层！",
                            "effect": {"wealth": 70, "mentality": 35},
                            "isFatal": False,
                            "hiddenRiskLog": "在资本市场历史大顶惊险逃顶，豪取时代巨额财富。"
                        }
                    ]
                },
                {
                    "text": "牢记‘当所有人都在狂欢时就是风险顶点’，坚决不碰场外配资杠杆，守紧家庭现金底线",
                    "choiceTags": ["时代：2000–2015", "年龄：22–60", "地域：全国城市", "门槛：理性克制投资者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "数周后千股跌停奇观上演，无数追高配资者血本无归，你全家存款分文未损，心平气和过好安稳日子。",
                            "effect": {"mentality": 25, "wealth": 10, "family": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "克制人性贪婪避开股灾灭顶之灾，守住财富根基。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_c2_baojian_chuangdian",
            "tier": "era",
            "title": "银发陷阱：免费鸡蛋讲座忽悠老人两万买磁疗床垫",
            "yearRange": [2008, 2015],
            "targetAge": [48, 75],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "针对城市退休老年群体的保健品骗局在此时期泛滥，不法商家以清晨排队免费领鸡蛋、组织廉价一日游为诱饵，推销数万元的三无磁疗床垫、量子饮水机。",
            "narrative": "老母亲/老人每天清晨五点准时去社区小剧场听‘养生健康讲座’领两枚免费鲜鸡蛋。今天老人兴冲冲回家，执意要取出一万八千元养老存折去买一张‘包治百病防中风’的磁疗床垫。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "听之任之，甚至觉得老人开心就好不愿惹老人生气，顺从陪同去银行取款全额买下磁疗床垫",
                    "choiceTags": ["时代：2000–2015", "年龄：48–75", "地域：全国城乡", "门槛：纵容放任家属"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 80,
                            "log": "床垫不仅毫无疗效更因劣质加热丝漏电灼伤老人皮肤，两万元积蓄落入骗子腰包，骗子公司随后卷铺盖跑路维权无门。",
                            "effect": {"wealth": -30, "family": -20, "mentality": -25, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "放任老人购买虚假伪劣保健床垫，巨额财产受损且损害身体。",
                            "status": "status_asset_wiped"
                        },
                        {
                            "type": "safe",
                            "weight": 20,
                            "log": "老人躺在电热床垫上获得心理安慰睡得踏实，虽花掉冤枉钱但未造成器质损害。",
                            "effect": {"wealth": -25, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "破财消灾换取老人心理寄托。"
                        }
                    ]
                },
                {
                    "text": "坚决阻拦取款，耐心搜集央视《焦点访谈》曝光视频给老人讲透骗局套路，并向工商部门实名举报该黑窝点",
                    "choiceTags": ["时代：2000–2015", "年龄：48–75", "地域：全国城乡", "门槛：清醒维权守护家庭者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "执法大队迅速查封该虚假宣传窝点退还预付款，老人恍然大悟保全了两万元棺材本，对你的孝顺与理智夸赞不已。",
                            "effect": {"wealth": 20, "family": 30, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "科学防骗及时阻击养老黑窝点，守护家庭核心积蓄。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_c3_naicha_jiameng",
            "tier": "era",
            "title": "快招泡沫：轻信招商会加盟网红奶茶店血本无归",
            "yearRange": [2010, 2015],
            "targetAge": [22, 45],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "餐饮新消费浪潮下‘快招公司’层出不穷，通过花钱请托排队制造火爆假象，骗取创业者数万到十几万元加盟费与高价专用原料设备后迅速失联弃店。",
            "narrative": "豪华酒店招商加盟大会上，PPT大肆宣扬日流水过万元的网红奶茶模式。现场样板店排队上百人，招商经理信誓旦旦保证‘三个月回本，总部全程带店扶持’。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "被狂热氛围煽动当场刷卡交纳六万元加盟费并高价购入全套专用设备开店",
                    "choiceTags": ["时代：2000–2015", "年龄：22–45", "地域：城市商圈", "门槛：盲从加盟创业者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 85,
                            "log": "开业后发现所谓排队全系雇人托儿，总部提供的果糖茶叶价格比市面贵一倍且根本不提供技术辅导，撑了四个月亏空十万元无奈转让！",
                            "effect": {"wealth": -45, "mentality": -30, "family": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "陷入快招网红奶茶加盟合同陷阱，半生积蓄被收割一空。",
                            "status": "status_asset_wiped"
                        },
                        {
                            "type": "safe",
                            "weight": 15,
                            "log": "凭借绝佳大学城选址和自身自创特色奶盖口味逆风翻盘，摆脱总部自立招牌实现盈利开出分店。",
                            "effect": {"wealth": 40, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "在恶劣快招骗局中依靠个人产品实力奇迹突围。"
                        }
                    ]
                },
                {
                    "text": "深知餐饮创业十人九亏，冷静蹲点暗访同城已开门店的真实流水，发现破绽后断然拒绝签约",
                    "choiceTags": ["时代：2000–2015", "年龄：22–45", "地域：城市商圈", "门槛：审慎调研投资者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "两个月后该快招公司因合同诈骗被经侦查处，你暗自庆幸守住了十万元血汗钱，稳健理财生活无忧。",
                            "effect": {"wealth": 15, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "以严密尽调识破快招加盟陷阱，守住家庭财务底牌。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_c4_shoufu_maifang",
            "tier": "era",
            "title": "时代关口：掏空全家六个钱包上车城市商品房",
            "yearRange": [2008, 2015],
            "targetAge": [24, 45],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.09,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "新世纪全国大中城市房价经历多轮暴涨，‘掏空父母祖辈六个钱包凑首付、承担三十年房贷按揭’成为青年一代成家立业与财富分化的决定性历史节点。",
            "narrative": "售楼处人声鼎沸号牌抢光，均价从五千飙升到八千。房产中介催促今天再不下定金明天每平米再涨三百。把夫妻两人与双方父母的全部定期存款凑在一起刚好够三成首付。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "掏空三代人积蓄凑足首付签下三十年商业按揭贷款，咬牙买下两居室电梯商品房",
                    "choiceTags": ["时代：2000–2015", "年龄：24–45", "地域：大中城市", "门槛：敢于负债上车者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "交楼入住拿到红本房产证！随后五年内城市房价翻了两番，资产实现跨越式几何级暴增，奠定整个家族财富基石！",
                            "effect": {"wealth": 60, "family": 35, "mentality": 30},
                            "isFatal": False,
                            "hiddenRiskLog": "在城市化黄金上升期果断杠杆买房，搭上时代财富特快列车。",
                            "status": "status_homeowner"
                        },
                        {
                            "type": "entangled",
                            "weight": 10,
                            "log": "每月房贷占去工资大半沦为‘房奴’，不敢换工作不敢生病，虽资产升值但生活质量骤降。",
                            "effect": {"wealth": 30, "mentality": -15, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "高额月供带来持久还贷心理压力。"
                        }
                    ]
                },
                {
                    "text": "坚信房价过高泡沫必破，拒绝背负巨债做房奴，坚持把钱存银行长期租房生活",
                    "choiceTags": ["时代：2000–2015", "年龄：24–45", "地域：大中城市", "门槛：空头观望者"],
                    "outcomes": [
                        {
                            "type": "redirected",
                            "weight": 100,
                            "log": "数年后眼睁睁看着房价一路狂飙翻倍，原先的首付款如今连厕所都买不起，租金水涨船高，懊悔万分。",
                            "effect": {"wealth": -30, "mentality": -35, "family": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "固守传统观念看空房市，彻底被时代资产泡沫抛弃落伍。"
                        }
                    ]
                }
            ]
        },

        # --- D. 亲友关系网与离别 ---
        {
            "id": "evt_2000_2015_d1_feidian_shouwang",
            "tier": "era",
            "title": "封控守望：非典时期亲人进隔离病房隔窗相望",
            "yearRange": [2003, 2003],
            "targetAge": [16, 65],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "2003年春非典（SARS）疫情袭来，北京等地启动定点传染病医院整建制全封闭隔离，家属无法探视，仅靠电话和隔窗字条传递亲情守望相助。",
            "narrative": "满城空气中弥漫着84消毒液的气味，亲人突发高热咳嗽被救护车闭环送入定点传染病区全封闭隔离。你戴着12层纱布口罩站在警戒线外，仰望着三楼病房紧闭的窗户。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "天天冒雨在医院铁栏杆外守候，用大号白纸写下‘我们等你回家’高高举起，每天按时给护士站递送可口饭菜",
                    "choiceTags": ["时代：2003", "年龄：16–65", "地域：疫情封控城市", "门槛：深情守望者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "亲人看到窗外的标语精神大振战胜病魔，两周后核酸转阴平安解除隔离出院，全家相拥而泣情感坚不可摧！",
                            "effect": {"family": 40, "mentality": 35, "wealth": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "在非典至暗时刻以无畏深情托举亲人康复，铸就家庭不朽精神支柱。"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "在医院外淋雨感冒发烧被作为疑似病例留观两日，所幸排除感染，虚惊一场。",
                            "effect": {"health": -15, "mentality": 20, "wealth": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "守护至亲受惊留观平安解除。"
                        }
                    ]
                },
                {
                    "text": "畏惧传染不敢靠近医院，仅在家里打座机通话询问，严格居家足不出户消毒自保",
                    "choiceTags": ["时代：2003", "年龄：16–65", "地域：疫情封控城市", "门槛：科学自保者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "自身零暴露风险安全渡过疫情危机，亲人在医护悉心救治下如期康复出院，家庭平稳回归正常轨道。",
                            "effect": {"health": 5, "family": 15, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "恪守卫生防疫规程，全家安度非典难关。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_d2_peihu_icu",
            "tier": "era",
            "title": "生命天平：至亲病危进ICU有创呼吸机陪护抉择",
            "yearRange": [2006, 2015],
            "targetAge": [26, 60],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_orphan"],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "现代重症监护室（ICU）普及后，每日自费数千至上万元的高昂维持费用与气管插管有创呼吸机创伤，给无数面临至亲终末期抢救的家庭带来巨大的伦理与经济考验。",
            "narrative": "重症监护室厚重的铁门打开，主治大夫拿着病危通知书：老母亲/老人多器官衰竭，若上有创呼吸机加CRRT血滤每日自费八千元，仅能维持微弱生命体征，催你签字定夺。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "哪怕倾家荡产负债累累，也绝不放弃最后一丝希望，签字同意全套有创抢救方案",
                    "choiceTags": ["时代：2000–2015", "年龄：26–60", "地域：现代三甲医院", "门槛：倾囊救亲者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 60,
                            "log": "在ICU鏖战二十一天奇迹般脱离呼吸机转入普通病房！虽然花光全家十余万储蓄，但老人保全生命多陪伴了家人五年。",
                            "effect": {"wealth": -50, "family": 40, "mentality": 25, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "倾尽全家财力逆天改命，从死神手中抢回至亲性命。"
                        },
                        {
                            "type": "entangled",
                            "weight": 40,
                            "log": "虽全力抢救但老人终因不可逆脑死亡安详离世，全家背负沉重债务，在悲痛中料理后事。",
                            "effect": {"wealth": -55, "mentality": -35, "family": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "尽心尽力抢救至亲未能挽回，留下高昂医疗债务与终生慰藉。",
                            "status": "status_bereaved_parent"
                        }
                    ]
                },
                {
                    "text": "不忍老人临终遭受插管切开之苦，遵从老人生前意愿签字放弃有创抢救，转入安宁疗护病房陪伴走完最后一程",
                    "choiceTags": ["时代：2000–2015", "年龄：26–60", "地域：现代三甲医院", "门槛：推崇安宁尊严者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "在镇痛舒适的轻柔音乐中，握着老人的手平静安详辞世，没有痛苦插管，家人克制平静送终。",
                            "effect": {"wealth": -15, "mentality": 20, "family": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "选择尊严安宁疗护，以克制深情陪伴至亲无痛告别。",
                            "status": "status_bereaved_parent"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_d3_jieqian_fanmu",
            "tier": "era",
            "title": "人情幻灭：昔日大学至交借走买房首付款成死账",
            "yearRange": [2008, 2015],
            "targetAge": [24, 50],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "在民间财富快速积累与房产狂飙期，无抵押熟人借贷极易因投资失败、资产暴跌演化为赖账纠纷，许多数十年的挚友情谊在巨额借款前彻底碎裂瓦解。",
            "narrative": "大学同窗四年的挚友痛哭流涕登门，称其炒股穿仓急需五万元周转过桥，保证三个月连本带利归还。你心一软拿出自己准备买房首付的五万元积蓄借给了他。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "三年到期后多次好言催讨，对方百般推诿拉黑电话，聘请律师持借条起诉申请法院强制执行",
                    "choiceTags": ["时代：2000–2015", "年龄：24–50", "地域：全国城市", "门槛：依法维权撕破脸皮者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 60,
                            "log": "法院查封其名下车辆拍卖追回大部分欠款，虽然收回了四万余元血汗钱，但二十年挚友情谊彻底灰飞烟灭。",
                            "effect": {"wealth": 20, "mentality": -15, "family": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "依法强执追回大部分借款，买断虚伪友谊。"
                        },
                        {
                            "type": "entangled",
                            "weight": 40,
                            "log": "对方名下无可供执行财产被列入老赖失信名单，五万元彻底化为死账，深感人性险恶。",
                            "effect": {"wealth": -40, "mentality": -35},
                            "isFatal": False,
                            "hiddenRiskLog": "轻信熟人借贷遭遇老赖死账，巨额财产化为泡影。",
                            "status": "status_debt_burdened"
                        }
                    ]
                },
                {
                    "text": "顾及昔日兄弟情面不忍对簿公堂，就此自认倒霉打碎牙往肚里咽，不再向其讨要",
                    "choiceTags": ["时代：2000–2015", "年龄：24–50", "地域：全国城市", "门槛：软弱好面子者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "钱打了水漂换来伴侣无尽的埋怨与争吵，五万元成为心头拔不掉的一根刺，发誓此生再也不借一分钱给外人。",
                            "effect": {"wealth": -35, "mentality": -25, "family": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "纵容老赖借贷流失巨资，痛定思痛筑牢财务防火墙。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2000_2015_d4_wenchuan_zhiyuan",
            "tier": "era",
            "title": "大爱无疆：汶川震后结对长期资助失亲孤儿",
            "yearRange": [2008, 2015],
            "targetAge": [24, 60],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "2008年5·12汶川特大地震发生后，全国涌现数百万志愿者与结对家庭，民间通过红十字会与妇联长期定向资助灾区失亲孤儿完成学业直至大学毕业。",
            "narrative": "电视画面里都江堰与映秀废墟触目惊心。妇联发起‘汶川地震失亲孤儿一对一定点助学’倡议，每月只需寄出三百元生活费，即可保障一名灾区孩子念完初高中。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "郑重在妇联助学协议上签字，承诺连续十年每月按期汇出三百元，并经常通信鼓励孩子自强",
                    "choiceTags": ["时代：2008–2015", "年龄：24–60", "地域：全国各地", "门槛：仁爱担当奉献者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "十年长流水般的爱心呵护，被资助的孩子顺利考上重点大学医学院，专程登门送上锦旗深情唤你‘第二父母’！",
                            "effect": {"mentality": 40, "family": 30, "wealth": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "十年坚守汶川孤儿助学铸就崇高道德楷模，收获终身跨血缘深情。",
                            "status": "status_family_protector"
                        },
                        {
                            "type": "entangled",
                            "weight": 5,
                            "log": "个别月份手头吃紧依然省吃俭用如期汇款，虽微有压力但问心无愧。",
                            "effect": {"wealth": -10, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "恪守爱心承诺无怨无悔。"
                        }
                    ]
                },
                {
                    "text": "只在单位组织的一次性捐款箱里投下一百元，觉得自己过好小日子才是最重要的",
                    "choiceTags": ["时代：2008–2015", "年龄：24–60", "地域：全国各地", "门槛：普通随大流者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "尽了一份普通公民的本分随大流捐助，生活继续波澜不惊如常前行。",
                            "effect": {"wealth": -5, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "随份子献爱心平稳安全过好小家生活。"
                        }
                    ]
                }
            ]
        }
    ]
