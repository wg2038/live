# tools/build_events_1978_1999_full.py
# -*- coding: utf-8 -*-
"""
生成 1978–1999 年共 42 条全要素历史事件库，严格遵循：
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

# --- 1-10 核心事件 ---
add_evt(
    "evt_1978_xiaogang_dabaogan", "era", "小岗村大包干与包产到户",
    [1978, 1982], [18, 65], ["ALL"], {"urbanRural": "rural"},
    ["farmer"], [], 0.85, 5, "确证",
    "1978年冬安徽凤阳小岗村18位农民按下红手印搞‘大包干’。随后家庭联产承包责任制在全国农村铺开，极大地释放了亿万农民的生产积极性。",
    "大队部前的打谷场上，老支书拿着红印泥宣布分田到户。祖祖辈辈给集体挣工分的社员们，第一次在属于自家的承包田里打下木桩。粮囤空瘪了多年，如今泥土带着希望的温热。",
    [
        {
            "text": "精耕细作自留承包田，兼搞生猪圈养与温棚菜",
            "choiceTags": ["时代：1978–1982", "年龄：18–65", "地域：全国农村", "门槛：承包社员"],
            "outcomes": [
                make_outcome("safe", 65, "起早贪黑伺候庄稼，秋天谷子堆满仓，卖出余粮摘掉贫困帽。", {"wealth": 25, "family": 15}, status="diligent_farmer", hidden_risk_log="赶上包产到户第一班春风，靠辛勤汗水换来全家温饱富足。"),
                make_outcome("injured", 25, "开荒抢种过度劳累扭伤腰肌，且被农具划破小腿发炎。", {"health": -20, "wealth": 15}, hidden_risk_log="农活繁重落下腰劳损，但家里粮仓终于有了余粮。"),
                make_outcome("entangled", 10, "因分地地界与邻舍发生纠纷，闹到公社调解方得平息。", {"family": -15, "mentality": -10}, hidden_risk_log="因地垄争端与族亲产生嫌隙，耗费数月调和。")
            ]
        },
        {
            "text": "种足口粮田即可，农闲时挑担走村串户做泥瓦木工手艺活",
            "choiceTags": ["时代：1978–1982", "年龄：18–50", "地域：乡村集镇", "门槛：有手艺农民"],
            "outcomes": [
                make_outcome("safe", 70, "凭一身过硬木工手艺挣回现钱，贴补家用日子过得颇为滋润。", {"wealth": 20, "mentality": 10}, status="rural_artisan", hidden_risk_log="农闲做手艺贴补家计，成为村里最早有现金活钱的家庭。"),
                make_outcome("entangled", 20, "挑担走乡遭遇雨雪路滑摔坏工具箱，白忙活半个月。", {"wealth": -10, "health": -10}, hidden_risk_log="风餐露宿跑手艺尝尽辛苦，换来微薄养家铜板。"),
                make_outcome("redirected", 10, "被邻县刚筹建的建筑队看中，收为固定泥瓦班长带队进城。", {"wealth": 30, "knowledge": 15}, new_career_track="worker", hidden_risk_log="凭手艺脱离纯农耕，成为第一批走出山乡的乡村建筑班长。")
            ]
        }
    ]
)

add_evt(
    "evt_1978_gongpai_liuxue", "era", "首批公派留学生选拔",
    [1978, 1980], [22, 40], ["ALL"], {"urbanRural": "urban"},
    ["higher_ed_degree"], [], 0.65, 5, "确证",
    "1978年教育部选拔首批52名公派访问学者赴美留学，标志着新时期留学大潮的正式拉开帷幕，入选者多为高校与科研院所骨干骨干精英。",
    "科研所红榜前聚满了人，泛黄的报名简章上写着公派赴美访问学者的选拔条件。英语口语测试、专业考核极为严苛，无数知识分子在微弱的台灯下重新捧起尘封多年的外文期刊。",
    [
        {
            "text": "全力备战选拔考试，争取出访北美名校担任公派学者",
            "choiceTags": ["时代：1978–1980", "年龄：22–40", "地域：重点高校科研院", "门槛：高级知识分子"],
            "outcomes": [
                make_outcome("safe", 60, "以拔尖专业成绩入选公派名单，身着统一深色西服飞赴大洋彼岸。", {"knowledge": 40, "wealth": 20, "mentality": 25}, status="overseas_scholar", hidden_risk_log="作为国家首批公派学者开眼看世界，奠定终生学术殿堂地位。"),
                make_outcome("entangled", 30, "政审与外语口语临场微弱失利落选，留守教研室继续带课。", {"mentality": -15, "knowledge": 15}, hidden_risk_log="公派竞争激烈擦肩而过，转而深耕国内重点实验室项目。"),
                make_outcome("injured", 10, "通宵突击查阅外文文献过度疲劳引发突发性耳鸣，调养两月。", {"health": -20, "mentality": -10}, hidden_risk_log="备考过度用脑伤及神经，但拓宽了科研学术眼界。")
            ]
        },
        {
            "text": "安于本院重点实验室，接手老教授留下的国产重点攻坚课题",
            "choiceTags": ["时代：1978–1980", "年龄：24–45", "地域：科研事业单位", "门槛：院所助教讲师"],
            "outcomes": [
                make_outcome("safe", 70, "主导攻克工业仪表国产化关键算法，获部委科技进步二等奖并晋级副高。", {"knowledge": 30, "wealth": 15, "family": 15}, status="lab_core", hidden_risk_log="留守本土潜心攻关，成为实验室不可或缺的技术掌门人。"),
                make_outcome("entangled", 30, "实验室耗材与外汇短缺陷入停滞，眼看同辈出洋内心难免落寞。", {"mentality": -15}, hidden_risk_log="在国内科研资源吃紧时期坚守书桌，甘坐数年冷板凳。")
            ]
        }
    ]
)

add_evt(
    "evt_1979_zhiqing_fancheng", "era", "知青大返城浪潮与接班顶替",
    [1979, 1981], [22, 35], ["ALL"], {"urbanRural": "rural"},
    ["worker"], [], 0.85, 4, "确证",
    "1979年前后全国迎来千万知青返城落户大潮。许多老职工通过‘退休顶替’政策让子女顶岗回城，大批返城青年面临待业安置与生计重整。",
    "知青农场的大铁门前，卡车装满行囊。红头文件下发，允许父母提前退休由知青子女接班回城。有人紧紧攥着盖着大红公章的回城审批表，有人则看着乡下的配偶与幼子陷入两难。",
    [
        {
            "text": "通过父母提前退休办理‘长安顶替’，回城进国营厂当学徒工",
            "choiceTags": ["时代：1979–1981", "年龄：22–35", "地域：城镇国企", "门槛：父母为国企老职工"],
            "outcomes": [
                make_outcome("safe", 65, "顺利顶替入厂端上铁饭碗，分到集体宿舍，开启踏实的工人岁月。", {"wealth": 20, "family": 15}, status="secured_factory_job", hidden_risk_log="顺利顶替父母工籍回归城市生活，获得铁饭碗安稳庇护。"),
                make_outcome("entangled", 25, "顶替岗位为车间脏苦累的翻砂工，工资微薄，与家人挤狭小偏房。", {"health": -15, "wealth": 10}, hidden_risk_log="回城后从事底层重体力车间工作，居住条件极为逼仄。"),
                make_outcome("injured", 10, "车间行车搬运钢板不慎砸伤脚趾，休工卧床两月方愈。", {"health": -25, "wealth": 5}, hidden_risk_log="顶替初入车间技术生疏受工伤，休养后逐步掌握要领。")
            ]
        },
        {
            "text": "因在农村已成家生子，毅然选择留乡扎根，在大队小学当公办教师",
            "choiceTags": ["时代：1979–1981", "年龄：23–35", "地域：乡村插队地", "门槛：有乡间家庭"],
            "outcomes": [
                make_outcome("safe", 60, "不忍抛妻弃子留守山乡，教书育人深得乡民敬仰，家庭和睦幸福。", {"family": 30, "knowledge": 15, "mentality": 20}, status="village_teacher", hidden_risk_log="为挚爱亲情放弃回城，在乡村讲台上桃李芬芳赢得一世尊崇。"),
                make_outcome("entangled", 30, "看着回城知青寄来的城市风景照，面对泥泞土路常发长叹。", {"mentality": -20, "wealth": -10}, hidden_risk_log="午夜梦回念及城市繁华难免怅然，但恪守为人父母之责。"),
                make_outcome("redirected", 10, "因文化功底扎实被公社选拔为乡党委秘书，开启基层公职之路。", {"knowledge": 20, "wealth": 15}, new_career_track="cadre_teacher", hidden_risk_log="留乡展现文字才能被提拔为公社干部，走出独特的晋升路。")
            ]
        }
    ]
)

add_evt(
    "evt_1979_duiyue_fanjizhan", "era", "1979南疆自卫还击作战动员",
    [1979, 1980], [18, 25], ["ALL"], {"urbanRural": "all"},
    [], [], 0.75, 4, "确证",
    "1979年2月对越自卫还击作战打响。大批热血军人与边境支前民兵奔赴南疆热带雨林山岳丛林作战，涌现出大批战斗英雄，有力维护了西南边境安全。",
    "武装部的大喇叭里播放着热血军歌，南疆边境哨所接连告急。火车站台上挤满了换上崭新草绿色军装的参军青年，胸前佩戴的大红花娇艳欲滴。车厢内歌声嘹亮，即将踏入湿热险峻的山岳丛林。",
    [
        {
            "text": "写下请战书报名开赴南疆前线，参加山地丛林穿插突击队",
            "choiceTags": ["时代：1979–1980", "年龄：18–25", "地域：全国", "门槛：热血青年男性"],
            "outcomes": [
                make_outcome("safe", 50, "在湿热丛林中奋勇穿插完成作战使命，荣立战功凯旋返乡。", {"mentality": 35, "knowledge": 15, "wealth": 20}, status="war_veteran", hidden_risk_log="参军经历南疆炮火洗礼，荣归故里成为受全社会敬仰的老兵功臣。"),
                make_outcome("injured", 35, "在山隘排雷时遭遇弹片击中左小腿致轻残，退伍安置进机关车队。", {"health": -35, "mentality": 15, "wealth": 15}, status="disabled_veteran", hidden_risk_log="排雷作战负伤致轻度伤残，退伍保送安置体制内工作。"),
                make_outcome("entangled", 13, "目睹战友牺牲患上创伤后应激障碍，深夜偶发惊悸盗汗。", {"mentality": -30, "health": -15}, hidden_risk_log="战后长期受PTSD困扰，在家人悉心照料下逐步恢复。"),
                make_outcome("fatal", 2, "在穿插阻击战中遭遇暗堡炮火伏击光荣牺牲。", is_fatal=True, hidden_risk_log="在南疆前线阻击阵地上光荣牺牲，被追授烈士称号。")
            ]
        },
        {
            "text": "服从地方分配报名参加边境弹药与战地伤员民兵汽车抢运队",
            "choiceTags": ["时代：1979–1980", "年龄：18–35", "地域：西南/华南", "门槛：青壮劳力/司机"],
            "outcomes": [
                make_outcome("safe", 65, "驾解放牌卡车冒着落石夜行盘山路抢送前线急需物资，平安立功。", {"wealth": 20, "knowledge": 20, "mentality": 20}, status="driver_hero", hidden_risk_log="作为战地运输骨干立功，锤炼出神入化的重型卡车驾驶技能。"),
                make_outcome("injured", 25, "卡车在盘山公路避让炮坑侧翻入边沟，锁骨轻微骨折。", {"health": -25, "wealth": 10}, hidden_risk_log="战地运输车遭遇险情翻车负伤，休养半年后重返工作岗位。"),
                make_outcome("entangled", 10, "因车辆遭炮火炸损承担审查损失，耗费数月才核销物资清单。", {"mentality": -15, "wealth": -10}, hidden_risk_log="战地物资损耗核查周折繁琐，心力交瘁。")
            ]
        }
    ]
)

add_evt(
    "evt_1980_shenzhen_tequ", "era", "深圳经济特区设立与开山拓荒",
    [1980, 1983], [18, 45], ["ALL"], {},
    [], [], 0.75, 4, "确证",
    "1980年8月全国人大常委会批准设立深圳经济特区。蛇口工业区响起‘开山第一炮’，竖起‘时间就是金钱，效率就是生命’标牌，吸引全国开拓者涌入南粤小渔村。",
    "海风吹过咸涩的泥沼，推土机与铁镐轰鸣不绝。罗湖黄泥漫天，简易工棚连绵数里。来自全国各地的基建工程兵与青年拓荒者汗流浃背，日夜抢建这片热土。",
    [
        {
            "text": "报名随工程基建大队开赴特区，在罗湖荒滩挑灯夜战打地基",
            "choiceTags": ["时代：1980–1983", "年龄：18–45", "地域：广东深圳", "门槛：基建青工/退役老兵"],
            "outcomes": [
                make_outcome("safe", 60, "随部队打通特区深南大道，经考核转为特区第一代建设发展公司正式员工。", {"wealth": 35, "knowledge": 15, "mentality": 20}, status="tequ_pioneer", hidden_risk_log="南下特区第一代拓荒牛，参与特区奠基并优先落户深圳。"),
                make_outcome("injured", 28, "炎热潮湿患上顽固烂裆与湿疹，手脚多处磕碰留疤。", {"health": -25, "wealth": 20}, hidden_risk_log="在恶劣工棚环境中负伤染疾，但赚回了可观的特区补贴。"),
                make_outcome("entangled", 10, "特区建设早期水土不服严重腹泻，因思乡一度动摇回乡念头。", {"mentality": -15, "health": -10}, hidden_risk_log="初期条件艰苦水土不服，咬牙挺过最艰难的开拓阶段。"),
                make_outcome("fatal", 2, "深基坑高空脚手架作业突遇暴风雨坍塌不幸坠亡。", is_fatal=True, hidden_risk_log="在特区早期基建突发事故中不幸罹难。")
            ]
        },
        {
            "text": "留守原籍老厂按部就班上工，不图风浪只求安稳旱涝保收",
            "choiceTags": ["时代：1980–1983", "年龄：18–50", "地域：内地城镇", "门槛：工矿职工"],
            "outcomes": [
                make_outcome("safe", 70, "老家日子波澜不惊，守在父母妻儿身边，每月准时领劳保粮票与工资。", {"family": 20, "wealth": 10}, hidden_risk_log="安居乡梓避开南下拓荒之苦，享受内地老工业基地的温情。"),
                make_outcome("entangled", 30, "数年后听闻昔日同僚在深圳月入数百元买上电视机，略有艳羡。", {"mentality": -15}, hidden_risk_log="内地发展相对平缓，与沿海特区拉开了一定收入差距。")
            ]
        }
    ]
)

add_evt(
    "evt_1980_dushengzinv", "era", "独生子女政策全面推行与领证抉择",
    [1980, 1984], [22, 38], ["ALL"], {},
    ["married"], [], 0.80, 5, "确证",
    "1980年9月中共中央发表《关于控制我国人口增长问题致全体共产党员共青团员的公开信》，提倡一对夫妇只生育一个孩子。全国城乡广泛发放《独生子女父母光荣证》与保健费。",
    "街道居委会与厂工会挂起了大红标语，计生宣传画上胖乎乎的单娃捧着大红花。单位领导找上门做思想工作，桌上摆着‘独生子女父母光荣证’与每月五元的营养保健费批条。",
    [
        {
            "text": "积极响应号召主动领取独生子女光荣证，不再生育二胎",
            "choiceTags": ["时代：1980–1984", "年龄：22–38", "地域：全国城乡", "门槛：已育一孩夫妇"],
            "outcomes": [
                make_outcome("safe", 75, "领受光荣证并获评单位计生模范，将全副心血与资源投入培养独生宝贝。", {"wealth": 15, "family": 15, "mentality": 15}, status="only_child_parent", hidden_risk_log="响应国家号召生育独子，集中家庭财力让孩子享受最好照料。"),
                make_outcome("entangled", 25, "老家公婆重男轻女思想严重，因生的是女孩引发家庭长达数年冷战。", {"family": -25, "mentality": -20}, hidden_risk_log="因未生男丁在传统宗族间承受沉重传统伦理压力。")
            ]
        },
        {
            "text": "渴望儿女双全，暗中回乡下老宅暂避风头，伺机超生二胎",
            "choiceTags": ["时代：1980–1984", "年龄：22–38", "地域：乡村边缘", "门槛：传统家庭"],
            "outcomes": [
                make_outcome("safe", 40, "辗转在远亲偏僻村庄生下二孩，虽东躲西藏但终于实现儿女双全。", {"family": 25, "mentality": -10, "wealth": -20}, status="multi_children", hidden_risk_log="东躲西藏诞下二胎，为全家未来生活平添一份子嗣依靠。"),
                make_outcome("entangled", 50, "被计生干部排查堵截，被按规定扣罚两年社会抚养费并通报开除公职。", {"wealth": -35, "mentality": -30, "family": -15}, status="status_penalized", hidden_risk_log="因超生遭受重额经济罚款与体制内除名，家庭一度极为拮据。"),
                make_outcome("injured", 10, "在乡村简陋接生婆处分娩发生大出血险些丧命，万幸抢救脱险。", {"health": -35, "wealth": -25}, hidden_risk_log="黑诊所简陋分娩遭遇大出血，伤及元气休养整年。")
            ]
        }
    ]
)

add_evt(
    "evt_1980_fuli_fenfang", "era", "国企大厂福利分房积分考评",
    [1980, 1983], [26, 55], ["ALL"], {"urbanRural": "urban"},
    ["worker"], [], 0.78, 4, "确证",
    "1980年前后城市住房极度紧张，国企大中型工厂依据工龄、技术职务、双职工身份与婚育状况进行综合算分排队分房，解决职工三代同堂的筒子楼居住困境。",
    "厂区公告栏前烟头落了一地，白底红字的大榜贴出了今年分房计分排位。祖孙三代蜗居在12平米暗间的青工老干们拿着放大镜对照积分，任何一分之差都决定能不能搬出筒子楼。",
    [
        {
            "text": "向厂部如实汇报三代同堂困难，凭借技术能手与无缺勤加分冲刺房榜",
            "choiceTags": ["时代：1980–1983", "年龄：26–55", "地域：国企工矿", "门槛：国企老职工"],
            "outcomes": [
                make_outcome("safe", 65, "顺利排进前十名分到红砖新楼两居室套房，告别公用厨房煤球炉。", {"wealth": 30, "family": 30, "mentality": 25}, status="welfare_housed", hidden_risk_log="凭工龄与贡献分得国企福利套房，彻底改变全家居住面貌。"),
                make_outcome("entangled", 30, "排名卡在边缘以0.5分之差惜败名落孙山，不得不继续在筒子楼挤住三年。", {"mentality": -20, "family": -10}, hidden_risk_log="福利分房因细微积分差抱憾落空，体味到体制内排队的不易。"),
                make_outcome("injured", 5, "搬家搬运沉重铸铁煤炉不慎扭伤腰椎，卧床两周。", {"health": -15, "wealth": 15}, hidden_risk_log="搬迁新居时不慎扭伤腰部，但在新房炕头上笑逐颜开。")
            ]
        },
        {
            "text": "自知工龄尚浅排不上号，自行动手用红砖在自建小院搭一间防震临时偏厦",
            "choiceTags": ["时代：1980–1983", "年龄：24–40", "地域：城镇街道", "门槛：平民家庭"],
            "outcomes": [
                make_outcome("safe", 70, "拉运废旧砖石搭起八平米干燥小屋分流居所，解了燃眉之急。", {"wealth": 10, "family": 15}, hidden_risk_log="不等不靠自搭小棚解决住处，体现普通百姓的坚韧与巧思。"),
                make_outcome("entangled", 30, "搭建的棚房被街道城管认定为违章搭建拆除一半，心疼不已。", {"wealth": -15, "mentality": -15}, hidden_risk_log="私搭棚房被整治拆除部分，但依然在缝隙中求得安身。")
            ]
        }
    ]
)

add_evt(
    "evt_1981_nvpai_duoguan", "era", "中国女排首夺世界冠军与振兴中华",
    [1981, 1981], [10, 70], ["ALL"], {},
    [], [], 0.90, 3, "确证",
    "1981年11月中国女排在第三届世界杯排球赛中以七战全胜首夺世界冠军。北大学子在燕园点燃扫帚游行高呼‘团结起来，振兴中华’，女排拼搏精神极大振奋了全国民心。",
    "黑白电视机前围满了整条胡同的邻里老少，信号天线晃动着雪花点。决胜局扣杀落地的瞬间，大杂院里爆发出掀翻屋顶的欢呼。敲脸盆、燃鞭炮，人们相拥在夜色里热泪盈眶。",
    [
        {
            "text": "深怀激动投身高校/单位夜校进修，将女排拼搏精神化为加班苦干动力",
            "choiceTags": ["时代：1981", "年龄：16–50", "地域：全国", "门槛：平民大众"],
            "outcomes": [
                make_outcome("safe", 75, "精神大受振奋，在岗位技术大比武中斩获第一名并记嘉奖一次。", {"mentality": 25, "knowledge": 15, "wealth": 10}, status="role_model_1981", hidden_risk_log="沐浴女排拼搏精神洗礼，将时代自豪感转化为实干晋升。"),
                make_outcome("safe", 25, "与满院邻里痛饮散装白酒庆贺，在激情燃烧的年代结下深厚邻里深情。", {"family": 20, "mentality": 20}, hidden_risk_log="在集体记忆中感受到久违的民族自信与家国大爱。")
            ]
        },
        {
            "text": "带头组建社区/车间青年排球与长跑队，坚持晨练强身健体",
            "choiceTags": ["时代：1981", "年龄：14–40", "地域：城镇街道", "门槛：热血青年"],
            "outcomes": [
                make_outcome("safe", 70, "常年长跑排球练就结实强健体魄，彻底摆脱幼年羸弱体质。", {"health": 25, "mentality": 15}, status="sports_enthusiast", hidden_risk_log="受女排带动坚持群众体育锻炼，为一生奠定过硬身体基础。"),
                make_outcome("injured", 30, "扣球起跳落地不慎扭伤右脚踝韧带，肿痛卧床两周。", {"health": -15, "mentality": 10}, hidden_risk_log="打排球扭伤脚踝，但在运动场上结识了相伴终生挚友。")
            ]
        }
    ]
)

add_evt(
    "evt_1982_yiwu_xiaoshangpin", "era", "义乌小商品市场开放与敲糖帮",
    [1982, 1985], [18, 50], ["华东"], {"provinces": ["zhejiang", "jiangsu", "anhui", "jiangxi"]},
    ["farmer"], [], 0.75, 4, "确证",
    "1982年浙江义乌县委正式提出‘四个允许’（允许农民经商、长途贩运、开放市场、多渠道竞争），开放第一代马路小商品市场，敲糖帮走向全国。",
    "青石板路两侧支起简易水泥板摊位，拨浪鼓的咚咚声清脆悦耳。针线包、尼龙袜、塑料纽扣铺满布单，县委干部的批条保护着这些曾被称为投机倒把的小挑担。",
    [
        {
            "text": "放下锄头摇起拨浪鼓，租下水泥摊位批发尼龙袜与小五金饰品",
            "choiceTags": ["时代：1982–1985", "年龄：18–50", "地域：浙东江浙", "门槛：敢闯农户"],
            "outcomes": [
                make_outcome("safe", 65, "勤俭耐劳走南闯北走量批发，成为义乌第一批日进斗金的小商品摊主。", {"wealth": 45, "knowledge": 15}, new_career_track="merchant", status="yiwu_merchant", hidden_risk_log="顺应市场经济萌芽敢为人先，从鸡毛换糖蜕变为民营老板。"),
                make_outcome("injured", 25, "长途挤绿皮车挤爆车窗刮伤右臂，且货物被小偷偷走两包。", {"health": -15, "wealth": 10}, new_career_track="merchant", hidden_risk_log="赶集长途颠簸受工伤与失窃，但摸清了全国商贸流通门路。"),
                make_outcome("entangled", 10, "在外省兜售小百货被当地市管人员按投机倒把扣押罚款，几经申诉方解。", {"wealth": -20, "mentality": -20}, hidden_risk_log="早期跨省贩运政策未完全普及，历经曲折洗礼。")
            ]
        },
        {
            "text": "留守本地承包田为摆摊亲友扎制竹篮编织纸盒，坐收稳定工钱",
            "choiceTags": ["时代：1982–1985", "年龄：18–60", "地域：浙东乡村", "门槛：传统农户"],
            "outcomes": [
                make_outcome("safe", 75, "手脚麻利加工包装盒，农忙种地农闲拿现款，日子稳步改善。", {"wealth": 20, "family": 15}, hidden_risk_log="为新兴市场做配套手工业加工，离土不离乡稳定增收。"),
                make_outcome("entangled", 25, "因收购商资金周转不灵拖欠半年货款，四处上门讨要账目。", {"wealth": -10, "mentality": -15}, hidden_risk_log="遭遇初期商业信用欠账考验，学会订立字据规避风险。")
            ]
        }
    ]
)

add_evt(
    "evt_1983_yanda_zhian", "era", "1983全国社会治安大整顿（“严打”）",
    [1983, 1984], [16, 45], ["ALL"], {},
    [], [], 0.85, 4, "确证",
    "1983年8月全国部署开展‘严厉打击严重刑事犯罪活动’（严打），从重从快惩处流氓、抢劫、杀人等犯罪，社会治安实现迅速根本好转，群众夜间出行重获安全感。",
    "城关广场挂起公捕公判大会巨幅横幅，军警卡车呼啸而过。街头的流氓混混、拍花拐骗与滋事阿飞被连根拔起。原本穿喇叭裤、在旱冰场吹口哨的青年纷纷理短头发，敛声屏气。",
    [
        {
            "text": "本分做人恪守规矩，夜间安心温书做工，规劝亲友远离社会不良圈子",
            "choiceTags": ["时代：1983–1984", "年龄：16–45", "地域：全国城镇", "门槛：守法市民"],
            "outcomes": [
                make_outcome("safe", 75, "遵纪守法安稳度日，走夜路再也不用提心吊胆，享受良好治安环境。", {"mentality": 15, "family": 15}, hidden_risk_log="身正不怕影子斜，严打期间规矩做人，享受社会安定红利。"),
                make_outcome("entangled", 20, "因早年借过隔壁劣迹青年十元钱被传唤协助核实笔录，洗清嫌疑。", {"mentality": -10}, hidden_risk_log="因江湖故交受短暂例行盘查，洗脱嫌疑后更懂人际分寸。"),
                make_outcome("redirected", 5, "看到治安大队招录，报名加入街道联防巡逻队，因勇敢转为公职保卫干部。", {"knowledge": 15, "wealth": 15}, new_career_track="cadre_teacher", hidden_risk_log="加入基层巡逻联防表现优异，转入体制内保卫干部编制。")
            ]
        },
        {
            "text": "在录像厅跳贴面舞起哄，与邻座因踩脚发生抓扯推搡",
            "choiceTags": ["时代：1983–1984", "年龄：17–28", "地域：城镇娱乐场所", "门槛：好动青年"],
            "outcomes": [
                make_outcome("safe", 40, "经家人紧急写检查托人作保，定性为一般民事纠纷批评释放。", {"wealth": -15, "mentality": -10}, hidden_risk_log="虚惊一场写下深刻检讨，从此脱胎换骨老实做人。"),
                make_outcome("entangled", 45, "被从严认定为扰乱公共场所秩序收容劳教一年，丢掉原有工作指标。", {"wealth": -30, "mentality": -35, "family": -20}, new_career_track="worker", hidden_risk_log="在严打风口浪尖因打闹受劳教处分，人生遭遇重大波折。"),
                make_outcome("injured", 15, "推搡冲突中左眼角被汽水瓶碎片划破，缝合五针留疤。", {"health": -25, "mentality": -20}, hidden_risk_log="录像厅纠纷负伤挂彩，成为青年时代深刻警醒教训。")
            ]
        }
    ]
)

# --- 11-20 历史事件 ---

add_evt(
    "evt_1984_shenfenzheng", "era", "第一代居民身份证制度实施",
    [1984, 1985], [16, 75], ["ALL"], {},
    [], [], 0.88, 4, "确证",
    "1984年4月国务院颁布《中华人民共和国居民身份证试行条例》，我国开始实施居民身份证制度。结束了千百年来凭借户口簿、工作证或介绍信证明身份的历史。",
    "居委会和派出所门前排起了照相长队，白色布幕挂在红砖墙上，镁光灯闪烁。大家整理着领口，第一次领到了那张塑料封膜、印着长城与单色黑白头像的身份证卡片。",
    [
        {
            "text": "拍照领证后小心塑封珍藏，凭身份证去银行开立个人独立存折",
            "choiceTags": ["时代：1984–1985", "年龄：16–75", "地域：全国", "门槛：普通公民"],
            "outcomes": [
                make_outcome("safe", 80, "拥有了全国通用的法定身份证件，出差住旅馆再也不用到处开单位介绍信。", {"knowledge": 10, "mentality": 15}, status="has_id_card", hidden_risk_log="第一代身份证见证公民个人身份权利的法定化。"),
                make_outcome("safe", 20, "领证时名字被派出所民警笔误写错一个同音字，费时一月更正。", {"mentality": -5}, hidden_risk_log="早期手工登记出现微小瑕疵，但顺利规范更正。")
            ]
        },
        {
            "text": "凭新办身份证办理边防通行证与车票，开启第一次跨省旅行远游",
            "choiceTags": ["时代：1984–1985", "年龄：18–35", "地域：城镇", "门槛：年轻市民"],
            "outcomes": [
                make_outcome("safe", 70, "凭身份证顺畅入住宿舍旅馆，饱览祖国名山大川，眼界大开。", {"knowledge": 20, "mentality": 20}, hidden_risk_log="新制度赋能个人自由流动，完成人生首次壮游。"),
                make_outcome("injured", 30, "火车站人流拥挤被扒手割破裤袋偷走钱包，所幸身份证藏在内袋。", {"wealth": -15, "mentality": -10}, hidden_risk_log="出门远游遭遇失窃受惊，学会财物贴身防范。")
            ]
        }
    ]
)

add_evt(
    "evt_1984_yanhai_kaifang", "era", "沿海14个港口城市开放与合资浪潮",
    [1984, 1986], [18, 45], ["华东", "华南", "华北", "东北"],
    {"provinces": ["shanghai", "tianjin", "guangdong", "jiangsu", "zhejiang", "shandong", "liaoning", "fujian"]},
    [], [], 0.78, 4, "确证",
    "1984年中央决定进一步开放大连、秦皇岛、天津、烟台、青岛、连云港、南通、上海、宁波、温州、福州、广州、湛江、北海14个沿海港口城市，中外合资合作企业蓬勃涌现。",
    "港口码头吊车林立，外商洽谈会与合资工厂招聘简章贴满了外贸大楼。第一批外企招录懂英语、懂机电操作的青工，身着合体工装、按时打卡、月薪翻倍的现代企业震撼着沿海年轻人。",
    [
        {
            "text": "报考合资机电/纺织大厂做熟练流水线工，接受外企严格规范管理",
            "choiceTags": ["时代：1984–1986", "年龄：18–35", "地域：沿海14开放港口", "门槛：青年工薪"],
            "outcomes": [
                make_outcome("safe", 65, "拿到比国企高出一倍的现钞工资与加班费，掌握现代ISO质量管理流程。", {"wealth": 35, "knowledge": 20}, status="joint_venture_worker", hidden_risk_log="进入早期合资外企开眼界，领跑同龄人工资水平。"),
                make_outcome("injured", 25, "车间两班倒高强度打卡劳累过度，神经衰弱视力下降。", {"health": -20, "wealth": 30}, hidden_risk_log="合资流水线高强度考核透支健康，但赚下丰厚第一桶金。"),
                make_outcome("entangled", 10, "外资因国际航运波动削减订单临时停产待料，收入骤降两个月。", {"wealth": -15, "mentality": -15}, hidden_risk_log="初步体味到国际外贸订单周期波动的不可控性。")
            ]
        },
        {
            "text": "留在原国有老港务局/机床厂，兼修夜校涉外商务英语等待机遇",
            "choiceTags": ["时代：1984–1986", "年龄：18–40", "地域：沿海老国企", "门槛：体制内员工"],
            "outcomes": [
                make_outcome("safe", 70, "学成英语出任港务局涉外货轮装卸调度主管，既有编制又享外勤津贴。", {"knowledge": 25, "wealth": 20}, status="port_cadre", hidden_risk_log="结合外向型经济提升自身外语，成为国企涉外骨干。"),
                make_outcome("entangled", 30, "眼见同龄人跳槽合资拿高薪买大件家电，心理一度难以平衡。", {"mentality": -15}, hidden_risk_log="面对沿海薪酬双轨制冲击，守住老厂安稳饭碗。")
            ]
        }
    ]
)

add_evt(
    "evt_1985_caijun_baiwan", "era", "裁军百万大精简与军转民潮",
    [1985, 1987], [18, 45], ["ALL"], {},
    ["soldier"], [], 0.85, 4, "确证",
    "1985年中央军委决定裁减军队员额100万，大批铁道兵、基建工程兵集体转业为铁道部与建设部工程局，军工企业大力推进‘军转民’生产摩托车、电冰箱与民品。",
    "营房大礼堂里军歌悲壮嘹亮，摘下领章帽徽的那一刻，钢铁般的男儿热泪盈眶。背起帆布行囊，数十万转业官兵退伍返乡或集体成建制并入地方建筑路桥单位。",
    [
        {
            "text": "服从整编集体转业为地方工程路桥集团施工队长，转战全国筑路",
            "choiceTags": ["时代：1985–1987", "年龄：20–45", "地域：全国工程线", "门槛：工程转业官兵"],
            "outcomes": [
                make_outcome("safe", 65, "保持军人优良作风雷厉风行，带队修建首条高等级公路荣立集体一等功。", {"wealth": 25, "knowledge": 20, "mentality": 25}, new_career_track="worker", status="veteran_builder", hidden_risk_log="脱下戎装投身国家大基建，成为路桥交通工程脊梁。"),
                make_outcome("injured", 25, "隧道开凿遭遇瓦斯涌出与塌方砸伤右臂，休养半年评轻残退二线。", {"health": -30, "wealth": 20}, new_career_track="worker", hidden_risk_log="转业工程施工负工伤致残，转为调度室主任。"),
                make_outcome("entangled", 10, "常年随筑路队风餐露宿浪迹荒野，与家人两地分居子女疏远。", {"family": -25, "mentality": -15}, hidden_risk_log="为国家大通道四海为家，家庭团聚成为奢侈期盼。")
            ]
        },
        {
            "text": "申请转业安置回原籍县城公安局或司法局，当基层执法干警",
            "choiceTags": ["时代：1985–1987", "年龄：22–40", "地域：原籍城镇", "门槛：转业干部"],
            "outcomes": [
                make_outcome("safe", 70, "安置进入县公安局巡警保卫科，分到单位福利房，守在妻儿父母身边。", {"wealth": 20, "family": 25, "mentality": 20}, new_career_track="cadre_teacher", status="police_officer", hidden_risk_log="转业落户家乡公安系统，家庭事业双圆满。"),
                make_outcome("injured", 20, "抓捕跨省重大盗窃团伙时被歹徒用匕首划伤左小臂，荣立三等功。", {"health": -20, "mentality": 20, "wealth": 10}, hidden_risk_log="转业从警忠于职守负伤立功，深受百姓拥戴。"),
                make_outcome("entangled", 10, "因县级财政紧张连续数月缓发警衔津贴，日子过得颇为清苦拮据。", {"wealth": -15, "mentality": -10}, hidden_risk_log="转业地方遭遇财政困难期，咬牙同舟共济。")
            ]
        }
    ]
)

add_evt(
    "evt_1985_dagongchao_dongnan", "era", "“孔雀东南飞”与珠三角打工潮",
    [1985, 1989], [17, 30], ["ALL"], {"urbanRural": "rural"},
    ["farmer"], [], 0.80, 4, "确证",
    "1980年代中后期数以百万计的内地农村青年背上编织袋涌入东莞、深圳、顺德等珠三角城镇。‘三来一补’玩具厂、电子厂拔地而起，中国第一代打工妹、打工仔登上历史舞台。",
    "春运绿皮列车挤得连过道和水池都站满了人。年轻人们提着印有‘上海’字样的旅行包，操着各省方言涌出广州火车站。街道上‘招录女工、包吃包住’的白纸红字随处可见。",
    [
        {
            "text": "跟随同村老乡南下东莞玩具电子厂，在日光灯下做流水线焊锡打包",
            "choiceTags": ["时代：1985–1989", "年龄：17–30", "地域：广东珠三角", "门槛：内地农家青年"],
            "outcomes": [
                make_outcome("safe", 60, "每月寄回两百元汇款单给老家盖楼，年底给父母寄回彩色画报与年货。", {"wealth": 35, "family": 20}, new_career_track="worker", status="migrant_pioneer", hidden_risk_log="第一代农民工典范，用流水线汗水撑起内地老家半边天。"),
                make_outcome("injured", 28, "焊锡松香烟雾刺鼻且通宵加班导致重度咽喉炎与手指烫伤。", {"health": -25, "wealth": 30}, new_career_track="worker", hidden_risk_log="恶劣劳保条件落下慢性咽喉病，但赚下扎实家底。"),
                make_outcome("entangled", 12, "路上遭遇火车站黑中介诈骗工本费，滞留街头靠老乡接济进厂。", {"wealth": -15, "mentality": -20}, new_career_track="worker", hidden_risk_log="初入大都市遭遇江湖险恶被骗，幸得同乡施以援手。")
            ]
        },
        {
            "text": "留在老家承包田伺候庄稼，照顾体弱多病的父母双亲",
            "choiceTags": ["时代：1985–1989", "年龄：18–35", "地域：内地乡村", "门槛：留守青年"],
            "outcomes": [
                make_outcome("safe", 70, "在父母膝前尽孝，农作有条不紊，村里小家庭和乐安宁。", {"family": 25, "health": 15}, hidden_risk_log="守望家乡麦田尽孝，享受传统乡村安稳淳朴。"),
                make_outcome("entangled", 30, "看着南下同伴过年带回洋气的录音机与尼龙大衣，内心五味杂陈。", {"mentality": -15, "wealth": -10}, hidden_risk_log="留守故土面对城乡收入拉大，饱尝心理落差。")
            ]
        }
    ]
)

add_evt(
    "evt_1985_chuguore_tuofu", "era", "托福外语热与自费留学潮",
    [1985, 1989], [20, 32], ["ALL"], {"urbanRural": "urban"},
    ["higher_ed_degree"], [], 0.72, 4, "确证",
    "1985年中国取消自费留学审批资格限制，放宽留学政策。大学校园刮起强劲的‘托福热’与‘出国狂潮’，红宝书词表与听力磁带成为青年学子人手一份的标配。",
    "高校阶梯教室通宵坐满刷题的学生，录音机里传来美音听力朗读。为了报考托福，大家连夜带着军大衣在考点门外排队三天三夜。大洋彼岸的奖学金成了改变阶层命运的最亮灯塔。",
    [
        {
            "text": "咬牙啃完厚厚词典考下高分托福，向北美大学狂投申请争取全奖",
            "choiceTags": ["时代：1985–1989", "年龄：20–32", "地域：大中城市高校", "门槛：本科学历/英语功底"],
            "outcomes": [
                make_outcome("safe", 55, "斩获全额奖学金顺利飞赴北美攻读博士，开启跨国学术与职场征程。", {"knowledge": 40, "wealth": 25, "mentality": 20}, status="overseas_scholar", hidden_risk_log="80年代自费留学成功飞跃重洋，跻身华人海外精英行列。"),
                make_outcome("entangled", 35, "成绩虽过关但签证数次遭遇无理拒签，耗费数千元积蓄遗憾抱憾留国。", {"wealth": -25, "mentality": -25}, hidden_risk_log="签证受挫断了出国念想，回国内高校继续带研究生。"),
                make_outcome("redirected", 10, "因精通外语被新成立的中外合资代表处高薪招为主管翻译。", {"wealth": 35, "knowledge": 25}, new_career_track="merchant", hidden_risk_log="借外语优势涉足沿海涉外商务，抢先享受外贸红利。")
            ]
        },
        {
            "text": "安心留守国内科研教学岗位，参与国家自然科学基金早期重点项目",
            "choiceTags": ["时代：1985–1989", "年龄：22–35", "地域：科研院所", "门槛：青年教师/助教"],
            "outcomes": [
                make_outcome("safe", 65, "作为国内青年学术骨干破格提拔为副研究员，分得两居室福利套房。", {"knowledge": 30, "wealth": 20, "family": 20}, status="promoted_scholar", hidden_risk_log="留守国内挑大梁，快速晋升为科研学术带头人。"),
                make_outcome("entangled", 35, "面对‘造导弹不如卖茶叶蛋’的脑体倒挂，每月领薄弱死工资感到迷茫。", {"mentality": -20, "wealth": -10}, hidden_risk_log="在脑体倒挂岁月坚守清贫书桌，历经考验。")
            ]
        }
    ]
)

add_evt(
    "evt_1986_yiwujiaoyu", "era", "《义务教育法》颁布与九年制普及",
    [1986, 1989], [6, 15], ["ALL"], {},
    [], [], 0.90, 5, "确证",
    "1986年4月全国人大审议通过《中华人民共和国义务教育法》，确立国家实行九年制义务教育制度，普及少年儿童免费基础教育，成为中国现代教育史里程碑。",
    "村头泥泞的土台阶被水泥台阶取代，琅琅书声在瓦房小学里回荡。黑板上写着‘再穷不能穷教育，再苦不能苦孩子’。适龄孩童必须送进学校，辍学打工受到严格律法约束。",
    [
        {
            "text": "每天背着缝补的书包步行五里泥路上学，刻苦自律打牢各门功课基础",
            "choiceTags": ["时代：1986–1989", "年龄：6–15", "地域：全国城乡", "门槛：适龄学生"],
            "outcomes": [
                make_outcome("safe", 75, "顺利读完初中九年义务教育，数理语文基础极为扎实，名列前茅考入县一中。", {"knowledge": 30, "mentality": 15}, status="middle_school_graduate", hidden_risk_log="完整享受九年义务教育红利，为后半生奠定知识基石。"),
                make_outcome("injured", 15, "冬天雨雪路滑在山路上摔倒擦伤膝盖，仍瘸着腿坚持到校上早自习。", {"health": -15, "knowledge": 25}, hidden_risk_log="求学之路艰辛但意志如铁，深得师生赞赏。"),
                make_outcome("entangled", 10, "因学校缺少合格外语老师，初中英语底子薄弱，成为偏科隐患。", {"knowledge": 10}, hidden_risk_log="乡村教育资源匮乏造成外语薄弱，日后加倍补足。")
            ]
        },
        {
            "text": "父母观念保守认为读书无用，暗中帮家里在田头放羊做手工贴补家用",
            "choiceTags": ["时代：1986–1989", "年龄：10–15", "地域：贫困偏远山村", "门槛：特困家庭子女"],
            "outcomes": [
                make_outcome("safe", 50, "被村委会与驻村教师三次登门劝返复课，终于保住求学之路。", {"knowledge": 15, "family": 10}, status="returned_student", hidden_risk_log="在基层干部与乡村教师挽救下重返课堂，改变辍学命运。"),
                make_outcome("entangled", 50, "过早辍学在家务农，因文化水平不足，后半生打工就业严重受限。", {"wealth": 10, "knowledge": -25, "mentality": -15}, status="status_dropped_out", hidden_risk_log="失去义务教育庇护过早辍学，成为一生难以弥补的遗憾。")
            ]
        }
    ]
)

add_evt(
    "evt_1986_laodonghetong", "era", "国企劳动合同制试点与铁饭碗松动",
    [1986, 1988], [18, 50], ["ALL"], {"urbanRural": "urban"},
    ["worker"], [], 0.75, 4, "确证",
    "1986年国务院发布国营企业实行劳动合同制暂行规定，明确国营企业招用工人一律实行劳动合同制，彻底打破了‘一进国企干一辈子’的铁饭碗大锅饭格局。",
    "厂部人事科的大桌上摊开一份份蓝皮合同书。老工人们围在一旁议论纷纷，新招录的青年职工按手印签约。‘能进能出、打破铁饭碗’的标语让工厂大院泛起阵阵不安涟漪。",
    [
        {
            "text": "作为新进合同制工人踏实苦干，狠抓数控车床与装配技能争当先进",
            "choiceTags": ["时代：1986–1988", "年龄：18–35", "地域：国企工矿", "门槛：新入厂青工"],
            "outcomes": [
                make_outcome("safe", 70, "凭过硬技术指标被评为标兵工人，签订首批五年长期稳定劳动合同。", {"wealth": 25, "knowledge": 20}, status="contract_worker", hidden_risk_log="顺应劳动制度改革靠技能立足，成为国企骨干技工。"),
                make_outcome("entangled", 30, "因车间生产线整顿被转入辅助包装组，工资奖金减半，倍感压力。", {"wealth": -15, "mentality": -15}, hidden_risk_log="初入职场尝到合同制流动压力，督促自己不断学技术。")
            ]
        },
        {
            "text": "仗着老职工正式编制身份安于现状，在后勤仓库喝茶看报混日子",
            "choiceTags": ["时代：1986–1988", "年龄：30–55", "地域：老国企机关", "门槛：原固定工编制"],
            "outcomes": [
                make_outcome("safe", 60, "继续享受大锅饭编制工资，但面对改革浪潮内心总泛着一丝惶惶不可终日。", {"wealth": 10, "mentality": -10}, hidden_risk_log="固守传统体制舒适区，未能提前掌握市场化生存技能。"),
                make_outcome("entangled", 40, "因考核长期处于末位被调至看大门保安岗，威望与奖金大打折扣。", {"wealth": -15, "mentality": -20}, hidden_risk_log="考核落后转岗边际职位，为九十年代下岗危机埋下隐患。")
            ]
        }
    ]
)

add_evt(
    "evt_1987_tanqinchao_laobing", "era", "台湾老兵探亲潮与两岸亲人相认",
    [1987, 1989], [15, 80], ["ALL"], {},
    [], [], 0.70, 5, "确证",
    "1987年11月台湾当局开放老兵赴大陆探亲，结束了两岸近40年的隔绝状态。白发苍苍的老兵提着三大件五小件踏上故土，老家亲人抱头痛哭，骨肉终团聚。",
    "村头和弄堂口驶入一辆挂着外埠牌照的出租车，戴金丝眼镜、穿笔挺西服的白发老翁颤巍巍下车，手里紧攥着泛黄的老家宗谱。离别四十载，相顾泪满巾。",
    [
        {
            "text": "热情迎接远归的海外至亲骨肉，摆家宴叙离情，陪同修缮祖坟宗祠",
            "choiceTags": ["时代：1987–1989", "年龄：15–80", "地域：全国", "门槛：涉台侨属亲友"],
            "outcomes": [
                make_outcome("safe", 75, "亲情融洽获赠彩电录像机大件家电与侨汇资助，祖坟得以重修祭扫。", {"wealth": 35, "family": 35, "mentality": 25}, status="overseas_family_tied", hidden_risk_log="两岸骨肉相认获侨汇支持，家境与人脉实现巨大跨越。"),
                make_outcome("entangled", 25, "因远亲资助资金分配不均与同族兄弟产生隔阂，引起财产口舌纠纷。", {"family": -20, "wealth": 15}, hidden_risk_log="外来侨资带来财富的同时引发宗族分配矛盾，费力平息。")
            ]
        },
        {
            "text": "协助地方台办与统战部门组织接待联谊，宣传家乡投资经贸环境",
            "choiceTags": ["时代：1987–1989", "年龄：25–60", "地域：县市城镇", "门槛：体制干部/知识分子"],
            "outcomes": [
                make_outcome("safe", 70, "成功促成台商亲友在县城投资创办第一家中外合资鞋服厂，受市委记功表彰。", {"knowledge": 20, "wealth": 25, "mentality": 20}, status="taiwan_liaison", hidden_risk_log="以侨为桥招商引资，成为当地改革开放涉外骨干。"),
                make_outcome("entangled", 30, "沟通繁琐垫支多笔接待经费迟迟未报销，工作劳心伤神。", {"wealth": -10, "mentality": -15}, hidden_risk_log="涉台接待工作繁重琐碎，历经协调磨练。")
            ]
        }
    ]
)

add_evt(
    "evt_1987_kenji_qianmen", "era", "肯德基中国首店在前门开业",
    [1987, 1988], [8, 55], ["华北"], {"provinces": ["beijing", "tianjin", "hebei"]},
    [], [], 0.75, 4, "确证",
    "1987年11月中国首家美式快餐肯德基在北京前门繁华地段开业。三层楼的大店门口天天排长队，原味吮指原味鸡与土豆泥成为国人接触西方快餐文化的早期窗口。",
    "前门大街飘着炸鸡的焦香，玻璃橱窗里桑德斯上校笑脸迎人。门口排队的人流拐了两个弯，有人为了尝一块两块五毛钱的炸鸡，宁肯攒下半个月的零花钱。",
    [
        {
            "text": "拿出省下的半月零花钱带家人尝鲜排队购买原味炸鸡和土豆泥",
            "choiceTags": ["时代：1987–1988", "年龄：8–50", "地域：京津华北", "门槛：城市居民"],
            "outcomes": [
                make_outcome("safe", 75, "吃上一口酥脆多汁的炸鸡，在红色餐盒前留影合影，成为大院里炫耀谈资。", {"wealth": -10, "family": 20, "mentality": 15}, status="tried_western_fastfood", hidden_risk_log="第一次品尝洋快餐，亲身感受对外开放的现代商业气息。"),
                make_outcome("safe", 25, "觉得炸鸡油腻不对胃口，心疼花掉的两张大钞，但满足了全家好奇心。", {"wealth": -10, "mentality": 5}, hidden_risk_log="体验西洋新鲜事物后回归传统饮食，生活充满时代烟火。")
            ]
        },
        {
            "text": "敏锐洞察现代快餐连锁运营模式，在附近小吃街学做本土脆皮炸鸡摊",
            "choiceTags": ["时代：1987–1988", "年龄：20–45", "地域：京津城镇", "门槛：个体经营者"],
            "outcomes": [
                make_outcome("safe", 65, "以低一半的平民价格做国产炸鸡风靡街巷，成为前门红火的万元个体户。", {"wealth": 40, "knowledge": 15}, new_career_track="merchant", status="fastfood_entrepreneur", hidden_risk_log="敏锐模仿洋快餐本土化，抢占早期大众小吃餐饮蓝海。"),
                make_outcome("injured", 25, "操作电炸锅时不慎被高温沸油溅伤右手背，住院包扎三周。", {"health": -20, "wealth": 20}, new_career_track="merchant", hidden_risk_log="炸锅操作受烫伤留疤，但生意越做越大。"),
                make_outcome("entangled", 10, "油烟扰民遭附近居民举报整改，搬迁摊位损失一周营业额。", {"wealth": -15, "mentality": -15}, hidden_risk_log="小吃摊初创遭遇合规波折，学会规范排烟经营。")
            ]
        }
    ]
)

add_evt(
    "evt_1988_jiage_chuangguan", "era", "1988年“价格闯关”与全国抢购狂潮",
    [1988, 1989], [16, 75], ["ALL"], {},
    [], [], 0.90, 4, "确证",
    "1988年夏中央尝试放开绝大多数商品价格进行‘价格闯关’。由于通胀预期，全国大中城市爆发罕见挤兑抢购风潮，市民囤积火柴、肥皂、食盐、电风扇甚至毛线面料。",
    "百货大楼的柜台被围得水泄不通，货架在半天内被扫荡一空。人们手里攥着厚厚的人民币和存折，不管有用没用，见货就买，扛着整箱肥皂和几台电风扇穿过混乱街道。",
    [
        {
            "text": "跟随街坊人流连夜排队提款，抢购保值棉花、火柴与几箱日用肥皂",
            "choiceTags": ["时代：1988–1989", "年龄：18–75", "地域：全国城镇", "门槛：城镇市民"],
            "outcomes": [
                make_outcome("safe", 60, "抢购的物资虽然占满床底，但确实在随后数月物价飞涨中省下了过日子钱。", {"wealth": 15, "family": 15}, hidden_risk_log="参与88抢购潮自保过日子，囤积物资抵御通胀波动。"),
                make_outcome("injured", 25, "百货商场门前极度拥挤发生踩踏推搡，脚踝被铁门挤压骨裂休养。", {"health": -25, "wealth": -10}, hidden_risk_log="在商场抢购人潮中被踩伤脚踝，体味到抢购盲动之苦。"),
                make_outcome("entangled", 15, "高位盲目抢购了三台残次黑白电视机，随后价格平抑亏掉半年积蓄。", {"wealth": -30, "mentality": -20}, hidden_risk_log="盲目抢购囤积残次家电折损身家，吸取深刻理财教训。")
            ]
        },
        {
            "text": "保持冷静理性不参与挤兑，将积蓄存为定期保值储蓄对抗通胀",
            "choiceTags": ["时代：1988–1989", "年龄：22–65", "地域：全国", "门槛：理性居民"],
            "outcomes": [
                make_outcome("safe", 70, "国家随后出台保值储蓄补贴利息政策，本息安然无恙，免去折腾搬运之苦。", {"wealth": 10, "mentality": 20}, hidden_risk_log="冷静不盲从跟风抢购，依托保值储蓄平稳度过物价闯关期。"),
                make_outcome("entangled", 30, "短时间内物价翻倍导致生活日用开支骤增，节衣缩食两三年。", {"wealth": -20, "mentality": -15}, hidden_risk_log="物价上涨侵蚀固定工薪，度过数年精打细算的清贫岁月。")
            ]
        }
    ]
)

print(f"Adding era 1978-1999 events... Current count: {len(events)}")
