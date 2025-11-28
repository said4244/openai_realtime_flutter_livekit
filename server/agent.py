import logging
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai
from livekit.plugins.openai import realtime
from livekit.plugins.openai.realtime import *
from openai.types.beta.realtime.session import  InputAudioTranscription, TurnDetection

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        logger.info("Initializing Assistant agent")
        super().__init__(instructions="Talk like a normal Arab human, be conversational,  very talkative,  chatty outgoing, be an attention seeker and basically a motor mouth. Use the syrian dialect exclusively. Also drag out and stretch your words like a real syrian especially at the end of word and sentences. PLEASE TALK ONLY IN SYRIAN DIALECT AND ACCENT. only syrian Your name is layla and you are extremely feminine and shy and giggly")
    
    async def on_error(self, error: Exception):
        logger.error(f"Agent error: {str(error)}", exc_info=True)

async def entrypoint(ctx: agents.JobContext):
    logger.info("Starting agent entrypoint")
    try:
        await ctx.connect()
        logger.info("Successfully connected to LiveKit room")
        # Initialize the realtime model with detailed configuration
        llm = openai.realtime.RealtimeModel(
            model="gpt-4o-realtime-preview-2024-12-17",
            voice="alloy",
            api_key="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",
            input_audio_transcription=InputAudioTranscription(
                model="gpt-4o-transcribe",
                language="ar",
                prompt="expect a syrian dialect"
            ),
            temperature=1.0,
            turn_detection=TurnDetection(
                type="semantic_vad",
                eagerness="auto",
                create_response=True,
                interrupt_response=True,
            ),
        )
        
        logger.debug(f"Initialized realtime model with config: {llm}")

        session = AgentSession(llm=llm)
        logger.info("Created agent session")

        try:
            await session.start(
                room=ctx.room,
                agent=Assistant(),
            )
            logger.info("Successfully started agent session")
        except Exception as e:
            logger.error(f"Failed to start session: {str(e)}", exc_info=True)
            raise

    except Exception as e:
        logger.error(f"Critical error in entrypoint: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("Starting agent application")
    try:
        agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}", exc_info=True)
        raise