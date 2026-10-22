# -*- coding: utf-8 -*-
"""
将 5 个年代共 80 条四大机制新事件批量安全注入 data/events/ 对应文件
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools.batch_events.era_1937_1949 import get_events as g1
from tools.batch_events.era_1950_1977 import get_events as g2
from tools.batch_events.era_1978_1999 import get_events as g3
from tools.batch_events.era_2000_2015 import get_events as g4
from tools.batch_events.era_2016_2026 import get_events as g5

DATA_DIR = os.path.join(ROOT, "data", "events")

plan = [
    ("events_1937_1949.json", g1()),
    ("events_1950_1977.json", g2()),
    ("events_1978_1999.json", g3()),
    ("events_2000_2026.json", g4() + g5()),
]

total_injected = 0

for fname, new_evts in plan:
    fpath = os.path.join(DATA_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        existing = json.load(f)
    
    existing_ids = {e["id"] for e in existing}
    added = 0
    for evt in new_evts:
        if evt["id"] not in existing_ids:
            existing.append(evt)
            existing_ids.add(evt["id"])
            added += 1
            total_injected += 1
    
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    
    print(f"[{fname}] Injected {added} new events. Total now: {len(existing)}")

print(f"\nSuccessfully injected a total of {total_injected} new events.")
