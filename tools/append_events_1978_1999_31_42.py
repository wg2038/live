# tools/append_events_1978_1999_31_42.py
# -*- coding: utf-8 -*-
import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root)

import tools.append_events_1978_1999_21_42 as app
import tools.build_events_1978_1999_full as base
add_evt = base.add_evt
make_outcome = base.make_outcome

# 31. 1993 海南房地产泡沫破裂
add_evt(
    "evt_1993_hainan_pomo", "era", "1993海南房地产泡沫破裂与烂尾楼潮",
    [1993, 1995], [22, 55], ["ALL"], {},
    ["merchant"], [], 0.75, 4, "确证",
    "1993年6月国务院发布十六条整顿金融秩序措施，给过热的房地产踩下紧急刹车。海南、北海等地疯狂炒作地皮与楼花的泡沫瞬间破裂，留下数百栋烂尾楼与数千亿坏账沉淀。",
    "海口与三亚的滨海大道旁，昨夜还在击鼓传花的售楼处一夜间人去楼空。未封顶的钢筋混凝土框架在海风中生锈，炒房客抵押的存折与借据化为废纸，满大街都是慌乱催债的人群。",
    [
        {
            "text": "在调控前夕敏锐察觉危险，果断降价两成果断甩卖楼花地皮套现离场",
            "choiceTags": ["时代：1993–1995", "年龄：24–55", "地域：海南/沿海", "门槛：涉足地产商人"],
            "outcomes": [
                make_outcome("safe", 65, "成功在泡沫彻底破灭前落袋为安保住本金利润，在商界赢得极高声誉。", {"wealth": 50, "mentality": 30}, status="crisis_escape_survivor", hidden_risk_log="在海南房产大崩盘前全身而退，展现极强风险控制力。"),
                make_outcome("entangled", 35, "虽转手多处地块但被下游买家连累拖欠尾款数十万，追索三年未果。", {"wealth": -20, "mentality": -20}, hidden_risk_log="虽提前脱身仍受坏账三角债牵连，元气有所损伤。")
            ]
        },
        {
            "text": "抱持侥幸心理继续高杠杆接盘借贷炒楼，楼盘烂尾被银行与债主堵门",
            "choiceTags": ["时代：1993–1995", "年龄：24–50", "地域：海南/沿海", "门槛：盲目加杠杆者"],
            "outcomes": [
                make_outcome("entangled", 60, "资金链彻底断裂负债累累，不得不变卖家产潜回内地隐姓埋名自谋生路。", {"wealth": -55, "mentality": -40, "family": -25}, status="debt_crisis", hidden_risk_log="遭遇海南房地产泡沫破裂血本无归，历经数年艰难还债。"),
                make_outcome("safe", 30, "将烂尾楼宇改造成热带仓储和水产养殖基地，咬牙自救在数年后逐步翻盘。", {"wealth": 20, "knowledge": 25, "mentality": 25}, status="resilient_entrepreneur", hidden_risk_log="绝境中变通将烂尾资产盘活自救，展现极强商海韧性。"),
                make_outcome("injured", 10, "遭暴怒债权人雇凶追债殴打致右小腿骨折，在医院调养两月。", {"health": -30, "wealth": -30}, hidden_risk_log="深陷债务纠纷负伤，成为商海盲目加杠杆的惨痛烙印。")
            ]
        }
    ]
)

