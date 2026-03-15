from netmiko import ConnectHandler


device = {

   "device_type": "cisco_ios" ,
   "host": "192.168.8.10",
   "username": "admin",
   "password": "cisco123",
   "secret": "cisco123",

}


print("Connecting to R1...")
connection = ConnectHandler(**device)
connection.enable()


output = connection.send_command("show ip interface brief")
print(output)


connection.disconnect()
print("Done!")
