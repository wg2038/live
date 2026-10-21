# tools/build_events_trajectory.py
# -*- coding: utf-8 -*-
"""
生成轨迹层（职业暴露、生活习惯、爱好行为）共 18 条高精度事件库：
- 涵盖矿工、大货车司机、建筑工、骑手、渔民、消防员、乡村教师、医护、程序员、小个体户等职业
- 涵盖长期吸烟、嗜酒、熬夜、野泳、登山、摩托骑行、体检延误等生活习惯与爱好
- 严格遵循：choiceTags 四元标签、hiddenRiskLog 因果回顾、致命分支 <= 2-4%
"""

import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root)

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

# 1. 矿井开采作业与粉尘顶板防护
add_evt(
    "evt_traj_kuangong_fengxian", "trajectory", "地下采掘作业：顶板支护与煤尘防护",
    [1937, 2026], [18, 55], ["ALL"], {},
    ["worker"], [], 0.75, 4, "确证",
    "中国是世界煤炭开采大国，深部井下作业长期面临瓦斯、顶板垮塌、煤尘等高危环境。伴随综采液压支架普及与湿式除尘推广，井下安全水平发生历史性飞跃。",
    "罐笼飞速下坠进入数百米地心，井下巷道阴暗潮湿，矿灯光柱在弥漫的煤尘中晃动。采煤机滚筒轰鸣割煤，头顶的岩层偶有碎石掉落，支护工正严密观察压力表指针。",
    [
        {
            "text": "严格佩戴正压防尘口罩，进掌子面前先用长钎细致敲帮问顶加固液压单体支柱",
            "choiceTags": ["时代：通用时代", "年龄：18–55", "地域：工矿井下", "门槛：采矿工人"],
            "outcomes": [
                make_outcome("safe", 75, "规范支护成功防范数起险情，月度安全采煤超额完成指标，获评矿区‘安全哨兵’模范标兵。", {"wealth": 25, "knowledge": 20, "mentality": 25}, status="miner_safety_model", hidden_risk_log="恪守井下安全规程与粉尘防护，一生避开肺部纤维化与瓦斯灾害。"),
                make_outcome("injured", 22, "顶板微小离层掉落煤矸石砸中安全帽与右肩挫伤，包扎休养一周后安全返岗。", {"health": -20, "wealth": 15}, hidden_risk_log="井下规范作业遇险逢凶化吉，仅受轻微皮肉挫伤。"),
                make_outcome("fatal", 3, "在深部采掘面遭遇突发大面积顶板冒顶岩石压塌不幸殉职。", is_fatal=True, hidden_risk_log="在井下采煤突发严重顶板垮塌事故中不幸遇难。")
            ]
        },
        {
            "text": "因井下闷热嫌憋闷擅自摘下防尘口罩，为赶出煤进度忽视临时支护空顶作业",
            "choiceTags": ["时代：通用时代", "年龄：18–50", "地域：工矿井下", "门槛：麻痹违章工人"],
            "outcomes": [
                make_outcome("injured", 65, "常年吸入高浓度煤粉导致肺部弥漫结节患上一期煤工尘肺，出现活动后气短，转岗地面保洁。", {"health": -35, "wealth": -10}, status="pneumoconiosis_worker", hidden_risk_log="长期忽视防尘口罩吸入大量矿尘罹患尘肺，悔恨终生。"),
                make_outcome("injured", 31, "空顶作业遭遇滚石砸裂左小腿腓骨，停工石膏固定休养三月。", {"health": -30, "wealth": -15}, hidden_risk_log="违章空顶作业受骨折重创，彻底吸取安全教训。"),
                make_outcome("fatal", 4, "在未支护空顶区域遭遇大块岩石瞬间坍塌砸中要害不幸身亡。", is_fatal=True, hidden_risk_log="在采煤作业违章空顶区域遭遇冒顶事故不幸罹难。")
            ]
        }
    ]
)

# 2. 长途货运夜驾与疲劳驾驶
add_evt(
    "evt_traj_huoche_pilao", "trajectory", "长途半挂车货运：千里夜驾与防疲劳博弈",
    [1980, 2026], [22, 55], ["ALL"], {},
    ["worker", "merchant"], [], 0.80, 4, "确证",
    "长途货车司机是支撑中国现代物流大动脉的无名英雄。长年奔波在国道高速上，面临夜间疲劳、山区长下坡刹车热衰退和货物绑扎风险。",
    "午夜两点的国道上，半挂重卡的远光灯撕裂漆黑夜色。驾驶室内柴油机沉闷低吼，眼皮沉重得像挂了铅块。前方进入连续数十公里长下坡危险路段，警示牌反光刺目：‘严禁空挡滑行’。",
    [
        {
            "text": "绝不疲劳驾驶，见服务区果断进站洗冷水脸并在卧铺踏实小憩两小时再启程",
            "choiceTags": ["时代：1980–2026", "年龄：22–55", "地域：全国公路网", "门槛：长途货车司机"],
            "outcomes": [
                make_outcome("safe", 85, "精力充沛安全驶过险峻下坡路段，按时交付数十吨绿通鲜活农产品，创百万公里无事故纪录。", {"wealth": 30, "mentality": 25, "knowledge": 15}, status="million_mile_driver", hidden_risk_log="长途货运守住不疲劳驾驶铁律，平平安安撑起全家生计。"),
                make_outcome("entangled", 15, "因在服务区休息延误两小时被货主要求扣发两百元迟到违约金，坦然接受。", {"wealth": -10, "mentality": 15}, hidden_risk_log="宁丢数百违约金绝不玩命疲劳驾驶，以理智避开致命车祸。")
            ]
        },
        {
            "text": "为赶货主高额早到奖励连灌两罐浓茶强撑瞌睡，盲目紧咬前车超速夜行",
            "choiceTags": ["时代：1980–2026", "年龄：22–50", "地域：高速干线", "门槛：盲目赶路司机"],
            "outcomes": [
                make_outcome("injured", 60, "下半夜极度瞌睡瞬间打盹追尾防护栏，车头变形导致右小腿骨折与面部碎玻璃划伤。", {"health": -35, "wealth": -35}, status="injured_trucker", hidden_risk_log="长途夜驾打瞌睡发生追尾骨折，修车赔款惨痛折损家底。"),
                make_outcome("safe", 36, "在车轮擦响路边震动减速标线时猛然惊醒急打方向死里逃生，后背湿透再不敢硬撑。", {"mentality": -20, "knowledge": 20}, hidden_risk_log="震动标线惊醒捡回一条命，从此对安全驾驶怀敬畏之心。"),
                make_outcome("fatal", 4, "在高速长下坡因严重瞌睡失控冲破水泥防撞墙坠落山崖不幸遇难。", is_fatal=True, hidden_risk_log="长途货运疲劳驾驶失控坠崖不幸遇难。")
            ]
        }
    ]
)

