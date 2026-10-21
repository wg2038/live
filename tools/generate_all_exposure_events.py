"""
全面构建《中国历史人生模拟》暴露 x 风险驱动事件库 (Three-Tier Exposure x Risk Event System)
严格遵循用户规范 1-10 条与 A、B、C、D、E 五大分类
"""

import json
import os

events = []

def make_outcome(outcome_type, weight, log, effect=None, is_fatal=False, status=None, hidden_risk_log="", new_career_track=None):
    res = {
        "type": outcome_type,  # safe, injured, entangled, redirected, fatal
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

def add_event(
    evt_id, tier, title, year_range, target_age, regions,
    exposure, pre_tags, trigger_prob, fact_level,
    historical_fact, narrative, choices
):
    events.append({
        "id": evt_id,
        "tier": tier,
        "title": title,
        "yearRange": year_range,
        "targetAge": target_age,
        "applicableRegions": regions,
        "exposureConditions": exposure,
        "preTags": pre_tags,
        "triggerProbability": trigger_prob,
        "factLevel": fact_level,
        "historicalFact": historical_fact,
        "narrative": narrative,
        "isDecision": True,
        "choices": choices
    })

print("Helper ready...")
