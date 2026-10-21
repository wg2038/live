# tools/build_events_1937_1949_full.py
# -*- coding: utf-8 -*-
"""
生成 1937–1949 年共 40 条全要素历史事件库，严格遵循：
- choiceTags 四元标签
- safe / injured / entangled / redirected / fatal 多元权重分支 (fatal <= 2-5%)
- hiddenRiskLog 用于终局因果回顾
- factLevel (确证/估计/文学化)
- 历史沉郁、克制、真实
"""

import json
import os
import sys

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

# 1. 1937 卢沟桥事变与全面抗战爆发
add_evt(
    "evt_1937_lugouqiao_shibian", "era", "卢沟桥事变：全面抗战与平津告急",
    [1937, 1937], [12, 65], ["华北"],
    {"provinces": ["beijing", "tianjin", "hebei", "shanxi"]},
    [], [], 0.95, 4, "确证",
    "1937年7月7日夜日军在北平宛平城卢沟桥挑起事变。第二十九军奋起抵抗，全国抗日战争全面爆发。随后平津相继沦陷，中华民族到了最危险的时刻。",
    "永定河畔炮声隆隆，宛平城墙被炮火炸开豁口。北平城内人心惶惶，前门火车站挤满了拖家带口的逃难百姓。城楼上贴着‘誓与北平共存亡’的抗战布告，战乱烽火吞没了宁静古都。",
    [
        {
            "text": "随学校、工厂撤离人员连夜挤上难民列车南下保定转赴后方，保留读书与实业火种",
            "choiceTags": ["时代：1937", "年龄：14–50", "地域：平津及华北", "门槛：学生/职员/市民"],
            "outcomes": [
                make_outcome("safe", 60, "历经颠簸跋涉千里南下抵达汉口，虽盘缠散尽但成功避开沦陷浩劫，转入后方复学工作。", {"wealth": -20, "knowledge": 20, "mentality": 15}, status="southward_evacuee_1937", hidden_risk_log="卢沟桥烽火中果断南撤保留生机，成为流亡大后方的建设骨干。"),
                make_outcome("injured", 25, "挤列车车顶被急刹车甩下摔伤右肋骨与擦伤双手，受红十字会难民所收治转运。", {"health": -25, "wealth": -15}, hidden_risk_log="南下逃难路上负伤流落，备尝战乱流离艰辛。"),
                make_outcome("entangled", 13, "途中随身金银细软与毕业证书全被溃兵洗劫，赤贫流落河南洛阳以代写书信糊口。", {"wealth": -35, "mentality": -15}, hidden_risk_log="逃难遇劫一贫如洗，凭一手毛笔字在异乡艰难维生。"),
                make_outcome("fatal", 2, "在车站遭遇敌机低空俯冲扫射不幸中弹罹难。", is_fatal=True, hidden_risk_log="在平津南下逃难车站遭遇空袭不幸遇难。")
            ]
        },
        {
            "text": "留守北平故土暗中看守老宅，闭门谢客绝不出仕伪政权，保持民族气节",
            "choiceTags": ["时代：1937", "年龄：16–65", "地域：沦陷平津", "门槛：平津本地市民"],
            "outcomes": [
                make_outcome("safe", 65, "靠地窖私藏粮食度日，坚决拒领伪政权差事，靠旧书变卖维持清贫生活，守住晚节。", {"wealth": -15, "mentality": 25, "family": 15}, status="beiping_unyielding_resident", hidden_risk_log="在北平沦陷期隐居守节，展现坚贞不屈的中华士民风骨。"),
                make_outcome("injured", 20, "因暗中接济抗日地下交通员被日伪宪兵盘查毒打致耳膜穿孔，经亲友重金赎出。", {"health": -30, "wealth": -30}, hidden_risk_log="暗助抗日受日伪严刑拷打致残，虽破财但守住忠义。"),
                make_outcome("entangled", 15, "因家中老宅被日伪特工强行霸占为办公据点，被驱逐至外城破庙栖身。", {"wealth": -40, "family": -20}, hidden_risk_log="祖产遭强占流落破庙，体会亡国奴之深重耻辱。")
            ]
        }
    ]
)

# 2. 1937 淞沪会战与沿海内迁
add_evt(
    "evt_1937_songhu_huizhan", "era", "淞沪会战血肉磨坊与中国实业高校大内迁",
    [1937, 1937], [14, 60], ["华东"],
    {"provinces": ["shanghai", "jiangsu", "zhejiang"]},
    [], [], 0.95, 4, "确证",
    "1937年8月淞沪会战爆发。中日双方投入百万大军激战三月，粉碎了日军‘三个月灭亡中国’的狂妄企图。与此同时，林继庸等人组织沿海数百家民营工厂、高校及精密机器拆卸西迁，抢救民族工业血脉。",
    "苏州河两岸火光冲天，闸北在炮火下化为瓦砾焦土。四行仓库墙头弹痕累累，八百壮士血战孤军。黄浦江码头上，工人们手拉肩扛把重达数吨的机床吊上木船，冒着敌机轰炸逆长江而上驶向西南。",
    [
        {
            "text": "若为上海工矿技工或技术员，随厂拆卸车床发电机，押运重型设备沿长江千里西迁入川",
            "choiceTags": ["时代：1937", "年龄：18–50", "地域：上海及苏浙", "门槛：产业工人/技术骨干"],
            "outcomes": [
                make_outcome("safe", 65, "突破长江险滩将全套机床完好无损运抵重庆大后方重建工厂，成为抗战后方工业脊梁。", {"knowledge": 30, "wealth": 20, "mentality": 25}, new_career_track="worker", status="industrial_evacuation_hero", hidden_risk_log="淞沪撤退中抢救民族工业机床西迁，在大后方支撑军工弹药生产。"),
                make_outcome("injured", 30, "在三峡险滩拉纤抢运机床遭遇缆绳崩断抽伤右腿胫骨骨裂，拄拐坚持复工。", {"health": -30, "wealth": 15}, new_career_track="worker", status="wounded_industrial_carrier", hidden_risk_log="三峡抢运机器受重伤，为民族工业保留抗战火种立大功。"),
                make_outcome("fatal", 5, "运输船在宜昌转口码头遭遇敌机特等航弹轰炸沉江不幸殉职。", is_fatal=True, hidden_risk_log="在宜昌抢运工厂内迁机器时遭遇空袭牺牲。")
            ]
        },
        {
            "text": "身为平民百姓，协助后方战地救护队运送前线伤兵，捐出全部门板旧布包扎伤口",
            "choiceTags": ["时代：1937", "年龄：14–60", "地域：淞沪战区周边", "门槛：热心民众"],
            "outcomes": [
                make_outcome("safe", 75, "救治转移数百名重伤战士，受到第三战区司令长官部发给抗战后援功勋奖状。", {"mentality": 30, "family": 20, "wealth": -10}, status="songhu_volunteer_helper", hidden_risk_log="以满腔爱国热血支前救护淞沪伤兵，谱写军民抗战浩歌。"),
                make_outcome("injured", 25, "在四行仓库周边冒火线抢运伤员被步枪流弹贯穿左肩，伤愈留疤。", {"health": -30, "mentality": 25}, hidden_risk_log="前线火线抢救负伤留疤，成为淞沪铁血见证者。")
            ]
        }
    ]
)

