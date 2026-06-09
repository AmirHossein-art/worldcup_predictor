from utils.constants import (
    EXACT_SCORE_POINTS,
    WINNER_DIFF_POINTS,
    WINNER_ONLY_POINTS,
    DRAW_ONLY_POINTS,
    QUALIFIED_TEAM_POINTS,
    TOURNAMENT_CHAMPION,
    CHAMPION_POINTS
)


def get_match_result(
    home_score: int,
    away_score: int
):

    if home_score > away_score:
        return "HOME"

    if away_score > home_score:
        return "AWAY"

    return "DRAW"


def calculate_prediction_score(
    prediction,
    match
):

    score = 0

    # محاسبه نتایج (برای استفاده در تمام بخش‌ها)
    predicted_result = get_match_result(
        prediction.pred_home,
        prediction.pred_away
    )

    actual_result = get_match_result(
        match.home_score,
        match.away_score
    )

    predicted_diff = (
        prediction.pred_home
        - prediction.pred_away
    )

    actual_diff = (
        match.home_score
        - match.away_score
    )

    # ==========================
    # Exact Score
    # ==========================

    if (
        prediction.pred_home
        == match.home_score
        and
        prediction.pred_away
        == match.away_score
    ):

        score += EXACT_SCORE_POINTS

    else:

        # ==========================
        # Winner + Goal Difference
        # ==========================

        if (
            predicted_result == actual_result
            and
            predicted_diff == actual_diff
        ):

            score += WINNER_DIFF_POINTS

        # ==========================
        # Draw Only
        # ==========================

        elif (
            predicted_result == "DRAW"
            and
            actual_result == "DRAW"
        ):

            score += DRAW_ONLY_POINTS

        # ==========================
        # Winner Only
        # ==========================

        elif predicted_result == actual_result:

            score += WINNER_ONLY_POINTS

    # ==========================
    # Qualified Team
    # ==========================
    # صعودکننده فقط در دو شرط:
    # 1. نتیجه برابری است (پنالتی‌ها) - صعودکننده باید انتخاب شود
    # 2. نتیجه برابری نیست - برنده خودکار صعودکننده است

    if match.qualified_team is not None:

        # شرط 1: برابری - صعودکننده باید انتخاب شود
        if (
            actual_result == "DRAW"
            and
            prediction.pred_qualified_team is not None
            and
            prediction.pred_qualified_team == match.qualified_team
        ):
            score += QUALIFIED_TEAM_POINTS

        # شرط 2: برنده معین - اگر نتیجه برنده درست است
        elif (
            actual_result != "DRAW"
            and
            predicted_result == actual_result
            and
            prediction.pred_qualified_team == match.qualified_team
        ):
            score += QUALIFIED_TEAM_POINTS

    return score

def calculate_user_score(
    user
):

    total_score = 0

    for prediction in user.predictions:

        match = prediction.match

        if not match.result_entered:
            continue

        total_score += (
            calculate_prediction_score(
                prediction,
                match
            )
        )

    tournament_score = 0

    if user.tournament_prediction:

        total_score += (
            calculate_tournament_score(
                user.tournament_prediction
            )
        )

    return total_score

def calculate_tournament_score(
    prediction
):
    score = 0
    if (
        TOURNAMENT_CHAMPION is None
    ):

        return 0
    if (
        prediction.champion
        and
        prediction.champion
        ==
        TOURNAMENT_CHAMPION
    ):
        score += CHAMPION_POINTS
    return score