# 3. 建筑高空作业与防护
add_evt(
    "evt_traj_jianzhu_gaokong", "trajectory", "高层建筑施工：脚手架高空防坠与双钩保险",
    [1970, 2026], [18, 55], ["ALL"], {},
    ["worker"], [], 0.80, 4, "确证",
    "改革开放以来中国城镇化建设一日千里，高楼大厦拔地而起。建筑脚手架搭设、钢筋绑扎和高空临边作业中，‘安全带高挂低用’与临边防护网是保命防线。",
    "四十米高的脚手架外挂着密目式安全网，高空气流呼啸吹刮。工友们踩在跳板上绑扎框架柱钢筋，脚下是悬空的深渊。安全员挂着红袖标在塔吊下大声吹哨巡查：‘安全带双钩必须全挂牢！’",
    [
        {
            "text": "严格遵照高空作业规范，将双大钩安全绳紧紧扣在坚固钢梁上，高挂低用规范施工",
            "choiceTags": ["时代：1970–2026", "年龄：18–55", "地域：城市建筑工地", "门槛：建筑架子工/钢筋工"],
            "outcomes": [
                make_outcome("safe", 80, "一丝不苟完成数十层高楼主体钢筋施工，工期零事故荣获鲁班奖工程优秀劳务标兵。", {"wealth": 30, "knowledge": 20, "mentality": 25}, status="construction_safety_master", hidden_risk_log="高空施工作业牢固系好安全带，靠精湛手艺在城市建设中站稳脚跟。"),
                make_outcome("injured", 18, "风大湿滑踩空跳板摔落半米被安全绳牢牢拉住悬挂半空，虽保全性命但肋软骨轻度挫伤。", {"health": -20, "wealth": 15}, hidden_risk_log="安全绳在踩空瞬间挽救生命，深切感受制度规范的生命分量。"),
                make_outcome("fatal", 2, "遭遇强对流极端阵风刮塌脚手架主立杆整体失稳突发倾覆不幸坠落。", is_fatal=True, hidden_risk_log="建筑施工遭遇突发强阵风脚手架倾覆不幸殉职。")
            ]
        },
        {
            "text": "嫌安全绳来回倒挂繁琐影响进度，图省事在临边无防护跳板上解开挂钩干活",
            "choiceTags": ["时代：1970–2026", "年龄：18–50", "地域：高空施工临边", "门槛：侥幸违章工人"],
            "outcomes": [
                make_outcome("injured", 65, "踩到未绑扎的探头跳板失足从二楼脚手架坠落跌入安全兜网扭伤腰椎，停工休养两月。", {"health": -35, "wealth": -20}, status="injured_builder", hidden_risk_log="违章解开安全绳坠落落网致腰伤，侥幸保命彻底长记性。"),
                make_outcome("safe", 31, "被巡场项目总监当场严厉喝止抓现行，被罚款两百元并在全工地大会做检讨。", {"wealth": -10, "mentality": -15, "knowledge": 20}, hidden_risk_log="违章被重罚点醒，避免了潜在高空坠亡风险。"),
                make_outcome("fatal", 4, "在高层临边倒退运送钢筋时失足踏空高空坠落不幸罹难。", is_fatal=True, hidden_risk_log="高空临边违章未系安全绳失足坠落不幸罹难。")
            ]
        }
    ]
)

# 4. 外卖快递风雨骑行
add_evt(
    "evt_traj_qishou_fengyu", "trajectory", "即时配送骑手：暴雨积水与倒计时安全博弈",
    [2012, 2026], [18, 48], ["ALL"], {"urbanRural": "urban"},
    ["worker"], [], 0.85, 4, "确证",
    "移动互联网普及后数百万外卖骑手与快递员穿梭在城市大街小巷。恶劣天气爆单与平台倒计时考核构成了骑手日常的真实生活写照。",
    "暴雨倾盆浇打在头盔面罩上，手机喇叭尖锐急促地播报：‘您有新的外卖订单，距离超时还有8分钟！’车道积水深达半轮，电瓶车轮胎在湿滑斑马线上打滑，前方十字路口黄灯正在闪烁。",
    [
        {
            "text": "宁可超时扣除少许配送费，果断减速慢行，换穿高亮防滑雨衣，过路口坚决停车守红灯",
            "choiceTags": ["时代：2012–2026", "年龄：18–48", "地域：城市街区", "门槛：外卖配送骑手"],
            "outcomes": [
                make_outcome("safe", 85, "暴雨天全天跑完四十单无一宗事故与差评，顾客暖心发来五星好评与小费打赏。", {"wealth": 25, "mentality": 25, "family": 15}, status="safe_delivery_rider", hidden_risk_log="风雨骑行坚守安全慢行底线，平安将每一份餐食送达万家。"),
                make_outcome("entangled", 15, "因暴雨减速慢行三单轻微超时被系统扣除二十元，但换来人身绝对平安。", {"wealth": -10, "mentality": 10}, hidden_risk_log="以微小超时扣款守住人车平安，理智抵御算法狂奔诱惑。")
            ]
        },
        {
            "text": "为抢准时率避免差评，在湿滑雨夜加速超车闯黄灯，单手骑车看手机导航",
            "choiceTags": ["时代：2012–2026", "年龄：18–45", "地域：雨夜街头", "门槛：赶时间骑手"],
            "outcomes": [
                make_outcome("injured", 65, "在积水处紧急刹车导致电动车侧滑侧翻，膝盖半月板撕裂挫伤伴双手擦伤破皮。", {"health": -30, "wealth": -25}, status="injured_rider", hidden_risk_log="雨天赶单盲目超速侧滑摔伤，修车看病耗尽半月收入。"),
                make_outcome("safe", 32, "路口险些与右转泥头车剐蹭擦肩而过，吓出一身冷汗立刻靠边停车检讨。", {"mentality": -25, "knowledge": 20}, hidden_risk_log="雨夜惊险避开盲区死里逃生，彻底戒除闯黄灯恶习。"),
                make_outcome("fatal", 3, "在暴雨视野极差路口逆行闯红灯遭遇货车盲区撞击不幸罹难。", is_fatal=True, hidden_risk_log="外卖配送严重违章闯红灯遭遇车祸不幸遇难。")
            ]
        }
    ]
)

