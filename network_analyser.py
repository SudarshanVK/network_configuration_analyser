## Imports batfish functions
from pybatfish.client.commands import *
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints
from pybatfish.datamodel import *
from colorama import Fore, init

import json
from N2G import drawio_diagram
import pandas as pd
import os
import pathlib

# Set warnings level to ERROR -> Change this if you need more logs for debugging
import logging
logging.getLogger('pybatfish').setLevel(logging.ERROR)

# Auto-reset colorama colours back after each print statement
init(autoreset=True)

#Initialize a Drawing
diagram = drawio_diagram()


# NETWORK_NAME = input("Enter network name: ")
# BASE_SNAPSHOT_NAME = input("Enter Snapshot name: ")
# BASE_SNAPSHOT_PATH = input("Enter Snapshot Path: ")
NETWORK_NAME = "Home_network"
BASE_SNAPSHOT_NAME = "batfish-candidate"
BASE_SNAPSHOT_PATH = "./network/Home/"

## establish the node on which batfish application is running
# <batfish_service_ip>
bf_session.host = "127.0.0.1"




def initialise_batfish():
    ## Load all the questions.
    load_questions()
    bf_set_network(NETWORK_NAME)
    bf_init_snapshot(BASE_SNAPSHOT_PATH, name=BASE_SNAPSHOT_NAME, overwrite=True)


def analyse_network(report_dir):
    parse_status = bfq.fileParseStatus().answer().frame()
    print(Fore.YELLOW + " ==> GETTING NODE PROPERTIES")
    # Batfish extract node properties and write to an excel file
    np = bfq.nodeProperties().answer().frame()
    print(Fore.YELLOW + " ==> GETTING INTERFACE PROPERTIES")
    # Batfish extract interface properties and write to excel file
    interface = bfq.interfaceProperties().answer().frame()
    print(Fore.YELLOW + " ==> GETTING VLAN PROPERTIES")
    vlan_prop = bfq.switchedVlanProperties().answer().frame()
    print(Fore.YELLOW + " ==> GETTING IPOWNERS")
    # Batfish extract IP addresses and write to an excel file
    ip_owners = bfq.ipOwners().answer().frame()
    print(Fore.YELLOW + " ==> GETTING L3 EDGES")
    # Batfish extract L3 edges and write to an excel file
    l3edge = bfq.layer3Edges().answer().frame()
    print(Fore.YELLOW + " ==> GETTING MLAG PROPERTIES")
    # Batfish extract OSPF session compatibility info and write to an excel file
    mlag = bfq.mlagProperties().answer().frame()
    print(Fore.YELLOW + " ==> GETTING OSPF CONFIGURATION")
    # Batfish extract OSPF configuration info and write to an excel file
    ospf_config = bfq.ospfProcessConfiguration().answer().frame()
    print(Fore.YELLOW + " ==> GETTING OSPF AREA CONFIGURATION")
    # Batfish extract OSPF configuration info and write to an excel file
    ospf_area_config = bfq.ospfAreaConfiguration().answer().frame()
    print(Fore.YELLOW + " ==> GETTING OSPF INTERFACE CONFIGURATION")
    # Batfish extract OSPF interface configuration info and write to an excel file
    ospf_interface = bfq.ospfInterfaceConfiguration().answer().frame()
    print(Fore.YELLOW + " ==> GETTING OSPF SESSION COMPATABILITY")
    # Batfish extract OSPF session compatibility info and write to an excel file
    ospf_session = bfq.ospfSessionCompatibility().answer().frame()
    print(Fore.YELLOW + " ==> GETTING BGP CONFIGURATION")
    # Batfish extract BGP configuration info and write to an excel file
    bgp_config = bfq.bgpProcessConfiguration().answer().frame()
    print(Fore.YELLOW + " ==> GETTING BGP PEER CONFIGURATION")
    bgp_peer_config = bfq.bgpPeerConfiguration().answer().frame()
    print(Fore.YELLOW + " ==> GETTING BGP SESSION COMPATIBILITY")
    # Batfish extract BGP session status info and write to an excel file
    bgp_session = bfq.bgpSessionStatus().answer().frame()
    print(Fore.YELLOW + " ==> GETTING ROUTE TABLE")
    # Batfish to extract routing table
    routing = bfq.routes().answer().frame()
    print(Fore.YELLOW + " ==> GETTING F5 VIP CONFIGURATION")
    f5_vip = bfq.f5BigipVipConfiguration().answer().frame()
    print(Fore.YELLOW + " ==> GETTING NAMED STRUCTURES")
    named_structure = bfq.namedStructures().answer().frame()
    print(Fore.YELLOW + " ==> GETTING STRUCTURE DEFINITIONS")
    def_structure = bfq.definedStructures().answer().frame()
    print(Fore.YELLOW + " ==> GETTING REFERENCED STRUCTURES")
    ref_structure = bfq.referencedStructures().answer().frame()
    print(Fore.YELLOW + " ==> GETTING UNDEFINED STRUCTURE REFERENCES")
    undefined_references = bfq.undefinedReferences().answer().frame()
    print(Fore.YELLOW + " ==> GETTING UNUSED STRUCTURES")
    unused_structure = bfq.unusedStructures().answer().frame()

    analysis_report_file = report_dir + "/" + NETWORK_NAME + "_analysis_report.xlsx"
    print(Fore.YELLOW + " ==> GENERATING REPORT")
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
    # Run batfish query to identify OSPF neighbors
    ospfneigh = bfq.ospfSessionCompatibility().answer().frame()
    if (ospfneigh.empty):
        print (Fore.RED + " ==> NO OSPF NEIGHBORS FOUND")
    else:
        print(Fore.YELLOW + " ==> PLOTTING OSPF GRAPH")
        ospfneigh_json = json.loads(ospfneigh.to_json(orient="index"))
        # print (json.dumps(ospfneigh_json, indent=4))
        # Initialise list to track nodes that are already plotted.
        mapped_node = []
        # Initialise list to track links that are already plotted
        mapped_link_list = []
        # initialise a drawing names OSPF
        diagram.add_diagram("OSPF")
        # Loop through each neighborship that batfish analysis has produced.
        for key in ospfneigh_json:
            # Initialise local list to map current link and reverse of current link.
            current_link = []
            current_link_reverse = []
            # Extract details of the neighbor
            neighbor = ospfneigh_json[key]
            # print (json.dumps(neighbor, indent=4))
            # Extract node id and remote node if of each neighbor
            node_id = f'{neighbor["Interface"]["hostname"]}'
            remote_node_id = f'{neighbor["Remote_Interface"]["hostname"]}'
            # print (node_id)
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
            # print (f" Current Link {current_link_list}")
            # print (f" Reverse of Current Link {current_link_list_reverse}")
            # Check if the current link is in the mapped link list
            # if not, plot the link and add both the link and the reverse of the link
            # to the mapped link list
            if current_link not in mapped_link_list:
                # print ("link not mapped")
                diagram.add_link(
                    f"{node_id}",
                    f"{remote_node_id}",
                    label=f'{node_id}({neighbor["IP"]})(AreaID={neighbor["Area"]})'
                    f' == {neighbor["Session_Status"]}'
                    f' == {remote_node_id}({neighbor["Remote_IP"]})(AreaID={neighbor["Remote_Area"]}',
                )
                mapped_link_list.append(current_link)
                mapped_link_list.append(current_link_reverse)
            #     print (f" Mapped Link {mapped_link_list}\n")
            # else:
            #     print (" Link already mapped\n")

