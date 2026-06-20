from datetime import date, timedelta

from database.models import User, UserScoreSnapshot
from services.scoring_service import calculate_user_score


def save_daily_score_snapshots(db, snapshot_date=None):
    if snapshot_date is None:
        snapshot_date = date.today()

    users = (
        db.query(User)
        .filter(User.is_verified == True)
        .all()
    )

    for user in users:
        score = calculate_user_score(user)

        existing_snapshot = (
            db.query(UserScoreSnapshot)
            .filter(
                UserScoreSnapshot.user_id == user.user_id,
                UserScoreSnapshot.snapshot_date == snapshot_date
            )
            .first()
        )

        if existing_snapshot:
            existing_snapshot.score = score
        else:
            snapshot = UserScoreSnapshot(
                user_id=user.user_id,
                snapshot_date=snapshot_date,
                score=score
            )
            db.add(snapshot)

    db.commit()


def get_daily_phenomenon(db, target_date=None):
    if target_date is None:
        target_date = date.today()

    today_snapshots = (
        db.query(UserScoreSnapshot)
        .filter(
            UserScoreSnapshot.snapshot_date == target_date
        )
        .all()
    )

    if not today_snapshots:
        return []

    previous_snapshot_date = (
        db.query(UserScoreSnapshot.snapshot_date)
        .filter(
            UserScoreSnapshot.snapshot_date < target_date
        )
        .order_by(
            UserScoreSnapshot.snapshot_date.desc()
        )
        .first()
    )

    if not previous_snapshot_date:
        previous_scores = {}
    else:
        previous_date = previous_snapshot_date[0]

        previous_snapshots = (
            db.query(UserScoreSnapshot)
            .filter(
                UserScoreSnapshot.snapshot_date == previous_date
            )
            .all()
        )

        previous_scores = {
            snapshot.user_id: snapshot.score
            for snapshot in previous_snapshots
        }

    candidates = []

    for today_snapshot in today_snapshots:

        previous_score = previous_scores.get(
            today_snapshot.user_id,
            0
        )

        score_delta = (
            today_snapshot.score
            -
            previous_score
        )

        if score_delta <= 0:
            continue

        candidates.append(
            {
                "user": today_snapshot.user,
                "previous_score": previous_score,
                "current_score": today_snapshot.score,
                "score_delta": score_delta
            }
        )

    candidates.sort(
        key=lambda item: (
            item["score_delta"],
            item["current_score"]
        ),
        reverse=True
    )

    return candidates