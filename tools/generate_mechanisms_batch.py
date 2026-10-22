# -*- coding: utf-8 -*-
"""
批量生成并注入四大通用机制事件（覆盖5个年代，共80条高精度历史人生事件）：
机制A：路径一致性与补救通道 (Remedial Paths & Strict Preconditions)
机制B：选择不一定正确，伤害渐进 (Fallible Options & Progressive Harm)
机制C：经济系统与消费诱惑 (Economic Loop & Period Temptations)
机制D：亲友关系网与离别 (Social Net Dynamics & Restrained Farewells)
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data", "events")

def create_event(
    id, title, year_range, target_age, fact_level, hist_fact, narrative, choices,
    regions=None, exposure=None, pre_tags=None, exclude_tags=None,
    prob=0.06, cooling=8, tier="era"
):
    return {
        "id": id,
        "tier": tier,
        "title": title,
        "yearRange": year_range,
        "targetAge": target_age,
        "applicableRegions": regions or ["ALL"],
        "exposureConditions": exposure or {},
        "preTags": pre_tags or [],
        "excludeTags": exclude_tags or [],
        "triggerProbability": prob,
        "coolingPeriod": cooling,
        "factLevel": fact_level,
        "historicalFact": hist_fact,
        "narrative": narrative,
        "isDecision": True,
        "passiveImpact": None,
        "choices": choices
    }

print("Base generator helper initialized.")