# 3. 1937 南京保卫战与平民避险
add_evt(
    "evt_1937_nanjing_baowei", "era", "1937南京保卫战烽火与避难逃离",
    [1937, 1937], [8, 70], ["华东"],
    {"provinces": ["jiangsu", "anhui"]},
    [], [], 0.96, 4, "确证",
    "1937年12月南京保卫战失利，侵华日军攻占南京城。侵略军展开灭绝人性的屠杀与暴行，造成三十万以上中国同胞惨遭杀害。拉贝、魏特琳等国际友人设立安全区保护难民，中华民族遭遇亘古未有之惨祸。",
    "雨花台与紫金山炮火连天，城门倾颓黑烟滚滚。下关码头挤满了呼天抢地的数十万军民，江面无船，波涛汹涌。城内火光冲天，枪声凄厉，生与死的界限只在转瞬之间。",
    [
        {
            "text": "在城破前夕千方百计寻得残破木筏横渡滚滚长江向江北逃生，避开屠城浩劫",
            "choiceTags": ["时代：1937", "年龄：12–65", "地域：江苏南京及周边", "门槛：逃难民众"],
            "outcomes": [
                make_outcome("safe", 50, "趁黑夜冒险渡江抵达江北浦口，虽受风寒九死一生脱险逃入安徽腹地保全性命。", {"health": -15, "mentality": 20, "wealth": -25}, status="nanjing_miracle_survivor", hidden_risk_log="在南京大屠杀前夜冒险渡江逃生，成为浩劫中的铁血幸存者。"),
                make_outcome("injured", 42, "江心木筏被激流打翻呛水昏迷，漂至江心洲受渔民救起，肺部重度吸入性感染发烧一月。", {"health": -40, "wealth": -30}, hidden_risk_log="渡江翻船溺水伤肺幸存，后半生饱尝战后创伤。"),
                make_outcome("fatal", 5, "在下关江滩抢渡时遭遇敌低空战机机枪密集扫射不幸罹难。", is_fatal=True, hidden_risk_log="在南京下关渡江时遭遇敌机扫射不幸罹难。"),
                make_outcome("entangled", 3, "成功逃至皖南山区与全家失散，在此后八年间辗转多省四处寻亲。", {"family": -40, "mentality": -25}, hidden_risk_log="战乱流离骨肉失散，历经八年烽火苦寻家人。")
            ]
        },
        {
            "text": "躲入拉贝与魏特琳设立的金陵女子文理学院国际安全区，避难庇护",
            "choiceTags": ["时代：1937", "年龄：8–70", "地域：南京城内", "门槛：城内被困妇孺"],
            "outcomes": [
                make_outcome("safe", 60, "在国际委员会中立旗帜庇护下分到少许稀粥，在防空地下室熬过最黑暗的数周洗劫。", {"family": 15, "mentality": -15, "wealth": -35}, status="safety_zone_survivor", hidden_risk_log="在国际安全区庇护下九死一生幸存，见证历史至暗时刻。"),
                make_outcome("injured", 35, "躲避敌搜查从二楼窗台跳下摔断右脚踝骨裂，由国际救护人员敷药隐匿保命。", {"health": -35, "mentality": -25}, hidden_risk_log="安全区避险摔伤致残幸存，深印战争浩劫创伤。"),
                make_outcome("fatal", 5, "被强行破门搜捕的日军当场抓捕不幸罹难。", is_fatal=True, hidden_risk_log="在南京城内遭遇强暴搜捕不幸遇难。")
            ]
        }
    ]
)

# 4. 1937 平型关大捷
add_evt(
    "evt_1937_pingxingguan_dajie", "era", "平型关大捷：打破日军“不可战胜”神话",
    [1937, 1937], [18, 30], ["华北"],
    {"provinces": ["shanxi", "hebei"]},
    [], [], 0.85, 4, "确证",
    "1937年9月八路军第一一五师在山西平型关设伏，伏击日军精锐第五师团辎重部队。歼敌千余人，缴获大批辎重枪炮，取得全国抗战以来中国军队第一个重大胜利，极大地振奋了全国军民抗战信心。",
    "乔沟古道两侧绝壁如削，秋雨过后道路泥泞不堪。日军车队在深沟里进退维谷，马达轰鸣。突然山头手榴弹如暴雨砸下，八路军战士跃出堑壕与敌展开白刃肉搏，红缨枪与刺刀寒光闪烁。",
    [
        {
            "text": "随八路军一一五师埋伏在乔沟山头，吹响冲锋号端刺刀冲入敌阵白刃肉搏",
            "choiceTags": ["时代：1937", "年龄：18–28", "地域：晋东北前线", "门槛：热血八路军战士"],
            "outcomes": [
                make_outcome("safe", 55, "白刃战刺倒两名敌寇缴获战马三匹，荣立战功升任排长，随部队开赴五台山创建根据地。", {"mentality": 40, "knowledge": 15, "wealth": 15}, status="pingxingguan_combat_hero", hidden_risk_log="平型关大捷战斗功臣，打破日寇不可战胜神话，成为八路军铁血骨干。"),
                make_outcome("injured", 40, "肉搏战被刺刀刺中左大腿贯通伤与擦破腹部，经老乡用土法马齿苋敷裹救治重返连队。", {"health": -35, "mentality": 25, "wealth": 10}, status="wounded_eighth_route_veteran", hidden_risk_log="平型关白刃战负重伤留疤，成为一生的抗战荣耀。"),
                make_outcome("fatal", 5, "在抢夺敌辎重车机枪掩体时遭遇掷弹筒近距离击中壮烈牺牲。", is_fatal=True, hidden_risk_log="在平型关首战阻击敌辎重联队时壮烈牺牲。")
            ]
        },
        {
            "text": "作为晋东北当地老乡，带领青壮年抬担架翻越险峻山梁抢运伤员与缴获军械",
            "choiceTags": ["时代：1937", "年龄：16–50", "地域：山西灵丘周边", "门槛：支前老乡"],
            "outcomes": [
                make_outcome("safe", 85, "一夜间将百余名重伤员安全转运入深山密洞老乡家，获八路军政治部发给功勋奖状与银元。", {"mentality": 25, "family": 20, "wealth": 15}, status="shanxi_logistics_supporter", hidden_risk_log="平型关大捷支前后勤功勋，筑牢军民鱼水深情。"),
                make_outcome("injured", 15, "夜间山路湿滑抬担架滑落陡坎扭伤右脚踝，仍坚持忍痛送伤员进洞。", {"health": -20, "mentality": 20}, hidden_risk_log="支前负伤受八路军军医悉心包扎，坚决投身抗日动员。")
            ]
        }
    ]
)

# 5. 1938 台儿庄大捷
add_evt(
    "evt_1938_taierzhuang_dajie", "era", "台儿庄大捷：鲁南血战歼敌万余",
    [1938, 1938], [18, 32], ["华东"],
    {"provinces": ["shandong", "jiangsu"]},
    [], [], 0.88, 4, "确证",
    "1938年春第五战区司令长官李宗仁指挥中国军队在山东台儿庄与日军矶谷、板垣两精锐师团决战。中国军队浴血奋战，歼灭日军万余人，重创侵略者气焰，取得正面战场空前大捷。",
    "台儿庄土城内每一栋砖房、每一个院落都成了血腥争夺的阵地。城内断墙残瓦焦黑一片，敢死队员腰缠手榴弹夜袭敌阵，白刃格斗杀声震天。运河水被血水染红，守军抱定与城共存亡的决心死守不退。",
    [
        {
            "text": "参加台儿庄城防敢死队，腰系四颗大抬枪手榴弹，夜袭破袭敌坦克与碉堡",
            "choiceTags": ["时代：1938", "年龄：18–28", "地域：鲁南前线", "门槛：守军敢死队军人"],
            "outcomes": [
                make_outcome("safe", 50, "成功炸毁敌重机枪地堡引导主力围歼敌寇，荣获宝鼎勋章晋升连长。", {"mentality": 40, "knowledge": 15, "wealth": 20}, status="taierzhuang_daredevil_hero", hidden_risk_log="台儿庄敢死队英雄，正面战场铁血功臣，享誉军界。"),
                make_outcome("injured", 45, "夜袭遭遇手榴弹破片炸伤背部及右小腿多处骨折，后送徐州野战医院保全性命。", {"health": -40, "mentality": 30, "wealth": 15}, status="disabled_veteran_taierzhuang", hidden_risk_log="台儿庄巷战身负重伤致残，战后深藏功名回归乡土。"),
                make_outcome("fatal", 5, "在坚守台儿庄北门最后碉堡阻击敌重炮轰击时壮烈牺牲。", is_fatal=True, hidden_risk_log="在台儿庄城垣保卫战中壮烈牺牲。")
            ]
        },
        {
            "text": "带领苏鲁民众修筑运河阻击工事，用木船连夜运送粮食干粮与抗日前线大刀",
            "choiceTags": ["时代：1938", "年龄：16–55", "地域：京杭大运河畔", "门槛：运河船工/百姓"],
            "outcomes": [
                make_outcome("safe", 80, "冒枪林弹雨穿行运河送达数十万发弹药，受第五战区通令嘉奖并获赠锦旗。", {"wealth": 20, "mentality": 25, "family": 15}, status="canal_logistics_hero", hidden_risk_log="运河水上粮弹抢运功臣，以民间之力筑牢正面战场补给。"),
                make_outcome("injured", 20, "木船遭敌低空机枪扫射右小臂中弹贯通伤，忍痛将弹药箱卸完方才就医。", {"health": -25, "mentality": 20}, hidden_risk_log="运河支前负枪伤，成为当地百姓敬重的抗日义士。")
            ]
        }
    ]
)

