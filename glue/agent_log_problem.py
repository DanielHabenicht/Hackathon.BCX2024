from pydantic import Field
from uagents import Agent, Context, Model, Protocol
from dotenv import load_dotenv
import os

from ai_engine import UAgentResponse, UAgentResponseType

load_dotenv()


class Message(Model):
    message: str
 
# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "home bcx 2024 log problem agent"
 
# Then go to https://agentverse.ai, register your agent in the Mailroom
# and copy the agent's mailbox key
AGENT_MAILBOX_KEY = os.getenv('AGENT_MAILBOX_KEY3')

 
# Now your agent is ready to join the agentverse!
agent = Agent(
    name="log_problem",
    seed=SEED_PHRASE,
    # port=8000,
    # endpoint="http://localhost:8000/submit",
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

class AgentAction(Model):
    device_type: str = Field(description="Device Type, Type Number or serial number of the device.")
    problem: str = Field(description="The problem with the device.")
    action_description: str = Field(description="Steps the user has taken.")
 
log_action = Protocol("LogAgentAction")

@log_action.on_message(model=AgentAction, replies={UAgentResponse})
async def handle_message(ctx: Context, sender: str, msg: AgentAction):
    if msg.device_type is not None:
        message = "I logged your problem with the " + msg.device_type + " device. Your last steps were recorded."
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
)

 
if __name__ == "__main__":
    print("uAgent address: ", agent.address)
    agent.include(log_action, publish_manifest=True)
    agent.run()