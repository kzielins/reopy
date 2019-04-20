### EXAMPLE ###

import reopy

IP_ADDRESS = input("Please enter your devices IP address...\n")
USERNAME = input("Please enter the username for your device (default: admin)...\n") or "admin"
PASSWORD = input(f"Please enter the password for user account '{USERNAME}'...\n")

CAM = reopy.Device(IP_ADDRESS, PASSWORD, USERNAME)

print("Login successful")
print(CAM)
print(CAM.get_connection_info())

# TODO Implement settings class
# TODO Implement connection class
# TODO Properly implement device class

# TODO Rework Exception system (priority: high)
# TODO Implement feature to retrieve live video stream (priority: low)
# TODO URL/IP modularity, see network detection system (priority: low)