# 32. 1994 全国清理三角债
add_evt(
    "evt_1994_sanjiaozhai", "era", "全国清理“三角债”与企业资金链博弈",
    [1993, 1996], [22, 55], ["ALL"], {"urbanRural": "urban"},
    ["worker", "merchant"], [], 0.80, 4, "确证",
    "1990年代中前期企业间相互拖欠货款与工程款的‘三角债’恶疾蔓延全国，涉及数千亿元。朱镕基副总理铁腕主导注入源头清欠资金，斩断债务链条，规范市场商业信用。",
    "厂长办公室的大门整日被催款者堵得水泄不通。仓库里堆满了发不出工资而抵顶债款的铝合金门窗与布匹。财务桌上摊着厚厚的承兑汇票与欠条，每个人都在四处找款解套保生产。",
    [
        {
            "text": "坚守现款现货原则，严控垫资，亲自带队上门以物抵债追讨源头陈欠",
            "choiceTags": ["时代：1993–1996", "年龄：25–55", "地域：全国工矿企业", "门槛：销售业务骨干/企业主"],
            "outcomes": [
                make_outcome("safe", 65, "成功追回八成关键流动资金，保障了车间职工足额发薪与原料采购。", {"wealth": 30, "knowledge": 20, "mentality": 20}, status="clearing_champion", hidden_risk_log="在三角债危机中铁腕控风险追回欠款，保全企业生命线。"),
                make_outcome("injured", 25, "在东北异地讨债遭遇地方保护人员推搡殴打受皮肉伤，艰难讨回两成货款。", {"health": -20, "wealth": 10}, hidden_risk_log="跨省清欠讨债吃尽苦头负伤，磨炼出过人谈判魄力。"),
                make_outcome("entangled", 10, "被迫接受客户以三卡车滞销罐头抵顶二十万货款，全厂职工发罐头抵工资。", {"wealth": -15, "mentality": -15}, hidden_risk_log="抵顶回实物商品变现折价，体会到实体转型的沉重。")
            ]
        },
        {
            "text": "服从大局参与国家政策性注入清欠闭环，依规核销坏账专心技改升级",
            "choiceTags": ["时代：1993–1996", "年龄：22–55", "地域：国有重点厂矿", "门槛：国企中层骨干"],
            "outcomes": [
                make_outcome("safe", 70, "借助政府注资斩断债务链条，企业产品打入外贸新渠道重获生机。", {"knowledge": 25, "wealth": 20}, status="tech_upgraded", hidden_risk_log="依托国家清欠闭环甩掉历史包袱，投身技术革新。"),
                make_outcome("entangled", 30, "清欠后全厂实行分流减员降薪三成，生活清简节流支撑度日。", {"wealth": -15, "mentality": -10}, hidden_risk_log="企业资金紧张承受降薪分流，同舟共济渡难关。")
            ]
        }
    ]
)

# 33. 1994 分税制改革
add_evt(
    "evt_1994_fenshuizhi", "era", "分税制财政体制改革与国税地税分设",
    [1994, 1995], [22, 55], ["ALL"], {"urbanRural": "urban"},
    ["cadre_teacher"], [], 0.75, 4, "确证",
    "1994年1月中国推行重大分税制财政体制改革，建立中央与地方两套税收体制，设立国税局与地税局，理顺中央与地方分配关系，极大增强了中央宏观调控与国家财政实力。",
    "税务局大楼前挂起了两块崭新的大牌子，税务系统青年干部忙着整理增值税发票与核算系统。金税工程的大型计算机终端嗡嗡作响，现代税收征管制度正全面筑牢国之基石。",
    [
        {
            "text": "钻研金税工程计算机发票交叉稽核系统，成为税务改革首批微机骨干",
            "choiceTags": ["时代：1994–1995", "年龄：22–45", "地域：税务机关系统", "门槛：财经税务干部"],
            "outcomes": [
                make_outcome("safe", 75, "熟练掌握现代微机增值税防伪税控体系，晋升为分局业务股长荣立三等功。", {"knowledge": 30, "wealth": 20, "mentality": 20}, status="tax_expert", hidden_risk_log="抓住分税制与金税工程技术红利，成为财税现代化骨干。"),
                make_outcome("injured", 20, "高强度上机录入发票连续加班一个月导致严重颈椎病与干眼症。", {"health": -15, "knowledge": 25}, hidden_risk_log="电脑录入繁重累及颈椎眼部，但练就过硬计算机本领。"),
                make_outcome("entangled", 5, "因严格依法核查偷漏税遭遇个别不良商贩恶劣言语威胁恐吓。", {"mentality": -10}, hidden_risk_log="严守国家税法顶住外部压力，彰显公职人员浩然正气。")
            ]
        },
        {
            "text": "若为企业财务人员，全面学习增值税专票抵扣规范，严格依法纳税规避发票风险",
            "choiceTags": ["时代：1994–1995", "年龄：22–55", "地域：工商企业", "门槛：企业会计"],
            "outcomes": [
                make_outcome("safe", 80, "建立全套规范的现代企业财务发票台账，帮助公司规避数笔虚开假发票大坑。", {"knowledge": 25, "wealth": 20}, status="senior_accountant", hidden_risk_log="精通新税制为企业筑牢合规防线，深得管理层倚重信任。"),
                make_outcome("entangled", 20, "因旧账抵扣不符被税务所追缴罚款三千元，被老板责怪扣除当月奖金。", {"wealth": -10, "mentality": -15}, hidden_risk_log="初涉新税制吃罚款教训，更加严谨细致对待账目。")
            ]
        }
    ]
)

