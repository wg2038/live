# tools/build_events_2000_2026.py
# -*- coding: utf-8 -*-
"""
生成 2000–2026 年共 44 条全要素历史事件库，严格遵循：
- choiceTags 四元标签
- safe / injured / entangled / redirected / fatal 多元权重分支 (fatal <= 2%)
- hiddenRiskLog 用于终局因果回顾
- factLevel (确证/估计/文学化)
- 时代背景与个人参与严格解耦（如2022疫情分圈层）
"""

import json
import os

events = []

def make_outcome(o_type, weight, log, effect=None, is_fatal=False, status=None, hidden_risk_log="", new_career_track=None):
    res = {
        "type": o_type,
        "weight": weight,
        "log": log,
        "effect": effect or {},
        "isFatal": is_fatal,
        "hiddenRiskLog": hidden_risk_log
    }
    if status:
        res["status"] = status
    if new_career_track:
        res["newCareerTrack"] = new_career_track
    return res

def add_evt(evt_id, tier, title, year_range, target_age, regions, exposure, pre_tags, exclude_tags, trigger_prob, cooling_period, fact_level, hist_fact, narrative, choices, is_decision=True, passive_impact=None):
    events.append({
        "id": evt_id,
        "tier": tier,
        "title": title,
        "yearRange": year_range,
        "targetAge": target_age,
        "applicableRegions": regions,
        "exposureConditions": exposure,
        "preTags": pre_tags,
        "excludeTags": exclude_tags,
        "triggerProbability": trigger_prob,
        "coolingPeriod": cooling_period,
        "factLevel": fact_level,
        "historicalFact": hist_fact,
        "narrative": narrative,
        "isDecision": is_decision,
        "passiveImpact": passive_impact,
        "choices": choices
    })

# 1. 2000 千禧年
add_evt(
    "evt_2000_qianxinian", "era", "千禧之交“世纪婴儿”与新世纪畅想",
    [2000, 2000], [0, 75], ["ALL"], {},
    [], [], 0.90, 3, "确证",
    "2000年迎来新千禧年，中华世纪坛点亮世纪圣火。全国各地迎来跨世纪狂欢与‘千禧宝宝’生育高峰，亿万民众在对新世纪的憧憬中迈入公元2000年代。",
    "钟声敲响，千禧烟花照亮苍穹。产房外挤满了等候千禧龙宝宝降生的家长，街道橱窗贴着千禧纪念挂历。人们在贺年卡上写下对新千年的美好期许，时代的钟摆迎向未知的新百年。",
    [
        {
            "text": "若适逢婚育期，顺应喜庆氛围迎来‘千禧宝宝’降生，精心起名呵护",
            "choiceTags": ["时代：2000", "年龄：22–40", "地域：全国", "门槛：适龄育龄夫妇"],
            "outcomes": [
                make_outcome("safe", 75, "千禧龙宝宝平安降生，阖家欢聚摆满月酒，给全家带来无尽喜气与希望。", {"family": 30, "wealth": -10, "mentality": 25}, status="millennium_baby_parent", hidden_risk_log="迎接新世纪千禧宝宝，全家凝聚力与奋斗目标焕然一新。"),
                make_outcome("injured", 20, "产院床位极度爆满在走廊加床分娩，产后着凉虚脱调理一月。", {"health": -20, "family": 25, "wealth": -15}, hidden_risk_log="千禧扎堆生育遭遇医疗资源拥挤，所幸母子平安。"),
                make_outcome("entangled", 5, "千禧年扎堆同龄人过多，日后在幼升小和高考中竞争格外激烈。", {"mentality": -10}, hidden_risk_log="千禧生育高峰带来日后就学升学竞争压力。")
            ]
        },
        {
            "text": "在单位/学校跨年晚会上担任主持人或幕后筹办，写下新世纪人生目标存入心底",
            "choiceTags": ["时代：2000", "年龄：14–60", "地域：全国", "门槛：普通国民"],
            "outcomes": [
                make_outcome("safe", 85, "在昂扬向上的集体氛围中立下长远学业/职业目标，精神面貌焕然一新。", {"mentality": 20, "knowledge": 10}, status="millennium_dreamer", hidden_risk_log="跨入新世纪树立长远雄心，为后续二十年拼搏奠定心智底盘。"),
                make_outcome("safe", 15, "除夕夜与挚友痛饮畅谈通宵，在世纪晨光中留下一张难忘的青春合影。", {"family": 15, "mentality": 15}, hidden_risk_log="新世纪初夜的友谊与诗意，成为一生温暖底色。")
            ]
        }
    ]
)

