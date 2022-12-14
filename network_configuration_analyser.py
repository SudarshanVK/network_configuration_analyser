"""
This tool analysis network configuration to generate a configuration analysis 
report and network graph. It utilises batfish as its analyser engine and N2G 
to plot network graphs.

The analysis report is a excel spreadsheet that catptures the following 
information in tabs.
- Node Properties
- Interface Properties
- VLAN Properties
- IP Owners
- Layer3 Edges
- MLAG Properties
- OSPF Configuration
- OSPF Interface Configuration
- OSPF Session Compatability
- BGP Configuration
- BGP Peer Configuration
- BGP Session Compatability
- Routing Table
- F5 VIP Configuration
- Named Structures
- Structure Definations
- References Structures
- Undefined Structure References
- Unused Structures

In addition to the analysis report, it also produces three sets of network
graphs which can be opened and edited by diagrams.net desktop or diagrams.net 
web applications
- OSPF Graph
- BGP Graph
- L3 Network Graph
"""
import json
import pathlib
import logging
import pandas as pd

from N2G import drawio_diagram
from pybatfish.client.commands import *
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints
from pybatfish.datamodel import *
from colorama import Fore, init

# Set warnings level to ERROR -> Change this if you need more logs for debugging
logging.getLogger('pybatfish').setLevel(logging.ERROR)

# Auto-reset colorama colours back after each print statement
init(autoreset=True)

#Initialize a Drawing
diagram = drawio_diagram()

#Accepts a network name and snapshot path as input.
NETWORK_NAME = input("ENTER NETWORK NAME: ")
BASE_SNAPSHOT_PATH = input("ENTER SNAPSHOT PATH: ")
# NETWORK_NAME = "Home_network"
BASE_SNAPSHOT_NAME = "batfish-candidate"
# BASE_SNAPSHOT_PATH = "./network/Home/"

## establish the node on which batfish application is running
bf_session.host = "127.0.0.1" # <batfish_service_ip>

def initialise_batfish():
    # Load all the questions.
    load_questions()
    # Initialises batfish.
    bf_set_network(NETWORK_NAME)
    bf_init_snapshot(BASE_SNAPSHOT_PATH, name=BASE_SNAPSHOT_NAME, overwrite=True)

