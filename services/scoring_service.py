from utils.constants import (
    EXACT_SCORE_POINTS,
    WINNER_DIFF_POINTS,
    WINNER_ONLY_POINTS,
    QUALIFIED_TEAM_POINTS,
    TOURNAMENT_CHAMPION,
    CHAMPION_POINTS
)
from config.stages import is_knockout_match

from services.stage_scoring_service import get_stage_scoring_rule

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
    match,
    db
):

    score = 0

    stage_points = get_stage_scoring_rule(
        db,
        match
    )

    exact_score_points = stage_points["exact_score_points"]
    winner_diff_points = stage_points["winner_diff_points"]
    winner_only_points = stage_points["winner_only_points"]
    qualified_team_points = stage_points["qualified_team_points"]

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
    # Match Score
    # ==========================

    if (
        prediction.pred_home
        == match.home_score
        and
        prediction.pred_away
        == match.away_score
    ):

        score += exact_score_points

    elif (
        predicted_result == actual_result
        and
        predicted_diff == actual_diff
    ):

        score += winner_diff_points

    elif predicted_result == actual_result:

        score += winner_only_points

    # ==========================
    # Qualified Team
    # فقط برای بازی‌های حذفی
    # ==========================

    if (
        is_knockout_match(match)
        and
        match.qualified_team is not None
    ):

        predicted_qualified_team = None

        if predicted_result == "HOME":

            predicted_qualified_team = match.home_team

        elif predicted_result == "AWAY":

            predicted_qualified_team = match.away_team

        elif (
            predicted_result == "DRAW"
            and
            prediction.pred_qualified_team is not None
        ):

            predicted_qualified_team = prediction.pred_qualified_team

        if (
            predicted_qualified_team is not None
            and
            predicted_qualified_team == match.qualified_team
        ):

            score += qualified_team_points

    return score


def calculate_user_score(
    user,
    db
):

    total_score = 0

    for prediction in user.predictions:

        match = prediction.match

        if not match.result_entered:
            continue

        total_score += (
            calculate_prediction_score(
                prediction,
                match,
                db
            )
        )

    
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
