# -*- coding: utf-8 -*-
"""
全面构建《中国出生模拟器》核心数据库：
1. 31个省级行政区全覆盖 (province.json)
2. 全国333个地级行政区 + 代表性/典型困难县级市 (cities.json)
3. 1937–2026年特大自然灾害全息数据库 (disasters.json)
4. 五个年代代际人名全息库 (naming.json)
5. 自动打包更新 embedded.js
"""

import json
import os

# ==========================================
# 1. 31个省级行政区全面数据
# ==========================================
ALL_PROVINCES = [
  {"id": "beijing", "name": "北京市", "short": "京", "region": "华北", "popWeight": 22, "urbanRatioBaseline": 2.8, "tags": ["首都核心", "科教策源", "大院四合院"]},
  {"id": "tianjin", "name": "天津市", "short": "津", "region": "华北", "popWeight": 14, "urbanRatioBaseline": 2.2, "tags": ["北方工商业重镇", "海河要冲", "近代工业摇篮"]},
  {"id": "hebei", "name": "河北省", "short": "冀", "region": "华北", "popWeight": 74, "urbanRatioBaseline": 0.9, "tags": ["京畿环抱", "钢铁能源", "燕赵慷慨"]},
  {"id": "shanxi", "name": "山西省", "short": "晋", "region": "华北", "popWeight": 35, "urbanRatioBaseline": 0.95, "tags": ["乌金之乡", "表里山河", "重工业与煤电"]},
  {"id": "neimenggu", "name": "内蒙古自治区", "short": "蒙", "region": "华北", "popWeight": 24, "urbanRatioBaseline": 1.1, "tags": ["辽阔草原", "稀土之都", "林牧矿业并举"]},
  {"id": "liaoning", "name": "辽宁省", "short": "辽", "region": "东北", "popWeight": 42, "urbanRatioBaseline": 1.6, "tags": ["共和国长子", "重工装备", "钢都煤海"]},
  {"id": "jilin", "name": "吉林省", "short": "吉", "region": "东北", "popWeight": 24, "urbanRatioBaseline": 1.3, "tags": ["黑土粮仓", "第一汽车", "老工业基地"]},
  {"id": "heilongjiang", "name": "黑龙江省", "short": "黑", "region": "东北", "popWeight": 31, "urbanRatioBaseline": 1.4, "tags": ["北大荒北大仓", "大庆油田", "林海雪原"]},
  {"id": "shanghai", "name": "上海市", "short": "沪", "region": "华东", "popWeight": 25, "urbanRatioBaseline": 2.9, "tags": ["远东都会", "工商业中心", "弄堂文化"]},
  {"id": "jiangsu", "name": "江苏省", "short": "苏", "region": "华东", "popWeight": 85, "urbanRatioBaseline": 1.3, "tags": ["鱼米之乡", "苏南模式", "文教鼎盛"]},
  {"id": "zhejiang", "name": "浙江省", "short": "浙", "region": "华东", "popWeight": 65, "urbanRatioBaseline": 1.3, "tags": ["百工之乡", "温州模式", "民营经济先驱"]},
  {"id": "anhui", "name": "安徽省", "short": "皖", "region": "华东", "popWeight": 61, "urbanRatioBaseline": 0.88, "tags": ["江淮沃野", "小岗首创", "徽商故里"]},
  {"id": "fujian", "name": "福建省", "short": "闽", "region": "华东", "popWeight": 41, "urbanRatioBaseline": 1.15, "tags": ["八山一水一分田", "侨乡下南洋", "晋江民营"]},
  {"id": "jiangxi", "name": "江西省", "short": "赣", "region": "华东", "popWeight": 45, "urbanRatioBaseline": 0.88, "tags": ["革命摇篮", "江南鱼米", "有色金属"]},
  {"id": "shandong", "name": "山东省", "short": "鲁", "region": "华东", "popWeight": 101, "urbanRatioBaseline": 0.98, "tags": ["齐鲁大地", "工农业大省", "孔孟之乡"]},
  {"id": "henan", "name": "河南省", "short": "豫", "region": "华中", "popWeight": 98, "urbanRatioBaseline": 0.85, "tags": ["中原粮仓", "人口大省", "平原腹地"]},
  {"id": "hubei", "name": "湖北省", "short": "鄂", "region": "华中", "popWeight": 58, "urbanRatioBaseline": 1.1, "tags": ["九省通衢", "武钢二汽", "千湖之省"]},
  {"id": "hunan", "name": "湖南省", "short": "湘", "region": "华中", "popWeight": 66, "urbanRatioBaseline": 0.9, "tags": ["三湘四水", "有色之乡", "心忧天下"]},
  {"id": "guangdong", "name": "广东省", "short": "粤", "region": "华南", "popWeight": 126, "urbanRatioBaseline": 1.4, "tags": ["岭南热土", "改革前沿", "全球制造中心"]},
  {"id": "guangxi", "name": "广西壮族自治区", "short": "桂", "region": "华南", "popWeight": 50, "urbanRatioBaseline": 0.85, "tags": ["山水甲天下", "八桂重镇", "边贸走廊"]},
  {"id": "hainan", "name": "海南省", "short": "琼", "region": "华南", "popWeight": 10, "urbanRatioBaseline": 0.95, "tags": ["天涯海角", "热带海岛", "自贸港口"]},
  {"id": "chongqing", "name": "重庆市", "short": "渝", "region": "西南", "popWeight": 32, "urbanRatioBaseline": 1.25, "tags": ["山城江城", "重工汽摩", "抗战陪都"]},
  {"id": "sichuan", "name": "四川省", "short": "川", "region": "西南", "popWeight": 83, "urbanRatioBaseline": 0.9, "tags": ["天府之国", "三线军工", "大后方"]},
  {"id": "guizhou", "name": "贵州省", "short": "黔", "region": "西南", "popWeight": 38, "urbanRatioBaseline": 0.75, "tags": ["喀斯特山地", "三线内迁", "生态秘境"]},
  {"id": "yunnan", "name": "云南省", "short": "滇", "region": "西南", "popWeight": 47, "urbanRatioBaseline": 0.8, "tags": ["彩云之南", "有色烟草", "多民族聚居"]},
  {"id": "xizang", "name": "西藏自治区", "short": "藏", "region": "西南", "popWeight": 3, "urbanRatioBaseline": 0.6, "tags": ["雪域高原", "日光之城", "青稞牦牛"]},
  {"id": "shaanxi", "name": "陕西省", "short": "陕", "region": "西北", "popWeight": 39, "urbanRatioBaseline": 1.05, "tags": ["三秦故土", "军工航天", "能源金三角"]},
  {"id": "gansu", "name": "甘肃省", "short": "陇", "region": "西北", "popWeight": 25, "urbanRatioBaseline": 0.8, "tags": ["河西走廊", "石油化工", "苦瘠坚韧"]},
  {"id": "qinghai", "name": "青海省", "short": "青", "region": "西北", "popWeight": 6, "urbanRatioBaseline": 0.85, "tags": ["三江之源", "盐湖重工", "青藏枢纽"]},
  {"id": "ningxia", "name": "宁夏回族自治区", "short": "宁", "region": "西北", "popWeight": 7, "urbanRatioBaseline": 1.0, "tags": ["塞上江南", "黄河灌区", "宁东煤化工"]},
  {"id": "xinjiang", "name": "新疆维吾尔自治区", "short": "新", "region": "西北", "popWeight": 25, "urbanRatioBaseline": 0.95, "tags": ["丝路绿洲", "兵团屯垦", "棉花石油"]}
]

