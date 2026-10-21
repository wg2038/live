# tools/events_era_1966_1989.py
# -*- coding: utf-8 -*-
from tools.build_all_exposure_events import add_event, make_outcome

def register_events_1966_1989():
    # 1. 1966 红卫兵与学校停课
    add_event(
        evt_id="evt_1966_hongweibing",
        tier="era",
        title="学校停课与串联风潮",
        year_range=[1966, 1967],
        target_age=[13, 24],
        regions=["ALL"],
        exposure={"urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.88,
        fact_level="估计/文学化",
        historical_fact="1966年夏全国大中专学校停课，青年学生广泛成立组织参加大串联，社会秩序受到剧烈冲击，大批师生被卷入狂热洪流，后演化为不同派系冲突。",
        narrative="学校广播喇叭终日播放高亢口号，大字报层层叠叠糊满了教学楼红砖墙。课桌椅被堆在操场，年轻人手臂上套着鲜艳的袖标。身边的同学有人狂热起草倡议书，有人悄悄打包铺盖返家避险。",
        choices=[
            {
                "text": "闭门谢客躲在家中温习数理古籍，坚决不参与任何集会派系",
                "choiceTags": ["时代：1966–1967", "年龄：13–24", "地域：城市学校", "门槛：平民子弟"],
                "outcomes": [
                    make_outcome("safe", 65, "闭门苦读数卷旧籍，躲过了狂热风潮与外界纷扰波及。", {"knowledge": 25, "mentality": 10}, hidden_risk_log="在十年狂热初起时选择独善其身，保全了求学求知火种。"),
                    make_outcome("entangled", 25, "因‘态度消极逍遥’被扣发两月粮票口粮，遭同学冷眼疏离。", {"wealth": -10, "mentality": -15}, hidden_risk_log="因置身事外被视为‘逍遥派’，受到短暂冷落孤立。"),
                    make_outcome("injured", 9, "家中藏书被翻出没收，推搡阻拦间扭伤手腕。", {"health": -15, "knowledge": -10}, hidden_risk_log="为保护旧藏书籍与人争执扭伤手腕，心留阴影。"),
                    make_outcome("fatal", 1, "家宅遭误击起火，在救火混乱中失足坠亡。", is_fatal=True, hidden_risk_log="混乱中遭遇火患不幸失足罹难。")
                ]
            },
            {
                "text": "戴上红袖标跟随狂热人潮外出大串联，挤免费绿皮车游历名胜",
                "choiceTags": ["时代：1966–1967", "年龄：15–24", "地域：全国交通干线", "门槛：热血学生"],
                "outcomes": [
                    make_outcome("safe", 55, "乘车游历数省开阔眼界，见识民间疾苦后内心渐生清醒与悔思。", {"knowledge": 15, "mentality": 15}, hidden_risk_log="大串联走遍大江南北，亲眼目睹民间艰难，狂热退去转化为成熟。"),
                    make_outcome("injured", 25, "列车极度拥挤发生踩踏，肋骨受轻微骨折挫伤，落魄返家。", {"health": -25, "wealth": -10}, hidden_risk_log="串联途中因列车严重挤压踩踏致肋骨骨折，养伤数月。"),
                    make_outcome("entangled", 12, "在异地被卷入派系对峙冲突，档案留下问询记录，懊悔不已。", {"mentality": -20, "knowledge": -5}, hidden_risk_log="盲目参与狂热活动卷入派系争吵，成为青年时期的悔恨记忆。"),
                    make_outcome("redirected", 7, "在串联途中结识铁路机务段老工人，转行入路局当临时搬运养路工。", {"knowledge": 10, "wealth": 10}, new_career_track="worker", hidden_risk_log="串联途中因故滞留铁路段，结缘机车检修开启工人岁月。"),
                    make_outcome("fatal", 1, "列车站台极度拥挤失足跌落轨道不幸罹难。", is_fatal=True, hidden_risk_log="大串联极度混乱中在站台失足不幸罹难。")
                ]
            }
        ]
    )

    # 2. 1967 派系武斗避险
    add_event(
        evt_id="evt_1967_wudou",
        tier="era",
        title="工矿派系冲突与城郊避险",
        year_range=[1967, 1968],
        target_age=[16, 60],
        regions=["西南", "华南", "华中", "东北"],
        exposure={"urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.82,
        fact_level="估计/文学化",
        historical_fact="1967至1968年间部分工业重镇与大中城市出现严重的造反派系武斗，工厂停产、交通中断，给社会秩序和人民生命财产造成深重创伤。",
        narrative="重工业区高音喇叭传来对峙派系的刺耳叫骂，街道两侧门窗紧闭，墙面残留着钢管与石块抛掷砸击的痕迹。车间已经停工，部分激进分子在街头设卡封路，气氛压抑恐怖。",
        choices=[
            {
                "text": "连夜带家眷潜出市区，投奔城郊农村亲友自留地暂避风头",
                "choiceTags": ["时代：1967–1968", "年龄：16–60", "地域：武斗重灾城市", "门槛：乡间有亲友"],
                "outcomes": [
                    make_outcome("safe", 65, "在宁静乡村帮亲戚挑水打谷，平安避开城中冲突风暴。", {"family": 15, "health": 10, "wealth": -10}, hidden_risk_log="机警果断避居乡野，让全家人毫发无伤渡过最危险阶段。"),
                    make_outcome("entangled", 25, "虽避居乡下但城区住房遭到侵占，回城后费尽周折才讨回一间。", {"wealth": -20, "mentality": -15}, hidden_risk_log="虽避开正面冲突但房屋遭侵占损坏，花费多年维权。"),
                    make_outcome("injured", 9, "出城夜路遭遇盘查推搡，小腿被路边铁丝网划伤感染发炎。", {"health": -20, "wealth": -5}, hidden_risk_log="夜行避乱时不慎被铁丝网划伤留疤。"),
                    make_outcome("fatal", 1, "夜间出城遭遇流弹波及不幸身亡。", is_fatal=True, hidden_risk_log="出城途中不幸遭遇突发流弹波及罹难。")
                ]
            },
            {
                "text": "坚守家门反锁门窗，备足咸菜井水，严禁家人外出露面",
                "choiceTags": ["时代：1967–1968", "年龄：16–60", "地域：市区", "门槛：平民住户"],
                "outcomes": [
                    make_outcome("safe", 60, "靠腌咸菜与囤积面粉硬抗数月，门板虽遭石块砸击但安然无恙。", {"wealth": -10, "mentality": -10}, hidden_risk_log="反锁门户坚忍避险，在动荡中以最低消耗熬过混乱。"),
                    make_outcome("injured", 25, "玻璃窗被流弹石块击碎，飞溅碎渣划伤面部留下细微瘢痕。", {"health": -20, "mentality": -15}, hidden_risk_log="家中窗户被飞石击碎划伤面庞，留下永久微痕。"),
                    make_outcome("entangled", 13, "因坚决拒绝为某派系提供水电被切断管线，生活极度困顿。", {"wealth": -15, "mentality": -20}, hidden_risk_log="秉持中立拒绝选边站队，遭短暂停水停电刁难。"),
                    make_outcome("fatal", 2, "街道流弹射穿薄木门板不幸击中要害身亡。", is_fatal=True, hidden_risk_log="家中紧闭房门仍不幸遭遇穿门流弹罹难。")
                ]
            }
        ]
    )

    # 3. 1968 上山下乡大潮
    add_event(
        evt_id="evt_1968_shangshanxiaxiang",
        tier="era",
        title="知识青年“上山下乡”抉择",
        year_range=[1968, 1975],
        target_age=[16, 23],
        regions=["ALL"],
        exposure={"urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.90,
        fact_level="确证",
        historical_fact="1968年12月全国开展轰轰烈烈的大规模知识青年上山下乡运动。先后有约1700万城市中学毕业生奔赴农村插队落户或戍边农垦兵团，经受严苛生存历练。",
        narrative="站台上铜锣大鼓喧天，绿皮车窗塞满挂着大红花的中学毕业青年。汽笛长鸣，车厢里歌声与家长的掩面啜泣交织。行李卷上捆着搪瓷脸盆与红宝书，火车向着遥远的边疆与荒原疾驰。",
        choices=[
            {
                "text": "报名去北大荒/新疆生产建设兵团，戍边垦荒半军事化管理",
                "choiceTags": ["时代：1968–1975", "年龄：16–23", "地域：边疆兵团", "门槛：身心健壮青工"],
                "outcomes": [
                    make_outcome("safe", 60, "在严寒黑土地上开荒驾拖拉机，练就粗粝过硬体魄，被提拔为连队机务排长。", {"knowledge": 20, "health": 15, "mentality": 15}, status="corps_cadre", hidden_risk_log="在兵团高强度农机垦荒中磨炼意志，成为技术骨干。"),
                    make_outcome("injured", 26, "冬修水利冻伤脚趾并患严重风湿关节炎，每逢阴雨酸痛难耐。", {"health": -30, "wealth": 5}, hidden_risk_log="在零下数十度极寒中抗冻修渠，落下终生顽固关节炎。"),
                    make_outcome("entangled", 12, "繁重劳动下探亲指标被扣，数年无法回城省亲，内心无比思乡。", {"family": -20, "mentality": -15}, hidden_risk_log="兵团制度严密探亲受限，数年无法与父母相聚。"),
                    make_outcome("fatal", 2, "深林伐木或农机抢修时遭遇重大滚木侧翻事故不幸罹难。", is_fatal=True, hidden_risk_log="在边疆兵团伐木生产中遭遇突发滚木事故罹难。")
                ]
            },
            {
                "text": "去陕北/中原偏远山区农村生产队插队落户，吃住在老乡窑洞",
                "choiceTags": ["时代：1968–1975", "年龄：16–23", "地域：内陆乡村插队", "门槛：城镇普通初高中生"],
                "outcomes": [
                    make_outcome("safe", 58, "跟老乡学会担粪耕地，当上大队民办小学代课教师，深得乡亲信任爱护。", {"knowledge": 20, "family": 15, "mentality": 15}, status="countryside_teacher", hidden_risk_log="在贫瘠山区担任民办教师启智乡村，深得老区百姓厚爱。"),
                    make_outcome("injured", 28, "挑重担压弯脊梁患上腰肌劳损，且因饮用生水患上伤寒痊愈。", {"health": -25, "mentality": -5}, hidden_risk_log="农活繁重落下一身慢性腰劳损，身体底子大受影响。"),
                    make_outcome("entangled", 12, "回城指标几经周折均被关系户占领，在窑洞苦闷徘徊数载。", {"mentality": -25, "wealth": -10}, hidden_risk_log="插队多年数次招工返城落空，在黄土高坡饱受迷茫煎熬。"),
                    make_outcome("fatal", 2, "山洪暴发时为抢救生产队耕牛不慎被泥石流冲走不幸牺牲。", is_fatal=True, hidden_risk_log="山洪泥石流中抢救集体财产不幸落水罹难。")
                ]
            }
        ]
    )

    # 4. 1975 招工招干与知青返城前夜
    add_event(
        evt_id="evt_1975_zhicheng_zhaogong",
        tier="era",
        title="知青推荐上大学（工农兵学员）与招工调配",
        year_range=[1973, 1976],
        target_age=[20, 28],
        regions=["ALL"],
        exposure={"urbanRural": "rural"},
        pre_tags=[],
        trigger_prob=0.75,
        fact_level="确证",
        historical_fact="1970年代中期国家通过‘群众推荐、领导批准、学校复审’方式选拔工农兵学员入读大学，并逐步恢复工矿就地招工指标，成为下乡知青改变处境的主要途径。",
        narrative="公社大队部点着煤油灯，桌上摊开几张盖着红印的‘工农兵大专学员推荐表’与‘矿山国营招工推荐表’。全大队的知青都在屏息凝神，任何一个名额都能彻底改写后半生轨迹。",
        choices=[
            {
                "text": "平时任劳任怨群众口碑极好，争取大队贫下中农联名推荐读师范大学",
                "choiceTags": ["时代：1973–1976", "年龄：20–28", "地域：插队大队", "门槛：政治表现好/群众评价高"],
                "outcomes": [
                    make_outcome("safe", 65, "成功获评工农兵学员迈入省城大学校门，毕业分配到重点公立中学执教。", {"knowledge": 30, "wealth": 20, "mentality": 20}, new_career_track="cadre_teacher", status="gongnongbing_college", hidden_risk_log="因老实苦干获得群众联名推荐上大学，一举摆脱泥腿子命运。"),
                    make_outcome("entangled", 25, "在县级最后审核阶段被当地干部子女顶替，空欢喜一场，沮丧心酸。", {"mentality": -25, "family": -10}, hidden_risk_log="指标在县里被违规顶替，饱尝权力寻租的不公与辛酸。"),
                    make_outcome("redirected", 10, "错失大学名额，但被公社农机修配厂破格招录为固定农机技工。", {"knowledge": 15, "wealth": 15}, new_career_track="worker", hidden_risk_log="虽未上成大学但凭农机手艺被就地招录进厂，端上饭碗。")
                ]
            },
            {
                "text": "主动报名报考三线重工/矿务局最艰苦的井下采掘招工名额直通返城",
                "choiceTags": ["时代：1973–1976", "年龄：20–28", "地域：内陆工矿", "门槛：身体健壮青年"],
                "outcomes": [
                    make_outcome("safe", 55, "成功招工转正成为全民所有制矿山正式工，每月领重劳保粮与定额工资。", {"wealth": 25, "health": -5}, new_career_track="worker", status="secured_factory_job", hidden_risk_log="通过吃苦耐劳报考矿务局名额，提早四年重获城市全民工编制。"),
                    make_outcome("injured", 32, "井下作业遭遇冒顶落石砸伤小腿腓骨，伤愈后调任地面仓库保管员。", {"health": -30, "wealth": 15}, new_career_track="worker", hidden_risk_log="矿下负伤落疾后转为后勤仓库管理，因祸得福避开重粉尘。"),
                    make_outcome("entangled", 13, "工种过于偏僻艰苦且与城市彻底隔绝，后半生留在了荒山矿区。", {"mentality": -15, "family": -15}, hidden_risk_log="虽转为正式工但一生绑在荒凉大山矿山，难以回归大都市。")
                ]
            }
        ]
    )

    # 5. 1976 唐山大地震
    add_event(
        evt_id="evt_1976_tangshan",
        tier="era",
        title="1976唐山大地震浩劫与全国铁血驰援",
        year_range=[1976, 1976],
        target_age=[0, 80],
        regions=["华北", "东北", "华东"],
        exposure={"provinces": ["hebei", "tianjin", "beijing", "liaoning", "shandong"]},
        pre_tags=[],
        trigger_prob=0.85,
        fact_level="确证",
        historical_fact="1976年7月28日凌晨河北唐山发生7.8级强震，百年重工之城瞬间被夷为平地，数十万人伤亡。全国军民与医护工程队伍连夜奔赴前线展开空前大营救。",
        narrative="凌晨3时42分，地光如白昼般炸裂，大地发出如雷鸣般的闷响狂暴颠簸。房梁砖墙在数秒内轰然坍塌，空气中弥漫着刺鼻的石灰粉尘与漫天烟云。呼号与哀鸣划破废墟夜空。",
        choices=[
            {
                "text": "若身处震中周边废墟，咬紧牙关拼命徒手刨掘瓦砾抢救被埋邻里老幼",
                "choiceTags": ["时代：1976", "年龄：14–65", "地域：唐山/津京冀震区", "门槛：幸存者"],
                "outcomes": [
                    make_outcome("safe", 50, "手掌磨烂出血但成功从断壁下救出三名邻家幼童，全家幸存。", {"health": -15, "mentality": 25, "family": 20}, hidden_risk_log="在唐山大地震绝境中舍己救人，经受生离死别大考，心性如铁。"),
                    make_outcome("injured", 35, "救援时遭遇强烈余震坍塌，右肩与腰背被水泥重物砸伤留残。", {"health": -35, "mentality": -10}, hidden_risk_log="余震救援负伤致残，被授予抗震救灾荣誉模范。"),
                    make_outcome("entangled", 12, "虽保全性命但家中房屋全部倒塌，数年居住在简易抗震棚中。", {"wealth": -35, "mentality": -20}, hidden_risk_log="家产房舍尽数毁于地震，住简易棚长达数年。"),
                    make_outcome("fatal", 3, "在熟睡中遭遇重磅预制板坍塌重创不幸罹难。", is_fatal=True, hidden_risk_log="在1976唐山特大地震核心震中遭遇预制板坍塌不幸罹难。")
                ]
            },
            {
                "text": "若身处外省市，主动响应号召报名参加抗震抢修救灾志愿铁道工兵队",
                "choiceTags": ["时代：1976", "年龄：18–50", "地域：全国", "门槛：青壮工矿职员"],
                "outcomes": [
                    make_outcome("safe", 65, "日夜兼程冒暴雨抢通唐胥铁道与救灾货运站，荣立救灾二等功。", {"knowledge": 20, "mentality": 25, "wealth": 10}, status="tangshan_rescuer", hidden_risk_log="奔赴灾区一线抢通交通生命线，荣立三等功，锤炼坚韧品质。"),
                    make_outcome("injured", 25, "在灾区搬运重物时扭伤腰椎，并因防疫消杀刺激患上接触性皮炎。", {"health": -20, "mentality": 10}, hidden_risk_log="一线高强度抢修落下腰扭伤，但目睹大灾人间真情。"),
                    make_outcome("entangled", 10, "连续两月在一线抢险后方家中无人照看，积压多项家事纠纷。", {"family": -15, "mentality": -10}, hidden_risk_log="全心扑在救灾一线，疏忽了家里私务导致家庭摩擦。")
                ]
            }
        ]
    )

    # 6. 1977 恢复高考
    add_event(
        evt_id="evt_1977_gaokao",
        tier="era",
        title="关闭十年的高考考场重新开启",
        year_range=[1977, 1979],
        target_age=[16, 32],
        regions=["ALL"],
        exposure={"education": ["juniorMiddle", "seniorHigh", "primary"]},
        pre_tags=[],
        trigger_prob=0.92,
        fact_level="确证",
        historical_fact="1977年冬中断十年的普通高等学校招生考试正式恢复。570万积压十年的知青、工人、民办教师涌入冬月考场，全国录取率仅4.8%，深刻改变了个人与国家历史走向。",
        narrative="油印机散发着刺鼻的油墨香气，全公社唯一的数理化自学丛书被翻得卷了边。冬风呼啸的破教室里，手握铅笔的指节冻得通红。坐在身边的有三十出头的大叔，也有十七岁的青涩少年，所有人眼里全是灼热的光。",
        choices=[
            {
                "text": "点燃煤油灯通宵达旦刷题，辞去杂务全力以赴冲刺首届高考",
                "choiceTags": ["时代：1977–1979", "年龄：16–32", "门槛：初中及以上文化"],
                "outcomes": [
                    make_outcome("safe", 55, "以高分被省属重点大学理工科录取，拿到通知书那一夜痛哭失声。", {"knowledge": 45, "wealth": 25, "mentality": 30}, new_career_track="cadre_teacher", status="college_student_1977", hidden_risk_log="77级天之骄子，凭借一支钢笔逆天改命，跨入精英阶层。"),
                    make_outcome("entangled", 32, "几分之差遗憾名落孙山，面对繁杂家计不得不重返老本行营生。", {"mentality": -20, "knowledge": 15}, hidden_risk_log="几分之差未被录取，但自学积累的文化知识在日后工作中发挥实效。"),
                    make_outcome("injured", 13, "数月通宵备考极度透支视力与胃部，落下一度神经衰弱与重度近视。", {"health": -25, "mentality": -10}, hidden_risk_log="备考过度用脑患上神经衰弱，调理数年方才复原。")
                ]
            },
            {
                "text": "自知底子薄弱上有老下有小，放弃应考坚守现有岗位求安稳工薪",
                "choiceTags": ["时代：1977–1979", "年龄：22–35", "门槛：成家有负担者"],
                "outcomes": [
                    make_outcome("safe", 65, "本分工作领工资照顾老人小孩，生活虽平淡但柴米油盐踏实安详。", {"family": 20, "wealth": 15}, hidden_risk_log="选择现实安稳过日子，避开了千军万马挤独木桥的激烈竞争。"),
                    make_outcome("entangled", 25, "多年后看着考上大学的昔日同伴走上领导与高工岗位，心头泛起微涩。", {"mentality": -15}, hidden_risk_log="错过高考窗口期，在后来的学历崇尚时代感触良多。"),
                    make_outcome("redirected", 10, "靠勤奋踏实自学参加电大/夜大业余函授，亦拿到大专文凭晋升中级。", {"knowledge": 25, "wealth": 15}, new_career_track="cadre_teacher", hidden_risk_log="通过参加成人夜大弥补遗憾，走出一条踏实的业余求学路。")
                ]
            }
        ]
    )

    # 7. 1979 对越自卫还击战
    add_event(
        evt_id="evt_1979_duiyue_fanjizhan",
        tier="era",
        title="1979南疆自卫还击作战与支前动员",
        year_range=[1979, 1980],
        target_age=[18, 28],
        regions=["华南", "西南", "ALL"],
        exposure={"gender": "male", "urbanRural": "all"},
        pre_tags=[],
        trigger_prob=0.75,
        fact_level="确证",
        historical_fact="1979年2月对越自卫还击作战打响。大批热血军人与边境支前民兵奔赴南疆热带雨林山岳丛林作战，涌现出大批战斗英雄，有力维护了西南边境安全。",
        narrative="武装部的大喇叭里播放着热血军歌，南疆边境哨所接连告急。火车站台上挤满了换上崭新草绿色军装的参军青年，胸前佩戴的大红花娇艳欲滴。车厢内歌声嘹亮，即将踏入湿热险峻的山岳丛林。",
        choices=[
            {
                "text": "写下请战书报名开赴南疆前线，参加山地丛林穿插穿突击队",
                "choiceTags": ["时代：1979–1980", "年龄：18–25", "地域：全国", "门槛：热血青年男性"],
                "outcomes": [
                    make_outcome("safe", 50, "在猫耳洞与湿热丛林中奋勇穿插完成作战使命，荣立战功凯旋返乡。", {"mentality": 35, "knowledge": 15, "wealth": 20}, status="war_veteran", hidden_risk_log="参军经历南疆炮火洗礼，荣归故里成为受全社会敬仰的老兵功臣。"),
                    make_outcome("injured", 35, "在山隘排雷时遭遇弹片击中左小腿致轻残，退伍安置进机关车队。", {"health": -35, "mentality": 15, "wealth": 15}, status="disabled_veteran", hidden_risk_log="排雷作战负伤致轻度伤残，退伍保送安置体制内工作。"),
                    make_outcome("entangled", 13, "目睹战友牺牲患上创伤后应激障碍（PTSD），深夜偶发惊悸盗汗。", {"mentality": -30, "health": -15}, hidden_risk_log="战后长期受PTSD困扰，在家人悉心照料下逐步恢复。"),
                    make_outcome("fatal", 2, "在穿插阻击战中遭遇暗堡炮火伏击光荣牺牲。", is_fatal=True, hidden_risk_log="在南疆前线阻击阵地上光荣牺牲，被追授烈士称号。")
                ]
            },
            {
                "text": "服从地方分配报名参加边境弹药与战地伤员民兵公路抢运队",
                "choiceTags": ["时代：1979–1980", "年龄：18–35", "地域：西南/华南", "门槛：汽车兵/卡车司机/青壮"],
                "outcomes": [
                    make_outcome("safe", 65, "驾解放牌卡车冒着落石夜行盘山路抢送前线急需物资，平安立功。", {"wealth": 20, "knowledge": 20, "mentality": 20}, status="driver_hero", hidden_risk_log="作为战地运输骨干立功，锤炼出神入化的重型卡车驾驶技能。"),
                    make_outcome("injured", 25, "卡车在盘山公路遭遇特工伏击颠簸翻入边沟，锁骨骨折。", {"health": -25, "wealth": 10}, hidden_risk_log="战地运输车遭遇险情翻车负伤，休养半年后重返工作岗位。"),
                    make_outcome("entangled", 10, "因车辆遭炮火炸损承担审查损失，耗费半年才核销物资清单。", {"mentality": -15, "wealth": -10}, hidden_risk_log="战地物资损耗核查周折繁琐，心力交瘁。")
                ]
            }
        ]
    )

    # 8. 1983 严打治安整顿
    add_event(
        evt_id="evt_1983_yanda",
        tier="era",
        title="1983年全国社会治安大整顿（“严打”）",
        year_range=[1983, 1984],
        target_age=[16, 45],
        regions=["ALL"],
        exposure={"gender": "male", "urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.80,
        fact_level="确证",
        historical_fact="1983年8月起党中央在全国范围部署开展依法从重从快严厉打击严重刑事犯罪活动的斗争（严打），迅速扭转了十年动荡遗留的社会治安混乱局面，但也出现个别定罪过严过快情况。",
        narrative="街头大喇叭天天宣读公捕公判大会布告，白纸黑字下印着鲜红的对勾与公章。流氓阿飞、打架斗殴、调戏妇女等不良习气被雷霆扫荡。街头原本跳贴面舞、穿喇叭裤的青年们纷纷剪掉长发，收敛行径。",
        choices=[
            {
                "text": "本分做人恪守规矩，收起奇装异服，夜间绝不在街头巷尾游荡扎堆",
                "choiceTags": ["时代：1983–1984", "年龄：16–45", "地域：城镇街道", "门槛：守法市民"],
                "outcomes": [
                    make_outcome("safe", 70, "遵纪守法安稳度日，走夜路再也不用担心被小流氓劫道勒索，治安大好。", {"mentality": 15, "family": 15}, hidden_risk_log="身正不怕影子斜，严打期间规矩做人，享受社会治安好转红利。"),
                    make_outcome("entangled", 20, "曾与街头不良少年吃过两次饭被派出所叫去核实情况做笔录，虚惊一场。", {"mentality": -15}, hidden_risk_log="因早年江湖义气朋友受牵连协助调查，吸取教训远离不良圈子。"),
                    make_outcome("redirected", 10, "看到治安大队招募治安联防员，主动报名加入，协助社区抓捕盗窃分子。", {"wealth": 15, "mentality": 15}, new_career_track="cadre_teacher", hidden_risk_log="加入基层联防巡逻队，因表现突出转为街道保卫干部。")
                ]
            },
            {
                "text": "在舞厅因跳贴面舞与人发生口角推搡，被联防队员当场堵截扭送",
                "choiceTags": ["时代：1983–1984", "年龄：18–30", "地域：城市旱冰场/舞厅", "门槛：叛逆青年"],
                "outcomes": [
                    make_outcome("safe", 40, "经家人多方托人保释并写深刻检讨，免于处分释放回家痛改前非。", {"wealth": -15, "mentality": -10}, hidden_risk_log="虚惊一场写深刻检讨被领回家，彻底斩断与街头混混的联系。"),
                    make_outcome("entangled", 45, "被认定为‘聚众扰乱社会治安’收容劳教一年，工籍开除沦为待业人员。", {"wealth": -25, "mentality": -30, "family": -20}, new_career_track="worker", hidden_risk_log="严打风口浪尖因推搡被劳教一年除名，尝尽人情冷暖。"),
                    make_outcome("injured", 15, "抓捕推搡过程中肋骨被扭伤，在看守所内反思数月留下案底。", {"health": -25, "mentality": -25}, hidden_risk_log="抓捕拉扯负伤留下案底，成为青年时代难以磨灭的教训。")
                ]
            }
        ]
    )

    # 9. 1984 乡镇企业与首批万元户
    add_event(
        evt_id="evt_1984_xiangzhen_qiye",
        tier="era",
        title="乡镇企业“异军突起”与包产万元户",
        year_range=[1984, 1986],
        target_age=[20, 50],
        regions=["华东", "华南", "华中", "华北"],
        exposure={"urbanRural": "rural"},
        pre_tags=[],
        trigger_prob=0.82,
        fact_level="确证",
        historical_fact="1984年中央一号文件放宽农村劳动力向二三产业转移限制，乡镇企业‘异军突起’，温州模式、苏南模式席卷江南江北，首批靠养殖加工致富的‘万元户’戴红花上报纸。",
        narrative="村头原先的打谷场盖起两排红砖瓦房，里面传出冲压机和织布机的轰鸣。公社供销社的牌子换成了‘乡镇五金编织厂’。十里八乡第一台黑白电视机在村支书家点亮，老乡们趴在窗台上争相围观。",
        choices=[
            {
                "text": "拿出全家积蓄拉拢亲友入股，在村头创办小型塑料编织/冲压五金小厂",
                "choiceTags": ["时代：1984–1986", "年龄：22–50", "地域：乡镇", "门槛：有数千元启动金与手艺"],
                "outcomes": [
                    make_outcome("safe", 60, "赶上供不应求大行情，产品销往全省，成为全县敲锣打鼓的‘首届十万元户’。", {"wealth": 50, "mentality": 25}, new_career_track="merchant", status="village_entrepreneur", hidden_risk_log="敢为人先创办乡镇民营作坊，赶上市场短缺红利，奠定数十年家业。"),
                    make_outcome("injured", 25, "车间简陋冲压机切削不慎夹伤左手两指，虽落残疾但厂子保住产值。", {"health": -25, "wealth": 30}, new_career_track="merchant", hidden_risk_log="创业初期缺乏安全规程夹伤手指，但企业成功做大走上正轨。"),
                    make_outcome("entangled", 15, "因原材料被中间商诈骗亏光全副身家，负债累累被亲友上门催债。", {"wealth": -35, "mentality": -25}, hidden_risk_log="乡镇企业采购被皮包公司欺诈，负债两年才靠重操旧业还清。")
                ]
            },
            {
                "text": "进乡镇企业当计件固定包装工，农忙回村收麦打谷，离土不离乡",
                "choiceTags": ["时代：1984–1986", "年龄：18–45", "地域：乡镇村庄", "门槛：农村闲散劳力"],
                "outcomes": [
                    make_outcome("safe", 70, "月月领计件现金工资，家里添置了永久牌自行车与缝纫机，日子蒸蒸日上。", {"wealth": 20, "family": 15}, new_career_track="worker", hidden_risk_log="踏入乡镇企业成为中国第一代农民工，兼顾农田家庭两不误。"),
                    make_outcome("entangled", 20, "化工厂染料气味刺鼻引发严重皮肤过敏与慢性咳嗽，干满一年辞工。", {"health": -20, "wealth": 10}, hidden_risk_log="乡镇小化工厂劳保不足导致过敏鼻炎，及时止损返乡务农。"),
                    make_outcome("redirected", 10, "在厂里跟外聘老师傅掌握精修模具技术，被县城农机大厂挖走转正。", {"knowledge": 25, "wealth": 20}, new_career_track="worker", hidden_risk_log="自学掌握车床模具手艺，被县城全民所有制大厂当技术能手挖走。")
                ]
            }
        ]
    )

    # 10. 1985 出国留学与外语热
    add_event(
        evt_id="evt_1985_chuguore",
        tier="era",
        title="1980年代中期的“出国热”与托福狂潮",
        year_range=[1985, 1988],
        target_age=[20, 32],
        regions=["ALL"],
        exposure={"education": ["higherEd"], "urbanRural": "urban"},
        pre_tags=[],
        trigger_prob=0.75,
        fact_level="确证",
        historical_fact="1980年代中期随着改革开放深入，自费留学政策逐步放开，高校与科研院所刮起迅猛的‘出国热’。托福考试一票难求，大批优秀青年学者负笈海外求学。",
        narrative="外语培训班的黑板前挤满了戴黑框眼镜的大学生，录音机一遍遍倒带重放英语九百句。图书馆里最抢手的是泛黄的英汉大词典与美国大学院校名录。有人为了积攒留学考试费省吃俭用，四处寻找海外亲友担保。",
        choices=[
            {
                "text": "连夜排队报考托福GRE，向所有海外教授投递全奖申请信",
                "choiceTags": ["时代：1985–1988", "年龄：20–32", "门槛：高等学历/英语基础"],
                "outcomes": [
                    make_outcome("safe", 55, "斩获全额奖学金顺利飞赴北美名校攻读博士，开启跨国科研求学生涯。", {"knowledge": 40, "wealth": 25, "mentality": 20}, status="overseas_scholar", hidden_risk_log="80年代公派/全奖负笈海外，成为中国早期留学生精英。"),
                    make_outcome("entangled", 30, "托福成绩达标但签证数次被拒，白白耗费多年心血与积蓄，重回原单位工作。", {"wealth": -20, "mentality": -20}, hidden_risk_log="签证受挫未能成行，回原单位继续从事科研教职。"),
                    make_outcome("redirected", 15, "凭借娴熟英语与涉外技能，被外贸部合资代表处高薪聘为主管翻译。", {"wealth": 35, "knowledge": 25}, new_career_track="merchant", hidden_risk_log="因精通外语转入沿海合资外贸大潮，抢先享受涉外高薪待遇。")
                ]
            },
            {
                "text": "认定国内百废待兴机遇无限，留守国内科研院所/合资企业深耕",
                "choiceTags": ["时代：1985–1988", "年龄：22–35", "门槛：高校科研人员"],
                "outcomes": [
                    make_outcome("safe", 65, "作为重点项目青年骨干破格提拔为副研究员，分得两居室福利套房。", {"wealth": 25, "knowledge": 30, "family": 20}, status="promoted_scholar", hidden_risk_log="留守国内挑大梁，快速晋升为科研学术带头人并分得福利住房。"),
                    make_outcome("entangled", 25, "面对物价飞涨与‘造原子弹不如卖茶叶蛋’的脑体倒挂，心理落差明显。", {"mentality": -20, "wealth": -10}, hidden_risk_log="80年代末面对脑体倒挂经受过短暂迷茫，但坚持深耕本职。"),
                    make_outcome("redirected", 10, "接受沿海经济特区高薪招贤引才邀请，带技术档案南下深圳创办实业。", {"wealth": 40, "knowledge": 20}, new_career_track="merchant", hidden_risk_log="携技术成果南下特区投身实业转化，成为早期科技创业者。")
                ]
            }
        ]
    )

    # 11. 1989 年特殊事件见证与抉择（遵循严格准则9：事实性、克制、不渲染、不编造细节、史实等级标注为“估计/文学化”）
    add_event(
        evt_id="evt_1989_beijing_fengbo",
        tier="era",
        title="1989年春夏之交的风波与人生抉择",
        year_range=[1989, 1989],
        target_age=[17, 55],
        regions=["华北", "ALL"],
        exposure={"provinces": ["beijing", "tianjin", "shanghai", "hubei", "shaanxi"]},
        pre_tags=[],
        trigger_prob=0.85,
        fact_level="估计/文学化",
        historical_fact="1989年春夏之交北京及部分大城市发生政治风波，社会秩序与各行各业受到严重影响，随后国家平息局势并重新调整政策导向。",
        narrative="初夏的街头人流涌动，各类传单在大街小巷流传，公共交通陷入停滞。面对复杂的局面与纷乱的声音，单位与学校要求坚守岗位与考场，每个人都在复杂的时代漩涡前驻足沉思。",
        choices=[
            {
                "text": "坚守图书馆与科研车间本职岗位，闭门研读毕业论文，严守纪律",
                "choiceTags": ["时代：1989", "年龄：17–55", "地域：涉事大城市", "门槛：大中专师生/职工"],
                "outcomes": [
                    make_outcome("safe", 65, "潜心完成论文毕业设计并顺利通过答辩，如期分配进入省属科研事业单位。", {"knowledge": 20, "wealth": 15, "mentality": 10}, hidden_risk_log="在动荡时刻保持冷静克制守住书桌，平稳进入体制内开展学术生涯。"),
                    make_outcome("entangled", 25, "虽未参与任何活动，但因所属班级宿舍受到常规谈话审查，延期三月定岗。", {"mentality": -15}, hidden_risk_log="随大流经受例行谈话排查，虽无处分但心有郁结。"),
                    make_outcome("redirected", 10, "看淡虚浮纷扰，决定提前办理解约离京，奔赴广东沿海开放前沿发展。", {"wealth": 20, "mentality": 15}, new_career_track="merchant", hidden_risk_log="受时代风波感触提前南下南粤求索，开启民营经济打拼历程。")
                ]
            },
            {
                "text": "出于朴素关切在街头巷尾送开水、维持交通秩序与救护帮扶",
                "choiceTags": ["时代：1989", "年龄：18–45", "地域：大城市街头", "门槛：热心市民/青年"],
                "outcomes": [
                    make_outcome("safe", 55, "局势平息后默默重回原单位，将深切的感悟埋藏心底，踏实生活。", {"mentality": 15, "family": 10}, hidden_risk_log="见证时代剧变后回归寻常日子，以务实求真态度过好后半生。"),
                    make_outcome("injured", 20, "在夜间人流拥挤推搡中摔倒擦伤手臂与前胸，养伤一月。", {"health": -20, "wealth": -5}, hidden_risk_log="在夜间人流推挤中摔伤留痕，体会到现实的沉重与残酷。"),
                    make_outcome("entangled", 15, "被要求在单位连续三周写思想检查报告，入党考察期被推迟两年。", {"mentality": -25}, hidden_risk_log="因街头帮扶被要求写思想检讨并延缓提拔，历经数年方平复。"),
                    make_outcome("redirected", 9, "毅然辞去原有公职编制，远赴海南岛或深圳经济特区自谋生路。", {"wealth": 25, "mentality": 20}, new_career_track="merchant", hidden_risk_log="受风波影响脱离原体制南下商海，成为海南特区拓荒者之一。"),
                    make_outcome("fatal", 1, "在极度混乱的街区走避不及时遭遇突发意外不幸失去音讯罹难。", is_fatal=True, hidden_risk_log="在极度混乱的城市街区中遭遇突发意外不幸罹难。")
                ]
            }
        ]
    )

    print("Era 1966-1989 registered successfully!")