def plot_bgp_graph():   
    # Run batfish query to identify BGP neighbors
    bgpneigh = bfq.bgpSessionStatus().answer().frame()
    if (bgpneigh.empty):
        print(Fore.RED + " ==> NO BGP NEIGHBORS FOUND")
    else:
        print(Fore.YELLOW + " ==> PLOTTING BGP GRAPH")
        bgpneigh_json = json.loads(bgpneigh.to_json(orient="index"))
        # print (json.dumps(bgpneigh_json, indent=4))
        # Initialise list to track nodes that are already plotted.
        # Initialise list to track nodes that are already plotted.
        mapped_node = []
        # Initialise list to track links that are already plotted
        mapped_link_list = []
        # initialise a drawing names BGP
        diagram.add_diagram("BGP")
        for key in bgpneigh_json:
            # Initialise local list to map current link and reverse of current link.
            current_link = []
            current_link_reverse = []
            # Extract details of the neighbor
            neighbor = bgpneigh_json[key]
            # print (json.dumps(neighbor, indent=4))
            # Extract node id and remote node if of each neighbor
            node_id = f'{neighbor["Node"]}\n({neighbor["Local_AS"]})'
            remote_node_id = f'{neighbor["Remote_Node"]}\n({neighbor["Remote_AS"]})'
            # print(node_id)
            # print(remote_node_id)
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
                # print ("link not mapped")
                diagram.add_link(
                    f"{node_id}",
                    f"{remote_node_id}",
                    label=f'{node_id}({neighbor["Local_IP"]})'
                    f' == {neighbor["Established_Status"]}'
                    f' == {remote_node_id}({neighbor["Remote_IP"]})',
                )
                mapped_link_list.append(current_link)
                mapped_link_list.append(current_link_reverse)
            #     print (f" Mapped Link {mapped_link_list}\n")
            # else:
            #     print (" Link already mapped\n")

def plot_l3_graph():
    # Run batfish query to identify L3 edges
    l3edges = bfq.layer3Edges().answer().frame()
    if (l3edges.empty):
        print(Fore.RED + " ==> NO L3 ADJENCIES FOUND")
    else:
        print(Fore.YELLOW + " ==> PLOTTING L3 NETWORK GRAPH")
        l3edges_json = json.loads(l3edges.to_json(orient="index"))
        # print (json.dumps(l3edges_json, indent=4))
        # # Initialise list to track nodes that are already plotted.
        mapped_node = []
        # # Initialise list to track links that are already plotted
        # mapped_link_list = []
        # # initialise a drawing names OSPF
        diagram.add_diagram("L3")
        for key in l3edges_json:
            # Initialise local list to map current link and reverse of current link.
            current_link = []
            current_link_reverse = []
            # Extract details of the neighbor
            neighbor = l3edges_json[key]
            # print (key)
            # print (json.dumps(neighbor, indent=4))
            node_id = f'{neighbor["Interface"]["hostname"]}'
            remote_node_id = f'{neighbor["Remote_Interface"]["hostname"]}'
            # print(node_id)
            # print(remote_node_id)
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
            + "\n*        CHECK CURRENT WORKING DIRECTORY FOR REPORTS          *"
            + "\n***************************************************************"
            )



if __name__ == "__main__":
    main()