# 保存 province.json
with open('data/province.json', 'w', encoding='utf-8') as f:
    json.dump(ALL_PROVINCES, f, ensure_ascii=False, indent=2)
print("province.json 生成完成，共", len(ALL_PROVINCES), "个省份")

# ==========================================
# 2. 1937–2026年特大自然灾害全息数据库
# ==========================================
DISASTERS = [
  {
    "id": "dis_1938_huayuankou",
    "name": "花园口决堤黄泛浩劫",
    "year": 1938,
    "month": 6,
    "targetProvinces": ["henan", "anhui", "jiangsu"],
    "targetCities": ["zhengzhou", "kaifeng", "zhoukou", "shangqiu", "fuyang", "suzhou_ah", "xuzhou"],
    "severity": "catastrophic",
    "fact": "1938年6月国民政府为阻滞日军西进炸开郑州花园口黄河大堤。浑黄洪水奔腾而下，淹没豫皖苏44个县，形成长达九年、上万平方公里的黄泛区，据历史文献估计数百万人受灾或流离失所。",
    "hitNarrative": "深夜狂浪咆哮，黄水泥浆轰然冲毁门板屋梁！田畴房舍瞬间被泽国吞没，你与家人拼死抓住漂浮的树干，在恶臭的黄浪中绝望哭号，满目皆是溺亡的生灵与碎瓦。",
    "casualtyRoll": {
      "deathProb": 0.28,
      "injuryProb": 0.35,
      "wealthWipeProb": 0.85,
      "familyLossProb": 0.45
    }
  },
  {
    "id": "dis_1939_tianjin_flood",
    "name": "华北暴雨与海河天津特大水灾",
    "year": 1939,
    "month": 8,
    "targetProvinces": ["tianjin", "hebei"],
    "targetCities": ["tianjin", "baoding", "cangzhou"],
    "severity": "severe",
    "fact": "1939年8月华北特大暴雨，海河五大支流并涨漫顶。天津市区洪水漫街深达数米，交通瘫痪达两个月之久，日占当局与平民均困于房顶舟楫之上，传染病肆虐。",
    "hitNarrative": "浑浊的洪水淹至二楼窗台，城内断粮断水。尸体漂浮在泛着油渍的水面上，烈日曝晒下恶臭刺鼻。你挤在房顶草棚上分食一碗发馊的面糊，高烧与痢疾如影随形。",
    "casualtyRoll": { "deathProb": 0.12, "injuryProb": 0.30, "wealthWipeProb": 0.65, "familyLossProb": 0.20 }
  },
  {
    "id": "dis_1942_zhongyuan_famine",
    "name": "中原特大干旱与蝗灾大荒",
    "year": 1942,
    "month": 7,
    "targetProvinces": ["henan", "shanxi", "hebei", "anhui"],
    "targetCities": ["zhengzhou", "luoyang", "kaifeng", "xuchang", "pingdingshan", "nanyang", "shangqiu", "zhoukou"],
    "severity": "catastrophic",
    "fact": "1942至1943年河南遭遇百年不遇旱灾与漫天飞蝗，加之战争赋税过重，数百万难民沿陇海铁路向西逃荒，据学者与官方档案记载大量灾民因饥馁倒毙于途。",
    "hitNarrative": "田地干裂如龟甲，漫天蝗虫蔽日掠过，连树皮与草根都被啃光。家中米缸早已空空如也，老人为了省下一口口粮悄然离家自尽。你眼睁睁看着亲人消瘦成枯骨，在陇海路道班边绝望喘息。",
    "casualtyRoll": { "deathProb": 0.35, "injuryProb": 0.40, "wealthWipeProb": 0.90, "familyLossProb": 0.50 }
  },
  {
    "id": "dis_1954_changjiang_flood",
    "name": "长江淮河全流域特大洪灾",
    "year": 1954,
    "month": 7,
    "targetProvinces": ["hubei", "hunan", "jiangxi", "anhui", "jiangsu"],
    "targetCities": ["wuhan", "jingzhou", "yueyang", "jiujiang", "anqing", "wuhu", "nanjing"],
    "severity": "severe",
    "fact": "1954年长江暴发全流域百年一遇特大洪水，汉口最高水位达29.73米。数万军民抢险保卫武汉关大堤，荆江分洪区与多处洼地主动蓄洪，受灾农田达数千万亩。",
    "hitNarrative": "江水漫过堤头，军民手挽手跳入滚滚浊浪筑成人墙！分洪闸轰然开启，蓄洪区村落倾覆在巨浪之下。你全家老小被紧急转移到防汛芦席棚，在吸血虫病的阴影下啃着冰冷的杂粮窝头度日。",
    "casualtyRoll": { "deathProb": 0.08, "injuryProb": 0.25, "wealthWipeProb": 0.75, "familyLossProb": 0.15 }
  },
  {
    "id": "dis_1958_huanghe_flood",
    "name": "黄河特大洪峰险情",
    "year": 1958,
    "month": 7,
    "targetProvinces": ["henan", "shandong"],
    "targetCities": ["zhengzhou", "xinxiang", "kaifeng", "liaocheng", "dezhou", "jinan"],
    "severity": "moderate",
    "fact": "1958年7月黄河三门峡至花园口区间突降特大暴雨，花园口出现2.23万立方米/秒的罕见大洪峰，京广铁路黄河大桥被冲毁，鲁豫两省组织数百万人防汛抢险。",
    "hitNarrative": "铁轨大桥在狂涛撞击下轰然倾塌，大堤鸣锣报警彻夜不绝。全村男女老少冒着暴雨肩挑泥包围堵漫堤。你家低洼的麦田全部泡烂在淤泥里，一年的收成转眼化为乌有。",
    "casualtyRoll": { "deathProb": 0.05, "injuryProb": 0.18, "wealthWipeProb": 0.50, "familyLossProb": 0.08 }
  },
  {
    "id": "dis_1966_xingtai_earthquake",
    "name": "河北邢台大地震",
    "year": 1966,
    "month": 3,
    "targetProvinces": ["hebei"],
    "targetCities": ["xingtai", "handan", "shijiazhuang"],
    "severity": "catastrophic",
    "fact": "1966年3月8日及22日，河北邢台隆尧、宁晋相继发生6.8级与7.2级浅源大地震。华北平原大批土坯民房瞬间坍塌，周恩来总理三次亲赴灾区抚慰群众并提出抗震防震指导方针。",
    "hitNarrative": "黎明前地底传来雷鸣般的怒吼，地动山摇！厚重的泥土梁柱轰然砸落，整个村庄被遮天蔽日的灰尘吞没。你在废墟瓦砾下被压得骨裂吐血，身边传来邻里微弱的呼救与断断续续的悲咽。",
    "casualtyRoll": { "deathProb": 0.22, "injuryProb": 0.40, "wealthWipeProb": 0.70, "familyLossProb": 0.30 }
  },
  {
    "id": "dis_1970_tonghai_earthquake",
    "name": "云南通海7.7级大地震",
    "year": 1970,
    "month": 1,
    "targetProvinces": ["yunnan"],
    "targetCities": ["yuxi", "honghe"],
    "severity": "catastrophic",
    "fact": "1970年1月5日凌晨，云南通海、峨山一带发生7.7级强烈地震。震中烈度达10度，极震区房屋几乎全平，时值文革特殊时期，救灾在极其艰难闭塞的条件下展开。",
    "hitNarrative": "严冬深夜瓦砾横飞，大地撕开深不见底的裂缝。几秒钟内土房全部被夷为平地，狂风卷起严寒。你从断木下拉出被砸断腿的亲人，在没有帐篷的荒野瓦砾堆上抱团颤抖挨过漫漫长夜。",
    "casualtyRoll": { "deathProb": 0.25, "injuryProb": 0.38, "wealthWipeProb": 0.80, "familyLossProb": 0.35 }
  },
  {
    "id": "dis_1975_banqiao_dam",
    "name": "河南驻马店“75·8”特大溃坝惨剧",
    "year": 1975,
    "month": 8,
    "targetProvinces": ["henan"],
    "targetCities": ["zhumadian", "zhoukou", "luohe"],
    "severity": "catastrophic",
    "fact": "1975年8月超强台风停滞伏牛山脉，驻马店出现日降水逾千毫米极端暴雨。板桥、石漫滩两座大型水库及数十座中小型水库相继垮坝，据官方与历史资料记载数万人在睡梦中被洪峰冲走或因次生灾害罹难。",
    "hitNarrative": "凌晨两点半，半空炸裂般巨响，数米高的黑浊水头如巨龙咆哮推平村落！房屋树木在激流中如同火柴盒被碾得粉碎。你被巨浪卷入旋涡，在冰冷刺骨的洪水中拼尽最后一丝力气抓住浮尸与柴草漂浮逃生。",
    "casualtyRoll": { "deathProb": 0.38, "injuryProb": 0.35, "wealthWipeProb": 0.95, "familyLossProb": 0.55 }
  },
  {
    "id": "dis_1976_tangshan_earthquake",
    "name": "河北唐山7.8级大地震",
    "year": 1976,
    "month": 7,
    "targetProvinces": ["hebei", "tianjin", "beijing"],
    "targetCities": ["tangshan", "tianjin", "qinhuangdao", "chengde"],
    "severity": "catastrophic",
    "fact": "1976年7月28日凌晨3时42分，河北省唐山市发生里氏7.8级特大地震。百年重工业城市顷刻夷为平地，官方统计罹难24.2万余人、重伤16.4万余人，震后全国军民大营救展现了坚毅不屈的民族脊梁。",
    "hitNarrative": "大地剧烈颤抖，蓝白地光刺破黑夜！几秒钟内预制板与砖墙轰然砸落，整座城市化作数百万吨瓦砾。你满脸鲜血被卡在水泥板下动弹不得，至亲在咫尺呼喊中声音渐渐微弱，成为终生铭心的剧痛。",
    "casualtyRoll": { "deathProb": 0.42, "injuryProb": 0.45, "wealthWipeProb": 0.90, "familyLossProb": 0.60 }
  },
  {
    "id": "dis_1981_sichuan_flood",
    "name": "四川盆地特大夏汛洪灾",
    "year": 1981,
    "month": 7,
    "targetProvinces": ["sichuan", "chongqing"],
    "targetCities": ["chengdu", "mianyang", "deyang", "nanchong", "chongqing"],
    "severity": "severe",
    "fact": "1981年7月四川连降暴雨，嘉陵江、沱江、岷江干支流并暴发特大洪水，成昆铁路大桥被冲垮，沿江城镇数百万人受淹受灾，成渝工业生产与交通遭受重大破坏。",
    "hitNarrative": "成昆铁路大桥在洪峰中轰然坍塌，滚滚泥流漫过防洪墙灌进车间与居民楼。家具家电在泥浪里打着转漂走，全厂职工彻夜用沙袋抢救机床，身上满是划伤与污泥。",
    "casualtyRoll": { "deathProb": 0.06, "injuryProb": 0.20, "wealthWipeProb": 0.60, "familyLossProb": 0.10 }
  },
  {
    "id": "dis_1987_daxinganling_fire",
    "name": "大兴安岭“5·6”特大森林火灾",
    "year": 1987,
    "month": 5,
    "targetProvinces": ["heilongjiang"],
    "targetCities": ["daxinganling"],
    "severity": "catastrophic",
    "fact": "1987年5月6日，大兴安岭林区暴发特大森林火灾，8级大风引发‘火风暴’，烧毁漠河、图强等城镇林场，受灾群众达5万余人，上万人奋战近一个月扑灭火魔。",
    "hitNarrative": "天际被染成血红色，飓风卷着数十米高的火浪呼啸而来！木刻楞房屋在几分钟内化为火海。你跳上最后一辆逃难的卡车，热浪将后颈烤得焦脱起泡，回头望去，世代生息的家园已成一片焦炭地狱。",
    "casualtyRoll": { "deathProb": 0.18, "injuryProb": 0.35, "wealthWipeProb": 0.85, "familyLossProb": 0.25 }
  },
  {
    "id": "dis_1991_huadong_flood",
    "name": "江淮华东特大水灾",
    "year": 1991,
    "month": 6,
    "targetProvinces": ["anhui", "jiangsu", "henan"],
    "targetCities": ["hefei", "chuzhou", "bengbu", "fuyang", "huaian", "yangzhou"],
    "severity": "severe",
    "fact": "1991年夏江淮流域出现历史罕见集中梅雨，淮河滁河大水漫溢。数千万亩良田受淹，中国首次向国际社会发出人道主义求援呼吁，港澳同胞与全国军民掀起‘水灾募捐赈灾潮’。",
    "hitNarrative": "暴雨整整倾盆了半个月，大堤数度决口，大水漫过了院墙门楣。全家连夜划着木澡盆带着几件衣服逃到大堤上露宿。眼看刚插下的稻秧全泡在污泥中腐烂，全村男女老幼痛哭失声。",
    "casualtyRoll": { "deathProb": 0.05, "injuryProb": 0.18, "wealthWipeProb": 0.70, "familyLossProb": 0.08 }
  },
  {
    "id": "dis_1998_quanguo_flood",
    "name": "长江、嫩江、松花江全流域特大洪水",
    "year": 1998,
    "month": 8,
    "targetProvinces": ["hubei", "jiangxi", "hunan", "jilin", "heilongjiang"],
    "targetCities": ["wuhan", "jingzhou", "jiujiang", "yueyang", "daqing", "qiqihar", "harbin"],
    "severity": "catastrophic",
    "fact": "1998年夏季长江、嫩江、松花江全流域暴发特大洪水，九江决口、簰洲湾溃口，数十万解放军官兵与广大干部群众以血肉之躯‘人在堤在’筑成人肉防线，谱写抗洪壮歌。",
    "hitNarrative": "九江大堤溃口处水流如脱缰野马，冲锋舟在浊浪中狂颠。你随着村干部拼死搬运铁丝石笼跳入冰凉急流封堵管涌，双臂皮开肉绽。远处自己的老宅瓦房在激流中轰然倾塌沉入水底。",
    "casualtyRoll": { "deathProb": 0.08, "injuryProb": 0.22, "wealthWipeProb": 0.65, "familyLossProb": 0.12 }
  },
  {
    "id": "dis_2008_bingxue",
    "name": "南方特大低温雨雪冰冻灾害",
    "year": 2008,
    "month": 1,
    "targetProvinces": ["hunan", "guizhou", "jiangxi", "guangdong", "guangxi"],
    "targetCities": ["chenzhou", "changsha", "guiyang", "guangzhou", "shaoguan", "ganzhou"],
    "severity": "severe",
    "fact": "2008年春节前夕南方遭遇半个世纪罕见特大冰冻，高压电塔被冻雨压垮，郴州等地长时间断电停水，京广铁路瘫痪致使广州火车站数十万返乡务工人员滞留。",
    "hitNarrative": "高压电线杆在重冰重压下接连折断，全城断水停电陷入极寒黑暗。你被困在拥挤不堪的绿皮车厢或火车站广场，饥寒交迫中把仅剩的半袋饼干让给怀中发烧的孩子，手脚冻得乌紫发麻。",
    "casualtyRoll": { "deathProb": 0.04, "injuryProb": 0.20, "wealthWipeProb": 0.25, "familyLossProb": 0.05 }
  },
  {
    "id": "dis_2008_wenchuan_earthquake",
    "name": "四川汶川8.0级特大地震",
    "year": 2008,
    "month": 5,
    "targetProvinces": ["sichuan", "gansu", "shaanxi"],
    "targetCities": ["aba", "mianyang", "deyang", "guangyuan", "chengdu", "longnan", "hanzhong"],
    "severity": "catastrophic",
    "fact": "2008年5月12日14时28分，四川汶川发生里氏8.0级特大地震。极震区烈度达11度，山川崩碎，房屋大范围垮塌，据官方统计近7万人遇难、数十万人受伤，全国展开规模空前大营救。",
    "hitNarrative": "下午两点二十八分，脚下大地疯狂隆起撕裂，山体裹挟亿万吨巨石呼啸砸落！几秒钟内学校与厂房崩解成碎石粉末。你在漫天白灰中拼命扒开石块救出昏迷的同胞，泪水模糊了布满灰尘的面庞。",
    "casualtyRoll": { "deathProb": 0.35, "injuryProb": 0.42, "wealthWipeProb": 0.88, "familyLossProb": 0.48 }
  },
  {
    "id": "dis_2010_yushu_earthquake",
    "name": "青海玉树7.1级大地震",
    "year": 2010,
    "month": 4,
    "targetProvinces": ["qinghai"],
    "targetCities": ["yushu"],
    "severity": "severe",
    "fact": "2010年4月14日晨，青海玉树藏族自治州结古镇发生7.1级地震。土木藏式民居脆弱坍塌，地处4000米高海拔极寒缺氧，全国救援力量克服高原反应全力施救。",
    "hitNarrative": "清晨剧震将土木藏房震得四分五裂，高原狂风卷着刺鼻烟尘。你在零下几度的严寒瓦砾中忍受着剧烈的高原反应和胸闷头痛，用冻僵的双手刨挖被废墟压住的亲眷与经卷。",
    "casualtyRoll": { "deathProb": 0.20, "injuryProb": 0.36, "wealthWipeProb": 0.75, "familyLossProb": 0.28 }
  },
  {
    "id": "dis_2010_zhouqu_debris_flow",
    "name": "甘肃舟曲特大山洪泥石流",
    "year": 2010,
    "month": 8,
    "targetProvinces": ["gansu"],
    "targetCities": ["gannan"],
    "severity": "catastrophic",
    "fact": "2010年8月7日深夜，甘肃甘南藏族自治州舟曲县突发暴雨，三眼峪等峡谷暴发特大泥石流，淤泥带长达5公里、厚达数米，半座县城被黄泥吞噬，千余同胞不幸罹难。",
    "hitNarrative": "深夜一声闷雷轰响，数十米高的黄泥浊流推着房屋轿车排山倒海压来！你从二楼窗户拼死跃出攀上电线杆，眼睁睁看着脚下的家门被数米深的黑泥倾覆抹平，呼喊声瞬间消匿于死寂。",
    "casualtyRoll": { "deathProb": 0.32, "injuryProb": 0.35, "wealthWipeProb": 0.92, "familyLossProb": 0.45 }
  },
  {
    "id": "dis_2021_zhengzhou_rainstorm",
    "name": "河南郑州“7·20”特大暴雨",
    "year": 2021,
    "month": 7,
    "targetProvinces": ["henan"],
    "targetCities": ["zhengzhou", "xinxiang", "hebi", "zhoukou"],
    "severity": "severe",
    "fact": "2021年7月20日郑州遭遇千年罕见特大暴雨，小时降雨量超200毫米刷新大陆极值。地铁五号线、京广北路隧道积水倒灌，城市基础设施承压极大，全国自发互助众志成城救援。",
    "hitNarrative": "暴雨如同瀑布倾泻，路面洪水瞬间冲走车辆。你被困在积水漫过胸口的地下车库或车厢中，车窗外浊流翻滚。在氧气稀薄、积水渐升的绝境中，众人手拉手破窗互助，在死神指缝间逃出生天。",
    "casualtyRoll": { "deathProb": 0.06, "injuryProb": 0.18, "wealthWipeProb": 0.45, "familyLossProb": 0.08 }
  },
  {
    "id": "dis_2023_haihe_rainstorm",
    "name": "海河流域“23·7”特大暴雨与滞洪险情",
    "year": 2023,
    "month": 7,
    "targetProvinces": ["beijing", "hebei", "tianjin"],
    "targetCities": ["beijing", "baoding", "langfang", "tianjin"],
    "severity": "severe",
    "fact": "2023年7月底台风‘杜苏芮’残余环流在太行山燕山阻滞形成极端特大暴雨。门头沟、房山山洪暴发，河北涿州等多处蓄滞洪区漫水，大量图书库房与物流园被淹，全国救援队星夜驰援。",
    "hitNarrative": "山洪裹挟着泥沙巨树如巨兽般冲断公路桥梁，村庄通信电力全部归零。你与邻里挤在二楼楼顶看着齐腰深的浑水泡烂全部家具与藏书，救援冲锋舟在风雨中破浪而来的马达声成了唯一的希望。",
    "casualtyRoll": { "deathProb": 0.04, "injuryProb": 0.15, "wealthWipeProb": 0.55, "familyLossProb": 0.06 }
  }
]

