import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from dealer import logger  
from dealer.messaging.rabbitmq_consumer import MessageConsumer
from dealer.messaging.rabbitmq_producer import MessageProducer
from dealer.routers import dealer_router
from dealer.routers.connector import ConnectManager
from dealer.services.dealer_service import DealerManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        dealer_manager = DealerManager()
        connect_manager = ConnectManager()

        app.state.dealer_manager = dealer_manager
        app.state.connect_manager = connect_manager
        
        dealer_manager.set_connect_manger(connect_manager)
        message_consumer = MessageConsumer()
        message_producer = MessageProducer()
        message_consumer.set_connect_manager(connect_manager)
        dealer_manager.set_producer(message_producer)
        dealer_manager.set_consumer(message_consumer)

        task1 = asyncio.create_task(message_consumer.start_consuming())
        task2 = asyncio.create_task(message_producer.start_producing())
        task3 = asyncio.create_task(dealer_manager.start_table())
        task4 = asyncio.create_task(connect_manager.dynamic_expire())
        # 폴링방식
        # task4 = asyncio.create_task(dealer_manager.finish_table())
        logger.info("All Dealer tasks started successfully.")
        try:
            yield
        finally:
            task1.cancel()
            task2.cancel()
            task3.cancel()
            task4.cancel()
            tasks : list[asyncio.Task] = [task1, task2, task3, task4]
            for task in tasks:
                try:
                    await task 
                except asyncio.CancelledError:
                    logger.info(f"Dealer task {task.get_coro().__name__} cancelled successfully.")
                except Exception as e:
                    logger.error(e, exc_info=True)
            logger.info("All Dealer tasks cancelled and resources released")
    except Exception as e:
        logger.error(e, exc_info=True)
app = FastAPI(lifespan=lifespan)
app.include_router(dealer_router.router)

if __name__ == '__main__':
    try:
        logger.info("Starting Dealer FastAPI application...")
        uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
    except Exception as e:
        logger.error(e, exc_info=True)