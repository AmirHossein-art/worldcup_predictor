from database.connection import Base
from database.connection import engine

from database.models import User, Match, Prediction, TournamentPrediction, ScoringRule


def create_tables():

    #Base.metadata.create_all(
    #    bind=engine
    #)


if __name__ == "__main__":
    create_tables()

    print("Tables created successfully")