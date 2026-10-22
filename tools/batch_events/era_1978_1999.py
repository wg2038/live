# -*- coding: utf-8 -*-
"""
1978–1999 改革开放与市场转轨时代：四大机制事件批次 (16条)
A. 路径补救 (高等教育自学考试逆袭、乡镇模具厂学徒拜师、托战友跨系统借调、周末夜大考取涉外会计)
B. 渐进伤害 (私营冲压厂压断指节瞒报、棉纺厂棉尘咳嗽硬挺、农田喷洒除草剂轻度中毒、工地生井水急性菌痢)
C. 经济诱惑 (闽浙民间标会互助会倒会崩盘、气功特异功能智商税、深圳排队抢购股票认购证、讲哥们义气担保连带债务)
D. 亲友离别 (双职工买断下岗患难与共、借钱筹路费连夜奔丧、老宅动迁兄弟分家反目、站台目送好友南下闯特区)
"""

def get_events():
    return [
        # --- A. 路径补救 ---
        {
            "id": "evt_1978_1999_a1_dianda_gaokao",
            "tier": "era",
            "title": "逆光苦读：高等教育自学考试攻取专科文凭",
            "yearRange": [1981, 1998],
            "targetAge": [20, 38],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "1981年国家首创高等教育自学考试（自考），为数千万未能通过高考全日制录取的落榜青年、在职职工提供国家承认学历的进修通道，通过率约15%-25%。",
            "narrative": "白天在工厂机床前站满八小时，夜晚在单身宿舍借着走廊灯光猛啃厚厚的《政治经济学》与《哲学原理》。今年已通过了九门统考，距离拿到专科大红文凭只差最后三门。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "推掉所有周末牌局与聚餐，连续六个月每晚苦读至凌晨一点，志在必得冲刺全科通过",
                    "choiceTags": ["时代：1978–1999", "年龄：20–38", "地域：全国城乡", "门槛：无全日制大专文凭者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 82,
                            "log": "查分单公布全部在七十分以上！你昂首走上台阶领到了省自考委颁发的大专毕业证书，转年顺利转为干部编制调入企管科。",
                            "effect": {"mentality": 35, "wealth": 25, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "靠自学考试顽强斩获国家承认大专学历，完成人生阶层重要跨越。",
                            "status": "status_college_diploma"
                        },
                        {
                            "type": "injured",
                            "weight": 18,
                            "log": "长期熬夜浓茶刺激导致严重神经衰弱与急性十二指肠溃疡，虽文凭到手但吃药调理了大半年。",
                            "effect": {"health": -20, "mentality": 20, "wealth": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "拼命自考耗损脾胃与睡眠质量，落下慢性胃疾。"
                        }
                    ]
                },
                {
                    "text": "觉得自考文凭不如铁饭碗实在，放弃最后几门考试，把精力转去厂外兼职倒腾小百货",
                    "choiceTags": ["时代：1978–1999", "年龄：20–38", "地域：全国城乡", "门槛：急功近利者"],
                    "outcomes": [
                        {
                            "type": "redirected",
                            "weight": 100,
                            "log": "自学考试中途弃考，小百货摆摊虽赚得三五百元零花，但在九十年代定岗评级时因缺少文凭未能转正。",
                            "effect": {"wealth": 15, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "半途荒废自考学业，错失转干关键资格。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_a2_xiangzhen_xietu",
            "tier": "era",
            "title": "落榜转轨：投奔乡镇五金模具厂拜师学艺",
            "yearRange": [1983, 1996],
            "targetAge": [17, 25],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_college_student"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "改革开放初期江浙、广东乡镇企业与‘星期天工程师’崛起，大量高考落榜农村青年投奔模具、注塑、五金小厂拜师，靠一身硬技术成长为民营实业骨干。",
            "narrative": "高考榜上无名，老父亲借来自行车把你带到邻乡新兴的模具厂。机床轰鸣油烟弥漫，从国企退休的技术厂长扫了你一眼，问你吃不吃得了手上长厚茧的苦头。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "当场递烟磕头认师父，立志把冲压模与线切割机床彻底摸透，甘心打杂学艺两年",
                    "choiceTags": ["时代：1978–1999", "年龄：17–25", "地域：沿海乡镇", "门槛：初高中毕业生"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "冬夏不辍，你不仅学会了手工装配精密冲压模，还能看懂复杂的机械装配图纸，两年后成为厂里顶梁柱开出千元月薪。",
                            "effect": {"wealth": 30, "mentality": 25, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "在乡镇制造业黄金期习得精密模具核心技术，开辟实业致富坦途。",
                            "status": "status_craft_successor"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "装配模具时手指被沉重滑块夹破指甲缝出血，由师父上药包扎，带伤坚持学会了整套工序。",
                            "effect": {"health": -10, "wealth": 20, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "学徒受伤磨练心性，奠定扎实技术功底。"
                        }
                    ]
                },
                {
                    "text": "嫌弃民营小作坊又脏又累且没有劳保，拒绝当学徒，回村帮家里继续承包田插秧",
                    "choiceTags": ["时代：1978–1999", "年龄：17–25", "地域：沿海乡镇", "门槛：求安稳守土者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "守在几亩责任田里面朝黄土背朝天，虽然粮食产量连年上升，但始终未能分享到工业化的高额利润红利。",
                            "effect": {"wealth": 5, "mentality": -5, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "拒绝进厂学艺错过乡镇工业化浪潮，固守小农传统。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_a3_tuo_jiediao",
            "tier": "era",
            "title": "人脉运作：托老战友关系跨系统借调进城",
            "yearRange": [1980, 1993],
            "targetAge": [24, 45],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.07,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "计划经济向市场经济转轨期间体制流动存在壁垒，偏远林场、农机站干部常利用战友、知青战线‘借调’、‘商调’至县市级物资局、商业局完成身份进城。",
            "narrative": "在偏僻的大山林场工作了八年，孩子眼看就要到上小学的年龄。老部队的老战友如今在县物资局当科长，私下表示只要备足土特产并按政策走，可以办借调。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "带上深山野蜂蜜与鹿茸登门拜会老班长，诚恳托付，并回单位耐心跑妥两地商调函",
                    "choiceTags": ["时代：1978–1999", "年龄：24–45", "地域：山区林场", "门槛：有退伍或体制资历者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "借调函与组织调令顺利下发，全家户口迁入县城，分配到县物资局机关大院职工宿舍，孩子如愿进入县一小。",
                            "effect": {"family": 35, "wealth": 20, "mentality": 30},
                            "isFatal": False,
                            "hiddenRiskLog": "借助战友战线完成关键调动迁徙，全家彻底跳出大山深处。",
                            "status": "status_urban_settled"
                        },
                        {
                            "type": "entangled",
                            "weight": 15,
                            "log": "原林场场长卡壳拖延大半年不肯放人，多方送烟送茶协调方得成行，耗费不少心力盘缠。",
                            "effect": {"wealth": -15, "mentality": -10, "family": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "调动审批阻力重重，虽成行但深感人情世故盘剥。"
                        }
                    ]
                },
                {
                    "text": "顾虑送礼求人有违原则，心想深山空气好衣食无忧，索性打消调动念头留在林场",
                    "choiceTags": ["时代：1978–1999", "年龄：24–45", "地域：山区林场", "门槛：清高不愿求人者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "继续在林区巡山护林，生活宁静自足，但数年后随林业停伐改制面临转岗压力，孩子教育也明显落后于城镇。",
                            "effect": {"mentality": 5, "health": 10, "family": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "恪守清高放弃进城契机，后代教育资源相对受限。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_a4_yeda_waiyu",
            "tier": "era",
            "title": "时代潮头：周末夜校恶补涉外经贸与财会",
            "yearRange": [1988, 1999],
            "targetAge": [19, 35],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "沿海对外开放与合资企业浪潮下，懂英文函电、现代借贷记账法的涉外财会人员严重紧缺，各大高校夜大与职工进修班学费昂贵但门庭若市。",
            "narrative": "特区外贸公司贴出招聘启事，月薪开到惊人的八百元加奖金，但必须熟练掌握外贸英文函电与电脑电算化。你站在涉外培训班招生简章前，学费要整整两个月工资。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "咬牙交纳两个月工资报名夜大周末班，买来收录机天天跟着许国璋英语磁带反复跟读练习",
                    "choiceTags": ["时代：1978–1999", "年龄：19–35", "地域：沿海城市", "门槛：有一定英语基础者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "一年后考取外贸会计资格证书并在面试中流利解答信用证流程，成功跳槽合资公司担任总账会计，月薪翻倍。",
                            "effect": {"wealth": 40, "mentality": 30, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "前瞻性学习涉外财经技能，搭上九十年代外贸经济腾飞快车。",
                            "status": "status_white_collar"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "白天上班晚上看盘带耳机音量过大引发持续性耳鸣，伴随轻微偏头痛，但总算拿下证书。",
                            "effect": {"health": -15, "wealth": 25, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "突击听磁带落下轻微听觉疲劳旧疾。"
                        }
                    ]
                },
                {
                    "text": "认为外国话太拗口学不会，把学费省下来存入银行吃保值储蓄高利息",
                    "choiceTags": ["时代：1978–1999", "年龄：19–35", "地域：沿海城市", "门槛：保守存钱者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "拿着稳定的存单吃利息，日子平稳无波，但十年后看着当年报班的同事纷纷买房买车，心中难免落寞。",
                            "effect": {"wealth": 10, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "选择守成规避学习风险，错失涉外高薪红利窗口。"
                        }
                    ]
                }
            ]
        },

        # --- B. 渐进伤害与可错选项 ---
        {
            "id": "evt_1978_1999_b1_chongya_shangshou",
            "tier": "era",
            "title": "安全脱节：私营五金厂冲床连冲压伤指节",
            "yearRange": [1985, 1999],
            "targetAge": [18, 50],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "八九十年代珠三角、长三角乡镇民营五金冲压厂多采用脚踏连冲老式机械，无红外安全光电保护装置，工人工伤断指（被称为‘断指之城’现象）频发。",
            "narrative": "为赶外贸交货期连续加班十四个小时，眼皮沉重。脚下一踩踏板，冲床滑块猛然连冲砸下，右手食指指端一阵剧烈钻心剧痛，机床上鲜血狂溅！",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "听信老板‘别闹大包两千私了’的劝说，由工友骑摩托送往无证黑诊所做简单缝合包扎",
                    "choiceTags": ["时代：1978–1999", "年龄：18–50", "地域：民营工业园", "门槛：私了息事宁人者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 75,
                            "log": "黑诊所未规范清创导致骨髓炎坏疽，最终食指被迫截除末节指骨，两千元医药费很快花光，右手握力大减。",
                            "effect": {"health": -35, "wealth": 10, "mentality": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "私了黑诊所处置不当致骨髓炎截指，留下永久性手部残疾。",
                            "status": "sequelae_motor_impairment"
                        },
                        {
                            "type": "safe",
                            "weight": 25,
                            "log": "所幸未伤及指骨中节，黑诊所草药包扎后侥幸未感染，留下一截短粗畸形指头，勉强能捏拿物品。",
                            "effect": {"health": -15, "wealth": 15, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "断指虽留畸形但勉强保全关节功能。"
                        }
                    ]
                },
                {
                    "text": "断然拒绝私了，找来红领巾包扎断指，坚持叫救护车直奔市骨科医院做断指显微再植手术",
                    "choiceTags": ["时代：1978–1999", "年龄：18–50", "地域：民营工业园", "门槛：懂显微外科维权者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "显微外科专家在显微镜下吻合微小动静脉与神经，再植指完全成活，经劳动仲裁由厂方全额赔付医疗费与停工工资。",
                            "effect": {"health": -5, "wealth": 20, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "依靠现代显微外科成功挽回断指，依法维权获全额赔偿。"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "血管痉挛虽接活但指尖感觉神经迟钝，遇冷则苍白发麻，厂方老板怀恨在心事后将你辞退。",
                            "effect": {"health": -15, "wealth": -10, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "再植成活但指端麻木，且面临劳资关系破裂失业转岗。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_b2_fangzhi_feibing",
            "tier": "era",
            "title": "职业暗疾：棉纺织厂清花车间长期咳嗽胸闷",
            "yearRange": [1980, 1996],
            "targetAge": [20, 50],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "纺织工业八十年代常年三班倒，清花、梳棉车间棉尘飞扬，工人虽配发白纱布口罩，但长期吸入棉尘内毒素易患‘棉尘病’（纺织工人哮喘）。",
            "narrative": "清花车间里空中弥漫着肉眼可见的白棉绒絮。每到周一上班就胸闷憋气、干咳不止，工友笑称这是‘星期一综合征’，但最近咳出的痰里已有黑丝与血星。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "觉得这是纺织工的家常便饭，每天猛灌甘草片和自熬川贝雪梨膏硬挺，拒绝调岗降薪",
                    "choiceTags": ["时代：1978–1999", "年龄：20–50", "地域：轻纺工业城市", "门槛：贪恋挡车工高津贴者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 75,
                            "log": "棉尘内毒素引起永久性气道不可逆重塑，转为慢性阻塞性肺疾病，一爬三楼就气喘吁吁，体力大打折扣。",
                            "effect": {"health": -30, "wealth": 15, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "忽视职业病早期信号硬扛，致慢性不可逆肺气肿损伤。",
                            "status": "sequelae_respiratory"
                        },
                        {
                            "type": "safe",
                            "weight": 25,
                            "log": "自身呼吸道纤毛屏障较好，配合甘草调理勉强控制了进展，维持在轻微慢性咳嗽水平。",
                            "effect": {"health": -10, "wealth": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "呼吸系统轻微受累但未发生急性恶化。"
                        }
                    ]
                },
                {
                    "text": "拿着胸片找厂医开具职业病诊断证明，坚决申请调离高粉尘车间去成品包装仓库",
                    "choiceTags": ["时代：1978–1999", "年龄：20–50", "地域：轻纺工业城市", "门槛：健康优先理智者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 92,
                            "log": "调离粉尘污染环境后肺功能逐步逆转止咳，虽然每月少了二十元特殊粉尘津贴，但身体彻底保全。",
                            "effect": {"health": 15, "wealth": -10, "mentality": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "果断脱离粉尘危害环境，斩断职业肺病致残链条。"
                        },
                        {
                            "type": "injured",
                            "weight": 8,
                            "log": "仓库老员工排挤新人，多干了不少搬运重活，但空气清新让人心安。",
                            "effect": {"health": 5, "mentality": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "转岗带来短暂人际适应成本。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_b3_nongyao_zhongdu",
            "tier": "era",
            "title": "盛夏劳作：背喷雾器喷百草枯轻微渗透中毒",
            "yearRange": [1988, 1999],
            "targetAge": [18, 65],
            "applicableRegions": ["RURAL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "九十年代百草枯等灭生性除草剂在农村广泛推广，农民烈日下赤膊背喷雾器打药，药液经常顺着背带渗漏腐蚀后背皮肤造成局部吸收中毒与溃烂。",
            "narrative": "酷暑三十八度烈日下，你光着膀子背着漏药水的铁皮农药喷雾器给柑橘园除草。药液渗入破背心，后背整片皮肤灼痛如被火烧，泛起大片黄水泡并头晕心慌。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "随手抓一把河滩青泥擦抹后背，大口灌下冰冷井水，咬牙先把剩下的两亩药水打完",
                    "choiceTags": ["时代：1978–1999", "年龄：18–65", "地域：广大农村", "门槛：盲目蛮干硬扛者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 75,
                            "log": "高浓度除草剂经大面积溃破皮肤吸收损害肺脏与肝脏，后背整块皮肤溃烂化脓，发烧十天留下巴掌大增生性疤痕。",
                            "effect": {"health": -35, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "百草枯皮肤吸收并发严重接触性皮炎与肺损伤隐患。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "fatal",
                            "weight": 3,
                            "log": "大量吸收除草剂引发进行性迟发性肺间质纤维化，呼吸衰竭抢救无效离世。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "农药大面积皮肤吸收延误抢救致肺纤维化罹难。"
                        },
                        {
                            "type": "safe",
                            "weight": 22,
                            "log": "自身排毒强侥幸未累及脏器，后背烂皮脱落换上一层黑硬老茧，免于大劫。",
                            "effect": {"health": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "除草剂皮肤灼伤侥幸未致内脏衰竭。"
                        }
                    ]
                },
                {
                    "text": "扔掉喷雾器立刻跳入水渠彻底冲刷全身半小时，换上干净衣服急赴县医院皮肤科做酸碱中和抗毒治疗",
                    "choiceTags": ["时代：1978–1999", "年龄：18–65", "地域：广大农村", "门槛：具备化学防护常识者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "大量流动清水清洗彻底去除了表皮农药残留，外用紫草油与烧伤膏一周结痂平整，未引起全身中毒。",
                            "effect": {"health": 5, "wealth": -10, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "黄金时间内大量清水冲洗阻断农药透皮吸收，彻底转危为安。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "背部留下一小块淡褐色色素沉着，无任何功能影响。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "轻微色素沉着无碍大局。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_b4_shui_liji",
            "tier": "era",
            "title": "夏令暴饮：工地生饮生冷压水井水急性菌痢",
            "yearRange": [1982, 1998],
            "targetAge": [16, 65],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "八九十年代城乡结合部建筑工地与打工棚饮水卫生条件简陋，志贺氏痢疾杆菌随浅层压水井污染水源，极易造成民工群发性黏液脓血便与重度脱水。",
            "narrative": "高温四十度在脚手架上扎钢筋汗如雨下，工地大锅绿豆汤早被抢空。你扑到老式压水井旁连按压杆，对着冰凉甘冽的生井水狂饮了整整半铁瓢。半夜腹内如绞肉机翻滚。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "觉得肚痛拉肚子只是受凉，吞服两瓣生大蒜和几粒去痛片，蒙头硬撑继续上工",
                    "choiceTags": ["时代：1978–1999", "年龄：16–65", "地域：建筑工地", "门槛：土法抗痢疾硬挺者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 70,
                            "log": "止痛片掩盖病情，痢疾杆菌在结肠大量繁殖脱落黏膜形成假膜，剧烈里急后重便脓血十余次，休克晕倒在脚手架上送医抢救大伤元气。",
                            "effect": {"health": -35, "wealth": -15, "mentality": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "盲信生大蒜硬扛急性菌痢延误治疗致败血休克。",
                            "status": "sequelae_vitality_drain"
                        },
                        {
                            "type": "fatal",
                            "weight": 2,
                            "log": "中毒型细菌性痢疾突发脑水肿抽搐昏迷，在救护车转院途中不幸衰竭离世。",
                            "effect": {},
                            "isFatal": True,
                            "hiddenRiskLog": "重度中毒性菌痢延误输液治疗殒命。"
                        },
                        {
                            "type": "safe",
                            "weight": 28,
                            "log": "凭借自身极强的消化道抗体，连拉两天稀水后居然慢慢自限痊愈，虚汗淋漓。",
                            "effect": {"health": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "强壮体魄硬涉险关自愈脱险。"
                        }
                    ]
                },
                {
                    "text": "立即停工请假，叫工友陪同就近前往镇卫生院化验大便，遵医嘱口服诺氟沙星（氟哌酸）并静脉输注糖盐水",
                    "choiceTags": ["时代：1978–1999", "年龄：16–65", "地域：建筑工地", "门槛：及时规范就医者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "喹诺酮类抗生素精准杀灭痢疾杆菌，两瓶补液迅速纠正水电解质紊乱，次日腹痛全消，三天后体力生龙活虎如初。",
                            "effect": {"health": 5, "wealth": -10, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "科学使用特效抗菌药与补液，闪电化解急性菌痢危机。"
                        },
                        {
                            "type": "injured",
                            "weight": 5,
                            "log": "输液部位出现轻度静脉炎红肿，硫酸镁湿敷后消退。",
                            "effect": {"health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "输液轻微静脉刺激无后患。"
                        }
                    ]
                }
            ]
        },

        # --- C. 经济系统与诱惑 ---
        {
            "id": "evt_1978_1999_c1_minjian_biaohui",
            "tier": "era",
            "title": "民间借贷：闽浙民间标会互助会崩盘倒会",
            "yearRange": [1986, 1998],
            "targetAge": [22, 60],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "改革开放民营经济早期银行贷款难，沿海盛行互助性的民间标会（摇会、互助会）。部分会头以高达两三分月息非法集资，倒会跑路潮频发，导致大量家庭半生积蓄化为乌有。",
            "narrative": "街坊邻里都在热烈讨论某某做会头组织十万元大标会，月息高达两分五厘。会头是看着你长大的表叔，极力劝你拿出存单入会当会脚，一年稳赚大半年工资。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "取出全家三年储蓄一万元投入标会，期盼利滚利三年后买一间街面商铺",
                    "choiceTags": ["时代：1978–1999", "年龄：22–60", "地域：沿海工商业带", "门槛：贪图民间高息者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 75,
                            "log": "不到半年下游会脚链条断裂，会头半夜携款潜逃不知所踪！数十受害群众围堵哭天抢地，你的一万元老本血本无归，全家抱头痛哭。",
                            "effect": {"wealth": -50, "mentality": -35, "family": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "陷入民间标会倒会骗局，全家半生积蓄荡然无存。",
                            "status": "status_debt_burdened"
                        },
                        {
                            "type": "safe",
                            "weight": 25,
                            "log": "在崩盘前夕敏锐察觉会头买豪宅苗头，提前以微亏利息抢标退会套现，惊险保全本金并小赚千元。",
                            "effect": {"wealth": 25, "mentality": 25},
                            "isFatal": False,
                            "hiddenRiskLog": "在民间标会风暴来临前精准逃顶，保全财富。"
                        }
                    ]
                },
                {
                    "text": "牢记‘贪高息吃大亏’古训，坚决拒绝亲戚劝诱，将积蓄老老实实锁在国有银行定存",
                    "choiceTags": ["时代：1978–1999", "年龄：22–60", "地域：沿海工商业带", "门槛：克制本分稳健者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "数月后该标会轰然爆雷牵连全村半数人家，你家存款分文未损安稳如初，邻里无不佩服你的定力。",
                            "effect": {"mentality": 25, "wealth": 10, "family": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "坚拒民间非法集资高息诱惑，守住家庭财务底线。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_c2_qigong_zhishangshui",
            "tier": "era",
            "title": "特异狂潮：气功大师带功报告与信息锅热卖",
            "yearRange": [1985, 1995],
            "targetAge": [20, 65],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": [],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "八九十年代全国泛滥‘气功热’，所谓严新、张香玉等大师在体育馆召开万人带功报告会，售卖铝锅改造的‘信息感应锅’、录音带，敛财数以亿计。",
            "narrative": "市工人文化宫体育馆挤满了数千名头顶铝锅的人群，号称能接收宇宙高能信息包治百病。门票炒到五十元一张，推销员围着你称购买一套大师亲笔开光的功法磁带可延寿三十年。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "跟风花去整月工资买下信息铝锅和三盘功法录音带，回家每夜头顶铝锅打坐晃脑练功",
                    "choiceTags": ["时代：1978–1999", "年龄：20–65", "地域：全国城市", "门槛：盲信伪科学气功者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 70,
                            "log": "自我催眠导致剧烈精神恍惚幻听‘气冲脑门’，出现严重神经官能症夜不能寐，被家属送精神专科门诊服药纠偏，白白损失巨款。",
                            "effect": {"wealth": -25, "mentality": -30, "health": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "盲信伪气功走火入魔损伤身心健康，缴足时代智商税。",
                            "status": "sequelae_mental_trauma"
                        },
                        {
                            "type": "safe",
                            "weight": 30,
                            "log": "权当茶余饭后散步拉伸锻炼，未陷太深，不久气功大师卷款潜逃案发，自嘲一笑将铝锅拿回厨房炖肉。",
                            "effect": {"wealth": -15, "mentality": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "轻微破财但及时清醒止损。"
                        }
                    ]
                },
                {
                    "text": "指责其纯属江湖装神弄鬼骗局，捂紧钱包转身离开会场，买了一套正规科普十万个为什么给孩子",
                    "choiceTags": ["时代：1978–1999", "年龄：20–65", "地域：全国城市", "门槛：崇尚唯物科学者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "理智守护了家庭钱袋子，几年后该类伪科学组织被国家依法取缔，你的唯物主义理性在邻里间树立了清醒威信。",
                            "effect": {"mentality": 25, "family": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "秉持科学理性抵制封建迷信气功潮，家庭家风严正。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_c3_yuanshi_gupiao",
            "tier": "era",
            "title": "资本狂澜：1992深圳排队抢购股票认购证",
            "yearRange": [1992, 1993],
            "targetAge": [20, 55],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 6,
            "factLevel": "确证",
            "historicalFact": "1992年8月深圳‘8·10’风波，全国上百万人涌入深圳排队抢购新股认购抽签表，认购表倒卖价格飙升十倍，酿成中国资本市场建立初期的狂热狂欢与阵痛。",
            "narrative": "深圳体育场门口下着瓢泼大雨，数十万人前胸贴后背在铁栏杆前连轴排队两天两夜。有人开价五百元当场收购你手中的白条抽签表，也可以自己留着博取新股上市暴利。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "咬牙在暴雨人海中死守，凭两千元老本买下二十张认购表，全部拿去抽签认购新股上市",
                    "choiceTags": ["时代：1992–1993", "年龄：20–55", "地域：特区金融前线", "门槛：敢闯敢赌资本市场者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 65,
                            "log": "抽签高中五张！新股上市当天暴涨四倍抛出，净赚三万多元巨资，瞬间成为人均羡慕的‘万元户’！",
                            "effect": {"wealth": 60, "mentality": 35, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "抓住特区股票认购证历史红利豪取第一桶金，实现资本原始积累。"
                        },
                        {
                            "type": "injured",
                            "weight": 35,
                            "log": "在排队拥挤中被踩伤右脚踝，且因舞弊抽签未中几张，高价认购表大半亏损，仅剩一身泥水。",
                            "effect": {"health": -20, "wealth": -25, "mentality": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "盲目狂热追高股票认购证踩踏负伤亏损。"
                        }
                    ]
                },
                {
                    "text": "排到两张表后见好就收，转手加价八百元倒卖给队尾收表的炒家，揣着净利润迅速离场回旅社睡觉",
                    "choiceTags": ["时代：1992–1993", "年龄：20–55", "地域：特区金融前线", "门槛：落袋为安谨慎客"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "轻松赚到相当于大半年工资的八百元现金落袋为安，避开了随后的骚乱与踩踏，舒舒服服坐火车返乡。",
                            "effect": {"wealth": 25, "mentality": 20, "health": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "适度套现落袋为安，规避了狂热泡沫后期的踩踏风险。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_c4_danbao_liandai",
            "tier": "era",
            "title": "人情枷锁：为同乡做生意经营贷款签字担保",
            "yearRange": [1990, 1999],
            "targetAge": [24, 60],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 8,
            "factLevel": "确证",
            "historicalFact": "九十年代下海经商潮中信用体系薄弱，信用社与商业银行多采用联保或熟人担保制度，一人经营失败跑路常导致无辜担保人全额承担连带清偿责任。",
            "narrative": "一起长大的发小下海开办建材批发部，拿着农行五万元贷款申请书登门，称万事俱备只差一个在国企有正式工作的体制内人员签字做连带责任担保。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "碍于多年情面与两瓶好酒，看都没看合同条款就在连带责任保证人一栏签上大名并按上手印",
                    "choiceTags": ["时代：1978–1999", "年龄：24–60", "地域：全国各地", "门槛：抹不开面子讲哥们义气者"],
                    "outcomes": [
                        {
                            "type": "entangled",
                            "weight": 75,
                            "log": "发小因投机失败血本无归举家连夜跑路不知所踪！法院直接查封冻结你的月工资卡按月抵债，家庭陷入长达数年的拮据窘境。",
                            "effect": {"wealth": -45, "mentality": -35, "family": -20},
                            "isFatal": False,
                            "hiddenRiskLog": "盲目为人情担保背负巨额连带死债，工资遭长期扣押。",
                            "status": "status_debt_burdened"
                        },
                        {
                            "type": "safe",
                            "weight": 25,
                            "log": "发小建材部赶上城市大拆迁赚了大钱，三年后如期本息还清银行并送你一套红木大衣柜酬谢，虚惊一场。",
                            "effect": {"wealth": 20, "family": 15, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "侥幸涉险过关未遭连带爆雷。"
                        }
                    ]
                },
                {
                    "text": "哪怕被发小痛骂‘忘恩负义不近人情’，也坚决守住底线只借五百元现金资助，绝不签字担保",
                    "choiceTags": ["时代：1978–1999", "年龄：24–60", "地域：全国各地", "门槛：法律意识清醒者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "虽然得罪了发小断了往来，但一年后该发小欠债失联数十担保人遭法院起诉执行，你安居乐业保全了自家全部资产。",
                            "effect": {"mentality": 25, "wealth": 10, "family": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "坚守法律财务边界拒绝连带担保，保全家庭长治久安。"
                        }
                    ]
                }
            ]
        },

        # --- D. 亲友关系网与离别 ---
        {
            "id": "evt_1978_1999_d1_xiagang_fufu",
            "tier": "era",
            "title": "潮落共担：国企重组双职工买断下岗自谋出路",
            "yearRange": [1995, 1999],
            "targetAge": [30, 52],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.09,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "1990年代中后期国企深化改革‘减员增效’，全国累计约三千万产业工人下岗分流。双职工家庭同时失去铁饭碗，夫妻搭伙摆地摊、开早点铺成为时代悲壮剪影。",
            "narrative": "厂大会宣布全厂关停并转，夫妻两人同一天领到了按工龄计算的买断补偿金。站在冷清紧闭的厂大门外，看着手里的下岗优惠证，孩子正值初中交学费当口。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "夫妻同心其利断金，拿出两千元买下二手人力三轮车和铁皮煤炉，清晨四点出摊卖油条豆浆",
                    "choiceTags": ["时代：1978–1999", "年龄：30–52", "地域：老工业基地", "门槛：能屈能伸自强自立者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 85,
                            "log": "起早贪黑双手炸起老茧，油条分量足赢得居民口碑，每天进账四五十元超过原工厂工资，全家昂首挺胸杀出一条血路！",
                            "effect": {"wealth": 30, "family": 35, "mentality": 30, "health": -5},
                            "isFatal": False,
                            "hiddenRiskLog": "下岗逆境中夫妻相濡以沫自力更生，摆脱铁饭碗依赖实现创业生存。",
                            "status": "status_self_employed"
                        },
                        {
                            "type": "injured",
                            "weight": 15,
                            "log": "热油锅溅起烫伤手臂，又逢城管驱赶扣押三轮车，抱头痛哭后在亲友资助下重新租了正规店面。",
                            "effect": {"health": -15, "wealth": -10, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "个体摆摊饱经波折但淬炼家庭坚韧品格。"
                        }
                    ]
                },
                {
                    "text": "放不下昔日国企老大哥面子，成天窝在家里借酒浇愁互相埋怨，指责厂长政策不公",
                    "choiceTags": ["时代：1978–1999", "年龄：30–52", "地域：老工业基地", "门槛：怨天尤人者"],
                    "outcomes": [
                        {
                            "type": "injured",
                            "weight": 100,
                            "log": "微薄买断金坐吃山空，夫妻天天因柴米油盐爆发激烈争吵甚至动手，生活陷入持久绝望与抑郁。",
                            "effect": {"wealth": -30, "family": -35, "mentality": -35, "health": -15},
                            "isFatal": False,
                            "hiddenRiskLog": "消极对抗下岗现实导致家庭关系破裂陷入贫困陷阱。",
                            "status": "status_asset_wiped"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_d2_bensang_panchan",
            "tier": "era",
            "title": "千里奔丧：四处借凑四十元车票赶回老家送终",
            "yearRange": [1980, 1995],
            "targetAge": [20, 55],
            "applicableRegions": ["ALL"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_orphan"],
            "triggerProbability": 0.08,
            "coolingPeriod": 12,
            "factLevel": "确证",
            "historicalFact": "绿皮火车时代跨省交通费用对普通工薪族是沉重开销，一张跨省硬座票相当于普通人半月工资。长辈离世发来‘母病危速归’急电，常需借凑差旅费连夜奔丧。",
            "narrative": "电报局敲开门递上一张加急电报，上面仅有‘父病危速归’五个字。口袋里只剩七块五毛钱，而回老家的慢车硬座票加转大巴要整整四十元。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "连夜敲开全楼三家邻居与车间主任房门借齐四十元，直扑火车站跳上最近一班绿皮慢车",
                    "choiceTags": ["时代：1978–1999", "年龄：20–55", "地域：全国各地", "门槛：至孝急迫者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 90,
                            "log": "站立颠簸三十个小时终于在咽气前半小时赶到父亲床头，紧握住老人的手听完最后叮嘱，尽了人子大孝。",
                            "effect": {"wealth": -20, "mentality": 20, "family": 30, "health": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "借钱千里奔丧见上最后一面，人生无悔无憾。",
                            "status": "status_bereaved_parent"
                        },
                        {
                            "type": "injured",
                            "weight": 10,
                            "log": "长途拥挤硬座双腿严重水肿，因极度悲痛在灵堂昏厥脱水，经乡村医生注射葡萄糖苏醒。",
                            "effect": {"health": -25, "wealth": -25, "mentality": 10},
                            "isFatal": False,
                            "hiddenRiskLog": "奔丧劳顿哀毁过礼伤及身躯。"
                        }
                    ]
                },
                {
                    "text": "嫌借钱丢人又自认火车太慢赶不上，只拍了一份加急汇款单与唁电回乡，自己留在原地照常上班",
                    "choiceTags": ["时代：1978–1999", "年龄：20–55", "地域：全国各地", "门槛：冷漠算计者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "虽然省下了差旅费与人情借条，但未能送老父最后一程成为心头永远结疤的死穴，遭族人冷眼痛斥。",
                            "effect": {"wealth": 10, "family": -35, "mentality": -30},
                            "isFatal": False,
                            "hiddenRiskLog": "因盘缠吝啬缺席至亲葬礼，铸成终生不可挽回之道德痛悔。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_d3_zhengchan_fenjia",
            "tier": "era",
            "title": "老宅动迁：手足同胞因分房平方尺数闹上法庭",
            "yearRange": [1989, 1999],
            "targetAge": [28, 62],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "九十年代城市旧城改造大拆迁启动，原按人头福利分房或老私房折算回迁面积，手足兄弟常因赡养义务与户口留存产生激烈博弈乃至反目成仇。",
            "narrative": "父母留下的三间老瓦房面临市政拓宽动迁，可置换两套两居室安置房。三个同胞兄弟姐妹聚集在逼仄客堂里，为了谁当年照顾老人多、谁户口在老宅争吵不休大拍桌子。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "寸步不让，聘请律师搜集多年水电赡养单据对簿公堂，誓死捍卫自己应得的一套房产产权",
                    "choiceTags": ["时代：1978–1999", "年龄：28–62", "地域：城市动迁区", "门槛：据理力争维权者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 70,
                            "log": "法院一审判决你胜诉获得独立一套套房产权！虽拿到了遮风避雨的红本房产，但与哥嫂弟妹彻底断绝往来老死不相往来。",
                            "effect": {"wealth": 50, "family": -40, "mentality": -10},
                            "isFatal": False,
                            "hiddenRiskLog": "依法捍卫合法房产产权，代价是亲情网络彻底撕裂碎解。"
                        },
                        {
                            "type": "entangled",
                            "weight": 30,
                            "log": "官司拉锯三年耗费万余元诉讼费，最终两败俱伤按比例折中折价，亲人变成仇家。",
                            "effect": {"wealth": 10, "family": -45, "mentality": -25},
                            "isFatal": False,
                            "hiddenRiskLog": "家庭房产诉讼旷日持久身心俱疲。"
                        }
                    ]
                },
                {
                    "text": "念及骨肉同胞一脉相传，主动提议折价两万元补偿让给住房困难的弟弟，自己退保小户型",
                    "choiceTags": ["时代：1978–1999", "年龄：28–62", "地域：城市动迁区", "门槛：顾全亲情长兄风范者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "退一步海阔天空，弟弟全家感激涕零尊你为一家之主，家庭和睦如初，逢年过节阖家欢聚其乐融融。",
                            "effect": {"wealth": 20, "family": 40, "mentality": 30},
                            "isFatal": False,
                            "hiddenRiskLog": "以大度谦让化解手足争产死局，守住最珍贵的宗族亲情。"
                        }
                    ]
                }
            ]
        },
        {
            "id": "evt_1978_1999_d4_nanxia_bieyi",
            "tier": "era",
            "title": "站台目送：挚友辞去铁饭碗决然南下闯深圳",
            "yearRange": [1988, 1996],
            "targetAge": [22, 45],
            "applicableRegions": ["URBAN"],
            "exposureConditions": {},
            "preTags": [],
            "excludeTags": ["status_peasant_illiterate"],
            "triggerProbability": 0.08,
            "coolingPeriod": 10,
            "factLevel": "确证",
            "historicalFact": "邓小平南方谈话前后引发全国数十万体制内干部、知识分子‘孔雀东南飞’砸掉铁饭碗下海闯深圳特区，老火车站台送别成为时代转折的标志性缩影。",
            "narrative": "单位最有前途的年轻工程师挚友不顾领导挽留，毅然递交辞职信南下蛇口。昏黄的站台灯光下，他提着一口人造革皮箱，眼眶泛红握紧你的双手告别。",
            "isDecision": True,
            "passiveImpact": None,
            "choices": [
                {
                    "text": "掏出积攒的两个月工资塞进他口袋作为盘缠，并赠送他一本最新版《现代实用英汉词典》相约顶峰相见",
                    "choiceTags": ["时代：1978–1999", "年龄：22–45", "地域：火车站台", "门槛：真诚托举挚友者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 95,
                            "log": "五年后挚友在特区创业成功开办科技公司，特意寄来巨额股份期权邀请你南下合伙，当年一饭之恩铸成终身莫逆同盟！",
                            "effect": {"wealth": 30, "mentality": 35, "family": 20},
                            "isFatal": False,
                            "hiddenRiskLog": "倾力支持挚友时代下海壮举，未来收获惊人事业回报。"
                        },
                        {
                            "type": "entangled",
                            "weight": 5,
                            "log": "挚友在南下途中被人扒窃身无分文，幸得你接济的两月工资才在罗湖租下床位活了下来。",
                            "effect": {"wealth": -10, "mentality": 15},
                            "isFatal": False,
                            "hiddenRiskLog": "盘缠成为挚友异乡立足的救命稻草。"
                        }
                    ]
                },
                {
                    "text": "苦口婆心劝阻他留在体制内保铁饭碗，指责特区风大浪大搞不好就是盲流，劝阻无效后失望挥手",
                    "choiceTags": ["时代：1978–1999", "年龄：22–45", "地域：火车站台", "门槛：安于现状者"],
                    "outcomes": [
                        {
                            "type": "safe",
                            "weight": 100,
                            "log": "两人思想从此分道扬镳，你留在老体制安稳过完余生，昔日同窗在南方大风大浪中渐行渐远，再无共同话题。",
                            "effect": {"mentality": -5, "wealth": 5},
                            "isFatal": False,
                            "hiddenRiskLog": "观念分歧导致时代挚友情谊渐行渐远。"
                        }
                    ]
                }
            ]
        }
    ]