# 5. 远洋渔民遭遇海上风暴
add_evt(
    "evt_traj_yumin_fenglang", "trajectory", "远洋近海捕捞：狂风巨浪与甲板抢网",
    [1937, 2026], [18, 55], ["华东", "华南"],
    {}, ["farmer", "worker"], [], 0.78, 4, "确证",
    "沿海渔民长年在海上搏击风浪。从早期的木质帆船到现代千吨钢质远洋拖网渔船，起网机绞缠、风浪打湿失足落水是渔业生产的固有风险。",
    "海面上天空瞬间黑压压压下，海浪高达四五米如巨兽般拍打在钢铁甲板上。渔船在浪尖剧烈横摇三十度，拖网机正从滚滚黑浪中死死拉起沉甸甸的大网，缆绳在狂风中紧绷得吱吱作响。",
    [
        {
            "text": "穿好救生衣系紧甲板安全绳，遵照老船长指令立刻启动备用缆索抢护渔网固定重物",
            "choiceTags": ["时代：通用时代", "年龄：18–55", "地域：沿海/远洋渔场", "门槛：海船渔民"],
            "outcomes": [
                make_outcome("safe", 80, "全船合力抢回数十吨金枪鱼和鲳鱼大网并安全驶入避风港，分得丰厚出海渔利分红。", {"wealth": 35, "mentality": 25, "knowledge": 20}, status="ocean_fishing_veteran", hidden_risk_log="搏击风浪规范系挂安全绳，凭借过硬航海本领满载凯旋。"),
                make_outcome("injured", 18, "巨浪打上甲板被漂移的渔箱撞伤右小腿软组织挫伤，船医敷贴冰袋后平安回港。", {"health": -20, "wealth": 25}, hidden_risk_log="甲板抗风浪负轻微挫伤，平安随船满载而归。"),
                make_outcome("fatal", 2, "在固定船艏缆桩时遭遇十米巨浪拍击卷入狂暴深海不幸牺牲。", is_fatal=True, hidden_risk_log="在远洋渔船遭遇特大风浪抢险中不幸坠海牺牲。")
            ]
        },
        {
            "text": "在狂晃甲板上嫌救生衣笨重脱在一旁，徒手靠近飞速旋转的起网机绞盘拉网绳",
            "choiceTags": ["时代：通用时代", "年龄：18–50", "地域：渔船甲板", "门槛：盲动冒险渔工"],
            "outcomes": [
                make_outcome("injured", 65, "右手手套被绞盘缆绳卷入导致右手中指远端压榨骨折，老船长紧急拉闸刹车救出保命。", {"health": -35, "wealth": 10}, status="injured_deckhand", hidden_risk_log="甲板违章操作致指骨骨折留残疾，深刻吸取海上血的教训。"),
                make_outcome("safe", 31, "一个趔趄险些翻过船舷栏杆被大副一把拽回甲板痛骂，从此救生衣绝不离身。", {"mentality": -20, "knowledge": 25}, hidden_risk_log="大副神手拉回捡得一命，彻底根除麻痹侥幸心理。"),
                make_outcome("fatal", 4, "在船尾起网遭遇巨浪拍击未穿救生衣落入冰冷海水中失踪牺牲。", is_fatal=True, hidden_risk_log="海上起网未着救生衣失足落水不幸罹难。")
            ]
        }
    ]
)

# 6. 消防排险灭火
add_evt(
    "evt_traj_xiaofang_jiuyuan", "trajectory", "火场逆行：浓烟化工排险与生命救援",
    [1950, 2026], [18, 45], ["ALL"], {},
    ["worker", "cadre_teacher"], [], 0.80, 4, "确证",
    "消防救援队伍是和平时期同危险最贴近的钢铁力量。从老式帆布水带到现代重型防化服与破拆机器人，消防指战员在火海浓烟中筑起守护群众平安的血肉长城。",
    "刺耳的警铃撕破深夜宁静，居民楼顶层火舌翻卷冲天，夹杂着煤气罐爆炸的沉闷巨响。防毒面罩里回荡着沉重的呼吸声，水枪喷射出白龙般的高压水柱，热浪烤得防护服隔热手套滚烫发焦。",
    [
        {
            "text": "严格佩戴空气呼吸器与热成像仪，在水枪掩护下深入浓烟腹地背出受困被烧伤老人",
            "choiceTags": ["时代：1950–2026", "年龄：18–45", "地域：火场一线", "门槛：消防救援战士"],
            "outcomes": [
                make_outcome("safe", 75, "成功救出两名受困群众并扑灭猛烈大火，荣立个人二等功，被授予‘火海铁汉’荣誉奖章。", {"mentality": 40, "knowledge": 25, "wealth": 20}, status="firefighter_rescue_hero", hidden_risk_log="火场逆行勇救群众立大功，铸就无愧于时代的钢铁卫士荣光。"),
                make_outcome("injured", 22, "救人途中遭遇吊顶石膏板坍塌砸伤右肩胛骨并造成面颊轻度热灼伤，抢救群众生还后就医。", {"health": -25, "mentality": 30, "wealth": 15}, status="wounded_firefighter", hidden_risk_log="火海舍己救人负灼烫轻伤，赢得人民群众长久尊崇。"),
                make_outcome("fatal", 3, "在撤离最后关头突遇化工物料二次闪爆坍塌壮烈牺牲。", is_fatal=True, hidden_risk_log="在火灾抢险一线搜救受困群众时壮烈牺牲。")
            ]
        },
        {
            "text": "负责火场外围远距离大口径水炮供水压制与开辟外部逃生云梯通道",
            "choiceTags": ["时代：1950–2026", "年龄：18–45", "地域：火场外围", "门槛：消防战勤人员"],
            "outcomes": [
                make_outcome("safe", 90, "精准操控云梯车疏散数十名顶楼被困居民，供水干线无一中断，获评战勤保障模范标兵。", {"knowledge": 30, "wealth": 20, "mentality": 25}, status="fire_support_master", hidden_risk_log="精湛操控现代化消防装备挽救大批生命，成为战勤中坚。"),
                make_outcome("injured", 10, "收拢沉重水带时因水锤高压后坐力扭伤手腕软组织，冰敷休养一周。", {"health": -15, "mentality": 20}, hidden_risk_log="火场战勤负轻微扭伤，恪尽职守保卫城市安宁。")
            ]
        }
    ]
)

