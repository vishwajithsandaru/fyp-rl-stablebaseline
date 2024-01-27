import os
import sys
import sumolib
import traci
from string import Template

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("SUMO_HOME not defined.")

net_xml_path = 'grid/demo.net.xml'
net = sumolib.net.readNet(net_xml_path)

def get_lane_detectors(color_lights):

    detectors = {color_light.getID():{'ns':[], 'ew':[], 'sn': [], 'we':[]} for color_light in color_lights}
    
    for color_light in color_lights:
        edges = color_light.getEdges()
        for edge in edges:
            detector_id_template = "detector-$edge_id-$lane"
            template = Template(detector_id_template)

            for i in range(0,3):
                id = template.substitute(edge_id=edge.getID(), lane=str(i))
                if(edge.getID() == '(4_2)'):
                    detectors[color_light.getID()]['ns'].append(id)
                if(edge.getID() == '(1_2)'):
                    detectors[color_light.getID()]['ew'].append(id)
                if(edge.getID() == '(5_2)'):
                    detectors[color_light.getID()]['sn'].append(id)
                if(edge.getID() == '(3_2)'):
                    detectors[color_light.getID()]['we'].append(id)    

    return detectors

# def start():
#     step = 0
#     color_lights = net.getTrafficLights()
#     detectors = get_lane_detectors(color_lights)

#     while(traci.simulation.getMinExpectedNumber() > 0):
#         traci.simulationStep()

#         # Prioritize vehicles comming from North to South if there are more than 5 vehicles in the queue

#         for color_light in color_lights:
#             curr_phase = traci.trafficlight.getPhase(color_light.getID())
#             north_south_detectors = detectors[color_light.getID()]['ns']
#             v_count = 0
#             for detector in north_south_detectors:
#                 v_count += traci.lanearea.getLastStepVehicleNumber(detector)
            
#             if(v_count > 5 and curr_phase == 2):
#                 traci.trafficlight.setPhase(color_light.getID(), 3)

#         step += 1
#     traci.close()
#     sys.stdout.flush()

def start():
    step = 0
    color_lights = net.getTrafficLights()
    detectors = get_lane_detectors(color_lights)

    while(traci.simulation.getMinExpectedNumber() > 0):
        traci.simulationStep()

        # Prioritize vehicles comming from North to South if there are more than 5 vehicles in the queue

    traci.close()
    sys.stdout.flush()

if __name__=="__main__":
    sumoBinary = sumolib.checkBinary('sumo-gui')
    traci.start([sumoBinary, "-c", "grid/demo.sumocfg", "--tripinfo-output", "tripinfo.xml"])
    start()