def analyse_network(report_dir):
    """
    This function runs batfish questions and captures the query results into 
    a spread sheet.

    :param report_dir: defines the directory in which the analysis report gets 
                        saved
    """
    # Captures the status of the configurations that were Parsed.
    parse_status = bfq.fileParseStatus().answer().frame()
    # Batfish question to extract node properties
    print(Fore.YELLOW + " ==> GETTING NODE PROPERTIES")
    np = bfq.nodeProperties().answer().frame()
    # Batfish question to extract interface properties
    print(Fore.YELLOW + " ==> GETTING INTERFACE PROPERTIES")
    interface = bfq.interfaceProperties().answer().frame()
    # Batfish question to extract VLAN properties
    print(Fore.YELLOW + " ==> GETTING VLAN PROPERTIES")
    vlan_prop = bfq.switchedVlanProperties().answer().frame()
    # Batfish question to extract IP Owners
    print(Fore.YELLOW + " ==> GETTING IPOWNERS")
    ip_owners = bfq.ipOwners().answer().frame()
    # Batfish question to extract L3 edges
    print(Fore.YELLOW + " ==> GETTING L3 EDGES")
    l3edge = bfq.layer3Edges().answer().frame()
    # Batfish question to extract MPLAG properties
    print(Fore.YELLOW + " ==> GETTING MLAG PROPERTIES")
    mlag = bfq.mlagProperties().answer().frame()
    # Batfish question to extract OSPF configuration
    print(Fore.YELLOW + " ==> GETTING OSPF CONFIGURATION")
    ospf_config = bfq.ospfProcessConfiguration().answer().frame()
    # Batfish question to extract OSPF area configuration
    print(Fore.YELLOW + " ==> GETTING OSPF AREA CONFIGURATION")
    ospf_area_config = bfq.ospfAreaConfiguration().answer().frame()
    # Batfish question to extract OSPF interface configuration
    print(Fore.YELLOW + " ==> GETTING OSPF INTERFACE CONFIGURATION")
    ospf_interface = bfq.ospfInterfaceConfiguration().answer().frame()
    # Batfish question to extract OSPF Session compatability
    print(Fore.YELLOW + " ==> GETTING OSPF SESSION COMPATABILITY")
    ospf_session = bfq.ospfSessionCompatibility().answer().frame()
    # Batfish question to extract BGP configuration
    print(Fore.YELLOW + " ==> GETTING BGP CONFIGURATION")
    bgp_config = bfq.bgpProcessConfiguration().answer().frame()
    # Batfish question to extract BGP peer configuration
    print(Fore.YELLOW + " ==> GETTING BGP PEER CONFIGURATION")
    bgp_peer_config = bfq.bgpPeerConfiguration().answer().frame()
    # Batfish question to extract BGP session compatibility
    print(Fore.YELLOW + " ==> GETTING BGP SESSION COMPATIBILITY")
    bgp_session = bfq.bgpSessionStatus().answer().frame()
    # Batfish question to extract routing table
    print(Fore.YELLOW + " ==> GETTING ROUTE TABLE")
    routing = bfq.routes().answer().frame()
    # Batfish question to extract F5 VIP configuration
    print(Fore.YELLOW + " ==> GETTING F5 VIP CONFIGURATION")
    f5_vip = bfq.f5BigipVipConfiguration().answer().frame()
    # Batfish question to extract Named Structures
    print(Fore.YELLOW + " ==> GETTING NAMED STRUCTURES")
    named_structure = bfq.namedStructures().answer().frame()
    # Batfish question to extract Structure deginitions
    print(Fore.YELLOW + " ==> GETTING STRUCTURE DEFINITIONS")
    def_structure = bfq.definedStructures().answer().frame()
    # Batfish question to extract referenced structures
    print(Fore.YELLOW + " ==> GETTING REFERENCED STRUCTURES")
    ref_structure = bfq.referencedStructures().answer().frame()
    # Batfish question to extract undefined references
    print(Fore.YELLOW + " ==> GETTING UNDEFINED STRUCTURE REFERENCES")
    undefined_references = bfq.undefinedReferences().answer().frame()
    # Batfish question to extract used structures
    print(Fore.YELLOW + " ==> GETTING UNUSED STRUCTURES")
    unused_structure = bfq.unusedStructures().answer().frame()
    # Setting the path and file name were the analysis report will be saved
    analysis_report_file = report_dir + "/" + NETWORK_NAME + "_analysis_report.xlsx"
    print(Fore.YELLOW + " ==> GENERATING REPORT")
    # Writes previously computed configuration analysis into a excel file
    with pd.ExcelWriter(analysis_report_file) as f:
        parse_status.to_excel(f,sheet_name="parse_satus", engine="xlsxwriter")
        np.to_excel(f, sheet_name="node_properties", engine="xlsxwriter")
        interface.to_excel(f, sheet_name="interface_properties", engine="xlsxwriter")
        vlan_prop.to_excel(f, sheet_name="vlan_properties", engine="xlsxwriter")
        ip_owners.to_excel(f, sheet_name="IPOwners", engine="xlsxwriter")
        l3edge.to_excel(f, sheet_name="l3edges", engine="xlsxwriter")
        mlag.to_excel(f, sheet_name="mlag", engine="xlsxwriter")
        ospf_session.to_excel(f, sheet_name="ospf_session", engine="xlsxwriter")
        ospf_config.to_excel(f, sheet_name="ospf_config", engine="xlsxwriter")
        ospf_area_config.to_excel(f, sheet_name="ospf_area_config", engine="xlsxwriter")
        ospf_interface.to_excel(f, sheet_name="ospf_interface", engine="xlsxwriter")
        bgp_config.to_excel(f, sheet_name="bgp_config", engine="xlsxwriter")
        bgp_peer_config.to_excel(f, sheet_name="bgp_peer_config", engine="xlsxwriter")
        bgp_session.to_excel(f, sheet_name="bgp_session", engine="xlsxwriter")
        routing.to_excel(f, sheet_name="routing_table", engine="xlsxwriter")
        f5_vip.to_excel(f, sheet_name="f5_vip", engine="xlsxwriter")
        named_structure.to_excel(f, sheet_name="named_structure", engine="xlsxwriter")
        def_structure.to_excel(f, sheet_name="defined_structures", engine="xlsxwriter")
        ref_structure.to_excel(
            f, sheet_name="referrenced_structures", engine="xlsxwriter"
        )
        undefined_references.to_excel(
            f, sheet_name="undefined_references", engine="xlsxwriter"
        )
        unused_structure.to_excel(f, sheet_name="unused_structure", engine="xlsxwriter")


