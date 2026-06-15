from pathlib import Path


FLAGS_DIR = Path("assets") / "flags"


TEAMS = {
    "مکزیک": "mx",
    "کره جنوبی": "kr",
    "آفریقای جنوبی": "za",
    "جمهوری چک": "cz",

    "کانادا": "ca",
    "سوییس": "ch",
    "قطر": "qa",
    "بوسنی و هرزگوین": "ba",

    "برزیل": "br",
    "مراکش": "ma",
    "هائیتی": "ht",
    "اسکاتلند": "gb-sct",

    "آمریکا": "us",
    "پاراگوئه": "py",
    "استرالیا": "au",
    "ترکیه": "tr",

    "آلمان": "de",
    "کوراسائو": "cw",
    "ساحل عاج": "ci",
    "اکوادور": "ec",

    "هلند": "nl",
    "ژاپن": "jp",
    "تونس": "tn",
    "سوئد": "se",

    "بلژیک": "be",
    "مصر": "eg",
    "ایران": "ir",
    "نیوزیلند": "nz",

    "اسپانیا": "es",
    "کیپ ورد": "cv",
    "عربستان سعودی": "sa",
    "اروگوئه": "uy",

    "فرانسه": "fr",
    "سنگال": "sn",
    "نروژ": "no",
    "عراق": "iq",

    "آرژانتین": "ar",
    "الجزایر": "dz",
    "اتریش": "at",
    "اردن": "jo",

    "پرتغال": "pt",
    "ازبکستان": "uz",
    "کلمبیا": "co",
    "کنگو دموکراتیک": "cd",

    "انگلیس": "gb-eng",
    "کرواسی": "hr",
    "غنا": "gh",
    "پاناما": "pa",
}

TEAMS_FLAGS = {
    team_name: ""
    for team_name in TEAMS.keys()
}


def get_team_names():
    return list(TEAMS.keys())

def get_team_code(team_name):
    return TEAMS.get(team_name)

def get_flag_path(team_name):
    code = TEAMS.get(team_name)

    if not code:
        return None

    return FLAGS_DIR / f"{code}.svg"

def has_flag_image(team_name):
    flag_path = get_flag_path(team_name)

    return(
        flag_path is not None
        and 
        flag_path.exists()
    )


def get_team_display_text(team_name):
    if not team_name:
        return "-"

    return team_name