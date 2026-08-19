from sport_engine.registry import register
from sport_engine.adapters.tennis import TennisAdapter
from sport_engine.adapters.football import FootballAdapter

register(TennisAdapter)
register(FootballAdapter)
