# Changelog


## [1.2.2] - 2023/03/16

### Fixed

- Fix BaseException being raised instead of caught with JSONDecodeError (issue 62) [JEPooley]
- Extents `from_radius` method no longer errors if the coordinate is not a tuple - now accepts any Iterable (issue 66) [JEPooley]
- Updated setup.cfg and tox.ini to reflect python3.11 compatability (issue 68) [JEPooley] [dchirst]

### Features

- Added proxy support using the `osdatahub.set_proxies` method (issue 55) [JEPooley] [FHunt-OS] [abiddiscombe]

## [1.2.1] - 2022/12/08

### Fixed

- Fixed paging for NGD Features requests

## [1.2.0] - 2022/11/07

### Features

- Added NGD API [dchirst] [BenDickens] [JEPooley]
- Fixed typos in Features and Places APIs [dchirst]
- Added NGD quick start to README [dchirst] [JEPooley]

## [1.1.0] - 2022/08/22

### Features

- Support the new Data Hub API v2 [dchirst]
- Allow filters to be joined using bitwise operators [E-Paine]
- Improved warnings when queries are too large (issue 25) [E-Paine]
- Allow any type of collection to be used to construct a bounding box (issue 22) [E-Paine]
- Warn when using EPSG:4329 with the features API (issue 29) [E-Paine]

### Bugs

- Error when `nearest` returned an empty feature set (issue 24) [E-Paine]

