import json

events = []

# ==============================================================================
# Helper to build standard event
# ==============================================================================
def make_event(
    evt_id,
    tier,
    title,
    year_range,
    target_age,
    regions,
    exposure,
    pre_tags,
    trigger_prob,
    fact_level,
    historical_fact,
    narrative,
    choices
):
    return {
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
    }

print("Helper defined successfully")
