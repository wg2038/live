# tools/build_events_1950_1977_full.py
# -*- coding: utf-8 -*-
"""
生成 1950–1977 年共 42 条全要素历史事件库，严格遵循：
- choiceTags 四元标签
- safe / injured / entangled / redirected / fatal 多元权重分支 (fatal <= 2%)
- hiddenRiskLog 用于终局因果回顾
- factLevel (确证/估计/文学化)
- 敏感历史事件克制表述
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

# 1. 1950 颁布婚姻法
add_evt(
    "evt_1950_hunyinfa", "era", "新中国首部法律《婚姻法》与婚姻自主",
    [1950, 1952], [16, 35], ["ALL"], {},
    [], [], 0.88, 4, "确证",
    "1950年4月中央人民政府颁布《中华人民共和国婚姻法》，废除封建包办买卖婚姻，实行男女婚姻自由、一夫一妻、男女权利平等，亿万妇女从宗法枷锁中彻底解脱。",
    "县城与乡村的泥墙上刷起醒目的白字标语：婚姻自由，男女平等。区公所门口摆着婚姻登记小木桌，不少深受包办童养媳虐待的妇女在妇联干部的鼓励下鼓起勇气，走向自主幸福。",
    [
        {
            "text": "勇敢挣脱包办指腹为婚旧俗，与自由恋爱的意中人到区公所领证登记结婚",
            "choiceTags": ["时代：1950–1952", "年龄：18–35", "地域：全国城乡", "门槛：适婚青年"],
            "outcomes": [
                make_outcome("safe", 75, "领到盖有红五星的大红结婚证，夫妻自主恩爱，共同操持家务劳动，家庭和睦幸福。", {"family": 30, "mentality": 25, "wealth": 10}, status="free_marriage_pioneer", hidden_risk_log="率先拥抱新婚姻法走入自由婚姻，摆脱封建宗法阴霾。"),
                make_outcome("entangled", 25, "退掉旧式包办婚约遭到夫家旧宗族上门纠缠争吵，经村干群大会严厉调解方告平息。", {"family": -15, "mentality": -10}, hidden_risk_log="冲破封建包办经历宗族阻力，经政府撑腰彻底翻身。")
            ]
        },
        {
            "text": "遵从父母之命媒妁之言成婚，婚后依法签署平等平顺互助夫妻契约",
            "choiceTags": ["时代：1950–1952", "年龄：18–32", "地域：传统乡土", "门槛：本分青年"],
            "outcomes": [
                make_outcome("safe", 80, "伴侣勤劳善良守本分，虽无轰烈恋爱但相敬如宾，踏踏实实过起柴米油盐寻常日子。", {"family": 25, "wealth": 10}, status="harmonious_traditional_couple", hidden_risk_log="在传统与现代过渡期相敬如宾持家，生活稳固踏实。"),
                make_outcome("safe", 20, "婚后共同参加夜校扫盲班，互相教写名字算账，感情日益笃厚融洽。", {"knowledge": 20, "family": 20}, hidden_risk_log="夫妻携手在夜校识字学文化，共同迈入新社会。")
            ]
        }
    ]
)

# 2. 1950 土地改革法
add_evt(
    "evt_1950_tudigaige_fenchan", "era", "《土地改革法》与三亿无地农民分田地",
    [1950, 1952], [14, 65], ["ALL"], {"urbanRural": "rural"},
    ["farmer"], [], 0.92, 4, "确证",
    "1950年6月中央颁布《中华人民共和国土地改革法》，在全国新解放区废除封建剥削土地所有制，三亿无地少地农民分得约七亿亩土地及大量耕牛农具，真正实现‘耕者有其田’。",
    "工作队进村丈量田亩界石，地主旧地契在祠堂前的大火盆里化为灰烬。祖辈给东家当牛做马的佃农赤着脚抚摸分到的三亩水田泥土，眼眶里含满滚烫的泪花。",
    [
        {
            "text": "精心侍弄分到的良田与老耕牛，深翻细耙施农家肥，迎头打出翻身大丰收",
            "choiceTags": ["时代：1950–1952", "年龄：16–65", "地域：全国农村", "门槛：翻身农民"],
            "outcomes": [
                make_outcome("safe", 75, "秋收打下满缸金黄稻谷麦子，交够公粮后余粮堆满囤，家里添置了新被褥与铁犁。", {"wealth": 30, "family": 20, "mentality": 25}, status="land_reform_beneficiary", hidden_risk_log="在土改中分得土地彻底翻身，以极高劳动热情改变赤贫命运。"),
                make_outcome("injured", 20, "日夜开荒抢种过度劳累扭伤右肩并患急性结膜炎，草药敷贴调理半月。", {"health": -20, "wealth": 25}, hidden_risk_log="翻身干劲过猛受劳损，但家里粮仓从此充盈。"),
                make_outcome("entangled", 5, "因界石划分与同村中农产生微小地头争执，经大队评议和气化解。", {"family": -10, "wealth": 15}, hidden_risk_log="土改确权经历细微磨合，更加懂得团结友邻。")
            ]
        },
        {
            "text": "积极参加村农会与民兵自卫队，站岗放哨巡逻守护新生翻身果实",
            "choiceTags": ["时代：1950–1952", "年龄：18–40", "地域：乡村基层", "门槛：青年农民"],
            "outcomes": [
                make_outcome("safe", 75, "手握红缨枪守卫粮库与关卡，抓获两名潜伏破坏特务，被评为全县民兵战斗模范。", {"mentality": 30, "knowledge": 15, "wealth": 15}, status="militia_model", hidden_risk_log="担任基层民兵守护胜利果实，因表现突出成为村党支部骨干。"),
                make_outcome("injured", 25, "夜间巡逻盘查遭遇顽匪负隅顽抗搏斗被匕首刺伤左小臂，伤愈后受通令表彰。", {"health": -25, "mentality": 25, "wealth": 15}, hidden_risk_log="保卫土改成果英勇负伤，赢得乡亲们长久尊崇。")
            ]
        }
    ]
)

# 3. 1950 抗美援朝
add_evt(
    "evt_1950_kangmei_yuanzhao", "era", "抗美援朝：志愿军出征与后方动员",
    [1950, 1953], [17, 30], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "1950年10月中国人民志愿军跨过鸭绿江，拉开伟大的抗美援朝保家卫国战争。全国掀起参军参战狂潮，后方工农开展爱国增产节约运动，常香玉等各界爱国人士慷慨捐献飞机大炮。",
    "火车站台挂满‘抗美援朝、保家卫国’巨幅标语，锣鼓喧天。胸佩大红花的志愿军青年扒着闷罐列车车窗，向送行的白发父母挥动军帽。鸭绿江对岸炮火连天，英雄儿女即将踏入冰天雪地。",
    [
        {
            "text": "毅然报名参加中国人民志愿军开赴朝鲜前线，参加长津湖与上甘岭战役",
            "choiceTags": ["时代：1950–1953", "年龄：17–28", "地域：全国", "门槛：热血青年男性"],
            "outcomes": [
                make_outcome("safe", 45, "在上甘岭坑道坚守数日打退数十次冲锋，荣立战功凯旋回国，安置入省重点工业大厂转正。", {"mentality": 40, "knowledge": 15, "wealth": 25}, status="korean_war_hero", hidden_risk_log="抗美援朝铁血老兵，经受世界最严酷战火淬炼，荣归故里受一世敬仰。"),
                make_outcome("injured", 38, "在极寒阻击战中遭遇严重冻伤致两只脚趾截肢，且被炮弹破片击中左肩，评残退伍保送干部学校。", {"health": -40, "mentality": 25, "wealth": 20}, status="disabled_veteran_korea", hidden_risk_log="朝鲜战场英勇负重伤冻伤致残，受到国家长久抚恤保障。"),
                make_outcome("entangled", 15, "目睹战友牺牲长年患有严重失眠与惊悸，在地方农场默默耕耘不求闻达。", {"mentality": -25, "health": -15}, hidden_risk_log="战后深藏功名默默归乡，在平凡劳作中安抚战火创伤。"),
                make_outcome("fatal", 2, "在坚守前线阻击阵地时遭遇敌机重磅航弹直接轰炸光荣牺牲。", is_fatal=True, hidden_risk_log="在抗美援朝保家卫国前线光荣牺牲，被追授革命烈士。")
            ]
        },
        {
            "text": "留守后方厂矿或农村，夜以继日加班加点超额完成生产支前军需与捐献",
            "choiceTags": ["时代：1950–1953", "年龄：16–60", "地域：全国大后方", "门槛：后方工农大众"],
            "outcomes": [
                make_outcome("safe", 75, "带领全组完成三倍军用帆布鞋与炒面罐头加工任务，获评后方爱国增产模范奖章。", {"wealth": 20, "knowledge": 15, "mentality": 20}, status="production_support_model", hidden_risk_log="在后方拼命苦干支前，以实打实的物资产量支援前线大捷。"),
                make_outcome("injured", 25, "连轴转三天三夜通宵赶制军用铁镐手掌严重烫伤开裂，卧床包扎三天继续上岗。", {"health": -20, "wealth": 15}, hidden_risk_log="后方支前忘我奉献负轻伤，体现深厚爱国情操。")
            ]
        }
    ]
)

# 4. 1951 “三反”“五反”
add_evt(
    "evt_1951_sanfan_wufan", "era", "“三反”“五反”运动与廉洁整风",
    [1951, 1952], [20, 60], ["ALL"], {"urbanRural": "urban"},
    ["worker", "cadre_teacher", "merchant"], [], 0.85, 4, "确证",
    "1951年底党和政府在国家机关内部开展反贪污、反浪费、反官僚主义的‘三反’运动，随后在私营工商业中开展反行贿、反偷税漏税、反盗骗国家财产、反偷工减料、反盗窃经济情报的‘五反’运动，树立廉洁新风尚。",
    "机关大院与商会礼堂贴满了揭发检举的大字报，清账查账小组进驻各大私营厂店。干部坦白交代收受礼金账目，工商业主对照账目退赔偷漏税款，社会廉洁风气空前纯洁。",
    [
        {
            "text": "若为公职人员，一尘不染经受审查，主动交清两包香烟私账，获评廉洁大模范",
            "choiceTags": ["时代：1951–1952", "年龄：22–55", "地域：城镇机关系统", "门槛：体制公职人员"],
            "outcomes": [
                make_outcome("safe", 85, "账目分毫不差一清二白，经群众公议评为廉洁自律标兵，提拔为主管财经科长。", {"knowledge": 20, "wealth": 15, "mentality": 25}, status="clean_honest_cadre", hidden_risk_log="在三反大考中坚守清正廉洁，赢得极高党纪与群众公信力。"),
                make_outcome("entangled", 15, "因经办采购发票字迹模糊受隔离审查三天核实，澄清嫌疑后心有余悸。", {"mentality": -15}, hidden_risk_log="例行审查虚惊一场，更加注重账目字据严谨。")
            ]
        },
        {
            "text": "若为私营手工业主，主动如实补缴以往少报税金，绝不掺假偷工减料制造次品",
            "choiceTags": ["时代：1951–1952", "年龄：22–60", "地域：工商企业", "门槛：私营业主/账房"],
            "outcomes": [
                make_outcome("safe", 70, "诚实守法规范台账，按时足额交税，被定为守法户并在后续合营中获评工商业代表。", {"wealth": 15, "knowledge": 15}, status="law_abiding_merchant", hidden_risk_log="遵纪守法规范经营，为后续公私合营打牢信用根基。"),
                make_outcome("entangled", 30, "因过去倒卖棉纱偷税账目被勒令全额退税并罚款八百元，家底大受折损。", {"wealth": -30, "mentality": -20}, hidden_risk_log="贪图旧社会陋规吃罚单受挫，彻底吸取教训遵规守法。")
            ]
        }
    ]
)

# 5. 1952 爱国卫生运动
add_evt(
    "evt_1952_aiguo_weisheng", "era", "全民爱国卫生运动与消灭霍乱天花",
    [1952, 1954], [6, 75], ["ALL"], {},
    [], [], 0.95, 3, "确证",
    "1952年全国范围内轰轰烈烈展开反美细菌战爱国卫生运动。动员全民‘除四害’（苍蝇、蚊子、老鼠、麻雀），清扫污泥水沟、填平死水洼、全民接种牛痘与霍乱疫苗，历史性控制住烈性传染病蔓延。",
    "锣鼓声中全城男女老幼拿着竹扫帚和铁铲清掏百年陈腐臭水沟。墙角撒上刺鼻的生石灰白粉，井口加盖上锁。防疫队员背着药箱给胡同里每一个孩子胳膊上划痕接种牛痘花针。",
    [
        {
            "text": "积极排队接种牛痘与伤寒霍乱疫苗，带领邻里清扫大杂院臭水沟与灭蚊蝇",
            "choiceTags": ["时代：1952–1954", "年龄：6–70", "地域：全国城乡", "门槛：全体居民"],
            "outcomes": [
                make_outcome("safe", 85, "接种疫苗形成牢固终身免疫抗体，彻底远离天花霍乱等致命恶疾，身体健康强壮。", {"health": 30, "family": 20, "mentality": 15}, status="hygiene_model_1952", hidden_risk_log="享受新中国现代公共卫生接种首轮红利，打牢终生免疫底子。"),
                make_outcome("injured", 15, "接种牛痘后手臂局部化脓肿胀伴发高烧三天，草药湿敷后平安结痂留花印。", {"health": -10, "family": 15}, hidden_risk_log="牛痘接种轻度不良反应安然自愈，手臂留下时代接种印记。")
            ]
        },
        {
            "text": "因迷信旧俗逃避打针吃药，拒绝清理自家后院陈年垃圾堆，引发苍蝇孳生",
            "choiceTags": ["时代：1952–1954", "年龄：14–65", "地域：落后边远乡村", "门槛：保守居民"],
            "outcomes": [
                make_outcome("injured", 65, "饮用生水不幸感染急性肠伤寒高热抽搐脱水，幸得巡回防疫队灌服黄连素大蒜素抢救脱险。", {"health": -35, "wealth": -10}, hidden_risk_log="逃避卫生管理染重疾险丧命，深刻反思转为卫生模范。"),
                make_outcome("safe", 35, "在干部严肃批评教育下打消顾虑补种疫苗，并主动掏干水井淤泥认错。", {"knowledge": 15, "mentality": 10}, hidden_risk_log="破除迷信转危为安，拥抱科学公卫新风。")
            ]
        }
    ]
)

# 6. 1953 “一五”计划与156项重点工程
add_evt(
    "evt_1953_yiwujihua_gongye", "era", "“一五”计划启动与156项重点工程奠基",
    [1953, 1956], [16, 45], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "1953年中国开始执行发展国民经济的第一个五年计划，以苏联援建的156项重点工程为骨干。鞍钢无缝钢管厂、长春第一汽车制造厂、沈阳第一机床厂拔地而起，中国重工业基础全面奠定。",
    "高耸的红砖高炉直插云霄，苏联专家的吉斯小轿车停在厂区大礼堂门前。城里招工红榜刚一贴出，无数青年农民背起包袱进城考核。穿蓝色咔叽布工装、戴大厂胸章成为最荣耀体面的象征。",
    [
        {
            "text": "通过钳工车工学徒考核考入国营大厂，随苏联老专家苦练车床精密切削手艺",
            "choiceTags": ["时代：1953–1956", "年龄：16–35", "地域：东北/华北/华东工矿", "门槛：身体健康青工"],
            "outcomes": [
                make_outcome("safe", 70, "三年满师考取四级车工，每月领四十八元高工资并分到单身职工宿舍，端稳铁饭碗。", {"wealth": 30, "knowledge": 25, "mentality": 20}, new_career_track="worker", status="first_gen_industrial_worker", hidden_risk_log="新中国第一代产业工人标杆，掌握苏联图纸技术，奠定终生工薪阶层地位。"),
                make_outcome("injured", 20, "车床高速旋转铁屑飞溅烫伤右手背并留伤疤，所幸戴防护镜保全双眼。", {"health": -20, "wealth": 25}, new_career_track="worker", hidden_risk_log="机械加工操作负轻微烫伤，练就过硬安全防护警惕。"),
                make_outcome("entangled", 10, "三班倒夜班高强度重体力劳作导致严重慢性胃炎胃下垂，常备胃舒平止痛。", {"health": -25, "wealth": 20}, new_career_track="worker", hidden_risk_log="工业强基年代透支脾胃，在奉献中铸就大工业脊梁。")
            ]
        },
        {
            "text": "响应号召留在农村参与修筑水库大坝与引水渠，以工分换粮食支援前线工矿",
            "choiceTags": ["时代：1953–1956", "年龄：16–50", "地域：全国农村", "门槛：农村整劳力"],
            "outcomes": [
                make_outcome("safe", 75, "参与修建中型水库保得全乡旱涝保收，因推独轮车运土创纪录评为县治水模范。", {"family": 20, "mentality": 20, "wealth": 10}, status="water_conservancy_model", hidden_risk_log="治水兴农夯实农业根基，深得公社大队信赖尊重。"),
                make_outcome("injured", 25, "大坝石料爆破排险被飞石砸伤小腿腓骨，休工在生产队草棚养伤一个月。", {"health": -25, "family": 15}, hidden_risk_log="修大坝水利负轻工伤，留下荣耀劳动印记。")
            ]
        }
    ]
)

# 7. 1954 长江大洪水
add_evt(
    "evt_1954_changjiang_hongshui", "era", "1954长江特大洪水与武汉防汛保卫战",
    [1954, 1954], [10, 75], ["华中", "华东"],
    {"provinces": ["hubei", "hunan", "jiangxi", "anhui", "jiangsu"]},
    [], [], 0.90, 4, "确证",
    "1954年夏长江流域遭遇百年未有特大洪涝。最高水位达29.73米超越历史极值。三十万军民在武汉龙王庙、荆江分洪区严防死守、‘人在堤在’，毛主席亲笔题词庆贺抗洪伟大胜利。",
    "江水狂暴漫涨，汉口江滩已被黄浪淹没，江水高过沿江大道房顶数米。大堤上搭满芦席棚，铁镐叮当、沙袋如山。警报声整夜凄厉鸣响，人们跳进激流以血肉之躯堵住致命管涌。",
    [
        {
            "text": "若身处武汉或沿江受灾区，报名抢险突击队日夜跳入混浊江水打木桩抢护江堤",
            "choiceTags": ["时代：1954", "年龄：16–55", "地域：湖北武汉及沿江", "门槛：沿江军民"],
            "outcomes": [
                make_outcome("safe", 60, "在大堤上连熬十天十夜成功封堵险情保住大武汉，获颁防汛抗洪纪念章与大红花。", {"mentality": 30, "family": 20, "health": -10}, status="changjiang_flood_hero_1954", hidden_risk_log="五四长江特大抗洪英雄，以钢铁意志守护九省通衢安澜。"),
                make_outcome("injured", 35, "江水中搬运沉重麻袋被漂木撞伤胸口肋骨骨裂，并患重度浸渍性烂脚。", {"health": -35, "mentality": 25}, status="injured_flood_hero_1954", hidden_risk_log="抗洪抢险负伤荣立三等功，终身以保卫家园为荣。"),
                make_outcome("entangled", 3, "身后自家低洼旧棚被倒灌内涝浸泡倒塌，一家老小在安置帐篷生活两月。", {"wealth": -30, "family": -15}, hidden_risk_log="家园受淹经受困苦，在政府救济下重建新居。"),
                make_outcome("fatal", 2, "夜间突发决口合龙打桩时被狂暴激流卷入江底不幸牺牲。", is_fatal=True, hidden_risk_log="在武汉防汛大堤最危急关头英勇牺牲。")
            ]
        },
        {
            "text": "在后方开辟后勤炊事线，通宵熬煮防风寒大锅姜汤与高粱杂粮馍馍送上大堤",
            "choiceTags": ["时代：1954", "年龄：14–65", "地域：沿江城镇", "门槛：普通市民"],
            "outcomes": [
                make_outcome("safe", 85, "每天挑送上百碗热气腾腾的姜汤与干粮给前线官兵充饥，获大堤指挥部通报表扬。", {"family": 20, "mentality": 20}, status="flood_logistics_champion", hidden_risk_log="以温暖后勤支援大堤抢险，展现血浓于水同胞深情。"),
                make_outcome("safe", 15, "腾出自家干燥阁楼收留安置四名受淹灾区亲戚居住两月，共克时艰。", {"family": 25, "wealth": -10}, hidden_risk_log="患难中接济宗亲，筑牢家庭温暖亲情纽带。")
            ]
        }
    ]
)

# 8. 1955 农业合作化高潮
add_evt(
    "evt_1955_hezuohua_gaochao", "era", "农业合作化高潮：初级社向高级社迈进",
    [1955, 1956], [16, 65], ["ALL"], {"urbanRural": "rural"},
    ["farmer"], [], 0.90, 4, "确证",
    "1955年下半年毛主席发表《关于农业合作化问题》报告，全国掀起农业合作化狂潮。亿万农户将土地、大牲畜折价入社，由土地分红的初级社迅速转变为集体所有制的高级农业生产合作社。",
    "村头敲锣打鼓贴红榜，大铁锅里煮着庆祝高级社成立的红薯稀饭。老农们牵着自家刚喂壮的黄牛来到社部，在土地牲畜入社交割薄上按红手印，集体记工分的生产队时代全面来临。",
    [
        {
            "text": "带头将耕牛、铁犁与水田折资入社，在生产队担任第一任大队长或记工员",
            "choiceTags": ["时代：1955–1956", "年龄：20–50", "地域：全国农村", "门槛：积极社员/中贫农"],
            "outcomes": [
                make_outcome("safe", 75, "公正记工分公平调度农活，社里秋收打下高产粮食，被公社评为模范生产队长。", {"knowledge": 20, "wealth": 15, "mentality": 20}, status="coop_leader", hidden_risk_log="顺应集体化大潮挑大梁，成为基层生产队威信卓著的当家人。"),
                make_outcome("entangled", 25, "因牲口折价折算过低与个别老农产生争执，经大队核算调补差价方才和解。", {"family": -10, "mentality": -10}, hidden_risk_log="合作化资产折价协调劳心伤神，磨炼群众调解经验。")
            ]
        },
        {
            "text": "安心在生产队当出满勤整劳力，凭一身农耕力气每天挣满十分头等工分",
            "choiceTags": ["时代：1955–1956", "年龄：16–60", "地域：全国农村", "门槛：本分社员"],
            "outcomes": [
                make_outcome("safe", 80, "出满勤干满点，年终分红分得足额口粮与分红柴火，日子平稳温饱。", {"family": 20, "health": 10, "wealth": 10}, status="ten_workpoint_peasant", hidden_risk_log="本分劳作挣满十分工分，在集体化初期享受安稳分红。"),
                make_outcome("injured", 20, "开荒挑土过猛闪了腰岔气，卧床休工一周扣发数日工分。", {"health": -15, "wealth": -5}, hidden_risk_log="重体力农活劳损腰部，学会量力而行科学劳作。")
            ]
        }
    ]
)

# 9. 1956 公私合营高潮
add_evt(
    "evt_1956_gongsi_heying", "era", "社会主义三大改造：公私合营与手工业入社",
    [1956, 1956], [18, 65], ["ALL"], {"urbanRural": "urban"},
    ["merchant", "worker"], [], 0.90, 4, "确证",
    "1956年全国掀起资本主义工商业社会主义改造高潮。北京、上海等大城市私营商户与老字号敲锣打鼓申请合营，纳入公私合营工厂或手工业生产合作社，发放定息，确立公有制主体地位。",
    "街头巷尾红旗如海，爆竹硝烟弥漫弄堂。同仁堂、全聚德等老字号掌柜带头交出账本，私营小商贩和修鞋补锅匠也纷纷把担子工具折价入社，领到了统一盖有红章的职工证和工薪存折。",
    [
        {
            "text": "主动带头将自家祖传铺面作坊资产申报合营，转为公私合营工厂的正式带班技师",
            "choiceTags": ["时代：1956", "年龄：22–60", "地域：城镇工商界", "门槛：私营店主/手工业者"],
            "outcomes": [
                make_outcome("safe", 75, "领受国家定息并被定为车间副主任兼高级技师，每月享受稳定固定工资与劳保看病全报销。", {"wealth": 25, "knowledge": 20, "mentality": 20}, new_career_track="worker", status="joint_ownership_master", hidden_risk_log="公私合营带头人，平稳由个体私营跨入社会主义产业工人编制。"),
                make_outcome("entangled", 25, "初入大车间对定岗打卡考勤与繁琐账目感到不适，怀念以往散漫自由，经半年适应。", {"mentality": -15}, new_career_track="worker", hidden_risk_log="适应集体工厂严格纪律经历阵痛，逐步融入体制保障。")
            ]
        },
        {
            "text": "将零碎手艺工具折算加入街道便民生产服务合作组，走街串巷做定点零修保底",
            "choiceTags": ["时代：1956", "年龄：18–60", "地域：城镇街巷", "门槛：底层小手艺人"],
            "outcomes": [
                make_outcome("safe", 80, "在街道服务站领固定津贴，凭精湛修补手艺深受街坊爱戴，过着体面踏实的小日子。", {"wealth": 15, "family": 15}, status="street_artisan_stable", hidden_risk_log="加入便民合作社端上稳饭碗，免除以往受流氓盘剥之苦。"),
                make_outcome("safe", 20, "热心替大杂院孤寡老人免费修补门窗瓦片，被街道评选为便民雷锋式模范。", {"mentality": 20, "family": 15}, hidden_risk_log="便民助人赢得邻里口碑，社会地位大幅提升。")
            ]
        }
    ]
)

# 10. 1957 知识分子反右
add_evt(
    "evt_1957_fanyou_yundong", "era", "1957年整风反右运动与知识分子抉择",
    [1957, 1958], [18, 60], ["ALL"], {"urbanRural": "urban"},
    ["cadre_teacher", "higher_ed_degree"], [], 0.85, 5, "估计/文学化",
    "1957年夏党内整风转向反右派斗争。运动出现严重扩大化，大批知识分子、教师与干部被错划为‘右派分子’下放农村劳动改造，对国家民主与文化建设造成重大历史创伤。",
    "会议室里烟雾缭绕，批判大字报层层叠叠贴满礼堂走廊。往日谈笑风生的教授与编辑在台上低头检讨发言。昔日同窗好友在发言记录前小心翼翼，任何一句学术探讨都可能被无限拔高定性。",
    [
        {
            "text": "面对复杂风浪坚守学术科研书桌，闭门谢客撰写纯数理教材，绝不妄议政事",
            "choiceTags": ["时代：1957–1958", "年龄：20–60", "地域：高校科研院所", "门槛：知识分子/教师"],
            "outcomes": [
                make_outcome("safe", 65, "独善其身避开政治狂飙波及，潜心完成两部国家重点工程专著，保全学术火种。", {"knowledge": 30, "mentality": 10}, status="scholar_preserved", hidden_risk_log="在反右扩大化狂潮中冷静克制独善其身，守住学术底线与平安。"),
                make_outcome("entangled", 30, "因历史日记被个别人摘抄借题发挥，受到大会公开批判并做深刻检讨停课半年。", {"mentality": -30, "wealth": -10}, hidden_risk_log="无端受牵连检讨经受心理重创，后恢复基础教研工作。"),
                make_outcome("injured", 5, "被下放农场监督劳动期间劳累过度导致慢性腰肌劳损与营养不良浮肿。", {"health": -30, "mentality": -20}, hidden_risk_log="下放农场经受体力磨难，磨炼出顽强生存定力。")
            ]
        },
        {
            "text": "出于对党和教育事业的朴素热忱，如实针对高校教条主义与后勤官僚风气直言进谏",
            "choiceTags": ["时代：1957–1958", "年龄：20–55", "地域：高校与文教系统", "门槛：热血青年知识分子"],
            "outcomes": [
                make_outcome("safe", 45, "所提意见纯属业务后勤改善且态度极为诚恳，经党组织客观保护免于处分过关。", {"knowledge": 15, "mentality": 15}, hidden_risk_log="虚惊一场获开明领导保护，从此更加懂得实事求是智慧。"),
                make_outcome("entangled", 45, "不幸被认定为思想严重偏向戴上右派帽子，降级降薪并下放到偏远国营农场劳动改造。", {"wealth": -35, "mentality": -40, "family": -25}, status="rightist_rehabilitated_later", hidden_risk_log="遭遇反右扩大化被错划下放，历经二十载沉浮后于1979年彻底平反昭雪。"),
                make_outcome("injured", 10, "在严寒农场盐碱地繁重劳动冻伤脚趾破溃，且患严重胃溃疡吐血保外就医。", {"health": -40, "wealth": -20}, hidden_risk_log="农场劳动落下终生病痛，但在逆境中手不释卷坚守真理。")
            ]
        }
    ]
)

print(f"Adding 1950-1977 events... Current count: {len(events)}")
