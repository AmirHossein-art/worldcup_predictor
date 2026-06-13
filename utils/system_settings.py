from database.models import SystemSettings


def get_system_settings(db):
    settings = (
        db.query(SystemSettings)
        .first()
    )

    if settings is None:

        settings = SystemSettings()

        db.add(settings)

        db.commit()

        db.refresh(settings)

    return settings