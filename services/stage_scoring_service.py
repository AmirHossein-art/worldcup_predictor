from database.models import StageScoringRule


DEFAULT_GROUP_STAGE_POINTS = {
    "exact_score_points": 12,
    "winner_diff_points": 8,
    "winner_only_points": 4,
    "qualified_team_points": 0,
}


DEFAULT_KNOCKOUT_STAGE_POINTS = {
    "exact_score_points": 12,
    "winner_diff_points": 8,
    "winner_only_points": 4,
    "qualified_team_points": 3,
}

def get_scoring_lookup_stages(stage):

    if stage == "فینال":

        return [
            "فینال",
            "رده بندی",
        ]

    return [
        stage
    ]

def get_stage_scoring_rule(db, match):

    lookup_stages = get_scoring_lookup_stages(
        match.stage
    )

    rule = (
        db.query(StageScoringRule)
        .filter(
            StageScoringRule.stage.in_(lookup_stages),
            StageScoringRule.is_active == True
        )
        .order_by(StageScoringRule.rule_id.asc())
        .first()
    )

    if rule:

        return {
            "exact_score_points": rule.exact_score_points,
            "winner_diff_points": rule.winner_diff_points,
            "winner_only_points": rule.winner_only_points,
            "qualified_team_points": rule.qualified_team_points,
        }

    if match.stage == "مرحله گروهی":

        return DEFAULT_GROUP_STAGE_POINTS

    return DEFAULT_KNOCKOUT_STAGE_POINTS