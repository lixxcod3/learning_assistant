# Define XP thresholds for each level
# Level: Minimum XP required
LEVEL_THRESHOLDS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5000,
    9: 7500,
    10: 10000
}

def calculate_level_stats(total_xp):
    """
    Calculate current level, XP required for next level, and progress percentage.
    """
    current_level = 1
    next_level_xp = LEVEL_THRESHOLDS[2]
    current_level_base_xp = 0

    # Determine current level based on thresholds
    for level, threshold in sorted(LEVEL_THRESHOLDS.items()):
        if total_xp >= threshold:
            current_level = level
            current_level_base_xp = threshold
        else:
            next_level_xp = threshold
            break
            
    # Handle max level cap
    if current_level == max(LEVEL_THRESHOLDS.keys()):
        return {
            "current_level": current_level,
            "next_level_xp": "MAX",
            "progress_percent": 100.0,
            "xp_into_level": total_xp - current_level_base_xp
        }

    # Calculate progress for the progress bar
    xp_into_level = total_xp - current_level_base_xp
    xp_required_for_level = next_level_xp - current_level_base_xp
    progress_percent = (xp_into_level / xp_required_for_level) * 100

    return {
        "current_level": current_level,
        "next_level_xp": next_level_xp,
        "progress_percent": min(100.0, progress_percent),
        "xp_into_level": xp_into_level,
        "xp_required": xp_required_for_level
    }