def plot_ospf_graph():
    """
    This function extracts OSPF session compatibility and plots a graph of 
    OSPF neighborships.
    """
    # Run batfish query to identify OSPF session compatibility
    ospfneigh = bfq.ospfSessionCompatibility().answer().frame()
    # Conditional check to ensure the OSPF session list is not empty
    if ospfneigh.empty:
        print (Fore.RED + " ==> NO OSPF NEIGHBORS FOUND")
    else:
        print(Fore.YELLOW + " ==> PLOTTING OSPF GRAPH")
        ospfneigh_json = json.loads(ospfneigh.to_json(orient="index"))
        # print (json.dumps(ospfneigh_json, indent=4))
        # Initialise list to track nodes that are already plotted.
        mapped_node = []
        # Initialise list to track links that are already plotted
        mapped_link_list = []
        # initialise a drawing named OSPF
        diagram.add_diagram("OSPF")
        # Loop through each neighborship that batfish analysis has produced.
        for key in ospfneigh_json:
            # Initialise local list to map current link and reverse of current link.
            current_link = []
            current_link_reverse = []
            # Extract details of the neighbor
            neighbor = ospfneigh_json[key]
            # Extract node id and remote node if of neighbor
            node_id = f'{neighbor["Interface"]["hostname"]}'
            remote_node_id = f'{neighbor["Remote_Interface"]["hostname"]}'
            # Check if node has already been plotted
            # plot the node it is not and add node to mapped_node list
            if node_id not in mapped_node:
                diagram.add_node(id=f"{node_id}")
                mapped_node.append(node_id)
            # Check if remote node has already been plotted
            # plot the remote node is not and add remote node to mapped_node list
            if remote_node_id not in mapped_node:
                diagram.add_node(id=f"{remote_node_id}")
                mapped_node.append(remote_node_id)
            # Extract details of current link and reverse of the current link
            current_link = [f"{node_id}", f"{remote_node_id}"]
            current_link_reverse = [f"{remote_node_id}", f"{node_id}"]
            # Check if the current link is in the mapped link list
            # if not, plot the link and add both the link and the reverse of the link
            # to the mapped link list
            if current_link not in mapped_link_list:
                diagram.add_link(
                    f"{node_id}",
                    f"{remote_node_id}",
                    label=f'{node_id}({neighbor["IP"]})(AreaID={neighbor["Area"]})'
                    f' == {neighbor["Session_Status"]}'
                    f' == {remote_node_id}({neighbor["Remote_IP"]})(AreaID={neighbor["Remote_Area"]}',
                )
                mapped_link_list.extend((current_link, current_link_reverse))