# 34. 1995 双休日工作制
add_evt(
    "evt_1995_shuangxiri", "era", "双休日工作制正式推行：告别“单休”历史",
    [1995, 1995], [16, 70], ["ALL"], {"urbanRural": "urban"},
    ["worker", "cadre_teacher", "tech_whitecollar"], [], 0.92, 3, "确证",
    "1995年5月1日起中国在全国机关、企事业单位正式实行每周5天工作制（双休日），从每周48小时、大小周过渡到法定双休，深刻改变了亿万职工的生活节奏与精神风貌。",
    "工厂星期五下午的下班铃声格外清脆，工人们换下蓝色工装互道‘周一见’。以往只有周日一天洗衣服洗被褥、喘不上气来的日子，如今多出了宝贵的一整天闲暇周末时光。",
    [
        {
            "text": "充分享受双休日闲暇，周末带全家逛公园野餐、教子女骑自行车",
            "choiceTags": ["时代：1995", "年龄：20–65", "地域：全国城镇", "门槛：工薪职工"],
            "outcomes": [
                make_outcome("safe", 85, "家庭和睦其乐融融，精神压力大为缓解，身体机能与心肺活力明显改善。", {"family": 25, "health": 15, "mentality": 20}, status="weekend_enjoyer", hidden_risk_log="沐浴双休日改革春风，家庭亲子关系与健康素质大幅跃升。"),
                make_outcome("safe", 15, "利用周六周日整修了老宅厨房管道，家里被收拾得窗明几净。", {"family": 15, "wealth": 5}, hidden_risk_log="利用富余闲暇料理家事，生活充满温馨烟火气。")
            ]
        },
        {
            "text": "利用多出来的周末两天从事第二职业副业，做课外辅导/电器零修/开夜市",
            "choiceTags": ["时代：1995", "年龄：22–50", "地域：城镇街市", "门槛：有技能副业者"],
            "outcomes": [
                make_outcome("safe", 70, "周末兼职每月额外增收五百元，家里迅速换上大屏幕彩电与全自动洗衣机。", {"wealth": 30, "health": -10}, status="sideline_master", hidden_risk_log="利用双休拼命打拼副业，成为率先享受消费升级的一批人。"),
                make_outcome("injured", 20, "常年无休兼职身心极度疲惫，患上偏头痛与顽固神经衰弱。", {"health": -25, "wealth": 25}, hidden_risk_log="周末透支体力搞副业累伤身体，后逐步回归健康平衡。"),
                make_outcome("entangled", 10, "兼职摆摊被单位同事碰见传为谈资，在办公室面对微言风语。", {"mentality": -15}, hidden_risk_log="早期搞副业面对体制内保守观念指点，坦然处之。")
            ]
        }
    ]
)

# 35. 1996 中国第一家网吧在上海开业
add_evt(
    "evt_1996_wangba_hulianwang", "era", "第一代网吧开业与早期互联网瀛海威",
    [1996, 1998], [15, 35], ["ALL"], {"urbanRural": "urban"},
    [], [], 0.75, 4, "确证",
    "1996年11月中国第一家电脑网络咖啡屋‘威雀网吧’在上海威海路开业。中关村竖起‘中国人离信息高速公路还有多远’巨幅广告，56K调制解调器拨号声开启了早期互联网大门。",
    "沉重的笨重CRT显示器前散发着主机的热气，耳畔是吱吱作响的猫（Modem）拨号音。屏幕上Netscape浏览器一点点加载出大洋彼岸的文字。青年学生聚精会神注册自己第一个电子邮箱。",
    [
        {
            "text": "拿出半月伙食费购买上网机时，潜心自学HTML网页制作与BBS社区发帖",
            "choiceTags": ["时代：1996–1998", "年龄：15–35", "地域：大中城市", "门槛：高校学生/科技青年"],
            "outcomes": [
                make_outcome("safe", 65, "熟练掌握早期网络建站技术，受聘为首批商业门户网站早班技术编辑，月薪翻倍。", {"knowledge": 35, "wealth": 25, "mentality": 20}, new_career_track="tech_whitecollar", status="internet_pioneer", hidden_risk_log="中国第一代网虫与互联网弄潮儿，提前跨入IT数字新时代。"),
                make_outcome("injured", 25, "通宵泡网吧眼睛严重干涩近视加深，且昼夜颠倒落下顽固胃炎。", {"health": -20, "knowledge": 25}, hidden_risk_log="沉迷早期网络熬夜伤身，但收获了前沿数字技能视野。"),
                make_outcome("entangled", 10, "昂贵的国际长途电话拨号费让家里收到上千元天价账单，被父母痛责。", {"wealth": -20, "family": -15}, hidden_risk_log="因昂贵上网费交学费，后转为规范控制上网时间。")
            ]
        },
        {
            "text": "认定互联网是富家子弟的虚无玩具，专心于现有工厂设备车间或农田营生",
            "choiceTags": ["时代：1996–1998", "年龄：18–50", "地域：全国", "门槛：传统工薪/农户"],
            "outcomes": [
                make_outcome("safe", 75, "恪守本分手艺赚工薪，生活节奏波澜不惊，免受网络虚火纷扰。", {"wealth": 10, "family": 15}, hidden_risk_log="恪守实体行当安稳度日，虽未沾互联网之光但也无风险。"),
                make_outcome("entangled", 25, "数年后面对电脑办公与无纸化普及显得略微生疏，不得不从零学打字。", {"knowledge": -10}, hidden_risk_log="未能提前拥抱数字化浪潮，日后在办公自动化中加倍追赶。")
            ]
        }
    ]
)

