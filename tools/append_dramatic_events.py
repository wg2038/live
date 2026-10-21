import json

with open('data/events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

new_events = [
  {
    "id": "evt_1976_tangshan_chuchai",
    "title": "塞翁失马：赴唐山出差名额与天意",
    "yearRange": [1976, 1976],
    "applicableRegions": ["华北", "东北", "华东"],
    "targetAge": [20, 55],
    "urbanRural": "urban",
    "isDecision": True,
    "historicalFact": "1976年7月28日河北唐山发生7.8级大地震。当时多地厂矿派员赴唐山机车车辆厂出差交流，有人因公在震中罹难，亦有人因偶发变故阴差阳错避开浩劫，祸福难料。",
    "narrative": "单位分到一个赴河北唐山机车车辆厂出差学习的名额，不仅食宿补助优渥，还能顺道采购紧俏工业品，车间同事人人争抢。行前两日，家中突生变故且你腹泻发烧，正犹豫是否咬牙前往。",
    "choices": [
      {
        "text": "咬牙服下止泻药，按原计划登上开往唐山的列车",
        "effect": { "health": -35, "mentality": -20 },
        "log": "抵达唐山招待所次日凌晨突遭大地震，被倒塌梁柱重压埋于瓦砾之下，历尽九死一生重伤获救。"
      },
      {
        "text": "因病无奈将名额让给同科老同事，留守原厂",
        "effect": { "mentality": 25, "family": 15 },
        "log": "塞翁失马：虽错失优渥差补，数日后闻听唐山大地震噩耗，老同事不幸罹难，自己因病偶避死劫，感叹冥冥天意。"
      }
    ]
  },
  {
    "id": "evt_1988_zhongzhuan_vs_dagong",
    "title": "塞翁失马：中专包分配与落榜南下",
    "yearRange": [1988, 1990],
    "applicableRegions": ["ALL"],
    "targetAge": [16, 20],
    "urbanRural": "all",
    "isDecision": True,
    "historicalFact": "80年代末中专、中技是无数底层寒门子弟跳出农门的捷径（包分配铁饭碗）。而落榜青年早早南下打工学手艺，却在90年代民营潮中各历沉浮，福祸相倚。",
    "narrative": "中考与中专放榜，这是决定两代人命运的关口。考上中专能立刻脱去农皮捧上铁饭碗；落榜者则只能收拾铺盖卷，跟着同乡长辈挤上南下的绿皮列车进厂谋生。",
    "choices": [
      {
        "text": "苦读考上省属中专技校，捧上令人艳羡的‘铁饭碗’",
        "effect": { "knowledge": 25, "family": 20, "wealth": 10 },
        "status": "chose_iron_bowl",
        "log": "中专毕业分配进国营大厂，当年全村敲锣打鼓放鞭炮，端上了令人敬仰的铁饭碗。"
      },
      {
        "text": "两分之差名落孙山，痛哭一场后南下沿海学五金模具手艺",
        "effect": { "wealth": 15, "health": -10, "knowledge": 10 },
        "status": "chose_south_artisan",
        "log": "塞翁失马：当年虽名落孙山受尽乡邻冷眼，却在珠三角摸爬滚打学通了开模手艺，为日后自己办厂埋下伏笔。"
      }
    ]
  },
  {
    "id": "evt_1994_biaohui_chuangye",
    "title": "祸福相倚：下海借贷扩产与民间标会爆雷",
    "yearRange": [1993, 1996],
    "applicableRegions": ["ALL"],
    "targetAge": [23, 50],
    "urbanRural": "all",
    "isDecision": True,
    "historicalFact": "90年代初商品经济狂飙，民间标会、抬会等高息集资盛行。部分创业者过度扩张遭遇货款三角债与标会链条断裂，顷刻间家破人亡、负债累累。",
    "narrative": "南巡讲话后处处是倒包货与办厂的暴富神话。同乡好友拉你入伙‘民间标会’借高息杠杆大举扩建厂房，月息高达两三分。这是一夜暴富的捷径，也是吃人不吐骨头的深渊。",
    "choices": [
      {
        "text": "抵押全家房产向标会借入数十万巨资猛扑扩产",
        "effect": { "wealth": -35, "mentality": -35, "family": -20 },
        "status": "hit_debt_crisis",
        "log": "大举加杠杆后遭遇三角债坏账与标会崩盘，血本无归被债主连日堵门催讨，跌入人生债务深渊。"
      },
      {
        "text": "胆小谨慎，谢绝高息借贷，仅靠自有薄利稳扎稳打",
        "effect": { "wealth": 10, "mentality": 15, "family": 10 },
        "log": "塞翁失马：虽被同行讥笑胆小无魄力，半年后标会全线崩盘会长潜逃，自己因保守本分保全了家小平安。"
      }
    ]
  },
  {
    "id": "evt_2018_jiage_touzi",
    "title": "祸福相倚：高杠杆加盟房产与现金求稳",
    "yearRange": [2017, 2019],
    "applicableRegions": ["ALL"],
    "targetAge": [25, 55],
    "urbanRural": "all",
    "isDecision": True,
    "historicalFact": "2018年前后实体商铺加盟、按揭多套投资与借贷炒作盛行。部分普通人盲目加杠杆，随后在2020突发疫情冲击中遭遇现金流断裂与债务违约。",
    "narrative": "身边朋友纷纷借网贷、刷信用卡按揭买下商铺或加盟网红餐饮店，言必称‘赚快钱逆风翻盘’。你手里捏着打拼半生的几十万血汗积蓄，正站在跟风扩张或谨小慎微的十字路口。",
    "choices": [
      {
        "text": "借贷加码，把全部积蓄投入加盟网红餐饮实体店",
        "effect": { "wealth": -25, "mentality": -20, "health": -10 },
        "status": "hit_entity_loss",
        "log": "大举借贷开业不久即遇突发封控客流断流，巨额房租与人员开支把多年积蓄亏个精光。"
      },
      {
        "text": "克制贪念，将积蓄老老实实存入银行定期大额存单",
        "effect": { "wealth": 10, "mentality": 15 },
        "log": "塞翁失马：虽错失了当老板的风光，几年后却凭借这笔结实的现金流安稳护佑全家挺过经济萧条。"
      }
    ]
  },
  {
    "id": "evt_2024_tibet_landslide",
    "title": "微观黑天鹅：高原公路突发山体滑坡与泥石流",
    "yearRange": [2024, 2026],
    "applicableRegions": ["西南", "西北"],
    "targetAge": [18, 65],
    "urbanRural": "all",
    "isDecision": True,
    "historicalFact": "近年来青藏高原及川西峡谷因强降雨诱发突发高位山体滑坡与泥石流地质灾害，道路瞬间阻断，行车安全瞬息万变，常有车辆因偶发小修整而绝处逢生。",
    "narrative": "行车于高原悬崖公路，窗外暴雨连绵，山体碎石偶有滚落。临近峡谷关口，车辆突然报警提示右后轮严重漏气，必须在路边简陋小客栈停留半日补胎，你正为耽误行程焦急烦躁。",
    "choices": [
      {
        "text": "塞翁失马：在客栈耐心等候补胎，就着热水吃碗泡面",
        "effect": { "mentality": 20, "family": 15 },
        "log": "塞翁失马：数小时后获知前方关口突发巨型山体滑坡掩埋路面，自己因车胎漏气耽搁反倒与死神擦肩而过！"
      },
      {
        "text": "不顾报警强行带伤车硬闯峡谷抢工期",
        "effect": { "health": -35, "wealth": -15, "mentality": -20 },
        "log": "行至半山遭遇突发落石泥石流砸翻车身，在激流碎石中被抢救脱险，身负多处骨折重伤。"
      }
    ]
  }
]

events.extend(new_events)

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print('Updated events.json! Total events now:', len(events))
