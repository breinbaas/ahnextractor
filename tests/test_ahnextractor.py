from ahnextractor import __version__
from ahnextractor.ahnextractor import AhnExtractor, AhnVersion, AhnSource
from ahnextractor.polyline import Polyline

def test_version():
    assert __version__ == '0.1.0'

def test_ahn3_dtm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DTM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20) 
    i = 1   

def test_ahn2_dtm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DTM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)

def test_ahn3_dsm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DSM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)    

def test_ahn2_dsm():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DSM)
    data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)

def test_rdp():
    ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DTM)
    data1 = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)
    data2 = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20, rdp_epsilon=0.05)
    assert len(data1) == 6
    assert len(data2) == 4
    