# 7. 乡村基层教师咽炎与家访
add_evt(
    "evt_traj_jiaoshi_yanyan", "trajectory", "乡村三尺讲台：数十载粉笔灰与翻山家访",
    [1950, 2026], [20, 60], ["ALL"], {"urbanRural": "rural"},
    ["cadre_teacher"], [], 0.85, 4, "确证",
    "乡村教师是照亮大山深处孩子的灯塔。常年吸入黑板粉笔灰导致慢性咽喉炎，翻山越岭家访劝返辍学儿童，托举起一代代农家子弟走向广阔天地。",
    "乡村小学的木窗外大雨连绵，黑板上写满了工整的拼音与算术。老师的声音已有些沙哑，口袋里常备着润喉糖。傍晚放学，山路泥泞，老师打着手电筒翻过两道山梁去劝说一户打算让女儿辍学的农家。",
    [
        {
            "text": "拿出微薄工资资助贫困学生学杂费，走几十里山路家访促成孩子重返课堂，自备护嗓茶坚持教学",
            "choiceTags": ["时代：1950–2026", "年龄：20–60", "地域：乡村小学", "门槛：乡村人民教师"],
            "outcomes": [
                make_outcome("safe", 85, "班上数十名农家孩子全部考取中专大学走出大山，成为名扬全县的‘最美乡村教师’，桃李满天下。", {"knowledge": 35, "mentality": 35, "family": 30}, status="beloved_rural_teacher", hidden_risk_log="扎根山乡教书育人三十载，以心血托举几代山里娃改变命运。"),
                make_outcome("injured", 15, "常年粉笔粉尘刺激患上慢性肥厚性咽喉炎伴声带小结，经中药雾化调理坚守讲台。", {"health": -20, "knowledge": 30, "mentality": 25}, hidden_risk_log="执教生涯落下慢性咽喉病，但深受全体乡民与弟子世代爱戴。")
            ]
        },
        {
            "text": "带领学生自制简易物理化学教具，利用课余开辟校园小菜园传授科学种植",
            "choiceTags": ["时代：1950–2026", "年龄：20–55", "地域：乡村学校", "门槛：实干乡村教师"],
            "outcomes": [
                make_outcome("safe", 90, "寓教于乐培养出学生的浓厚科学兴趣，学校小发明在市科技创新大赛荣获一等奖。", {"knowledge": 30, "wealth": 15, "mentality": 25}, status="creative_educator", hidden_risk_log="自制教具启蒙乡村孩子科学梦想，展现卓越教育智慧。"),
                make_outcome("injured", 10, "雨天山路护送低年级留守儿童回家失足滑倒擦伤手肘与膝盖，所幸护住孩子未伤。", {"health": -15, "mentality": 25}, hidden_risk_log="护送学童滑跌负轻伤，铸就山乡师表崇高风范。")
            ]
        }
    ]
)

# 8. 医护急诊抗疲劳与院感防护
add_evt(
    "evt_traj_yihu_jizhen", "trajectory", "医院白衣天使：急诊连轴转与防锐器伤感染",
    [1960, 2026], [22, 55], ["ALL"], {},
    ["cadre_teacher"], [], 0.85, 4, "确证",
    "医院医护人员长年奋战在救死扶伤一线。面对急危重症抢救、昼夜三班倒和针刺伤暴露风险，以高度责任心筑起公共卫生第一道堤坝。",
    "急诊抢救室监护仪嘀嘀报警，推车轮子在地砖上急速飞驰。大咯血患者血氧饱和度急速下坠，年轻护士戴着护目镜双层手套迅速开通静脉通路。窗外夜色深沉，白大褂已被汗水彻底浸湿透。",
    [
        {
            "text": "严格遵照院感无菌操作规程，规范使用安全留置针与防锐器盒，沉着参与危重病人复苏",
            "choiceTags": ["时代：1960–2026", "年龄：22–55", "地域：医院急诊/病区", "门槛：专业医护人员"],
            "outcomes": [
                make_outcome("safe", 85, "规范施救成功逆转三名心跳骤停患者生命，无一例院感差错，晋升为主管护师/副主任医师。", {"knowledge": 35, "mentality": 30, "wealth": 20}, status="master_clinician", hidden_risk_log="医术精湛严谨守纪，在救死扶伤一线成为同行与病患信赖的骨干医圣。"),
                make_outcome("injured", 15, "夜班连轴转高强度救护引发急性下肢静脉曲张伴重度腰背酸痛，穿弹力袜调适。", {"health": -20, "knowledge": 25}, hidden_risk_log="长期站立急救落下静脉曲张轻疾，一生拯救生命无数。")
            ]
        },
        {
            "text": "连做三台急诊手术极度疲劳双手颤抖，回套针帽时不慎遭遇带血针头刺破指腹",
            "choiceTags": ["时代：1960–2026", "年龄：22–50", "地域：医院抢救室", "门槛：疲劳医护人员"],
            "outcomes": [
                make_outcome("safe", 70, "立即从近心端挤出血液并流动水冲洗碘伏消毒，第一时间服用阻断药阻断成功，虚惊一场。", {"knowledge": 25, "mentality": 15}, status="prudent_medic", hidden_risk_log="针刺伤规范阻断自救成功，从此严守不双手回套针帽铁律。"),
                make_outcome("injured", 30, "针刺伤局部化脓感染伴高热两周，经强力抗生素静滴治疗后痊愈留下轻微指端麻木。", {"health": -25, "mentality": -15}, hidden_risk_log="职业暴露感染经受惊魂大考，更加深刻理解院感防护规程重要性。")
            ]
        }
    ]
)

# 9. 程序员长期久坐熬夜与健康维保
add_evt(
    "evt_traj_chengxuyuan_996", "trajectory", "信息产业研发：通宵攻坚与腰椎颈椎保卫战",
    [1995, 2026], [22, 50], ["ALL"], {"urbanRural": "urban"},
    ["worker", "cadre_teacher"], [], 0.85, 4, "确证",
    "中国互联网与软件信息技术产业飞速发展，催生了数百万研发工程师。高强度高脑力劳作下，‘996’加班、颈椎病和腰椎间盘突出成为普遍的职业健康挑战。",
    "深夜科技园大厦灯火通明，敲击机械键盘的噼啪声不绝于耳。咖啡杯在桌角堆了三四个，屏幕上数千行代码正在跑编译单元测试。后腰传来一阵钻心的酸痛，程序员伸手揉了揉僵硬发胀的后颈。",
    [
        {
            "text": "注重工位人效人体工程学，坚持番茄工作法每小时起身做拉伸，下班坚持慢跑游泳",
            "choiceTags": ["时代：1995–2026", "年龄：22–50", "地域：科技园区", "门槛：IT研发工程师"],
            "outcomes": [
                make_outcome("safe", 80, "高质高效攻克大型分布式底层框架架构，体魄硬朗远离颈椎病，晋升为大厂资深技术专家。", {"wealth": 35, "knowledge": 35, "mentality": 25}, status="healthy_tech_lead", hidden_risk_log="在脑力高压行业中找到身心平衡，技术进阶与健康长寿两不误。"),
                make_outcome("injured", 20, "项目攻坚上线连熬三宿导致轻度颈椎曲度变直头晕恶心，针灸理疗两周后改善。", {"health": -20, "wealth": 25}, hidden_risk_log="阶段攻坚透支颈椎，及时通过正骨复健恢复。")
            ]
        },
        {
            "text": "长期窝在软椅上连续十几个小时不喝水不起身，靠高糖能量饮料通宵硬熬写代码",
            "choiceTags": ["时代：1995–2026", "年龄：22–45", "地域：写字楼工位", "门槛：严重久坐程序员"],
            "outcomes": [
                make_outcome("injured", 65, "突发腰椎间盘膨出压迫坐骨神经痛得无法下床，卧床牵引治疗一月转为站立办公。", {"health": -35, "wealth": -15}, status="disc_herniation_patient", hidden_risk_log="严重缺乏运动久坐致腰突重疾，彻底痛改前非养成运动习惯。"),
                make_outcome("injured", 31, "长期喝能量饮料暴饮暴食导致急性肾结石剧烈绞痛急诊碎石，住院三天。", {"health": -25, "wealth": -10}, hidden_risk_log="不良饮水作息引发结石重痛，从此养成大口饮白水作风。"),
                make_outcome("fatal", 4, "连续高强度加班熬夜后突发恶性室性心律失常心源性猝死不幸英年早逝。", is_fatal=True, hidden_risk_log="长期重度熬夜透支身体不幸发生心源性猝死。")
            ]
        }
    ]
)

