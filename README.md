# libcrowds-statistics

[![Build Status](https://travis-ci.org/LibCrowds/libcrowds-statistics.svg?branch=master)](https://travis-ci.org/LibCrowds/libcrowds-statistics)
[![Coverage Status](https://coveralls.io/repos/LibCrowds/libcrowds-statistics/badge.svg)](https://coveralls.io/github/LibCrowds/libcrowds-statistics?branch=master)

Global statistics page for LibCrowds, designed to integrate with the
[libcrowds-pybossa-theme](https://github.com/LibCrowds/libcrowds-pybossa-theme) and
provide a bit more control over how analytical data is generated on the platform.
It's also a nice excuse to generate pretty charts.


## Installation

Copy the [libcrowds_statistics](libcrowds_statistics) folder into your PyBossa
[plugins](https://github.com/PyBossa/pybossa/tree/master/pybossa/plugins) directory. The
plugin will be available after you next restart the server.


## Usage

The plugin makes a new global statistics page available at:

``` HTTP
/statistics
```

In order to generate location based statistics for all users this plugin also registers an
event listener to record IP addresses for all new task runs (the PyBossa default
is to record IP addresses for anonymous users only). All other statistics are
generated from the standard PyBossa data.


## Integration

If using the [libcrowds-pybossa-theme](https://github.com/LibCrowds/libcrowds-pybossa-theme) the
**Statistics** link on the main navigation bar will point to the page defined in this plugin.


## Testing

This plugin makes use of the PyBossa test suite while running tests. The
[Travis CI configuration file](.travis.yml) contains all of the required commands to set
up a test environment and run the tests.


## Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to suggest improvements,
report bugs or submit pull requests.
