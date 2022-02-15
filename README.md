## What it is

The AHNExtractor is able to extract AHN data (height data for The Netherlands) based on a given polyline. The code is a rewrite of the [original code](https://github.com/viktor-platform/sample-ahn-profile) but with some extra functionality like x, y, z output and (hopefully?) AHN2 / AHN3 / AHN4 choices.

Sample code
```python
ahnextractor = AhnExtractor()
data = ahnextractor.get(polyline=Polyline.from_points((122864,473437), (122907,473492), (122930, 473499)), interval=2.0)
```

which will result in a list like;
```
[
    (122864.0, 473437.0, -5.751999855041504), 
    (122876.31843932795, 473452.75614332646, -3.997999906539917),
    (122888.6368786559, 473468.51228665287, -2.1730000972747803),
    (122900.95531798385, 473484.26842997933, -2.4189999103546143),
    (122907.0, 473492.0, -2.4070000648498535),
    (122926.13347760857, 473497.82323231566, -2.4489998817443848),
]
```

## Todo

* [ ] check if AHN2 is possible
* [ ] check if AHN4 is possible
* [ ] more tests
* [ ] documenting
* [ ] publish it on PyPI
* [ ] add option for the RDP (Ramer-Douglas-Peucker) algorithm 
* [ ] add option for spike removal if the data is nasty
* [ ] add DTM, DSM option

## Credits

Most of the code was copied from [this repository](https://github.com/viktor-platform/sample-ahn-profile) so the credits for the async data fetching code goes to [Sylvian van der Meer](https://github.com/svandermeer) and [Viktor AI](https://www.viktor.ai/)