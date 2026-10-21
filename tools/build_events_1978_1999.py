# tools/build_events_1978_1999.py
# -*- coding: utf-8 -*-
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

# 1. 1978 小岗村大包干
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

# 2. 1978 首批公派留学生赴美
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

# 3. 1979 知青大返城与顶替接班
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

# 4. 1980 深圳特区建立与蛇口开山炮
add_evt(
    "evt_1980_shenzhen_tequ", "era", "深圳经济特区建立与开山打拼",
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

# 5. 1980 独生子女政策与光荣证
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

# 6. 1980 国企福利分房排队
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

# 7. 1981 首届中国女排夺冠
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

# 8. 1982 义乌第一代小商品市场
add_evt(
    "evt_1982_yiwu_xiaoshangpin", "era", "义乌小商品市场开放与敲糖帮下江南",
    [1982, 1985], [18, 50], ["华东"], {"provinces": ["zhejiang", "jiangsu", "anhui", "jiangxi"]},
    ["farmer"], [], 0.75, 4, "确证",
    "1982年浙江义乌县委正式提出‘四个允许’（允许农民经商、允许从事长途贩运、允许开放城乡市场、允许多渠道竞争），开放稠城镇第一代马路小商品市场，敲糖帮走向全国。",
    "青石板路两侧支起简易水泥板摊位，拨浪鼓的咚咚声清脆悦耳。针线包、尼龙袜、塑料纽扣铺满布单，县委干部的批条保护着这些曾被称为投机倒把的鸡毛换糖小挑担。",
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

# 9. 1983 全国严打
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

# 10. 1984 乡镇企业异军突起
add_evt(
    "evt_1984_xiangzhen_qiye", "era", "乡镇企业‘异军突起’与离土不离乡",
    [1984, 1987], [18, 50], ["ALL"], {"urbanRural": "rural"},
    ["farmer"], [], 0.82, 4, "确证",
    "1984年中央一号文件放宽农村劳动力二三产业限制，邓小平赞誉乡镇企业‘异军突起’。苏南模式、珠江模式迅速蔓延，数千万农民‘洗脚上田’进厂当工薪工人。",
    "田垄尽头的村口竖起‘红星针织印染厂’的大招牌，织机嗒嗒声昼夜不停。村民们收工后洗干净脚上的泥巴换上胶鞋进车间计件。村里大喇叭天天催着招录车工和打包女工。",
    [
        {
            "text": "报名进乡镇企业当全职熟练冲压/印染工，拿稳定计件现金工资",
            "choiceTags": ["时代：1984–1987", "年龄：18–45", "地域：乡村集镇", "门槛：农村劳力"],
            "outcomes": [
                make_outcome("safe", 65, "每月领现钞工资给家里盖上三间大瓦房，添置永久自行车与收录机。", {"wealth": 30, "family": 20}, new_career_track="township_worker", status="township_worker", hidden_risk_log="抓住乡镇企业腾飞机遇进厂，成为中国第一代富裕起来的农民工。"),
                make_outcome("injured", 25, "机器防护简陋不慎挤伤右手两指，厂部赔偿三月工伤工资。", {"health": -20, "wealth": 15}, new_career_track="township_worker", hidden_risk_log="初期乡镇厂机械防护简陋负轻伤，伤愈后转为质检员。"),
                make_outcome("entangled", 10, "化工厂刺鼻染料气味引发严重过敏性哮喘咳嗽，被迫辞工回家休养。", {"health": -25, "wealth": 10}, hidden_risk_log="乡镇小化工厂污染伤及呼吸道，及时离厂返家保全身体。")
            ]
        },
        {
            "text": "坚守自留承包地搞蔬菜温棚与生猪养殖，当科技种粮大户",
            "choiceTags": ["时代：1984–1987", "年龄：20–55", "地域：农村腹地", "门槛：种养能手"],
            "outcomes": [
                make_outcome("safe", 70, "自建两座反季节塑料大棚供应县城菜市，年节出栏十头大肥猪净赚数千。", {"wealth": 35, "health": 10}, status="expert_farmer", hidden_risk_log="精耕农业现代养殖，成为全县表彰的科技示范万元户。"),
                make_outcome("entangled", 30, "遭遇春季猪瘟疫病折损半数仔猪，幸得县兽医站上门打疫苗止损。", {"wealth": -20, "mentality": -15}, hidden_risk_log="养殖遇瘟疫波折损失，在坎坷中掌握科学防疫技能。")
            ]
        }
    ]
)

print("Writing events_1978_1999 builder script...")
