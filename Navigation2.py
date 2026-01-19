import os
import cv2
import networkx as nx
from flask import Flask, render_template, request, jsonify
import numpy as np

# --- Core Data Structures (Rooms and Graph) ---

# 1. Room List: Dictionary of rooms with properties (Imported from Navigation.py)
rooms = {
    "G-03": {
        "building": "North",
        "floor": "G",
        "room_type": "Lecture Hall",
        "connected_node": "north_g_main_junction"
    },
    "G-14": {
        "building": "North",
        "floor": "G",
        "room_type": "Instrument Store",
        "connected_node": "north_g_main_junction"
    },
    "G-01": {
        "building": "North",
        "floor": "G",
        "room_type": "Lecture Hall",
        "connected_node": "north_g_east_junction"
    },
    "G-02": {
        "building": "North",
        "floor": "G",
        "room_type": "Lecture Hall",
        "connected_node": "north_g_east_junction"
    },
    "G-05": {
        "building": "North",
        "floor": "G",
        "room_type": "Projection Room",
        "connected_node": "north_g_east_junction"
    },
    "G-06": {
        "building": "North",
        "floor": "G",
        "room_type": "Standards Laboratory",
        "connected_node": "north_g_west_junction"
    },
    "G-07": {
        "building": "North",
        "floor": "G",
        "room_type": "Computer Reception",
        "connected_node": "north_g_west_junction"
    },
    "G-09": {
        "building": "North",
        "floor": "G",
        "room_type": "Acoustics Store",
        "connected_node": "north_g_west_junction"
    },
    "G-08": {
        "building": "North",
        "floor": "G",
        "room_type": "Acoustics Control room",
        "connected_node": "north_g_west_junction"
    },
    "G-10": {
        "building": "North",
        "floor": "G",
        "room_type": "Acoustics Lab",
        "connected_node": "north_g_west_junction"
    },
    "G-11": {
        "building": "North",
        "floor": "G",
        "room_type": "High Vacuum & Semiconductor Research Lab",
        "connected_node": "north_g_west_south_junction"
    },
    "G-13": {
        "building": "North",
        "floor": "G",
        "room_type": "Clean Room",
        "connected_node": "north_g_west_south_junction"
    },
    "G-12": {
        "building": "North",
        "floor": "G",
        "room_type": "Materials Science",
        "connected_node": "north_g_south_junction"
    },
    "G-26": {
        "building": "North",
        "floor": "G",
        "room_type": "High-Voltage Lab",
        "connected_node": "north_g_south_junction"
    },
    "G-25": {
        "building": "North",
        "floor": "G",
        "room_type": "Generator Research Lab",
        "connected_node": "north_g_south_junction"
    },
    "G-20": {
        "building": "North",
        "floor": "G",
        "room_type": "Heavy Current Workshop",
        "connected_node": "north_g_south_junction"
    },
    "G-24": {
        "building": "North",
        "floor": "G",
        "room_type": "Machinery Hall",
        "connected_node": "north_g_south_junction"
    },
    "1-10": {
        "building": "North",
        "floor": "1",
        "room_type": "Printed Circuit Processing Lab",
        "connected_node": "north_1_west_junction"
    },
    "1-11": {
        "building": "North",
        "floor": "1",
        "room_type": "Printed Circuit Photo-graphical",
        "connected_node": "north_1_west_junction"
    },
    "1-12": {
        "building": "North",
        "floor": "1",
        "room_type": "Dark Room",
        "connected_node": "north_1_west_junction"
    },
    "1-01": {
        "building": "North",
        "floor": "1",
        "room_type": "Post Graduate Office",
        "connected_node": "north_1_east_junction"
    },
    "1-02": {
        "building": "North",
        "floor": "1",
        "room_type": "Air Conditioned Motor Room",
        "connected_node": "north_1_east_junction"
    },
    "1-13": {
        "building": "North",
        "floor": "1",
        "room_type": "Control Research",
        "connected_node": "north_1_west_junction"
    },
    "1-14": {
        "building": "North",
        "floor": "1",
        "room_type": "Kitchen",
        "connected_node": "north_1_west_junction"
    },
    "1-30": {
        "building": "North",
        "floor": "1",
        "room_type": "Small Machines Lab",
        "connected_node": "north_1_main_junction"
    },
    "1-27": {
        "building": "North",
        "floor": "1",
        "room_type": "Illumination Lab",
        "connected_node": "north_1_main_junction"
    },
    "1-25": {
        "building": "North",
        "floor": "1",
        "room_type": "Power Electronics Lab",
        "connected_node": "north_1_main_junction"
    },
    "2-01": {
        "building": "North",
        "floor": "2",
        "room_type": "Advanced Communication Lab",
        "connected_node": "north_2_east_junction"
    },
    "2-02": {
        "building": "North",
        "floor": "2",
        "room_type": "Communication Lab",
        "connected_node": "north_2_east_junction"
    },
    "2-11": {
        "building": "North",
        "floor": "2",
        "room_type": "Communication Development Lab",
        "connected_node": "north_2_west_junction"
    },
    "3-01": {
        "building": "North",
        "floor": "3",
        "room_type": "Machine Research Lab",
        "connected_node": "north_3_east_junction"
    },
    "4-01": {
        "building": "North",
        "floor": "4",
        "room_type": "Digital Proccesses Lab",
        "connected_node": "north_4_east_junction"
    },
    "5-01": {
        "building": "North",
        "floor": "5",
        "room_type": "Microwave Lab",
        "connected_node": "north_5_east_junction"
    },
    "2-07s": {
        "building": "South",
        "floor": "2",
        "room_type": "2nd Year Laboratory",
        "connected_node": "south_2_main_junction"
    },
    "2-13s": {
        "building": "South",
        "floor": "2",
        "room_type": "4th Year Control Laboratory",
        "connected_node": "south_2_east_junction"
    },
    "2-14s": {
        "building": "South",
        "floor": "2",
        "room_type": "Digital Systems Laboratory",
        "connected_node": "south_2_east_junction"
    },
    "2-15s": {
        "building": "South",
        "floor": "2",
        "room_type": "DSP Laboratory",
        "connected_node": "south_2_east_junction"
    },
    "1-13s": {
        "building": "South",
        "floor": "1",
        "room_type": "3rd Year Laboratory",
        "connected_node": "south_1_west_junction"
    },
    "1-14s": {
        "building": "South",
        "floor": "1",
        "room_type": "4th Year Electronic Computer Lab",
        "connected_node": "south_1_main_junction"
    },
    "1-15s": {
        "building": "South",
        "floor": "1",
        "room_type": "4th Year Electrical Computer Lab",
        "connected_node": "south_1_main_junction"
    },
    "1-16s": {
        "building": "South",
        "floor": "1",
        "room_type": "3rd Year Electronic Computer Lab",
        "connected_node": "south_1_main_junction"
    },
    "G-06s": {
        "building": "South",
        "floor": "G",
        "room_type": "All Year Design Laboratory",
        "connected_node": "south_g_west_junction"
    },
    "G-07s": {
        "building": "South",
        "floor": "G",
        "room_type": "4th Year Computer Design Lab",
        "connected_node": "south_g_main_junction"
    },
    "G-08s": {
        "building": "South",
        "floor": "G",
        "room_type": "2nd Year & 24-Hour Computer Lab",
        "connected_node": "south_g_main_junction"
    },
    "B-03s": {
        "building": "South",
        "floor": "B",
        "room_type": "Machines & Drives Lab",
        "connected_node": "south_B_main_junction"
    },
    "1-04": {
        "building": "North",
        "floor": "1",
        "room_type": "Office",
        "connected_node": "north_1_main_junction"
    },
    "1-06": {
        "building": "North",
        "floor": "1",
        "room_type": "Academic Staff Room",
        "connected_node": "north_1_main_junction"
    },
    "1-07": {
        "building": "North",
        "floor": "1",
        "room_type": "Departmental Records",
        "connected_node": "north_1_main_junction"
    },
    "1-08": {
        "building": "North",
        "floor": "1",
        "room_type": "Store Room",
        "connected_node": "north_1_main_junction"
    },
    "1-17": {
        "building": "North",
        "floor": "1",
        "room_type": "Store Room",
        "connected_node": "north_1_main_junction"
    },
    "5-05": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_main_junction"
    },
    "1-12s": {
        "building": "South",
        "floor": "1",
        "room_type": "Office",
        "connected_node": "south_1_main_junction"
    },
    "3-03": {
        "building": "North",
        "floor": "3",
        "room_type": "Office",
        "connected_node": "north_3_east_junction"
    },
    "3-06": {
        "building": "North",
        "floor": "3",
        "room_type": "Office",
        "connected_node": "north_3_main_junction"
    },
    "5-06": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_main_junction"
    },
    "1-03": {
        "building": "North",
        "floor": "1",
        "room_type": "Office",
        "connected_node": "north_1_east_junction"
    },
    "2-01s": {
        "building": "South",
        "floor": "2",
        "room_type": "Office",
        "connected_node": "south_2_bridge"
    },
    "4-10": {
        "building": "North",
        "floor": "4",
        "room_type": "Office",
        "connected_node": "north_4_central_junction"
    },
    "4-11": {
        "building": "North",
        "floor": "4",
        "room_type": "Post Graduate Office",
        "connected_node": "north_4_central_junction"
    },
    "G-23": {
        "building": "North",
        "floor": "G",
        "room_type": "Chief Technician's Office",
        "connected_node": "north_g_south_junction"
    },
    "2-04s": {
        "building": "South",
        "floor": "2",
        "room_type": "Office",
        "connected_node": "south_2_bridge"
    },
    "2-05s": {
        "building": "South",
        "floor": "2",
        "room_type": "Office",
        "connected_node": "south_2_bridge"
    },
    "5-02": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_east_junction"
    },
    "5-11": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_main_junction"
    },
    "5-14": {
        "building": "North",
        "floor": "5",
        "room_type": "Computer Machine Room",
        "connected_node": "north_5_west_junction"
    },
    "2-02s": {
        "building": "South",
        "floor": "2",
        "room_type": "Office",
        "connected_node": "south_2_bridge"
    },
    "4-04": {
        "building": "North",
        "floor": "4",
        "room_type": "Office",
        "connected_node": "north_4_east_junction"
    },
    "5-07": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_main_junction"
    },
    "5-08": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_main_junction"
    },
    "1-05": {
        "building": "North",
        "floor": "1",
        "room_type": "Office",
        "connected_node": "north_1_main_junction"
    },
    "1-09": {
        "building": "North",
        "floor": "1",
        "room_type": "Office",
        "connected_node": "north_1_main_junction"
    },
    "3-02": {
        "building": "North",
        "floor": "3",
        "room_type": "Office",
        "connected_node": "north_3_east_junction"
    },
    "3-08": {
        "building": "North",
        "floor": "3",
        "room_type": "Office",
        "connected_node": "north_3_main_junction"
    },
    "3-11": {
        "building": "North",
        "floor": "3",
        "room_type": "Liberary & Student work room",
        "connected_node": "north_3_main_junction"
    },
    "2-04": {
        "building": "North",
        "floor": "2",
        "room_type": "Office",
        "connected_node": "north_2_main_junction"
    },
    "2-05": {
        "building": "North",
        "floor": "2",
        "room_type": "Electronics Workshop",
        "connected_node": "north_2_main_junction"
    },
    "2-06": {
        "building": "North",
        "floor": "2",
        "room_type": "Chief Technician's Office",
        "connected_node": "north_2_main_junction"
    },
    "2-07": {
        "building": "North",
        "floor": "2",
        "room_type": "Store",
        "connected_node": "north_2_main_junction"
    },
    "2-08": {
        "building": "North",
        "floor": "2",
        "room_type": "Store",
        "connected_node": "north_2_main_junction"
    },
    "5-03": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_east_junction"
    },
    "3-07": {
        "building": "North",
        "floor": "3",
        "room_type": "Office",
        "connected_node": "north_3_main_junction"
    },
    "4-07": {
        "building": "North",
        "floor": "4",
        "room_type": "Office",
        "connected_node": "north_4_central_junction"
    },
    "5-12": {
        "building": "North",
        "floor": "5",
        "room_type": "Office",
        "connected_node": "north_5_main_junction"
    }
}