# 6. 1938 花园口决堤
add_evt(
    "evt_1938_huayuankou_juedi", "era", "1938年花园口决堤：黄泛区浩劫与以水代兵",
    [1938, 1938], [8, 70], ["华中", "华东"],
    {"provinces": ["henan", "anhui", "jiangsu"]},
    [], [], 0.95, 4, "确证",
    "1938年6月为阻止日军沿陇海路西进，国民政府在郑州花园口炸开黄河大堤‘以水代兵’。黄河改道夺淮入海，造成豫、皖、苏44个县被淹，近九十万人溺死，产生千万流离失所的黄泛区难民。",
    "滔天黄浪奔腾呼啸，水头高达数丈，将村庄麦田瞬间化为一片汪洋。屋顶上、树权上挂满了呼救的难民，漂浮的箱柜、牲畜与尸体在浊浪中翻滚。狂风暴雨中，数百万难民背着仅有的破锅烂席向西逃荒。",
    [
        {
            "text": "若身处豫东黄泛区，在浊浪滔天中拆下门板绑成木筏救出家人，沿陇海铁路路基向西逃荒",
            "choiceTags": ["时代：1938", "年龄：12–65", "地域：河南中东部", "门槛：灾区平民"],
            "outcomes": [
                make_outcome("safe", 45, "历经千难万险逃入伏牛山区避过洪灾，靠开荒种杂粮立足，保全全家老小性命。", {"family": 25, "mentality": 20, "wealth": -35}, status="yellow_river_flood_survivor", hidden_risk_log="在花园口滔天洪水浩劫中带领全家逃出生天，磨炼出极其刚毅的生存本能。"),
                make_outcome("injured", 45, "在污泥浊浪中浸泡数日受重度烂脚溃疡与疟疾高热折磨，沿途讨饭辗转逃至陕西。", {"health": -40, "wealth": -40}, hidden_risk_log="黄泛区逃荒染上恶性疟疾与严重溃疡致残，饱尝亡国流离之痛。"),
                make_outcome("fatal", 5, "夜间突发洪峰破门房屋倒塌不幸被滚滚黄浪卷走溺亡。", is_fatal=True, hidden_risk_log="在花园口黄河泛滥决堤洪水中不幸罹难。"),
                make_outcome("entangled", 5, "逃荒路上与部分子女亲友彻底失散，沿途留下记号期盼他日重逢。", {"family": -40, "mentality": -30}, hidden_risk_log="黄泛逃荒骨肉流散，成为一生难以抚平的时代创伤。")
            ]
        },
        {
            "text": "在未受淹的大后方开封或洛阳参与组建难民收容所，熬大锅菜稀饭接济黄泛难民",
            "choiceTags": ["时代：1938", "年龄：16–60", "地域：后方城镇", "门槛：慈善市民/乡绅"],
            "outcomes": [
                make_outcome("safe", 80, "出资设立粥厂连续三月救活数百名黄泛难民孤儿，受社会各界普遍赞颂敬仰。", {"mentality": 30, "family": 20, "wealth": -20}, status="refugee_camp_founder", hidden_risk_log="倾家荡产救济黄泛难民同胞，赢得崇高道德声望与宗亲爱戴。"),
                make_outcome("injured", 20, "在难民所高强度施粥救治期间不幸感染急性霍乱腹泻脱水，经名中医抢救脱险。", {"health": -30, "wealth": -10}, hidden_risk_log="接济难民染疫九死一生，更笃定积德行善初心。")
            ]
        }
    ]
)

# 7. 1938 武汉会战与保卫大武汉
add_evt(
    "evt_1938_wuhan_huizhan", "era", "武汉会战：“保卫大武汉”与抗战转入相持",
    [1938, 1938], [14, 65], ["华中"],
    {"provinces": ["hubei", "jiangxi", "anhui", "hunan"]},
    [], [], 0.92, 4, "确证",
    "1938年6月至10月中国军队在武汉外围展开规模空前的武汉会战。历时四个半月，毙伤日军十余万人，彻底粉碎日军迅速解决中国事变的战略企图，抗日战争由此正式进入战略相持阶段。",
    "长江两岸炮声震天，田家镇要塞弹雨如倾。汉口沿江大道到处贴着‘保卫大武汉’的红绿标语，青年学生沿街进行抗日救亡募捐宣传。军警在街头维持秩序，最后一批机关与物资从粤汉铁路抢运撤离。",
    [
        {
            "text": "随第九战区部队在万家岭或田家镇江防要塞浴血阻击，利用崇山密林围歼敌寇",
            "choiceTags": ["时代：1938", "年龄：18–30", "地域：赣北/鄂东外围", "门槛：守军将士"],
            "outcomes": [
                make_outcome("safe", 50, "在万家岭大捷中英勇冲杀斩获战功，歼灭敌第一〇六师团主力，荣立二等功提拔少尉。", {"mentality": 40, "knowledge": 15, "wealth": 20}, status="wanjialing_hero", hidden_risk_log="万家岭大捷战斗功臣，在武汉会战血战中立下赫赫威名。"),
                make_outcome("injured", 45, "要塞防守遭遇敌航弹重磅轰炸被泥土掩埋震伤内脏呕血，伤愈调后方后勤部门。", {"health": -35, "mentality": 25, "wealth": 15}, status="injured_fortress_defender", hidden_risk_log="江防要塞血战震伤内脏致慢性咳喘，转入后方战勤保障。"),
                make_outcome("fatal", 5, "在坚守前沿主阵地打退敌数次波浪式冲锋时中弹光荣牺牲。", is_fatal=True, hidden_risk_log="在保卫大武汉要塞保卫战中壮烈牺牲。")
            ]
        },
        {
            "text": "在汉口码头与火车站协助最后一批工业资产与重要档案抢运撤往湘西与四川",
            "choiceTags": ["时代：1938", "年龄：16–55", "地域：湖北武汉", "门槛：后勤运输队员/码头工人"],
            "outcomes": [
                make_outcome("safe", 80, "冒敌机昼夜轰炸把最后一批军火图纸装上火车并安然撤出武汉，获战时交通部嘉奖。", {"knowledge": 25, "wealth": 20, "mentality": 20}, status="wuhan_evacuation_master", hidden_risk_log="成功组织武汉大撤退关键物资入川，为大后方相持奠定物资底气。"),
                make_outcome("injured", 20, "码头扛运重型机床时滑跌扭伤腰椎并被飞溅弹片擦伤左耳，搭乘最后江轮西撤入蜀。", {"health": -25, "wealth": 10}, hidden_risk_log="武汉撤离火线负轻伤，随江轮抵达重庆立足。")
            ]
        }
    ]
)

