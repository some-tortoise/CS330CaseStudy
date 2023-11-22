edges = []
passengers = []
drivers = []
nodes = []
reversedNodes = {}
avgSpeedList = [0]*48
adjacencyListsWeekdays = [0]*24 
adjacencyListsWeekends = [0]*24 
kdroot = ''

minDistToBecomeNewNode = 0.0

center = (40.7054378, -73.9778828)
clusterRange = 26

clusterPoints = [(40.8003, -73.9693), (40.667, -73.8713), (40.8365, -74.1461), (40.9341, -73.8462), (40.7383, -73.6027)]
clusters = ''

hotspotPoints = [(40.6928, -74.1831), 
                 (40.6452, -73.7844), 
                 (40.7739, -73.8725), 
                 (40.7144, -73.9612), 
                 (40.6843, -73.9776), 
                 (40.7253, -73.994), 
                 (40.7401, -74.0053), 
                 (40.7608, -73.9734), 
                 (40.8224, -73.943), 
                 (40.7059, -74.0098), 
                 (40.7599, -73.9915), 
                 (40.7768, -73.9525), 
                 (40.7878, -73.9759), 
                 (40.8678, -73.9206), 
                 (40.7426, -74.0342), 
                 (40.6277, -74.0258), 
                 (40.7447, -73.9889), 
                 (40.725, -74.0358), 
                 (40.7736, -73.9182), 
                 (40.7024, -73.9886), 
                 (40.6961, -73.8572), 
                 (40.7163, -74.0149), 
                 (40.7488, -73.9922), 
                 (40.7526, -73.9791), 
                 (40.7427, -73.993), 
                 (40.678, -73.998), 
                 (40.6993, -73.9233),
                 (40.7281, -74.002), 
                 (40.7193, -74.0063),
                 (40.7198, -73.9873),
                 (40.7402, -73.9864),
                 (40.7385, -73.9855),
                 (40.7427, -73.9923),
                 (40.7449, -73.9888),
                 (40.7571, -74.0011),
                 (40.7615, -74),
                 (40.7604, -73.9875),
                 (40.7566, -73.9756),
                 (40.7646, -73.9644),
                 (40.7772, -73.9597),
                 (40.7785, -73.9626),
                 (40.774, -73.9485),
                 (40.7736, -73.9816)
                 ]
percentOfIdleDriversThatGoToHotspots = 0.5