# 2. Graph Nodes and Connections
graph = nx.DiGraph()

# Define nodes (Imported from Navigation.py)
nodes = {
    "north_g_main_junction": {
        "description": "North Ground Floor - Main Hallway Junction",
        "building": "North",
        "floor": "G"
    },
    "north_g_east_junction": {
        "description": "North Ground Floor - East Corridor Junction",
        "building": "North",
        "floor": "G"
    },
    "north_g_west_junction": {
        "description": "North Ground Floor - West Corridor Junction",
        "building": "North",
        "floor": "G"
    },
    "north_g_west_south_junction": {
        "description": "North Ground Floor - West South Corridor Junction",
        "building": "North",
        "floor": "G"
    },
    "north_g_south_junction": {
        "description": "North Ground Floor - South Corridor Junction",
        "building": "North",
        "floor": "G"
    },
    "north_1_main_junction": {
        "description": "North 1st Floor - Main Hallway Junction",
        "building": "North",
        "floor": "1"
    },
    "north_1_west_junction": {
        "description": "North 1st Floor - West Corridor Junction",
        "building": "North",
        "floor": "1"
    },
    "north_1_east_junction": {
        "description": "North 1st Floor - East Corridor Junction",
        "building": "North",
        "floor": "1"
    },
    "north_2_main_junction": {
        "description": "North 2nd Floor - Main Hallway Junction",
        "building": "North",
        "floor": "2"
    },
    "north_2_west_junction": {
        "description": "North 2nd Floor - West Corridor Junction",
        "building": "North",
        "floor": "2"
    },
    "north_2_east_junction": {
        "description": "North 2nd Floor - East Corridor Junction",
        "building": "North",
        "floor": "2"
    },
    "north_3_main_junction": {
        "description": "North 3rd Floor - Main Hallway Junction",
        "building": "North",
        "floor": "3"
    },
    "north_3_east_junction": {
        "description": "North 3rd Floor - East Corridor Junction",
        "building": "North",
        "floor": "3"
    },
    "north_4_central_junction": {
        "description": "North 4th Floor - Central Stairwell Junction",
        "building": "North",
        "floor": "4"
    },
    "north_4_east_junction": {
        "description": "North 4th Floor - East Corridor Junction",
        "building": "North",
        "floor": "4"
    },
    "north_5_main_junction": {
        "description": "North 5th Floor - Main Hallway Junction",
        "building": "North",
        "floor": "5"
    },
    "north_5_west_junction": {
        "description": "North 5th Floor - West Corridor Junction",
        "building": "North",
        "floor": "5"
    },
    "north_5_east_junction": {
        "description": "North 5th Floor - East Corridor Junction",
        "building": "North",
        "floor": "5"
    },
    "south_2_main_junction": {
        "description": "South 2nd - Main Hallway Junction",
        "building": "South",
        "floor": "2"
    },
    "south_2_east_junction": {
        "description": "South 2nd - Main Hallway Junction",
        "building": "South",
        "floor": "2"
    },
    "south_1_west_junction": {
        "description": "South 1st Floor - Lab West Junction",
        "building": "South",
        "floor": "1"
    },
    "south_1_stairwell": {
        "description": "South 1st Floor - Stairwell B",
        "building": "South",
        "floor": "1"
    },
    "south_1_main_junction": {
        "description": "South 1st Floor - Main Hallway",
        "building": "South",
        "floor": "1"
    },
    "south_1_east_junction": {
        "description": "South 1st Floor - East Junction",
        "building": "South",
        "floor": "1"
    },
    "south_1_lab_junction": {
        "description": "South 1st Floor - Lab Junction",
        "building": "South",
        "floor": "1"
    },
    "south_g_main_junction": {
        "description": "South Ground Floor - Main Hallway",
        "building": "South",
        "floor": "G"
    },
    "south_g_west_junction": {
        "description": "South Ground Floor - West Junction",
        "building": "South",
        "floor": "G"
    },
    "south_2_bridge": {
        "description": "South 2nd Floor - Link Bridge Entrance",
        "building": "South",
        "floor": "2"
    },
    "north_2_bridge": {
        "description": "North 2nd Floor - Link Bridge Entrance",
        "building": "North",
        "floor": "2"
    },
    "south_B_main_junction": {
        "description": "South Basement  - Main Hallway",
        "building": "South",
        "floor": "B"
    },
}

