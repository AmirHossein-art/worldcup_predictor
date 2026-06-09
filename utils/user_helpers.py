from config.teams import TEAMS_FLAGS


def get_user_champion_flag(user):
    """
    گرفتن پرچم تیم قهرمان انتخابی کاربر
    
    Args:
        user: User model instance
        
    Returns:
        str: پرچم تیم یا رشته خالی
    """
    if not user.tournament_prediction:
        return ""

    champion = (
        user.tournament_prediction.champion
    )

    return TEAMS_FLAGS.get(
        champion,
        ""
    )


def get_user_champion_display(user):
    """
    نمایش قهرمان انتخابی کاربر (پرچم + نام)
    
    Args:
        user: User model instance
        
    Returns:
        str: "🇸🇵 اسپانیا" یا "❌ انتخاب نشده"
    """
    if not user.tournament_prediction:
        return "❌ انتخاب نشده"

    champion = (
        user.tournament_prediction.champion
    )
    flag = TEAMS_FLAGS.get(champion, "")

    return f"{flag} {champion}" if flag else "❌ انتخاب نشده"
