from datetime import datetime, timedelta


def can_predict(match):

    deadline = (
        match.kickoff_time
        - timedelta(hours=24)
    )

    return datetime.utcnow() < deadline