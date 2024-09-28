from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from reception import logger 
from reception.messaging import rabbitmq_consumer, rabbitmq_producer
from reception.utils import key_generator
from reception.routers import user_router
from reception.database import connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        key_generator.generate_secret_key(algorithm="HS256")
        
        await connection.init_db()  # 데이터베이스 연결 및 테이블 생성
        logger.info("Reception DB initialized.")

        message_consumer = rabbitmq_consumer.MessageConsumer()
        message_producer = rabbitmq_producer.MessageProducer()
        message_consumer.set_producer(message_producer)
        
        task1 = asyncio.create_task(message_consumer.start_consuming())
        task2 = asyncio.create_task(message_producer.start_producing())
        logger.info("All Reception tasks started successfully.")
        try:
            yield
        finally:
            await connection.close_db() 
            logger.info("Reception DB connection closed.")
            task1.cancel()
            task2.cancel()
            tasks = [task1, task2]
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    logger.info(f"Reception task {task.get_coro().__name__} cancelled successfully.")
                except Exception as e:
                    logger.error(e, exc_info=True)
            logger.info("All Reception tasks cancelled and resources released")
    except Exception as e:
        logger.error(e, exc_info=True)
        
app = FastAPI(lifespan=lifespan)
app.include_router(user_router.router, prefix="/reception", tags=["Account Manage"])

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
        logger.info("Starting Reception FastAPI application...")
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    except Exception as e:
        logger.error(e, exc_info=True)