# 8. 1938 西南联大西迁昆明
add_evt(
    "evt_1938_xinan_lianda", "era", "西南联大西迁昆明：“刚毅坚卓”弦歌不辍",
    [1938, 1940], [16, 35], ["西南"],
    {"provinces": ["yunnan", "guizhou", "sichuan"]},
    [], [], 0.88, 4, "确证",
    "北京大学、清华大学、南开大学南迁后在昆明组建国立西南联合大学。师生在极为简陋的铁皮房与茅草屋里，秉持‘刚毅坚卓’校训，克服轰炸、物价飞涨与饥寒，培养出杨振宁、李政道等一批大师巨匠。",
    "昆明大西门外的土基操场上，简易泥土校舍屋顶盖着铁皮与茅草。雨点打在铁皮顶上声如擂鼓，教授在黑板上平静写下：‘静听雨声’。夜晚桐油灯摇曳，师生裹着破棉袍苦读，弦歌不绝于耳。",
    [
        {
            "text": "若为联大学子或青年学者，在四合院茅草教室里潜心苦读数理文史，在茶馆桐油灯下撰写学术论文",
            "choiceTags": ["时代：1938–1940", "年龄：16–30", "地域：云南昆明", "门槛：热血青年学子/教师"],
            "outcomes": [
                make_outcome("safe", 75, "师从学术泰斗打下渊博学识根底，发表开创性论文，成为新中国现代科学与文化的奠基学者。", {"knowledge": 45, "mentality": 30, "wealth": 10}, new_career_track="cadre_teacher", status="lianda_scholar_elite", hidden_risk_log="西南联大杰出学子，在茅草屋下淬炼出大师风骨，一生为国家科教栋梁。"),
                make_outcome("injured", 22, "日军频繁轰炸昆明跑警报在防空沟摔伤右臂，且因常年清苦生活患重度营养不良肺弱。", {"health": -30, "knowledge": 40}, status="lianda_resilient_student", hidden_risk_log="在西南联大艰难环境下求学体弱伤臂，但铸就百折不挠的坚毅意志。"),
                make_outcome("fatal", 3, "在城北疏散跑防空警报时不幸遭遇敌机重磅航弹直接命中罹难。", is_fatal=True, hidden_risk_log="在昆明遭遇日军无差别空袭不幸罹难。")
            ]
        },
        {
            "text": "在昆明街头开办平价学生饭堂，为联大师生提供实惠的烧饵块、过桥米线与豆浆充饥",
            "choiceTags": ["时代：1938–1940", "年龄：18–55", "地域：云南昆明", "门槛：昆明本地商贩"],
            "outcomes": [
                make_outcome("safe", 85, "饭堂成为联大师生高谈阔论的温暖港湾，与众多教授文人结为莫逆之交，生意红火稳定。", {"wealth": 25, "family": 20, "knowledge": 20}, new_career_track="merchant", status="lianda_beloved_caterer", hidden_risk_log="以平价食肆温暖西南联大师生，积累宽广人脉与良好口碑。"),
                make_outcome("injured", 15, "深夜厨房推车被巡逻军警车辆剐蹭撞翻伤及右小腿，休养月余后继续摆摊。", {"health": -15, "wealth": 15}, hidden_risk_log="在战时昆明摆摊受皮外轻伤，见证春城抗战风云。")
            ]
        }
    ]
)

# 9. 1938 晋察冀根据地创立与敌后游击
add_evt(
    "evt_1938_jinchaji_genjudi", "era", "晋察冀抗日根据地创立与敌后减租减息",
    [1938, 1941], [16, 55], ["华北"],
    {"provinces": ["hebei", "shanxi"]},
    [], [], 0.90, 4, "确证",
    "聂荣臻率部开辟晋察冀抗日根据地，建立模范抗日根据地。推行‘减租减息’、‘合理负担’政策，发动千万农友组织农会、妇救会与民兵自卫队，开展麻雀战、地雷战，使敌后成为陷敌泥潭的汪洋大海。",
    "太行山下的村头大槐树上挂着敲击报警的铁轨道钟。村公所门前张贴着二五减租法令布告。农会干部带领贫苦长工算细账，地主退回了多收的租谷。年轻媳妇坐在门槛上连夜赶做军鞋，山村处处是抗日铁壁。",
    [
        {
            "text": "参加村农会民兵自卫队，跟八路军工作队学习制造土雷、石雷与开挖地道网",
            "choiceTags": ["时代：1938–1941", "年龄：16–45", "地域：晋察冀边区", "门槛：边区青年农民"],
            "outcomes": [
                make_outcome("safe", 70, "在地雷战中巧妙炸毁敌装甲巡逻车，被边区政府授予模范爆炸手称号，晋升区中队副队长。", {"knowledge": 25, "mentality": 30, "wealth": 15}, status="jinchaji_militia_hero", hidden_risk_log="晋察冀模范爆炸英雄，开创地雷战地道战克敌制胜，后成为地方武装骨干。"),
                make_outcome("injured", 25, "手工配制黑火药研磨硫磺意外闪燃灼伤双手与面部，休养两月后继续造雷参战。", {"health": -25, "mentality": 25}, hidden_risk_log="研制石雷土火药负灼伤，练就过硬军工爆破绝活。"),
                make_outcome("fatal", 5, "在村口埋雷阻击敌扫荡掩护乡亲转移进山时中弹英勇牺牲。", is_fatal=True, hidden_risk_log="在掩护根据地乡亲转移反扫荡阻击战中壮烈牺牲。")
            ]
        },
        {
            "text": "积极响应边区减租减息政策，合理退租租地耕种，超额交纳公粮支援前线",
            "choiceTags": ["时代：1938–1941", "年龄：18–60", "地域：边区乡村", "门槛：边区本分农民"],
            "outcomes": [
                make_outcome("safe", 85, "减租后家里第一次有了余粮给孩子做新棉袄，打出高产糜子送大平车支援部队，评为爱国公粮模范户。", {"wealth": 25, "family": 25, "mentality": 20}, status="jinchaji_model_farmer", hidden_risk_log="受益于根据地新政翻身自立，坚定跟党走抗日救国。"),
                make_outcome("entangled", 15, "被顽固旧地主暗中告密给伪军扫荡队抄走部分余粮，经区小队夺回。", {"wealth": -15, "mentality": 10}, hidden_risk_log="经受地主反攻倒算考验，更加坚定了保卫边区信念。")
            ]
        }
    ]
)

# 10. 1939 重庆大轰炸与“愈炸愈强”防空洞
add_evt(
    "evt_1939_chongqing_hongzha", "era", "重庆大轰炸：“愈炸愈强”与防空洞生死劫",
    [1939, 1941], [8, 70], ["西南"],
    {"provinces": ["chongqing", "sichuan"]},
    [], [], 0.95, 4, "确证",
    "1938至1943年侵华日军对陪都重庆实施长达五年的无差别大轰炸，投掷炸弹数万枚，造成数万人死伤，市区大半沦为焦土。英雄的重庆人民在断壁残垣中打出‘愈炸愈强’的巨幅标语，在防空洞里坚持生产生活。",
    "刺耳的防空警报凄厉长鸣，嘉陵江畔红球高高挂起。天空传来敌机低沉的嗡鸣，重磅燃烧弹呼啸而下，解放碑与较场口瞬间化为火海。黑压压的人群涌入潮湿深邃的大隧道防空洞，在浓烟与憋闷中屏住呼吸等待天明。",
    [
        {
            "text": "若身处重庆市区，警报拉响时沉着引导老人幼童有序撤入坚固深岩防空洞避险",
            "choiceTags": ["时代：1939–1941", "年龄：14–65", "地域：重庆陪都", "门槛：重庆市民"],
            "outcomes": [
                make_outcome("safe", 60, "在防空洞深处避过密集轰炸，空袭后立刻参与抬石灭火自救，在废墟上贴上‘愈炸愈强’木牌。", {"mentality": 35, "family": 20, "health": -10}, status="chongqing_resilient_citizen", hidden_risk_log="在重庆大轰炸火海中幸存并挺立，淬炼出顶天立地的不屈性格。"),
                make_outcome("injured", 35, "遭遇较场口大隧道窒息风潮踩踏推搡摔伤右膝骨裂并重度烟熏呛伤，由救护队抬出抢救苏生。", {"health": -40, "mentality": 20}, status="injured_tunnel_survivor", hidden_risk_log="经历重庆大隧道窒息踩踏浩劫死里逃生，晚年患慢性支气管旧疾。"),
                make_outcome("fatal", 5, "在防空洞外不幸遭遇敌机重磅高爆炸弹近距离直接炸塌掩体罹难。", is_fatal=True, hidden_risk_log="在重庆大轰炸中不幸在空袭中罹难。")
            ]
        },
        {
            "text": "加入陪都防空消防抢险队，冒着二次空袭与漫天火海奋力扑救民房与军工原料仓库",
            "choiceTags": ["时代：1939–1941", "年龄：18–45", "地域：重庆火线", "门槛：热血抢险队员"],
            "outcomes": [
                make_outcome("safe", 70, "带领班组成功扑灭二十余处烈火保住长江军火仓库，荣获市防空司令部特等抢险勋章。", {"knowledge": 25, "mentality": 30, "wealth": 15}, status="chongqing_firefighter_hero", hidden_risk_log="重庆大轰炸铁血救火英雄，出生入死守护战时陪都生命线。"),
                make_outcome("injured", 25, "救火时被烧塌的横梁砸伤后背并造成二级局部烫伤，伤愈后继续参加抢修队。", {"health": -30, "mentality": 25}, hidden_risk_log="抢险灭火负烧烫伤留疤，成为战时火线英雄。"),
                make_outcome("fatal", 5, "在扑救军火库危急关头遭遇延时炸弹二次爆炸壮烈殉职。", is_fatal=True, hidden_risk_log="在重庆扑救大火抢救军工物资时壮烈牺牲。")
            ]
        }
    ]
)

