from reopy import device

IP_ADDRESS = input("Please enter your devices IP address...\n")
USERNAME = input("Please enter the username for your device (default: admin)...\n") or "admin"
PASSWORD = input("Please enter the password for user account '{}'...\n".format(USERNAME))

CAM = device.Device(IP_ADDRESS, PASSWORD, USERNAME)
print(CAM)
print(CAM.get_general_device_info())
print(CAM.get_open_ports_services())
print(CAM.get_available_recordings())

# TODO Implement settings class
# TODO Properly implement device class

# TODO Remove print functions, THIS IS A LIBRARY
# TODO Implement feature to retrieve live video stream
# TODO Initialize git repository (priority: middle)
# TODO Rework Exception system (priority: low)
# TODO URL/IP modularity, see network detection system (priority: low)