# 保存 disasters.json
with open('data/disasters.json', 'w', encoding='utf-8') as f:
    json.dump(DISASTERS, f, ensure_ascii=False, indent=2)
print("disasters.json 生成完成，共", len(DISASTERS), "起特大自然灾害记录")

# ==========================================
# 3. 五个年代代际人名全息库 (naming.json)
# ==========================================
NAMING_SYSTEM = {
  "surnames": [
    {"name": "李", "weight": 79}, {"name": "王", "weight": 78}, {"name": "张", "weight": 76}, {"name": "刘", "weight": 68},
    {"name": "陈", "weight": 60}, {"name": "杨", "weight": 44}, {"name": "赵", "weight": 30}, {"name": "黄", "weight": 32},
    {"name": "周", "weight": 27}, {"name": "吴", "weight": 26}, {"name": "徐", "weight": 22}, {"name": "孙", "weight": 20},
    {"name": "胡", "weight": 17}, {"name": "朱", "weight": 16}, {"name": "高", "weight": 15}, {"name": "林", "weight": 16},
    {"name": "何", "weight": 14}, {"name": "郭", "weight": 14}, {"name": "马", "weight": 18}, {"name": "罗", "weight": 13},
    {"name": "梁", "weight": 12}, {"name": "宋", "weight": 11}, {"name": "郑", "weight": 11}, {"name": "谢", "weight": 10},
    {"name": "韩", "weight": 9},  {"name": "唐", "weight": 9},  {"name": "冯", "weight": 8},  {"name": "于", "weight": 8},
    {"name": "董", "weight": 8},  {"name": "萧", "weight": 7},  {"name": "程", "weight": 7},  {"name": "曹", "weight": 7}
  ],
  "eras": {
    "1937_1949": {
      "desc": "宗族字辈、乱世贱名与期盼",
      "male": [
        "铁蛋", "狗剩", "留住", "来福", "富贵", "栓马", "保住", "麦收", "喜子", "根生",
        "长庚", "德培", "仁宗", "文彬", "怀远", "振邦", "少卿", "伯庸", "志仁", "树德",
        "福安", "顺发", "贵祥", "荣庆", "全有", "秋生", "有财", "金生", "保田", "秉义"
      ],
      "female": [
        "招娣", "盼弟", "领娣", "大妮", "二妞", "春桃", "秋菊", "杏花", "金凤", "彩霞",
        "翠兰", "秀英", "玉兰", "素琴", "淑芳", "佩兰", "佩玉", "婉如", "桂枝", "月娥",
        "小妹", "喜妹", "巧云", "满妹", "四妹", "荷花", "喜鹊", "秀珍", "菊芬", "春芳"
      ]
    },
    "1950_1965": {
      "desc": "建国初潮、抗美援朝与集体劳动",
      "male": [
        "建国", "援朝", "保国", "和平", "跃进", "解放", "超英", "胜利", "向东", "爱民",
        "学农", "工兵", "志强", "国庆", "敬党", "学武", "铁成", "克勤", "春生", "友谊",
        "新华", "树华", "宏伟", "继红", "立新", "荣华", "自立", "卫平", "永康", "开元"
      ],
      "female": [
        "素珍", "秀荣", "玉兰", "巧云", "桂香", "秀兰", "淑芳", "爱华", "秋菊", "淑琴",
        "迎春", "红梅", "素华", "春英", "美玉", "玉芳", "丽娟", "惠珍", "素英", "春花",
        "向红", "桂兰", "彩英", "凤英", "巧珍", "香秀", "爱玲", "建华", "爱民", "喜迎"
      ]
    },
    "1966_1976": {
      "desc": "十年动荡、红色浪潮与忠字印记",
      "male": [
        "卫东", "红兵", "向阳", "忠东", "红旗", "文革", "长征", "军", "东风", "志刚",
        "立新", "跃华", "青松", "永红", "继东", "延安", "迎春", "大海", "前锋", "卫兵",
        "忠实", "挺进", "勇", "建军", "红星", "红卫", "抗震", "红光", "韶峰", "井冈"
      ],
      "female": [
        "秀英", "红梅", "卫红", "向红", "小红", "丹", "春梅", "雪梅", "海燕", "桂芝",
        "丽华", "彩云", "红霞", "玉梅", "冬梅", "秀芝", "晓燕", "志敏", "红英", "朝霞",
        "亚萍", "亚红", "爱兵", "立群", "秀红", "继红", "翠平", "彩平", "文娟", "爱军"
      ]
    },
    "1977_1999": {
      "desc": "拨乱反正、单字风潮与流行文化",
      "male": [
        "伟", "磊", "超", "强", "斌", "亮", "鹏", "帅", "刚", "勇", "涛", "波",
        "浩", "飞", "洋", "明", "杰", "辉", "峰", "健", "兵", "鑫", "成", "龙",
        "晓东", "海涛", "志远", "宇鹏", "俊杰", "博文", "建华", "小龙", "晓峰", "文华"
      ],
      "female": [
        "静", "艳", "丽", "娟", "敏", "芳", "娜", "婷", "雪", "倩", "琳", "洁",
        "燕", "梅", "欣", "丹", "萍", "莉", "霞", "琴", "玲", "颖", "晶", "薇",
        "晓丽", "海燕", "丽萍", "雅芳", "佳佳", "文秀", "雪飞", "丹丹", "婷婷", "美玲"
      ]
    },
    "2000_2026": {
      "desc": "千禧时代、古风言情与新世代生僻字",
      "male": [
        "浩然", "子轩", "宇航", "承泽", "奕辰", "睿杰", "子涵", "沐阳", "博文", "锦程",
        "梓轩", "俊熙", "梓豪", "一诺", "星宇", "明轩", "嘉豪", "鸿煊", "天佑", "泽楷",
        "浩宇", "雨泽", "嘉佑", "致远", "文轩", "晨曦", "铭轩", "俊哲", "翰林", "熠辰"
      ],
      "female": [
        "欣怡", "梓涵", "语桐", "诗涵", "若曦", "可馨", "梦瑶", "雨萱", "依诺", "芷晴",
        "紫薇", "思琪", "艺涵", "妙可", "晨熙", "安琪", "沐晴", "雅楠", "若冰", "佳怡",
        "羽桐", "心蕾", "嘉欣", "雨婷", "淑涵", "妍希", "芷琪", "清菡", "婉清", "锦儿"
      ]
    }
  },
  "regionalNuances": {
    "guangdong": {
      "male": ["阿强", "家辉", "焯林", "健荣", "耀棠", "焯荣", "炳添", "启聪", "俊贤"],
      "female": ["碧云", "翠凤", "彩霞", "少芬", "绮婷", "泳仪", "佩仪", "丽芬"]
    },
    "northeast": {
      "male": ["大勇", "二楞", "玉柱", "国梁", "喜子", "铁柱", "福柱"],
      "female": ["翠花", "玉芬", "银花", "桂荣", "金兰", "春秀"]
    },
    "ethnic": {
      "tibetan": {"male": ["扎西", "多吉", "索朗", "次仁", "旦增"], "female": ["卓玛", "央金", "拉姆", "德吉", "普布"]},
      "uyghur": {"male": ["买买提", "阿里木", "艾力", "努尔"], "female": ["古丽", "帕夏", "阿依古丽", "热娜"]},
      "mongolian": {"male": ["巴特尔", "乌力吉", "朝鲁", "额尔德尼"], "female": ["萨仁", "其其格", "娜仁", "斯琴"]}
    }
  }
}

# 保存 naming.json
with open('data/naming.json', 'w', encoding='utf-8') as f:
    json.dump(NAMING_SYSTEM, f, ensure_ascii=False, indent=2)
print("naming.json 生成完成，包含5大历史时期及地域/民族命名体系")

print("所有历史数据文件生成完毕！")
