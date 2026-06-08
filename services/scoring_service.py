def get_match_result(
    home_score,
    away_score
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

    if (
        prediction.pred_home
        == match.home_score
        and
        prediction.pred_away
        == match.away_score
    ):

        score += 10

    elif (
        get_match_result(
            prediction.pred_home,
            prediction.pred_away
        )
        ==
        get_match_result(
            match.home_score,
            match.away_score
        )
    ):

        score += 5

    if (
        match.qualified_team
        and
        prediction.pred_qualified_team
        ==
        match.qualified_team
    ):

        score += 3

    return score