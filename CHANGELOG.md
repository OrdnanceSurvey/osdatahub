# Changelog

## [1.2.6] - 2023/06/28

### Features
- Added check for chunk size when straming data. Program should error if file download is incomplete [JEPooley]

## [1.2.5] - 2023/05/17

### Fixed

- Import error for osdatahub.post in PlacesAPI [FHunt-OS] [JEPooley]

### Features

- Added support for the dataset parameter within the PlacesAPI wrapper [FHunt-OS] [JEPooley]

## [1.2.4] - 2023/04/20

### Fixed

- Removed requests wrapper for Downloads API as it breaks requests that stream the data (issue #79)
- Improved pbar to include total number of files to be downloaded. Also removed the finished download writeout to preserve aesthetics

## [1.2.3] - 2023/04/12

### Fixed

- Added requests wrapper that raises an error in the case of an incomplete response (issue 73) [JEPooley]

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

