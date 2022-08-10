from app.db.session import SessionLocal
from app.api.api_v1.routers.geo_stats import add_geo_stats_route, get_geo_stats
from fastapi import APIRouter

from unittest.mock import MagicMock


def test_adds_route():
    router = MagicMock(spec=APIRouter)
    add_geo_stats_route(router)
    router.add_api_route.assert_called_once()


def test_queries_db():
    db = MagicMock(spec=SessionLocal)
    print(db.__dict__)
    get_geo_stats(123, db, None)
    db.assert_called_once()
