from utils.teams import (
    get_flag_path,
    get_team_display_text
)


def get_user_champion_flag(user):
    """
    مسیر فایل پرچم قهرمان انتخابی کاربر را برمی‌گرداند.
    اگر کاربر انتخابی نداشته باشد یا فایل پرچم موجود نباشد،
    رشته خالی برمی‌گرداند.
    """

    if not user.tournament_prediction:
        return ""

    champion = (
        user.tournament_prediction.champion
    )

    flag_path = get_flag_path(
        champion
    )

    if (
        flag_path
        and
        flag_path.exists()
    ):

        return str(flag_path)

    return ""


def get_user_champion_display(user):
    """
    نمایش قهرمان انتخابی کاربر برای جدول‌ها.
    فعلاً فقط نام کشور را برمی‌گرداند تا وابسته به emoji نباشیم.
    """

    if not user.tournament_prediction:
        return "❌ انتخاب نشده"

    champion = (
        user.tournament_prediction.champion
    )

    return get_team_display_text(
        champion
    )