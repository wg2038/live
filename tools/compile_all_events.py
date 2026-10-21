# tools/compile_all_events.py
# -*- coding: utf-8 -*-
"""
编译全量事件与离线嵌入包：
1. 聚合 data/events/*.json 全部事件 -> data/events.json
2. 整合 data/ 下所有数据文件生成 data/embedded.js，实现完全离线单页运行
"""

import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(root, "data")
events_dir = os.path.join(data_dir, "events")

all_events = []
seen_ids = set()

# 1. 扫描 data/events/*.json
for fname in sorted(os.listdir(events_dir)):
    if fname.endswith(".json"):
        fpath = os.path.join(events_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            chunk = json.load(f)
            print(f"Loading {fname}: {len(chunk)} events")
            for evt in chunk:
                eid = evt.get("id")
                if eid in seen_ids:
                    print(f"⚠️ Warning: Duplicate event ID '{eid}' in {fname}, skipping")
                    continue
                seen_ids.add(eid)
                all_events.append(evt)

print(f"\nTotal merged events: {len(all_events)}")

# 2. 写入 data/events.json
master_events_path = os.path.join(data_dir, "events.json")
with open(master_events_path, "w", encoding="utf-8") as f:
    json.dump(all_events, f, ensure_ascii=False, indent=2)
print(f"✅ Master events written to {master_events_path}")

# 3. 构造完整 EMBEDDED_DATA 对象
embedded_data = {}

# provinces
prov_path = os.path.join(data_dir, "province.json")
if os.path.exists(prov_path):
    with open(prov_path, "r", encoding="utf-8") as f:
        embedded_data["provinces"] = json.load(f)

# stats
stats_path = os.path.join(data_dir, "stats.json")
if os.path.exists(stats_path):
    with open(stats_path, "r", encoding="utf-8") as f:
        embedded_data["stats"] = json.load(f)

# cities
cities_path = os.path.join(data_dir, "cities.json")
if os.path.exists(cities_path):
    with open(cities_path, "r", encoding="utf-8") as f:
        embedded_data["cities"] = json.load(f)

# disasters
dis_path = os.path.join(data_dir, "disasters.json")
if os.path.exists(dis_path):
    with open(dis_path, "r", encoding="utf-8") as f:
        embedded_data["disasters"] = json.load(f)

# naming
naming_path = os.path.join(data_dir, "naming.json")
if os.path.exists(naming_path):
    with open(naming_path, "r", encoding="utf-8") as f:
        embedded_data["naming"] = json.load(f)

# transitions
trans_path = os.path.join(data_dir, "transitions.json")
if os.path.exists(trans_path):
    with open(trans_path, "r", encoding="utf-8") as f:
        embedded_data["transitions"] = json.load(f)

# details
details_path = os.path.join(data_dir, "details.json")
if os.path.exists(details_path):
    with open(details_path, "r", encoding="utf-8") as f:
        embedded_data["details"] = json.load(f)

# events
embedded_data["events"] = all_events

# 4. 写入 data/embedded.js (兼容浏览器全局挂载与 Node 模块导出)
embedded_js_path = os.path.join(data_dir, "embedded.js")
json_str = json.dumps(embedded_data, ensure_ascii=False)
js_content = f"""var EMBEDDED_DATA = {json_str};
if (typeof window !== 'undefined') {{ window.EMBEDDED_DATA = EMBEDDED_DATA; }}
if (typeof module !== 'undefined' && module.exports) {{ module.exports = EMBEDDED_DATA; }}
"""

with open(embedded_js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ Successfully bundled all game data into {embedded_js_path} (size: {len(js_content)/1024:.1f} KB)")