# 11. 1939 白求恩逝世与战地救护
add_evt(
    "evt_1939_baiqiuen_shishi", "era", "白求恩大夫逝世与战地救死扶伤精神",
    [1939, 1940], [16, 50], ["华北"],
    {"provinces": ["hebei", "shanxi"]},
    [], [], 0.85, 4, "确证",
    "加拿大共产党员诺尔曼·白求恩大夫率医疗队万里迢迢支援中国抗日。在晋察冀前线冒着炮火做手术，抢救成千上万伤员。1939年11月在抢救伤员时不幸感染败血症逝世。毛主席写下《纪念白求恩》，号召学习其毫不利己专门利人的崇高精神。",
    "黄土高坡上的战地小庙里，白求恩穿着白大褂在烛光下连续做手术几十个小时。外面炮声隆隆，尘土簌簌落下。大夫把自己的鲜血直接输给重伤八路军战士，最后昏迷在简陋的担架上，永远留在了中国的大地。",
    [
        {
            "text": "若为战地护士或青年卫生员，跟随白求恩野战医疗队在火线救死扶伤学习清创缝合",
            "choiceTags": ["时代：1939–1940", "年龄：16–35", "地域：晋察冀野战前线", "门槛：卫生员/热血青年"],
            "outcomes": [
                make_outcome("safe", 80, "继承白求恩精湛医术与纯粹医德，成为边区白求恩卫生学校骨干教员，救活上千抗日伤员。", {"knowledge": 40, "mentality": 35, "wealth": 15}, status="bethune_disciple_medic", hidden_risk_log="白求恩传人，战地救死扶伤医术精湛，一生践行毫不利己专门利人。"),
                make_outcome("injured", 20, "火线抢运截肢伤员被弹片擦伤左小臂感染，经草药消炎抢救脱险保全手臂。", {"health": -20, "knowledge": 30}, hidden_risk_log="战地救护负轻伤，经受血与火的洗礼成长为过硬军医。")
            ]
        },
        {
            "text": "手抄毛主席《纪念白求恩》全文，在村头小学与民兵营里开展全员宣讲悼念活动",
            "choiceTags": ["时代：1939–1940", "年龄：14–60", "地域：抗日根据地", "门槛：文教宣传员/学生"],
            "outcomes": [
                make_outcome("safe", 90, "宣讲深入人心极大激发了根据地军民崇高奉献精神，被评为模范宣传干事。", {"knowledge": 25, "mentality": 30}, status="spiritual_propagandist", hidden_risk_log="传播国际主义与为人民服务精神，成为深受信任的基层政工骨干。"),
                make_outcome("safe", 10, "以白求恩为榜样自学野外急救常识，在村里多次成功抢救难产与跌伤乡亲。", {"knowledge": 25, "family": 25}, hidden_risk_log="学医助人造福全村，成为广受乡里爱戴的仁厚长者。")
            ]
        }
    ]
)

# 12. 1940 百团大战破袭华北交通线
add_evt(
    "evt_1940_baituan_dazhan", "era", "百团大战：华北破袭正太铁路与拔除据点",
    [1940, 1940], [16, 50], ["华北"],
    {"provinces": ["shanxi", "hebei", "henan"]},
    [], [], 0.95, 4, "确证",
    "1940年8月八路军副总司令彭德怀指挥105个团、二十余万人对华北日伪军封锁线发起‘百团大战’。破毁铁路千余里、公路三千里，拔除敌据点近三千个，沉重打击了敌人的‘囚笼政策’，坚定了全国军民抗战必胜信心。",
    "黑夜里正太铁路的铁轨下响起了闷雷般的起爆声。枕木在冲天大火中燃烧，成千上万军民拿着铁锤钢钎撬下铁轨扔下悬崖。娘子关碉堡前枪声激烈，战士们抬着梯子冲向敌楼，硝烟遮蔽了夜空。",
    [
        {
            "text": "随八路军主力夜袭娘子关或破袭狮脑山制高点，顶住敌重炮轰击死守阵地",
            "choiceTags": ["时代：1940", "年龄：18–30", "地域：山西正太路沿线", "门槛：八路军战士"],
            "outcomes": [
                make_outcome("safe", 55, "奋战六天六夜血战狮脑山打退敌多次反扑，荣立大功保送抗日军政大学深造提干。", {"mentality": 40, "knowledge": 20, "wealth": 20}, status="hundred_regiments_hero", hidden_risk_log="百团大战钢铁功臣，浴血华北撕破敌人囚笼，成长为战功卓著的军官。"),
                make_outcome("injured", 40, "在破袭敌碉堡时遭遇毒气瓦斯弹中毒肺部烧灼伴双耳被炮震伤聋，住院休养数月。", {"health": -40, "mentality": 25, "wealth": 15}, status="disabled_veteran_1940", hidden_risk_log="百团大战遭遇敌毒气重伤留后遗症，享受根据地终生抚恤。"),
                make_outcome("fatal", 5, "在攀登娘子关要隘碉堡爆破时被敌重机枪密集封锁壮烈牺牲。", is_fatal=True, hidden_risk_log="在百团大战进攻娘子关战斗中壮烈牺牲。")
            ]
        },
        {
            "text": "带领村农会民兵连夜带大锤与钢钎撬毁铁轨割断敌军用电线，运回钢料自制土炮",
            "choiceTags": ["时代：1940", "年龄：16–55", "地域：铁路沿线各县", "门槛：支前民兵/老乡"],
            "outcomes": [
                make_outcome("safe", 80, "一夜撬毁五里铁路运回数吨优质钢轨改铸成手榴弹，获评华北破袭特等支前模范。", {"wealth": 20, "mentality": 25, "knowledge": 15}, status="railway_breaker_model", hidden_risk_log="全民破袭战支前标兵，以群众智慧摧毁敌交通补给网。"),
                make_outcome("injured", 20, "搬运百斤铁轨时滑倒被重型钢轨砸伤右脚跖骨骨折，村医正骨敷药卧床休养两月。", {"health": -25, "mentality": 20}, hidden_risk_log="破袭铁轨砸伤脚骨留印记，深以参与百团大战为荣。")
            ]
        }
    ]
)

