#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import codecs
import sys
import os
from platform import python_version
from svmon_client import remoteConfig

_services={}

_services['b2safe']=['b2safe','irods']
_services['gitlab']=['gitlab']
_services['svmon']=['spring','angular']
_services['b2access']=['b2access_unity']
_services['b2find']=['b2find','ckan']
_services['b2drop']=['nextcloud']
_services['dpmt']=['plone']
_services['eudat_website']=['drupal']
_services['b2gether']=['b2gether']
_services['gocdb']=['creg']
_services['b2access']=['unity']
_services['svmon_client']=['client']
_services['b2share']=["b2share"]
_services['b2handle'] = ['handle']
_services['B2HANDLE'] = ['handle']

_rpm_packages={}
_rpm_packages['b2safe']='b2safe'
_rpm_packages['irods']='irods-icat'

_tags={}
_tags['svmon']=['3.1','1.7']

def in_service_list(service_type):
    if service_type == None or service_type == "" or isinstance(service_type,str) == False:
        print("The service type argument should be a non-empty string")
        exit(1)
    if service_type in _services.keys():
        return True
    else:
        print("Your service type is unsupported. Please type --list-service-type see supported services.")
        exit(1)

def get_service_name(service_type):
    if service_type == None or service_type == "" or isinstance(service_type,str) == False:
        print("The service type argument should be a non-empty string")
        exit(1)
    if in_service_list(service_type):
        return _services.get(service_type)
    return []


def get_service_tag(service_type,configs=None):
    config = remoteConfig.RemoteConfig().getConfig()
    enableDebug = config["DEBUG_MODE"]

    if(enableDebug):
        print("Get service tag called... with service type: ", service_type)

    tags=[]
    if service_type == None or service_type == "" or isinstance(service_type,str) == False:
        print("The service type argument should be a non-empty string")
        exit(1)

    if in_service_list(service_type) == False:
        print("The service type is currently unsupported in svmon client")
        exit(1)

    if service_type == "svmon_client":
        print("Getting tag for svmon_client")
        tags.append(get_version())
        return tags

    elif service_type == "gitlab":
        tmp = get_package_version("gitlab", 0 , 1)
        if(enableDebug):
            print('get_service_tag for gitlab result: ', tmp)
        tmp = to_bytes(tmp)
        if tmp == None or tmp == '' or tmp.find('Failed'.encode('utf-8')) >-1:
            print("no gitlab version can be resolved")
            exit(1)
        tags.append(tmp)
        return tags

    elif service_type == "b2safe":
        tmp=get_package_version("b2safe")
        if(enableDebug):
            print('get_service_tag for b2safe result: ', tmp)
        if tmp == "":
            print("no b2safe version can be resolved")
            exit(1)
        tags.append(tmp)

        tmp=get_package_version("irods-server")
        if(enableDebug):
            print('get_service_tag for irods-server result: '+ tmp)
        if tmp != None and tmp != '' and tmp.find('Failed'.encode('utf-8')) == -1:
            tags.append(tmp)
            return tags
        tmp=get_package_version("irods-icat")
        if(enableDebug):
            print('get_service_tag for irods-icat result: '+tmp)
        tmp = to_bytes(tmp)
        if tmp != None and tmp != '' and tmp.find('Failed'.encode('utf-8')) == -1:
            tags.append(tmp)
            return tags
        print("No irods version can be resolved")
        exit(-1)

    elif service_type == "svmon":
        if configs != None and 'svmon_app_path' in configs:
            print('Getting svmon version from config file')
            tags={}
            if configs.get('svmon_app_path') != None and configs.get('svmon_app_path') != '' :
                svmonVersions = get_svmon_version(configs.get('svmon_app_path'))
                tags['svmon'] = [svmonVersions[1], svmonVersions[3]]
                _services['svmon']=[svmonVersions[0], svmonVersions[2]]
            return tags['svmon']
        else:
            print('No svmon configuration to get versions, returning default versions for svmon')
            return _tags['svmon']

    elif service_type == "b2handle" or service_type == "B2HANDLE":
        if configs != None and 'handle_server_path' in configs:
            tags=[]
            if configs.get('handle_server_path') != None and configs.get('handle_server_path') != '' :
                tags.append(get_handle_server(configs.get('handle_server_path')))
            return tags
        else:
            print("No b2handle configuration to get versions")
            exit(1)

