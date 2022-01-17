# osdatahub <!-- omit in toc -->

`osdatahub` is a python package from Ordnance Survey (OS) that makes it easier to interact with OS data via the [OS Data Hub APIs](https://osdatahub.os.uk/).


OS is the national mapping agency for Great Britain and produces a large variety of mapping
and geospatial products. Much of OS's data is available via the [OS Data Hub](https://osdatahub.os.uk/), a platform
that hosts both free and premium data products. `osdatahub` provides a user-friendly way to interact with these data products
in Python.

![The OS Logo](https://raw.githubusercontent.com/OrdnanceSurvey/osdatahub/modify-links/media/os-logo.png)

## Features <!-- omit in toc -->
- Get access to Ordnance Survey data in as few as 2-3 lines of code
- Easily query geographic extents using bounding boxes, radii and ONS geographies
- Request as much data as you need with automatic API paging
- Supports the OS Features and OS Places APIs

## Links <!-- omit in toc -->
- GitHub repo: https://github.com/OrdnanceSurvey/osdatahub
- Documentation: https://osdatahub.readthedocs.io/en/latest/
- PyPI: https://pypi.org/project/osdatahub/
- Free Software: Open Government License

**Note:** This package is under active development.

## Contents <!-- omit in toc -->

- [Setup](#setup)
- [Quick Start](#quick-start)
  - [Features API](#features-api)
  - [Places API](#places-api)
- [Tutorials](#tutorials)
- [Contribute](#contribute)


# Setup

`osdatahub` is available on [PyPI](https://pypi.org/project/osdatahub/). To install `osdatahub`, run this command in your terminal:

```bash
pip install osdatahub
```

You'll also need to sign-up for an account on the [OS Data Hub](https://osdatahub.os.uk/) and get an API key. If you've setup you're account and need help getting a key, try the 
following steps:

1. Navigate to the **API Dashboard** located on the top navigation bar
2. Go to **My Projects**
3. Click **Create a new project**, give your project a name, then click **Create project**
4. Select **Add an API to this project**
5. Choose the APIs you would like to use and click **Done** (Note: osdatahub supports 
   the OS Features API and the OS Places API)


# Quick Start

## Features API

Data can be queried within a geographical extent in just a few simple steps!

First, we need to import the **FeaturesAPI** class (which helps us runs queries) and 
the **Extent** class (which helps us to define a target region):

```python
from osdatahub import FeaturesAPI, Extent
```

Then we need to get our [OS API key](https://osdatahub.os.uk/) and store it as a variable ([find out how to 
do this securely with environment variables](https://github.com/OrdnanceSurvey/osdatahub/blob/modify-links/Examples/Setting%20up%20an%20API%20key.ipynb)):

```python
key = "[YOUR KEY GOES HERE]"
```

Next, we define our geographic extent. For this example we're going use a 
bounding box, but it is also possible to specify radial extents, ONS 
geographies and custom polygons.

These bounding box coordinates are BNG coordinates in the order 
(West, South, East, North):

```python
extent = Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700")
```

And now we can run our query! We just have to assemble the parts and decide 
which OS Features product we want to explore. In this case, we're going to 
choose "zoomstack_local_buildings" — an open data set of Great Britain's 
local buildings:

```python
product = "zoomstack_local_buildings"
features = FeaturesAPI(key, product, extent)
results = features.query(limit=50)
```

The data stored in the results variable will be in geojson format, limited to 
50 features. To save the query results as a geojson file, you need to import 
the [geojson module](https://github.com/jazzband/geojson) and use the .dump() 
function:

```python
import geojson

geojson.dump(results, open("FILENAME.geojson", "w"))
```

Putting this all together, we get:

```python
from osdatahub import FeaturesAPI, Extent
import geojson

key = "[YOUR KEY GOES HERE]"
extent = Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700")
product = "zoomstack_local_buildings"
features = FeaturesAPI(key, product, extent)
results = features.query(limit=50)

geojson.dump(results, open("FILENAME.geojson", "w"))
```
## Places API

To run a similar query using the OS Places API, we just need to make two changes. 
First, we no longer need to decide on a product — the Places API is always 
going to give us addresses! Secondly, the **PlacesAPI** class does not require 
an extent (because there are other, non-geographic, queries available). 
Therefore, our bounding box extent does not need to be passed in until the 
query is run.

The final result looks like this:

```python
from osdatahub import PlacesAPI, Extent
import geojson

key = "[YOUR KEY GOES HERE]"
extent = Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700")
places = PlacesAPI(key) # No extent or product is given to PlacesAPI
results = places.query(extent, limit=50) # Extent is passed directly into the .query() function

geojson.dump(results, open("FILENAME.geojson", "w"))
```
Note: The PlacesAPI requires a *premium* API key!

# Tutorials

Example notebooks, demonstrating various `osdatahub` features can be found in 
the Examples folder. Here is a list of the available content:

- [Setting up an API Key](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Setting%20up%20an%20API%20key.ipynb)
- [Defining Extents](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Defining%20Extents%20for%20API%20Queries.ipynb)
- [Filtering Attributes](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Filtering%20Attributes%20for%20API%20Queries.ipynb)
- [Plotting Query Results - GeoPandas, Matplotlib, Contextily](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Plotting%20API%20Results%20-%20GeoPandas%2C%20Matplotlib%20and%20Contextily.ipynb)
- [Interactive Plotting for Query Results](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Interactive%20Plotting%20for%20API%20Results%20-%20Folium.ipynb)
- [Converting Query Results into Common Formats](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Converting%20API%20Results%20into%20Common%20Data%20Formats.ipynb)
- [Post Processing Query Results](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Post%20Processing%20API%20Queries.ipynb)
- [Common CRS Pitfalls](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/CRS%20pitfalls.ipynb)

# Contribute

This package is still under active developement and we welcome contributions from the community via issues and pull requests.

To install osdatahub, along with the tools you need to develop and run tests, 
run the following in your environment:

```bash
pip install -e .[dev]
```