# Add nodes to graph
for node_id, attrs in nodes.items():
    graph.add_node(node_id, **attrs)

# Define edges with instructions (Imported from Navigation.py)
# North Ground Floor horizontal
graph.add_edge("north_g_main_junction", "north_g_east_junction", instruction="Walk east down the main corridor past reception.")
graph.add_edge("north_g_east_junction", "north_g_main_junction", instruction="Walk west down the main corridor to the main junction.")

graph.add_edge("north_g_main_junction", "north_g_west_junction", instruction="Walk down the main corridor then take your first left.")
graph.add_edge("north_g_west_junction", "north_g_main_junction", instruction="Walk down the main corridor then take your first right.")

graph.add_edge("north_g_west_junction", "north_g_west_south_junction", instruction="Walk down the west corridor then turn right.")
graph.add_edge("north_g_west_south_junction", "north_g_west_junction", instruction="Walk down the west corridor then turn left.")

graph.add_edge("north_g_main_junction", "north_g_south_junction", instruction="Walk straight down the main corridor the instrument store.")
graph.add_edge("north_g_south_junction", "north_g_main_junction", instruction="Walk straight up the main corridor from the instrument store.")

graph.add_edge("north_g_west_south_junction", "north_g_south_junction", instruction="Walk straight down the west south corridor the Valve lab.")
graph.add_edge("north_g_south_junction", "north_g_west_south_junction", instruction="Walk straight up the west south corridor from the Valve lab.")

