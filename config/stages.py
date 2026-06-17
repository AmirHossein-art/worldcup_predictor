GROUP_STAGES = [
    "مرحله گروهی"
]

KNOCKOUT_STAGES = [
    "1/32 نهایی",
    "1/16 نهایی",
    "1/8 نهایی",
    "1/4 نهایی",
    "نیمه نهایی",
    "رده بندی",
    "فینال"
]

STAGES = (
    GROUP_STAGES +
    KNOCKOUT_STAGES
)

def is_group_stage(stage):
    return stage in GROUP_STAGES


def is_knockout_stage(stage):
    return stage in KNOCKOUT_STAGES


def is_knockout_match(match):
    return is_knockout_stage(
        match.stage
    )