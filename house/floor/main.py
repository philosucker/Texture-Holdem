
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import State 

from floor import logger  
from floor.database import connection
from floor.messaging import rabbitmq_consumer, rabbitmq_producer
from floor.routers import lobby_router 
from floor.routers.connector import ConnectManager
from floor.services.big_boss import BigBoss
from floor.services.floor_service import FloorManager
from floor.services.lobby_service import LobbyManager
from floor.services.broadcasting_service import ChatBroadcaster
from floor.services.broadcasting_service import TableBroadcaster
# 페널티 대상

# 벳이 없는 상황에서 폴드 (체크만을 마주하고 있는데 폴드하거나 포스트 플롭에서 가장 먼저 하는 액션이 폴드인 경우)
# 지속적인 게임 지연 행위
# 폭력적인 언행
# 핸드 공개
# 블라인드 회피
# 라운드에서 받은 페널티 수와 모든 플레이어 수를 곱한 만큼의 핸드 수 참여 불가

@asynccontextmanager
async def lifespan(app : FastAPI):
    try:
        db_client = await connection.init_db()
        logger.info("Floor DB initialized.")

        floor_manager = FloorManager()
        lobby_manager = LobbyManager()
        connect_manager = ConnectManager()
        big_boss = BigBoss()

        app.state.lobby_manager = lobby_manager
        app.state.connect_manager = connect_manager
        app.state.big_boss = big_boss

        lobby_manager.set_db = db_client
        lobby_manager.set_connect_manger(connect_manager)
        lobby_manager.set_big_boss(big_boss)
        connect_manager.set_db = db_client

        message_consumer = rabbitmq_consumer.MessageConsumer()
        message_producer = rabbitmq_producer.MessageProducer()
        
        floor_manager.set_connect_manger(connect_manager)
        floor_manager.set_consumer(message_consumer)
        floor_manager.set_producer(message_producer)

        message_consumer.set_db(db_client)
        message_consumer.set_producer(message_producer)
        
        chat_broadcaster = ChatBroadcaster()
        table_broadcaster = TableBroadcaster()

        chat_broadcaster.set_connect_manger(connect_manager)
        table_broadcaster.set_connect_manger(connect_manager)
        
        task1 = asyncio.create_task(message_consumer.start_consuming())
        task2 = asyncio.create_task(message_producer.start_producing())
        task3 = asyncio.create_task(chat_broadcaster.start_broadcasting())
        task4 = asyncio.create_task(table_broadcaster.start_broadcasting())
        task5 = asyncio.create_task(floor_manager.start_managing())
        task6 = asyncio.create_task(big_boss.supervising_floor())
        logger.info("All Floor tasks started successfully.")
        try:
            yield
        finally:
            await connection.close_db(db_client)
            logger.info("Floor DB connection closed.")
            task1.cancel()
            task2.cancel()
            task3.cancel()
            task4.cancel()
            task5.cancel()
            tasks : list[asyncio.Task] = [task1, task2, task3, task4, task5]
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
app.include_router(lobby_router.router)

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
        logger.info("Starting Floor FastAPI application...")
        uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
    except Exception as e:
        logger.error(e, exc_info=True)