# North 1st Floor horizontal
graph.add_edge("north_1_main_junction", "north_1_west_junction", instruction="Walk down the main corridor then take your first right.")
graph.add_edge("north_1_west_junction", "north_1_main_junction", instruction="Walk down the main corridor then take your first left.")

graph.add_edge("north_1_main_junction", "north_1_east_junction", instruction="Walk down the main corridor then take your first left.")
graph.add_edge("north_1_east_junction", "north_1_main_junction", instruction="Walk down the main corridor then take your first right.")

# North 2nd Floor horizontal
graph.add_edge("north_2_main_junction", "north_2_west_junction", instruction="Walk down the main corridor then take your first right.")
graph.add_edge("north_2_west_junction", "north_2_main_junction", instruction="Walk down the main corridor then take your first left.")

graph.add_edge("north_2_main_junction", "north_2_east_junction", instruction="Walk down the main corridor then take your first left.")
graph.add_edge("north_2_east_junction", "north_2_main_junction", instruction="Walk down the main corridor then take your first right.")

graph.add_edge("north_2_east_junction", "north_2_bridge", instruction="Walk down the the corridor to the link bridge entrance.")
graph.add_edge("north_2_bridge", "north_2_east_junction", instruction="Walk back from the link bridge entrance down the corridor.")

