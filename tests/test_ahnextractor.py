from ahnextractor import __version__
from ahnextractor.ahnextractor import AhnExtractor
from ahnextractor.polyline import Polyline

def test_version():
    assert __version__ == '0.1.0'

def test_polyline():
    ahnextractor = AhnExtractor()

    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)))
    i = 1
