from Connector import *
import time

client = Client()
client.connect("192.168.199.210", 5966)
future = client.put_folder("Image", block=False)