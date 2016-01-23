# libcrowds-statistics

Global statistics page for LibCrowds, designed to integrate with the
[libcrowds-pybossa-theme](https://github.com/LibCrowds/libcrowds-pybossa-theme) and
provide a bit more control over how analytical data is generated on the platform. 
It's also a nice excuse to generate pretty charts.


## Installation

Download this repository and copy [libcrowds_statistics](libcrowds_statistics)
into your PyBossa [plugins](https://github.com/PyBossa/pybossa/tree/master/pybossa/plugins)
directory. The global statistics page will be available after you next restart
the server.


## Testing

This plugin makes use of the PyBossa test suite while running tests. The 
[Travis CI configuration file](.travis.yml) contains all of the required commands to set
up a test environment and run the tests.


## Contributing

See the [CONTRIBUTING](https://github.com/alexandermendes/Flask-Z3950/blob/master/CONTRIBUTING.md) 
file for guidelines on how to suggest improvements, report bugs or submit pull requests.