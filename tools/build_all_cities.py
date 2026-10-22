# -*- coding: utf-8 -*-
"""
生成全国完整城市库 data/cities.json。

口径：
- 4 个直辖市
- 333 个地级行政区（地级市 / 地区 / 自治州 / 盟）
- 397 个县级市（含省直辖县级市、兵团城市）

共 734 个城市。县、市辖区不单列；每个县都归属于其所在地级市。
149 个手工校准城市（含括号注释、产业权重、历史称谓）原样保留；
新增城市复用 8 大产业原型，并按省份/城市地理与历史做类型归类。

用法：
    python3 -I tools/build_all_cities.py \
        --prefectures tools/data/cn_prefectures.json \
        --areas tools/data/cn_areas.json \
        --curated tools/data/curated_149_cities.json \
        --provinces data/province.json \
        --out data/cities.json
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from city_archetypes import ARCHETYPE_INDUSTRIES

PROVINCE_BY_CODE = {
    "11": "beijing", "12": "tianjin", "13": "hebei", "14": "shanxi",
    "15": "neimenggu", "21": "liaoning", "22": "jilin", "23": "heilongjiang",
    "31": "shanghai", "32": "jiangsu", "33": "zhejiang", "34": "anhui",
    "35": "fujian", "36": "jiangxi", "37": "shandong", "41": "henan",
    "42": "hubei", "43": "hunan", "44": "guangdong", "45": "guangxi",
    "46": "hainan", "50": "chongqing", "51": "sichuan", "52": "guizhou",
    "53": "yunnan", "54": "xizang", "61": "shaanxi", "62": "gansu",
    "63": "qinghai", "64": "ningxia", "65": "xinjiang",
}

MUNICIPALITIES = {
    "11": "beijing", "12": "tianjin", "31": "shanghai", "50": "chongqing",
}

SKIP_PREFECTURE_NAMES = {
    "市辖区", "县", "省直辖县级行政区划", "自治区直辖县级行政区划",
}

ETHNIC_WORDS = (
    "蒙古族", "蒙古", "藏族", "藏", "羌族", "羌", "维吾尔族", "维吾尔",
    "彝族", "彝", "苗族", "苗", "土家族", "土家", "布依族", "布依",
    "侗族", "侗", "哈尼族", "哈尼", "壮族", "壮", "傣族", "傣",
    "白族", "白", "景颇族", "景颇", "傈僳族", "傈僳", "回族", "回",
    "朝鲜族", "朝鲜", "哈萨克族", "哈萨克", "柯尔克孜族", "柯尔克孜",
    "仡佬族", "仡佬", "拉祜族", "拉祜", "佤族", "佤", "纳西族", "纳西",
    "瑶族", "瑶", "畲族", "畲", "黎族", "黎", "水族", "水",
)


def strip_annotations(name):
    return re.sub(r"[（(].*?[）)]", "", name).strip()


def base_name(name):
    """把 阿坝藏族羌族自治州 / 甘南州 / 喀什地区 / 昆山市 统一成 阿坝/甘南/喀什/昆山。"""
    s = strip_annotations(name)
    for word in ETHNIC_WORDS:
        s = s.replace(word, "")
    s = re.sub(r"(自治州|自治县|地区|盟|市|县|区|州)$", "", s)
    return s.strip()


def short_name(name):
    clean = strip_annotations(name)
    if "自治州" in clean:
        return base_name(clean) + "州"
    if clean.endswith("地区"):
        return base_name(clean) + "地区"
    if clean.endswith("盟"):
        return clean
    return base_name(clean) or clean


# 新增地级行政区的类型校准。键为去掉行政后缀后的地名。
# 未列出的新地级市使用省份默认类型。
TYPE_OVERRIDES = {
    # 河北
    "廊坊": "民营轻工集群型", "衡水": "传统农业劳务型",
    # 山西
    "晋城": "重工业资源型", "朔州": "重工业资源型", "晋中": "重工业资源型",
    "忻州": "重工业资源型", "吕梁": "重工业资源型",
    # 内蒙古
    "乌海": "重工业资源型", "赤峰": "重工业资源型", "通辽": "传统农业劳务型",
    "巴彦淖尔": "传统农业劳务型", "乌兰察布": "贫瘠特困型",
    "兴安": "边陲农牧林业型", "锡林郭勒": "边陲农牧林业型", "阿拉善": "边陲农牧林业型",
    # 辽宁
    "丹东": "沿海商贸外贸型", "锦州": "沿海商贸外贸型", "营口": "沿海商贸外贸型",
    "辽阳": "重工业资源型", "铁岭": "传统农业劳务型", "朝阳": "贫瘠特困型",
    "葫芦岛": "沿海商贸外贸型",
    # 吉林
    "四平": "传统农业劳务型", "辽源": "重工业资源型", "通化": "重工业资源型",
    "白山": "边陲农牧林业型", "松原": "重工业资源型", "白城": "贫瘠特困型",
    # 黑龙江
    "鸡西": "重工业资源型", "双鸭山": "重工业资源型", "伊春": "边陲农牧林业型",
    "佳木斯": "传统农业劳务型", "牡丹江": "民营轻工集群型", "黑河": "边陲农牧林业型",
    # 江苏
    "常州": "民营轻工集群型", "连云港": "沿海商贸外贸型", "盐城": "沿海商贸外贸型",
    "镇江": "民营轻工集群型", "泰州": "民营轻工集群型", "宿迁": "传统农业劳务型",
    # 浙江
    "嘉兴": "民营轻工集群型", "湖州": "民营轻工集群型", "衢州": "重工业资源型",
    "舟山": "沿海商贸外贸型", "丽水": "边陲农牧林业型",
    # 安徽
    "马鞍山": "重工业资源型", "铜陵": "重工业资源型", "安庆": "传统农业劳务型",
    "黄山": "边陲农牧林业型", "宿州": "传统农业劳务型", "六安": "贫瘠特困型",
    "亳州": "传统农业劳务型", "池州": "传统农业劳务型", "宣城": "传统农业劳务型",
    # 福建
    "莆田": "民营轻工集群型", "三明": "重工业资源型", "漳州": "沿海商贸外贸型",
    "南平": "边陲农牧林业型", "龙岩": "重工业资源型", "宁德": "贫瘠特困型",
    # 江西
    "景德镇": "民营轻工集群型", "新余": "重工业资源型", "鹰潭": "重工业资源型",
    "吉安": "传统农业劳务型", "宜春": "传统农业劳务型", "抚州": "传统农业劳务型",
    "上饶": "传统农业劳务型",
    # 山东
    "枣庄": "重工业资源型", "东营": "重工业资源型", "济宁": "重工业资源型",
    "泰安": "传统农业劳务型", "威海": "沿海商贸外贸型", "日照": "沿海商贸外贸型",
    "德州": "传统农业劳务型", "聊城": "传统农业劳务型", "滨州": "传统农业劳务型",
    # 河南
    "安阳": "重工业资源型", "鹤壁": "重工业资源型", "焦作": "重工业资源型",
    "濮阳": "重工业资源型", "许昌": "民营轻工集群型", "漯河": "民营轻工集群型",
    "三门峡": "重工业资源型", "信阳": "传统农业劳务型",
    # 湖北
    "黄石": "重工业资源型", "鄂州": "重工业资源型", "荆门": "重工业资源型",
    "孝感": "传统农业劳务型", "黄冈": "传统农业劳务型", "咸宁": "传统农业劳务型",
    "随州": "传统农业劳务型", "恩施": "贫瘠特困型",
    # 湖南
    "湘潭": "重工业资源型", "邵阳": "传统农业劳务型", "常德": "传统农业劳务型",
    "张家界": "边陲农牧林业型", "益阳": "传统农业劳务型", "永州": "传统农业劳务型",
    "怀化": "边陲农牧林业型", "娄底": "重工业资源型", "湘西": "贫瘠特困型",
    # 广东
    "韶关": "重工业资源型", "珠海": "沿海商贸外贸型", "江门": "民营轻工集群型",
    "肇庆": "民营轻工集群型", "惠州": "沿海商贸外贸型", "梅州": "边陲农牧林业型",
    "汕尾": "沿海商贸外贸型", "河源": "贫瘠特困型", "阳江": "沿海商贸外贸型",
    "清远": "传统农业劳务型", "中山": "民营轻工集群型", "潮州": "民营轻工集群型",
    "揭阳": "民营轻工集群型", "云浮": "传统农业劳务型",
    # 广西
    "梧州": "民营轻工集群型", "北海": "沿海商贸外贸型", "防城港": "沿海商贸外贸型",
    "钦州": "沿海商贸外贸型", "贵港": "传统农业劳务型", "玉林": "传统农业劳务型",
    "百色": "贫瘠特困型", "贺州": "传统农业劳务型", "河池": "贫瘠特困型",
    "来宾": "传统农业劳务型", "崇左": "边陲农牧林业型",
    # 海南
    "三沙": "边陲农牧林业型", "儋州": "沿海商贸外贸型",
    # 四川
    "自贡": "重工业资源型", "泸州": "重工业资源型", "德阳": "三线军工型",
    "广元": "三线军工型", "遂宁": "传统农业劳务型", "内江": "传统农业劳务型",
    "眉山": "传统农业劳务型", "广安": "传统农业劳务型", "达州": "三线军工型",
    "巴中": "贫瘠特困型", "资阳": "传统农业劳务型", "甘孜": "边陲农牧林业型",
    "凉山": "边陲农牧林业型",
    # 贵州
    "安顺": "三线军工型", "毕节": "贫瘠特困型", "黔西南": "边陲农牧林业型",
    "黔东南": "边陲农牧林业型", "黔南": "边陲农牧林业型",
    # 云南
    "曲靖": "重工业资源型", "保山": "边陲农牧林业型", "昭通": "贫瘠特困型",
    "丽江": "边陲农牧林业型", "普洱": "边陲农牧林业型", "临沧": "边陲农牧林业型",
    "楚雄": "边陲农牧林业型", "文山": "边陲农牧林业型", "西双版纳": "边陲农牧林业型",
    "大理": "边陲农牧林业型", "德宏": "边陲农牧林业型", "怒江": "贫瘠特困型",
    "迪庆": "贫瘠特困型",
    # 西藏
    "昌都": "边陲农牧林业型", "林芝": "边陲农牧林业型", "山南": "边陲农牧林业型",
    "那曲": "边陲农牧林业型", "阿里": "边陲农牧林业型",
    # 陕西
    "铜川": "重工业资源型", "咸阳": "传统农业劳务型", "渭南": "传统农业劳务型",
    "安康": "三线军工型", "商洛": "贫瘠特困型",
    # 甘肃
    "嘉峪关": "重工业资源型", "金昌": "重工业资源型", "天水": "三线军工型",
    "武威": "传统农业劳务型", "张掖": "传统农业劳务型", "平凉": "传统农业劳务型",
    "庆阳": "传统农业劳务型", "陇南": "贫瘠特困型", "临夏": "贫瘠特困型",
    # 青海
    "海东": "传统农业劳务型", "海北": "边陲农牧林业型", "黄南": "边陲农牧林业型",
    "海南": "边陲农牧林业型", "果洛": "贫瘠特困型",
    # 宁夏
    "吴忠": "传统农业劳务型", "中卫": "传统农业劳务型",
    # 新疆
    "吐鲁番": "传统农业劳务型", "哈密": "重工业资源型", "昌吉": "传统农业劳务型",
    "博尔塔拉": "边陲农牧林业型", "巴音郭楞": "边陲农牧林业型",
    "阿克苏": "边陲农牧林业型", "克孜勒苏": "贫瘠特困型", "和田": "贫瘠特困型",
    "伊犁": "边陲农牧林业型", "塔城": "边陲农牧林业型", "阿勒泰": "边陲农牧林业型",
}

PROVINCE_DEFAULT_TYPE = {
    "hebei": "重工业资源型", "shanxi": "重工业资源型", "neimenggu": "边陲农牧林业型",
    "liaoning": "重工业资源型", "jilin": "传统农业劳务型", "heilongjiang": "重工业资源型",
    "jiangsu": "民营轻工集群型", "zhejiang": "民营轻工集群型", "anhui": "传统农业劳务型",
    "fujian": "民营轻工集群型", "jiangxi": "传统农业劳务型", "shandong": "传统农业劳务型",
    "henan": "传统农业劳务型", "hubei": "传统农业劳务型", "hunan": "传统农业劳务型",
    "guangdong": "民营轻工集群型", "guangxi": "传统农业劳务型", "hainan": "沿海商贸外贸型",
    "sichuan": "传统农业劳务型", "guizhou": "传统农业劳务型", "yunnan": "边陲农牧林业型",
    "xizang": "边陲农牧林业型", "shaanxi": "传统农业劳务型", "gansu": "传统农业劳务型",
    "qinghai": "边陲农牧林业型", "ningxia": "传统农业劳务型", "xinjiang": "边陲农牧林业型",
}

# 县级市默认继承所在地级市的类型；以下几个组合做特殊处理。
COUNTY_TYPE_FROM_PARENT = {
    "综合科教中心": "民营轻工集群型",
    "沿海商贸外贸型": "民营轻工集群型",
}

PRE_NAME_OVERRIDES = {
    "北京": ("北京市", 1949, "北平市"),
    "天津": ("天津市", 1949, "天津市"),
    "上海": ("上海市", 1949, "上海特别市"),
    "重庆": ("重庆市", 1997, "四川省重庆市"),
    "深圳": ("深圳市", 1979, "宝安县"),
    "珠海": ("珠海市", 1979, "香山县"),
    "中山": ("中山市", 1988, "香山县"),
    "东莞": ("东莞市", 1988, "东莞县"),
    "佛山": ("佛山市", 1949, "南海县"),
    "海口": ("海口市", 1926, "琼山县"),
    "三亚": ("三亚市", 1987, "崖县"),
    "儋州": ("儋州市", 2015, "儋县"),
    "三沙": ("三沙市", 2012, "崖县西沙群岛"),
    "乌鲁木齐": ("乌鲁木齐市", 1954, "迪化市"),
    "呼和浩特": ("呼和浩特市", 1954, "归绥市"),
    "包头": ("包头市", 1950, "包头县"),
    "鄂尔多斯": ("鄂尔多斯市", 2001, "伊克昭盟"),
    "呼伦贝尔": ("呼伦贝尔市", 2001, "呼伦贝尔盟"),
    "赤峰": ("赤峰市", 1983, "昭乌达盟"),
    "通辽": ("通辽市", 1999, "哲里木盟"),
    "巴彦淖尔": ("巴彦淖尔市", 2004, "巴彦淖尔盟"),
    "乌兰察布": ("乌兰察布市", 2003, "乌兰察布盟"),
    "兴安": ("兴安盟", 1949, "兴安盟"),
    "锡林郭勒": ("锡林郭勒盟", 1949, "锡林郭勒盟"),
    "阿拉善": ("阿拉善盟", 1949, "阿拉善盟"),
    "沈阳": ("沈阳市", 1949, "奉天市"),
    "大连": ("大连市", 1950, "旅大市"),
    "丹东": ("丹东市", 1965, "安东市"),
    "大庆": ("大庆市", 1979, "安达特区"),
    "攀枝花": ("攀枝花市", 1965, "渡口市"),
    "十堰": ("十堰市", 1969, "郧县十堰镇"),
    "东营": ("东营市", 1983, "垦利县"),
    "克拉玛依": ("克拉玛依市", 1958, "黑油山矿区"),
    "嘉峪关": ("嘉峪关市", 1971, "酒泉县嘉峪关"),
    "金昌": ("金昌市", 1981, "永昌县"),
    "六盘水": ("六盘水市", 1978, "水城特区"),
    "吐鲁番": ("吐鲁番市", 2015, "吐鲁番县"),
    "哈密": ("哈密市", 2016, "哈密县"),
    "昌都": ("昌都市", 2014, "昌都地区"),
    "林芝": ("林芝市", 2015, "林芝地区"),
    "山南": ("山南市", 2016, "山南地区"),
    "那曲": ("那曲市", 2018, "那曲地区"),
    "海东": ("海东市", 2013, "海东地区"),
    "毕节": ("毕节市", 2011, "毕节地区"),
    "中卫": ("中卫市", 2004, "中卫县"),
    "吴忠": ("吴忠市", 1998, "吴忠县"),
    "黄山": ("黄山市", 1987, "徽州地区"),
    "普洱": ("普洱市", 2007, "思茅市"),
    "丽江": ("丽江市", 2002, "丽江地区"),
    "张家界": ("张家界市", 1994, "大庸市"),
    "鄂尔多斯_": ("鄂尔多斯市", 2001, "伊克昭盟"),
}

# 为保持 disasters.json 中已有的城市 ID 兼容，新增城市沿用这些历史 ID。
LEGACY_IDS = {
    ("anhui", "prefecture", "安庆"): "anqing",
    ("sichuan", "prefecture", "德阳"): "deyang",
    ("shandong", "prefecture", "德州"): "dezhou",
    ("sichuan", "prefecture", "广元"): "guangyuan",
    ("henan", "prefecture", "鹤壁"): "hebi",
    ("hebei", "prefecture", "廊坊"): "langfang",
    ("shandong", "prefecture", "聊城"): "liaocheng",
    ("gansu", "prefecture", "陇南"): "longnan",
    ("henan", "prefecture", "漯河"): "luohe",
    ("guangdong", "prefecture", "韶关"): "shaoguan",
    ("anhui", "prefecture", "宿州"): "suzhou_ah",
    ("henan", "prefecture", "许昌"): "xuchang",
}

COUNTY_TYPE_OVERRIDES = {
    "济源": "重工业资源型",
    "仙桃": "传统农业劳务型",
    "潜江": "传统农业劳务型",
    "天门": "传统农业劳务型",
    "恩施": "传统农业劳务型",
    "大理": "边陲农牧林业型",
    "楚雄": "传统农业劳务型",
    "文山": "边陲农牧林业型",
    "临夏": "传统农业劳务型",
    "玉树": "边陲农牧林业型",
    "昌吉": "传统农业劳务型",
    "阿克苏": "边陲农牧林业型",
    "喀什": "边陲农牧林业型",
    "和田": "贫瘠特困型",
    "塔城": "边陲农牧林业型",
    "阿勒泰": "边陲农牧林业型",
}

MAJOR_CITY_WEIGHTS = {
    "北京": 22, "天津": 14, "上海": 25, "重庆": 32,
    "广州": 20, "深圳": 20, "成都": 18, "武汉": 16, "西安": 15,
    "杭州": 15, "南京": 14, "沈阳": 12, "哈尔滨": 11, "长春": 10,
    "济南": 12, "青岛": 13, "郑州": 13, "长沙": 12, "合肥": 11,
    "福州": 10, "厦门": 9, "昆明": 10, "南宁": 9, "贵阳": 8,
    "兰州": 8, "太原": 9, "石家庄": 11, "南昌": 9, "乌鲁木齐": 8,
    "呼和浩特": 7, "银川": 6, "西宁": 5, "拉萨": 4,
    "苏州": 12, "无锡": 10, "常州": 8, "南通": 8, "徐州": 8,
    "宁波": 10, "温州": 9, "佛山": 10, "东莞": 10, "中山": 6,
    "珠海": 5, "惠州": 6, "汕头": 6, "泉州": 7, "烟台": 7,
    "唐山": 8, "保定": 8, "洛阳": 8, "襄阳": 7, "宜昌": 6,
}

# 县级市设市年份的常见取值。默认 1985，个别早期设市城市单独校准。
COUNTY_FOUNDING_OVERRIDES = {
    "石河子": 1976, "昆山": 1989, "江阴": 1987, "义乌": 1988,
    "晋江": 1992, "涿州": 1986, "北票": 1985, "仙桃": 1986,
    "辛集": 1986, "遵化": 1992, "迁安": 1996, "任丘": 1986,
    "泊头": 1982, "南宫": 1986, "沙河": 1987, "武安": 1988,
    "兖州": 1992, "曲阜": 1986, "邹城": 1992, "滕州": 1988,
    "龙口": 1986, "莱州": 1988, "招远": 1991, "蓬莱": 1991,
    "荣成": 1988, "文登": 1988, "乳山": 1993, "寿光": 1993,
    "诸城": 1987, "青州": 1986, "高密": 1994, "昌邑": 1994,
    "仪征": 1986, "高邮": 1991, "兴化": 1987, "靖江": 1993,
    "泰兴": 1992, "启东": 1989, "海门": 1994, "如皋": 1991,
    "溧阳": 1990, "宜兴": 1988, "张家港": 1986, "常熟": 1983,
    "太仓": 1993, "吴江": 1992, "慈溪": 1988, "余姚": 1985,
    "诸暨": 1989, "嵊州": 1995, "海宁": 1986, "桐乡": 1993,
    "平湖": 1991, "温岭": 1994, "临海": 1986, "玉环": 2017,
    "乐清": 1993, "瑞安": 1987, "永康": 1992, "东阳": 1988,
    "兰溪": 1985, "江山": 1987, "龙泉": 1990, "福清": 1990,
    "长乐": 1994, "永安": 1984, "石狮": 1988, "南安": 1993,
    "龙海": 1993, "邵武": 1983, "武夷山": 1989, "建瓯": 1992,
    "福安": 1989, "福鼎": 1995, "瑞金": 1994, "井冈山": 1984,
    "丰城": 1988, "樟树": 1988, "高安": 1993, "德兴": 1990,
    "乐平": 1992, "贵溪": 1996, "南康": 2013, "龙南": 2020,
    "巩义": 1991, "新密": 1994, "新郑": 1994, "登封": 1994,
    "荥阳": 1994, "偃师": 1993, "孟州": 1996, "沁阳": 1989,
    "卫辉": 1988, "辉县": 1988, "长垣": 2019, "林州": 1994,
    "禹州": 1988, "长葛": 1993, "舞钢": 1990, "汝州": 1988,
    "项城": 1993, "永城": 1996, "邓州": 1988, "固始": 2014,
    "汉川": 1997, "应城": 1986, "安陆": 1987, "广水": 1988,
    "仙桃": 1986, "潜江": 1988, "天门": 1987, "石首": 1986,
    "洪湖": 1987, "松滋": 1995, "宜城": 1994, "老河口": 1987,
    "枣阳": 1988, "宜都": 1987, "当阳": 1988, "枝江": 1996,
    "大冶": 1994, "阳新": 1996, "赤壁": 1986, "武穴": 1987,
    "麻城": 1986, "恩施市": 1981, "利川": 1986, "浏阳": 1993,
    "醴陵": 1985, "湘乡": 1986, "韶山": 1990, "耒阳": 1986,
    "常宁": 1996, "武冈": 1994, "邵东": 2019, "汨罗": 1987,
    "临湘": 1992, "津市": 1979, "沅江": 1988, "资兴": 1984,
    "洪江": 1979, "冷水江": 1987, "涟源": 1987, "吉首": 1982,
    "增城": 1993, "从化": 1994, "台山": 1992, "开平": 1993,
    "鹤山": 1993, "恩平": 1994, "四会": 1993, "兴宁": 1994,
    "乐昌": 1994, "南雄": 1996, "英德": 1994, "连州": 1994,
    "普宁": 1993, "罗定": 1993, "阳春": 1994, "信宜": 1995,
    "高州": 1993, "化州": 1994, "吴川": 1994, "雷州": 1994,
    "廉江": 1993, "岑溪": 1995, "东兴": 1996, "桂平": 1994,
    "北流": 1994, "容县": 1990, "陆川": 1997, "博白": 1998,
    "靖西": 2015, "平果": 2019, "荔浦": 2018, "凭祥": 1956,
    "文昌": 1995, "琼海": 1992, "万宁": 1996, "五指山": 1986,
    "东方": 1997, "都江堰": 1988, "彭州": 1993, "邛崃": 1994,
    "崇州": 1994, "简阳": 1994, "广汉": 1988, "什邡": 1995,
    "绵竹": 1996, "江油": 1988, "射洪": 2019, "隆昌": 2017,
    "峨眉山": 1988, "阆中": 1991, "华蓥": 1985, "万源": 1993,
    "西昌": 1979, "会理": 2021, "康定": 2015, "马尔康": 2015,
    "清镇": 1992, "赤水": 1990, "仁怀": 1995, "盘州": 2017,
    "兴义": 1987, "凯里": 1983, "都匀": 1966, "福泉": 1996,
    "安宁": 1995, "宣威": 1994, "腾冲": 2015, "瑞丽": 1992,
    "芒市": 1996, "景洪": 1993, "大理市": 1983, "楚雄市": 1983,
    "文山市": 2010, "蒙自": 2010, "弥勒": 2013, "个旧": 1951,
    "开远": 1981, "香格里拉": 2001, "泸水": 2016, "水富": 2018,
    "兴平": 1993, "彬州": 2018, "韩城": 1983, "华阴": 1990,
    "神木": 2017, "玉门": 1955, "敦煌": 1987, "临夏市": 1983,
    "合作": 1996, "同仁": 1992, "玉树市": 2013, "德令哈": 1988,
    "格尔木": 1980, "茫崖": 2018, "灵武": 1996, "青铜峡": 1984,
    "库尔勒": 1979, "阿克苏市": 1983, "喀什市": 1952, "和田市": 1983,
    "伊宁": 1952, "奎屯": 1975, "乌苏": 1996, "沙湾": 2019,
    "昌吉市": 1983, "阜康": 1992, "博乐": 1985, "阿拉山口": 2012,
    "阿勒泰市": 1984, "塔城市": 1984, "哈密市_": 1961, "吐鲁番市_": 1984,
}


def make_city(pid, name, level, code, curated=None):
    cur = curated or {}
    base = base_name(name)
    ctype = cur.get("type") or TYPE_OVERRIDES.get(base) or PROVINCE_DEFAULT_TYPE.get(pid, "传统农业劳务型")
    is_county = level == "county"

    if is_county and not cur:
        # 县级市默认跟随母地级市类型（在调用处已经通过 parent_type 传入则优先）
        ctype = PROVINCE_DEFAULT_TYPE.get(pid, "传统农业劳务型")

    weight = cur.get("popWeight")
    if weight is None:
        if level == "municipality":
            weight = 12
        elif is_county:
            weight = 1
        else:
            weight = 5 if base in MAJOR_CITY_WEIGHTS else 4
            if base in {"兴安", "锡林郭勒", "阿拉善", "阿里", "那曲", "果洛", "玉树", "海北", "黄南", "海南", "克孜勒苏", "和田"}:
                weight = 2
    if cur:
        weight = cur.get("popWeight", weight)

    founding = cur.get("foundingYear")
    pre_name = cur.get("historicalNamePre")
    if not cur:
        override = PRE_NAME_OVERRIDES.get(base) or PRE_NAME_OVERRIDES.get(name)
        if override:
            _, founding, pre_name = override
        elif is_county:
            founding = COUNTY_FOUNDING_OVERRIDES.get(base, 1985)
            pre_name = base + "县"
        else:
            founding = 1949
            pre_name = name

    archetype = ARCHETYPE_INDUSTRIES.get(ctype)
    if archetype is None:
        ctype = "传统农业劳务型"
        archetype = ARCHETYPE_INDUSTRIES[ctype]

    return {
        "id": cur.get("id") or "",
        "name": cur.get("name") or name,
        "shortName": short_name(cur.get("name") or name),
        "provinceId": pid,
        "region": cur.get("region", ""),
        "level": level,
        "type": ctype,
        "popWeight": weight,
        "foundingYear": founding if founding is not None else 1949,
        "historicalNamePre": pre_name or (cur.get("name") or name),
        "eraIndustries": cur.get("eraIndustries") or {
            "era_1937_1949": archetype["era_1937_1949"],
            "era_1950_1978": archetype["era_1950_1978"],
            "era_1979_2000": archetype["era_1979_2000"],
            "era_2001_2026": archetype["era_2001_2026"],
        },
        "riskModifiers": cur.get("riskModifiers") or archetype["riskModifiers"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefectures", required=True)
    ap.add_argument("--areas", required=True)
    ap.add_argument("--curated", required=True)
    ap.add_argument("--provinces", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.prefectures, encoding="utf-8") as f:
        prefectures = json.load(f)
    with open(args.areas, encoding="utf-8") as f:
        areas = json.load(f)
    with open(args.curated, encoding="utf-8") as f:
        curated = json.load(f)
    with open(args.provinces, encoding="utf-8") as f:
        provinces = json.load(f)

    province_by_id = {p["id"]: p for p in provinces}

    # 官方地级行政区索引（用于区分“喀什地区”与“喀什市”这类同名市县）
    pref_keys = set()
    pref_code_by_key = {}
    for p in prefectures:
        if p["name"] in SKIP_PREFECTURE_NAMES:
            continue
        pid = PROVINCE_BY_CODE.get(p["provinceCode"])
        if not pid:
            continue
        key = (pid, base_name(p["name"]))
        pref_keys.add(key)
        pref_code_by_key[key] = p["code"]

    # 手工城市按行政级别分别索引：大理州与大理市、喀什地区与喀什市不能互相覆盖。
    curated_by_key = {}
    curated_level = {}
    for c in curated:
        pid = c["provinceId"]
        base = base_name(c["name"])
        if pid in MUNICIPALITIES.values() and base == base_name(province_by_id[pid]["name"]):
            level = "municipality"
        elif "县级市" in c["name"]:
            level = "county"
        elif (pid, base) in pref_keys:
            level = "prefecture"
        else:
            level = "county"
        curated_level[id(c)] = level
        curated_by_key.setdefault((level, pid, base), c)

    curated_used = set()
    out = []

    # 1) 直辖市
    for code, pid in MUNICIPALITIES.items():
        prov = province_by_id[pid]
        key = ("municipality", pid, base_name(prov["name"]))
        cur = curated_by_key.get(key)
        city = make_city(pid, prov["name"], "municipality", code + "00", cur)
        city["id"] = cur["id"] if cur else pid
        city["region"] = prov.get("region", "")
        if cur:
            curated_used.add(id(cur))
        out.append(city)

    # 2) 地级行政区
    prefecture_by_code = {}
    prefecture_name_to_code = {}
    for p in prefectures:
        name = p["name"]
        if name in SKIP_PREFECTURE_NAMES:
            continue
        code = p["code"]
        pid = PROVINCE_BY_CODE.get(p["provinceCode"])
        if not pid:
            continue
        base = base_name(name)
        cur = curated_by_key.get(("prefecture", pid, base))
        city = make_city(pid, name, "prefecture", code, cur)
        city["id"] = (
            cur["id"] if cur
            else LEGACY_IDS.get((pid, "prefecture", base))
            or "cn_" + code
        )
        city["region"] = province_by_id[pid].get("region", "")
        city["parentCityId"] = None
        if cur:
            curated_used.add(id(cur))
        out.append(city)
        prefecture_by_code[code] = city
        prefecture_name_to_code[name] = code

    # 3) 县级市
    county_cities = [a for a in areas if a["name"].endswith("市")]
    for a in county_cities:
        pid = PROVINCE_BY_CODE.get(a["provinceCode"])
        if not pid:
            continue
        parent = prefecture_by_code.get(a.get("cityCode"))
        # 东莞/中山/儋州/嘉峪关等“不设区的地级市”也会出现在 areas.json 中；
        # 它们已经作为地级行政区收录，不能重复算作县级市。
        parent_clean = parent["name"].split("（")[0] if parent else ""
        if parent and parent_clean.endswith("市") and a["name"] == parent_clean:
            continue

        base = base_name(a["name"])
        cur = curated_by_key.get(("county", pid, base))
        if cur:
            ctype = cur.get("type")
        elif base in COUNTY_TYPE_OVERRIDES:
            ctype = COUNTY_TYPE_OVERRIDES[base]
        elif parent:
            ctype = COUNTY_TYPE_FROM_PARENT.get(parent["type"], parent["type"])
        else:
            ctype = PROVINCE_DEFAULT_TYPE.get(pid, "传统农业劳务型")

        city = make_city(pid, a["name"], "county", a["code"], cur)
        city["type"] = ctype
        # 产业模板跟随最终类型
        arch = ARCHETYPE_INDUSTRIES.get(ctype, ARCHETYPE_INDUSTRIES["传统农业劳务型"])
        if not cur:
            city["eraIndustries"] = {
                "era_1937_1949": arch["era_1937_1949"],
                "era_1950_1978": arch["era_1950_1978"],
                "era_1979_2000": arch["era_1979_2000"],
                "era_2001_2026": arch["era_2001_2026"],
            }
            city["riskModifiers"] = arch["riskModifiers"]
        city["id"] = cur["id"] if cur else "cn_" + a["code"]
        city["region"] = province_by_id[pid].get("region", "")
        city["parentCityId"] = parent["id"] if parent else None
        if cur:
            curated_used.add(id(cur))
        out.append(city)

    # 4) 保底：保留所有未匹配到官方列表的手工城市（例如兵团城市/特殊县级市）
    for c in curated:
        if id(c) in curated_used:
            continue
        pid = c["provinceId"]
        level = curated_level.get(id(c), "prefecture")
        city = make_city(pid, c["name"], level, "", c)
        city["id"] = c["id"]
        city["region"] = province_by_id.get(pid, {}).get("region", "")
        city["parentCityId"] = None
        out.append(city)

    # 5) 清理、排序、补全
    seen_ids = set()
    final = []
    for c in out:
        if not c["id"] or c["id"] in seen_ids:
            continue
        seen_ids.add(c["id"])
        if not c.get("region"):
            c["region"] = province_by_id.get(c["provinceId"], {}).get("region", "")
        final.append(c)

    level_order = {"municipality": 0, "prefecture": 1, "county": 2}
    province_order = {p["id"]: i for i, p in enumerate(provinces)}
    final.sort(key=lambda c: (province_order.get(c["provinceId"], 999), level_order.get(c["level"], 9), c["id"]))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    types = Counter(c["type"] for c in final)
    levels = Counter(c["level"] for c in final)
    print(f"✅ wrote {len(final)} cities -> {args.out}")
    print("levels:", dict(levels))
    print("types:", dict(types))
    missing = [c["id"] for c in final if c["type"] not in ARCHETYPE_INDUSTRIES]
    if missing:
        print("⚠️ missing archetypes:", missing[:10])


if __name__ == "__main__":
    main()
