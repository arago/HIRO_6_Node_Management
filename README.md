# HIRO 6 Nodes
Helpers for HIRO MARS

#### NodeManagement.py

Requirements: python3 and pip3

OS: CentOS and RedHat

Modules: requests json glob urllib urllib3

Use this Python script to load nodes to a HIRO 6.x instance. The source nodes must be in JSON format. The script will ask whether you want to perform a creation, update. deletion or create edges.

Hint: Export nodes with this command

Sample file content for for node creation:

     {"ogit/name":"Node1", "ogit/_owner":"arago.co", "/CustomAttribute":"MyAttr"}
     {"ogit/name":"Node2", "ogit/_owner":"arago.co", "/CustomAtrribute":"5"}

Sample file content for edge creation:

cjsvyoihfggejjskkuurn76rf
cjstyuppgjf775jfngw9dnfg7