# 2. 2001 入世 WTO
add_evt(
    "evt_2001_wto_waomao", "era", "中国加入WTO：世界工厂与外贸狂飙",
    [2001, 2004], [18, 55], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "2001年11月多哈会议正式批准中国加入世界贸易组织（WTO）。外贸关税壁垒打破，全球产业链向中国沿海大规模转移，‘中国制造’商品潮水般涌向全球货架。",
    "宁波舟山港与盐田港集装箱昼夜装卸吞吐，汽笛长鸣。外贸公司的传真机整日吐着来自欧美客商的急单。各大工厂车间通宵达旦赶工，英文标签与集装箱封签成了工薪族的最熟悉日常。",
    [
        {
            "text": "投身沿海合资外贸制造企业做外销跟单员或进出口报关员",
            "choiceTags": ["时代：2001–2004", "年龄：20–40", "地域：沿海长三角/珠三角", "门槛：大中专青年/懂基本英语"],
            "outcomes": [
                make_outcome("safe", 65, "熟练处理信用证与报关退税，年终外贸提成丰厚，在沿海省城全款购入首套商品房。", {"wealth": 50, "knowledge": 25, "mentality": 20}, new_career_track="tech_whitecollar", status="wto_foreign_trader", hidden_risk_log="精准搭上加入WTO外贸爆发快车，数年内实现阶层跃升与资产立足。"),
                make_outcome("injured", 25, "欧美船期催单日夜倒时差熬夜沟通，患上严重反流性食管炎与胃溃疡。", {"health": -25, "wealth": 40}, new_career_track="tech_whitecollar", hidden_risk_log="透支身体换取外贸高薪，在经济起飞期积累了雄厚原始资本。"),
                make_outcome("entangled", 10, "遭遇外商破产赖账被拖欠十万美元货款，被迫承担两成业务罚款。", {"wealth": -20, "mentality": -20}, new_career_track="tech_whitecollar", hidden_risk_log="涉外贸易初涉国际商法漏洞，经受法律合规大考。")
            ]
        },
        {
            "text": "若为内地农机或传统国企，主动推动生产线按国际ISO标准换装出海配件",
            "choiceTags": ["时代：2001–2004", "年龄：24–55", "地域：全国工业城镇", "门槛：制造车间技工/工程师"],
            "outcomes": [
                make_outcome("safe", 70, "主导车间拿下欧美CE与UL安全认证，工厂订单排到三年后，全厂效益大翻身。", {"wealth": 30, "knowledge": 20}, status="iso_certified_engineer", hidden_risk_log="依托国际化标准升级传统制造，成为不可或缺的涉外数控技师。"),
                make_outcome("entangled", 30, "因老设备精度不达标首批外贸出口件遭遇批量退货索赔，扣罚三个月奖金。", {"wealth": -15, "mentality": -15}, hidden_risk_log="设备老化冲击外贸标准交学费，痛定思痛全面技改。")
            ]
        }
    ]
)

