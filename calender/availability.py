# calender/availability.py

def compute_free_slots(events, work_start_utc, work_end_utc):
    free_slots = []
    current_time = work_start_utc

    for event in events:
        if current_time < event["start_utc"]:
            free_slots.append({
                "start_utc": current_time,
                "end_utc": event["start_utc"]
            })
        current_time = max(current_time, event["end_utc"])

    if current_time < work_end_utc:
        free_slots.append({
            "start_utc": current_time,
            "end_utc": work_end_utc
        })

    return free_slots


def intersect_two_users(slots_a, slots_b):
    """
    slots_a, slots_b: list of dicts with keys start_utc, end_utc
    returns: list of intersected slots
    """
    intersections = []

    i, j = 0, 0
    while i < len(slots_a) and j < len(slots_b):
        start = max(slots_a[i]["start_utc"], slots_b[j]["start_utc"])
        end = min(slots_a[i]["end_utc"], slots_b[j]["end_utc"])

        if start < end:
            intersections.append({
                "start_utc": start,
                "end_utc": end
            })

        if slots_a[i]["end_utc"] < slots_b[j]["end_utc"]:
            i += 1
        else:
            j += 1

    return intersections

