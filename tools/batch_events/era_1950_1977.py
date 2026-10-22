# -*- coding: utf-8 -*-
"""
1950–1977 建国与工业化时代：四大机制事件批次 (16条)
A. 路径补救 (扫盲班脱盲、工农速成中学进修、赤脚医生培训出师、学徒工出师考级)
B. 渐进伤害 (小煤窑塌方砸伤、农药拌种轻微中毒、修水库腰肌劳损、困难期观音土腹胀)
C. 经济诱惑 (集资凭票购买二八飞鸽、黑市私兑粮票布票、典当寄卖旧表、跟风土法炼铁损锅)
D. 亲友离别 (困难时期至亲病殁、大三线深山信件、火车站台目送知青、因公殉职老技师遗物)
"""

def get_events():
    return [
        # --- A. 路径补救 ---
        {
            "id": "evt_1950_1977_a1_saomang_tuomang",
            "tier": "era",
            "title": "火热扫盲：农村冬学识字班煤油灯下苦读",
            "yearRange": [1950, 1958],
            "targetAge": [14, 45],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student", "status_high_school_diploma"],
            "triggerProbability": 0.09,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "建国初期全国掀起轰轰烈烈的扫盲运动，各村创办冬学和夜校，推行祁建华速成识字法，数百万人摘掉文盲帽子，学会记工分与写条据。",
            "narrative": "寒冬农闲，村大队部点起了汽灯与罩子灯，黑板上写着‘毛主席万岁’和‘抗美援朝’。村支书敲锣号召所有大姑娘小伙子都来扫盲班认字记工分。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "每晚顶风冒雪坚持上夜校，苦记注音字母与五百常用汉字，争当扫盲积极分子",
                    "choiceTags": ["时代：1950–1977", "年龄：14–45", "地域：全国农村", "门槛：无全日制文凭者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "经过两个冬天的刻苦突击，你顺利通过县扫盲验收大考，获发脱盲证书，被公社选派为生产队副记工员。",
                            "effect": {"mentality": 30, "wealth": 15, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "在建国初期扫盲运动中脱颖而出，从纯文盲跃升为基层记工骨干。",
                            "status": "status_literate"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "深夜在雪地返家途中摔入结冰水渠扭伤踝关节，由同班社员轮流背回家中，卧床休养大半月。",
                            "effect": {"health": -15, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "冬学上进途中摔伤扭骨，留下轻微阴雨天脚踝酸胀。"
                        }
                    ]
                },
                {
                    "text": "自认大老粗种地不需要咬文嚼字，宁愿窝在土炕上烤火编草鞋睡大觉",
                    "choiceTags": ["时代：1950–1977", "年龄：14–45", "地域：全国农村", "门槛：因循守旧者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "避开了冬夜严寒，但此后在公社分粮划字时依然只能按红手印，与文书会计岗位彻底无缘。",
                            "effect": {"health": 5, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "放弃扫盲脱贫机会，一生受困于文盲粗活。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_a2_gongnong_zhongxue",
            "tier": "era",
            "title": "组织选拔：保送工农速成中学带薪深造",
            "yearRange": [1951, 1957],
            "targetAge": [18, 32],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.07,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "1950年代初国家设立工农速成中学，抽调优秀青年工人、革命功臣带薪入学，用三年时间完成普通中学六年课程，随后直升大学工科。",
            "narrative": "厂工会与党委贴出光荣榜，鉴于你在车间技术革新中表现优异、政治过硬，决定保送你进入省立工农速成中学，保留原工资福利脱产深造三年。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "告别机床背起行囊，立下军令状誓把数理化硬骨头啃下来，决不辜负工人阶级嘱托",
                    "choiceTags": ["时代：1950–1977", "年龄：18–32", "地域：工业城市", "门槛：工矿先进生产者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "三年夜以继日苦攻代数立体几何与物理，顺利以优异成绩结业，直接升入工业专科学校成为技术骨干。",
                            "effect": {"mentality": 35, "wealth": 20, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "抓住工农速成中学历史机遇实现学历飞跃，晋升厂级技术干部。",
                            "status": "status_high_school_diploma"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "底子太薄拼命赶进度导致神经衰弱与重度胃溃疡，虽勉强结业但身形大为消瘦。",
                            "effect": {"health": -20, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "速成高强度学习引发慢性消化道功能紊乱。"
                        }
                    ]
                },
                {
                    "text": "担忧自己底子太差跟不上数理公式，主动向厂长请辞留在车间继续当机床能手",
                    "choiceTags": ["时代：1950–1977", "年龄：18–32", "地域：工业城市", "门槛：安于实操者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "留在熟悉的车间继续当老师傅，虽踏实受敬重，但随着新工艺引进而逐步落后于新一代科班工程师。",
                            "effect": {"wealth": 10, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "放弃进修干部通道，终身保留老资格一线技术工人身份。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_a3_chijiao_yisheng",
            "tier": "era",
            "title": "公社送教：参加赤脚医生卫生员集训",
            "yearRange": [1965, 1976],
            "targetAge": [16, 28],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "1965年毛泽东发出‘把医疗卫生工作的重点放到农村去’的号召，全国培训了百万名半农半医的赤脚医生，一根银针一把草药解决基层看病难。",
            "narrative": "大队贫下中农管理委员会推选你参加县人民医院举办的‘赤脚医生三个月速成班’。桌上发了《赤脚医生手册》、一套针灸针和几盒常用磺胺类药。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "在自己身上练习扎针，熟悉银针穴位与急救包扎，毕业背起红十字小药箱走村串户",
                    "choiceTags": ["时代：1950–1977", "年龄：16–28", "地域：广大农村", "门槛：初中文化青年"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "白天赤脚下田割谷，夜晚提马灯出诊为社员接生治感冒，成为全大队公认的救命好后生，工分待遇优渥。",
                            "effect": {"mentality": 30, "wealth": 15, "health": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "成为受人敬重的半农半医赤脚医生，建立深厚群众威望。",
                            "status": "status_barefoot_doctor"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "深夜翻山越岭抢救难产孕妇失足滚下山坡，手肘擦伤挫骨，忍痛赶到现场接生母子平安。",
                            "effect": {"health": -15, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "夜路出诊负伤但救活两命，树立医者崇高仁心。"
                        }
                    ]
                },
                {
                    "text": "畏惧给乡亲打针见血出事故，借口晕血把名额让给大队会计的侄子",
                    "choiceTags": ["时代：1950–1977", "年龄：16–28", "地域：广大农村", "门槛：胆小规避者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "继续留在生产队挣十个工分，虽无责任风险，但也错失了改变社会阶层的良机。",
                            "effect": {"mentality": -5, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "主动推辞卫生员机遇，继续全日制重体力劳作。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_a4_xuetong_zhuanzheng",
            "tier": "era",
            "title": "苦练技术：国营大厂三年学徒满期考核",
            "yearRange": [1953, 1965],
            "targetAge": [17, 24],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "计划经济时期国营工矿严格推行八级工资制，学徒工三年期满需通过工件锉削、游标卡尺测量等严苛操作考核方能转正为二级工。",
            "narrative": "三年当学徒，给八级钳工师父端茶递扳手扫铁屑。今天车间主任和工会代表站在机床旁监考，要求你在两小时内徒手锉出一个公差千分之二毫米的凹凸配块。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "凝神静气，端正站姿，严格按照师父传授的手法推锉，反复用刀口尺精密验光",
                    "choiceTags": ["时代：1950–1977", "年龄：17–24", "地域：重工业工矿", "门槛：学徒三年期满者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 88,
                            "log": "零件严丝合缝不见一丝漏光！考官集体起立鼓掌，顺利通过转正考核定为二级工，月工资涨至38.5元。",
                            "effect": {"wealth": 25, "mentality": 30, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "以过硬基本功考取正式国企钳工编制，端上铁饭碗。",
                            "status": "status_certified_mechanic"
                        },
                        {
                            "type": "injured",
                            "weight": 12,
                            "log": "过度紧张左手大拇指被铁件毛刺深扎流血，咬牙强撑完成，虽勉强及格定为一级工，但伤口发炎化脓。",
                            "effect": {"health": -10, "wealth": 10, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "考核带伤勉强过关，起薪级别略受压制。"
                        }
                    ]
                },
                {
                    "text": "妄图耍小聪明用电动砂轮机偷懒磨光工件，被现场老技师当场识破严厉训斥",
                    "choiceTags": ["时代：1950–1977", "年龄：17–24", "地域：重工业工矿", "门槛：投机取巧者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 100,
                            "log": "因违规操作且公差严重超标被判定不及格，延长学徒期一年并在车间大会上作深刻检讨。",
                            "effect": {"mentality": -25, "wealth": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "违章取巧转正延期，成为车间反面典型受挫。"
                        }
                    ]
                }
            ]
        },

        # --- B. 渐进伤害与可错选项 ---
        {
            "id": "evt_1950_1977_b1_kuangong_tanfang",
            "tier": "era",
            "title": "井下险情：地方小煤矿掌子面落石砸伤",
            "yearRange": [1958, 1976],
            "targetAge": [18, 55],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "五六十年代各地群办地方小煤窑、社队煤矿，木质支护简陋，‘大跃进’与战备时期经常冒顶塌方，压伤骨折与矽肺发生率较高。",
            "narrative": "井下百米深处阴冷潮湿，掌子面突然发出吱吱呀呀木头断裂声，碎石如雨点般砸下。几块百余斤重的坚硬矸石从顶板直直向你压来！",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "不顾一切抱头向安全通风副巷猛扑，尽量贴紧坚硬岩壁避开落石中心",
                    "choiceTags": ["时代：1950–1977", "年龄：18–55", "地域：采掘工矿", "门槛：具备逃生避险反应者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 75,
                            "log": "狂尘弥漫中你滚入副巷，大块矸石擦背而过砸断铁轨，仅受轻微皮肉擦伤，安然脱险。",
                            "effect": {"health": -10, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "果断避险险涉冒顶塌方，被评为矿井安全自救典型。"
                        },
                        {
                            "type": "injured",
                            "weight": 22,
                            "log": "右腿被崩飞的矸石击中造成闭合性胫骨骨折，由工友用矿车推出井口送县医院打石膏打钢针。",
                            "effect": {"health": -35, "wealth": -10, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "矿山落石导致胫骨骨折，伤愈后阴雨天隐痛不适。",
                            "status": "sequelae_motor_impairment"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "巨石砸毁顶梁瞬间压塌整个巷道，胸腹部严重压榨伤不幸当场殉职。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "煤窑严重冒顶事故不幸以身殉职。"
                        }
                    ]
                },
                {
                    "text": "舍不得刚装满优质原煤的矿车，试图先推走矿车再撤离",
                    "choiceTags": ["时代：1950–1977", "年龄：18–55", "地域：采掘工矿", "门槛：贪恋公家资产者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 70,
                            "log": "矿车被整块煤壁砸扁，你被气浪推倒撞在支柱上断裂两根肋骨，被赶来的救护队挖出捡回一命。",
                            "effect": {"health": -45, "wealth": 0, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "贪恋物资滞留险境致多发肋骨骨折，胸壁留下畸形痛。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "fatal",
                            "weight": 5,
                            "log": "二次大面积冒顶瞬间活埋整个掌子面，未能生还。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "为护矿车延误撤离时机遭矸石掩埋罹难。"
                        },
                        {
                            "type": "safe",
                            "weight": 25,
                            "log": "幸运推车冲出塌方边缘，矿车保住人未挂彩，受到矿部通报表扬记大功一次。",
                            "effect": {"wealth": 15, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "冒险抢救公物大难不死受奖。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_b2_huishou_zhongdu",
            "tier": "era",
            "title": "农药防护缺失：拌种六六六粉头晕恶心",
            "yearRange": [1956, 1975],
            "targetAge": [16, 65],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "建国后大量使用六六六粉、DDT等有机氯有机磷农药消灭麦蚜与蝗虫，农民因无手套口罩赤手拌种，常发急慢性吸入性神经毒性反应。",
            "narrative": "公社库房里弥漫着刺鼻的六六六农药粉尘。你徒手翻拌麦种大半天，午后突然头痛欲裂、恶心呕吐、视物模糊成双，汗毛倒竖四肢颤抖。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "听信老农偏方，猛灌两大碗生冷绿豆汤与陈醋，关上房门蒙头大睡发汗硬扛",
                    "choiceTags": ["时代：1950–1977", "年龄：16–65", "地域：农村库房", "门槛：盲信民间解毒方者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 70,
                            "log": "有机磷毒素未能及时络合清除，在炕上剧烈呕吐抽搐两天，毒素损害肝功能，休养三个月始能勉强下床。",
                            "effect": {"health": -30, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "偏方抗农药中毒延误病情，导致慢性中毒性肝损害。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "农药肺水肿伴随呼吸衰竭，在深夜熟睡中窒息离世。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "农药吸入重度中毒盲信偏方致呼吸衰竭逝世。"
                        },
                        {
                            "type": "safe",
                            "weight": 27,
                            "log": "因中毒剂量尚浅，吐出残胃物后大量排尿，依靠强壮肝脏代谢侥幸脱险痊愈。",
                            "effect": {"health": -10, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "轻度农药中毒体质较硬自行代谢恢复。"
                        }
                    ]
                },
                {
                    "text": "立刻用大量肥皂水彻底冲洗面部与双手皮肤，由家人急送公社卫生院洗胃并注射解磷定",
                    "choiceTags": ["时代：1950–1977", "年龄：16–65", "地域：农村公社", "门槛：具备卫生洗消常识者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "洗胃排毒与特异性解毒剂阻断了胆碱酯酶抑制，卧床输液两天症状全消，完全康复无后遗症。",
                            "effect": {"health": 5, "wealth": -10, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "科学洗消排毒阻断有机磷中毒，完好保全身体各脏器。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "洗胃过程插管擦伤食管黏膜，胸骨后轻微疼痛一周。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "急救轻微器械擦伤无大碍。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_b3_shuiku_laoshun",
            "tier": "era",
            "title": "水利大会战：独轮车推土过度腰椎急性扭伤",
            "yearRange": [1958, 1975],
            "targetAge": [17, 50],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.09,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "五六十年代全国农田水利建设如火如荼，数千万民工肩挑手推修筑十三陵、红旗渠、丹江口等水库，重负荷下腰肌劳损与椎间盘病变普遍。",
            "narrative": "红旗猎猎的水库大坝工地上，你推着四百斤湿重黄土的木独轮车冲陡坡，前轮猛地磕在暗石上骤停，后腰咔嚓一声剧痛，整个人直不起腰跪倒在泥坡上。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "咬牙喊出‘轻伤不下火线’口号，用麻绳狠扎腰间强行站起，继续咬牙推完十车",
                    "choiceTags": ["时代：1950–1977", "年龄：17–50", "地域：水库工地", "门槛：硬扛吃苦拼命者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 80,
                            "log": "急性腰肌纤维严重撕裂并导致腰椎间盘纤维环破裂，神经根受压，从此落下弯腰受限的顽固腰痛。",
                            "effect": {"health": -30, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "过度硬扛导致急性腰扭伤转为终身慢性腰椎病。",
                            "status": "sequelae_chronic_backpain"
                        },
                        {
                            "type": "safe",
                            "weight": 20,
                            "log": "精神原子弹爆发，靠青年强健筋骨熬过了剧痛，被工地指挥部评为‘铁人标兵’奖红脸盆一个。",
                            "effect": {"mentality": 30, "wealth": 5, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "拼命精神换来政治荣誉，但身体透支埋下隐患。"
                        }
                    ]
                },
                {
                    "text": "立即向排长请假，在工地医疗棚硬板床上平躺绝对卧床三天，配合热敷拔火罐",
                    "choiceTags": ["时代：1950–1977", "年龄：17–50", "地域：水库工地", "门槛：遵医嘱理智休养者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 92,
                            "log": "经充分平卧休克与红外线理疗，腰背筋膜水肿完全吸收，腰力逐步复原，未落下病根。",
                            "effect": {"health": 5, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "及时制动卧床化解腰部重伤，保全劳动能力。"
                        },
                        {
                            "type": "injured",
                            "weight": 8,
                            "log": "因请假扣除三天工分，同班组有些风言风语，但身体确实保住了。",
                            "effect": {"wealth": -5, "mentality": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "短暂停工受扣工分，但换来健康长远利益。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_b4_guanyintu_zhongzhang",
            "tier": "era",
            "title": "饥馑度荒：误食观音土致重度腹胀便结",
            "yearRange": [1959, 1961],
            "targetAge": [6, 70],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "估计/文学化",
            "historicalFact": "1959-1961年部分受灾农村粮食供应极度紧张，群众被迫采集榆树皮、野草根乃至含高岭土的‘观音白泥’充饥，常引发机械性肠梗阻。",
            "narrative": "青黄不接春荒难熬，肚子如火烧般绞痛。你咽下了掺着粗麦麸的一块白观音土饼子，三天后腹部鼓胀硬如磐石，剧痛难忍无法排便，冷汗淋漓。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "硬忍着不敢告诉公社干部，独自关在柴房用棉布狠勒腹部妄图把干硬物挤压出来",
                    "choiceTags": ["时代：1950–1977", "年龄：6–70", "地域：饥荒重灾村", "门槛：盲目蛮干硬挺者"],
                    "outcomes": [
                        {
                            "type": "fatal",
                            "weight": 4,
                            "log": "暴力压迫导致缺血肠管穿孔并发急性弥漫性腹膜炎，在无手术条件下不幸休克离世。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "观音土肠梗阻暴力挤压致肠穿孔不幸殒命。"
                        },
                        {
                            "type": "injured",
                            "weight": 76,
                            "log": "肠管严重水肿坏死边缘，最后由家人发现用植物油灌肠抠掏出干结泥团，九死一生大伤肠胃。",
                            "effect": {"health": -45, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "机械性肠梗阻险死还生，消化功能遭受持久打击。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "safe",
                            "weight": 20,
                            "log": "依靠自身肠道强烈蠕动拼死排出，虚脱后狂饮温开水，逐渐排空缓过劲来。",
                            "effect": {"health": -20, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "侥幸自行排出高岭土硬块脱险。"
                        }
                    ]
                },
                {
                    "text": "向大队赤脚医生坦白求助，服用蓖麻油导泻并配合温盐水连续深部灌肠",
                    "choiceTags": ["时代：1950–1977", "年龄：6–70", "地域：农村公社", "门槛：敢于如实求医者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 92,
                            "log": "在医生耐心润滑灌肠协助下排出干硬土块，腹胀大消，饮用米汤三天后身体逐渐平复。",
                            "effect": {"health": 5, "mentality": 15, "family": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "科学灌肠导泻解除了致命性肠梗阻，平稳度过危局。"
                        },
                        {
                            "type": "injured",
                            "weight": 8,
                            "log": "灌肠机械性刺激轻微引起结肠黏膜擦伤出血，服用止血草药数日好转。",
                            "effect": {"health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "灌肠伴随轻度黏膜损伤已完全受控。"
                        }
                    ]
                }
            ]
        },

        # --- C. 经济系统与诱惑 ---
        {
            "id": "evt_1950_1977_c1_jizhi_feige",
            "tier": "era",
            "title": "家庭大件：集全家积蓄凭工业券抢购飞鸽单车",
            "yearRange": [1962, 1976],
            "targetAge": [20, 55],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "计划经济时期自行车、缝纫机、手表并称‘老三大件’，一辆天津飞鸽或上海永久标价约150-180元，相当于普通工人四五个月工资，且需凭特供工业券购买。",
            "narrative": "全家省吃俭用三年攒足一百六十元，又托单位老工长弄到一张宝贵的天津飞鸽自行车工业购货券。百货大楼玻璃柜台前人头攒动，黑油漆二八大杠散发着机油清香。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "全额交纳一百六十元现金与工业券，推走崭新的二八飞鸽单车，套上自织红毛线车把套",
                    "choiceTags": ["时代：1950–1977", "年龄：20–55", "地域：城镇矿区", "门槛：手头有大笔储蓄者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "推车骑过厂区引来无数羡慕目光！不仅通勤省下一个多小时，更成为全家最骄傲的传家重器。",
                            "effect": {"wealth": -25, "family": 30, "mentality": 30},
                            "isFatal": False,
                            "hiddenRiskLog": "购置家庭第一辆传世飞鸽自行车，极大改善家庭生活便利度与社会声望。"
                        },
                        {
                            "type": "entangled",
                            "weight": 10,
                            "log": "车停在菜场门口车铃盖被顽童拧走，心痛了整整三天，赶忙找铁匠配了个铜挂锁。",
                            "effect": {"wealth": -30, "family": 20, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "拥有一辆珍贵单车增添了日常看护与防盗挂虑。"
                        }
                    ]
                },
                {
                    "text": "舍不得掏空全家老小积蓄，将工业券原价转让给待婚的工友，留钱应对生老病死",
                    "choiceTags": ["时代：1950–1977", "年龄：20–55", "地域：城镇矿区", "门槛：过日子精打细算者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "把钱老老实实存入人民银行储蓄所，继续安步当车，工友感激你的转让，两家关系坚如钢铁。",
                            "effect": {"wealth": 10, "family": 15, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "守住现金安全防线，克制消费赢得良好人情赞誉。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_c2_heishi_bupiao",
            "tier": "era",
            "title": "票证调剂：粮店后巷私下倒兑全国粮票与布票",
            "yearRange": [1960, 1976],
            "targetAge": [18, 55],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 6,
            "factLevel": "确证",
            "historicalFact": "计划经济时期一切日用品凭票供应，全国通用粮票含油水可带出省，黑市上常有人以鸡蛋、香油或高价私兑粮票布票，被定性为投机倒把受到巡查打击。",
            "narrative": "过年想给长身体的孩子扯两尺纯棉蓝布做身新棉袄，但家里布票早已用尽。粮站后巷的拐角处，几个低檐帽常客正在鬼鬼祟祟用香油私换全国粮票和布票。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "用家中省下来的两斤清油，在暗处悄悄跟票贩子兑换三尺布票与十斤地方粮票",
                    "choiceTags": ["时代：1950–1977", "年龄：18–55", "地域：城市后巷", "门槛：急需生活布匹者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 70,
                            "log": "顺利避开巡逻民警换回布票，母亲连夜踩缝纫机为孩子赶出崭新小棉袄，除夕夜全家喜气洋洋。",
                            "effect": {"family": 25, "mentality": 20, "wealth": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "暗中调剂紧缺票证满足生活之需，阖家温暖。"
                        },
                        {
                            "type": "entangled",
                            "weight": 30,
                            "log": "刚接手就被居委会治保主任和联防队员当场截获，油和票全被没收，被责令在居委会作深刻检讨。",
                            "effect": {"wealth": -20, "mentality": -25, "family": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "黑市私兑票证被抓现行，家庭档案记上投机倒把批评。"
                        }
                    ]
                },
                {
                    "text": "坚决不碰黑市底线，将旧棉被拆洗翻新重新絮棉花，熬到明年发新票",
                    "choiceTags": ["时代：1950–1977", "年龄：18–55", "地域：城市后巷", "门槛：遵纪守法者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "虽然衣服打着补丁，但一家人平平安安行得正坐得直，未给工作单位招惹半分嫌疑与麻烦。",
                            "effect": {"mentality": 15, "family": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "安贫乐道坚守政策底线，家庭政审清白。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_c3_diandang_shoubiao",
            "tier": "era",
            "title": "应急变现：委托信托商店寄卖半钢旧手表",
            "yearRange": [1963, 1976],
            "targetAge": [22, 60],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.07,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "公私合营后原当铺被改组为国营信托商店（寄卖行），负责估价寄卖民间旧钟表、毛料大衣和照相机，收取手续费，是普通市民变现应急的合法通道。",
            "narrative": "家中老人突发重疾急需自费药物与白糖营养品，积蓄告罄。你将结婚时购买的七成新上海牌半钢手表摘下，步入街角高挂‘信托寄卖’招牌的门市。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "接受店员六十元的压价估价，当场办结寄存转让手续，拿走沉甸甸的救急现钞",
                    "choiceTags": ["时代：1950–1977", "年龄：22–60", "地域：城市信托寄卖店", "门槛：持有旧大件者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "六十元现金及时付清了老人住院药费，将老人从鬼门关拉回，全家渡过重大危机。",
                            "effect": {"wealth": 20, "family": 25, "mentality": -5, "health": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "变卖心爱手表挽回至亲健康，舍身尽孝担当家庭支柱。"
                        },
                        {
                            "type": "entangled",
                            "weight": 10,
                            "log": "事后伴侣因失去重要定情信物伤心落泪，两口子心有芥蒂互相沉默了多日。",
                            "effect": {"family": -10, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "变卖结婚纪念大件引发家庭内部情感隔阂。"
                        }
                    ]
                },
                {
                    "text": "舍不得卖掉定情物，掉头向车间几十个工友挨个开口每人借两三元拼凑医药费",
                    "choiceTags": ["时代：1950–1977", "年龄：22–60", "地域：城市信托寄卖店", "门槛：好面子借债者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "工人阶级互助友爱，工友们凑足五十元解了燃眉之急，此后你发工资逐月按期奉还，赢得众人信赖。",
                            "effect": {"wealth": -10, "mentality": 15, "family": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "借债度难保住传家手表，守信履约铸就良好工友情谊。"
                        },
                        {
                            "type": "entangled",
                            "weight": 15,
                            "log": "个别工友催债言辞刻薄，闹得车间人尽皆知，背负人情债心头沉重。",
                            "effect": {"mentality": -15, "wealth": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "四处小额借款伤及自尊脸面。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_c4_genfeng_tugaolu",
            "tier": "era",
            "title": "狂热跟风：后院私搭土高炉砸铁锅炼钢",
            "yearRange": [1958, 1959],
            "targetAge": [16, 60],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.09,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "1958年大跃进全民大炼钢铁，全国数千万人土法上马建土高炉，砸烂铁锅、铜门环甚至锄头投入炉中，炼出大量无法工业使用的脆生铁渣。",
            "narrative": "满城红旗招展锣鼓喧天，单位和胡同院里垒起冒浓烟的黏土高炉。积极分子登门动员，要求各家交出废旧铁器砸锅熔铁，誓向国庆献礼超英赶美。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "将家中仅有的一口双耳生铁大锅和旧铁锁主动砸碎上缴土高炉，彻夜拉风箱苦战",
                    "choiceTags": ["时代：1958–1959", "年龄：16–60", "地域：全国城乡", "门槛：狂热跟风积极分子"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 70,
                            "log": "炉中烧出一坨毫无韧性的海绵脆生铁渣，自家大锅却彻底毁坏，不久公共食堂停办全家连口做饭铁锅都没有。",
                            "effect": {"wealth": -25, "mentality": -15, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "砸铁锅炼出无用铁疙瘩，日常生活陷入严重物资匮乏困境。"
                        },
                        {
                            "type": "safe",
                            "weight": 28,
                            "log": "因拉风箱表现积极获评‘红旗炼钢好手’，戴大红花上台表彰，弥补了经济损失。",
                            "effect": {"mentality": 25, "wealth": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "以毁损家用铁器为代价换得短期政治荣誉。"
                        },
                        {
                            "type": "fatal",
                            "weight": 2,
                            "log": "土高炉耐火泥坍塌发生钢水喷溅爆燃，重度烧伤不幸身亡。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "土法炼铁严重违章发生钢渣爆炸事故殒命。"
                        }
                    ]
                },
                {
                    "text": "悄悄把祖传做饭铁锅埋入后院菜地泥土下伪装遗失，仅上缴两把废旧烂生锈火钳应付差事",
                    "choiceTags": ["时代：1958–1959", "年龄：16–60", "地域：全国城乡", "门槛：机警务实保底者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "风潮过后全村铁器奇缺，你从土里刨出完好无损的铁锅，全家老小安稳开火做饭，暗自佩服自己的远见。",
                            "effect": {"wealth": 15, "family": 20, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "机警藏锅躲过荒诞狂热，守住最核心的温饱家当。"
                        }
                    ]
                }
            ]
        },

        # --- D. 亲友关系网与离别 ---
        {
            "id": "evt_1950_1977_d1_kunnan_shangou",
            "tier": "era",
            "title": "春荒讣告：远房堂兄病故倾尽口粮接济遗孤",
            "yearRange": [1959, 1962],
            "targetAge": [18, 65],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 12,
            "factLevel": "估计/文学化",
            "historicalFact": "三年经济困难时期农村受灾严重，宗族亲邻之间节衣缩食、通过邮局互寄几斤炒面红枣接济孤残成为维系生命的重要民间温情通道。",
            "narrative": "邮递员送来一封薄薄的毛边纸信，老家来报堂兄因严重浮肿不治病故，丢下两个刚上小学的孩子，孤儿寡母口粮眼看就要彻底断绝。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "全家每顿饭勒紧裤带少吃一口，省下十斤晒干的红薯干和五元钱，寄往老家抚养遗孤",
                    "choiceTags": ["时代：1950–1977", "年龄：18–65", "地域：全国各地", "门槛：血浓于水顾家者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "寄出的红薯干让两个苦命孩子活了下来。两年后嫂子带孩子登门深情跪谢，亲情血脉紧紧相依。",
                            "effect": {"wealth": -20, "family": 35, "mentality": 20, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "在困难时期倾囊接济兄长遗孤，托举至亲骨肉保全血脉。",
                            "status": "status_family_protector"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "自家本就极度缺少油脂，长期过量节食导致自身也出现双下肢轻度凹陷性水肿。",
                            "effect": {"health": -20, "family": 30, "wealth": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "舍身救助同胞导致自身轻度营养不良水肿。"
                        }
                    ]
                },
                {
                    "text": "自家孩子也面黄肌瘦，狠下心肠只回一封劝慰信，不敢掏出仅有的活命粮",
                    "choiceTags": ["时代：1950–1977", "年龄：18–65", "地域：全国各地", "门槛：泥菩萨过江自保者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "保全了自家小家庭平稳渡过难关，但老家亲族从此对你形同陌路，来往音讯渐绝。",
                            "effect": {"health": 5, "family": -25, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "灾荒之年独善其身，导致宗族骨肉情感裂痕难以弥合。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_d2_sanxian_guahao",
            "tier": "era",
            "title": "深山来信：大三线挚友跨越千里的挂号家书",
            "yearRange": [1965, 1976],
            "targetAge": [18, 60],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "1960年代中期起数百万人奔赴‘好人好马上三线’的西南西北深山，隐姓埋名建设军工基地，与沿海故土亲友主要通过严格审验的邮政挂号信联系。",
            "narrative": "收到一封来自‘四川某地404信箱’的厚重挂号信。同窗挚友响应号召进山造雷达已整整五年，信中夹着一片山里的红枫叶与几张泛黄的手绘蓝图。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "精心挑选两本机械设计工具书与一盒青岛蛤蜊油，包裹挂号寄往深山给挚友御寒",
                    "choiceTags": ["时代：1950–1977", "年龄：18–60", "地域：全国各地", "门槛：珍惜友谊者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "挚友回信热泪盈眶，称这盒蛤蜊油在冰冷防空洞里治好了他溃烂的双手，两人相约建设祖国各自发光。",
                            "effect": {"mentality": 30, "family": 15, "wealth": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "遥寄书籍油膏温暖深山三线战友，成就跨越一生的莫逆之交。"
                        },
                        {
                            "type": "entangled",
                            "weight": 5,
                            "log": "包裹因保密信箱地址核验延误两月，所幸完好送达。",
                            "effect": {"mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "保密通信延时无大碍。"
                        }
                    ]
                },
                {
                    "text": "工作繁忙随手把信压在台玻璃下，心想大山阻隔各安天命，未作回音",
                    "choiceTags": ["时代：1950–1977", "年龄：18–60", "地域：全国各地", "门槛：疏于联络者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "日子一天天过去，信箱那头再也没有信件寄来，那段少年时代的情谊悄然沉寂于万重青山之中。",
                            "effect": {"mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "时空阻隔任由旧友情谊消磨无痕。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_d3_zhiqing_zhantai",
            "tier": "era",
            "title": "站台惜别：蒸汽机车汽笛下目送至亲知青下乡",
            "yearRange": [1968, 1976],
            "targetAge": [16, 65],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "上山下乡运动中全国1700多万城镇知青奔赴农村与边疆农场。火车站台挤满敲锣打鼓与掩面痛哭的父母家眷，一列列绿皮车承载了一代人的青春远行。",
            "narrative": "站台上人山人海红旗招展，大喇叭放着革命歌曲。绿皮列车即将开往黑龙江北大荒，胞弟/同胞从车窗探出身子，满眼泪花使劲挥舞着红宝书。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "挤过人流追赶缓缓启动的列车，将自己棉袄内贴身缝有十五元私房钱的小布袋死命塞进车窗",
                    "choiceTags": ["时代：1950–1977", "年龄：16–65", "地域：火车站台", "门槛：手足情深者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "列车在一声长鸣中远去，小布袋里的救命钱让至亲在寒冷边陲买到了第一件厚羊皮坎肩，安然挺过首个严冬。",
                            "effect": {"wealth": -15, "family": 30, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "站台飞车塞钱救急手足，成为两地思念中最温情的支撑。"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "追车跑动中在湿滑站台台阶扭伤脚腕，目送列车消失在风雪地平线，心中满是悲壮与担忧。",
                            "effect": {"health": -15, "family": 25, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "送别至亲崴脚挂彩，一代青春记忆深深烙印。"
                        }
                    ]
                },
                {
                    "text": "服从纪律在后排站立克制情绪，响应号召大声领头呼喊欢送口号，不流半滴眼泪",
                    "choiceTags": ["时代：1950–1977", "年龄：16–65", "地域：火车站台", "门槛：克制坚毅者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "保持了积极庄重的政治觉悟，列车离去后独自在站台吸完半截劣质香烟，咽下所有酸楚。",
                            "effect": {"mentality": 10, "family": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "以沉毅冷峻外表送别亲人，内心深处锁住时代的沉重。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1950_1977_d4_gongshang_laoshi",
            "tier": "era",
            "title": "车间悼念：老八级机修师抢修设备因公殉职",
            "yearRange": [1955, 1976],
            "targetAge": [18, 55],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.07,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "在赶超生产指标的抢修过程中，由于防护简陋与长时间连轴转疲劳作业，工矿企业经常发生皮带绞伤、触电或重物坠落导致骨干师傅因公殉职。",
            "narrative": "防空警报声响彻车间，为排除主电机轴承过热事故，带了你五年的老八级机修师傅冲入狭窄地坑抢修，不幸被飞落的配重滑轮砸中胸膛壮烈牺牲。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "含泪主持灵堂守夜，接下师傅生前磨得发亮的老工具箱，并主动承担按月接济师娘孤幼的道义责任",
                    "choiceTags": ["时代：1950–1977", "年龄：18–55", "地域：工矿国企", "门槛：重师徒情深者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "师傅的工具箱陪伴你走过往后三十年工匠生涯，全厂上下赞誉你仁厚重义，师傅的技艺与精神由你完整传承。",
                            "effect": {"mentality": 35, "wealth": -10, "family": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "继承烈士师傅衣钵并赡养遗眷，赢得车间至高声望。",
                            "status": "status_craft_successor"
                        },
                        {
                            "type": "injured",
                            "weight": 10,
                            "log": "因连日守灵悲伤过度诱发急性胃出血，住院输液数天康复。",
                            "effect": {"health": -20, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "哀毁过礼伤及脾胃，但尽显赤子之心。"
                        }
                    ]
                },
                {
                    "text": "参加工会统一追悼会随大流默哀三分钟，随后全身心投入机床抢产以实际行动表忠诚",
                    "choiceTags": ["时代：1950–1977", "年龄：18–55", "地域：工矿国企", "门槛：恪尽职守者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "将悲痛化作动力完成双倍生产指标，获厂党委授予‘硬骨头标兵’奖状，按常规程序完成悼念。",
                            "effect": {"mentality": 15, "wealth": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "以工厂流水线标准节奏消化悲痛，步入正规劳模晋升轨道。"
                        }
                    ]
                }
            ]
        }
    ]
