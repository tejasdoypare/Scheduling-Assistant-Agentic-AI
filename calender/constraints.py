def tag_constraints(slot, users_working_hours):
    """
    slot: {start_utc, end_utc}
    users_working_hours: dict[user_id] -> (work_start_utc, work_end_utc)
    """
    within_hours = True

    for user, (work_start, work_end) in users_working_hours.items():
        if slot["start_utc"] < work_start or slot["end_utc"] > work_end:
            within_hours = False
            break

    return {
        "within_working_hours": within_hours,
        "duration_ok": True,  # placeholder (we’ll refine later)
        "conflicts": []
    }



def slot_duration_minutes(slot):
    delta = slot["end_utc"] - slot["start_utc"]
    return delta.total_seconds() / 60


def duration_ok(slot, required_minutes):
    return slot_duration_minutes(slot) >= required_minutes


def disruption_score(slot, users):
    """
    users: dict[user_id] -> flexibility (0 to 1)
    """
    avg_flex = sum(users.values()) / len(users)
    return round(1 - avg_flex, 2)


def timezone_fairness_score(slot, users_timezones):
    """
    users_timezones: dict[user_id] -> UTC offset hours
    """
    offsets = list(users_timezones.values())
    spread = max(offsets) - min(offsets)
    return round(1 / (1 + spread), 2)


def enrich_slot(slot, slot_id, participants, constraints, scores):
    return {
        "slot_id": slot_id,
        "start_utc": slot["start_utc"],
        "end_utc": slot["end_utc"],
        "participants": participants,
        "constraints": constraints,
        "scores": scores
    }