# 36. 1997 香港回归祖国
add_evt(
    "evt_1997_xianggang_huigui", "era", "1997香港回归祖国历史盛典见证",
    [1997, 1997], [8, 80], ["ALL"], {},
    [], [], 0.95, 3, "确证",
    "1997年7月1日零点中国政府对香港恢复行使主权，历经百年沧桑的香港重回祖国怀抱。天安门广场数十万人狂欢倒计时，五星红旗与紫荆花区旗在会展中心冉冉升起。",
    "电视机前通宵达旦，军乐演奏着《义勇军进行曲》。当英国米字旗缓缓降下、五星红旗在零点分秒不差准时升起时，大江南北鞭炮齐鸣，人们相拥在阳台挥动国旗，百年屈辱终雪。",
    [
        {
            "text": "彻夜守在电视前见证零点历史交接，翌日参加单位/学校迎回归大联欢",
            "choiceTags": ["时代：1997", "年龄：8–80", "地域：全国", "门槛：全体国民"],
            "outcomes": [
                make_outcome("safe", 85, "爱国热忱空前高涨，在集体自豪感中备受鼓舞，珍藏整套香港回归首日封特种邮票。", {"mentality": 25, "family": 15}, status="hk_handover_witness", hidden_risk_log="亲历百年国耻洗雪的高光时刻，凝聚深厚爱国民族自豪感。"),
                make_outcome("safe", 15, "与亲朋好友畅饮庆贺回归，深切感受到国家日益强盛带来的安全感与荣光。", {"family": 20, "mentality": 15}, hidden_risk_log="在举国狂欢中体会到国家富强对个体生活的坚实庇护。")
            ]
        },
        {
            "text": "若为广东或沿海涉外经贸人员，积极参与深港口岸通关保障与经贸对接业务",
            "choiceTags": ["时代：1997", "年龄：20–55", "地域：广东珠三角", "门槛：涉外/交通人员"],
            "outcomes": [
                make_outcome("safe", 70, "在皇岗与文锦渡口岸圆满完成跨境穿梭运输保障，获省涉外保畅模范表彰。", {"wealth": 25, "knowledge": 20, "mentality": 20}, status="border_cadre", hidden_risk_log="在一线保驾护航深港融合，拓展大批香港外贸优质客户资源。"),
                make_outcome("injured", 30, "暴雨中在口岸高强度指挥疏导导致严重滑倒挫伤手肘，休工治疗一周。", {"health": -15, "wealth": 15}, hidden_risk_log="回归保畅执勤负轻伤，以汗水换来通关顺畅。")
            ]
        }
    ]
)

