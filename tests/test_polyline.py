from ahnextractor.polyline import Polyline

def test_from_points():
    pl = Polyline.from_points((0,0), (10.0, 10.0), (20.0, 0.0))
    assert len(pl.points) == 3