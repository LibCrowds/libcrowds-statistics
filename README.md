# libcrowds-statistics

[![Build Status](https://travis-ci.org/LibCrowds/libcrowds-statistics.svg?branch=master)]
(https://travis-ci.org/LibCrowds/libcrowds-statistics)
[![Coverage Status](https://coveralls.io/repos/LibCrowds/libcrowds-statistics/badge.svg)]
(https://coveralls.io/github/LibCrowds/libcrowds-statistics?branch=master)

Global statistics page for LibCrowds, designed to integrate with the
[libcrowds-pybossa-theme](https://github.com/LibCrowds/libcrowds-pybossa-theme) and
provide a bit more control over how analytical data is generated on the platform.
It's also a nice excuse to generate pretty charts.


## Installation

Copy the [libcrowds_statistics](libcrowds_statistics) folder into your PyBossa
[plugins](https://github.com/PyBossa/pybossa/tree/master/pybossa/plugins) directory. The
plugin will be available after you next restart the server.


## Configuration

The default configuration settings for the plugin are:

``` Python
# Record user IP addresses for all task runs.
# WARNING: This setting is mainly here for testing purposes. If set to False
# location data will no longer be available for all users.
STATISTICS_RECORD_ALL_IPS = True
```

You can modify these settings by adding them to your main PyBossa configuration
file.


## Integration

If using the [libcrowds-pybossa-theme](https://github.com/LibCrowds/libcrowds-pybossa-theme) the
**Statistcs** link on the main navigation bar will point to the page defined in this plugin.


## Testing

This plugin makes use of the PyBossa test suite while running tests. The
[Travis CI configuration file](.travis.yml) contains all of the required commands to set
up a test environment and run the tests.


## Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to suggest improvements,
report bugs or submit pull requests.