# 13. 1940 滇缅公路与二十四道拐抢运
add_evt(
    "evt_1940_dianmian_gonglu", "era", "滇缅公路与南侨机工血战二十四道拐",
    [1940, 1942], [18, 45], ["西南"],
    {"provinces": ["yunnan", "guizhou"]},
    [], [], 0.88, 4, "确证",
    "中国沿海口岸全部沦陷后，二十万云南各族妇女老幼靠双手在悬崖峭壁上抠出‘抗战生命线’滇缅公路。三千二百余名南洋华侨机工回国参战，冒着敌机轰炸和恶性疟疾，在险峻的怒江天险和二十四道拐日夜抢运国际援华物资。",
    "晴隆二十四道拐如苍龙盘旋在陡峭绝壁上，一侧是万丈深渊。满载航空汽油和弹药的大卡车马达轰鸣，刹车片摩擦出焦糊青烟。雨季道路泥泞打滑，敌机在头顶盘旋俯冲扫射，机工们咬紧牙关把车轮紧贴悬崖飞驰。",
    [
        {
            "text": "若为南洋归国华侨机工或老汽车兵，驾大卡车穿梭在怒江天险与二十四道拐抢运军火",
            "choiceTags": ["时代：1940–1942", "年龄：18–35", "地域：滇缅公路沿线", "门槛：南侨机工/汽车兵"],
            "outcomes": [
                make_outcome("safe", 55, "克服山崩与空袭奇迹般运送数十吨紧缺军火直抵陪都，荣获战时最高荣誉云麾勋章。", {"wealth": 30, "knowledge": 25, "mentality": 35}, status="nanyang_mechanic_hero", hidden_risk_log="南洋华侨机工赤子楷模，以血肉之躯维系抗战国际生命线。"),
                make_outcome("injured", 40, "途中遭遇暴雨滑坡翻车摔落陡坡致多处软组织重伤并感染恶性疟疾高烧，被救回昆明。", {"health": -40, "mentality": 25, "wealth": 15}, status="injured_mechanic_survivor", hidden_risk_log="滇缅公路翻车染疟疾九死一生，谱写海外侨胞报国赤忱。"),
                make_outcome("fatal", 5, "在惠通桥抢运军火时遭遇敌机俯冲轰炸坠入怒江万丈深渊壮烈牺牲。", is_fatal=True, hidden_risk_log="在怒江峡谷抢运抗战战略物资时不幸英勇牺牲。")
            ]
        },
        {
            "text": "在滇西公路沿途开办民间车辆补胎加水站与草药救护站，免费救助机工与运输队员",
            "choiceTags": ["时代：1940–1942", "年龄：16–55", "地域：滇南各县", "门槛：沿途百姓"],
            "outcomes": [
                make_outcome("safe", 85, "用祖传草药方救治数百名过往机工的恶性疟疾与外伤，被誉为天险路上的救命活菩萨。", {"family": 25, "wealth": 20, "mentality": 25}, status="highway_lifesaver", hidden_risk_log="在滇缅公路上舍身筑起民间救护生命站，深受广大机工敬重。"),
                make_outcome("injured", 15, "深夜为军车加水抢修时被过往车辆后视镜刮伤右肩，草药敷贴后继续开张。", {"health": -15, "wealth": 15}, hidden_risk_log="坚守天险驿站救助军车，为抗战生命线默默奉献。")
            ]
        }
    ]
)

# 14. 1941 敌后大生产运动与南泥湾开荒
add_evt(
    "evt_1941_dashengchan_yundong", "era", "延安大生产运动：“自己动手，丰衣足食”",
    [1941, 1943], [16, 50], ["西北"],
    {"provinces": ["shaanxi", "gansu", "ningxia"]},
    [], [], 0.90, 4, "确证",
    "面对日军残酷‘扫荡’和国民党顽固派的严密封锁，陕甘宁边区遭遇空前严重的财政经济困难。毛主席发出‘自己动手，丰衣足食’的号召。三五九旅在王震率领下挺进荒无人烟的南泥湾，一手拿枪一手拿镐，把‘烂泥湾’变成‘陕北好江南’。",
    "南泥湾的荒草漫过人头，荆棘丛生，野兽出没。没有铁镐，战士们就捡来废铁土法打制；没有房屋，大家就挖地窨子、掏窑洞安身。天不亮山梁上就传来嘹亮的开荒号子，荒原上翻出黑油油的肥沃泥土，稻浪在陕北高原翻滚。",
    [
        {
            "text": "随三五九旅挺进南泥湾，一把镢头一把枪，在荆棘沼泽中日夜苦干开荒种水稻",
            "choiceTags": ["时代：1941–1943", "年龄：16–35", "地域：陕北南泥湾", "门槛：八路军战士"],
            "outcomes": [
                make_outcome("safe", 75, "开荒创下一天掘地三亩的劳动纪录，打出数万斤金黄谷物，被边区政府授予一等劳动英雄模范奖章。", {"wealth": 25, "mentality": 30, "knowledge": 15}, status="naniwan_labor_hero", hidden_risk_log="南泥湾大生产特等劳动模范，自己动手丰衣足食，为边区打破封锁立奇功。"),
                make_outcome("injured", 22, "砍伐深山野林荆棘被毒蛇咬伤小腿并患严重风湿性关节炎，经老草药医排毒保命。", {"health": -25, "mentality": 25}, status="resilient_naniwan_pioneer", hidden_risk_log="开辟荒原负毒伤风湿留旧患，铸就吃苦耐劳的南泥湾精神。"),
                make_outcome("fatal", 3, "在深山伐木构筑粮仓遭遇百年大树突发倾倒砸中头部不幸牺牲。", is_fatal=True, hidden_risk_log="在南泥湾开荒伐木重大建设中不幸因公殉职。")
            ]
        },
        {
            "text": "在延安机关学校大院带头摇纺车纺线、织土布并开荒种菜自给自足",
            "choiceTags": ["时代：1941–1943", "年龄：14–55", "地域：陕甘宁边区机关", "门槛：延安青年学子/干部"],
            "outcomes": [
                make_outcome("safe", 85, "练就飞快的纺线绝活，纺出又匀又细的棉纱荣获延安纺线比赛标兵，不仅自己穿暖还支援前线。", {"knowledge": 25, "wealth": 20, "mentality": 25}, status="spinning_competition_winner", hidden_risk_log="自力更生纺纱织布树榜样，深得延安质朴纯洁作风熏陶。"),
                make_outcome("injured", 15, "开荒挖窑洞被崩塌土方压住下半身造成盆骨软组织挫伤，静卧调养一个月。", {"health": -20, "mentality": 20}, hidden_risk_log="挖窑洞开荒负轻伤，磨砺出极强生存与建设才干。")
            ]
        }
    ]
)

# 15. 1941 太平洋战争爆发与租界沦陷
add_evt(
    "evt_1941_taipingyang_zhanzheng", "era", "太平洋战争爆发：上海孤岛沦陷与反法西斯大同盟",
    [1941, 1942], [14, 65], ["华东"],
    {"provinces": ["shanghai", "jiangsu", "zhejiang"]},
    [], [], 0.90, 4, "确证",
    "1941年12月日军偷袭珍珠港，太平洋战争爆发。日军随即强行开进上海公共租界和法租界，历时四年的上海‘孤岛’彻底沦陷。美、英、中等26国签署《联合国家宣言》，反法西斯统一战线正式形成。",
    "南京路上的外国巡捕被日军缴械接管，外滩汇丰银行大楼插上日军膏药旗。租界内的英美侨民被戴上臂章关入集中营，市面上米价一夜暴涨十倍，市民揣着贬值的储备券在铁丝网前受尽日伪盘查。",
    [
        {
            "text": "若身处上海，拒绝在日伪控制的洋行工厂任职，潜入地下抗日出版物印刷发行网络",
            "choiceTags": ["时代：1941–1942", "年龄：18–45", "地域：沦陷上海", "门槛：爱国知识分子/青工"],
            "outcomes": [
                make_outcome("safe", 70, "在阁楼暗室秘密印发数万份抗日救亡传单与大后方战况号外，成为地下情报战线坚强哨兵。", {"knowledge": 30, "wealth": 15, "mentality": 30}, status="shanghai_underground_pressman", hidden_risk_log="孤岛沦陷期隐秘坚守地下抗日宣传，为黑暗中的沪上民众点亮明灯。"),
                make_outcome("injured", 25, "被敌特搜查抄走石印机遭毒打致右耳失聪与断折两根肋骨，经地下党营救保全性命转入乡下。", {"health": -35, "mentality": 30}, status="wounded_underground_fighter", hidden_risk_log="地下抗日坚贞不屈受酷刑致残，展现极高革命气节。"),
                make_outcome("fatal", 5, "在秘密运送电台零件通过日军刺刀关卡时被特工开枪击中不幸牺牲。", is_fatal=True, hidden_risk_log="在上海沦陷区执行抗日秘密联络任务时光荣牺牲。")
            ]
        },
        {
            "text": "依靠缝纫织补或摆弄旧货摊在弄堂深处艰难糊口，暗中掩护被搜捕的同胞藏身阁楼",
            "choiceTags": ["时代：1941–1942", "年龄：16–65", "地域：上海弄堂", "门槛：本分底层市民"],
            "outcomes": [
                make_outcome("safe", 85, "在亭子间成功隐藏掩护两名抗日师生脱险西撤，自己靠一手缝纫好手艺勉强熬过饥馑。", {"family": 25, "wealth": 15, "mentality": 25}, status="alley_righteous_protector", hidden_risk_log="弄堂里以平凡身躯掩护抗日志士，义薄云天。"),
                make_outcome("entangled", 15, "因物价暴涨法币中储券交替贬值，半生积蓄被恶性通胀洗劫一空，家徒四壁。", {"wealth": -35, "mentality": -20}, hidden_risk_log="承受日伪恶性印钞通胀洗劫，在清贫中守住人格尊严。")
            ]
        }
    ]
)