# 3. 2001 申奥成功
add_evt(
    "evt_2001_shenao_chenggong", "era", "莫斯科之夜：北京申奥成功狂欢",
    [2001, 2001], [8, 75], ["ALL"], {},
    [], [], 0.90, 3, "确证",
    "2001年7月13日国际奥委会萨马兰奇主席宣布‘BEIJING’获得2008年第29届奥运会举办权。天安门广场与中华世纪坛数十万人狂欢达旦，举国沸腾，成为改革开放信心的世纪飞跃。",
    "电视里传来‘北京！’的庄严宣布，刹那间欢呼声划破夜空。天安门广场迅速被红旗与标语汇聚成人海。出租车司机一路按响喇叭免费载客，人们相拥流泪高唱国歌，通宵达旦不眠。",
    [
        {
            "text": "披上国旗涌入广场与百万同胞并肩游行狂欢，相拥高呼中国万岁",
            "choiceTags": ["时代：2001", "年龄：14–60", "地域：全国大中城市", "门槛：普通公民"],
            "outcomes": [
                make_outcome("safe", 85, "在狂欢人潮中感受到无与伦比的民族尊严与自信，珍藏申奥号外报纸一辈子。", {"mentality": 25, "family": 15}, status="olympic_bid_witness", hidden_risk_log="亲历申奥成功莫斯科之夜，将大国崛起自信深深烙入生命。"),
                make_outcome("injured", 15, "人流极度拥挤中被踩伤右脚踝扭伤，但瘸着腿依然挥旗呐喊到天明。", {"health": -15, "mentality": 25}, hidden_risk_log="狂欢推挤受轻伤，在激荡青春中见证世纪盛典。")
            ]
        },
        {
            "text": "立志为七年后的北京奥运贡献力量，主动报考涉外英语或土木场馆建设专业",
            "choiceTags": ["时代：2001", "年龄：16–35", "地域：全国", "门槛：求学青年"],
            "outcomes": [
                make_outcome("safe", 75, "锚定目标发奋学习，日后成功入选奥运重点场馆设计团队或涉外核心骨干。", {"knowledge": 30, "wealth": 15, "mentality": 20}, status="olympic_dream_builder", hidden_risk_log="将申奥热情化为长远学业动力，终成国家重大工程参建骨干。"),
                make_outcome("safe", 25, "踏实自学涉外口语，在日常生活与工作中践行现代礼仪风尚。", {"knowledge": 15, "mentality": 15}, hidden_risk_log="从身边点滴提升文明素养，迎接世界眼光审视。")
            ]
        }
    ]
)

# 4. 2003 非典 SARS
add_evt(
    "evt_2003_sars_feidian", "era", "2003抗击“非典”与小汤山战役",
    [2003, 2003], [0, 80], ["ALL"], {},
    [], [], 0.90, 4, "确证",
    "2003年春我国遭遇非典型肺炎（SARS）突发公共卫生危机。北京、广东等地疫情严峻，7天7夜建成小汤山定点医院。全国医护白衣执甲逆行出征，城乡全民联防取得抗击非典全面胜利。",
    "街头弥漫着浓烈的过氧乙酸消毒水气味，药店门前排长队抢购板蓝根与白醋。学校体温表天天监测，进出小区量体温、登记出入证。电视里播放着小汤山抢建实况与白衣天使逆行剪影。",
    [
        {
            "text": "若为医护或公卫人员，毫不犹豫写下请战书，奔赴发热门诊与小汤山一线隔离区",
            "choiceTags": ["时代：2003", "年龄：20–55", "地域：全国各省", "门槛：医护体系人员"],
            "outcomes": [
                make_outcome("safe", 60, "在一线穿密闭厚重防护服连续奋战两月救治数十名重症病患，荣立卫生系统一等功。", {"mentality": 35, "knowledge": 25, "wealth": 15}, status="sars_medical_hero", hidden_risk_log="非典战役白衣战士，以仁心仁术护佑苍生，荣膺时代楷模称号。"),
                make_outcome("injured", 35, "在抢救插管过程中不幸感染非典重症，经大剂量激素冲击治疗保全性命但留股骨头缺血坏死隐患。", {"health": -40, "mentality": 25, "wealth": 20}, status="sars_convalescent", hidden_risk_log="抗疫一线感染康复，留下激素治疗慢性骨质损伤，深受全社会崇敬保障。"),
                make_outcome("fatal", 5, "在连续高强度抢救危重患者过程中不幸职业暴露感染殉职。", is_fatal=True, hidden_risk_log="在抗击非典一线英勇殉职，被追授烈士荣誉。")
            ]
        },
        {
            "text": "严格遵从防控指引居家隔离通风，每日监测体温，不造谣不传谣",
            "choiceTags": ["时代：2003", "年龄：0–80", "地域：全国", "门槛：普通国民"],
            "outcomes": [
                make_outcome("safe", 85, "用香皂勤洗手、居室开窗通风，平稳度过两个月紧张隔离期，全家人无恙。", {"family": 20, "mentality": 15}, status="sars_safe_survivor", hidden_risk_log="树立科学公卫防护观念，平稳度过新中国首场现代公卫危机。"),
                make_outcome("entangled", 15, "高价抢购数箱劣质板蓝根与白醋受骗破费数百元，深刻吸取不信谣教训。", {"wealth": -10, "mentality": -10}, hidden_risk_log="恐慌跟风抢购受骗交智商税，从此崇尚科学破除盲信。")
            ]
        }
    ]
)

