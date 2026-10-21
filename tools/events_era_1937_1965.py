# tools/events_era_1937_1965.py
from tools.build_all_exposure_events import add_event, make_outcome

def register_events_1937_1965():
    # 1. 南京沦陷、日军轰炸与扫荡
    add_event(
        evt_id="evt_1937_nanjing_kongxi",
        tier="era",
        title="战乱烽火与后方空袭避险",
        year_range=[1937, 1941],
        target_age=[10, 65],
        regions=["华东", "华中", "西南"],
        exposure={"urbanRural": "urban", "provinces": ["shanghai", "jiangsu", "hubei", "chongqing", "sichuan"]},
        pre_tags=[],
        trigger_prob=0.85,
        fact_level="确证",
        historical_fact="1937年全面抗战爆发后沿海主要城市相继沦陷，日军对重庆、成都等大后方展开长期无差别大轰炸，千万百姓流离失所。",
        narrative="尖锐的防空警报在头顶呼啸长鸣，黑烟遮蔽了日光，四处是碎砖断瓦与逃难人潮。面对漫天火海与炸弹呼啸，你必须在数秒内做出抉择。",
        choices=[
            {
                "text": "随难民与西迁公学车船向大后方撤退避乱",
                "choiceTags": ["时代：1937–1941", "年龄：10–65", "地域：沿海/大后方", "门槛：平民"],
                "outcomes": [
                    make_outcome("safe", 55, "历经颠簸跋涉数千里抵达川蜀大后方，安顿立足。", {"wealth": -15, "mentality": 10}, hidden_risk_log="避开战乱浩劫，虽折损家财但在大后方保全性命。"),
                    make_outcome("injured", 25, "逃难路上遭遇空袭气浪掀翻摔伤右臂，留下伤疤。", {"health": -20, "wealth": -10}, hidden_risk_log="战乱流离中负伤留疤，成为一生的沧桑烙印。"),
                    make_outcome("entangled", 13, "途中行李盘缠尽数遗失，与部分至亲失散。", {"family": -25, "wealth": -20}, hidden_risk_log="战乱导致亲族离散，耗费数年多方打听下落。"),
                    make_outcome("redirected", 6, "流亡途中投笔从戎，加入后方军工修配大队。", {"knowledge": 15, "mentality": 20}, new_career_track="worker", hidden_risk_log="因战乱西迁而结缘军工修配，彻底走上工匠之路。"),
                    make_outcome("fatal", 1, "在渡口遭遇突发弹雨不幸罹难牺牲。", is_fatal=True, hidden_risk_log="在逃难渡口遭遇突发空袭不幸罹难。")
                ]
            },
            {
                "text": "留守故土看守老宅，躲入自建土防空洞避险",
                "choiceTags": ["时代：1937–1941", "年龄：16–65", "地域：原籍城市", "门槛：有私宅"],
                "outcomes": [
                    make_outcome("safe", 50, "靠地窖藏匿少许杂粮，在残垣断壁间保全家小平安。", {"wealth": 10, "health": -10}, hidden_risk_log="坚守故土保全祖宅基业，在艰辛中熬过战乱岁月。"),
                    make_outcome("injured", 28, "防空洞被震塌落土砸伤背脊，常年阴雨隐痛。", {"health": -25, "mentality": -10}, hidden_risk_log="防空洞坍塌伤及腰脊，晚年落下严重慢性风湿。"),
                    make_outcome("entangled", 15, "房屋被烧毁半间，被伪政权苛捐杂税盘剥殆尽。", {"wealth": -35, "mentality": -15}, hidden_risk_log="留守故土遭遇重税搜刮，家底几乎归零。"),
                    make_outcome("redirected", 6, "暗中为地下抗日交通站传递药品，成为地下工作者。", {"knowledge": 15, "mentality": 25}, new_career_track="cadre_teacher", hidden_risk_log="因留守而接触地下抗日联络，走上革命与公职道路。"),
                    make_outcome("fatal", 1, "旧宅不幸遭重磅航弹直接命中罹难。", is_fatal=True, hidden_risk_log="老宅遭遇直接命中不幸在轰炸中罹难。")
                ]
            }
        ]
    )

    # 2. 1938 花园口决堤
    add_event(
        evt_id="evt_1938_huayuankou",
        tier="era",
        title="1938花园口决堤与黄泛浩劫",
        year_range=[1938, 1939],
        target_age=[0, 75],
        regions=["华中", "华东"],
        exposure={"urbanRural": "rural", "provinces": ["henan", "anhui", "jiangsu"]},
        pre_tags=[],
        trigger_prob=0.80,
        fact_level="确证",
        historical_fact="1938年6月国民政府为阻止日军西进掘开郑州花园口黄河大堤，滔滔黄水淹没豫、皖、苏三省44县，形成大片黄泛区，数百万人流离失所。",
        narrative="黄浪滔天，浑浊泥水一夜间吞没了万亩良田与泥墙村舍。鸡犬漂零，哭声震野，全家人仅剩头顶的高粱秸秆柴堆与一艘借来的破木划子。",
        choices=[
            {
                "text": "用木盆托着幼童，全家沿陇海线向西逃荒避难",
                "choiceTags": ["时代：1938", "年龄：0–75", "地域：黄泛区", "门槛：农户"],
                "outcomes": [
                    make_outcome("safe", 45, "一路乞讨跋涉到达豫西深山，开荒搭窝棚落脚幸存。", {"wealth": -20, "mentality": 10}, hidden_risk_log="在黄泛浩劫中果断西逃，虽吃尽苦头但全家得以保全。"),
                    make_outcome("injured", 30, "在泥浆中跋涉染上严重痢疾与浮肿，九死一生脱险。", {"health": -30, "wealth": -15}, hidden_risk_log="黄泛逃荒途中患上恶性肠疾，身体元气大伤。"),
                    make_outcome("entangled", 16, "在拥挤流民队伍中与亲人走散，沦落异乡寄人篱下。", {"family": -30, "mentality": -20}, hidden_risk_log="大水导致至亲失散，在异乡孤独求生多年。"),
                    make_outcome("redirected", 7, "逃至西安被纱厂收留当学徒工，脱离农门进城做工。", {"wealth": 15, "knowledge": 10}, new_career_track="worker", hidden_risk_log="因大水逃荒机缘巧合进入近代纱厂，由农户转为纺织技工。"),
                    make_outcome("fatal", 2, "大水突袭被激流卷走不幸溺亡。", is_fatal=True, hidden_risk_log="在黄泛洪峰突袭中不幸被卷入激流。")
                ]
            },
            {
                "text": "爬上村头大土台高岗，抱紧百年古树等待水退",
                "choiceTags": ["时代：1938", "年龄：6–75", "地域：黄泛区", "门槛：村落高地"],
                "outcomes": [
                    make_outcome("safe", 40, "水退后在满地淤泥中抢种早熟荞麦，勉强度过荒年。", {"wealth": -10, "health": -15}, hidden_risk_log="守在高台熬过大水，在黄泛沉积盐碱地上重新扎根。"),
                    make_outcome("injured", 32, "高台缺水缺粮饥寒交迫，数日暴晒落下皮肤烂疮。", {"health": -25, "mentality": -15}, hidden_risk_log="水困高台多日饥渴，落下陈旧皮肤与胃肠疾患。"),
                    make_outcome("entangled", 18, "家中小牛与仅有农具全被冲光，生计陷入极度贫困。", {"wealth": -35, "family": -15}, hidden_risk_log="生产资料荡然无存，战后沦为村中极度贫困户。"),
                    make_outcome("redirected", 8, "参与黄河堵口修堤水利工程，掌握全套打桩石工手艺。", {"knowledge": 20, "wealth": 10}, new_career_track="worker", hidden_risk_log="参与治黄抢险掌握石工打桩手艺，日后成为水利建筑工。"),
                    make_outcome("fatal", 2, "高台受激流掏空坍塌不幸落水遇难。", is_fatal=True, hidden_risk_log="避难高台被泥水掏空坍塌不幸溺亡。")
                ]
            }
        ]
    )

    # 3. 1942–43 河南大饥荒
    add_event(
        evt_id="evt_1942_zhongyuan_jihuang",
        tier="era",
        title="1942中原旱蝗大饥荒生死迁徙",
        year_range=[1942, 1943],
        target_age=[0, 75],
        regions=["华中", "华北"],
        exposure={"urbanRural": "rural", "provinces": ["henan", "hebei", "shandong", "shanxi"]},
        pre_tags=[],
        trigger_prob=0.85,
        fact_level="确证",
        historical_fact="1942年至1943年河南发生大旱灾与蝗灾交织，叠加战乱苛捐杂税，导致严重大饥荒，据学术界考证有数百万人受灾与大迁徙。",
        narrative="漫天飞蝗蔽日，枯黄的麦苗被啃食殆尽。树皮与观音土已成为争抢之物，米缸见底，集市上用几斗麦子甚至换不回半块粗布，死神在干瘪的田埂上徘徊。",
        choices=[
            {
                "text": "收拾仅有破棉絮，扒上开往洛阳关中的闷罐货车逃难",
                "choiceTags": ["时代：1942", "年龄：0–75", "地域：中原腹地", "门槛：饥荒农户"],
                "outcomes": [
                    make_outcome("safe", 45, "历尽千辛万苦抵达八府庄陕西落脚，靠打短工活命。", {"wealth": -15, "mentality": 10}, hidden_risk_log="在1942大饥荒中扒车西逃保全骨肉，扎根西北。"),
                    make_outcome("injured", 28, "路上吞食观音土腹胀如鼓，险些肠梗阻丧命。", {"health": -30, "wealth": -10}, hidden_risk_log="饥荒吞食观音土伤及肠胃，晚年常年消化不良。"),
                    make_outcome("entangled", 18, "万般无奈将幼小弟妹托付给好心老乡收养以保其活命。", {"family": -35, "mentality": -25}, hidden_risk_log="大荒之年无奈送养骨肉，成为长达数十年的心底剧痛。"),
                    make_outcome("redirected", 7, "逃至宝鸡被秦岭铁路工程局招为筑路杂工，脱离农籍。", {"knowledge": 15, "wealth": 15}, new_career_track="worker", hidden_risk_log="因大旱西逃进入筑路工区，转为铁路产业工人。"),
                    make_outcome("fatal", 2, "在漫长的逃荒古道上极度虚脱倒下闭眼。", is_fatal=True, hidden_risk_log="在1942大荒年漫漫流亡路上饥寒交迫倒下。")
                ]
            },
            {
                "text": "留守村落掘地三尺挖草根，靠地窖藏匿的半升豆子死守",
                "choiceTags": ["时代：1942", "年龄：6–75", "地域：中原腹地", "门槛：留守农户"],
                "outcomes": [
                    make_outcome("safe", 40, "靠吃榆树皮磨面熬到次年夏粮救济，全家骨瘦如柴幸存。", {"wealth": -20, "health": -20}, hidden_risk_log="坚守故土挖草根死里逃生，见证了人间最深沉的苦难。"),
                    make_outcome("injured", 32, "极度消瘦导致身体骨骼发育受阻，落下慢性肺病。", {"health": -35, "mentality": -15}, hidden_risk_log="严重营养不良落下终身虚弱与肺部宿疾。"),
                    make_outcome("entangled", 19, "为保全家小忍痛变卖祖传地契与所有铁制农具。", {"wealth": -40, "family": -10}, hidden_risk_log="典当全部田产农具换救命粮，解放前沦为赤贫。"),
                    make_outcome("redirected", 7, "被回乡探亲的公学先生收为学徒，走上半工半读之路。", {"knowledge": 25, "mentality": 15}, new_career_track="cadre_teacher", hidden_risk_log="在大荒中得遇恩师收留求学，改写了一生命运轨迹。"),
                    make_outcome("fatal", 2, "因饥饿导致器官衰竭未能熬过大荒之春。", is_fatal=True, hidden_risk_log="在漫漫大荒中未能熬过开春的青黄不接。")
                ]
            }
        ]
    )

    # 4. 国立高校公学西迁流亡
    add_event(
        evt_id="evt_1938_xinanlianda",
        tier="era",
        title="战时高校公学西迁流亡（联大精神）",
        year_range=[1938, 1941],
        target_age=[15, 26],
        regions=["ALL"],
        exposure={"jobTracks": ["cadre_teacher", "tech_whitecollar"], "urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.75,
        fact_level="确证",
        historical_fact="抗战期间北京大学、清华大学、南开大学等高校南迁昆明组建西南联合大学，大批中等院校亦辗转西迁，弦歌不辍，培养了大批民族栋梁。",
        narrative="学校奉命拆解仪器图书打包西迁。黑板前先生含泪写下‘读书不忘救国’。前路是千里步行跋涉，土匪流寇与疟疾蚊虫横行，你背着书箱站在了人生的分岔口。",
        choices=[
            {
                "text": "加入青年步行团，风餐露宿徒步千余里西迁求学",
                "choiceTags": ["时代：1938", "年龄：15–26", "门槛：在校学生/知识青年"],
                "outcomes": [
                    make_outcome("safe", 60, "在简陋铁皮茅草顶校舍刻苦求学，打下深厚学问底子。", {"knowledge": 35, "mentality": 25}, hidden_risk_log="历经徒步长征洗礼，成为战时公学培育的学术中坚。"),
                    make_outcome("injured", 20, "途中染上重度恶性疟疾（打摆子），身体极度虚弱。", {"health": -25, "knowledge": 20}, hidden_risk_log="跋涉途中染上疟疾，寒热交替险些丧命。"),
                    make_outcome("entangled", 12, "因家信中断断绝经济来源，不得不半工半读抄写度日。", {"wealth": -20, "knowledge": 20}, hidden_risk_log="失去家庭资助，靠图书馆刻蜡版打零工勉强维系学业。"),
                    make_outcome("redirected", 7, "结识进步青年团体，投身抗日后方宣传与报馆编辑。", {"knowledge": 25, "mentality": 20}, new_career_track="cadre_teacher", hidden_risk_log="在联大思想激荡中转向新闻文化与宣传教育事业。"),
                    make_outcome("fatal", 1, "途中不幸失足坠崖落入湍急江水罹难。", is_fatal=True, hidden_risk_log="西迁徒步翻越险峻峡谷时不幸失足罹难。")
                ]
            },
            {
                "text": "投笔从戎报考战时青年远征军与后方通讯机要学校",
                "choiceTags": ["时代：1938", "年龄：17–26", "门槛：青年学生"],
                "outcomes": [
                    make_outcome("safe", 55, "精通无线电发报与测绘技能，成为骨干通讯技术员。", {"knowledge": 30, "wealth": 15}, hidden_risk_log="战时精研无线电机要，日后成为邮电通信系统技术先驱。"),
                    make_outcome("injured", 24, "后方机房遭遇偷袭负弹片伤，立功受奖转入文职。", {"health": -20, "mentality": 20}, hidden_risk_log="坚守发报机房负伤，战后转入地方邮电局。"),
                    make_outcome("entangled", 14, "部队整编过程中蒙受审查，脱离军界返乡任教。", {"mentality": -15, "knowledge": 15}, new_career_track="cadre_teacher", hidden_risk_log="战后档案审查复杂，离开军界转任地方中学教师。"),
                    make_outcome("redirected", 6, "因技术过硬受聘大型后方机械修配总厂担任工程师。", {"knowledge": 25, "wealth": 20}, new_career_track="worker", hidden_risk_log="由军用发报转向工业机械，转型为现代工程技工。"),
                    make_outcome("fatal", 1, "在前线运送电台物资途中遭遇伏击牺牲。", is_fatal=True, hidden_risk_log="前线运输途中遭敌伏击不幸壮烈牺牲。")
                ]
            }
        ]
    )

    # 5. 抓壮丁与战乱兵役
    add_event(
        evt_id="evt_1946_zhuazhuangding",
        tier="era",
        title="战乱兵役拉夫与抓壮丁风暴",
        year_range=[1946, 1948],
        target_age=[17, 35],
        regions=["ALL"],
        exposure={"urbanRural": "all", "jobTracks": ["farmer", "worker"]},
        pre_tags=[],
        trigger_prob=0.65,
        fact_level="确证",
        historical_fact="解放战争后期国民党统治区兵源枯竭，保甲长勾结军警大肆抓捕青壮年充当壮丁，绑缚押解前线，底层百姓苦不堪言。",
        narrative="夜半狗叫连声，保长带着武装军警破门而入，手电筒直照床头。街坊四处传来抓捕青壮年的呼喊与哭啼，绳索与枪托已逼在眼前。",
        choices=[
            {
                "text": "四处借钱托保，凑足粮款买替身免除壮丁差役",
                "choiceTags": ["时代：1946–1948", "年龄：17–35", "门槛：借贷能力"],
                "outcomes": [
                    make_outcome("safe", 55, "虽欠下一屁股债，但终于保全自身留在老小身边。", {"wealth": -30, "family": 15}, hidden_risk_log="借贷买免役保全人身自由，虽负重债但避开了内战火线。"),
                    make_outcome("injured", 25, "逃避纠缠中被枪托砸断左肋骨，在家中暗藏休养半月。", {"health": -20, "wealth": -15}, hidden_risk_log="反抗抓捕被打伤肋骨，留下陈旧内伤。"),
                    make_outcome("entangled", 14, "钱被保长吞没依然被绑走，押至半路伺机脱逃。", {"wealth": -25, "mentality": -20}, hidden_risk_log="被骗走巨款依然遭掳走，历尽艰险逃回乡里。"),
                    make_outcome("redirected", 6, "被迫远走高飞逃入解放区参加生产支前队翻身。", {"mentality": 25, "knowledge": 10}, new_career_track="worker", hidden_risk_log="为避抓丁逃入解放区，彻底翻身成为建设骨干。"),
                    make_outcome("fatal", 0, "押解途中被枪击（概率极微，归为逃生分支）", hidden_risk_log="押解途中险遭枪击，九死一生。")
                ]
            },
            {
                "text": "连夜翻越山岭潜入深山炭窑打短工避风头",
                "choiceTags": ["时代：1946–1948", "年龄：17–35", "门槛：体力较好"],
                "outcomes": [
                    make_outcome("safe", 60, "在深山烧炭两年风餐露宿，安然躲过抓丁大网迎解放。", {"wealth": 10, "health": -10}, hidden_risk_log="深山避乱烧炭安然迎解放，积累了坚毅吃苦筋骨。"),
                    make_outcome("injured", 24, "炭窑坍塌砸伤右腿，在草棚敷草药留下轻微瘸拐。", {"health": -25, "mentality": -10}, hidden_risk_log="深山烧炭遇窑塌伤腿，留下轻度瘸腿残疾。"),
                    make_outcome("entangled", 11, "家中老父因交不出丁粮被保甲关押受辱罚款。", {"family": -25, "wealth": -20}, hidden_risk_log="躲入深山导致家眷受保甲株连关押催罚。"),
                    make_outcome("redirected", 5, "与山中采药人结识，学会辨认数百种中草药改行行医。", {"knowledge": 25, "mentality": 20}, new_career_track="cadre_teacher", hidden_risk_log="避居深山潜心学医，日后成为乡间受人敬重的郎中。")
                ]
            }
        ]
    )

    # 6. 土改与阶级成分划定
    add_event(
        evt_id="evt_1950_tudigaige",
        tier="era",
        title="《土地改革法》与家庭阶级成分划定",
        year_range=[1950, 1952],
        target_age=[18, 65],
        regions=["ALL"],
        exposure={"urbanRural": "rural"},
        pre_tags=[],
        trigger_prob=0.90,
        fact_level="确证",
        historical_fact="1950年中央人民政府颁布《中华人民共和国土地改革法》，在全国广大新解放区开展轰轰烈烈的土地改革，彻底废除封建地主土地所有制，划分阶级成分。",
        narrative="工作队进村扎根串连，开大会评议每家每户的田亩、雇工与放贷历史。木桩界石钉满田埂，红榜公布了各户成分，这几个字将深刻影响全家两代人的命运。",
        choices=[
            {
                "text": "主动配合工作队清丈田亩，如实坦陈家境并积极参加农会",
                "choiceTags": ["时代：1950", "年龄：18–65", "地域：农村新解放区", "门槛：农户"],
                "outcomes": [
                    make_outcome("safe", 65, "定为贫农/下中农成分，分得朝阳良田三亩与耕牛一头。", {"wealth": 25, "mentality": 25, "family": 15}, status="poor_peasant_class", hidden_risk_log="顺利定为贫下中农红五类成分，分得翻身水田与耕牛。"),
                    make_outcome("entangled", 22, "因祖上曾出租半亩薄田被争论评定为富裕中农，工分受限。", {"wealth": 10, "mentality": -10}, status="middle_peasant_class", hidden_risk_log="被评为富裕中农，在后续集体化招工中有微弱限制。"),
                    make_outcome("injured", 8, "在丈量荒山纠纷中被邻里推搡扭伤脚踝。", {"health": -10, "wealth": 15}, hidden_risk_log="量田争执伤及脚踝，虽分得土地但与邻里略有积怨。"),
                    make_outcome("redirected", 5, "因为人公道被推选为大队治安民兵队长，走上基层干部道路。", {"knowledge": 15, "mentality": 20}, new_career_track="cadre_teacher", status="village_cadre", hidden_risk_log="在土改积极表现获评模范，走上农村基层干部轨道。")
                ]
            },
            {
                "text": "低调守成少说话，由家族德高望重的老长辈出面应对评议",
                "choiceTags": ["时代：1950", "年龄：18–65", "地域：农村新解放区", "门槛：家族户"],
                "outcomes": [
                    make_outcome("safe", 60, "稳妥定为普通中农，保全自耕田产安稳过日子。", {"wealth": 15, "mentality": 10}, status="middle_peasant_class", hidden_risk_log="本分低调定为普通中农，平稳融入新政权农业生产。"),
                    make_outcome("entangled", 25, "因长辈言辞不慎被疑隐瞒私产，多摊派支前公粮。", {"wealth": -15, "mentality": -15}, hidden_risk_log="应对失误被扣帽子多缴统购统销粮，家境略显紧巴。"),
                    make_outcome("redirected", 15, "见农村重组格局已定，托城里亲戚进城报考机床厂学徒。", {"wealth": 20, "knowledge": 15}, new_career_track="worker", hidden_risk_log="敏锐察觉时代变迁，借机进城招工成为国营工人。")
                ]
            }
        ]
    )

    # 7. 抗美援朝
    add_event(
        evt_id="evt_1951_kangmei",
        tier="era",
        title="抗美援朝动员与保家卫国参军",
        year_range=[1950, 1953],
        target_age=[18, 28],
        regions=["ALL"],
        exposure={"jobTracks": ["worker", "farmer"]},
        pre_tags=[],
        trigger_prob=0.60,
        fact_level="确证",
        historical_fact="1950年10月中国人民志愿军跨过鸭绿江抗美援朝。国内掀起参军参战、捐献飞机大炮的热潮，大批优秀热血儿女奔赴三八线浴血奋战。",
        narrative="‘雄赳赳，气昂昂，跨过鸭绿江’的歌声响彻街巷广场。居委会与村公所前挤满了咬破手指写请战书的同龄青年，大红花与行军背包就在眼前。",
        choices=[
            {
                "text": "咬破指头递交血书，毅然报名参加志愿军奔赴朝鲜前线",
                "choiceTags": ["时代：1950–1953", "年龄：18–28", "门槛：体检合格青年"],
                "outcomes": [
                    make_outcome("safe", 50, "在上甘岭坑道战中立三等功，停战后保送军校转业地方公职。", {"mentality": 35, "wealth": 20, "knowledge": 15}, new_career_track="cadre_teacher", status="hero_veteran", hidden_risk_log="浴血奋战立功受奖光荣转业，享有一生崇高的军属荣誉。"),
                    make_outcome("injured", 26, "战场排雷腿部负重伤致残二等乙级，荣休返乡定额抚恤。", {"health": -35, "mentality": 25, "wealth": 15}, status="injured_veteran", hidden_risk_log="战场负伤致残退伍，每月享有国家优抚粮款保障。"),
                    make_outcome("entangled", 15, "战火严寒导致双足冻伤严重脱甲，终身不能剧烈跑跳。", {"health": -25, "mentality": 15}, hidden_risk_log="朝鲜战场极寒严冬冻伤脚趾，晚年行走畏寒。"),
                    make_outcome("redirected", 8, "在志愿军铁道兵大队抢修清川江大桥，练成顶级铁道工匠。", {"knowledge": 25, "wealth": 20}, new_career_track="worker", status="railway_hero", hidden_risk_log="在铁道兵抢修中练成过硬技术，转战新中国成渝大动脉。"),
                    make_outcome("fatal", 1, "在前线阻击战中不幸被炮火覆盖壮烈牺牲。", is_fatal=True, hidden_risk_log="在朝鲜前线阵地阻击战中壮烈牺牲，追认为革命烈士。")
                ]
            },
            {
                "text": "留守后方厂矿与公社，三班倒突击赶制支前军需与棉被",
                "choiceTags": ["时代：1950–1953", "年龄：18–45", "门槛：产业劳动力"],
                "outcomes": [
                    make_outcome("safe", 65, "通宵加班缝制棉军被获评支前后方先进劳模，工资晋升一级。", {"wealth": 15, "knowledge": 15, "mentality": 15}, hidden_risk_log="后方保产表现优异晋升为正式技工，获评模范标兵。"),
                    make_outcome("injured", 22, "长期疲劳夜班患上严重神经衰弱与贫血，休养月余。", {"health": -15, "wealth": 10}, hidden_risk_log="支前高负荷加班导致气血亏虚，经调养后平稳。"),
                    make_outcome("entangled", 10, "个人捐出一个月薪资支援购买飞机大炮，手头略显拮据。", {"wealth": -15, "mentality": 20}, hidden_risk_log="倾力捐赠支援国防，展现了赤诚爱国情怀。"),
                    make_outcome("redirected", 3, "表现出色被吸收选派入省工业干校深造工程机械制造。", {"knowledge": 30, "wealth": 15}, new_career_track="tech_whitecollar", hidden_risk_log="因支前功绩被保送工农速成中学，改写了工匠生涯。")
                ]
            }
        ]
    )

    # 8. 1957 反右
    add_event(
        evt_id="evt_1957_fanyou",
        tier="era",
        title="1957年整风鸣放与言论考评",
        year_range=[1957, 1957],
        target_age=[20, 60],
        regions=["ALL"],
        exposure={"jobTracks": ["cadre_teacher", "tech_whitecollar"], "urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.70,
        fact_level="确证",
        historical_fact="1957年反右派斗争严重扩大化，大批知识分子、教师、爱国民主人士和党员干部被错划为‘右派分子’，下放边远农场监督劳动，造成长期历史悲剧。",
        narrative="单位礼堂贴满了‘大鸣大放’的大字报，领导动员人人‘帮党整风’‘畅所欲言’。同事们纷纷在发言簿上记录着意见，桌上的白纸和钢笔沉重如铁。",
        choices=[
            {
                "text": "谨言慎行闭门不谈时政，全副身心埋头备课与钻研业务",
                "choiceTags": ["时代：1957", "年龄：20–60", "门槛：教师/文教/干部"],
                "outcomes": [
                    make_outcome("safe", 65, "安稳度过风暴保全公职岗位，受到保守安分评语。", {"mentality": 10, "knowledge": 15}, hidden_risk_log="谨言慎行规避了整风扩大化漩涡，稳稳保住教职。"),
                    make_outcome("entangled", 25, "因发言‘不够热情积极’被要求在支部大会做自我批评检讨。", {"mentality": -15}, hidden_risk_log="虽未划右派但受警告批评，行事更加小心翼翼。"),
                    make_outcome("redirected", 10, "主动申请调往偏远县城初级中学任教远离是非旋涡。", {"wealth": -10, "knowledge": 15}, hidden_risk_log="主动下沉偏远基层躲避风暴，潜心扎根乡村教育。")
                ]
            },
            {
                "text": "本着真诚负责之心，如实反映基层工薪统销粮食短缺问题",
                "choiceTags": ["时代：1957", "年龄：20–60", "门槛：知识分子"],
                "outcomes": [
                    make_outcome("safe", 40, "因言论尚属中肯在老领导力保下深刻检讨过关。", {"mentality": -10, "knowledge": 10}, hidden_risk_log="老领导力保过关免予处分，心有余悸。"),
                    make_outcome("entangled", 35, "被划定为右派指标，撤职降薪下放偏远农场劳动改造。", {"wealth": -30, "health": -25, "mentality": -30}, status="labeled_rightist", hidden_risk_log="不幸错划为右派分子下放农场改造，直至1979年平反昭雪。"),
                    make_outcome("injured", 15, "被停发工资下放农场修渠劳作积劳成疾咳血。", {"health": -35, "wealth": -35}, status="labeled_rightist", hidden_risk_log="在农场繁重劳役中损伤肺脏，平反后依然体弱。"),
                    make_outcome("redirected", 9, "平反后被调入社科文史馆从事文书典籍整理工作。", {"knowledge": 30, "mentality": 15}, new_career_track="cadre_teacher", hidden_risk_log="晚年平反后专注文史档案整理，终成地方史学专家。"),
                    make_outcome("fatal", 1, "在极度抑郁与恶劣苦役中身心枯竭早逝。", is_fatal=True, hidden_risk_log="在农场恶劣寒冬劳作中积劳成疾不幸早逝。")
                ]
            }
        ]
    )

    # 9. 1958 大炼钢铁
    add_event(
        evt_id="evt_1958_dayuejin",
        tier="era",
        title="大炼钢铁动员与农业生产现实",
        year_range=[1958, 1959],
        target_age=[16, 65],
        regions=["ALL"],
        exposure={"jobTracks": ["worker", "farmer"]},
        pre_tags=[],
        trigger_prob=0.85,
        fact_level="确证",
        historical_fact="1958年全民大炼钢铁与大跃进运动全面展开，各地搭建土高炉昼夜开工，公社食堂大锅饭放开肚皮吃，部分地区虚报亩产浮夸风盛行。",
        narrative="土高炉火光通红照亮半边天，锣鼓喧天报捷。干部号召砸碎铁锅门环支援国家指标，公社大食堂敲响开饭钟声。漫天的浮夸口号下，田埂里的秋收却已无人看顾。",
        choices=[
            {
                "text": "佩戴防护手套规矩看守风门，严格按炉温加焦炭保安全",
                "choiceTags": ["时代：1958", "年龄：16–65", "门槛：工矿/社员"],
                "outcomes": [
                    make_outcome("safe", 60, "扎实掌握耐火砖风箱结构，未出任何安全事故平安收工。", {"knowledge": 20, "mentality": 10}, hidden_risk_log="在大炼钢铁中坚守安全规程，学通了冶炼风道基本原理。"),
                    make_outcome("injured", 25, "飞溅铁水烫穿胶鞋脚背留下红疤，敷烫伤膏治疗。", {"health": -20, "mentality": -5}, hidden_risk_log="高炉飞溅铁水烫伤脚面，留下永久性烫伤疤痕。"),
                    make_outcome("entangled", 12, "被邻组批评‘右倾保守出铁慢’，扣除当月工分补贴。", {"wealth": -10, "mentality": -15}, hidden_risk_log="因坚持安全操作被批保守，受扣罚工分委屈。"),
                    make_outcome("redirected", 3, "因懂风道机修被县农机局相中调入农机修配站当正式工。", {"knowledge": 20, "wealth": 15}, new_career_track="worker", hidden_risk_log="机修手艺被县农机局看中招录为正式职工。")
                ]
            },
            {
                "text": "悄悄向生产队长反映实情，趁夜色抢收垄里红薯藏入地窖",
                "choiceTags": ["时代：1958", "年龄：16–65", "门槛：农家社员"],
                "outcomes": [
                    make_outcome("safe", 65, "偷抢收的一窖红薯风干成片，成为全家随后荒年的救命口粮。", {"wealth": 20, "family": 20}, hidden_risk_log="务实低调藏下红薯干，护佑全家人挺过随后三年紧缩。"),
                    make_outcome("entangled", 25, "私藏粮食被民兵查抄，在大队社员大会上受通报批评。", {"wealth": -15, "mentality": -20}, hidden_risk_log="私藏红薯被搜出受大会批斗，但换来家门警醒。"),
                    make_outcome("injured", 10, "夜行抢收不慎踩滑跌落水渠擦伤大腿。", {"health": -15, "family": 10}, hidden_risk_log="夜间抢收滑落田渠扭伤右膝。")
                ]
            }
        ]
    )

    # 10. 1959–61 困难时期
    add_event(
        evt_id="evt_1959_kunnan_fuzhong",
        tier="era",
        title="三年自然灾害与粮食定量紧缩考验",
        year_range=[1959, 1961],
        target_age=[0, 80],
        regions=["ALL"],
        exposure={"urbanRural": "all"},
        pre_tags=[],
        trigger_prob=0.90,
        fact_level="确证",
        historical_fact="1959年至1961年因三年严重自然灾害叠加政策失误，全国粮食大幅减产，城乡面临严峻粮食短缺与生活困难，许多地区出现严重浮肿病与非正常死亡。",
        narrative="粮票按两称重，供销社柜台空空如也，饭碗里的稀汤能照出人影。许多亲邻双腿水肿一按一个坑，草根树皮早已剥净，漫长的寒冬里死亡阴影逼近每扇柴门。",
        choices=[
            {
                "text": "全家实行严格口粮定额，掺红薯叶洋槐花熬野菜团充饥度荒",
                "choiceTags": ["时代：1959–1961", "年龄：0–80", "门槛：全体城乡家庭"],
                "outcomes": [
                    make_outcome("safe", 55, "全家精打细算咬牙捱过至暗三年，消瘦如柴但骨肉全部保全。", {"health": -15, "family": 25, "mentality": 15}, hidden_risk_log="以极致节俭与坚韧互助熬过三年困难，家风坚忍。"),
                    make_outcome("injured", 28, "严重营养不良出现双下肢重度凹陷性水肿与夜盲症。", {"health": -35, "wealth": -10}, hidden_risk_log="严重缺粮导致重度营养不良性水肿，体质受损多年。"),
                    make_outcome("entangled", 12, "家中体衰老辈未能熬过严冬不幸离世，含泪草席安葬。", {"family": -30, "mentality": -25}, hidden_risk_log="三年困难时期痛失年迈长辈，成为长久之痛。"),
                    make_outcome("redirected", 4, "跟随老乡盲流南下逃荒至沿海茶场务工扎根异乡。", {"wealth": 10, "knowledge": 10}, new_career_track="worker", hidden_risk_log="荒年南下逃荒进入国营林茶场，由北向南迁徙定居。"),
                    make_outcome("fatal", 1, "在极端饥荒与极度虚脱中不幸殁于冬夜。", is_fatal=True, hidden_risk_log="在严寒冬荒极度营养衰竭中不幸离世。")
                ]
            },
            {
                "text": "向深山远涉数十里挖掘野生葛根橡子面，换取微薄热量",
                "choiceTags": ["时代：1959–1961", "年龄：14–60", "门槛：中青年劳力"],
                "outcomes": [
                    make_outcome("safe", 60, "采得数百斤葛根磨粉解了燃眉之急，支撑一家老小挺过春荒。", {"wealth": 15, "health": -10, "family": 20}, hidden_risk_log="涉险深山采野葛救全家于水火，赢得乡邻敬仰。"),
                    make_outcome("injured", 26, "误食未脱毒的苦楝子树皮导致急性中毒呕吐抢救脱险。", {"health": -30, "mentality": -10}, hidden_risk_log="误食野果树皮中毒，经洗胃中药灌服脱险。"),
                    make_outcome("entangled", 12, "采摘葛根被邻村巡逻队扣押没收一半，空手折返心酸痛哭。", {"mentality": -25, "wealth": -15}, hidden_risk_log="采粮被扣押折损，体味到荒年世态炎凉。"),
                    make_outcome("fatal", 2, "在悬崖采摘野生葛根时不慎踩空坠落不幸身亡。", is_fatal=True, hidden_risk_log="在险峻山崖挖掘野葛根时不慎失足罹难。")
                ]
            }
        ]
    )

    # 11. 1962 调整还乡
    add_event(
        evt_id="evt_1962_tiaozheng",
        tier="era",
        title="国民经济“八字方针”与精简职工还乡",
        year_range=[1962, 1963],
        target_age=[18, 55],
        regions=["ALL"],
        exposure={"jobTracks": ["worker"], "urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.75,
        fact_level="确证",
        historical_fact="1962年党中央贯彻“调整、巩固、充实、提高”八字方针，为压缩城市粮食和财政负担，动员近2000万城镇职工和家属精简退粮还乡支援农业一线。",
        narrative="厂广播站整日播送压缩基建战线、精简人员的通报。财务室在发放退职补助金与车票，许多刚进城两三年的青年工人们卷起被褥，站在去留十字路口。",
        choices=[
            {
                "text": "坚决留厂服从调配，主动报名去条件最艰苦的翻砂铸造车间保岗位",
                "choiceTags": ["时代：1962", "年龄：18–55", "门槛：城镇工矿职工"],
                "outcomes": [
                    make_outcome("safe", 60, "在艰苦车间任劳任怨保住全民所有制正式工编制与城市粮本。", {"wealth": 15, "knowledge": 15}, status="secured_factory_job", hidden_risk_log="咬牙苦干保住国企正式编制，为后半生奠定工薪保障。"),
                    make_outcome("injured", 25, "翻砂车间粉尘极重患上早期尘肺气管炎，胸闷常咳。", {"health": -25, "wealth": 15}, hidden_risk_log="翻砂重度粉尘伤及气管肺脏，落下慢性呼吸道病。"),
                    make_outcome("entangled", 15, "虽留厂但连续降薪两级，生活清贫节约支撑全家。", {"wealth": -10, "mentality": -10}, hidden_risk_log="降级降薪留厂保编，度过数年清苦日子。")
                ]
            },
            {
                "text": "服从大局领路费退粮还乡，回大队当整劳力侍奉老小侍弄承包田",
                "choiceTags": ["时代：1962", "年龄：18–55", "门槛：农村原籍职工"],
                "outcomes": [
                    make_outcome("safe", 65, "带回一笔安置费在村里修缮老屋，陪伴年迈父母享安稳日子。", {"family": 25, "health": 15, "wealth": -10}, new_career_track="farmer", status="returned_peasant", hidden_risk_log="退职还乡尽孝双亲，成为生产队懂机械的种田能手。"),
                    make_outcome("entangled", 25, "回乡后失去商品粮待遇，在繁重农活工分中略显失落沮丧。", {"mentality": -20, "wealth": -15}, new_career_track="farmer", hidden_risk_log="由城市职工退回农家，经历了长达数年的心理落差。"),
                    make_outcome("redirected", 10, "凭在工厂学到的机修车床手艺，担任大队拖拉机农机修配员。", {"knowledge": 20, "wealth": 15}, new_career_track="worker", hidden_risk_log="工厂手艺赋能乡村农机，成为全公社不可替代的拖拉机手。")
                ]
            }
        ]
    )

print("Era 1937-1965 registered!")
