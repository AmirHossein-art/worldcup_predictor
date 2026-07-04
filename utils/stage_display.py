def normalize_stage_name(stage):

    if stage is None:
        return ""

    return (
        str(stage)
        .strip()
        .replace("ي", "ی")
        .replace("ك", "ک")
        .replace("\u200c", " ")
        .replace("  ", " ")
    )


STAGE_DISPLAY_NAMES = {
    "1/32 نهایی": "1/16 نهایی",
    "1/32نهایی": "1/16 نهایی",
    "رده بندی": "فینال و رده‌بندی",
    "رده‌بندی": "فینال و رده‌بندی",
    "فینال": "فینال و رده‌بندی",
}


def get_stage_display_name(stage):

    normalized_stage = normalize_stage_name(stage)

    return STAGE_DISPLAY_NAMES.get(
        normalized_stage,
        normalized_stage
    )