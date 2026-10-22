# -*- coding: utf-8 -*-
"""
【历史脚本，已废弃】早期 149 城生成器，仅供追溯手工校准数据。

现行数据请用 tools/build_all_cities.py 生成（734 城）。
直接运行本脚本不会覆盖 data/cities.json，除非显式传入 --legacy。
"""

import json
import os
import sys

# 城市原型产业模板库
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from city_archetypes import ARCHETYPE_INDUSTRIES

CITIES_RAW = [
  # 1. 直辖市
  {"id": "beijing", "name": "北京市", "provinceId": "beijing", "region": "华北", "type": "综合科教中心", "popWeight": 22, "foundingYear": 1937, "preName": "北平市"},
  {"id": "tianjin", "name": "天津市", "provinceId": "tianjin", "region": "华北", "type": "沿海商贸外贸型", "popWeight": 14, "foundingYear": 1937, "preName": "天津市"},
  {"id": "shanghai", "name": "上海市", "provinceId": "shanghai", "region": "华东", "type": "沿海商贸外贸型", "popWeight": 25, "foundingYear": 1937, "preName": "上海特别市"},
  {"id": "chongqing", "name": "重庆市", "provinceId": "chongqing", "region": "西南", "type": "重工业资源型", "popWeight": 32, "foundingYear": 1997, "preName": "四川省重庆市"},

  # 2. 河北省 (含唐山、邢台、涿州等关键灾难与工业市县)
  {"id": "shijiazhuang", "name": "石家庄市", "provinceId": "hebei", "region": "华北", "type": "重工业资源型", "popWeight": 11, "foundingYear": 1947, "preName": "获鹿县石门镇"},
  {"id": "tangshan", "name": "唐山市", "provinceId": "hebei", "region": "华北", "type": "重工业资源型", "popWeight": 8, "foundingYear": 1938, "preName": "滦县唐山镇"},
  {"id": "handan", "name": "邯郸市", "provinceId": "hebei", "region": "华北", "type": "重工业资源型", "popWeight": 9, "foundingYear": 1952, "preName": "邯郸县"},
  {"id": "baoding", "name": "保定市", "provinceId": "hebei", "region": "华北", "type": "传统农业劳务型", "popWeight": 10, "foundingYear": 1948, "preName": "清苑县"},
  {"id": "xingtai", "name": "邢台市", "provinceId": "hebei", "region": "华北", "type": "传统农业劳务型", "popWeight": 7, "foundingYear": 1953, "preName": "邢台县"},
  {"id": "zhuozhou", "name": "涿州市（县级市）", "provinceId": "hebei", "region": "华北", "type": "沿海商贸外贸型", "popWeight": 4, "foundingYear": 1986, "preName": "涿县"},
  {"id": "cangzhou", "name": "沧州市", "provinceId": "hebei", "region": "华北", "type": "重工业资源型", "popWeight": 7, "foundingYear": 1961, "preName": "沧县"},
  {"id": "qinhuangdao", "name": "秦皇岛市", "provinceId": "hebei", "region": "华北", "type": "沿海商贸外贸型", "popWeight": 3, "foundingYear": 1948, "preName": "临榆县"},
  {"id": "zhangjiakou", "name": "张家口市", "provinceId": "hebei", "region": "华北", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1939, "preName": "万全县"},
  {"id": "chengde", "name": "承德市", "provinceId": "hebei", "region": "华北", "type": "重工业资源型", "popWeight": 3, "foundingYear": 1955, "preName": "热河承德县"},

  # 3. 山西省 (大同煤炭、长治三线)
  {"id": "taiyuan", "name": "太原市", "provinceId": "shanxi", "region": "华北", "type": "重工业资源型", "popWeight": 6, "foundingYear": 1947, "preName": "太原县"},
  {"id": "datong", "name": "大同市", "provinceId": "shanxi", "region": "华北", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1949, "preName": "大同县"},
  {"id": "yangquan", "name": "阳泉市", "provinceId": "shanxi", "region": "华北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1947, "preName": "平定县阳泉镇"},
  {"id": "changzhi", "name": "长治市", "provinceId": "shanxi", "region": "华北", "type": "三线军工型", "popWeight": 4, "foundingYear": 1945, "preName": "长治县"},
  {"id": "linfen", "name": "临汾市", "provinceId": "shanxi", "region": "华北", "type": "重工业资源型", "popWeight": 4, "foundingYear": 2000, "preName": "临汾地区"},
  {"id": "yuncheng", "name": "运城市", "provinceId": "shanxi", "region": "华北", "type": "传统农业劳务型", "popWeight": 5, "foundingYear": 2000, "preName": "运城专区"},

  # 4. 辽宁省 (鞍山钢都、抚顺煤都、本溪、北票资源枯竭)
  {"id": "shenyang", "name": "沈阳市", "provinceId": "liaoning", "region": "东北", "type": "重工业资源型", "popWeight": 9, "foundingYear": 1937, "preName": "奉天市"},
  {"id": "dalian", "name": "大连市", "provinceId": "liaoning", "region": "东北", "type": "沿海商贸外贸型", "popWeight": 7, "foundingYear": 1937, "preName": "大连市"},
  {"id": "anshan", "name": "鞍山市", "provinceId": "liaoning", "region": "东北", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1937, "preName": "辽阳县鞍山驿"},
  {"id": "fushun", "name": "抚顺市", "provinceId": "liaoning", "region": "东北", "type": "重工业资源型", "popWeight": 3, "foundingYear": 1937, "preName": "抚顺县"},
  {"id": "benxi", "name": "本溪市", "provinceId": "liaoning", "region": "东北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1939, "preName": "本溪县"},
  {"id": "fuxin", "name": "阜新市", "provinceId": "liaoning", "region": "东北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1940, "preName": "阜新县"},
  {"id": "beipiao", "name": "北票市（县级市）", "provinceId": "liaoning", "region": "东北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1985, "preName": "北票煤矿县"},
  {"id": "panjin", "name": "盘锦市", "provinceId": "liaoning", "region": "东北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1984, "preName": "辽河油田盘山县"},

  # 5. 黑龙江省 (大庆石油、大兴安岭林区、鹤岗煤炭)
  {"id": "harbin", "name": "哈尔滨市", "provinceId": "heilongjiang", "region": "东北", "type": "重工业资源型", "popWeight": 10, "foundingYear": 1937, "preName": "滨江省哈尔滨"},
  {"id": "qiqihar", "name": "齐齐哈尔市", "provinceId": "heilongjiang", "region": "东北", "type": "重工业资源型", "popWeight": 5, "foundingYear": 1936, "preName": "齐齐哈尔市"},
  {"id": "daqing", "name": "大庆市", "provinceId": "heilongjiang", "region": "东北", "type": "重工业资源型", "popWeight": 3, "foundingYear": 1979, "preName": "安达特区石油会战指挥部"},
  {"id": "hegang", "name": "鹤岗市", "provinceId": "heilongjiang", "region": "东北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1949, "preName": "鹤岗矿区汤原县"},
  {"id": "qitaihe", "name": "七台河市", "provinceId": "heilongjiang", "region": "东北", "type": "重工业资源型", "popWeight": 1, "foundingYear": 1983, "preName": "七台河煤矿特区"},
  {"id": "suihua", "name": "绥化市", "provinceId": "heilongjiang", "region": "东北", "type": "传统农业劳务型", "popWeight": 4, "foundingYear": 1999, "preName": "绥化专区黑土农区"},
  {"id": "daxinganling", "name": "大兴安岭地区（漠河/塔河）", "provinceId": "heilongjiang", "region": "东北", "type": "边陲农牧林业型", "popWeight": 1, "foundingYear": 1970, "preName": "呼玛县漠河林场"},

  # 6. 吉林省 (长春一汽、吉林化工、延边朝族)
  {"id": "changchun", "name": "长春市", "provinceId": "jilin", "region": "东北", "type": "重工业资源型", "popWeight": 9, "foundingYear": 1937, "preName": "新京特别市"},
  {"id": "jilin_city", "name": "吉林市", "provinceId": "jilin", "region": "东北", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1936, "preName": "吉林省城"},
  {"id": "yanbian", "name": "延边朝鲜族自治州", "provinceId": "jilin", "region": "东北", "type": "边陲农牧林业型", "popWeight": 3, "foundingYear": 1952, "preName": "延吉专区"},

  # 7. 江苏省 (苏南模式苏州无锡昆山，苏北徐州淮安)
  {"id": "nanjing", "name": "南京市", "provinceId": "jiangsu", "region": "华东", "type": "综合科教中心", "popWeight": 10, "foundingYear": 1937, "preName": "首都南京"},
  {"id": "suzhou", "name": "苏州市", "provinceId": "jiangsu", "region": "华东", "type": "民营轻工集群型", "popWeight": 13, "foundingYear": 1949, "preName": "吴县"},
  {"id": "kunshan", "name": "昆山市（县级市）", "provinceId": "jiangsu", "region": "华东", "type": "沿海商贸外贸型", "popWeight": 4, "foundingYear": 1989, "preName": "昆山县"},
  {"id": "wuxi", "name": "无锡市", "provinceId": "jiangsu", "region": "华东", "type": "民营轻工集群型", "popWeight": 8, "foundingYear": 1949, "preName": "无锡县"},
  {"id": "jiangyin", "name": "江阴市（县级市）", "provinceId": "jiangsu", "region": "华东", "type": "民营轻工集群型", "popWeight": 4, "foundingYear": 1987, "preName": "江阴县华西村"},
  {"id": "xuzhou", "name": "徐州市", "provinceId": "jiangsu", "region": "华东", "type": "重工业资源型", "popWeight": 9, "foundingYear": 1945, "preName": "铜山县徐州城"},
  {"id": "nantong", "name": "南通市", "provinceId": "jiangsu", "region": "华东", "type": "民营轻工集群型", "popWeight": 8, "foundingYear": 1949, "preName": "南通县纺织之乡"},
  {"id": "huaian", "name": "淮安市", "provinceId": "jiangsu", "region": "华东", "type": "传统农业劳务型", "popWeight": 5, "foundingYear": 1983, "preName": "淮阴地区清江市"},
  {"id": "yangzhou", "name": "扬州市", "provinceId": "jiangsu", "region": "华东", "type": "民营轻工集群型", "popWeight": 5, "foundingYear": 1949, "preName": "江都县扬州城"},

  # 8. 浙江省 (温州模式、义乌小商品、诸暨珍珠)
  {"id": "hangzhou", "name": "杭州市", "provinceId": "zhejiang", "region": "华东", "type": "综合科教中心", "popWeight": 12, "foundingYear": 1937, "preName": "杭县杭州城"},
  {"id": "ningbo", "name": "宁波市", "provinceId": "zhejiang", "region": "华东", "type": "沿海商贸外贸型", "popWeight": 10, "foundingYear": 1949, "preName": "鄞县宁波府"},
  {"id": "wenzhou", "name": "温州市", "provinceId": "zhejiang", "region": "华东", "type": "民营轻工集群型", "popWeight": 10, "foundingYear": 1949, "preName": "永嘉县温州街"},
  {"id": "jinhua", "name": "金华市", "provinceId": "zhejiang", "region": "华东", "type": "民营轻工集群型", "popWeight": 7, "foundingYear": 1985, "preName": "金华地区"},
  {"id": "yiwu", "name": "义乌市（县级市）", "provinceId": "zhejiang", "region": "华东", "type": "民营轻工集群型", "popWeight": 5, "foundingYear": 1988, "preName": "义乌县稠城镇"},
  {"id": "taizhou", "name": "台州市", "provinceId": "zhejiang", "region": "华东", "type": "民营轻工集群型", "popWeight": 6, "foundingYear": 1994, "preName": "台州地区临海市"},
  {"id": "shaoxing", "name": "绍兴市", "provinceId": "zhejiang", "region": "华东", "type": "民营轻工集群型", "popWeight": 5, "foundingYear": 1983, "preName": "绍兴县"},

  # 9. 安徽省 (凤阳小岗村、阜阳劳务大市、合肥新锐)
  {"id": "hefei", "name": "合肥市", "provinceId": "anhui", "region": "华东", "type": "综合科教中心", "popWeight": 9, "foundingYear": 1949, "preName": "合肥县庐州城"},
  {"id": "wuhu", "name": "芜湖市", "provinceId": "anhui", "region": "华东", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1949, "preName": "芜湖县米市"},
  {"id": "fuyang", "name": "阜阳市", "provinceId": "anhui", "region": "华东", "type": "传统农业劳务型", "popWeight": 9, "foundingYear": 1996, "preName": "阜阳地区颍州"},
  {"id": "bengbu", "name": "蚌埠市", "provinceId": "anhui", "region": "华东", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1947, "preName": "怀远县蚌埠镇"},
  {"id": "chuzhou", "name": "滁州市（凤阳小岗）", "provinceId": "anhui", "region": "华东", "type": "传统农业劳务型", "popWeight": 4, "foundingYear": 1992, "preName": "滁县地区凤阳县"},
  {"id": "huainan", "name": "淮南市", "provinceId": "anhui", "region": "华东", "type": "重工业资源型", "popWeight": 3, "foundingYear": 1952, "preName": "淮南矿区九龙岗"},
  {"id": "huaibei", "name": "淮北市", "provinceId": "anhui", "region": "华东", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1960, "preName": "濉溪煤矿矿区"},

  # 10. 福建省 (晋江鞋服、厦门特区、福州侨乡)
  {"id": "fuzhou", "name": "福州市", "provinceId": "fujian", "region": "华东", "type": "综合科教中心", "popWeight": 8, "foundingYear": 1946, "preName": "闽侯县福州城"},
  {"id": "xiamen", "name": "厦门市", "provinceId": "fujian", "region": "华东", "type": "沿海商贸外贸型", "popWeight": 5, "foundingYear": 1937, "preName": "思明县厦门港"},
  {"id": "quanzhou", "name": "泉州市", "provinceId": "fujian", "region": "华东", "type": "民营轻工集群型", "popWeight": 9, "foundingYear": 1985, "preName": "晋江地区泉州刺桐"},
  {"id": "jinjiang", "name": "晋江市（县级市）", "provinceId": "fujian", "region": "华东", "type": "民营轻工集群型", "popWeight": 5, "foundingYear": 1992, "preName": "晋江县陈埭镇"},

  # 11. 江西省 (景德镇瓷都、九江抗洪大堤、萍乡煤矿)
  {"id": "nanchang", "name": "南昌市", "provinceId": "jiangxi", "region": "华东", "type": "综合科教中心", "popWeight": 7, "foundingYear": 1937, "preName": "南昌县省城"},
  {"id": "ganzhou", "name": "赣州市", "provinceId": "jiangxi", "region": "华东", "type": "重工业资源型", "popWeight": 9, "foundingYear": 1999, "preName": "赣州地区稀土钨都"},
  {"id": "jiujiang", "name": "九江市", "provinceId": "jiangxi", "region": "华东", "type": "传统农业劳务型", "popWeight": 5, "foundingYear": 1980, "preName": "九江地区簰洲湾"},
  {"id": "pingxiang", "name": "萍乡市", "provinceId": "jiangxi", "region": "华东", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1960, "preName": "安源煤矿萍乡县"},

  # 12. 山东省 (青岛外贸、寿光蔬菜、曹县电商木雕、淄博工业)
  {"id": "jinan", "name": "济南市", "provinceId": "shandong", "region": "华东", "type": "综合科教中心", "popWeight": 10, "foundingYear": 1937, "preName": "历城县省城"},
  {"id": "qingdao", "name": "青岛市", "provinceId": "shandong", "region": "华东", "type": "沿海商贸外贸型", "popWeight": 11, "foundingYear": 1937, "preName": "青岛特别市"},
  {"id": "weifang", "name": "潍坊市（寿光蔬菜）", "provinceId": "shandong", "region": "华东", "type": "民营轻工集群型", "popWeight": 10, "foundingYear": 1948, "preName": "潍县寿光"},
  {"id": "linyi", "name": "临沂市", "provinceId": "shandong", "region": "华东", "type": "民营轻工集群型", "popWeight": 11, "foundingYear": 1994, "preName": "临沂地区沂蒙山"},
  {"id": "heze", "name": "菏泽市（曹县电商）", "provinceId": "shandong", "region": "华东", "type": "民营轻工集群型", "popWeight": 9, "foundingYear": 2000, "preName": "菏泽专区曹县"},
  {"id": "zibo", "name": "淄博市", "provinceId": "shandong", "region": "华东", "type": "重工业资源型", "popWeight": 5, "foundingYear": 1954, "preName": "淄川博山工矿特区"},
  {"id": "yantai", "name": "烟台市", "provinceId": "shandong", "region": "华东", "type": "沿海商贸外贸型", "popWeight": 7, "foundingYear": 1950, "preName": "芝罘特区"},

  # 13. 河南省 (郑州7·20、驻马店75·8溃坝、周口黄泛区、洛阳老工矿)
  {"id": "zhengzhou", "name": "郑州市", "provinceId": "henan", "region": "华中", "type": "综合科教中心", "popWeight": 12, "foundingYear": 1948, "preName": "郑县铁路枢纽"},
  {"id": "luoyang", "name": "洛阳市", "provinceId": "henan", "region": "华中", "type": "重工业资源型", "popWeight": 7, "foundingYear": 1954, "preName": "洛阳县一拖矿山"},
  {"id": "nanyang", "name": "南阳市", "provinceId": "henan", "region": "华中", "type": "传统农业劳务型", "popWeight": 10, "foundingYear": 1994, "preName": "南阳专区宛城"},
  {"id": "zhoukou", "name": "周口市（原黄泛区中心）", "provinceId": "henan", "region": "华中", "type": "传统农业劳务型", "popWeight": 9, "foundingYear": 2000, "preName": "周口专区商水淮阳"},
  {"id": "zhumadian", "name": "驻马店市（75·8板桥溃坝地）", "provinceId": "henan", "region": "华中", "type": "传统农业劳务型", "popWeight": 7, "foundingYear": 2000, "preName": "驻马店专区遂平泌阳"},
  {"id": "shangqiu", "name": "商丘市", "provinceId": "henan", "region": "华中", "type": "传统农业劳务型", "popWeight": 8, "foundingYear": 1997, "preName": "商丘专区睢阳"},
  {"id": "xinxiang", "name": "新乡市", "provinceId": "henan", "region": "华中", "type": "重工业资源型", "popWeight": 6, "foundingYear": 1949, "preName": "新乡县平原省会"},
  {"id": "pingdingshan", "name": "平顶山市", "provinceId": "henan", "region": "华中", "type": "重工业资源型", "popWeight": 5, "foundingYear": 1957, "preName": "平顶山煤矿特区"},
  {"id": "kaifeng", "name": "开封市", "provinceId": "henan", "region": "华中", "type": "传统农业劳务型", "popWeight": 5, "foundingYear": 1937, "preName": "开封省城"},

  # 14. 湖北省 (武汉长江大水、十堰二汽三线、仙桃无纺布)
  {"id": "wuhan", "name": "武汉市", "provinceId": "hubei", "region": "华中", "type": "综合科教中心", "popWeight": 13, "foundingYear": 1949, "preName": "汉口汉阳武昌三镇"},
  {"id": "shiyan", "name": "十堰市（二汽卡车三线）", "provinceId": "hubei", "region": "华中", "type": "三线军工型", "popWeight": 4, "foundingYear": 1969, "preName": "郧县十堰公社"},
  {"id": "xiangyang", "name": "襄阳市", "provinceId": "hubei", "region": "华中", "type": "重工业资源型", "popWeight": 6, "foundingYear": 1951, "preName": "襄樊市襄阳县"},
  {"id": "yichang", "name": "宜昌市（三峡葛洲坝）", "provinceId": "hubei", "region": "华中", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1949, "preName": "宜昌县峡江要塞"},
  {"id": "jingzhou", "name": "荆州市（洪湖抗洪）", "provinceId": "hubei", "region": "华中", "type": "传统农业劳务型", "popWeight": 6, "foundingYear": 1994, "preName": "荆州专区沙市"},
  {"id": "xiantao", "name": "仙桃市（县级市）", "provinceId": "hubei", "region": "华中", "type": "民营轻工集群型", "popWeight": 3, "foundingYear": 1986, "preName": "沔阳县"},

  # 15. 湖南省 (郴州雪灾、株洲重机电、湘潭)
  {"id": "changsha", "name": "长沙市", "provinceId": "hunan", "region": "华中", "type": "综合科教中心", "popWeight": 10, "foundingYear": 1937, "preName": "长沙县文夕大火城"},
  {"id": "chenzhou", "name": "郴州市（08冰灾断电重灾区）", "provinceId": "hunan", "region": "华中", "type": "重工业资源型", "popWeight": 5, "foundingYear": 1995, "preName": "郴州地区南岭隘口"},
  {"id": "zhuzhou", "name": "株洲市", "provinceId": "hunan", "region": "华中", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1951, "preName": "湘潭县株洲镇电力机车"},
  {"id": "hengyang", "name": "衡阳市", "provinceId": "hunan", "region": "华中", "type": "重工业资源型", "popWeight": 7, "foundingYear": 1942, "preName": "衡阳县衡阳保卫战"},
  {"id": "yueyang", "name": "岳阳市（八百里洞庭防汛）", "provinceId": "hunan", "region": "华中", "type": "传统农业劳务型", "popWeight": 6, "foundingYear": 1983, "preName": "岳阳地区城陵矶"},

  # 16. 广东省 (深圳特区、东莞世界工厂、佛山顺德家电、贵屿电子垃圾拆解)
  {"id": "guangzhou", "name": "广州市", "provinceId": "guangdong", "region": "华南", "type": "综合科教中心", "popWeight": 19, "foundingYear": 1937, "preName": "广州特别市"},
  {"id": "shenzhen", "name": "深圳市（特区前沿）", "provinceId": "guangdong", "region": "华南", "type": "沿海商贸外贸型", "popWeight": 18, "foundingYear": 1979, "preName": "惠阳地区宝安县"},
  {"id": "dongguan", "name": "东莞市（世界制造业之都）", "provinceId": "guangdong", "region": "华南", "type": "沿海商贸外贸型", "popWeight": 11, "foundingYear": 1985, "preName": "东莞县虎门太平"},
  {"id": "foshan", "name": "佛山市（顺德家电/南海五金）", "provinceId": "guangdong", "region": "华南", "type": "民营轻工集群型", "popWeight": 10, "foundingYear": 1951, "preName": "南海县佛山镇"},
  {"id": "shantou_guiyu", "name": "汕头市（潮阳贵屿电子垃圾拆解）", "provinceId": "guangdong", "region": "华南", "type": "民营轻工集群型", "popWeight": 6, "foundingYear": 1937, "preName": "潮阳县贵屿酸洗镇"},
  {"id": "zhanjiang", "name": "湛江市", "provinceId": "guangdong", "region": "华南", "type": "沿海商贸外贸型", "popWeight": 7, "foundingYear": 1945, "preName": "广州湾租借地"},
  {"id": "maoming", "name": "茂名市", "provinceId": "guangdong", "region": "华南", "type": "重工业资源型", "popWeight": 6, "foundingYear": 1959, "preName": "茂名油页岩工矿区"},

  # 17. 广西壮族自治区 (柳州工业汽轧、桂林文旅、百色铝业)
  {"id": "nanning", "name": "南宁市", "provinceId": "guangxi", "region": "华南", "type": "综合科教中心", "popWeight": 9, "foundingYear": 1949, "preName": "邕宁县南宁城"},
  {"id": "liuzhou", "name": "柳州市（柳钢五菱神车）", "provinceId": "guangxi", "region": "华南", "type": "重工业资源型", "popWeight": 5, "foundingYear": 1946, "preName": "柳江县柳州城"},
  {"id": "guilin", "name": "桂林市", "provinceId": "guangxi", "region": "华南", "type": "沿海商贸外贸型", "popWeight": 5, "foundingYear": 1940, "preName": "临桂县省城桂林"},

  # 18. 海南省 (天涯海角、农垦热带胶园)
  {"id": "haikou", "name": "海口市", "provinceId": "hainan", "region": "华南", "type": "沿海商贸外贸型", "popWeight": 3, "foundingYear": 1950, "preName": "琼山县海口所"},
  {"id": "sanya", "name": "三亚市", "provinceId": "hainan", "region": "华南", "type": "沿海商贸外贸型", "popWeight": 1, "foundingYear": 1984, "preName": "崖县南端渔村"},

  # 19. 四川省 (汶川地震核心区、攀枝花钢城、绵阳科技城、石棉县)
  {"id": "chengdu", "name": "成都市", "provinceId": "sichuan", "region": "西南", "type": "综合科教中心", "popWeight": 21, "foundingYear": 1937, "preName": "成都县省城"},
  {"id": "panzhihua", "name": "攀枝花市（大三线攀钢渡口）", "provinceId": "sichuan", "region": "西南", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1965, "preName": "盐边盐源渡口公社"},
  {"id": "mianyang", "name": "绵阳市（两弹一星国防科技）", "provinceId": "sichuan", "region": "西南", "type": "三线军工型", "popWeight": 5, "foundingYear": 1976, "preName": "绵阳县安县北川"},
  {"id": "aba_wenchuan", "name": "阿坝藏族羌族自治州（汶川县）", "provinceId": "sichuan", "region": "西南", "type": "边陲农牧林业型", "popWeight": 1, "foundingYear": 1953, "preName": "汶川县映秀镇"},
  {"id": "ya_an_shimian", "name": "雅安市（石棉县石棉矿）", "provinceId": "sichuan", "region": "西南", "type": "重工业资源型", "popWeight": 2, "foundingYear": 2000, "preName": "石棉县大渡河矿工区"},
  {"id": "leshan_jinkouhe", "name": "乐山市（金口河绝密核原料）", "provinceId": "sichuan", "region": "西南", "type": "三线军工型", "popWeight": 3, "foundingYear": 1985, "preName": "峨边县金口河三线区"},
  {"id": "nanchong", "name": "南充市", "provinceId": "sichuan", "region": "西南", "type": "传统农业劳务型", "popWeight": 6, "foundingYear": 1950, "preName": "南充专区川北行署"},
  {"id": "yibin", "name": "宜宾市（五粮液万里长江第一城）", "provinceId": "sichuan", "region": "西南", "type": "重工业资源型", "popWeight": 5, "foundingYear": 1951, "preName": "宜宾县叙府"},

  # 20. 贵州省 (万山汞矿、六盘水江南煤海、遵义)
  {"id": "guiyang", "name": "贵阳市（三线铝业与大数据）", "provinceId": "guizhou", "region": "西南", "type": "综合科教中心", "popWeight": 6, "foundingYear": 1941, "preName": "贵筑县省城"},
  {"id": "liupanshui", "name": "六盘水市（江南煤都）", "provinceId": "guizhou", "region": "西南", "type": "重工业资源型", "popWeight": 3, "foundingYear": 1978, "preName": "六枝盘县水城煤矿特区"},
  {"id": "tongren_wanshan", "name": "铜仁市（万山特区汞矿）", "provinceId": "guizhou", "region": "西南", "type": "重工业资源型", "popWeight": 3, "foundingYear": 2011, "preName": "万山特区汞矿开采区"},
  {"id": "zunyi", "name": "遵义市（转折之地与茅台）", "provinceId": "guizhou", "region": "西南", "type": "重工业资源型", "popWeight": 7, "foundingYear": 1950, "preName": "遵义县仁怀茅台镇"},

  # 21. 云南省 (个旧锡都、红河、通海地震带、昆明)
  {"id": "kunming", "name": "昆明市", "provinceId": "yunnan", "region": "西南", "type": "综合科教中心", "popWeight": 9, "foundingYear": 1937, "preName": "昆明县春城"},
  {"id": "honghe_gejiu", "name": "红河州（个旧市世界锡都）", "provinceId": "yunnan", "region": "西南", "type": "重工业资源型", "popWeight": 5, "foundingYear": 1951, "preName": "个旧锡矿采矿专区"},
  {"id": "yuxi_tonghai", "name": "玉溪市（通海县通海大地震）", "provinceId": "yunnan", "region": "西南", "type": "传统农业劳务型", "popWeight": 3, "foundingYear": 1997, "preName": "玉溪专区通海峨山"},

  # 22. 西藏自治区
  {"id": "lasa", "name": "拉萨市", "provinceId": "xizang", "region": "西南", "type": "边陲农牧林业型", "popWeight": 1, "foundingYear": 1960, "preName": "日光圣城拉萨"},
  {"id": "rikaze", "name": "日喀则市", "provinceId": "xizang", "region": "西南", "type": "边陲农牧林业型", "popWeight": 1, "foundingYear": 2014, "preName": "后藏日喀则宗"},

  # 23. 陕西省 (西安军工科教、宝鸡凤县三线、延安、榆林能源)
  {"id": "xi_an", "name": "西安市", "provinceId": "shaanxi", "region": "西北", "type": "综合科教中心", "popWeight": 13, "foundingYear": 1943, "preName": "长安县西京筹备市"},
  {"id": "baoji_fengxian", "name": "宝鸡市（凤县秦岭航天三线）", "provinceId": "shaanxi", "region": "西北", "type": "三线军工型", "popWeight": 4, "foundingYear": 1949, "preName": "宝鸡县凤县秦岭大山"},
  {"id": "hanzhong", "name": "汉中市（陕飞运八大三线）", "provinceId": "shaanxi", "region": "西北", "type": "三线军工型", "popWeight": 4, "foundingYear": 1996, "preName": "汉中地区城固三线"},
  {"id": "yan_an", "name": "延安市（革命圣地与石油延长）", "provinceId": "shaanxi", "region": "西北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1972, "preName": "肤施县延安边区"},
  {"id": "yulin", "name": "榆林市（神府煤田能源新都）", "provinceId": "shaanxi", "region": "西北", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1999, "preName": "榆林地区神木府谷"},

  # 24. 甘肃省 (兰州石化、舟曲泥石流、通渭会宁苦瘠甲天下、玉门石油)
  {"id": "lanzhou", "name": "兰州市", "provinceId": "gansu", "region": "西北", "type": "重工业资源型", "popWeight": 4, "foundingYear": 1941, "preName": "皋兰县兰州城"},
  {"id": "dingxi_tongwei", "name": "定西市（通渭/会宁苦瘠甲天下）", "provinceId": "gansu", "region": "西北", "type": "贫瘠特困型", "popWeight": 3, "foundingYear": 2003, "preName": "定西地区通渭旱塬"},
  {"id": "gannan_zhouqu", "name": "甘南州（舟曲泥石流重灾区）", "provinceId": "gansu", "region": "西北", "type": "贫瘠特困型", "popWeight": 1, "foundingYear": 1953, "preName": "舟曲藏族大石峡"},
  {"id": "jiuquan_yumen", "name": "酒泉市（玉门铁人王进喜摇篮）", "provinceId": "gansu", "region": "西北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 2002, "preName": "玉门老君庙石油局"},
  {"id": "baiyin", "name": "白银市（有色金属铜城）", "provinceId": "gansu", "region": "西北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 1958, "preName": "白银矿山采选区"},

  # 25. 青海省 (玉树地震、西宁、海西格尔木柴达木)
  {"id": "xining", "name": "西宁市", "provinceId": "qinghai", "region": "西北", "type": "重工业资源型", "popWeight": 3, "foundingYear": 1944, "preName": "湟中县西宁城"},
  {"id": "yushu", "name": "玉树藏族自治州（结古镇地震区）", "provinceId": "qinghai", "region": "西北", "type": "边陲农牧林业型", "popWeight": 1, "foundingYear": 1951, "preName": "玉树结古千户区"},
  {"id": "haixi_geermu", "name": "海西州（格尔木盐湖戈壁）", "provinceId": "qinghai", "region": "西北", "type": "重工业资源型", "popWeight": 1, "foundingYear": 1954, "preName": "青藏公路兵站格尔木"},

  # 26. 宁夏回族自治区 (固原西海固贫困、石嘴山煤矿、银川)
  {"id": "yinchuan", "name": "银川市", "provinceId": "ningxia", "region": "西北", "type": "综合科教中心", "popWeight": 3, "foundingYear": 1944, "preName": "宁夏省城宁朔"},
  {"id": "guyuan_xiji", "name": "固原市（西吉西海固贫瘠极地）", "provinceId": "ningxia", "region": "西北", "type": "贫瘠特困型", "popWeight": 2, "foundingYear": 2001, "preName": "固原专区西海固旱山"},
  {"id": "shizuishan", "name": "石嘴山市", "provinceId": "ningxia", "region": "西北", "type": "重工业资源型", "popWeight": 1, "foundingYear": 1960, "preName": "石嘴山大武口矿区"},

  # 27. 新疆维吾尔自治区 (克拉玛依石油、石河子兵团屯垦、喀什)
  {"id": "wulumuqi", "name": "乌鲁木齐市", "provinceId": "xinjiang", "region": "西北", "type": "综合科教中心", "popWeight": 4, "foundingYear": 1945, "preName": "迪化市"},
  {"id": "kelamayi", "name": "克拉玛依市（黑油山新中国第一大油田）", "provinceId": "xinjiang", "region": "西北", "type": "重工业资源型", "popWeight": 1, "foundingYear": 1958, "preName": "克拉玛依荒漠戈壁油矿"},
  {"id": "shihezi", "name": "石河子市（兵团屯垦第一城）", "provinceId": "xinjiang", "region": "西北", "type": "边陲农牧林业型", "popWeight": 1, "foundingYear": 1976, "preName": "新疆农八师石河子芦苇荒原"},
  {"id": "kashi", "name": "喀什地区", "provinceId": "xinjiang", "region": "西北", "type": "边陲农牧林业型", "popWeight": 4, "foundingYear": 1952, "preName": "疏勒喀什噶尔绿洲"},

  # 28. 内蒙古自治区 (包头包钢、呼伦贝尔、鄂尔多斯煤海)
  {"id": "huhehaote", "name": "呼和浩特市", "provinceId": "neimenggu", "region": "华北", "type": "综合科教中心", "popWeight": 3, "foundingYear": 1954, "preName": "绥远省归绥市"},
  {"id": "baotou", "name": "包头市（草原钢城与稀土高岭）", "provinceId": "neimenggu", "region": "华北", "type": "重工业资源型", "popWeight": 3, "foundingYear": 1950, "preName": "包头县昆都仑水草滩"},
  {"id": "eerduosi", "name": "鄂尔多斯市（羊煤土气暴富逆袭）", "provinceId": "neimenggu", "region": "华北", "type": "重工业资源型", "popWeight": 2, "foundingYear": 2001, "preName": "伊克昭盟东胜"},
  {"id": "hulunbeier", "name": "呼伦贝尔市（满洲里/额尔古纳大草原）", "provinceId": "neimenggu", "region": "华北", "type": "边陲农牧林业型", "popWeight": 2, "foundingYear": 2001, "preName": "呼伦贝尔盟海拉尔"}
]

# 为每个城市附加完整的四大时期产业结构轨迹与风险系数
ALL_CITIES_PROCESSED = []
for c in CITIES_RAW:
  arch = ARCHETYPE_INDUSTRIES.get(c["type"], ARCHETYPE_INDUSTRIES["传统农业劳务型"])
  city_entry = {
    "id": c["id"],
    "name": c["name"],
    "provinceId": c["provinceId"],
    "region": c["region"],
    "type": c["type"],
    "popWeight": c["popWeight"],
    "foundingYear": c["foundingYear"],
    "historicalNamePre": c["preName"],
    "eraIndustries": {
      "era_1937_1949": arch["era_1937_1949"],
      "era_1950_1978": arch["era_1950_1978"],
      "era_1979_2000": arch["era_1979_2000"],
      "era_2001_2026": arch["era_2001_2026"]
    },
    "riskModifiers": arch["riskModifiers"]
  }
  ALL_CITIES_PROCESSED.append(city_entry)

if '--legacy' in sys.argv:
  with open('data/cities.json', 'w', encoding='utf-8') as f:
    json.dump(ALL_CITIES_PROCESSED, f, ensure_ascii=False, indent=2)
  print("cities.json 生成完成，共精准收录", len(ALL_CITIES_PROCESSED), "个典型地级市与特色县级市！")
else:
  print("本脚本已废弃：当前全国城市数据请运行 python3 tools/build_all_cities.py")
  print("如确需重建旧版 149 城数据，请追加 --legacy（会覆盖 data/cities.json）。")
