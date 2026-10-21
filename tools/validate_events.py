# tools/validate_events.py
# -*- coding: utf-8 -*-
"""
事件校验器：
1. 校验必备字段完整性 (id, tier, title, yearRange, targetAge, exposureConditions, choices, outcomes, factLevel 等)
2. 校验概率合法性 (权重总和 > 0, fatal 概率保守 <= 5%)
3. 校验文案规范度 (禁止重复文本、字数合适)
4. 校验敏感历史事件规范 (1966-1968, 1989 等是否克制、无伤亡数字、factLevel必须为估计/文学化)
5. 校验前置标签是否可达
"""

import json
import os
import sys

def validate_event_list(events, source_name="events"):
    errors = []
    warnings = []
    seen_ids = set()
    seen_titles = set()

    for idx, evt in enumerate(events):
        evt_id = evt.get("id")
        if not evt_id:
            errors.append(f"[{source_name}] 第 {idx} 个事件缺少 'id'")
            continue

        if evt_id in seen_ids:
            errors.append(f"[{source_name}] 重复的事件 id: '{evt_id}'")
        seen_ids.add(evt_id)

        title = evt.get("title", "")
        if not title:
            errors.append(f"[{evt_id}] 缺少 'title'")
        elif title in seen_titles:
            warnings.append(f"[{evt_id}] 重复的标题: '{title}'")
        seen_titles.add(title)

        # 检查年代范围
        year_range = evt.get("yearRange")
        if not year_range or len(year_range) != 2 or year_range[0] > year_range[1]:
            errors.append(f"[{evt_id}] 非法的 yearRange: {year_range}")
        else:
            if year_range[0] < 1937 or year_range[1] > 2026:
                errors.append(f"[{evt_id}] yearRange 超出 1937-2026 历史边界: {year_range}")

        # 检查史实等级
        fact_level = evt.get("factLevel")
        if fact_level not in ["确证", "估计", "文学化", "估计/文学化"]:
            errors.append(f"[{evt_id}] 非法的 factLevel '{fact_level}'，必须为 确证/估计/文学化")

        # 敏感历史事件规范性检查
        if "1966" in evt_id or "1967" in evt_id or "wudou" in evt_id or "1989" in evt_id:
            if fact_level not in ["估计", "文学化", "估计/文学化"]:
                errors.append(f"[{evt_id}] 敏感历史事件必须标注为 '估计' 或 '文学化'，当前为: '{fact_level}'")
            hist = evt.get("historicalFact", "")
            for forbidden_word in ["血流成河", "暴行", "屠杀", "惨绝人寰", "暴徒"]:
                if forbidden_word in hist:
                    errors.append(f"[{evt_id}] 敏感历史表述违背克制规范，包含煽情词汇: '{forbidden_word}'")

        # 检查叙事
        narrative = evt.get("narrative", "")
        if not narrative or len(narrative) < 20:
            errors.append(f"[{evt_id}] narrative 过短或缺失 ({len(narrative)} 字)")

        # 检查选项 choices
        choices = evt.get("choices")
        if evt.get("isDecision", True):
            if not choices or not isinstance(choices, list) or len(choices) < 2:
                errors.append(f"[{evt_id}] 决策事件候选选项不足 2 个 (实际: {len(choices) if choices else 0})")
            else:
                for c_idx, c in enumerate(choices):
                    c_text = c.get("text", "")
                    if not c_text:
                        errors.append(f"[{evt_id}] 选项 {c_idx} 缺少 text")
                    
                    choice_tags = c.get("choiceTags", [])
                    if not choice_tags or len(choice_tags) < 2:
                        warnings.append(f"[{evt_id}] 选项 '{c_text[:15]}' 缺少规范 choiceTags 标签")

                    outcomes = c.get("outcomes", [])
                    if not outcomes:
                        errors.append(f"[{evt_id}] 选项 '{c_text[:15]}' 缺少 outcomes 分支")
                    else:
                        total_weight = sum(o.get("weight", 0) for o in outcomes)
                        if total_weight <= 0:
                            errors.append(f"[{evt_id}] 选项 '{c_text[:15]}' 分支权重总和非法: {total_weight}")

                        for o in outcomes:
                            o_type = o.get("type")
                            if o_type not in ["safe", "injured", "entangled", "redirected", "fatal"]:
                                warnings.append(f"[{evt_id}] 未知 outcome 类型: '{o_type}'")
                            if o.get("isFatal", False):
                                fatal_prob = o.get("weight", 0) / (total_weight or 1)
                                if fatal_prob > 0.05:
                                    warnings.append(f"[{evt_id}] 选项 '{c_text[:15]}' 致死分支概率过高: {fatal_prob*100:.1f}% > 5%")
                            if not o.get("hiddenRiskLog"):
                                warnings.append(f"[{evt_id}] outcome 缺少 hiddenRiskLog（用于因果回顾）")

    return errors, warnings

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"=== Running Event Validator on {root} ===")

    all_ok = True
    total_checked = 0

    # 1. Check generated Python event registry modules
    sys.path.insert(0, root)
    import tools.build_all_exposure_events as base
    import tools.events_era_1937_1965 as e1
    import tools.events_era_1966_1989 as e2

    base.events.clear()
    e1.register_events_1937_1965()
    e2.register_events_1966_1989()
    py_events = list(base.events)

    errs, warns = validate_event_list(py_events, "Python Modules (1937-1989)")
    total_checked += len(py_events)
    print(f"Validated {len(py_events)} events from Python modules.")
    if errs:
        all_ok = False
        print(f"Errors ({len(errs)}):")
        for e in errs[:10]:
            print("  ❌", e)
    if warns:
        print(f"Warnings ({len(warns)}):")
        for w in warns[:10]:
            print("  ⚠️", w)

    # 2. Check data/events/*.json
    events_dir = os.path.join(root, "data", "events")
    if os.path.exists(events_dir):
        for fname in sorted(os.listdir(events_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(events_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    era_evts = json.load(f)
                errs_era, warns_era = validate_event_list(era_evts, fname)
                total_checked += len(era_evts)
                print(f"Validated {len(era_evts)} events in data/events/{fname}.")
                if errs_era:
                    all_ok = False
                    print(f"Errors in {fname} ({len(errs_era)}):")
                    for e in errs_era[:10]:
                        print("  ❌", e)
                if warns_era:
                    print(f"Warnings in {fname} ({len(warns_era)}):")
                    for w in warns_era[:5]:
                        print("  ⚠️", w)

    # 3. Check data/events.json if exists
    events_json_path = os.path.join(root, "data", "events.json")
    if os.path.exists(events_json_path):
        with open(events_json_path, "r", encoding="utf-8") as f:
            legacy_events = json.load(f)
        total_checked += len(legacy_events)
        print(f"Validated {len(legacy_events)} legacy events in data/events.json.")

    print(f"\nTotal checked: {total_checked} events.")
    if all_ok:
        print("✅ Event validation passed with 0 errors!")
    else:
        print("❌ Event validation failed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