# North 3rd Floor horizontal
graph.add_edge("north_3_main_junction", "north_3_east_junction", instruction="Walk down the main corridor then take your first left.")
graph.add_edge("north_3_east_junction", "north_3_main_junction", instruction="Walk down the main corridor then take your first right.")

# North 4th Floor horizontal
graph.add_edge("north_4_central_junction", "north_4_east_junction", instruction="Walk down the main corridor then take your first left.")
graph.add_edge("north_4_east_junction", "north_4_central_junction", instruction="Walk down the main corridor then take your first right.")

# North 5th Floor horizontal
graph.add_edge("north_5_main_junction", "north_5_west_junction", instruction="Walk down the main corridor then take your first right.")
graph.add_edge("north_5_west_junction", "north_5_main_junction", instruction="Walk down the main corridor then take your first left.")

graph.add_edge("north_5_main_junction", "north_5_east_junction", instruction="Walk down the main corridor then take your first left.")
graph.add_edge("north_5_east_junction", "north_5_main_junction", instruction="Walk down the main corridor then take your first right.")

# Bridge
graph.add_edge("north_2_bridge", "south_2_bridge", instruction="Walk down the  link bridge untill to reach the South Building.")
graph.add_edge("south_2_bridge", "north_2_bridge", instruction="Walk down the  link bridge untill to reach the North Building.")