# 37. 1998 亚洲金融危机与国企下岗潮
add_evt(
    "evt_1998_xiagangchao", "era", "国企“抓大放小”改制与下岗再就业潮",
    [1997, 2000], [28, 55], ["ALL"], {"urbanRural": "urban"},
    ["worker"], [], 0.85, 4, "确证",
    "1990年代末伴随亚洲金融危机冲击与国企深化改革，全国开展大规模‘下岗分流、减员增效’。数千万产业工人脱下工装领受‘下岗证’自谋出路，骑自行车穿梭在劳务市场从头再来。",
    "厂区广播站播送着再就业倡议与《从头再来》歌声。车间大门贴着第一批协议买断工龄与分流下岗名单，昔日风光无限的国企职工手捧红本下岗证，在凛冽寒风中茫然四顾不知何去何从。",
    [
        {
            "text": "擦干眼泪领受买断工龄补偿金，置办三轮车在菜市/夜市摆摊卖早点做馄饨",
            "choiceTags": ["时代：1997–2000", "年龄：28–50", "地域：老工业基地城市", "门槛：下岗国企工"],
            "outcomes": [
                make_outcome("safe", 60, "起早贪黑炸油条做早点，靠货真价实客流如云，收入反超昔日工厂，撑起一家老小。", {"wealth": 30, "family": 20, "mentality": 20}, new_career_track="merchant", status="xiagang_self_employed", hidden_risk_log="不向命运低头自食其力，从国企下岗工逆袭为红火个体老板。"),
                make_outcome("injured", 28, "冬天推三轮车在泥雪中摔翻砸伤左膝，且长期双手浸冷水长满冻疮皲裂。", {"health": -25, "wealth": 15}, new_career_track="merchant", hidden_risk_log="地摊谋生风吹雨淋受工伤，但用粗茧双手托起孩子大学梦想。"),
                make_outcome("entangled", 12, "摆摊占道屡遭城管暂扣三轮锅具，夫妻二人相拥抱头痛哭，心酸苦涩。", {"wealth": -20, "mentality": -30}, new_career_track="merchant", hidden_risk_log="下岗初期谋生饱尝底层人情冷暖，在屈辱中苦苦支撑。")
            ]
        },
        {
            "text": "参加政府举办的免费免费下岗再就业技能培训，考取电工/出租车从业资格证",
            "choiceTags": ["时代：1997–2000", "年龄：28–50", "地域：全国城镇", "门槛：有学习意愿职工"],
            "outcomes": [
                make_outcome("safe", 65, "开上城市出租车或受聘为物业首席工程电工，每月领两千元现钞，重拾职业尊严。", {"wealth": 25, "knowledge": 20, "mentality": 20}, new_career_track="flexible_labor", status="taxi_driver_master", hidden_risk_log="靠技能再就业转型开出租车，成为城市灵活就业排头兵。"),
                make_outcome("entangled", 30, "因出租车份子钱沉重且同行竞争加剧，每月早出晚归勉强维持温饱。", {"wealth": 10, "health": -15}, new_career_track="flexible_labor", hidden_risk_log="出租车高强度驾驶劳累过度，但保住了全家口粮底线。"),
                make_outcome("injured", 5, "夜间出车遭遇两车轻度剐蹭致手腕扭伤，修车破费一千元。", {"health": -20, "wealth": -10}, new_career_track="flexible_labor", hidden_risk_log="开出租遇轻微车祸有惊无险，开车更加谨慎专注。")
            ]
        }
    ]
)

# 38. 1998 住房实物分配终结与商品房
add_evt(
    "evt_1998_shangpinfang_anjie", "era", "福利分房终结与商品房按揭时代开启",
    [1998, 2000], [25, 55], ["ALL"], {"urbanRural": "urban"},
    [], [], 0.85, 4, "确证",
    "1998年7月国务院发布《关于进一步深化城镇住房制度改革加快住房建设的通知》，宣布全国停止住房实物分配，逐步实行住房分配货币化，中国正式迈入商业化商品房与银行按揭时代。",
    "厂区房管科正式贴出封印大榜，宣告延续近半个世纪的福利分房画上句号。大街上房地产中介与售楼处如雨后春笋般冒出，五万元首付、按揭贷款二十年买红砖防盗门新房成为街谈巷议新热词。",
    [
        {
            "text": "掏空两代人全部积蓄并向银行办理按揭贷款，咬牙在城区购买首套商品房",
            "choiceTags": ["时代：1998–2000", "年龄：25–50", "地域：全国城镇", "门槛：有两万元首付储蓄"],
            "outcomes": [
                make_outcome("safe", 70, "成为第一批吃商品房红利的人，住进带阳台独立卫浴的明亮套房，房产日后翻数倍。", {"wealth": 50, "family": 25, "mentality": 20}, status="home_owner_1998", hidden_risk_log="敢为人先在房改初期贷款买商品房，锁定时代财富超级红利。"),
                make_outcome("entangled", 30, "每月按揭月供几乎占去工资大半，日子紧巴巴不敢吃肉下馆子，尝到房奴压力。", {"wealth": -15, "mentality": -15}, status="home_owner_1998", hidden_risk_log="早期扛按揭生活拮据，但最终熬成城市有产中产。")
            ]
        },
        {
            "text": "嫌商品房价格高不可攀且背负银行利息，坚决不买房，继续租住老旧筒子楼",
            "choiceTags": ["时代：1998–2000", "年龄：25–55", "地域：全国城镇", "门槛：保守居民"],
            "outcomes": [
                make_outcome("safe", 60, "无债一身轻免受房贷压迫，吃喝从容自由，每月将工钱存为银行存单。", {"wealth": 10, "mentality": 10}, hidden_risk_log="拒绝房贷过好当下寻常日子，避开按揭负债压力。"),
                make_outcome("entangled", 40, "数年后看着周边房价一路狂飙扶摇直上，自己积蓄连个卫生间都买不起，扼腕长叹。", {"wealth": -25, "mentality": -25}, hidden_risk_log="严重错失城镇住房市场化早期低价红利，后半生租房漂泊。")
            ]
        }
    ]
)

