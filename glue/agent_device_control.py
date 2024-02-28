from pydantic import Field
from uagents import Agent, Context, Model, Protocol
from dotenv import load_dotenv
import os

from ai_engine import UAgentResponse, UAgentResponseType
import paho.mqtt.client as mqtt
import time

load_dotenv()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("isPistonOut")
    client.subscribe("doPistonOut")
    client.subscribe("BeltPosition")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("10.52.249.73", 1883, 60)
mqttc.loop_start()


class Message(Model):
    message: str
 
# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "home bcx 2024 second attempt"
 
# Then go to https://agentverse.ai, register your agent in the Mailroom
# and copy the agent's mailbox key
AGENT_MAILBOX_KEY = os.getenv('AGENT_MAILBOX_KEY')

 
# Now your agent is ready to join the agentverse!
agent = Agent(
    name="device_control",
    seed=SEED_PHRASE,
    # port=8000,
    # endpoint="http://localhost:8000/submit",
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

class AgentAction(Model):
    action: str = Field(description="The action. Must be out or in.")
 
device_action_protocol = Protocol("DeviceAction")

@device_action_protocol.on_message(model=AgentAction, replies={UAgentResponse})
async def handle_message(ctx: Context, sender: str, msg: AgentAction):
    if msg.action == "in":
        mqttc.publish("doPistonOut", "false", qos=2)
        message = "Piston retracted!"
    else:
        mqttc.publish("doPistonOut", "true", qos=2)
        message = "Piston extended!"
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
)
    



 
if __name__ == "__main__":
    print("uAgent address: ", agent.address)
    agent.include(device_action_protocol, publish_manifest=True)
    agent.run()

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqttc.loop_stop()