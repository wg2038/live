# -*- coding: utf-8 -*-
"""
2016–2026 移动互联、转型与当代：四大机制事件批次 (16条)
A. 路径补救 (百万高职扩招免试大专、中年失业自媒体转行、考取植保无人机飞手、应聘社区微网格员)
B. 渐进伤害 (通宵刷短视频频发室早、网购三无微商减肥药、雨夜外卖急刹滑倒挫伤、重度焦虑迷信神婆)
C. 经济诱惑 (P2P网贷理财连环爆雷、年轻人分期乐以贷养贷、区块链数字藏品传销、MCN高额网红培训费)
D. 亲友离别 (疫情跨省阻断视频连线云送终、独生子女意外重创失独之痛、老宅未公证遗产继承风波、翻看父母生前缝补账本)
"""

def get_events():
    return [
        # --- A. 路径补救 ---
        {
            "id": "evt_2016_2026_a1_gaozhi_kuozhao",
            "tier": "era",
            "title": "政策红利：搭乘百万高职扩招快车重返大学",
            "yearRange": [2019, 2023],
            "targetAge": [22, 45],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "2019年政府工作报告提出高职院校大规模扩招100万人，面向退役军人、下岗失业人员、农民工和新型职业农民，实行免文化素质考试、弹性学制入读全日制大专。",
            "narrative": "早年高中毕业一直在电子厂做普工。县人社局群里发来‘百万高职扩招专项行动’通知，免文化课考试，弹性上课三年，顺利毕业即可获得全日制统招普通大专学历。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "果断提交退役/农民工证明报名新能源汽车维修技术专业，半工半读苦学三年",
                    "choiceTags": ["时代：2016–2026", "年龄：22–45", "地域：全国城乡", "门槛：无全日制大专文凭者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "顺利通过毕业实操答辩领到教育部电子注册的全日制大专毕业证，被新能源头部车企直聘为售后技术专家！",
                            "effect": {"wealth": 35, "mentality": 30, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "抓住高职扩招国家级红利摘掉低学历帽子，切入新能源朝阳产业。",
                            "status": "status_college_diploma"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "工学兼顾连轴转经常熬夜赶写作业引起胃炎，但坚持拿到文凭，前途豁然开朗。",
                            "effect": {"health": -10, "wealth": 20, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "工学矛盾略耗心力无后遗症。"
                        }
                    ]
                },
                {
                    "text": "觉得大专文凭早已烂大街不值钱，懒得花时间折腾，下班继续躺平打游戏",
                    "choiceTags": ["时代：2016–2026", "年龄：22–45", "地域：全国城乡", "门槛：消极躺平者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "避开了读书之苦，但不久电子厂流水线大面积推行机械臂自动化替换，无技术工人首批被优化淘汰。",
                            "effect": {"wealth": -10, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "放弃政策扩招提升机遇，遭遇制造业自动化替代危机。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_a2_zimeiti_zhuanxing",
            "tier": "era",
            "title": "中年自救：遭遇裁员转行三农短视频直播带货",
            "yearRange": [2018, 2026],
            "targetAge": [32, 52],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "随着短视频与快手、抖音直播电商普及，大批遭遇城市‘35岁职场危机’的中年人返乡创业，利用乡村原生态风貌开辟‘三农自媒体’带货农产品实现自救。",
            "narrative": "年过三十五岁遭遇公司降本增效裁员，投出上百份简历全部已读不回。回到县城老家，看到满山熟透滞销的蜜橘，你拿起智能手机支架，决定放手一搏短视频。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "自学视频剪辑与脚本，每天清晨五点上山下地实景直播，以真诚质朴风格推销家乡土特产",
                    "choiceTags": ["时代：2016–2026", "年龄：32–52", "地域：县域乡村", "门槛：敢于出镜自强者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "一条记录母亲柴火灶炖笋的视频全网爆火获赞百万！不仅帮全村卖光了滞销橘子，更建立自有助农电商品牌！",
                            "effect": {"wealth": 45, "mentality": 35, "family": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "在移动互联网流量新生态中二次创业崛起，实现财务与个人价值飞跃。",
                            "status": "status_self_employed"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "户外直播突遇暴雨感冒高烧失声，吃金嗓子含片调整后恢复，收获第一批忠实粉丝。",
                            "effect": {"health": -10, "wealth": 20, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "创业初期吃苦耐劳打下基础。"
                        }
                    ]
                },
                {
                    "text": "觉得在镜头前抛头露面丢不起那个人，拒绝转型，靠开网约车和吃微薄老本度日",
                    "choiceTags": ["时代：2016–2026", "年龄：32–52", "地域：县域乡村", "门槛：思想保守者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "每天跑车十二小时仅够勉强糊口，随着平台派单运价下降，收入逐月走低身心俱疲。",
                            "effect": {"wealth": 5, "mentality": -15, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "守旧不敢突破，深陷零工低薪内卷泥潭。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_a3_wurenji_feishou",
            "tier": "era",
            "title": "智慧农业：自费考取农用植保无人机飞手执照",
            "yearRange": [2017, 2026],
            "targetAge": [19, 45],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "大疆等农业植保无人机在全国农田飞速普及，取代传统人工背药喷洒，‘职业飞手’日作业面积达数百亩，收入可观且避免了农药中毒风险。",
            "narrative": "村里年轻人纷纷进城打工，农田面临无人种地荒芜。农业合作社引进大型八轴植保无人机，你看到招募飞手培训班公告，学费三千元包拿CAAC无人机驾驶员执照。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "拿出压岁钱报名无人机飞手培训，在模拟器与外场苦练航线规划与避障喷洒技能",
                    "choiceTags": ["时代：2016–2026", "年龄：19–45", "地域：现代农田", "门槛：对智能科技感兴趣青年"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "高分拿下无人机驾驶证！一人操纵两架无人机跨省接单喷药，一个作业季净赚八万多元，成为现代农业明星！",
                            "effect": {"wealth": 40, "mentality": 30, "health": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "掌握现代无人机精准农事技能，从传统老农跃升为高薪农业工程师。",
                            "status": "status_skilled_welder"
                        },
                        {
                            "type": "injured",
                            "weight": 10,
                            "log": "外场试飞时螺旋桨气流掀起沙尘眯伤右眼角膜，冲洗点抗生素眼药膏三天痊愈。",
                            "effect": {"health": -5, "wealth": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "训练轻微眼部擦伤无碍执飞。"
                        }
                    ]
                },
                {
                    "text": "认为几万块钱的无人机摔了赔不起，宁愿继续人工背负电动喷雾器打药",
                    "choiceTags": ["时代：2016–2026", "年龄：19–45", "地域：现代农田", "门槛：因循传统者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "烈日下依然要赤膊吸农药，效率低下收入微薄，眼睁睁看着农田服务订单全被外地飞手抢走。",
                            "effect": {"health": -10, "wealth": 5, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "抗拒智能化农机，在农业现代化转型中被边陲化。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_a4_shequ_wangge",
            "tier": "era",
            "title": "基层兜底：应聘街道社区专职网格员获社保托底",
            "yearRange": [2018, 2026],
            "targetAge": [28, 55],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "城市网格化精细治理与疫情防控期间，全国各街道大量招募社区专职网格员，提供五险一金和稳定财政托底，成为吸纳大龄就业困难群体的政策安全网。",
            "narrative": "原私企倒闭后断缴社保近两年，上有四位老人下有在读子女。街道党群服务中心贴出招聘微网格员启事，月薪三千五百元缴纳正规五险一金，负责两百户日常巡查。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "认真准备笔试面试顺利通过政审，穿上红马甲走楼入户做走访登记，扎根基层服务",
                    "choiceTags": ["时代：2016–2026", "年龄：28–55", "地域：城市社区", "门槛：热心社区事务者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "五险一金重新续接无断缴之虞！靠细心与热忱帮独居孤寡老人解决多桩急难，获评年度‘优秀金牌网格员’转聘专职副书记。",
                            "effect": {"family": 25, "wealth": 20, "mentality": 25, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "通过社区微网格员实现社保与职业再托底，建立稳定职业归宿。",
                            "status": "status_white_collar"
                        },
                        {
                            "type": "injured",
                            "weight": 10,
                            "log": "爬楼梯过多致轻度膝盖滑膜炎，贴膏药配合慢走缓解，工作平稳有条不紊。",
                            "effect": {"health": -10, "wealth": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "社区爬楼巡查引发轻微膝关节劳损。"
                        }
                    ]
                },
                {
                    "text": "嫌弃网格员成天处理邻里狗皮膏药琐事太繁琐，拒绝应聘，继续赋闲在家啃老",
                    "choiceTags": ["时代：2016–2026", "年龄：28–55", "地域：城市社区", "门槛：眼高手低者"],
                    "outcomes": [
                        {
                            "type": "redirected",
                            "weight": 100,
                            "log": "社保长期断缴面临未来养老医保无法办结的危机，家庭日常开销捉襟见肘，家庭矛盾日趋白热化。",
                            "effect": {"wealth": -15, "family": -20, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "放弃基层兜底就业，社保断缴陷入中年财务泥淖。"
                        }
                    ]
                }
            ]
        },

        # --- B. 渐进伤害与可错选项 ---
        {
            "id": "evt_2016_2026_b1_aoye_zaobo",
            "tier": "era",
            "title": "数字成瘾：深宵刷短视频频发室性早搏胸闷",
            "yearRange": [2018, 2026],
            "targetAge": [16, 45],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "智能手机算法无限信息流推送导致当代青年重度熬夜普遍化，长期交感神经处于过度亢奋状态，导致功能性乃至器质性室性早搏、心悸高发。",
            "narrative": "连续几个月每夜熄灯后侧卧刷短视频至凌晨三点，蓝光刺眼。今天午睡醒来心口突然猛烈‘咯噔’漏跳一拍，紧接着心慌发紧、四肢发凉、呼吸不畅频发心慌。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "以为只是白天咖啡喝多了，自作主张网购稳心颗粒自服，戴上降噪耳机继续熬夜追剧硬挺",
                    "choiceTags": ["时代：2016–2026", "年龄：16–45", "地域：全国城乡", "门槛：自作聪明乱用药者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 75,
                            "log": "频发室性早搏发展为短阵室性心动过速，在地铁站突发黑朦晕厥倒地磕破额头，急诊动态心电图显示单日早搏高达两万次！",
                            "effect": {"health": -40, "wealth": -20, "mentality": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "漠视严重心律失常继续熬夜，导致心脏电生理功能重度紊乱。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "fatal",
                            "weight": 2,
                            "log": "熬夜极度疲劳诱发恶性恶性心律失常室颤，深夜在被窝中心源性猝死。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "重度熬夜数字成瘾突发恶性心律失常猝死。"
                        },
                        {
                            "type": "safe",
                            "weight": 23,
                            "log": "受惊后强制放下手机早睡三天，早搏大幅减少自行恢复，彻底吓戒了熬夜恶习。",
                            "effect": {"health": 5, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "及时受惊止损保全心脏。"
                        }
                    ]
                },
                {
                    "text": "立即卸载短视频软件，前往三甲医院心内科做24小时动态心电图与心脏彩超，遵医嘱按时作息",
                    "choiceTags": ["时代：2016–2026", "年龄：16–45", "地域：全国城乡", "门槛：具备数字健康自律者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "查明为交感神经兴奋性功能性早搏，无器质性病变。通过规律作息与有氧慢跑，早搏完全归零自愈！",
                            "effect": {"health": 15, "wealth": -5, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "科学纠正作息成功化解心律失常危机，养成终身健康作息习惯。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "偶尔劳累后仍有极个别偶发早搏，无须服药定期复查即可。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "轻微偶发早搏完全受控。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_b2_jianfei_shixin",
            "tier": "era",
            "title": "微商乱象：网购三无微商减肥胶囊心慌手抖",
            "yearRange": [2016, 2024],
            "targetAge": [16, 40],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "朋友圈微商兜售的所谓‘纯天然酵素/燃脂胶囊’常非法添加国家明令禁用的西布曲明、酚酞或甲状腺素，导致服用者出现严重厌食、精神狂躁与肺动脉高压。",
            "narrative": "为在婚礼前快速减重十斤，花八百元网购了微商极力推荐的‘进口果蔬纯天然燃脂素’。连服三天体重骤降，但伴随口干舌燥如吞火炭、双手剧烈颤抖、瞳孔放大失眠。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "看到体重秤数字下降欣喜若狂，以为燃脂就是这样，继续加大剂量连吃半个月",
                    "choiceTags": ["时代：2016–2026", "年龄：16–40", "地域：全国城乡", "门槛：盲目容貌焦虑急功近利者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 76,
                            "log": "违禁西布曲明导致重度药物性躁狂症与不可逆肺动脉高压，晕倒送医洗胃抢救，留下轻微活动即气喘后遗症！",
                            "effect": {"health": -45, "wealth": -25, "mentality": -30},
                            "isFatal": False,
                            "hiddenRiskLog": "滥用含非法违禁添加物减肥药致心肺不可逆毒性损伤。",
                            "status": "sequelae_respiratory"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "严重药物过量引发恶性高热与急性心跳骤停不幸香消玉殒。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "违禁减肥药严重中毒致心搏骤停罹难。"
                        },
                        {
                            "type": "safe",
                            "weight": 21,
                            "log": "停药后大量喝水排毒，虽反弹了五斤但年轻身体代谢完毕，心悸慢慢平息。",
                            "effect": {"health": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "侥幸排毒脱险，彻底戒除有害减肥药。"
                        }
                    ]
                },
                {
                    "text": "果断将剩余药丸送食药监部门检测，停止服用并前往综合医院做尿检与电解质监测",
                    "choiceTags": ["时代：2016–2026", "年龄：16–40", "地域：全国城乡", "门槛：具备食品安全防范意识者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "化验检出超标西布曲明由经侦依法立案，你及时大量补液排毒，两日内心跳恢复窦性律，未留脏器损伤！",
                            "effect": {"health": 5, "wealth": -5, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "机警识破三无有毒违禁药果断止损，协助警方捣毁制假窝点。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "肠胃轻度受损腹泻两天，喝小米粥逐步调养自愈。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "轻度胃肠不适迅速平复。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_b3_qishou_diandao",
            "tier": "era",
            "title": "骑手抢时：暴雨天赶送外卖急刹打滑挫裂伤",
            "yearRange": [2018, 2026],
            "targetAge": [18, 48],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "外卖平台严格的‘超时扣款’算法机制驱使数百万骑手在恶劣天气下涉险疾驰，雨雪天电动车道路打滑侧翻跌打挫伤频发，普遍存在带伤送单现象。",
            "narrative": "暴雨滂沱视线模糊，手机系统倒计时只剩八分钟，超时将面临客户差评与重金扣罚。转弯过斑马线时电动车突然侧滑甩飞，重重砸在路牙石上，膝盖血肉模糊剧痛难忍。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "用矿泉水胡乱冲洗伤口贴上创口贴，咬紧牙关扶起电动车一瘸一拐继续冒雨把这单外卖送到客人手中",
                    "choiceTags": ["时代：2016–2026", "年龄：18–48", "地域：全国城市", "门槛：为免差评拼命硬挺者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 78,
                            "log": "泥沙深部感染引发化脓性滑膜炎与半月板三度撕裂，因延误处理导致膝关节僵直积液，不得不卧床两个月并动了关节镜手术！",
                            "effect": {"health": -35, "wealth": -20, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "车祸创伤带泥硬挺导致关节严重化脓与半月板损伤。",
                            "status": "sequelae_motor_impairment"
                        },
                        {
                            "type": "safe",
                            "weight": 22,
                            "log": "送达后客人看到浑身是血的骑手感动不已，当场取消差评并打赏两百元医药费，包扎后未伤及骨头。",
                            "effect": {"wealth": 15, "mentality": 15, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "拼命精神打动客户，皮外伤未伤筋动骨。"
                        }
                    ]
                },
                {
                    "text": "立刻向平台报备交通事故上传照片申请异常订单免责，打车直奔附近公立医院骨科拍片缝合清创",
                    "choiceTags": ["时代：2016–2026", "年龄：18–48", "地域：全国城市", "门槛：生命安全优先者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "急诊彻底清除伤口砂石缝合五针，骑手专享意外险全额报销了治疗费，休息一周平稳拆线，膝盖完好无损。",
                            "effect": {"health": 5, "wealth": 0, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "正规清创缝合激活保险理赔，妥善保全肢体运动能力。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "膝盖留下两寸白色线状疤痕，阴天稍有紧绷，无碍骑车跑单。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "微小线状瘢痕无功能受限。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_b4_jiaolv_shenpo",
            "tier": "era",
            "title": "迷途心魔：重度抑郁焦虑轻信神婆驱邪延误治疗",
            "yearRange": [2017, 2026],
            "targetAge": [18, 55],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "当代生活节奏加快与内卷压力下，抑郁症、焦虑症等心理精神疾病发病率上升，部分基层患者因病耻感拒绝正规心理科，转求民间神婆画符招魂延误病情。",
            "narrative": "长期失眠胸闷惊恐发作，脑子里总是冒出绝望轻生念头，甚至连床都起不来。亲戚悄悄拉住你，称城郊有个老神婆‘通灵查虚病’极灵，花八千元烧符斩煞包好。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "瞒着家人掏出八千元私房钱去神婆堂口烧符纸喝香灰水，寄希望于玄学驱散心魔",
                    "choiceTags": ["时代：2016–2026", "年龄：18–55", "地域：全国城乡", "门槛：因病耻感盲求封建玄学"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 78,
                            "log": "延误正规神经递质抗抑郁治疗导致重度精神崩溃出现自残冲动，重度铅汞香灰水更损害肠胃，最终被家人送精神卫生中心强制封闭治疗！",
                            "effect": {"health": -45, "wealth": -35, "mentality": -35},
                            "isFatal": False,
                            "hiddenRiskLog": "迷信偏方香灰驱邪延误重度抑郁治疗，导致严重心理危机。",
                            "status": "sequelae_mental_trauma"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "在极度幻灭自责中突发冲动轻生意外离世，酿成家庭永久悲剧。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "重度心理危机延误现代医学干预不幸轻生。"
                        },
                        {
                            "type": "safe",
                            "weight": 19,
                            "log": "在堂口受惊反而清醒意识到封建迷信的荒谬，毅然逃离窝点自救。",
                            "effect": {"mentality": 10, "wealth": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "玄学闹剧警醒自拔。"
                        }
                    ]
                },
                {
                    "text": "破除心理病耻感，在好友陪同下前往正规三甲医院临床心理科做专业量表评估，按医嘱规范服用SSRIs药物配合认知行为疗法",
                    "choiceTags": ["时代：2016–2026", "年龄：18–55", "地域：全国城乡", "门槛：具备现代精神卫生科学认知"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 92,
                            "log": "服药两周后五羟色胺递质逐步平衡，胸闷失眠完全消除，重新体会到了阳光鸟鸣的美好，彻底重获新生！",
                            "effect": {"mentality": 40, "health": 15, "wealth": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "正规现代医学治疗驱散抑郁阴霾，彻底重拾身心掌控权。"
                        },
                        {
                            "type": "injured",
                            "weight": 8,
                            "log": "早期有轻微嗜睡胃部不适，一周后耐受，完全不影响正常工作学习。",
                            "effect": {"health": 5, "wealth": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "规范服药轻微初期副反应平稳度过。"
                        }
                    ]
                }
            ]
        },

        # --- C. 经济系统与诱惑 ---
        {
            "id": "evt_2016_2026_c1_p2p_baolei",
            "tier": "era",
            "title": "爆雷风暴：P2P互联网金融理财平台清盘跑路",
            "yearRange": [2016, 2020],
            "targetAge": [22, 65],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 6,
            "factLevel": "确证",
            "historicalFact": "2018年前后全国P2P网贷平台迎来史上最大爆雷潮，团贷网、爱投资等数千家宣称‘8%-12%保本保息、银行存管’的平台被公安经侦按非法吸收公众存款罪立案查处。",
            "narrative": "地铁、电梯广告铺天盖地都是知名明星代言的P2P理财APP，宣称上市公司背景、保本保息年化10%。你账上正躺着全家辛苦攒下的二十万元存折，同事都在晒每天到账的利息。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "把二十万全额充值买入该平台一年期定期标的，期盼一年净收两万利息换辆代步车",
                    "choiceTags": ["时代：2016–2020", "年龄：22–65", "地域：全国城市", "门槛：贪图互联网高息者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 85,
                            "log": "不到半年APP突然无法提现发出清盘公告，实际控制人携款外逃被警方通缉！全家二十万积蓄化为泡影，漫漫维权路心力交瘁。",
                            "effect": {"wealth": -60, "mentality": -40, "family": -30},
                            "isFatal": False,
                            "hiddenRiskLog": "陷入P2P互联网金融非法集资爆雷，家庭流动性资产瞬间蒸发。",
                            "status": "status_asset_wiped"
                        },
                        {
                            "type": "safe",
                            "weight": 15,
                            "log": "在爆雷前夕听到风吹草动提前提前一个月申请债转折价提现成功，侥幸保全本金并赚了千元利息逃出生天！",
                            "effect": {"wealth": 20, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "在网贷大崩盘前夕极限操作套现逃顶。"
                        }
                    ]
                },
                {
                    "text": "牢记银保监会‘收益率超过8%就很危险、超过10%就要准备损失全部本金’的警示，坚决不碰存入国有银行大额存单",
                    "choiceTags": ["时代：2016–2020", "年龄：22–65", "地域：全国城市", "门槛：遵循监管红线理智客"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "数月后该平台雷声震天无数受害者痛哭，你全家二十万存款在工行存单里安然无恙，本息安全如泰山！",
                            "effect": {"mentality": 30, "wealth": 15, "family": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "敬畏金融规律坚守本金底线，守护全家多年财富成果。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_c2_wangdai_fenqi",
            "tier": "era",
            "title": "消费深渊：分期乐与网贷连环套以贷养贷",
            "yearRange": [2016, 2024],
            "targetAge": [18, 30],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 6,
            "factLevel": "确证",
            "historicalFact": "移动互联网消费贷大肆渗透年轻人，‘0首付买最新款iPhone/潮牌’引导超前消费，拆东墙补西墙以贷养贷，年化实际利率往往通过服务费掩盖超过36%。",
            "narrative": "最新款折叠屏手机发布售价一万三，周围同学朋友都在用。你月工资只有三千五，分期平台弹窗提示‘日供只要十八元’，只需身份证一键人脸识别即可秒下款。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "忍不住虚荣心网贷分期拿下手机，随后又分期购买轻奢鞋包，靠在不同平台借新还旧",
                    "choiceTags": ["时代：2016–2026", "年龄：18–30", "地域：全国城市", "门槛：虚荣超前消费者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 85,
                            "log": "短短一年滚成八家网贷平台逾期三十余万！通讯录被催收爆破轰炸，父母变卖养老金替你填补窟窿，征信黑名单寸步难行！",
                            "effect": {"wealth": -50, "family": -40, "mentality": -35},
                            "isFatal": False,
                            "hiddenRiskLog": "陷入消费贷多头借贷债务雪球，信用彻底破产连累父母。",
                            "status": "status_debt_burdened"
                        },
                        {
                            "type": "safe",
                            "weight": 15,
                            "log": "咬牙做三份兼职送外卖在利滚利前彻底还清本金，剪碎所有信用卡发誓再不超前消费。",
                            "effect": {"wealth": -10, "mentality": 20, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "经历债务惊魂靠勤劳苦干上岸自救。"
                        }
                    ]
                },
                {
                    "text": "关闭所有消费分期额度，坚持‘赚多少花多少’原则，用二手旧手机安心过日子",
                    "choiceTags": ["时代：2016–2026", "年龄：18–30", "地域：全国城市", "门槛：量入为出极简者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "无债一身轻，每个月还能存下一千元应急金，征信报告干干净净，精神状态无比自由从容。",
                            "effect": {"wealth": 15, "mentality": 25, "family": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "彻底杜绝消费贷陷阱，牢牢把握个人财务自主权。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_c3_xuni_chuanxiao",
            "tier": "era",
            "title": "科技画皮：所谓元宇宙区块链数字藏品炒作",
            "yearRange": [2021, 2024],
            "targetAge": [20, 50],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 6,
            "factLevel": "确证",
            "historicalFact": "2021-2023年元宇宙概念火爆，国内涌现数百个无版权依托的‘数藏平台’，以击鼓传花二级市场炒作几十倍虚高价格，最终平台拔线关停涉嫌非法集资与传销。",
            "narrative": "微信群里疯狂转发某‘元宇宙数藏平台’的一张像素头像，号称限量发行、三天翻了五倍。群主信誓旦旦称这是未来虚拟房产门票，只要充值两万元入场拉两个下线就能分红十万。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "抱着投机暴富心态拿出两万元抢购数藏头像，并在朋友圈拼命拉亲戚朋友注册接盘",
                    "choiceTags": ["时代：2016–2026", "年龄：20–50", "地域：全国城市", "门槛：沉迷虚拟投机者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 80,
                            "log": "一周后平台服务器直接关停拔网线，负责人失联被公安经侦按传销立案查封！两万元血本无归更被亲友痛骂孤立！",
                            "effect": {"wealth": -35, "mentality": -30, "family": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "参与虚拟币数藏传销资金盘遭割韭菜，人财两空声名扫地。",
                            "status": "status_asset_wiped"
                        },
                        {
                            "type": "safe",
                            "weight": 20,
                            "log": "次日趁着狂热以两倍价格火速转手给新韭菜套现四万元提现离场，惊险落袋为安！",
                            "effect": {"wealth": 35, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "在庞氏骗局击鼓传花中侥幸收割离场。"
                        }
                    ]
                },
                {
                    "text": "一眼识破这是穿了新马甲的庞氏资金盘骗局，直接退群并向微信安全中心举报涉诈",
                    "choiceTags": ["时代：2016–2026", "年龄：20–50", "地域：全国城市", "门槛：清醒防诈卫士"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "不贪图泡沫横财，守紧钱袋子，目睹群里受骗者哭天抢地维权，庆幸自己保持了常识与定力。",
                            "effect": {"mentality": 20, "wealth": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "常识破除虚妄概念，远离新型互联网资金盘洗劫。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_c4_gaojia_kengweifei",
            "tier": "era",
            "title": "流量诱饵：被MCN虚假签约套路三万培训费",
            "yearRange": [2019, 2026],
            "targetAge": [18, 35],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "随着网红经济野蛮生长，部分劣质MCN机构以‘包装百万粉丝达人、包商单保底’为名签约年轻求职者，实则诱导其贷款购买高价化妆、形体与直播培训课，深陷合同陷阱。",
            "narrative": "应聘网红主播，面试官赞叹你形象气质极佳有‘爆火潜质’，承诺签约后分配百万级流量。但前提必须交纳三万元‘达人孵化包装培训与形象定制费’，可分期付款。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "沉浸在成为头部大主播的幻想中，爽快刷信用卡交纳三万元培训费签约",
                    "choiceTags": ["时代：2016–2026", "年龄：18–35", "地域：全国城市", "门槛：盲从网红明星梦者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 85,
                            "log": "签约后所谓培训只是几段网上下载的公开视频，直播间只有个位数机器人流量，解约反被索赔百万元违约金，深陷法庭纠纷！",
                            "effect": {"wealth": -40, "mentality": -35, "family": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "陷入黑心MCN套路贷合同霸王条款，背负巨债心力交瘁。",
                            "status": "status_debt_burdened"
                        },
                        {
                            "type": "safe",
                            "weight": 15,
                            "log": "自身表现力超群在深夜连麦中出圈，单飞打赢解约官司，成为真正自立的中腰部主播。",
                            "effect": {"wealth": 35, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "靠个人独特才华打破MCN霸王合同脱颖而出。"
                        }
                    ]
                },
                {
                    "text": "深知正规用人单位绝不收取培训费，当场索要正规合同并严词拒绝交钱，转身离开",
                    "choiceTags": ["时代：2016–2026", "年龄：18–35", "地域：全国城市", "门槛：洞悉职场骗局者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "避开套路陷阱，老老实实找了一家正规电商公司做运营助理，踏实积累数字营销真本事。",
                            "effect": {"wealth": 15, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "拒绝空头包装诱惑，选择脚踏实地职场成长。"
                        }
                    ]
                }
            ]
        },

        # --- D. 亲友关系网与离别 ---
        {
            "id": "evt_2016_2026_d1_yuntang_gaobie",
            "tier": "era",
            "title": "跨省阻隔：疫情封控跨省阻断视频连线云端送终",
            "yearRange": [2020, 2022],
            "targetAge": [22, 65],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_orphan"],
            "triggerProbability": 0.08,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "2020-2022年严格常态化疫情防控期间，受跨省列车停运、健康码弹窗及封闭隔离政策制约，大量在外游子未能见上病故长辈最后一面，依靠手机视频含泪云端告别。",
            "narrative": "老家老母亲/祖父重症病危弥留，而你所在城市正值全域静默管理，高铁停运。护士在病床前拨通微信视频，屏幕那头老人双目微睁，呼吸面罩上布满白雾。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "跪在出租屋冰冷地板上，隔着手机屏幕撕心裂肺向老人磕头道别，把所有的思念与祈愿字字说完",
                    "choiceTags": ["时代：2020–2022", "年龄：22–65", "地域：封控停运城市", "门槛：深情隐忍顾大局者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "老人微弱地点了点头安详合上双眼。虽然无法亲身送葬留下终身憾恨，但屏幕这头的跪拜尽了最后的深情与孝道。",
                            "effect": {"mentality": 15, "family": 30, "wealth": 0},
                            "isFatal": False,
                            "hiddenRiskLog": "在疫情至暗特殊年代云端跪别至亲，克制守望烙下一代特殊历史记忆。",
                            "status": "status_bereaved_parent"
                        },
                        {
                            "type": "injured",
                            "weight": 10,
                            "log": "悲痛欲绝哀恸过度诱发神经性胃痉挛大汗淋漓，独吞感伤与思念慢慢愈合。",
                            "effect": {"health": -20, "mentality": -10, "family": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "云端送终哀伤过度伤及身心。"
                        }
                    ]
                },
                {
                    "text": "冒着黄码拘留风险违规私自搭乘黑车强行翻越省界关卡，誓要冲回老家灵堂",
                    "choiceTags": ["时代：2020–2022", "年龄：22–65", "地域：封控停运城市", "门槛：不顾后果冲动者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 100,
                            "log": "在高速收费站被防疫卡点当场拦截并赋红码，不仅未能赶回老家送终，更被送入隔离点自费集中隔离十四天并处行政训诫！",
                            "effect": {"wealth": -20, "mentality": -40, "family": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "冲卡违规被截强隔，人财两失抱憾终身。",
                            "status": "status_bereaved_parent"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_d2_laonian_shidu",
            "tier": "era",
            "title": "折翼之殇：独生子女意外罹难老年失独抱团自救",
            "yearRange": [2016, 2026],
            "targetAge": [50, 75],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_lost_child"],
            "triggerProbability": 0.07,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "第一代独生子女父母步入老年后，部分家庭面临独生子女因车祸、疾病意外早逝的‘失独’困境。民间失独群体与社区互助会通过抱团取暖、心理救助艰难重建生活信心。",
            "narrative": "唯一的孩子在车祸中不幸早逝。客厅墙上挂着孩子名校毕业的微笑合影，房间纤尘不染，两张白发苍苍的面孔坐在空旷的餐桌前，天地寂静得让人窒息。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "夫妻相互搀扶走出家门，参加社区失独老人爱心互助会，把余生精力投入社区公益与流浪动物救助中",
                    "choiceTags": ["时代：2016–2026", "年龄：50–75", "地域：全国城乡", "门槛：大悲大痛自强走出者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "在帮助他人的善意中逐步疗愈心头剧痛，相濡以沫结识了同样遭遇的患难老友，重新找到了生命的尊严与微光。",
                            "effect": {"mentality": 30, "family": 35, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "走出失独至暗深渊投身社会公益，在互助中重建余生尊严。",
                            "status": "status_lost_child"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "每逢清明春节仍难免睹物思人暗自垂泪，但彼此手牵手坚定度过晚年。",
                            "effect": {"mentality": 10, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "心伤难全但相濡以沫安享晚年。"
                        }
                    ]
                },
                {
                    "text": "终日以泪洗面拉上全部窗帘闭门谢客，拒绝一切外界关怀，深陷无尽的自责与怨尤",
                    "choiceTags": ["时代：2016–2026", "年龄：50–75", "地域：全国城乡", "门槛：自我封闭者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 100,
                            "log": "长年封闭导致双双罹患严重老年抑郁症与心血管急症，身体机能断崖式衰退，晚境凄凉令人唏嘘。",
                            "effect": {"health": -40, "mentality": -40, "family": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "失独后自我封闭导致身心健康严重崩解衰朽。",
                            "status": "status_lost_child"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_d3_zhengchan_taoyuan",
            "tier": "era",
            "title": "遗嘱缺失：高龄父母离世手足亲戚争抢房产",
            "yearRange": [2017, 2026],
            "targetAge": [35, 68],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "城市高房价背景下，老人猝然离世未立公证遗嘱，按照民法典法定继承顺序转继承、代位继承牵扯七大姑八大姨数十人签字，公证继承纠纷屡见不鲜。",
            "narrative": "父母相继安详病故，留下一套价值三百万的市区老商品房。由于生前未立公证遗嘱，常年不露面的外地堂兄妹与再婚子女纷纷登门，要求按法定继承均分房产份额。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "聘请专业继承法律师，拿出多年床前尽孝垫付医药费的完整银行流水单据，要求多分份额并依法分割",
                    "choiceTags": ["时代：2016–2026", "年龄：35–68", "地域：城市商品房小区", "门槛：依法维权讲究法理者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "法院采信尽孝主要责任认定判决你继承75%核心份额并折价补偿他人，顺利过户取得红本，守卫了父母心血。",
                            "effect": {"wealth": 45, "family": -25, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "以完整尽孝证据赢得法定继承诉讼，依法捍卫家庭核心资产。"
                        },
                        {
                            "type": "entangled",
                            "weight": 15,
                            "log": "官司在亲戚群里闹得沸沸扬扬两败俱伤，虽拿到大部分房款但断绝了远房宗亲往来。",
                            "effect": {"wealth": 30, "family": -35, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "房产诉讼彻底斩断亲戚网络。"
                        }
                    ]
                },
                {
                    "text": "主动组织家庭调解会议，念在同胞血脉各退一步，折中折价各分一部分，签署人民调解协议息诉罢争",
                    "choiceTags": ["时代：2016–2026", "年龄：35–68", "地域：城市商品房小区", "门槛：以和为贵讲人情者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "各方握手言和在不动产中心完成平稳交割，虽然财产稍有让步，但避免了反目成仇的狗血闹剧，父母九泉之下亦得瞑目。",
                            "effect": {"wealth": 25, "family": 30, "mentality": 30},
                            "isFatal": False,
                            "hiddenRiskLog": "以胸怀大度化解遗产继承死结，保全宗族最后体面与情分。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_2016_2026_d4_yilai_yiyuan",
            "tier": "era",
            "title": "遗物静默：清理已故父母旧居翻出泛黄记账本",
            "yearRange": [2016, 2026],
            "targetAge": [28, 70],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_orphan"],
            "triggerProbability": 0.08,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "在当代清理已故老一辈居所时，翻检出的红木樟木箱、搪瓷茶缸、存折、泛黄的手写记账本，往往真实记录着一个普通中国家庭半个世纪以来的温饱奋斗史。",
            "narrative": "整理已故老父亲生前的红木五斗橱，在一个生锈的铁皮月饼盒深处，翻出一本用棉线装订的泛黄记账本。上面用工整小楷记录着：某年某月买自行车欠三十元、某年为你缴大学学费...",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "坐在空荡寂静的旧木椅上把记账本从头到尾读完，抚摸着字迹泪流满面，随后将其塑封珍藏进保险箱代代相传",
                    "choiceTags": ["时代：2016–2026", "年龄：28–70", "地域：全国各地", "门槛：至纯念旧至孝者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "父辈清贫而坚韧的一生如电影般在眼前闪过，懂得了父母省吃俭用托举自己的全部深意，胸中生出无尽的生活力量与感恩！",
                            "effect": {"mentality": 40, "family": 35, "wealth": 0},
                            "isFatal": False,
                            "hiddenRiskLog": "在父辈朴素账本遗物中领悟家庭传承真谛，精神获得崇高升华。",
                            "status": "status_bereaved_parent"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "深夜翻看旧物哀伤过甚失眠数日，随后在晨光中昂首迈向新生活。",
                            "effect": {"mentality": 25, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "克制追思慰藉心灵。"
                        }
                    ]
                },
                {
                    "text": "觉得都是陈年旧账毫无经济价值，随手连同旧报纸一并扔入废品回收袋打包卖掉",
                    "choiceTags": ["时代：2016–2026", "年龄：28–70", "地域：全国各地", "门槛：冷漠实利主义者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "旧屋清理一空转手挂牌出租，生活没有受到丝毫情感波澜打扰，只是在某些深夜，偶尔感到心口空落落无处落脚。",
                            "effect": {"wealth": 10, "mentality": -10, "family": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "弃置父辈精神印记，斩断历史情感纽带。"
                        }
                    ]
                }
            ]
        }
    ]
