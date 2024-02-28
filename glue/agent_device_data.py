from pydantic import Field
from uagents import Agent, Context, Model, Protocol
from dotenv import load_dotenv
import os

from ai_engine import UAgentResponse, UAgentResponseType
import paho.mqtt.client as mqtt
import time

load_dotenv()

piston_status = ""
belt_position = ""
pressure = ""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("isPistonOut")
    client.subscribe("doPistonOut")
    client.subscribe("BeltPosition")
    # client.subscribe("BeltPosition")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "isPistonOut":
        piston_status = "extended"
    if msg.topic == "doPistonOut":
        piston_status = "retracted"
    if msg.topic == "BeltPosition":
        belt_position = str(msg.payload)


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("10.52.249.73", 1883, 60)
mqttc.loop_start()


class Message(Model):
    message: str
 
# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "home bcx 2024 agent device info"
 
# Then go to https://agentverse.ai, register your agent in the Mailroom
# and copy the agent's mailbox key
AGENT_MAILBOX_KEY = os.getenv('AGENT_MAILBOX_KEY4')

 
# Now your agent is ready to join the agentverse!
agent = Agent(
    name="device_control",
    seed=SEED_PHRASE,
    # port=8000,
    # endpoint="http://localhost:8000/submit",
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

class AgentAction(Model):
    sensor_type: str = Field(description="The sensor type. Should be either 'piston' or 'belt' or 'pressure'.")
 
device_info_protocol = Protocol("DeviceInfo")

@device_info_protocol.on_message(model=AgentAction, replies={UAgentResponse})
async def handle_message(ctx: Context, sender: str, msg: AgentAction):
    print("Sensor Type: " + msg.sensor_type)
    if msg.sensor_type == "pressure":
        message = "The Pressure of the system currently is 1 Bar!"
    elif msg.sensor_type == "piston":
        message = "The Piston is position is " + piston_status
    elif msg.sensor_type == "belt":
        message = "The Belt is position is " + belt_position
    else:
        message = "I don't know this sensor!"
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
)
    



 
if __name__ == "__main__":
    print("uAgent address: ", agent.address)
    agent.include(device_info_protocol, publish_manifest=True)
    agent.run()

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqttc.loop_stop()