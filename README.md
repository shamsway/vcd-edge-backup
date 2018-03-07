# vcd-edge-backup
Backup script for vCloud Director 9.0 edge gateways. I wrote this script after reading through the first few chapters of [Network Programability and Automation](http://shop.oreilly.com/product/0636920042082.do).

This script is developed and tested against vCD 9.0 and probably will not work with earlier versions.

### Useage
* Edit config.yaml.example to specify the URL of your vCD instance, and save as config.yaml
* Login with 'username@org'. To log in with administrative credentials, login with 'username@System'
* Edge config XML files will be saved to the local directory with timestamp

### To do
* Add option to save credentials in config.yaml
* Verify correct username format
* Add command line arguments options
* Add option for creating directories based on date
* Add support to push config files to a git repo?
* Create a script to restore configs to an edge
