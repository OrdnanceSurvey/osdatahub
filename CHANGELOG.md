# Changelog

## [1.3.0] - 2024/11/18
- Removing Support for Python 3.7
- Adding Support for Python 3.12, 3.13

- Resolved issues on installation on later python versions
- Updated Typeguard Version
- Updated Packages to latest versions
- Fixed typing on GeoJson Outputs -> Feature Collection to Dict.

## [1.2.11] - 2024/07/08
- Package Resupported - Supported under new team [jmbraybrook]

## [1.2.10] - 2024/03/08

### Changed
- ⚠ PACKAGE DEPRECATED 

## [1.2.9] - 2023/10/04

### Changed
- Increased DownloadsAPI sleep time to 20

## [1.2.8] - 2023/10/04

### Added
- Downloads API outputs a missing_files.[datetime].json file that details the specific files that didn't successfully download [JEPooley] [Amber Thorne]

### Fixed
- Downloads API now shows correct number of downloaded files e.g. when some have failed or are missing [JEPooley] [Amber Thorne]

## [1.2.7] - 2023/06/28

### Fixed
- NamesAPI no longer raises a KeyError if the response status code is 200 [JEPooley] [sam596]

## [1.2.6] - 2023/06/28

### Added
- Added check for chunk size when streaming data. Program should error if file download is incomplete [JEPooley]

### Changed
- Upgrade requests version in dependencies to 2.31.0 [gwionap]

## [1.2.5] - 2023/05/17

### Fixed

- Import error for osdatahub.post in PlacesAPI [FHunt-OS] [JEPooley]

### Added

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

### Added

- Added proxy support using the `osdatahub.set_proxies` method (issue 55) [JEPooley] [FHunt-OS] [abiddiscombe]

## [1.2.1] - 2022/12/08

### Fixed

- Fixed paging for NGD Features requests

## [1.2.0] - 2022/11/07

### Added

- Added NGD API [dchirst] [BenDickens] [JEPooley]
- Fixed typos in Features and Places APIs [dchirst]
- Added NGD quick start to README [dchirst] [JEPooley]

## [1.1.0] - 2022/08/22

### Added

- Support the new Data Hub API v2 [dchirst]
- Allow filters to be joined using bitwise operators [E-Paine]
- Improved warnings when queries are too large (issue 25) [E-Paine]
- Allow any type of collection to be used to construct a bounding box (issue 22) [E-Paine]
- Warn when using EPSG:4329 with the features API (issue 29) [E-Paine]

### Fixed

- Error when `nearest` returned an empty feature set (issue 24) [E-Paine]

