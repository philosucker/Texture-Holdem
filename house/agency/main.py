import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from agency import logger  
from agency.messaging import rabbitmq_consumer, rabbitmq_producer
from agency.services import agency_service
from agency.database import connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db_client = await connection.init_db()
        app.state.db_client = db_client
        logger.info("Agency DB initialized.")
        agent_manager = agency_service.AgentManager()
        message_consumer = rabbitmq_consumer.MessageConsumer(db_client=db_client)
        message_producer = rabbitmq_producer.MessageProducer()
        message_consumer.set_producer(message_producer)
        message_consumer.set_agent_manager(agent_manager)

        agent_manager.set_producer(message_producer)
        agent_manager.set_consumer(message_consumer)

        task1 = asyncio.create_task(message_consumer.start_consuming())
        task2 = asyncio.create_task(message_producer.start_producing())
        logger.info("All Agency tasks started successfully")
        try:
            app.state.agent_manager = agent_manager
            yield
        finally:
            await connection.close_db(db_client)
            logger.info("Agency DB connection closed.")
            task1.cancel()
            task2.cancel()
            tasks : list[asyncio.Task] = [task1, task2]
            for task in tasks:
                try:
                    await task 
                except asyncio.CancelledError:
                    logger.info(f"Floor task {task.get_coro().__name__} cancelled successfully.")
                except Exception as e:
                    logger.error(e, exc_info=True)
                logger.info("All Floor tasks cancelled and resources released")
    except Exception as e:
        logger.error(e, exc_info=True)


app = FastAPI(lifespan=lifespan)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

if __name__ == '__main__':
    try:
        logger.info("Starting Agency FastAPI application...")
        uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)
    except Exception as e:
        logger.error(e, exc_info=True)