# What it is

The AHNExtractor is able to extract AHN data (height data for The Netherlands) based on a given polyline. The code is a rewrite of the [original code](https://github.com/viktor-platform/sample-ahn-profile) but with some extra functionality like x, y, z output and AHN2 / AHN3 choices. **Note that the changes are expected mid 2022 where AHN2 and AHN3 data might be moved to another server and AHN4 will become available**.

## Sample code AHN3 

### DTM 

DTM is bedoeld als maaiveldbestand, waarbij alle niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) uit de puntenwolk zijn verwijderd.

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DTM) 
data = ahnextractor.get(
    polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), 
    interval=20)
```

The result will be;
```python
[
    (0.0, 122864.0, 473437.0, -5.752),
    (20.0, 122876.32, 473452.76, -3.998),
    (40.0, 122888.64, 473468.51, -2.173),
    (60.0, 122900.96, 473484.27, -2.419),
    (69.81, 122907.0, 473492.0, -2.407),
    (89.81, 122926.13, 473497.82, -2.449),
]
```

which are coordinates in the form of (length from start [m], x in RD coordinates, y in RD coordinates, height [m])

**note that AHNExtractor will round the coordinates to 2 decimals and the height to 3 decimals**

### DSM 

DSM is bedoeld als ruw bestand, waarbij zowel het maaiveld als de niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) vanuit de puntenwolk tot een 0,5 meter raster zijn herbemonsterd. Er zijn geen verdere bewerkingen uitgevoerd. 

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DSM) 
data = ahnextractor.get(
    polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), 
    interval=20)
```


## Sample code AHN2

### DTM

DTM is bedoeld als maaiveldbestand, waarbij alle niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) uit de puntenwolk zijn verwijderd. Incidentele No-Data cellen zijn opgevuld.

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DTM)
data = ahnextractor.get(
    polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), 
    interval=20)
```

### DSM

DSM is bedoeld als ruw bestand, waarbij zowel het maaiveld als de niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) vanuit de puntenwolk tot een 0,5 meter raster zijn herbemonsterd. Er zijn geen verdere bewerkingen uitgevoerd. 

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DSM)
data = ahnextractor.get(
    polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)),
    interval=20)
```

## RDP

It is possible to apply the [Ramer-Douglas-Peucker algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) to filter points based on the height difference between the consecutive points. A value of 0.05 is recommended to filter out unnecessary points.

Example code;

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DTM)
data = ahnextractor.get(
    polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), 
    interval=20, 
    rdp_epsilon=0.05)
```

## Todo

* [x] implement AHN2 (changes expected as of mid 2022 see https://geoforum.nl/t/datasets-ahn1-en-ahn-2-bij-pdok-uit-productie/6624)
* [ ] implement AHN4 (expected mid 2022)
* [ ] more tests
* [ ] documenting
* [ ] publish it on PyPI
* [x] add option for the RDP (Ramer-Douglas-Peucker) algorithm 
* [ ] add option for spike removal if the data is nasty
* [x] add DTM, DSM option

## Credits

Most of the code was copied from [this repository](https://github.com/viktor-platform/sample-ahn-profile) so the credits go to [Sylvian van der Meer](https://github.com/svandermeer) and [Viktor AI](https://www.viktor.ai/)