# South 2nd Floor horizontal
graph.add_edge("south_2_bridge", "south_2_main_junction", instruction="Walk down the corridor then turn right.")
graph.add_edge("south_2_main_junction", "south_2_bridge", instruction="Walk down the corridor then turn left.")

graph.add_edge("south_2_main_junction", "south_2_east_junction", instruction="Walk down the corridor then turn right.")
graph.add_edge("south_2_east_junction", "south_2_main_junction", instruction="Walk down the corridor then turn left.")

# South 1st Floor horizontal
graph.add_edge("south_1_main_junction", "south_1_east_junction", instruction="Walk down the corridor then turn right.")
graph.add_edge("south_1_east_junction", "south_1_main_junction", instruction="Walk down the corridor then turn left.")

# South Ground Floor horizontal
graph.add_edge("south_g_main_junction", "south_g_west_junction", instruction="Walk down the corridor then turn left.")
graph.add_edge("south_g_west_junction", "south_g_main_junction", instruction="Walk down the corridor then turn right.")

# Stairs and other vertical
graph.add_edge("north_g_west_junction", "north_1_east_junction", instruction="Take the stairs to the first floor.")
graph.add_edge("north_1_east_junction", "north_g_west_junction", instruction="Take the stairs to the ground floor.")

graph.add_edge("north_g_west_south_junction", "north_1_west_junction", instruction="Take the stairs to the first floor.")
graph.add_edge("north_1_west_junction", "north_g_west_south_junction", instruction="Take the stairs to the ground floor.")

graph.add_edge("north_g_east_junction", "north_2_east_junction", instruction="Take the stairs or elevator to the 2nd floor.")
graph.add_edge("north_2_east_junction", "north_g_east_junction", instruction="Take the stairs or elevator to the ground floor.")

graph.add_edge("north_2_east_junction", "north_4_central_junction", instruction="Take the central staircase up to the 4th floor.")
graph.add_edge("north_4_central_junction", "north_2_east_junction", instruction="Take the central staircase down to the 2nd floor.")

graph.add_edge("north_4_central_junction", "north_5_west_junction", instruction="Take the stairs up to the 5th floor, turn right at the junction.")
graph.add_edge("north_5_west_junction", "north_4_central_junction", instruction="Take the stairs down to the 4th floor, turn left at the junction.")

graph.add_edge("south_1_stairwell", "south_1_lab_junction", instruction="Walk south from the stairwell to the lab corridor.")
graph.add_edge("south_1_lab_junction", "south_1_stairwell", instruction="Walk north from the lab corridor to the stairwell.")

