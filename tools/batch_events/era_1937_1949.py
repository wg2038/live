# -*- coding: utf-8 -*-
"""
1937–1949 战火与流亡时代：四大机制事件批次 (16条)
A. 路径补救 (学徒投奔、识字自学、流亡中学、商行转行)
B. 渐进伤害 (恶性疟疾、生锈铁片破伤风、极寒冻疮、难民营霍乱)
C. 经济诱惑 (法币金圆券贬值挤兑、黑市银元倒腾、典当传家宝、囤积秋粮)
D. 亲友离别 (战火至亲失散、老母道中病故、未寄出家书、代殓战友遗物)
"""

def get_events():
    return [
        # --- A. 路径补救 ---
        {
            "id": "evt_1937_1949_a1_xuetudang",
            "tier": "era",
            "title": "战乱避难：老字号国药铺拜师做学徒",
            "yearRange": [1937, 1948],
            "targetAge": [12, 22],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student", "status_high_official"],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "抗战时期大量失学难童投奔后方或租界中药铺、铁匠铺做三年零一节的学徒，管吃住无工钱，依靠苦力换取一门谋生手艺。",
            "narrative": "战火烧毁了家乡的屋舍，你流落到后方市镇，鞋底磨穿饥肠辘辘。街角同仁堂分号的老掌柜见你手脚勤快眼神老实，问你愿不愿立下字据三年学徒出师。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "跪地磕头立保约，甘愿起早贪黑打杂碾药三年，换取立足安身",
                    "choiceTags": ["时代：1937–1949", "年龄：12–22", "地域：全国城镇", "门槛：无正规文凭者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 78,
                            "log": "冬练三九夏练三伏，你记熟了上百味中草药炮制手艺，获掌柜赏识转为正式伙计，免受流民饥馑之苦。",
                            "effect": {"health": 5, "wealth": 15, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "乱世中以三年学徒之苦习得一技之长，奠定一生谋生根基。",
                            "status": "status_apprentice_certified"
                        },
                        {
                            "type": "injured",
                            "weight": 20,
                            "log": "研磨砒霜雄黄时粉尘吸入致慢性咽喉溃烂，虽学成出师但落下顽固咳嗽。",
                            "effect": {"health": -20, "wealth": 10, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "药铺研药落下呼吸道旧疾，劳动力略有受损。",
                            "status": "sequelae_respiratory"
                        },
                        {
                            "type": "fatal",
                            "weight": 2,
                            "log": "日寇敌机突袭市镇药铺中弹坍塌，在药窖中不幸被火舌吞没罹难。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "抗战乱世空袭无常，学徒生涯终断于战火。"
                        }
                    ]
                },
                {
                    "text": "嫌弃学徒规矩苛刻非打即骂，谢绝掌柜挽留，继续在码头做临时散工挑夫",
                    "choiceTags": ["时代：1937–1949", "年龄：12–22", "地域：沿江码头", "门槛：向往自由散漫者"],
                    "outcomes": [
                        {
                            "type": "redirected",
                            "weight": 90,
                            "log": "每天在码头扛大包出苦力，虽然日结两枚铜板自由自在，但一身皮肉多处拉伤，未来依然前途未卜。",
                            "effect": {"health": -10, "wealth": 5, "mentality": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "未能抓住学徒学艺之机，长期停留在底层苦力阶层。"
                        },
                        {
                            "type": "injured",
                            "weight": 10,
                            "log": "在雨夜跳板上滑倒，百斤麻袋重重砸在小腿上骨裂，卧床大半个月花光微薄积蓄。",
                            "effect": {"health": -25, "wealth": -15, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "码头苦力负伤缺乏保障，生活愈发窘迫。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_a2_saomang_zixue",
            "tier": "era",
            "title": "战火求知：桐油灯下借报识字扫盲",
            "yearRange": [1938, 1949],
            "targetAge": [10, 30],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student", "status_high_official"],
            "triggerProbability": 0.07,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "民国时期文盲率高达80%以上，后方战时民众教育馆与夜间识字班零星兴办，青年常借铅字旧报纸与桐油灯自学脱盲。",
            "narrative": "白天打柴劳作，夜晚在低矮土屋里点起如豆的桐油灯。你从教书先生门前捡回几张撕碎的《大公报》，用树枝沾水在青砖上反复临摹生字。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "省下口粮换桐油，每夜坚持临摹苦读两小时，向邻家老秀才虚心请教",
                    "choiceTags": ["时代：1937–1949", "年龄：10–30", "地域：全国城乡", "门槛：好学自律者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "一年下来你学会了八百常用字，能读懂布告家信与账册，被村里举荐为粮秣记账员。",
                            "effect": {"mentality": 30, "wealth": 15, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "战乱岁月中自学脱盲，成功打破文盲宿命改变社会阶层。",
                            "status": "status_literate"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "因长期在昏暗桐油烟气下用眼过度，双目严重近视红肿，视力大受折损。",
                            "effect": {"health": -15, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "苦读脱盲虽成，但过早落下重度眼疾。"
                        }
                    ]
                },
                {
                    "text": "觉得字不能当饭吃，早早吹灯睡觉以养精蓄锐应对明日重体力农活",
                    "choiceTags": ["时代：1937–1949", "年龄：10–30", "地域：农村山岭", "门槛：现实短视者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "日子如常在日出而作日落而息中消磨，文书官司依然要花铜钱请人代写代读。",
                            "effect": {"health": 5, "mentality": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "错失战时自学启蒙机会，终生停留在文盲阶层。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_a3_liuwang_zhongxue",
            "tier": "era",
            "title": "战火漂泊：后方联立流亡中学借读",
            "yearRange": [1937, 1945],
            "targetAge": [13, 19],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.06,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "抗战爆发后华北、东南各省中学师生跋涉数千里向后方流亡，教育部成立了国立第一至第二十二中学，收容上万流亡学生以工代赈求学。",
            "narrative": "学校在沦陷区停办，你跟随流亡师生队伍辗转千里抵达湘西山城。国立中学草建于破庙之中，以草席为被、苞谷饭度日，但书声琅琅不绝于耳。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "报名国立联中流亡借读生，半日出坡垦荒种菜，半日苦读数理英文",
                    "choiceTags": ["时代：1937–1945", "年龄：13–19", "地域：西南大后方", "门槛：初通文墨者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 80,
                            "log": "在破庙祠堂中完成了高中学业，结识了一批共患难的青年才俊，打下扎实国文与数理基础。",
                            "effect": {"mentality": 35, "wealth": -5, "health": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "在国立流亡中学坚持完结学业，保留了走向更高知识殿堂的火种。",
                            "status": "status_high_school_diploma"
                        },
                        {
                            "type": "injured",
                            "weight": 18,
                            "log": "流亡途中感染重度伤寒发热数日，幸得同窗倾力熬姜汤照料脱险，但身骨消瘦大半。",
                            "effect": {"health": -25, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "大后方求学期间罹患伤寒大病，体质转为虚弱。"
                        },
                        {
                            "type": "fatal",
                            "weight": 2,
                            "log": "遇敌机对后方小城野蛮低空轰炸，防空洞塌方不幸遇难牺牲。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "战火流亡青年学子殁于敌机轰炸。"
                        }
                    ]
                },
                {
                    "text": "因忍受不了山中饥寒与粗粝苞谷，选择离校投奔大后方城镇商铺投机谋生",
                    "choiceTags": ["时代：1937–1945", "年龄：13–19", "地域：后方市镇", "门槛：重实利者"],
                    "outcomes": [
                        {
                            "type": "redirected",
                            "weight": 95,
                            "log": "离开课堂进入茶馆打杂当跑堂，虽然顿顿有白米饭饱腹，但书本知识从此荒废。",
                            "effect": {"wealth": 20, "mentality": -10, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "中断正规中学教育，人生转轨为市井跑堂。"
                        },
                        {
                            "type": "entangled",
                            "weight": 5,
                            "log": "在茶馆打翻当地驻军军官茶碗遭殴打并讹诈钱财，连累掌柜赔偿。",
                            "effect": {"wealth": -20, "health": -15, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "市井谋生缺乏庇护，饱尝军阀兵痞欺凌。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_a4_tuoguanxi_diandang",
            "tier": "era",
            "title": "营生自救：托同乡引荐进米行记账",
            "yearRange": [1940, 1949],
            "targetAge": [18, 45],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.07,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "民国城市工商业高度依赖宗族同乡网络，谋求账房、跑街等体面职差往往需要三保俱全及同乡前辈作保引荐。",
            "narrative": "原籍工矿停摆，你在省城举目无亲。同乡会的老账房看你字迹端正且略懂算盘，私下表示若备得两块大洋作引荐茶钱，可保你进米行顶替空缺。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "东拼西凑凑齐引荐茶钱与保单，恭敬登门拜谒老账房求得差事",
                    "choiceTags": ["时代：1940–1949", "年龄：18–45", "地域：城市商圈", "门槛：懂珠算簿记者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "顺利进入粮行担任二账房，每月不仅有一斗平价米配额，更在混乱市面中获得庇护。",
                            "effect": {"wealth": 25, "family": 15, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "靠同乡地缘关系成功切入城市商界账房，避开失业流民厄运。",
                            "status": "status_merchant_clerk"
                        },
                        {
                            "type": "entangled",
                            "weight": 15,
                            "log": "粮行因囤粮倒卖被稽查处敲诈，账房被连带盘问三天，虽未受刑但惊吓不浅。",
                            "effect": {"wealth": -10, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "卷入战时粮行物资官司，深刻感受世道险恶。"
                        }
                    ]
                },
                {
                    "text": "拒绝送礼打点，坚信靠自己摆测字摊、替人代写家信维持生计",
                    "choiceTags": ["时代：1940–1949", "年龄：18–45", "地域：城市街巷", "门槛：清高自傲者"],
                    "outcomes": [
                        {
                            "type": "redirected",
                            "weight": 100,
                            "log": "在城隍庙摆摊代书，饥一顿饱一顿，全凭过路流民赏几个铜板过活，勉强维持温饱。",
                            "effect": {"wealth": -5, "mentality": -5, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "坚拒市井请托规则，沦为城隍庙清贫落魄文人。"
                        }
                    ]
                }
            ]
        },

        # --- B. 渐进伤害与可错选项 ---
        {
            "id": "evt_1937_1949_b1_nueji_caoyao",
            "tier": "era",
            "title": "夏秋瘴毒：突发恶性疟疾高热冷战",
            "yearRange": [1937, 1948],
            "targetAge": [6, 65],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.09,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "抗日战争期间华南与西南疟疾横行，奎宁（金鸡纳霜）被军阀与投机商炒成天价，普通百姓多以土方常山、青蒿或生姜硬扛。",
            "narrative": "午后突然周身冰凉如堕冰窖，盖三层棉被依然牙齿格格打战；紧接着热度如烈火燎原，满脸通红胡言乱语，大汗淋漓衣被湿透。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "咬牙变卖仅有的过冬棉被与铜盆，托人在黑市求购两颗真假难辨的奎宁丸吞服",
                    "choiceTags": ["时代：1937–1949", "年龄：6–65", "地域：全国城乡", "门槛：舍得倾囊医治者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 75,
                            "log": "药丸虽被奸商掺了面粉，但终含真奎宁，服用后冷热间歇拉长，七日后高烧退去彻底痊愈。",
                            "effect": {"health": 15, "wealth": -35, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "重金求购黑市抗疟药保全性命，但家中已一贫如洗。"
                        },
                        {
                            "type": "injured",
                            "weight": 22,
                            "log": "买到了掺杂假药，热度迟迟不退转为慢性疟疾，脾脏肿大如拳头，体能严重衰退。",
                            "effect": {"health": -30, "wealth": -30, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "黑市假药延误疟疾治疗，导致重度脾肿大与慢性贫血。",
                            "status": "sequelae_chronic_malaria"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "突发脑型疟疾昏迷抽搐，在深山茅屋中因高热惊厥不幸衰竭离世。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "恶性脑型疟疾夺去年轻生命。"
                        }
                    ]
                },
                {
                    "text": "舍不得花钱买天价西药，采用村里老法子大口吞服青蒿苦汁配烈酒发汗硬扛",
                    "choiceTags": ["时代：1937–1949", "年龄：6–65", "地域：乡村山岭", "门槛：笃信土方硬撑者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 65,
                            "log": "剧烈呕吐数天后侥幸退热保住一命，但肝脾受损，此后每逢农忙换季便频繁发作虚汗无力。",
                            "effect": {"health": -20, "wealth": 0, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "土法抗疟虽省钱，但遗留慢性脾肿大与易疲劳体质。",
                            "status": "sequelae_chronic_malaria"
                        },
                        {
                            "type": "safe",
                            "weight": 31,
                            "log": "自身免疫力过硬，生青蒿汁巧合对症，连饮数碗后大汗淋漓居然完全自愈。",
                            "effect": {"health": 5, "wealth": 0, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "凭借强悍体质险涉险关，传为村中奇谈。"
                        },
                        {
                            "type": "fatal",
                            "weight": 4,
                            "log": "烈酒与热病攻心导致神志不清，夜间呕吐物窒息不幸身故。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "盲信土方偏方烈酒发汗导致意外窒息。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_b2_shangshou_poshangfeng",
            "tier": "era",
            "title": "农具割伤：生锈铁镰划破脚底化脓",
            "yearRange": [1937, 1949],
            "targetAge": [8, 65],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "抗生素发明前，生锈农具造成的深部刺伤是农村破伤风与败血症的主要源头，民间多以灶灰、香灰覆盖，极易造成厌氧菌感染致死。",
            "narrative": "赤脚在烂泥田中抢割秋稻，脚底不慎踩在生锈的废铁犁头上，豁开一道寸许深口，鲜血混着黑泥汩汩外涌，痛彻心扉。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "听信同伴建议，抓起灶膛香灰和陈年牛粪敷在伤口上止血包扎，继续干活",
                    "choiceTags": ["时代：1937–1949", "年龄：8–65", "地域：农村泥滩", "门槛：盲从旧习硬扛者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 60,
                            "log": "创口深度厌氧感染化脓，整条小腿红肿如桶，发高烧半月，伤口烂见白骨终成跛足。",
                            "effect": {"health": -35, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "香灰糊伤口引发严重蜂窝织炎，导致终生行动跛行。",
                            "status": "sequelae_motor_impairment"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "破伤风梭菌蔓延致角弓反张、牙关紧闭，在痛苦抽搐中因呼吸肌麻痹不治。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "旧式封建泥灰糊伤口诱发急性破伤风殒命。"
                        },
                        {
                            "type": "safe",
                            "weight": 37,
                            "log": "老母亲见状急用开水冲洗泥沙并用烈酒浇创，居然顽强结痂愈合，未酿大祸。",
                            "effect": {"health": -10, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "开水清洗避免了严重感染，侥幸逃过截肢之灾。"
                        }
                    ]
                },
                {
                    "text": "立即停工，叫人用独轮车推到五里外县城教会红十字诊所做清创并注射破伤风血清",
                    "choiceTags": ["时代：1937–1949", "年龄：8–65", "地域：县城郊区", "门槛：具备卫生防范意识者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "外科大夫彻底扩创排净铁锈并注射血清，卧床两周伤口平整愈合，无任何后遗症。",
                            "effect": {"health": 5, "wealth": -20, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "科学现代清创打破破伤风致命锁链，保全完好肢体。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "异种马血清发生轻度过敏皮疹发痒，抗组胺治疗三日好转。",
                            "effect": {"health": -5, "wealth": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "血清轻微过敏，额外增加少许开销。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_b3_dongchuang_kuiyang",
            "tier": "era",
            "title": "极寒逃荒：严冬双足重度冻伤溃烂",
            "yearRange": [1938, 1948],
            "targetAge": [6, 70],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "北方与中原战乱流亡者在冰雪天气多着单薄破鞋，足趾耳廓冻死坏疽十分普遍，民间以雪搓、火烤常加剧组织坏死。",
            "narrative": "零下二十度的暴风雪中连夜跋涉，草鞋早已破烂漏出脚趾。等在破土地庙歇脚脱下草鞋时，发现双脚发硬苍白如木头，完全失去知觉。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "听信老辈传言，急忙扑到火堆边大火烘烤并抓起门外硬雪死命搓擦双脚",
                    "choiceTags": ["时代：1937–1949", "年龄：6–70", "地域：北方严寒地带", "门槛：盲从雪搓火烤偏方者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 70,
                            "log": "急剧升温与粗暴摩擦导致冻结毛细血管大面积破裂，两个脚趾发黑坏疽脱落，终生残疾。",
                            "effect": {"health": -30, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "错误使用火烤雪搓偏方导致肢端不可逆干性坏疽。",
                            "status": "sequelae_motor_impairment"
                        },
                        {
                            "type": "safe",
                            "weight": 30,
                            "log": "因冻结时间尚短，烤火后皮肉起大水疱溃烂数周，最终脱落新生红皮保全脚趾。",
                            "effect": {"health": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "重度冻疮侥幸未伤及骨骼，留下顽固冬令冻疮体质。"
                        }
                    ]
                },
                {
                    "text": "用体温微温的水慢慢温敷，撕下棉袄夹层干棉花严密包裹，置于怀中缓慢复温",
                    "choiceTags": ["时代：1937–1949", "年龄：6–70", "地域：北方严寒地带", "门槛：具备救护常识者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "双足刺痛麻木感逐渐消退恢复血色，仅起轻微冻疮红斑，半月后自如行走。",
                            "effect": {"health": 5, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "缓慢渐进复温科学化解严重冻伤，保全身躯完整。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "小脚趾遗留遇冷则发痒溃破的慢性冻疮顽疾。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "遗留季节性冻疮旧疾。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_b4_yinshi_huoluan",
            "tier": "era",
            "title": "疫病肆虐：夏日难民饮用浊井水剧烈吐泻",
            "yearRange": [1937, 1948],
            "targetAge": [6, 75],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "民国时期兵连祸结，战乱霍乱、副伤寒连年暴发，水源遭战死人畜污染，无抗生素与静脉输液条件下脱水致死率极高。",
            "narrative": "逃难路上酷暑难耐，你饮用了路边一口漂浮着死鼠的水井生水。入夜后肚腹绞痛如刀割，剧烈喷射状水样腹泻伴随呕吐，眼眶深陷双唇发紫。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "拼命硬撑，以为只是寻常中暑拉肚子，躺在草席上紧闭嘴巴滴水不进",
                    "choiceTags": ["时代：1937–1949", "年龄：6–75", "地域：战乱流徙地带", "门槛：盲目断水硬挺者"],
                    "outcomes": [
                        {
                            "type": "fatal",
                            "weight": 4,
                            "log": "重度脱水导致低血容量性休克与急性肾衰竭，在深夜无声无息停止了心跳。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "战乱期剧烈腹泻误判中暑滴水不进致严重脱水身故。"
                        },
                        {
                            "type": "injured",
                            "weight": 76,
                            "log": "身体虚脱濒死，三天后腹泻自限停止，但肾功能与心脏遭受打击，元气大伤一年无法干重活。",
                            "effect": {"health": -40, "wealth": -10, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "重度脱水休克险死还生，身体免疫系统与耐力持久减退。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "safe",
                            "weight": 20,
                            "log": "年轻底子硬，靠自身体液平衡熬过了最危险的二十四小时，虚脱后逐渐恢复。",
                            "effect": {"health": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "侥幸从烈性感染性肠炎中保全性命。"
                        }
                    ]
                },
                {
                    "text": "向同路老脚夫讨来粗盐和红糖，将井水彻底烧开数次，频频大口饮用糖盐温水",
                    "choiceTags": ["时代：1937–1949", "年龄：6–75", "地域：战乱宿营地", "门槛：懂口服补液法者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 92,
                            "log": "补充了大量电解质与水分，有效对抗了严重脱水，两日后排便成形转危为安。",
                            "effect": {"health": 5, "wealth": -5, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "自制糖盐水土法口服补液，成功战胜严重腹泻脱水险关。"
                        },
                        {
                            "type": "injured",
                            "weight": 8,
                            "log": "电解质虽得补足，但肠黏膜脱落较甚，消化功能在半年内较为脆弱。",
                            "effect": {"health": -10, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "消化系统恢复期偏长，需细粮调养。"
                        }
                    ]
                }
            ]
        },

        # --- C. 经济系统与诱惑 ---
        {
            "id": "evt_1937_1949_c1_jinyuanquan_tunmi",
            "tier": "era",
            "title": "恶性通胀：金圆券如废纸抢购平价米",
            "yearRange": [1948, 1949],
            "targetAge": [18, 65],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.12,
            "coolingPeriod": 5,
            "factLevel": "确证",
            "historicalFact": "1948年8月蒋介石发行金圆券强行收兑民间金银外币，数月间物价暴涨几万倍，市民推独轮车运钞票买米，工商业全面停摆崩溃。",
            "narrative": "街头报贩大喊金圆券今日又贬值三倍！厂里刚刚发下一大捆崭新的大额金圆券钞票，如不立刻花掉，到傍晚连一盒火柴都买不起。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "扛起整麻袋钞票发疯似地冲向南市米店，哪怕挨警棍也要抢购两袋白面与菜油",
                    "choiceTags": ["时代：1948–1949", "年龄：18–65", "地域：大中城市", "门槛：手头持有法币纸币者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "在头破血流的挤兑长队中抢回一袋精白面与两斤麻油，锁在箱底，确保全家老小一个月免于断炊。",
                            "effect": {"wealth": 15, "family": 25, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "敏锐洞察纸币贬值危机，以硬通货实物保卫家庭口粮。"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "在米店门口被哄抢人潮踩伤脚趾，买到的面粉袋被割破漏掉小半，勉强护住大半。",
                            "effect": {"health": -15, "wealth": 5, "mentality": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "抢米风潮中负伤，见证纸币崩溃时期的民生惨相。"
                        }
                    ]
                },
                {
                    "text": "轻信广播里官办平价物资宣传，犹豫等待明日物价管制生效后再去采购",
                    "choiceTags": ["时代：1948–1949", "年龄：18–65", "地域：大中城市", "门槛：犹豫盲信官方者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 100,
                            "log": "次日全城米行全部关门上锁，一麻袋金圆券只换回两个干瘪烧饼，积蓄化作废纸，全家陷入饥寒。",
                            "effect": {"wealth": -35, "mentality": -30, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "在恶性通货膨胀中错失变现时机，资产瞬间归零蒸发。",
                            "status": "status_asset_wiped"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_c2_heishi_yinyuan",
            "tier": "era",
            "title": "暗潮涌动：弄堂黑市倒腾袁大头银元",
            "yearRange": [1947, 1949],
            "targetAge": [20, 55],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 6,
            "factLevel": "确证",
            "historicalFact": "国统区末期民间全面拒用纸币，银元（袁大头、孙小头）成为实际流通货币。黑市银元贩子敲击银元听声辨伪，宪兵经常巡街查抄。",
            "narrative": "后街阴暗的过道里，几个熟人正手指夹着银元在耳边叮当作响听成色。邻居拉你入伙，称只要把乡下的土产换成十枚袁大头倒卖，几天就能赚一倍差价。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "拿出微薄家底加入黑市倒腾，走街串巷倒换银元赚取汇差",
                    "choiceTags": ["时代：1947–1949", "年龄：20–55", "地域：城市弄堂", "门槛：冒险求暴利者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 60,
                            "log": "你眼明手快，在宪兵来临前脱手套现，赚取了五枚成色十足的银元，发了笔小财。",
                            "effect": {"wealth": 35, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "在黑市投机倒把险中求胜，积累了一笔保底硬通货。"
                        },
                        {
                            "type": "entangled",
                            "weight": 35,
                            "log": "遇经济警察与宪兵突击搜查，连人带本钱全部被抄没，在拘留所关押三天才被保释。",
                            "effect": {"wealth": -40, "mentality": -25, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "黑市倒卖银元被宪兵搜缴一空，身陷拘押污点。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "因买到铜芯镀银假币与人争执，被黑帮打手持刀刺伤肩头。",
                            "effect": {"health": -25, "wealth": -30, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "黑市交易遭黑恶势力暗算负伤。"
                        }
                    ]
                },
                {
                    "text": "深知黑市龙蛇混杂且触犯禁令，坚拒诱惑，规矩守成安分守己",
                    "choiceTags": ["时代：1947–1949", "年龄：20–55", "地域：城市弄堂", "门槛：谨慎守序者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "几天后该弄堂的银元贩子被一锅端全部判刑，你暗自庆幸没有贪小便宜惹大祸。",
                            "effect": {"mentality": 20, "family": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "审慎克制避开黑市抓捕陷阱，保全阖家平安。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_c3_bianmai_shoushi",
            "tier": "era",
            "title": "度荒抉择：当铺典当母亲传家点翠金簪",
            "yearRange": [1938, 1947],
            "targetAge": [18, 60],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "抗日战争与内战期间灾荒频繁，典当行（押店）是城市贫民与破落户变现家产的残酷通道，当铺通常按实值两至三成苛刻折价。",
            "narrative": "全家已断炊两天，孩子饿得直哭。母亲从贴身棉袄深处摸出一支祖传点翠金簪，这是外婆传下来的唯一嫁妆，泪眼婆娑递到你手中。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "咬牙走向高高柜台的当铺，任凭朝奉百般贬损挑刺，换回半石杂面与几吊铜钱",
                    "choiceTags": ["时代：1938–1947", "年龄：18–60", "地域：全国城镇", "门槛：舍弃旧物救急者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "虽然金簪被苛扣了大半价值，但换来的杂粮让全家挺过了最青黄不接的寒冬。",
                            "effect": {"wealth": 15, "family": 15, "mentality": -10, "health": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "变卖祖传传家金簪救全家脱离饥荒，换来一家性命。"
                        },
                        {
                            "type": "entangled",
                            "weight": 10,
                            "log": "换来的伪钞在市场上被摊贩识破引发纠纷，所幸邻里出面调停化解。",
                            "effect": {"wealth": -5, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "当铺折现遭遇伪币暗算，深感底层生计艰难。"
                        }
                    ]
                },
                {
                    "text": "誓死不卖传家宝，四处向远房亲友厚着脸皮借讨米糠野菜勉强维持",
                    "choiceTags": ["时代：1938–1947", "年龄：18–60", "地域：全国城乡", "门槛：重情义守死节者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 65,
                            "log": "靠吃野菜榆树皮硬挺，幼子饿出重度浮肿病，虽保住金簪但家人身体大受摧残。",
                            "effect": {"health": -25, "family": -15, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "坚守旧物家传，代价是家人饱受饥馑营养不良折磨。"
                        },
                        {
                            "type": "safe",
                            "weight": 35,
                            "log": "亲友怜悯借了半斗苞谷，熬过了春荒，母亲的金簪得以完好传承。",
                            "effect": {"family": 20, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "在亲友接济下守住传家遗物。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_c4_touji_mihang",
            "tier": "era",
            "title": "险中博弈：借贷囤积新麦博取战乱差价",
            "yearRange": [1941, 1948],
            "targetAge": [22, 55],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.07,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "民国中晚期粮食统制政策漏洞百出，奸商与投机分子利用城防封锁与运力紧张囤粮居奇，但一旦遭遇兵变或物资查禁往往倾家荡产。",
            "narrative": "城外秋收新麦上市，运河船家私下联络称有一船小麦愿低价转让。只要借下月息三分的高利贷吃下这批粮，待下月关卡封锁物价必涨。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "抵押房契借高利贷赌上一把，将整船小麦悄悄运入自家地窖密藏",
                    "choiceTags": ["时代：1941–1948", "年龄：22–55", "地域：商埠水运枢纽", "门槛：借贷重仓投机者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 50,
                            "log": "战线变动运力阻断，城中粮价翻番，你顺利脱手归还本息，净赚一套街面铺房。",
                            "effect": {"wealth": 50, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "借高利贷投机倒把豪赌翻身，一跃成为本地富户。"
                        },
                        {
                            "type": "entangled",
                            "weight": 45,
                            "log": "地窖漏水小麦发霉发酸，又逢宪兵大搜查查扣大半，血本无归被高利贷逼得远走他乡。",
                            "effect": {"wealth": -60, "mentality": -35, "family": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "投机囤粮惨遭查封水渍，深陷高利债务断绝后路。",
                            "status": "status_debt_burdened"
                        },
                        {
                            "type": "fatal",
                            "weight": 5,
                            "log": "被城内饥民暴动发现囤粮地窖，争夺推搡中被踩踏致命。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "发国难财囤粮激化民愤不幸死于饥民暴动。"
                        }
                    ]
                },
                {
                    "text": "深知国难财不可发，且高利贷如虎狼，断然回绝投机邀约",
                    "choiceTags": ["时代：1941–1948", "年龄：22–55", "地域：商埠水运枢纽", "门槛：安守本分者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "不久后该批私粮遭驻军按倒卖军粮全额没收，倒买者入狱，你全身而退安宁无事。",
                            "effect": {"mentality": 20, "wealth": 0},
                            "isFatal": False,
                            "hiddenRiskLog": "不贪暴利规避灭顶之灾，守住平淡安全底线。"
                        }
                    ]
                }
            ]
        },

        # --- D. 亲友关系网与离别 ---
        {
            "id": "evt_1937_1949_d1_zhanluan_shisan",
            "tier": "era",
            "title": "烽火离散：码头拥挤逃难至亲下落不明",
            "yearRange": [1937, 1945],
            "targetAge": [6, 65],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "抗日战争造成近一亿难民大迁徙，汉口、宜昌、重庆等大撤退节点人潮拥挤失散者不计其数，许多家庭至死未能重逢。",
            "narrative": "敌机尖啸声中警报大作，难民潮疯狂涌向最后一艘客轮跳板。人流激荡冲撞间，紧拉着的手骤然被扯断，回头只见黑压压的人海哭喊，亲眷踪影全无。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "不上船，逆着逃难人流在江边废墟撕心裂肺搜寻三天三夜，张贴寻人墨字条",
                    "choiceTags": ["时代：1937–1945", "年龄：6–65", "地域：沿江码头", "门槛：重情重义者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 75,
                            "log": "未能找到失散亲眷，反因淋雨露宿高烧一场，只捡回亲人遗落的一只刻字旧铜墨盒，怀恨踏上未知前路。",
                            "effect": {"health": -20, "mentality": -30, "family": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "乱世中骨肉离散未能挽回，留下一生无尽的挂念与隐痛。",
                            "status": "status_lost_kin"
                        },
                        {
                            "type": "safe",
                            "weight": 22,
                            "log": "在难民收容所草棚角落奇迹般听到熟悉的呼唤，至亲抱头痛哭重聚，相约生死不离。",
                            "effect": {"family": 40, "mentality": 35, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "战火人海中奇迹寻回至亲，骨肉团聚支撑一生信念。"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "在码头寻找亲人时遭遇第二波敌机俯冲扫射，中弹罹难。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "战火寻亲不幸命丧空袭。"
                        }
                    ]
                },
                {
                    "text": "含泪顺从人流登上轮船撤往后方，牢记原籍地名，立誓日后登报寻访",
                    "choiceTags": ["时代：1937–1945", "年龄：6–65", "地域：沿江码头", "门槛：隐忍顾全大局者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "轮船缓缓起锚，江风如刀，你将泪水咽进肚里。虽然幸存抵达后方，但从此孑然一身。",
                            "effect": {"health": 5, "mentality": -20, "family": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "战火流散天各一方，成为漂泊后方的孤雁。",
                            "status": "status_lost_kin"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_d2_laomu_binggu",
            "tier": "era",
            "title": "异乡送终：逃荒古道上老母力竭安详离世",
            "yearRange": [1938, 1948],
            "targetAge": [14, 55],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_orphan"],
            "triggerProbability": 0.08,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "战乱期间长途跋涉对老弱妇孺是巨大磨难，饥渴、水土不服与痢疾常导致老人病故于荒野路侧，多只能就地薄葬。",
            "narrative": "鸡公独轮车推着年迈的老母亲行至秦岭山道，母亲的气息渐渐微弱。她颤抖着用枯槁的手抚摸你的额头，轻声嘱咐你要好好活下去，便闭上了双眼。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "向同路难民磕头借来两块洋钱买一口薄皮柳木棺材，在山冈松柏下掘穴成墓",
                    "choiceTags": ["时代：1938–1948", "年龄：14–55", "地域：山陕川黔驿道", "门槛：至孝尽礼者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "借钱为母亲立了一块无字石碑并向南磕了三个响头。虽背负一身盘缠债，但良心无愧。",
                            "effect": {"wealth": -20, "mentality": 10, "family": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "流亡途中尽孝送终，立下山岗石碑铭记母恩。",
                            "status": "status_bereaved_parent"
                        },
                        {
                            "type": "injured",
                            "weight": 10,
                            "log": "徒手掘石坑双手指节挫伤血肉模糊，寒冬感染发烧，同路人好心搀扶前行。",
                            "effect": {"health": -20, "wealth": -20, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "荒野葬母十指创伤，身心遭受重创。"
                        }
                    ]
                },
                {
                    "text": "囊空如洗无力买棺，只能用破旧草席将母亲仔细裹紧，就地深埋垒石为记",
                    "choiceTags": ["时代：1938–1948", "年龄：14–55", "地域：山陕川黔驿道", "门槛：现实无奈者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "在乱石堆前长跪不起，将母亲生前缝制的一双旧布鞋贴胸收好，擦干眼泪继续前行。",
                            "effect": {"wealth": 0, "mentality": -25, "family": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "草席葬母乱世无奈，带着母亲的针线布鞋活出坚韧。",
                            "status": "status_bereaved_parent"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_d3_weiji_jiashu",
            "tier": "era",
            "title": "泛黄心绪：行囊深处未寄出的原籍家书",
            "yearRange": [1940, 1949],
            "targetAge": [16, 60],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "抗战及内战阻断邮路，沦陷区与大后方通邮困难，需借由红十字会或中立国转递，万千家书滞留半途化作泛黄废纸。",
            "narrative": "整理多年颠沛流离的小铁盒，翻出一封五年前写好却因邮路阻断未能寄出的信件。信封已磨出毛边，墨迹微化，上面写着老家亲人的名字与地址。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "花两枚银角托付南下经商的民间走帮商人，请其辗转寻访投递此信",
                    "choiceTags": ["时代：1940–1949", "年龄：16–60", "地域：全国城乡", "门槛：执着念旧者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 60,
                            "log": "半年后客商托人捎回口信：老宅虽已毁于战火，但得知亲人已迁居乡下避难尚在人世，心头巨石落地。",
                            "effect": {"wealth": -10, "mentality": 30, "family": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "千里托信辗转获得原籍至亲音讯，慰藉半生漂泊。"
                        },
                        {
                            "type": "entangled",
                            "weight": 40,
                            "log": "客商收了银钱却杳无音信，信件如石沉大海，反添一层受骗的失落与悲凉。",
                            "effect": {"wealth": -10, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "托人捎信无果，徒增乱世离愁。"
                        }
                    ]
                },
                {
                    "text": "将信件就着油灯点燃化作灰烬，将对故土亲人的思念深埋心底，专注当下生存",
                    "choiceTags": ["时代：1940–1949", "年龄：16–60", "地域：全国城乡", "门槛：冷峻务实者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "纸灰在风中散尽，你不再回头望向沦陷的旧关河，神情变得更加坚毅沉着。",
                            "effect": {"mentality": 10, "wealth": 0},
                            "isFatal": False,
                            "hiddenRiskLog": "焚去旧信断绝执念，冷峻适应乱世求存规则。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1937_1949_d4_tongpao_fuxu",
            "tier": "era",
            "title": "烽火盟誓：代殓阵亡挚友送还染血铜墨盒",
            "yearRange": [1938, 1948],
            "targetAge": [18, 55],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.07,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "战争年代同僚战友朝夕相处生死托付，一人阵亡往往由幸存者代为收殓并设法将遗物送还孤儿寡母，是动荡岁月中最高尚的人性光芒。",
            "narrative": "轰炸过后硝烟弥漫，和你同甘共苦两年的同僚伤重不治。临终前他将随身的半瓶烧酒、一块怀表和染血的铜墨盒塞给你，求你将来带给他老家的妻儿。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "郑重对天起誓，将遗物视若生命妥善保管，跋涉千里亲手送抵挚友老家",
                    "choiceTags": ["时代：1938–1948", "年龄：18–55", "地域：全国各地", "门槛：诺重千钧者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "战事暂歇后你徒步寻访三个月，终于在僻远山村将遗物交到其白发老母手中，获全村人垂泪相敬。",
                            "effect": {"mentality": 35, "wealth": -15, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "千金一诺送还战友遗物，成就乱世中的道义丰碑。"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "送信途中遭溃兵抢劫，为死守挚友怀表右臂被枪托砸折，幸得路人营救保全遗物。",
                            "effect": {"health": -25, "wealth": -10, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "护送挚友遗物负伤受挫，虽体魄受损但义薄云天。"
                        }
                    ]
                },
                {
                    "text": "自身难保无力远涉，将怀表变卖换作两人逃难盘缠，将墨盒就地掩埋在坟头",
                    "choiceTags": ["时代：1938–1948", "年龄：18–55", "地域：战火前沿", "门槛：保全自我者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "靠变卖遗物换来的米面活了下来，但在每一个惊醒的梦夜，战友临终的眼神始终在心头挥之不去。",
                            "effect": {"wealth": 15, "mentality": -20, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "变卖亡友遗物救急虽换来苟活，却留下终生愧疚梦魇。"
                        }
                    ]
                }
            ]
        }
    ]
