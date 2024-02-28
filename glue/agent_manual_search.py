from pydantic import Field
from uagents import Agent, Context, Model, Protocol
from dotenv import load_dotenv
import os

from ai_engine import UAgentResponse, UAgentResponseType

load_dotenv()


class Message(Model):
    message: str
 
# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "home bcx 2024 manual agent attempt"
 
# Then go to https://agentverse.ai, register your agent in the Mailroom
# and copy the agent's mailbox key
AGENT_MAILBOX_KEY = os.getenv('AGENT_MAILBOX_KEY2')

 
# Now your agent is ready to join the agentverse!
agent = Agent(
    name="device_control",
    seed=SEED_PHRASE,
    # port=8000,
    # endpoint="http://localhost:8000/submit",
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

class AgentAction(Model):
    question: str = Field(description="The question to ask the agent.")
    device_type: str = Field(description="Device Type, Type Number or serial number of the device.")
 
manual_search_action = Protocol("ManualSearchAction")

@manual_search_action.on_message(model=AgentAction, replies={UAgentResponse})
async def handle_message(ctx: Context, sender: str, msg: AgentAction):
    if msg.question == "in":
        # request....
        message = "Dummy agent worked: " + msg.question
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
)
    



 
if __name__ == "__main__":
    print("uAgent address: ", agent.address)
    agent.include(manual_search_action, publish_manifest=True)
    agent.run()