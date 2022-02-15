from ahnextractor import __version__
from ahnextractor.ahnextractor import AhnExtractor, AhnVersion, AhnSource
from ahnextractor.polyline import Polyline

def test_version():
    assert __version__ == '0.1.0'

def test_ahn3_dtm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DTM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)    

def test_ahn2_dtm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DTM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)

def test_ahn3_dsm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DSM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)    

def test_ahn2_dsm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DSM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)