def plot_bgp_graph():
    """
    This function extracts BGP session compatibility and plots a graph of 
    BGP neighborships.
    """ 
    # Run batfish query to identify BGP neighbors
    bgpneigh = bfq.bgpSessionStatus().answer().frame()
    # Conditional check to ensure the BGP session list is not empty
    if bgpneigh.empty:
        print(Fore.RED + " ==> NO BGP NEIGHBORS FOUND")
    else:
        print(Fore.YELLOW + " ==> PLOTTING BGP GRAPH")
        bgpneigh_json = json.loads(bgpneigh.to_json(orient="index"))
        # Initialise list to track nodes that are already plotted.
        mapped_node = []
        # Initialise list to track links that are already plotted
        mapped_link_list = []
        # initialise a drawing named BGP
        diagram.add_diagram("BGP")
        for key in bgpneigh_json:
            # Initialise local list to map current link and reverse of current link.
            current_link = []
            current_link_reverse = []
            # Extract details of the neighbor
            neighbor = bgpneigh_json[key]
            # Extract node id and remote node if of each neighbor
            node_id = f'{neighbor["Node"]}\n({neighbor["Local_AS"]})'
            remote_node_id = f'{neighbor["Remote_Node"]}\n({neighbor["Remote_AS"]})'
            # Check if node has already been plotted
            # plot the node is not and add node to mapped_node list
            if node_id not in mapped_node:
                diagram.add_node(id=f"{node_id}")
                mapped_node.append(node_id)
            # Check if remote node has already been plotted
            # plot the remote node is not and add remote node to mapped_node list
            if remote_node_id not in mapped_node:
                diagram.add_node(id=f"{remote_node_id}")
                mapped_node.append(remote_node_id)
            # Extract details of current link and reverse of the current link
            current_link = [f"{node_id}", f"{remote_node_id}"]
            current_link_reverse = [f"{remote_node_id}", f"{node_id}"]
            if current_link not in mapped_link_list:
                diagram.add_link(
                    f"{node_id}",
                    f"{remote_node_id}",
                    label=f'{node_id}({neighbor["Local_IP"]})'
                    f' == {neighbor["Established_Status"]}'
                    f' == {remote_node_id}({neighbor["Remote_IP"]})',
                )
                mapped_link_list.extend((current_link, current_link_reverse))

def plot_l3_graph():
    """
    This function extracts L3 edges and plots a graph of L3 relationships
    """
    # Run batfish query to identify L3 edges
    l3edges = bfq.layer3Edges().answer().frame()
    # Conditional check to ensure the L3 edges list is not empty
    if l3edges.empty:
        print(Fore.RED + " ==> NO L3 ADJENCIES FOUND")
    else:
        print(Fore.YELLOW + " ==> PLOTTING L3 NETWORK GRAPH")
        l3edges_json = json.loads(l3edges.to_json(orient="index"))
        # Initialise list to track nodes that are already plotted.
        mapped_node = []
        # Initialise list to track links that are already plotted
        # initialise a drawing named L3
        diagram.add_diagram("L3")
        # Initialise local list to map current link and reverse of current link.
        current_link = []
        current_link_reverse = []
        for key in l3edges_json:
            # Extract details of the neighbor
            neighbor = l3edges_json[key]
            node_id = f'{neighbor["Interface"]["hostname"]}'
            remote_node_id = f'{neighbor["Remote_Interface"]["hostname"]}'
            # Check if node has already been plotted
            # plot the node is not and add node to mapped_node list
            if node_id not in mapped_node:
                diagram.add_node(id=f"{node_id}")
                mapped_node.append(node_id)
            # Check if remote node has already been plotted
            # plot the remote node is not and add remote node to mapped_node list
            if remote_node_id not in mapped_node:
                diagram.add_node(id=f"{remote_node_id}")
                mapped_node.append(remote_node_id)
            diagram.add_link(
                f"{node_id}",
                f"{remote_node_id}",
                label=f'{node_id}({neighbor["IPs"]})'
                f' == VLAN {key}'
                f' == {remote_node_id}({neighbor["Remote_IPs"]})',
                )      

def main():

    # Initialise batfish engine
    initialise_batfish()
    # Creates a new Folder to store reports
    report_dir = NETWORK_NAME + "_Reports"
    pathlib.Path(report_dir).mkdir(exist_ok=True)
    # Extract node propertied using batfish question and write to file
    print(Fore.CYAN
        + "\n===> ANALYSING CONFIGURATIONS ")
    analyse_network(report_dir)
    # Plot network grapf
    print(Fore.CYAN + "\n===> PLOTTING NETWORK GRAPHS")
    plot_ospf_graph()
    plot_bgp_graph()
    plot_l3_graph()
    diagram.layout(algo="kk")
    diagram_file_name = report_dir + "/" + NETWORK_NAME + "_network_map.drawio"
    diagram.dump_file(filename= diagram_file_name, folder="./")

    print (Fore.GREEN
            + "\n***************************************************************"
            + "\n*          NETWORK CONFIGURATION ANALYSIS COMPLETE            *"
            + "\n***************************************************************"
            )

if __name__ == "__main__":
    main()