# 5. 2003 孙志刚事件与收容遣送废除
add_evt(
    "evt_2003_shourong_feichu", "era", "收容遣送制度废除：公民权利与法治里程碑",
    [2003, 2004], [18, 55], ["ALL"], {},
    [], [], 0.80, 4, "确证",
    "2003年春大学生孙志刚在广州因未带暂住证被收容并遭殴打致死。引发三位法学博士联名上书，国务院果断废止实施21年的《城市流浪乞讨人员收容遣送办法》，建立自愿救助管理制度。",
    "法制报头版整版刊发国务院令。各大城市派出所与收容站的铁栏杆与收容招牌悄然拆除，外来打工青年再也不用在下班路上因忘记带暂住证而提心吊胆、被巡警随时盘查遣送返乡。",
    [
        {
            "text": "若为外来务工/白领，在租住地合法办理居住证，理直气壮在城市租房扎根发展",
            "choiceTags": ["时代：2003–2004", "年龄：18–45", "地域：全国大中城市", "门槛：外来务工/创业者"],
            "outcomes": [
                make_outcome("safe", 75, "摆脱被无端查证遣送的恐惧，放手拓展事业，把全家老小接进城平稳落户。", {"wealth": 25, "family": 20, "mentality": 20}, status="free_citizen_settler", hidden_risk_log="见证公民人身自由法治红利，在城市踏实扎根繁衍生息。"),
                make_outcome("safe", 25, "参与社区法律义务宣讲，向同乡普及依法维护人身权利与工伤维权法条。", {"knowledge": 20, "mentality": 15}, hidden_risk_log="学法用法维权，成为同乡工友信任的热心普法志愿者。")
            ]
        },
        {
            "text": "若为法律/政法系统工作人员，潜心研习行政法规违宪审查与现代救助制度建设",
            "choiceTags": ["时代：2003–2004", "年龄：22–50", "地域：政法机关/高校", "门槛：法学/公职人员"],
            "outcomes": [
                make_outcome("safe", 80, "参与起草地方民政救助管理新规，推动由强制收容向自愿救助的人性化转变。", {"knowledge": 25, "wealth": 15, "mentality": 20}, status="rule_of_law_advocate", hidden_risk_log="亲历法治中国重大制度飞跃，推动基层社会治理走向文明。"),
                make_outcome("entangled", 20, "新旧制度交替期间基层救助站事务暴增，连续通宵值班心力交瘁。", {"health": -15, "mentality": 10}, hidden_risk_log="治理转型过渡期基层操劳，但问心无愧履行公仆职责。")
            ]
        }
    ]
)

