from datetime import datetime, timedelta


def can_predict(match):

    return datetime.utcnow() < match.kickoff_time