# 10. 个体商户现金流与摆摊守店
add_evt(
    "evt_traj_getihu_jingying", "trajectory", "个体小微经营：起早贪黑进货与货款防坑",
    [1980, 2026], [20, 60], ["ALL"], {},
    ["merchant"], [], 0.85, 4, "确证",
    "亿万个体工商户是中国市场经济最活跃的微观细胞。夫妻店、早点铺、服装小档口起早贪黑，面临货款拖欠、库存积压与租金博弈等现实考验。",
    "凌晨四点的批发市场卸货区水汽弥漫，货车铁门砰砰作响。手推车装满大捆衣服和新鲜蔬菜穿梭在过道里。计算器归零的声音清脆作响，小账本上密密麻麻记着每一批进货价与欠条明细。",
    [
        {
            "text": "坚持现款现货规避赊账风险，诚信经营童叟无欺，注重商品品质赢得回头客口碑",
            "choiceTags": ["时代：1980–2026", "年龄：22–60", "地域：城镇商业街巷", "门槛：个体经营户"],
            "outcomes": [
                make_outcome("safe", 85, "十年如一日童叟无欺积累上千老熟客，店面稳步扩大为连锁便民超市，家庭经济大幅跃升。", {"wealth": 40, "family": 25, "mentality": 25}, status="prosperous_honest_merchant", hidden_risk_log="靠诚信实干立足商海，现金流健康稳健，成为社区金字招牌。"),
                make_outcome("injured", 15, "清晨起早卸货搬运沉重货物拉伤腰大肌，老伴贴膏药揉敷三天后继续开店迎客。", {"health": -15, "wealth": 25}, hidden_risk_log="辛勤劳作负轻度腰肌劳损，柴米油盐换来全家殷实。")
            ]
        },
        {
            "text": "轻信陌生大客户口头许诺盲目大量垫资赊销高档货物，遭遇空壳跑路催债无门",
            "choiceTags": ["时代：1980–2026", "年龄：22–55", "地域：商贸集市", "门槛：盲信赊销老板"],
            "outcomes": [
                make_outcome("entangled", 65, "被卷走半年流动资金打官司追讨未果，陷入资金链断裂危机靠亲友借款艰难保本。", {"wealth": -40, "mentality": -30}, status="debt_trapped_merchant", hidden_risk_log="商业轻信赊销蒙受重大呆账损失，惨痛交学费后建立严格风控。"),
                make_outcome("safe", 35, "果断向法院申请财产保全查封对方抵押货车追回七成货款，有惊无险渡过难关。", {"wealth": 15, "knowledge": 25}, hidden_risk_log="拿起法律武器维权追损，在商海沉浮中淬炼出精明法商。")
            ]
        }
    ]
)

# 11. 长期吸烟与戒烟自律
add_evt(
    "evt_traj_xiyan_copd", "trajectory", "健康抉择：长期吸烟咳嗽与果断戒烟保肺",
    [1937, 2026], [25, 75], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "烟草消费在中国历史悠久，从早期的旱烟袋到卷烟。医学明确证明吸烟是慢阻肺（COPD）、冠心病和肺癌的首要危险因素，戒烟越早健康获益越大。",
    "清晨醒来喉咙里像着了火，剧烈的干咳咳得胸口发疼，一口浓稠的黄痰吐在痰盂里。烟灰缸里堆满了泛黄的过滤嘴烟蒂，手指尖被尼古丁熏得焦黄。爬上三楼就已气喘吁吁，呼吸科医生严肃地指着胸片上的肺纹理增粗。",
    [
        {
            "text": "痛下决心彻底戒烟，扔掉打火机与烟盒，坚持含薄荷糖并在早晨慢跑替代尼古丁依赖",
            "choiceTags": ["时代：通用时代", "年龄：25–70", "地域：全国", "门槛：烟民觉醒者"],
            "outcomes": [
                make_outcome("safe", 85, "成功彻底戒断烟瘾，咳嗽咳痰彻底消失，肺活量大幅提升，晚年远离慢阻肺与心脑血管危机。", {"health": 35, "mentality": 30, "wealth": 15}, status="successful_smoking_quitter", hidden_risk_log="果断戒烟彻底挽救肺部健康，为中老年筑牢强健体魄底子。"),
                make_outcome("entangled", 15, "戒断期初一月出现严重焦躁失眠与食欲亢进体重增加十斤，经半年调适归于正常。", {"mentality": -10, "health": 20}, hidden_risk_log="克服戒断反应成功脱敏，意志力经受严峻考验后焕然新生。")
            ]
        },
        {
            "text": "抱持“饭后一支烟赛过活神仙”的侥幸心态继续每天抽一包半，拒绝医生规劝",
            "choiceTags": ["时代：通用时代", "年龄：30–75", "地域：全国", "门槛：重度烟民"],
            "outcomes": [
                make_outcome("injured", 65, "确诊慢性阻塞性肺疾病（COPD）二期，活动耐力严重下降，常年离不开吸入剂喷雾。", {"health": -40, "wealth": -20}, status="copd_patient", hidden_risk_log="顽固吸烟引发慢性阻塞性肺病，后半生饱受呼吸困难折磨。"),
                make_outcome("injured", 31, "诱发重度冠状动脉痉挛狭窄出现心绞痛，不得不入院放置心脏支架一枚。", {"health": -40, "wealth": -35}, status="stent_patient", hidden_risk_log="吸烟促发冠心病严重心梗放置支架，身体元气大受折损。"),
                make_outcome("fatal", 4, "晚年因重度吸烟恶化并发中央型肺鳞癌并转移不幸离世。", is_fatal=True, hidden_risk_log="长期重度吸烟最终引发恶性肺癌不幸病逝。")
            ]
        }
    ]
)