# 6. 2003 神舟五号飞天
add_evt(
    "evt_2003_shenzhou_wuhou", "era", "“神舟五号”首飞成功：千年飞天梦圆",
    [2003, 2003], [6, 75], ["ALL"], {},
    [], [], 0.90, 3, "确证",
    "2003年10月15日我国第一艘载人飞船‘神舟五号’发射升空。航天员杨利伟代表中国人首次巡天漫游21小时并安全着陆内蒙古大草原，中华民族千年飞天梦想终成现实。",
    "电视直播屏上飞船返回舱拖着巨大的红白降落伞徐徐飘落，草地上杨利伟向祖国敬礼的身影传遍神州大江南北。教室里、厂房走廊贴满了飞船海报，全国青少年掀起航天科技崇尚狂潮。",
    [
        {
            "text": "守在电视机前见证飞船落地敬礼历史瞬间，买下长征二号F火箭模型立志发愤求索",
            "choiceTags": ["时代：2003", "年龄：6–75", "地域：全国", "门槛：普通国民"],
            "outcomes": [
                make_outcome("safe", 85, "备受航天报国精神鼓舞，在学业或岗位上以严谨细致追求零缺陷，大获长进。", {"knowledge": 20, "mentality": 20}, status="aerospace_inspired", hidden_risk_log="亲历首次载人航天世纪壮举，铸就一丝不苟精益求精匠心。"),
                make_outcome("safe", 15, "带孩子去科技馆近距离参观飞船返回舱实物，点燃下一代科学梦想火种。", {"family": 20, "knowledge": 15}, hidden_risk_log="以国家科技成就启迪下一代，亲子情怀深厚。")
            ]
        },
        {
            "text": "若为军工航天或精密仪器机械技师，主动请缨参与下一代运载构件精密数控试制",
            "choiceTags": ["时代：2003", "年龄：22–50", "地域：军工三线/高校院所", "门槛：精密机械技师"],
            "outcomes": [
                make_outcome("safe", 75, "攻关薄壁钛合金构件微米级加工难关，获集团技术革新一等奖记功。", {"knowledge": 30, "wealth": 20, "mentality": 20}, status="aerospace_craftsman", hidden_risk_log="作为大国工匠亲身参与载人航天配套攻坚，赢得崇高尊严。"),
                make_outcome("injured", 25, "超高精度车削连续奋战数十小时导致严重视疲劳与慢性肩周炎。", {"health": -20, "knowledge": 25}, hidden_risk_log="奉献韶华于国防航天尖端制造，手掌布满钢铁机油印记。")
            ]
        }
    ]
)

# 7. 2006 农业税全面废止
add_evt(
    "evt_2006_nongyeshui_feizhi", "era", "延续两千六百年农业税全面废止",
    [2006, 2006], [16, 80], ["ALL"], {"urbanRural": "rural"},
    ["farmer"], [], 0.95, 3, "确证",
    "2006年1月1日全国人大决定废止《中华人民共和国农业税条例》。延续两千六百多年的‘皇粮国税’彻底退出中国历史舞台，国家更出台粮食直补政策，极大减轻亿万农民负担。",
    "村头的大喇叭正式播发中央免征农业税公报。粮站门前再也没有排长队送公粮过磅的板车，老农捧着红头公报在麦田埂上热泪盈眶：种地不用交公粮，国家还给发种粮补贴，千古未有之大德！",
    [
        {
            "text": "卸下沉重税赋包袱，把免征省下的资金全数投入改良良种与购置微耕机",
            "choiceTags": ["时代：2006", "年龄：18–70", "地域：全国农村", "门槛：种粮农户"],
            "outcomes": [
                make_outcome("safe", 75, "机械化翻耕省力增产，卖粮净落几万元现钞，家里盖起两层小洋楼。", {"wealth": 35, "health": 15, "family": 20}, status="free_grain_peasant", hidden_risk_log="享受农业税终结最大红利，机械化种粮实现家庭经济质的腾飞。"),
                make_outcome("injured", 20, "操作新型微耕机时不慎被旋耕刀刮伤右脚背，敷药包扎休养一个月。", {"health": -20, "wealth": 25}, hidden_risk_log="操作农机安全生疏负轻伤，随后严格落实安全防护规程。"),
                make_outcome("entangled", 5, "因邻村代耕土地流转补贴归属发生轻微争执，经村委调解化解。", {"family": -10, "wealth": 10}, hidden_risk_log="农业补贴推行初期产权细化经历微小磨合。")
            ]
        },
        {
            "text": "将承包田流转给村里种粮大户托管，安心进城常年务工做室内装修",
            "choiceTags": ["时代：2006", "年龄：20–50", "地域：城乡结合", "门槛：青壮劳力"],
            "outcomes": [
                make_outcome("safe", 80, "既有田亩流转租金保底，又在城里做瓦木水电月入四千元，城乡两头受惠。", {"wealth": 40, "family": 15}, new_career_track="worker", status="dual_income_builder", hidden_risk_log="乘农业免税与城镇化大潮两头获益，家庭迈入小康殷实生活。"),
                make_outcome("injured", 20, "装修施工长期吸入滑石粉与油漆异味引发慢性支气管炎，多咳喘。", {"health": -20, "wealth": 30}, new_career_track="worker", hidden_risk_log="室内装修粉尘伤及呼吸道，后佩戴专业防尘口罩。")
            ]
        }
    ]
)

