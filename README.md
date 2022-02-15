# What it is

The AHNExtractor is able to extract AHN data (height data for The Netherlands) based on a given polyline. The code is a rewrite of the [original code](https://github.com/viktor-platform/sample-ahn-profile) but with some extra functionality like x, y, z output and (hopefully?) AHN2 / AHN3 choices. **Note that the changes are expected mid 2022 where AHN2 and AHN3 data might be moved to another server and AHN4 will become available**.

## Sample code AHN3 

### DTM 

DTM is bedoeld als maaiveldbestand, waarbij alle niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) uit de puntenwolk zijn verwijderd.

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DTM) 
data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)
```

### DSM 

DSM is bedoeld als ruw bestand, waarbij zowel het maaiveld als de niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) vanuit de puntenwolk tot een 0,5 meter raster zijn herbemonsterd. Er zijn geen verdere bewerkingen uitgevoerd. 

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN3, source=AhnSource.DSM) 
data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)
```


## Sample code AHN2

### DTM

DTM is bedoeld als maaiveldbestand, waarbij alle niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) uit de puntenwolk zijn verwijderd. Incidentele No-Data cellen zijn opgevuld.

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DTM)
data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)
```

### DSM

DSM is bedoeld als ruw bestand, waarbij zowel het maaiveld als de niet-maaiveld objecten (bomen, gebouwen, bruggen en andere objecten) vanuit de puntenwolk tot een 0,5 meter raster zijn herbemonsterd. Er zijn geen verdere bewerkingen uitgevoerd. 

```python
ahnextractor = AhnExtractor(version=AhnVersion.AHN2, source=AhnSource.DSM)
data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=20)
```


## Todo

* [x] implement AHN2 (changes expected as of mid 2022 see https://geoforum.nl/t/datasets-ahn1-en-ahn-2-bij-pdok-uit-productie/6624)
* [ ] implement AHN4 (expected mid 2022)
* [ ] more tests
* [ ] documenting
* [ ] publish it on PyPI
* [ ] add option for the RDP (Ramer-Douglas-Peucker) algorithm 
* [ ] add option for spike removal if the data is nasty
* [x] add DTM, DSM option

## Credits

Most of the code was copied from [this repository](https://github.com/viktor-platform/sample-ahn-profile) so the credits go to [Sylvian van der Meer](https://github.com/svandermeer) and [Viktor AI](https://www.viktor.ai/)