graph.add_edge("south_1_lab_junction", "south_2_bridge", instruction="Take the stairs to the 2nd floor bridge entrance.")
graph.add_edge("south_2_bridge", "south_1_lab_junction", instruction="Take the stairs to the 1st floor lab junction.")

# Vertical for South (fixed instruction)
graph.add_edge("south_1_main_junction", "south_g_main_junction", instruction="Take the lift or stairs to the ground floor.")
graph.add_edge("south_g_main_junction", "south_1_main_junction", instruction="Take the lift or stairs to the 1st floor.")

# Add lift edges for North: connect all pairs (Imported from Navigation.py)
lift_nodes_north = [
    "north_g_west_junction",  # G
    "north_1_main_junction",  # 1
    "north_2_main_junction",  # 2
    "north_3_main_junction",  # 3
    "north_4_central_junction",  # 4
    "north_5_main_junction"   # 5
]
for i in range(len(lift_nodes_north)):
    for j in range(len(lift_nodes_north)):
        if i != j:
            start = lift_nodes_north[i]
            end = lift_nodes_north[j]
            target_floor = nodes[end]['floor']
            graph.add_edge(start, end, instruction=f"Take the lift to floor {target_floor}.")

# Add lift edges for South: connect all pairs (Imported from Navigation.py)
lift_nodes_south = [
    "south_B_main_junction",  # B
    "south_g_main_junction",  # G
    "south_1_main_junction",  # 1
    "south_2_main_junction"   # 2
]
for i in range(len(lift_nodes_south)):
    for j in range(len(lift_nodes_south)):
        if i != j:
            start = lift_nodes_south[i]
            end = lift_nodes_south[j]
            target_floor = nodes[end]['floor']
            graph.add_edge(start, end, instruction=f"Take the lift to floor {target_floor}.")

# --- Navigation Logic Function ---
def calculate_path(start_node, end_node, dest_room):
    """
    Use BFS to find shortest path and generate directions.
    Includes the final instruction using dest_room.
    """
    if not nx.has_path(graph, start_node, end_node):
        return None
    
    path = nx.shortest_path(graph, start_node, end_node)
    directions = []
    
    # 1. Generate junction-to-junction instructions
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i+1]
        instruction = graph.edges[current, next_node].get('instruction', "Move to next location.")
        directions.append(instruction)
        
    # 2. Add the final instruction to the destination room
    directions.append(f"Walk along the corridor until you see the room labeled {dest_room}")
    
    return directions

# --- Flask Setup ---
app = Flask(__name__)

@app.route('/')
def index():
    # Pass room choices to the HTML template for the dropdown menu
    room_choices = sorted(list(rooms.keys()))
    return render_template('index.html', room_choices=room_choices)

@app.route('/navigate', methods=['POST'])
def navigate():
    data = request.get_json()
    current_node = data.get('current_node')
    dest_room = data.get('destination_room')

    if not current_node or not dest_room:
        return jsonify({"status": "error", "message": "Missing current location or destination."}), 400

    if dest_room not in rooms:
        return jsonify({"status": "error", "message": f"Invalid destination room: {dest_room}"}), 400

    dest_node = rooms[dest_room]['connected_node']
    
    if current_node not in nodes:
        return jsonify({"status": "error", "message": f"Invalid node decoded: {current_node}"}), 400

    current_desc = nodes[current_node]['description']
    dest_type = rooms[dest_room]['room_type']
    
    # Check for arrival
    if current_node == dest_node:
        return jsonify({
            "status": "arrived",
            "current_desc": current_desc,
            "dest_room": dest_room,
            "dest_type": dest_type,
            "directions": ["You have arrived!"]
        })

    # Calculate path
    directions = calculate_path(current_node, dest_node, dest_room)

    if directions is None:
        return jsonify({"status": "error", "message": "No path found to the destination."}), 500

    return jsonify({
        "status": "success",
        "current_desc": current_desc,
        "dest_room": dest_room,
        "dest_type": dest_type,
        "directions": directions
    })

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(host='0.0.0.0', port=5000)