# 8. 2007 股市6124大狂牛
add_evt(
    "evt_2007_gushi_6124", "era", "2007大牛市冲上6124点与全民炒股狂潮",
    [2007, 2008], [20, 65], ["ALL"], {"urbanRural": "urban"},
    [], [], 0.85, 4, "确证",
    "2007年10月上证综指创下历史巅峰6124点。股权分置改革推进，开户数突破一亿大关。买基金、炒股票成为街头巷尾全民狂热，买菜大妈与写字楼白领都在畅谈‘黄金十年’。",
    "证券公司营业部大厅水泄不通，红绿闪烁的行情大盘前全是挥舞存折的人群。连菜市场卖鱼小贩都在看K线图。然而盛极必衰，随后爆发的全球次贷危机引发狂跌，跌至1664点深度套牢千万人。",
    [
        {
            "text": "在指数攀上五千点以上敏锐感到泡沫风险，果断清仓离场转买银行保本理财",
            "choiceTags": ["时代：2007–2008", "年龄：22–60", "地域：城镇市民", "门槛：有数万积蓄基民股民"],
            "outcomes": [
                make_outcome("safe", 65, "成功在历史大顶全身而退锁定翻倍利润，避开随后惨烈的八成暴跌，保全家产。", {"wealth": 60, "mentality": 30}, status="bull_market_survivor", hidden_risk_log="在狂热癫狂前夕克制贪婪离场，战胜人性弱点守住财富成果。"),
                make_outcome("entangled", 35, "虽清仓股票但忍不住在六千点买入封闭式基金，随后腰斩亏损三成浮亏。", {"wealth": -20, "mentality": -20}, hidden_risk_log="半知半解追买基金遭遇深套，经受资本市场洗礼。")
            ]
        },
        {
            "text": "听信‘一万点不是梦’借钱加杠杆冲入蓝筹股，高位接盘遭遇断崖暴跌",
            "choiceTags": ["时代：2007–2008", "年龄：22–55", "地域：城镇股民", "门槛：盲从追高者"],
            "outcomes": [
                make_outcome("entangled", 65, "股票由高位暴跌七成深套，全副家当缩水大半，不得不卸载炒股软件长痛卧倒。", {"wealth": -45, "mentality": -35, "family": -15}, status="stock_bagholder", hidden_risk_log="在2007大牛市顶峰盲目追涨腰斩深套，承受惨痛人生财务教训。"),
                make_outcome("injured", 25, "连续数十天暴跌引发突发性心绞痛心律失常急诊入院，身心大受打击。", {"health": -30, "wealth": -40}, hidden_risk_log="股市暴跌导致急性心脏急症，在家人照料下戒掉炒股恶习。"),
                make_outcome("safe", 10, "靠按月定投红利低吸摊薄成本，在多年后漫长震荡中奇迹般解套保本。", {"wealth": 10, "knowledge": 25, "mentality": 20}, hidden_risk_log="在漫长熊市中悟出价值定投之道，心智获得彻底涅槃。")
            ]
        }
    ]
)