# 12. 嗜酒与急性胰腺炎危机
add_evt(
    "evt_traj_yinjiu_yixian", "trajectory", "餐桌应酬：过量烈酒与急性消化道警讯",
    [1937, 2026], [22, 70], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "饮酒应酬文化在人情社会广泛存在。酗酒不仅增加脂肪肝、肝硬化风险，暴饮暴食更极易诱发致命的急性重症胰腺炎。",
    "酒桌上酒杯叮当，白酒香气刺鼻。同桌人起哄劝酒‘感情深一口闷’。几大杯高度白酒灌下肚，胃里翻江倒海。半夜回到家中上腹部突然传来刀割般的剧烈剧痛，冷汗瞬间浸透了衣衫。",
    [
        {
            "text": "坚决守住饮酒底线，以茶代酒婉拒拼酒陋习，日常生活中滴酒不沾注重养胃",
            "choiceTags": ["时代：通用时代", "年龄：22–65", "地域：全国", "门槛：理性养生者"],
            "outcomes": [
                make_outcome("safe", 90, "肝功能终身健康指标一清二白，无酒精性脂肪肝困扰，赢得意气风发的健康体魄。", {"health": 30, "family": 25, "mentality": 20}, status="sober_healthy_life", hidden_risk_log="拒绝酗酒陋习守护内脏健康，平平安安享受健康天伦。"),
                make_outcome("entangled", 10, "酒席上因坚持不喝酒被个别酒友冷嘲热讽扫兴，坦然面对不伤和气。", {"mentality": -10, "health": 15}, hidden_risk_log="顶住劝酒压力守住健康底线，展现强大定力。")
            ]
        },
        {
            "text": "贪杯逞能与人斗酒连喝一斤高度白酒伴随大鱼大肉，引发急性坏死性胰腺炎急诊抢救",
            "choiceTags": ["时代：通用时代", "年龄：22–65", "地域：酒席餐桌", "门槛：嗜酒拼酒者"],
            "outcomes": [
                make_outcome("injured", 65, "剧痛休克送ICU重症监护室腹腔穿刺引流抢救十天捡回一条命，花费数万元医疗费彻底戒酒。", {"health": -45, "wealth": -40}, status="pancreatitis_survivor", hidden_risk_log="暴饮暴食诱发重症胰腺炎ICU死里逃生，以惨痛代价彻底戒酒。"),
                make_outcome("injured", 31, "急性胃出血呕吐咖啡色液体急诊胃镜止血，留院观察一周后老实喝小米粥养胃。", {"health": -30, "wealth": -20}, hidden_risk_log="酗酒致急性胃黏膜病变大出血，深刻认清酒精之害。"),
                make_outcome("fatal", 4, "严重酒精中毒并发重症坏死性胰腺炎导致多器官功能衰竭不幸离世。", is_fatal=True, hidden_risk_log="因过量酗酒暴饮暴食诱发重度胰腺炎多器官衰竭不幸罹难。")
            ]
        }
    ]
)

# 13. 野外游泳水草暗流遇险
add_evt(
    "evt_traj_yeyong_choujin", "trajectory", "夏日水域：野外江河嬉水与突发抽筋自救",
    [1937, 2026], [10, 55], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "夏日野泳是许多青少年和水乡居民的爱好。未开发野外水域水温温差大、水草缠足和水下暗流漩涡常常是溺水事故的元凶。",
    "炎炎烈日烤得水面波光粼粼，无人的水库深潭绿得发黑。几个年轻人脱掉衣服扑通跳入清凉的水中。游到水库中央深水区时，一股冰凉的暗流从脚底掠过，右小腿腓肠肌突然剧烈抽筋痉挛缩成一团！",
    [
        {
            "text": "绝不盲目挣扎，深吸一口气仰卧漂浮在水面，用手用力扳住右脚大脚趾向身体方向拉伸解痉，大声呼救",
            "choiceTags": ["时代：通用时代", "年龄：10–55", "地域：江河水库", "门槛：水性良好且冷静者"],
            "outcomes": [
                make_outcome("safe", 80, "以标准仰面漂浮成功缓解小腿痉挛，同伴合力递过竹竿拉上岸脱险，从此野泳只在安全浅滩。", {"knowledge": 25, "mentality": 25, "health": -5}, status="water_rescue_survivor", hidden_risk_log="水中突发抽筋冷静仰面自救化险为夷，掌握终生保命涉水技能。"),
                make_outcome("injured", 17, "在水下被隐蔽水草割伤双小腿皮肉，呛水两口被岸边老渔民划小木船救起上岸敷药。", {"health": -20, "mentality": 15}, hidden_risk_log="水库游泳遇险幸得救助，从此严守不进危险水域铁规。"),
                make_outcome("fatal", 3, "在水深暗流处极度慌乱挣扎被急流漩涡吸入水底不幸溺水身亡。", is_fatal=True, hidden_risk_log="在野外未开发水库深水区突发抽筋不幸溺亡。")
            ]
        },
        {
            "text": "不去危险野水潭，坚持在配有救生员的正规游泳馆或结伴佩戴‘跟屁虫’救生浮囊锻炼",
            "choiceTags": ["时代：通用时代", "年龄：10–55", "地域：正规泳池", "门槛：谨慎游泳爱好者"],
            "outcomes": [
                make_outcome("safe", 95, "常年科学游泳锻炼心肺功能强劲，远离野泳溺水隐患，荣获业余游泳达人称号。", {"health": 30, "mentality": 20}, status="safe_swimmer_master", hidden_risk_log="科学游泳强身健体，杜绝野外涉险，尽享运动益处。"),
                make_outcome("safe", 5, "在正规泳池协助救生员救助一名呛水儿童，受到馆方免年费褒奖。", {"knowledge": 20, "mentality": 20}, hidden_risk_log="泳池见义勇为救护学童，体现良好公民素养。")
            ]
        }
    ]
)

# 14. 荒野登山失温与救援
add_evt(
    "evt_traj_dengshan_shiwen", "trajectory", "户外徒步：高山突降风雨与重度失温险境",
    [1985, 2026], [16, 55], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "高山徒步探险风靡全国。高海拔地区天气瞬息万变，大风、降水和低温叠加极易迅速带走人体热量导致致命的‘失温’（Hypothermia）。",
    "山脊上海拔迅速攀升，浓雾笼罩四周，能见度不足五米。狂风夹杂着冰冷的冻雨抽打在单薄的冲锋衣上，湿透的内衣紧贴前胸。四肢开始不受控制地剧烈颤抖，言语不清，甚至出现反常的‘脱衣幻觉’。",
    [
        {
            "text": "发现失温征兆立刻停止行进，躲入背风巨石凹处，迅速换上备用干燥保暖羽绒，穿上铝箔保温毯抱团取暖",
            "choiceTags": ["时代：1985–2026", "年龄：16–55", "地域：高山野外", "门槛：具备户外急救常识者"],
            "outcomes": [
                make_outcome("safe", 80, "科学避风与保温毯保温成功逆转失温恶化，饮用保温水壶热水复温，天明后安全下撤脱险。", {"knowledge": 30, "mentality": 30, "health": -10}, status="mountaineering_survival_expert", hidden_risk_log="遭遇荒野高山风雨失温以专业自救化险为夷，成为成熟户外安全导师。"),
                make_outcome("injured", 17, "冻雨导致手脚二级冻伤红肿水疱，被当地蓝天救援队用担架连夜抬下山救治。", {"health": -30, "wealth": -10}, status="rescued_hiker", hidden_risk_log="户外登山失温受冻伤幸遇救援脱险，学会对自然抱持敬畏。"),
                make_outcome("fatal", 3, "在失温神智昏迷时失足滑坠下高山陡崖不幸遇难。", is_fatal=True, hidden_risk_log="荒野高山徒步遭遇极端天气重度失温不幸遇难。")
            ]
        },
        {
            "text": "在恶劣强降雨和大风预警发布后坚决取消冲顶冒险，果断折返农家乐围炉烤火",
            "choiceTags": ["时代：1985–2026", "年龄：16–55", "地域：山脚营地", "门槛：理智户外爱好者"],
            "outcomes": [
                make_outcome("safe", 95, "理智避开山区山洪泥石流与失温恶性天气，与同行驴友在农家乐喝土鸡汤平安畅谈。", {"family": 20, "mentality": 25, "health": 15}, status="prudent_outdoor_adventurer", hidden_risk_log="敬畏自然不盲目冒险，以成熟理性守护生命与家庭。"),
                make_outcome("safe", 5, "在农家乐热心帮助受惊的受困散客包扎扭伤脚踝，被大家推为领队。", {"knowledge": 20, "mentality": 20}, hidden_risk_log="营地助人体现团结互助精神，深受山友信赖。")
            ]
        }
    ]
)