# 39. 1998 特大抗洪抢险
add_evt(
    "evt_1998_kanghong_qiangxian", "era", "1998长江、嫩江、松花江全流域特大抗洪",
    [1998, 1998], [14, 65], ["ALL"],
    {"provinces": ["hubei", "hunan", "jiangxi", "heilongjiang", "jilin", "neimenggu", "anhui", "jiangsu"]},
    [], [], 0.90, 4, "确证",
    "1998年夏长江、嫩江、松花江爆发百年罕见特大全流域全线洪涝灾害。三十万官兵与百万群众用血肉之躯在九江、荆江大堤上严防死守、‘人在堤在’，万众一心谱写抗洪壮歌。",
    "荆江大堤暴雨倾盆，江水已高出城区地面数米，如同头顶悬着一盆浩瀚巨湖。管涌喷涌浑水，大喇叭吼着‘死保九江大堤、决不后退半步’。红旗在风雨中猎猎作响，人墙手挽手跳入滚滚浊浪。",
    [
        {
            "text": "若身处沿江重灾区，带头扛运沙袋跳入冰冷江水筑起血肉防波人墙，死保大堤",
            "choiceTags": ["时代：1998", "年龄：17–55", "地域：长江/松花江防汛前线", "门槛：热血军民"],
            "outcomes": [
                make_outcome("safe", 55, "在大堤上连熬七天七夜成功封堵九江决口，保住身后百万居民生命财产，荣立大功。", {"mentality": 35, "health": -10, "family": 20}, status="flood_hero_1998", hidden_risk_log="九八抗洪铁血英雄，以血肉之躯护佑山河家园，锤炼出泰山不倒意志。"),
                make_outcome("injured", 32, "江水湍急受管涌乱石撞击导致右腿骨裂并患重度浸泡皮炎，住院养伤三月。", {"health": -35, "mentality": 25}, status="injured_rescuer_1998", hidden_risk_log="抗洪前线被乱石撞击负伤致轻度残疾，深受全社会崇高尊崇。"),
                make_outcome("entangled", 11, "身后家中老房被倒灌内涝浸泡倒塌，农田全部绝收，靠救济粮重建家园。", {"wealth": -35, "family": -15}, hidden_risk_log="洪水中家财尽毁，在政府安置下搭建板房度过寒冬。"),
                make_outcome("fatal", 2, "在封堵大堤突发决口合龙时被狂暴激流卷入深潭不幸牺牲。", is_fatal=True, hidden_risk_log="在1998年抗洪封堵决口危急时刻光荣牺牲。")
            ]
        },
        {
            "text": "在后方城市连夜赶制防汛救灾冲锋舟编织袋，并向受灾同胞捐赠一周薪水",
            "choiceTags": ["时代：1998", "年龄：14–70", "地域：全国", "门槛：普通国民"],
            "outcomes": [
                make_outcome("safe", 85, "生产线三班倒赶制出上万条加厚编织袋驰援九江，在后方尽己所能奉献力量。", {"wealth": -10, "mentality": 15}, hidden_risk_log="在后方为抗洪大局添砖加瓦，体现深厚家国同胞情谊。"),
                make_outcome("safe", 15, "收留安置沿江来投靠的落难远房表亲，腾出两间热屋管吃管住直到水退。", {"family": 25, "wealth": -15}, hidden_risk_log="在患难时刻接济亲族骨肉，诠释血脉相连的人间温情。")
            ]
        }
    ]
)