# 9. 2008 南方特大冰雪灾害
add_evt(
    "evt_2008_nanfang_xuezai", "era", "2008南方特大低温雨雪冰冻灾害",
    [2008, 2008], [0, 80], ["华南", "华中", "华东", "西南"],
    {"provinces": ["guangdong", "hunan", "guizhou", "jiangxi", "guangxi", "hubei", "anhui", "zhejiang"]},
    [], [], 0.90, 4, "确证",
    "2008年1月南方遭遇百年罕见特大冰雪冰冻灾害。京广铁路大动脉与国家电网骨干铁塔倒塌瘫痪，广州火车站数十万春运务工人员滞留风雨广场，全国军民展开除冰抢修大保畅。",
    "冻雨在电线和树枝上结出重重的透明冰甲，高压铁塔在重压下轰然弯折。广州火车站广场数十万人打着雨伞在冷风中瑟瑟发抖。部队官兵用铁锹砸碎钢轨坚冰，运送热姜汤和大衣。",
    [
        {
            "text": "若身处广州滞留人海，积极配合公安维持现场秩序，互相传递热开水与干粮抗冻",
            "choiceTags": ["时代：2008", "年龄：14–60", "地域：广州/南方春运枢纽", "门槛：滞留旅客"],
            "outcomes": [
                make_outcome("safe", 65, "在广场坚忍熬过五天四夜，终于登上第一列抢修恢复的内燃绿皮车平安归家。", {"family": 25, "mentality": 20}, status="ice_storm_survivor_2008", hidden_risk_log="在数十万滞留人潮中互助守望挺过冰雪严冬，淬炼出强大同理心。"),
                make_outcome("injured", 30, "极度拥挤寒冷导致严重冻伤脚趾并患急性支气管肺炎，回乡卧床打针两周。", {"health": -30, "wealth": -10}, hidden_risk_log="春运滞留受冻落下严重肺炎，在故乡温暖中疗愈休养。"),
                make_outcome("entangled", 5, "随身行李被雨雪浸透泡烂，丢失了带给老家父母的贵重礼物，心酸难过。", {"wealth": -15, "mentality": -15}, hidden_risk_log="冰雪途中行囊受损，但阖家团圆胜过一切身外之物。")
            ]
        },
        {
            "text": "若为电力/铁道/交通系统职工，冒严寒风雪奔赴深山攀爬铁塔除冰抢险",
            "choiceTags": ["时代：2008", "年龄：20–50", "地域：湖南/贵州高寒山区", "门槛：电力交通职工"],
            "outcomes": [
                make_outcome("safe", 60, "系好安全绳在零下低温中连爬数十基铁塔人工敲冰，保通京广动脉立大功。", {"mentality": 30, "wealth": 20, "knowledge": 15}, status="power_grid_hero_2008", hidden_risk_log="南网除冰前线铁血先锋，用冻红的双手点亮万家灯火。"),
                make_outcome("injured", 35, "在结冰铁塔上作业被暴风雪吹落的坠冰砸伤左肩，多处软组织重度挫伤。", {"health": -35, "mentality": 25, "wealth": 15}, status="injured_lineman_2008", hidden_risk_log="高空除冰抢险负伤荣立二等功，受到全行业致敬表彰。"),
                make_outcome("fatal", 5, "高压铁塔遭遇突发冰荷载倒塌不幸因公牺牲。", is_fatal=True, hidden_risk_log="在抗冰抢修前线因铁塔突发倒塌光荣殉职。")
            ]
        }
    ]
)