def get_package_version(software,start=0,end=0):
    config = remoteConfig.RemoteConfig().getConfig()
    enableDebug = config["DEBUG_MODE"]
    print('Get_package_version for software: '+software)
    if(enableDebug):
        print('Get_package_version for software: '+software)

    if isinstance(software,str)  == False or software == "" or software == None:
        print("Software name should be a non-empty string")
        exit(1)
    if isinstance(start,int) == False or isinstance(end, int) == False:
        print("The input of indices should be integers to fetch correct version,")
        exit(1)


    osSupportsDPKG = False
    try:
        dpkgRunResult = subprocess.check_output("dpkg -l", shell=True, stderr=subprocess.STDOUT)
        osSupportsDPKG = True
    except subprocess.CalledProcessError as e:
        if(enableDebug):
            print("Tried to run dpkg, is not working on this OS, output: ", e.output)

    if osSupportsDPKG == False:
        if(enableDebug):
                print('No dpkg found, running with rpm...')
        return get_by_rpm_packages(software, start,end)

    if(enableDebug):
        print('Dpkg found, running with dpkg...')
    return get_by_dpkg_packages(software,start,end)

# for package version that can be accessed via rpm management
def get_by_dpkg_packages(software,start=0,end=0):
    config = remoteConfig.RemoteConfig().getConfig()
    enableDebug = config["DEBUG_MODE"]
    if(enableDebug):
        print('Get_by_dpkg_packages for software: '+software, start,end)

    softwareListResult = subprocess.Popen("dpkg -l", shell=True, stdout=subprocess.PIPE)
    softwareListResult = subprocess.Popen('grep ' + software, shell=True, stdin=softwareListResult.stdout, stdout=subprocess.PIPE)
    softwareListResult = softwareListResult.communicate()
    if(enableDebug):
        print('Get_by_dpkg_packages final dpkg -l before parse result: ', softwareListResult)

    if softwareListResult[0] == None or softwareListResult == "":
        print('Failed, no dpkg packages can be found for ', software)
        return ''
    softwareListResult = softwareListResult[0]

    return extractVersionFromCommandResult(software.encode('utf-8'), softwareListResult, start,end)

# for package version that can be accessed via rpm management
def get_by_rpm_packages(software,start=0,end=0):
    config = remoteConfig.RemoteConfig().getConfig()
    enableDebug = config["DEBUG_MODE"]
    if(enableDebug):
        print('Get_by_rpm_packages for software: '+software, start,end)

    softwareListResult = subprocess.Popen("rpm -qa", shell=True, stdout=subprocess.PIPE)
    softwareListResult = subprocess.Popen('grep ' + software, shell=True, stdin=softwareListResult.stdout, stdout=subprocess.PIPE)
    softwareListResult = softwareListResult.communicate()
    if(enableDebug):
        print('Get_by_rpm_packages final rpm-qa before parse result: ', softwareListResult)

    if softwareListResult[0] == None or softwareListResult == "":
        print('Failed, no rpm packages can be found for ', software)
        return ''

    return extractVersionFromCommandResult(software, softwareListResult[0], start,end)

def to_bytes(s):
    if type(s) is bytes:
        return s
    elif type(s) is str or (sys.version_info[0] < 3 and type(s) is unicode):
        return codecs.encode(s, 'utf-8')
    else:
        raise TypeError("Expected bytes or string, but got %s." % type(s))

def extractVersionFromCommandResult(software,unparsedVersion, start,end):
    software=to_bytes(software)
    unparsedVersion=to_bytes(unparsedVersion)
    softwareIndex=unparsedVersion.find(software)
    softwareIndex=softwareIndex+len(software)
    versionIndex=unparsedVersion[softwareIndex+1:len(unparsedVersion)]
    versionIndex=to_bytes(versionIndex)
    parsedVersion=versionIndex.split('-'.encode('utf-8'))

    if len(parsedVersion) > end:
        if start == end:
            return ltmp[start]
        elif start < end:
            res=""
            for i in range(start,end+1):
                res=res+ltmp[i]
            return res
        else:
            print('Failed, the start index should be smaller than end index for a correct rpm package resolver')
            return ''
    else:
        print("Failed," + software +" version not resolved")
        return ''