# 40. 1999 大学扩招大门开启
add_evt(
    "evt_1999_daxue_kuozhao", "era", "1999年全国高校大扩招：走向大众化高等教育",
    [1999, 2001], [16, 22], ["ALL"], {},
    [], [], 0.88, 4, "确证",
    "1999年6月教育部出台高校扩招政策，当年全国普通高校招生总人数增加51万人，增幅达47.4%，录取率由36%跃升至56%。从此中国高等教育彻底告别精英象牙塔，步入大众化新纪元。",
    "高考发榜的高中学校门口挤满了查分的人群。喜报上的红榜比往年长了几乎一倍，许多原本只能读专科或回乡复读的乡村学子，惊喜地在省属本科院校录取名单里找到了自己的名字。",
    [
        {
            "text": "抓住扩招历史机遇以适度分数顺利迈进大学本科校门，勤工俭学读完学业",
            "choiceTags": ["时代：1999–2001", "年龄：17–22", "地域：全国", "门槛：高中高三学子"],
            "outcomes": [
                make_outcome("safe", 70, "成为家族首位全日制大学生，靠国家助学贷款与发传单打工读完本科，开启白领生涯。", {"knowledge": 35, "wealth": 20, "mentality": 25}, new_career_track="tech_whitecollar", status="expanded_college_student", hidden_risk_log="搭乘99大学扩招头班车圆大学梦，彻底完成由农家子向城市白领飞跃。"),
                make_outcome("entangled", 25, "扩招后每年数千元高昂学杂费让农村家庭债台高筑，父母借遍亲友才凑齐学费。", {"wealth": -25, "family": -15}, new_career_track="tech_whitecollar", hidden_risk_log="高昂学费让全家背上重债，毕业后拼命工作还清债务。"),
                make_outcome("injured", 5, "暑期为赚学费在砖窑做苦力中暑虚脱脱水，休养半月方缓过劲。", {"health": -20, "wealth": 15}, hidden_risk_log="打暑期工吃尽苦头攒齐学费，更加珍惜大学求学时光。")
            ]
        },
        {
            "text": "因家境极其困难弟妹众多，放弃读二本机会，直接进入沿海电子五金厂当技术员",
            "choiceTags": ["时代：1999–2001", "年龄：18–22", "地域：贫困家庭", "门槛：懂事实用青年"],
            "outcomes": [
                make_outcome("safe", 75, "进厂早早领两千元工资寄回老家供弟妹上学，凭高中扎实数理底子晋升车间排长。", {"wealth": 30, "family": 30}, new_career_track="worker", status="factory_senior_tech", hidden_risk_log="放弃求学牺牲自己托举全家，用大爱换来弟妹学有所成。"),
                make_outcome("entangled", 25, "多年后看着考上大学的同班同学在写字楼吹空调，内心深处难掩一丝遗憾。", {"mentality": -20}, hidden_risk_log="为家庭生计妥协放弃文凭，在平凡务实生活中守住无悔担当。")
            ]
        }
    ]
)

# 41. 1999 驻南联盟使馆遭北约轰炸
add_evt(
    "evt_1999_zhunan_shiguan", "era", "驻南使馆遭袭事件与青年爱国示威",
    [1999, 1999], [15, 60], ["ALL"], {},
    [], [], 0.90, 3, "确证",
    "1999年5月8日以美国为首的北约悍然使用导弹袭击中国驻南联盟大使馆，造成邵云环、许杏虎、朱颖3位优秀记者英勇牺牲，数十人受伤。全国高校学子与各界群众爆发空前爱国抗议。",
    "校园宣传栏前贴满了印有烈士遗照的号外报纸，群情激愤。大学生们额头上系着白色布条，手拉手走上街头高举抗议标语，向外国使领馆愤怒声讨霸权行径，国歌声整日响彻云霄。",
    [
        {
            "text": "加入青年爱国游行队伍高呼口号声讨霸权，誓言投身国防科技与发奋读书",
            "choiceTags": ["时代：1999", "年龄：15–40", "地域：全国大中城市", "门槛：热血青年"],
            "outcomes": [
                make_outcome("safe", 80, "深刻洗礼激发内心强国抱负，发愤图强考取军工科研所或国防重大工程专项。", {"mentality": 30, "knowledge": 20}, status="defense_aspirant", hidden_risk_log="亲历南使馆之痛立志科技报国，成长为国家国防尖端领域骨干。"),
                make_outcome("injured", 20, "抗议人潮极度拥挤发生踩踏磕碰，左膝被路牙石磕伤淤血两周。", {"health": -15, "mentality": 20}, hidden_risk_log="在抗议人潮中轻微擦伤，爱国热忱刻骨铭心。")
            ]
        },
        {
            "text": "坚守科研试验室或工矿生产线加班加点，以‘把自己的事情做好’实际行动爱国",
            "choiceTags": ["时代：1999", "年龄：18–60", "地域：全国", "门槛：工矿科研职工"],
            "outcomes": [
                make_outcome("safe", 85, "将满腔悲愤化为生产攻关动力，提前一个月完成重大型号核心部件试制交差。", {"wealth": 20, "knowledge": 25, "mentality": 20}, status="patriotic_worker", hidden_risk_log="化悲痛为实干力量，在平凡岗位上为挺起大国脊梁添砖加瓦。"),
                make_outcome("safe", 15, "参与单位组织的追思悼念仪式，深切感悟‘落后就要挨打’的铁血硬道理。", {"mentality": 20}, hidden_risk_log="牢记历史教训，以务实求真精神过好每一天。")
            ]
        }
    ]
)