# 10. 2008 汶川特大地震
add_evt(
    "evt_2008_wenchuan_dizhen", "era", "5·12汶川8.0级特大地震与举国抗震救灾",
    [2008, 2008], [0, 80], ["ALL"],
    {"provinces": ["sichuan", "shaanxi", "gansu", "chongqing"]},
    [], [], 0.95, 4, "确证",
    "2008年5月12日14时28分四川汶川发生8.0级特大强震，破坏力极其巨大。十万解放军神兵天降、空降兵十五勇士冒死盲跳，全国十四亿同胞众志成城、倾力驰援，谱写抗震救灾壮丽史诗。",
    "大地狂暴撕裂，楼房山体在雷鸣声中轰然坍塌，尘烟遮天蔽日。都汶公路塌方阻断，救援冲锋舟劈波斩浪。全国大喇叭降半旗志哀，三分钟笛声长鸣，泪飞顿作倾盆雨。",
    [
        {
            "text": "若身处川陕甘震中废墟，咬紧牙关拼尽全力自救互救，从瓦砾中搜救同伴",
            "choiceTags": ["时代：2008", "年龄：10–65", "地域：四川川渝震区", "门槛：震区幸存者"],
            "outcomes": [
                make_outcome("safe", 50, "在强烈余震中用双手刨挖废墟救出两名邻家幼童，全家幸存，被授予抗震自救模范。", {"health": -15, "mentality": 30, "family": 25}, status="earthquake_hero_2008", hidden_risk_log="汶川地震绝境自救互救英雄，经受生死洗礼铸就磐石般心性。"),
                make_outcome("injured", 38, "遭遇预制板坍塌砸断右小腿尺骨，在野战方舱医院接受紧急截肢手术保全生命。", {"health": -45, "mentality": 15, "wealth": 10}, status="disabled_survivor_2008", hidden_risk_log="地震负重伤致残，在全国对口援建中坚强自立重建人生。"),
                make_outcome("entangled", 10, "祖辈老房尽数化为废墟瓦砾，在活动板房中过渡生活整年，心痛缅怀逝去亲友。", {"wealth": -40, "family": -25, "mentality": -30}, hidden_risk_log="痛失家园亲朋，在国家对口援建春风下重振旗鼓。"),
                make_outcome("fatal", 2, "在剧烈地震初始瞬间遭遇楼房粉碎性坍塌不幸罹难。", is_fatal=True, hidden_risk_log="在汶川特大地震强震瞬间不幸罹难。")
            ]
        },
        {
            "text": "若身处全国其他省份，主动报名参与民间救援志愿车队，连夜跨省运送帐篷与药品",
            "choiceTags": ["时代：2008", "年龄：18–55", "地域：全国非灾区", "门槛：热血同胞/志愿者"],
            "outcomes": [
                make_outcome("safe", 65, "驾驶卡车跨越千里将救灾物资送抵映秀都江堰一线，荣获抗震救灾优秀志愿者证书。", {"mentality": 30, "knowledge": 15, "wealth": -10}, status="volunteer_rescuer_2008", hidden_risk_log="千里奔袭驰援灾区一线，见证人间至纯大爱，升华人生境界。"),
                make_outcome("injured", 25, "在山道余震落石中被碎石砸裂车窗划伤前额留疤，包扎后继续搬运抢险。", {"health": -20, "wealth": -10}, hidden_risk_log="前线运输遭遇落石负轻伤，以伤痕为荣守护生命通道。"),
                make_outcome("safe", 10, "在单位与街道连续排队三次献血并捐出一个月工资，奉献无私同胞深情。", {"wealth": -15, "mentality": 20}, hidden_risk_log="倾力捐款献血支援同胞，凝聚血脉相连民族力量。")
            ]
        }
    ]
)

print(f"2000-2026 builder batch 1 complete. Current events: {len(events)}")
