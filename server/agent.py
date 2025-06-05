from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="alloy"  # Changed from coral to alloy (valid OpenAI voice)
        )
    )
    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )
    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))