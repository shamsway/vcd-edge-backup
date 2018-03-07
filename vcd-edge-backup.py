#!/usr/local/bin/python

import getpass
import lxml.etree as etree
import requests
import urllib3
import datetime
import yaml
import logging

if __name__ == "__main__":
    # Disable warnings for self-signed certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with open('./config.yaml') as file:
        try:
            config = yaml.load(file)
        except yaml.YAMLError as exc:
            print "Error in configuration file:", exc

    baseurl = config['url']
    authurl = baseurl + "/api/sessions"
    edgesurl = baseurl + "/network/edges"

    print "Connecting to " + baseurl
    # Prompt for username and password
    user = raw_input("Username: ")
    password = getpass.getpass("Password: ")

    headers = {'Content-Type': 'application/xml', 'Accept': 'application/*;version=29.0'}

    # try:
    #     import http.client as http_client
    # except ImportError:
    #    import httplib as http_client
    # http_client.HTTPConnection.debuglevel = 1

    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    # Retrieve vCD authorization token
    auth_req = requests.post(authurl, auth = (user, password), verify = False, headers = headers)

    if auth_req.status_code == 200:
        print "Authentication successful"
        api_auth = auth_req.headers['x-vcloud-authorization']
    else:
        print "Authentication failed - Response code " + str(auth_req.status_code)
        quit()

    # Add auth token to headers
    headers['x-vcloud-authorization'] = api_auth

    # Request list of edges from vCD
    edges_req = requests.get(edgesurl, verify = False, headers = headers)

    if edges_req.status_code == 200:
        edges_xml = etree.fromstring(edges_req.text)
    else:
        print "Get Edges API request failed"
        quit()
    
    # Iterate through returned list of edges, retrieve edge configuration and create a file containing the edge config
    for edge in edges_xml.iter('edgeSummary'):
        # Find edge ID in XML (e.g. edge-10)
        edge_id = edge.find('objectId').text
        # Find edge name in XML - used to generate filename for config backup
        edge_name = edge.find('name').text
        # Find edge GUID in XML - used to request edge config via API
        edge_guid = edge.find('id').text
        edgeurl = edgesurl + "/" + edge_guid

        # Request edge configuration
        edge_req = requests.get(edgeurl, verify = False, headers = headers)

        if edge_req.status_code == 200:
            edge_xml = etree.fromstring(edge_req.text)

            # Create backup filename with timestamp
            filename = '{:%Y%m%d%H%M%S}-{}.conf.xml'.format(datetime.datetime.now(),edge_name)
            print 'Creating backup: ' + filename
            try:
                with open(filename,"w") as backup_file:
                    backup_file.write(etree.tostring(edge_xml, pretty_print=True))
                    backup_file.close()
            except IOError:
                print "Error writing backup file"
                quit()
        else:
            print "Get Edge " + edge_id + " API request failed"
            quit()