# 16. 1942 河南大旱蝗灾饥荒（“一九四二”）
add_evt(
    "evt_1942_henan_daji_huang", "era", "1942河南大旱蝗灾与千万灾民逃荒血泪",
    [1942, 1943], [6, 75], ["华中"],
    {"provinces": ["henan", "shaanxi", "hubei"]},
    [], [], 0.96, 4, "确证",
    "1942至1943年河南暴发百年未有的大旱灾，夏秋两季颗粒无收，遮天蔽日的蝗灾将树皮草根啃食殆尽。加之战时严酷的征粮征税与各级贪腐瞒报，数百万人死于饥饿和瘟疫，三百余万难民沿陇海线西逃陕西苟全性命。",
    "赤地千里，麦垄焦枯成灰。漫天蝗虫扑打在人脸上，发出沙沙的啃噬声。路旁白骨累累，树皮被刮得露出森森白骨般的木质。人们嚼着观音土肚子胀得像铜锣，难民潮挤在陇海铁路闷罐车顶向西挣扎逃命。",
    [
        {
            "text": "若身处河南灾区，果断变卖仅有破被，携一家老小爬上陇海线难民火车拼死西逃潼关陕西",
            "choiceTags": ["时代：1942–1943", "年龄：12–65", "地域：河南中原腹地", "门槛：逃荒难民家庭"],
            "outcomes": [
                make_outcome("safe", 45, "历经冻饿穿过潼关铁道隧道抵达关中平原，靠给人打农闲短工开荒扎根，保全骨肉生还。", {"family": 30, "wealth": -35, "mentality": 25}, status="henan_1942_miracle_survivor", hidden_risk_log="1942中原大饥荒大逃荒铁血幸存者，带领全家跨越生死关头在西北新生。"),
                make_outcome("injured", 42, "逃荒路上冻馁交加患恶性浮肿并染上斑疹伤寒，沿途吃观音土致严重肠梗阻手术脱险。", {"health": -45, "wealth": -40}, hidden_risk_log="大饥荒中遭受重度浮肿与肠伤残疾，终身对饥荒刻骨铭心。"),
                make_outcome("fatal", 5, "在陇海铁路过涵洞时不幸从车顶跌落或因极度饥馑衰竭在路旁长眠。", is_fatal=True, hidden_risk_log="在1942河南大饥荒逃荒路上不幸罹难。"),
                make_outcome("entangled", 8, "在极度饥荒中不得不将幼女托付给异地善良农户收养以求孩子活命，骨肉离散痛心疾首。", {"family": -45, "mentality": -35}, hidden_risk_log="灾年托孤骨肉离散，晚年耗尽心力寻访失散至亲。")
            ]
        },
        {
            "text": "在陕西西安或宝鸡开办民间难民救济施粥棚，尽微薄之力熬煮高粱米糊糊救济同胞",
            "choiceTags": ["时代：1942–1943", "年龄：16–60", "地域：陕西关中沿线", "门槛：有余粮良善市民"],
            "outcomes": [
                make_outcome("safe", 85, "拿出家中全部窖藏杂粮连续施粥半年，救活数百名饥寒濒死的河南难民同胞，积善流芳。", {"family": 25, "mentality": 30, "wealth": -20}, status="shaanxi_refugee_savior", hidden_risk_log="在民族危难关头倾力施粥救济中原难民，谱写血浓于水同胞大爱。"),
                make_outcome("injured", 15, "在灾民收容所照料病患时不幸感染急性副伤寒，幸得西医盘尼西林注射挽救生命。", {"health": -30, "wealth": -10}, hidden_risk_log="救济难民染疫重病生还，更加笃定救助苍生宏愿。")
            ]
        }
    ]
)

# 17. 1942 中国远征军入缅作战
add_evt(
    "evt_1942_yuanzhengjun_rumian", "era", "中国远征军入缅作战与野人山绝境撤退",
    [1942, 1943], [18, 32], ["西南"],
    {"provinces": ["yunnan", "guizhou", "sichuan"]},
    [], [], 0.88, 4, "确证",
    "1942年中国远征军十万人入缅作战保卫滇缅公路。孙立人率新三十八师在仁安羌以不满千人解救七千被围英军，震惊世界。随后战局逆转，杜聿明率部穿越蛮荒野人山热带雨林撤退，数万人因瘴气、蚂蟥与饥渴葬身异域荒野。",
    "缅北原始密林遮天蔽日，暴雨倾盆。瘴气升腾如毒烟，蚂蟥如雨般从树枝落入衣领。毒蛇出没，山洪暴发。撤退的官兵在没有粮草的泥浆中跋涉，战友倒在泥地里转瞬化为白骨，但幸存者依然高举军旗向前挣扎。",
    [
        {
            "text": "随新三十八师或新二十二师远征将士在缅北热带丛林与敌血战，随后突围翻越野人山",
            "choiceTags": ["时代：1942–1943", "年龄：18–28", "地域：缅北原始丛林", "门槛：热血远征军军人"],
            "outcomes": [
                make_outcome("safe", 48, "以钢铁意志活着走出野人山抵达印度兰姆伽基地，换装美械成为反攻核心主力战将。", {"mentality": 40, "knowledge": 25, "wealth": 25}, status="expeditionary_elite_survivor", hidden_risk_log="中国远征军铁血生还者，穿越野人山死亡绝境，威震印缅反法西斯前线。"),
                make_outcome("injured", 48, "在丛林撤退中感染恶性疟疾伴随右小腿枪伤溃烂见骨，被担架抬入印度野战医院抢救保命。", {"health": -45, "mentality": 25, "wealth": 15}, status="disabled_expeditionary_hero", hidden_risk_log="野人山绝境负重伤染重疾生还，成为抗日远征不屈丰碑。"),
                make_outcome("fatal", 4, "在野人山无名河谷断粮突遇山洪暴发泥石流不幸遇难。", is_fatal=True, hidden_risk_log="在缅北原始森林绝境撤退中不幸为国壮烈牺牲。")
            ]
        },
        {
            "text": "留守云南保山怒江惠通桥东岸，构筑坚固防御工事阻止日军渡江侵入西南大后方",
            "choiceTags": ["时代：1942–1943", "年龄：18–45", "地域：云南怒江沿线", "门槛：滇西守军/工兵将士"],
            "outcomes": [
                make_outcome("safe", 80, "关键时刻果断炸断惠通桥阻敌于怒江天堑西岸，保全昆明与大后方战略安全，立大功升职。", {"mentality": 30, "wealth": 20, "knowledge": 20}, status="huitong_bridge_defender", hidden_risk_log="锁死怒江天堑保卫大西南门户，立下扭转危局战功。"),
                make_outcome("injured", 20, "怒江东岸对峙时遭对岸敌山炮轰击被飞石击裂肩胛骨，缠石膏坚守一线指挥。", {"health": -25, "mentality": 20}, hidden_risk_log="怒江对峙前线负伤，捍卫祖国西南半壁江山。")
            ]
        }
    ]
)