def get_user():
    tmp=subprocess.Popen("whoami",shell=True,stdout=subprocess.PIPE)
    tmp=tmp.communicate()
    return tmp[0].replace('\n','')

def get():
    tags=get_service_tag("svmon_client")
    return tags[0]

def get_handle_server(handle_server_path):
    tmp = subprocess.Popen(handle_server_path, shell=True, stdout = subprocess.PIPE)
    tmp = tmp.communicate()
    if tmp == None and len(tmp) < 2:
        print("Handle server executable is incorrect")
        exit(1)
    tmp = tmp[0].decode("utf-8").split('\n')
    if tmp == None or len(tmp) < 2:
        print("Handle server executable is incorrect")
        exit(1)
    tmp = tmp[0]
    tmp = tmp.split('version')
    return tmp[1].lstrip()

# get svmon backend and frontend versions
def get_svmon_version(svmon_app_path):
    config = remoteConfig.RemoteConfig().getConfig()
    cwd = os.path.dirname(svmon_app_path + '/scripts/')
    filename = cwd + "/getVersions.bash"

    if os.path.exists(filename) == False:
        print("Svmon path does not exists or missing getVersions.bash")
        exit(-1)

    if os.access(filename,os.R_OK) == False:
        print("You have no access to read script file: getVersions.bash")
        exit(-1)

    svmonVersionExecResult = subprocess.Popen(filename, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    svmonVersionExecResult = svmonVersionExecResult.communicate()

    if svmonVersionExecResult == None and len(svmonVersionExecResult) < 1:
        print("Svmon path executable is incorrect")
        exit(1)

    # [,svmon-frontend, frontendVersion, svmon-backend, backendVersion,]
    svmonVersionsArray = svmonVersionExecResult[0].decode('utf-8').split(',')
    enableDebug = config["DEBUG_MODE"]
    if(enableDebug):
        print('SvmonVersionsArray: ')
        print(svmonVersionsArray)
        print('Length: ', len(svmonVersionsArray))

    if len(svmonVersionsArray) < 5:
        print("No versions were found for svmon")
        exit(1)

    frontendName = svmonVersionsArray[1].lstrip()
    frontendVersion = svmonVersionsArray[2].lstrip()
    backendName = svmonVersionsArray[3].lstrip()
    backendVersion = svmonVersionsArray[4].lstrip()

    return [frontendName, frontendVersion, backendName, backendVersion]

#get svmon client version
def get_version():
    config = remoteConfig.RemoteConfig().getConfig()
    enableDebug = config["DEBUG_MODE"]
    if(python_version() >= '3.0'):
        if(enableDebug):
            print("Running getVersion() for python3...")
        tmp = subprocess.Popen('python3 -m pip show svmon-client', shell=True, stdout=subprocess.PIPE)
    else:
        if(enableDebug):
            print("Running getVersion() for python2...")
        tmp = subprocess.Popen('python -m pip show svmon-client', shell=True, stdout=subprocess.PIPE)

    tmp = subprocess.Popen('grep Version', shell=True, stdin=tmp.stdout, stdout=subprocess.PIPE)
    tmp = tmp.communicate()
    tmp = tmp[0]
    if tmp == '' or tmp == None:
        print("No svmon client has been installed, please refer to https://gitlab.eudat.eu/EUDAT-TOOLS/SVMON/pysvmon")
        exit(1)
    ltmp = tmp.decode("utf-8").split('\n')
    ltmp = ltmp[0].split(':')
    if ltmp == None or len(ltmp) < 2:
        print("SVMON client can not be resolved, please check for installation")
        exit(1)
    ltmp = ltmp[1]
    ltmp.replace("\n", "")
    return ltmp

if __name__ == "__main__":
    print(get())