# 15. 摩托车骑行压弯侧滑
add_evt(
    "evt_traj_motuo_yawen", "trajectory", "摩托骑行：山道弯道侧滑与全套护具救命",
    [1990, 2026], [18, 45], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "摩托车机车文化深受年轻人喜爱。山路压弯超速、盲区占道超车是主要事故诱因，而头盔、气囊骑行服和护膝等专业护具是防骨折保命的关键。",
    "山路盘旋风景优美，排气管轰鸣回荡在山谷。一辆重型摩托车以六十码速度进入连续盲弯，路面突然出现一片前车漏出的湿滑机油。车轮瞬间失去抓地力侧滑倒地，火星四溅贴着地面滑向护栏！",
    [
        {
            "text": "骑行全程严格穿戴全盔、气囊马甲、专业防摔皮衣与护膝，弯前提前减速绝不占道盲超",
            "choiceTags": ["时代：1990–2026", "年龄：18–45", "地域：山区公路", "门槛：规范摩托骑手"],
            "outcomes": [
                make_outcome("safe", 85, "压过油污侧翻瞬间气囊瞬间弹开充气吸收冲击，皮衣磨破但身体无一处骨折擦伤，扶车安全归家。", {"mentality": 25, "knowledge": 20, "wealth": -10}, status="armored_safe_rider", hidden_risk_log="全套专业护具与气囊在侧滑中挽救生命，彰显规范骑行文化价值。"),
                make_outcome("injured", 13, "侧翻时脚踝被摩托车发动机排气管轻度烫伤破皮，防摔手套磨穿掌心挫伤，包扎康复。", {"health": -20, "wealth": -15}, hidden_risk_log="护具保全大局受轻微烫伤挫伤，从此更加注重路况预判。"),
                make_outcome("fatal", 2, "在盲弯侧翻失控撞击迎面超速违章下山货车不幸牺牲。", is_fatal=True, hidden_risk_log="摩托车山道骑行遭遇盲弯对向车辆撞击不幸罹难。")
            ]
        },
        {
            "text": "为了拍照帅气仅戴半盔穿短袖T恤短裤骑行，并在狭窄山路盲区压中线高速超车",
            "choiceTags": ["时代：1990–2026", "年龄：18–40", "地域：山间公路", "门槛：盲目追求刺激骑手"],
            "outcomes": [
                make_outcome("injured", 65, "侧滑摔倒在柏油路面大面积深度擦伤见肉并伴右侧锁骨骨折，急诊清创缝合住院半月。", {"health": -40, "wealth": -30}, status="scarred_motorcyclist", hidden_risk_log="不穿护具盲目飙车受重度皮肤挫伤与骨折，痛苦长教训。"),
                make_outcome("safe", 31, "险些刮蹭护栏紧急刹停在悬崖边吓得两腿发抖，当场将摩托车托运回家换回代步车。", {"mentality": -25, "knowledge": 25}, hidden_risk_log="悬崖边缘死里逃生彻底戒除飙车恶习，回归平稳生活。"),
                make_outcome("fatal", 4, "高速压弯侧滑头部未戴合格全盔撞击水泥防护栏不幸当场身亡。", is_fatal=True, hidden_risk_log="摩托车无防护飙车碰撞不幸罹难。")
            ]
        }
    ]
)

# 16. 体检延误与早筛醒悟
add_evt(
    "evt_traj_tijian_yanwu", "trajectory", "健康体检：忽视角膜结节隐患与早筛干预",
    [1990, 2026], [30, 75], ["ALL"], {},
    [], [], 0.88, 4, "确证",
    "现代预防医学强调‘早发现、早诊断、早治疗’。低剂量螺旋CT、胃肠镜与常规生化体检对阻断肿瘤与心脑血管病变具有决定性意义。",
    "体检通知单在办公桌抽屉里放了三个月，总是借口‘工作忙没时间、身体没有任何感觉’一拖再拖。某日单位组织集体体检，在老伴的严厉催促下，终于走进体检中心做了一次全面的低剂量螺旋CT与消化内镜筛查。",
    [
        {
            "text": "克服畏难情绪认真完成全套胃肠镜与胸部CT筛查，积极听取专科医生随访指导",
            "choiceTags": ["时代：1990–2026", "年龄：30–75", "地域：全国", "门槛：重视健康体检者"],
            "outcomes": [
                make_outcome("safe", 85, "通过内镜顺便切除两枚早期高危腺瘤性息肉，成功彻底阻断肠道癌变，体魄硬朗安享晚年。", {"health": 35, "wealth": -10, "mentality": 25}, status="early_screening_beneficiary", hidden_risk_log="重视早筛早治阻断恶性肿瘤演进，成为家庭健康管理的明白人。"),
                make_outcome("safe", 15, "筛查各项指标均在正常范围，彻底打消多年健康焦虑心结，身心轻盈投入工作。", {"mentality": 30, "health": 20}, hidden_risk_log="全面体检吃下定心丸，树立科学自信健康观念。")
            ]
        },
        {
            "text": "抱持“不查没病一查一身病”的鸵鸟心理连续八年逃避体检，忽视持续上腹隐痛消瘦",
            "choiceTags": ["时代：1990–2026", "年龄：35–75", "地域：全国", "门槛：盲目逃避体检者"],
            "outcomes": [
                make_outcome("injured", 65, "因剧烈腹痛就医终确诊进展期胃溃疡出血并伴重度贫血，急诊手术切除部分胃体挽救生命。", {"health": -45, "wealth": -35}, status="delayed_diagnosis_patient", hidden_risk_log="长期拖延体检将小病拖成大病开刀，以肉体痛苦换取深刻教训。"),
                make_outcome("safe", 31, "在一次轻微外伤急诊抽血时偶然发现严重高血糖高血脂，幡然醒悟开始规范服药打针控糖。", {"health": 15, "knowledge": 25}, hidden_risk_log="偶然急诊检出代谢综合征醒悟自救，及时扭转健康滑坡。"),
                make_outcome("fatal", 4, "恶性肿瘤晚期多处广泛转移发现过晚错失手术根治窗口期不幸离世。", is_fatal=True, hidden_risk_log="长期逃避体检导致恶性肿瘤晚期未能早诊不幸病逝。")
            ]
        }
    ]
)