# 18. 1942 延安文艺座谈会
add_evt(
    "evt_1942_wenyi_zuotanhui", "era", "延安文艺座谈会：“文艺为工农兵服务”",
    [1942, 1943], [16, 50], ["西北"],
    {"provinces": ["shaanxi", "gansu"]},
    [], [], 0.85, 4, "确证",
    "1942年5月毛主席在延安主持召开文艺座谈会并发表重要讲话，明确提出文艺要‘为工农兵服务’、首先是‘为工农兵的’。讲话为中国革命文艺指明方向，《白毛女》、《兄妹开荒》、《黄河大合唱》等名篇巨作由此诞生。",
    "杨家岭中央大礼堂前的枣树林里，阳光斑驳。来自全国大城市的青年作家、剧作家穿着打补丁的粗灰布棉衣与老乡盘腿坐在一起。窑洞里拉响激昂的二胡和腰鼓，秧歌剧唱出了庄稼汉的心里话，延安文艺气象一新。",
    [
        {
            "text": "响应号召背起行囊走向陕北农村深入群众，拜老农为师，创作反映减租抗日的新秧歌剧",
            "choiceTags": ["时代：1942–1943", "年龄：18–40", "地域：陕北乡村", "门槛：文艺青年/知识分子"],
            "outcomes": [
                make_outcome("safe", 85, "创作出脍炙人口的抗日新歌舞剧受到根据地军民热烈追捧，成为享誉全国的新人民文艺名家。", {"knowledge": 35, "mentality": 30, "wealth": 15}, status="revolutionary_artist_master", hidden_risk_log="深入生活扎根工农兵，成为中国现代新现实主义革命文艺中流砥柱。"),
                make_outcome("safe", 15, "在农村采风期间自编自演活报剧向老乡普及卫生防病知识，获边区卫生模范表彰。", {"knowledge": 25, "family": 25}, hidden_risk_log="以通俗文艺启蒙乡土公卫知识，深受基层百姓喜爱。")
            ]
        },
        {
            "text": "若为陕北民间老艺人，将传统的安塞腰鼓与陕北民歌说书融入抗战新内容宣讲支前",
            "choiceTags": ["时代：1942–1943", "年龄：16–60", "地域：陕北老区", "门槛：民间艺人/老农"],
            "outcomes": [
                make_outcome("safe", 90, "腰鼓震天响响彻黄土高坡，带领锣鼓队在延安军民大游行中夺得头彩，被评为民间艺术功臣。", {"mentality": 30, "family": 20, "wealth": 15}, status="folk_art_champion", hidden_risk_log="将传统民间艺术赋予时代新生，成为边区极具号召力的民间文化领袖。"),
                make_outcome("injured", 10, "连续多天激昂擂鼓打腰鼓双手虎口震裂磨破化脓，包扎后继续走村串户演出。", {"health": -15, "mentality": 25}, hidden_risk_log="倾情鼓乐演出版伤双手，体现质朴陕北人民报国情操。")
            ]
        }
    ]
)

# 19. 1942 国统区兵役“抓壮丁”浩劫
add_evt(
    "evt_1942_zhuazhuangding_bingyi", "era", "国民党统辖区严苛兵役与“抓壮丁”陋规",
    [1942, 1944], [16, 45], ["西南", "华南", "华中"],
    {"provinces": ["sichuan", "guizhou", "guangxi", "hunan", "yunnan"]},
    [], [], 0.90, 4, "确证",
    "抗战相持阶段国民党统辖区兵役制度腐败透顶，地方保甲长趁机横征暴敛，沿街拉夫‘抓壮丁’。穷苦农家子弟被麻绳串连押送，在壮丁营饱受克扣虐待、疾病缠身，兵役成为千万平民挥之不去的梦魇。",
    "泥泞的乡间小道上，乡公所团丁端着长枪突然包围集市。青年农民被反绑双手，粗麻绳将十几个人如牲口般串在一起。年迈的母亲扑在泥地里痛哭撕扯，却换来团丁粗暴的枪托毒打。壮丁营里臭气熏天，疫病流行。",
    [
        {
            "text": "在集市险遭团丁围堵时眼疾手快翻墙逃入深山密林隐匿，投奔深山猎户避开被拉夫",
            "choiceTags": ["时代：1942–1944", "年龄：16–35", "地域：西南后方乡村", "门槛：乡村青壮年"],
            "outcomes": [
                make_outcome("safe", 65, "在深山老林靠打猎采药避开兵役抓捕风头，学得一身野外生存本领，保全身家平安。", {"health": 15, "knowledge": 20, "wealth": -10}, status="draft_evasion_survivor", hidden_risk_log="凭借过人警惕避开腐朽抓壮丁浩劫，在山林自食其力守住生命。"),
                make_outcome("injured", 25, "翻墙逃跑被团丁放枪擦伤左小腿软组织，带伤藏身野山溶洞受寒患慢性咳嗽。", {"health": -25, "mentality": 15}, hidden_risk_log="逃避拉夫负轻伤受风寒，深刻认清旧政权腐朽本质。"),
                make_outcome("entangled", 10, "家中老父因未能交出壮丁被保甲长抓去顶罪拘押一月，花光积蓄托保赎出。", {"wealth": -35, "family": -20}, hidden_risk_log="兵役连累至亲破财赎人，对旧官僚劣绅深恶痛绝。")
            ]
        },
        {
            "text": "不幸被抓入壮丁营，在押运途中暗中组织同营穷苦壮丁团结自救抗击克扣军粮",
            "choiceTags": ["时代：1942–1944", "年龄：18–35", "地域：国统区壮丁营", "门槛：被抓壮丁青年"],
            "outcomes": [
                make_outcome("safe", 55, "带领大家据理力争制止军需官克扣伙食，并在整训中因表现刚勇被正规军长官看重转为文书。", {"mentality": 30, "knowledge": 15, "wealth": 10}, status="enlisted_brave_leader", hidden_risk_log="身陷壮丁营逆境自强维护同袍，展现极高领导力转危为安。"),
                make_outcome("injured", 40, "在长途押送中因营养极度不良患重度痢疾险些丧命，幸遇好心卫生兵给服黄连素捡回一条命。", {"health": -35, "wealth": -15}, hidden_risk_log="壮丁营痢疾折磨九死一生，饱尝人间炼狱辛酸。"),
                make_outcome("fatal", 5, "在暴雨泥泞山路押运中突发霍乱高烧脱水未能得到医治不幸死于途中。", is_fatal=True, hidden_risk_log="在国统区长途押解壮丁途中因霍乱疫病不幸罹难。")
            ]
        }
    ]
)

# 20. 1943 废除不平等条约与开罗宣言
add_evt(
    "evt_1943_feichu_tiaoyue", "era", "废除不平等条约与《开罗宣言》收复失地",
    [1943, 1943], [14, 75], ["ALL"], {},
    [], [], 0.90, 4, "确证",
    "1943年1月中美、中英分别签署新约，废除在华治外法权及租界特权，结束了百年来不平等条约的枷锁。同年底中、美、英三国发表《开罗宣言》，明确规定日本侵占的台湾、澎湖列岛及东北四省必须归还中国，中国大国地位获得确立。",
    "报童挥舞着号外满街狂奔：‘百年国耻今日雪，不平等条约废除啦！’大后方的茶馆礼堂里，士子老农交口称颂。街头学生打着横幅游行，一百年间鸦片战争以来的屈辱阴霾在抗战铁血奋战中被一扫而空。",
    [
        {
            "text": "与工友街坊走上街头参与盛大火炬游行，庆祝废除不平等条约与开罗会议大胜利",
            "choiceTags": ["时代：1943", "年龄：14–75", "地域：全国大后方", "门槛：广大爱国民众"],
            "outcomes": [
                make_outcome("safe", 90, "民族自尊心与自豪感空前高涨，坚定了抗战必胜信念，精神面貌焕然一新。", {"mentality": 35, "knowledge": 15}, status="unequal_treaties_abolition_witness", hidden_risk_log="亲历废除百年不平等条约高光时刻，形成崇高民族自豪与自信。"),
                make_outcome("safe", 10, "在夜校为贫民义务讲授中国近代抗争历史与国际法常识，启蒙民众爱国情怀。", {"knowledge": 25, "mentality": 25}, hidden_risk_log="以近代史宣讲普及国民常识，成为知书达理的文化栋梁。")
            ]
        },
        {
            "text": "若在外事、海关或法学界，着手研究接收租界主权与重建自主海关商贸法律规章",
            "choiceTags": ["时代：1943", "年龄：22–60", "地域：大后方司法经贸系统", "门槛：法律/外贸专业人员"],
            "outcomes": [
                make_outcome("safe", 85, "参与起草中国首批收回租界与治外法权后的海关涉外法规，成为国家级国际法学法权栋梁。", {"knowledge": 40, "wealth": 25, "mentality": 25}, status="international_law_scholar", hidden_risk_log="执笔废除不平等条约后续法制重建，确立崇高国际法权威地位。"),
                make_outcome("entangled", 15, "涉外谈判交涉过度劳累突发神经性耳鸣与眼疲劳，休整后继续投身收回利权工作。", {"health": -15, "knowledge": 30}, hidden_risk_log="为收回国家主权夜以继日耗尽心血，展现深厚法学报国担当。")
            ]
        }
    ]
)

print(f"Era 1937-1949 Part 1 loaded! Current events: {len(events)}")