# 42. 1999 首个“十一”黄金周
add_evt(
    "evt_1999_huangjinzhou", "era", "首个“十一”黄金周：假日经济与旅游热潮",
    [1999, 1999], [8, 75], ["ALL"], {},
    [], [], 0.88, 3, "确证",
    "1999年国庆节中国首个7天‘黄金周’长假落地。2800万人次涌向全国名胜古迹，华山、黄山、故宫客流爆棚，交通与文旅消费引爆神州，‘假日经济’横空出世。",
    "火车站售票窗口前排起了蜿蜒长龙，大巴车挂着‘黄山三日游’、‘北京观光’的横幅。饭店客房早早挂出满房招牌，背着双肩包戴着红遮阳帽的普通市民，兴奋地迈出体验休闲旅游的第一步。",
    [
        {
            "text": "第一次跟团或自由行带家人远赴北京故宫/泰山游览，体验长假旅游",
            "choiceTags": ["时代：1999", "年龄：12–70", "地域：全国", "门槛：普通工薪家庭"],
            "outcomes": [
                make_outcome("safe", 75, "领略祖国大好河山，拍下珍贵的彩色胶卷全家福冲印成册，精神文化生活极大丰富。", {"family": 25, "mentality": 20, "wealth": -10}, status="golden_week_traveler", hidden_risk_log="享受国家首个法定黄金周旅游红利，开创现代家庭度假生活方式。"),
                make_outcome("injured", 20, "景区人潮极度拥堵在山道台阶被踩伤右脚踝扭伤，排队如厕耗费数小时。", {"health": -15, "wealth": -10}, hidden_risk_log="黄金周首遇全国景点大拥堵受皮肉苦，学会错峰出行经验。"),
                make_outcome("entangled", 5, "遭遇黑导游虚假宣传强制购物消费，与旅行社交涉一周方退回部分款项。", {"wealth": -15, "mentality": -15}, hidden_risk_log="早期旅游市场不规范交学费，学会依法维权索赔。")
            ]
        },
        {
            "text": "若为景区/交通/餐饮从业者，全员无休坚守一线迎客，斩获丰厚长假营收",
            "choiceTags": ["时代：1999", "年龄：18–55", "地域：旅游城市与景区", "门槛：服务文旅从业者"],
            "outcomes": [
                make_outcome("safe", 80, "客栈餐饮天天爆满，七天长假净赚数万元利润，顶上平时整季度收入。", {"wealth": 40, "knowledge": 15}, new_career_track="merchant", status="tourism_beneficiary", hidden_risk_log="抓住首届黄金周井喷商机赚得盆满钵满，奠定文旅实业基石。"),
                make_outcome("injured", 20, "连续七天高强度掌勺迎宾劳累过度导致急性喉炎与腰肌扭伤住院。", {"health": -20, "wealth": 30}, hidden_risk_log="高强度服务长假透支咽喉与腰肌，后加聘帮手科学排班。")
            ]
        }
    ]
)

# 保存 events_1978_1999.json
out_dir = os.path.join(root, "data", "events")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "events_1978_1999.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(base.events, f, ensure_ascii=False, indent=2)

print(f"✅ Successfully written {len(base.events)} events to {out_path}!")
