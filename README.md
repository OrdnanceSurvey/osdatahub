# osdatahub <!-- omit in toc -->

[![GitHub issues](https://img.shields.io/github/issues/OrdnanceSurvey/osdatahub)](https://github.com/OrdnanceSurvey/osdatahub/issues)
[![Python package](https://github.com/OrdnanceSurvey/osdatahub/actions/workflows/python-package.yml/badge.svg)](https://github.com/OrdnanceSurvey/osdatahub/actions/workflows/python-package.yml)
<a href="https://codeclimate.com/github/dchirst/osdatahub/maintainability"><img src="https://api.codeclimate.com/v1/badges/471fd53dbb22e9e28546/maintainability" /></a>


`osdatahub` is a python package from Ordnance Survey (OS) that makes it easier to interact with OS data via
the [OS Data Hub APIs](https://osdatahub.os.uk/).

OS is the national mapping agency for Great Britain and produces a large variety of mapping
and geospatial products. Much of OS's data is available via the [OS Data Hub](https://osdatahub.os.uk/), a platform
that hosts both free and premium data products. `osdatahub` provides a user-friendly way to interact with these data
products
in Python. To see what data is available, you can use
the [OS Data Hub Explorer](https://labs.os.uk/public/data-hub-explorer/).

![The OS Logo](https://github.com/OrdnanceSurvey/osdatahub/blob/master/media/os-logo.png)

## Features <!-- omit in toc -->

- Get access to Ordnance Survey data in as few as 2-3 lines of code
- Easily query geographic extents using bounding boxes, radii and ONS geographies
- Request as much data as you need with automatic API paging
- Supports the OS Features, Places, Names, Linked Identifiers, and Downloads APIs

## Links <!-- omit in toc -->

- GitHub repo: https://github.com/OrdnanceSurvey/osdatahub
- Documentation: https://osdatahub.readthedocs.io/en/latest/
- PyPI: https://pypi.org/project/osdatahub/
- conda-forge:  https://anaconda.org/conda-forge/osdatahub
- Data Hub Explorer: https://labs.os.uk/prototyping/data-hub-explorer/
- Free Software: Open Government License

## Contents <!-- omit in toc -->

- [Setup](#setup)
- [Quick Start](#quick-start)
  - [NGD API](#ngd-api)
  - [Features API](#features-api)
  - [Places API](#places-api)
  - [Names API](#names-api)
  - [Linked Identifiers API](#linked-identifiers-api)
  - [Downloads API](#downloads-api)
- [Tutorials](#tutorials)
- [Proxies](#proxies)
- [Contribute](#contribute)
  - [Support](#support)


# Setup

`osdatahub` is available on [PyPI](https://pypi.org/project/osdatahub/). To install `osdatahub`, run this command in
your terminal:

```bash
pip install osdatahub
```

The library is also available to download via [conda](https://anaconda.org/conda-forge/osdatahub):

```bash
conda install -c conda-forge osdatahub
```

You'll also need to sign-up for an account on the [OS Data Hub](https://osdatahub.os.uk/) and get an API key. If you've
setup you're account and need help getting a key, try the
following steps:

1. Navigate to the **API Dashboard** located on the top navigation bar
2. Go to **My Projects**
3. Click **Create a new project**, give your project a name, then click **Create project**
4. Select **Add an API to this project**
5. Choose the APIs you would like to use and click **Done** (Note: osdatahub supports 
   the OS Features, Places, Names, Linked Identifiers, and Downloads APIs)


# Quick Start
## NGD API

Ordnance Survey's newest API replaces the Features API with extra functionality, better error handling, and an
OGC-compliant
GeoJSON return type. Currently, the NGD supports topographic features, with Places being added soon.

We can use the NGD API by importing the **NGD** class (which helps us run queries):

```python
from osdatahub import NGD
```

Then we need to get our [OS API key](https://osdatahub.os.uk/) and store it as a variable ([find out how to
do this securely with environment variables](https://github.com/OrdnanceSurvey/osdatahub/blob/master/Examples/Setting%20up%20an%20API%20key.ipynb)):

```python
key = "[YOUR KEY GOES HERE]"
```

Next, we must decide which NGD Collection we are interested in. We can discover the available collection ids in 2 ways:

1. Browse the [OS Data Hub Technical Documentation](https://osdatahub.os.uk/docs/ofa/technicalSpecification)
2. Run the `get_collections()` function:

```python
NGD.get_collections()
```

Then we can instantiate the NGD class, ready for us to query:

```python
collection = "bld-fts-buildingline"
ngd = NGD(key, collection)
results = ngd.query(max_results=50)
```

The `query()` function supports many different options and filters, such as various output CRS', CQL filters, and
start and end times for temporal features.

The data stored in the results variable will be in geojson format, limited to
50 features. To save the query results as a geojson file, you need to import
the [geojson module](https://github.com/jazzband/geojson) and use the `.dump() `
function:

```python
import geojson

geojson.dump(results, open("FILENAME.geojson", "w"))
```

If you have the ID of a specific feature you would like to query, you can use the `query_feature()` function instead:

```python
feature_id = "0000013e-5fed-447d-a627-dae6fb215138"
feature = ngd.query_feature(feature_id)
```

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


## Names API

The OS Data Hub also contains the OS Names API, which is a geographic directory containing basic information about 
identifiable places. The API allows us to identify places by their address/place name and can find the nearest 
address to a given point. 

The **NamesAPI** class is very similar to **PlacesAPI** as it needs only a (**premium**) API key. We can then query
the object with a place name to get more information:

```python
from osdatahub import NamesAPI

key = "[YOUR KEY GOES HERE]"

names = NamesAPI(key) # only a premium key is required to create a NamesAPI object
results = names.find("Buckingham Palace", limit=5)

geojson.dump(results, open("FILENAME.geojson", "w"))
```

Note: The NamesAPI requires a *premium* API key!

## Linked Identifiers API

The [OS Linked Identifiers API](https://osdatahub.os.uk/docs/linkedIdentifiers/overview) allows you to access the valuable relationships between properties, streets and OS MasterMap identifiers for free. It's as easy as providing the identifier you are interested in and the API will return the related feature identifiers. This allows you to find what addresses exist on a given street, or the UPRN for a building on a map, or the USRN for a road and more.

You can access the Linked Identifiers API via the **LinkedIdentifiersAPI** class. 
In it's simplest form, queries can be made using just an API key and an identifier:

```python
from osdatahub import LinkedIdentifiersAPI

key = "[YOUR KEY GOES HERE]"
linked_ids = LinkedIdentifiersAPI(key)
results = linked_ids.query(200001025758)
```

## Downloads API

If you'd like to download an entire dataset instead of querying the API on demand, the OS Data Hub has the 
[Downloads API](https://osdatahub.os.uk/docs/downloads/technicalSpecification). This API allows you to search, explore, and download both [Open Data Products](https://osdatahub.os.uk/downloads/open) (e.g. OS Open Rivers, Boundary-Line, and a 1:250,000 scale 
colour raster of Great Britain) and Premium Data Packages using Python.

It is possible to download Open Data products without an API key, but the Premium Data Packages require you to have
a premium API key and order the package you want to download on the [OS Data Hub website](https://osdatahub.os.uk/downloads/).

The first step to download data is to discover which products are available. You can see the available datasets on the
[OS Data Hub website](https://osdatahub.os.uk/downloads/) or using the following snippet of code:

```python
from osdatahub import OpenDataDownload

OpenDataDownload.all_products()
```

You can also see all Premium Data Packages available to download using your premium API key:

```python
from osdatahub import DataPackageDownload

key = "[YOUR KEY GOES HERE]"
DataPackageDownload.all_products(key)
```
Note: For Premium Data Packages, this query will only return datasets if you have previously *ordered* the dataset on the OS Data Hub
Website.

Once you have found a package you'd like to download, you can get a list of the different products you can download:

```python
greenspace = OpenDataDownload("OpenGreenspace")
greenspace.product_list()
```

Once you know the dataset and specific product you'd like to download, you can download the dataset locally:

```python
greenspace.download(file_name='opgrsp_essh_nj.zip')
```


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


# Proxies

To set proxies, use the `set_proxies` method from `osdatahub`. This should look something like:

```python
import osdatahub

osdatahub.set_proxies({"http": "http://ip:port", "https": "https://ip:port"})
```

and will apply to all the osdatahub api requests.


# Contribute

This package is still under active development and we welcome contributions from the community via issues and pull requests.

To install osdatahub, along with the tools you need to develop and run tests, 
run the following in your environment:

```bash
pip install -e .[dev]
```

## Support

For any kind of issues or suggestions please see the [**documentation**](https://osdatahub.readthedocs.io/en/latest/), open a **[github issue](https://github.com/OrdnanceSurvey/osdatahub/issues)** or contact us via Email **[datascience@os.uk](mailto:datascience@os.uk)**