# 17. 长期通宵熬夜心律失常
add_evt(
    "evt_traj_aoye_zaobo", "trajectory", "作息危机：长期通宵熬夜与心脏频发早搏警示",
    [1980, 2026], [18, 55], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "长期颠倒昼夜、通宵熬夜追剧刷手机或加班，会导致交感神经过度兴奋、内分泌紊乱，引发功能性频发室性早搏乃至恶性心律失常。",
    "时钟已指向上午四点半，卧室里只有手机屏幕惨蓝的荧光。心脏突然猛烈地‘咯噔’漏跳了一拍，紧接着一阵心慌气短胸口发空。额头渗出虚汗，手脚冰凉，二十四小时动态心电图记录下数千次频发室性早搏。",
    [
        {
            "text": "高度警醒彻底戒绝熬夜，晚上十点半准时关闭手机电子产品入睡，坚持打八段锦养心",
            "choiceTags": ["时代：1980–2026", "年龄：18–55", "地域：全国", "门槛：作息觉醒者"],
            "outcomes": [
                make_outcome("safe", 85, "作息规律三个月后心律彻底恢复平稳规律，早搏全部消失，精神焕发气血充盈。", {"health": 35, "mentality": 30}, status="restored_rhythm_master", hidden_risk_log="彻底痛改熬夜恶习恢复规律作息，守护心脏心律安宁。"),
                make_outcome("injured", 15, "阶段性心肌劳损需口服稳心颗粒调理半年，心功能逐步稳固复原。", {"health": -15, "knowledge": 20}, hidden_risk_log="早搏警讯推动生活方式重构，因祸得福学会爱惜身体。")
            ]
        },
        {
            "text": "抱持年轻扛得住心态继续夜夜通宵达旦，困了狂喝冰咖啡提神打游戏",
            "choiceTags": ["时代：1980–2026", "年龄：18–45", "地域：卧室床头", "门槛：顽固熬夜青年"],
            "outcomes": [
                make_outcome("injured", 65, "频发室早恶化为短阵室速晕厥倒地摔破额头，急诊行心脏射频消融手术治疗入院一周。", {"health": -40, "wealth": -30}, status="ablation_patient", hidden_risk_log="顽固熬夜引发严重心律失常接受射频消融，惊魂之后彻底收敛。"),
                make_outcome("injured", 31, "长期黑白颠倒导致重度神经衰弱焦虑症脱发，不得不停工服药休养数月。", {"health": -25, "mentality": -25}, hidden_risk_log="熬夜透支神经系统饱尝失眠焦虑之苦，花大价钱调理康复。"),
                make_outcome("fatal", 4, "在连续两夜通宵后突发恶性心室颤动心源性猝死不幸英年离世。", is_fatal=True, hidden_risk_log="长期重度熬夜导致恶性室颤猝死不幸英年早逝。")
            ]
        }
    ]
)

# 18. 农田耕作农药安全防护
add_evt(
    "evt_traj_nongye_laoshun", "trajectory", "田间农事：农药喷洒安全防护与腰肌劳损防护",
    [1955, 2026], [16, 65], ["ALL"], {"urbanRural": "rural"},
    ["farmer"], [], 0.88, 4, "确证",
    "现代农业广泛使用高效低毒杀虫剂除草剂。农药配药喷洒必须顺风操作并佩戴口罩手套，违章逆风喷洒或误服极易引发有机磷等急性农药中毒。",
    "盛夏午后烈日当空，稻田里稻飞虱蔓延。沉重的喷雾器背在肩上压得肩膀生疼，压杆上下起伏，农药化作白色烟雾喷向稻株。迎面风向突然变动，刺鼻的农药水雾向面部扑来。",
    [
        {
            "text": "立即停止作业转移到上风口，严格戴好防毒口罩长袖衣裤与橡胶手套，清晨无风时规范作业",
            "choiceTags": ["时代：1955–2026", "年龄：16–65", "地域：广大农村田头", "门槛：懂科学农技农民"],
            "outcomes": [
                make_outcome("safe", 85, "高效彻底消灭稻飞虱保全秋粮高产，自身未吸收一丝毒素健康硬朗，被评为科学种田模范标兵。", {"wealth": 30, "health": 20, "knowledge": 25}, status="scientific_farming_pioneer", hidden_risk_log="遵守科学农药防护规程，既保住庄稼丰收又守住自身生命健康。"),
                make_outcome("injured", 15, "长时间背负数十斤药桶导致腰大肌急性扭伤，村医拔罐针灸敷贴后平复。", {"health": -15, "wealth": 20}, hidden_risk_log="农事重体力闪腰受轻劳损，换来金黄稻谷丰收。")
            ]
        },
        {
            "text": "嫌戴口罩橡胶手套闷热赤膊上阵，顶风逆风喷洒农药并用沾满农药的脏手拿馒头吃",
            "choiceTags": ["时代：1955–2026", "年龄：16–60", "地域：田间地头", "门槛：粗心大意农民"],
            "outcomes": [
                make_outcome("injured", 65, "经皮肤与消化道吸收导致急性轻度有机磷农药中毒，恶心呕吐瞳孔缩小送卫生院打阿托品脱险。", {"health": -35, "wealth": -15}, status="pesticide_poisoning_survivor", hidden_risk_log="逆风打农药中毒阿托品解毒抢救脱险，吸取深刻教训。"),
                make_outcome("safe", 32, "闻到异味剧烈呛咳立刻跳入水渠用肥皂彻底清洗干净，虚惊一场从此严格穿防护服。", {"health": -10, "knowledge": 20}, hidden_risk_log="肥皂冲水自救脱险，彻底改掉马虎耕作习惯。"),
                make_outcome("fatal", 3, "在烈日下重度有机磷农药中毒未及时被发现致肺水肿呼吸衰竭不幸罹难。", is_fatal=True, hidden_risk_log="在农田喷洒农药严重中毒未能及时救治不幸遇难。")
            ]
        }
    ]
)

# 保存 events_trajectory.json
out_dir = os.path.join(root, "data", "events")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "events_trajectory.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print(f"✅ Successfully written {len(events)} events to {out_path}!")
