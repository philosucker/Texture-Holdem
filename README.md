# Text_Holdem

## Description: 
- An on-line Texas Hold'em game application that allows multiplaying using an artificial intelligence agent
  
---
### Project Objectives
1. Develop a Texas Holdem game application that supports multiplayer with online.  
2. Train AI agents capable of playing Texas Holdem and integrate them into the application.
     
### Project Background
1. The project aims to provide more people with an accessible and enjoyable way to experience Texas Holdem.  
   - **Characteristics of Existing Holdem Applications.**
     
          1) High Risk of Gambling Addiction: Often perceived as mere gambling.  
          2) High Entry Barrier: The rules are not easy to learn.  
          3) Lack of Solo Play Options: There are no holdem game applications yet that include plausible AI agents.
         
2. Texas Holdem presents a valuable opportunity for development  
     using Large Language Models (LLM) and Deep Reinforcement Learning (DRL).  
    
   - Texas Holdem is an **imperfect information game** with strategic simulation elements.  
   - Developing AI capable of making optimal decisions and bluffing with limited information requires  
        advanced techniques in multimodal input processing (text, images, video, sound).  
   
          1) Notable "Starcraft"(Real-Time Strategy Game) pro-gamers like Hong Jin-ho and Lim Yo-hwan
               have transitioned to professional Holdem players as of June 2024.
   
          2) Professional "Go"(Turn-Based Strategy Game) player Lee Sedol
               has also become a Holdem player as of June 2024.  
---
### Project Plan (8 months)
1. 2 months **from April until June in 2024:**
   - Leaning Texas Holdem game.  
   - Studying Python programming, FastAPI and Unity.    
   - Designing overall architecture.    

2. 4 months **from June until September in 2024:**    
   - Develop a Texas Holdem Game Application:  
  
     1) Back-end with FastAPI  
     2) Application UI with Unity.  
      
3. 2 months **from October until December in 2024**        
   - Develop an AI Agent for Holdem application:  

     1) Utilize LLM APIs to create an LLM model for playing Holdem.  
     2) Integrate the LLM model into the Holdem application to collect data for reinforcement learning.  
  
### Requirement Skills
1. Domain Knowledge : No Limit Texas Holdem  
2. Programming Language : Python, C#  
3. Backend : FastAPI  
4. Database : MySQL(SQLAlchemy), MongoDB(Beanie)  
5. Application : Unity
7. Network Programming : Nginx, HTTP, Web Socket, Message Broker(RabbitMQ)  
8. Asyncrnous Programming : AsyncIO  
9. Deep Learning : LLM, DRL for AI Holdem Agent  
10. DevOps : Docker, Kubernetes  

### "How to implement Texas Holdem game? It's so complicated;("  
#### I made reference for you:) Please refer to the documents in [docs](https://github.com/philosucker/Text_Holdem/tree/main/docs) directory  
---
## Development Log  
10.17.2024  
- Completed design of Table scene
  
10.16.2024  
- Completed design of Lobby scene  
    
10.08.2024  
- Improvement of server routers for WebGL Builds  
   
10.05.2024  
- Completed implementation of WebSocket Connection script between Unity Client and FastAPI Server(Floor and Dealer) through BestHTTP  
- Completed design of GoLobby scene and connection between Enter scene and GoLobby scene
  
09.27.2024   
- Completed implementation of HTTP connection script between Unity Client and FastAPI Server(Reception)
- Completed design of Enter scene

### 09.23.2024 Started development of Unity application  

    1. Reception-Client : application UI for user services 
    2. Floor-Client : application UI for floor services, lobby services, broadcasting services
    3. Dealer-Client : application UI for dealer services
    4. HTTP, WebSocket connection : using BestHTTP 
    5. UI Rendering : Images and Animations for scenes (Common, Enter, GoLobby, Lobby, GoTable, Table, LeaveTable)
    6. Build and Distribution test
    
[break 09.13 ~ 09.22]  
  
09.12.2024  

- Schematic diagram of class connection structure  
  <img src="https://github.com/user-attachments/assets/89deed65-aeae-4833-9340-23be703ad2a4" height="600" />  
  
|     **Server**    |     **Reception**    |       **Floor**       |      **Dealer**      |     **Agency**    |
|:-----------------:|:--------------------:|:---------------------:|:--------------------:|:-----------------:|
|     **Router**    |   UR : user_router   |   LR : lobby_router   |  DR : dealer_router  |                   |
|                   |                      |  CM : ConnectManager  |  CM : ConnectManager |                   |
|    **Service**    |   UM : UserManager   |  FM : FloorManager    |  DM : DealerManager  | AM : AgentManager |
|                   |   SM : StackManager  |   LM : lobbyManager   |        Dealer        | TM : TrainManager |
|                   |                      | TB : TableBroadcaster |         Base         |                   |
|                   |                      |  CB : ChatBroadcaster |                      |                   |
|                   |                      |      BB : BigBoss     |                      |                   |
|       **DB**      |      DB : MySQL      |      DB : MongoDB     |                      |    DB : MongoDB   |
| **MessageBroker** | MP : MessageProducer |  MP : MessageProducer | MP : MessageProducer |                   |
|                   | MC : MessageConsumer |  MC : MessageConsumer | MC : MessageConsumer |                   |

09.11.2024  
- Test log analysis
- completed implementation of logic for handling users who disconnect during the game  
- completed implementation of logic for handling users who reconnect to the game  
- completed implementation of logic for imposing penalties on users who violate the rules  
- completed implementation of server reconnection client logic  
- completed modification of table continuation logic  
- completed optimization of managing table logic  
- completed optimization of Hold'em game end conditions  

09.04.2024  
- completed test for Dealer server  
- completed test for Communication between servers  
  
08.14.2024
- completed test for Floor server  
  
08.08.2024
- completed test for Reception server  
- completed test for communication between Reception and Floor

### 08.07.2024 Started comprehensive backend testing  
    1. Reception: Test sign-up, sign-in, authentication procedures, and anti-fraud functions
    2. Floor: Test chat service, broadcasting service, and table matching service after connecting the client and websocket
    3. Dealer: Test hold'em game progress after connecting the client and websocket
    4. Communication between servers: Test message broker (Reception-Floor-Dealer)
    5. Asynchronous programming test
    6. Server performance test: Resource usage, load test, bottleneck test
    
08.06.2024  
- completed implementation of reception, floor, dealer server algorithms  
- completed implementation of floor server and dealer server connection with message broker  
  
08.03.2024  
- completed implementation of reception server and floor server connection with message broker  

07.31.2024  
- Completed implementation of floor server and client connection via websocket

07.30.2024    
- Concurrency test for CPU bound / disk I/O bound / CPU + diskI/O bound  
- Planned to additional test for network I/O bound test after back-end development.

07.29.2024  
- Completed implementation of dealer server and client connection via websocket
  
07.24.2024  
- Completed MicroService Architecture design.   
  <img src="https://github.com/user-attachments/assets/0a69cabd-80b6-4262-92fe-d7f274054019" width="1000" />   

### 07.22.2024 Started development of the backend  
    1. Implementing reception, floor, and dealer server algorithms  
    2. Implementing server-client connections  
    3. Implementing communication between servers  
   
07.19.2024   
- Started learning AsyncIO.   

07.18.2024    
- Started learning message broker.  

07.16.2024   
- Started learning socket programming. (WebSocket)


### 07.12.2024 Completed implementation of "dealer algorithm"
  
07.10.2024    
- Completed implementation of "side pot" creation and management algorithm.    
- Completed implementation of  "pot award" algorithm.

07.05.2024  
- Completed implementation of “end condition” algorithm.  
- Implement test case DB and test functions and start dealer logic testing.

07.02.2024  
- Completed implementation of “Showdown” ranking comparison algorithm.

07.01.2024  
- Review of “showdown” and “pot award” connection logic.
  
06.28.2024  
- Review “end condition” and “showdown” connection logic.

06.27.2024  
- Review “pot creation and management” logic.  
  
06.26.2024  
- Review “end condition” logic.  
  
06.25.2024  
- Completed implementation of “bet”, “raise”, “all-in”, “call”, “check”, and “fold action” algorithms.  
  
### 06.24.2024 Started development of texas holdem dealer algorithm.  
    1. Implementing an algorithm that acts as a dealer in a Texas Hold'em game
    2. Implementing calculations of the types of actions a user can make each turn
    3. Implementing calculations of conditions for ending each street and hand
    4. Implementing calculations of main pot and side pot
    5. Implementing showdown
    6. Implementing pot distribution
    
06.19.2024  
- Completed Monolithic Architecture design.

- Planned to upgrade to MicroService Architecture after development of texas holdem dealer algorithm.  
  <img src="https://github.com/user-attachments/assets/e81c95d4-a30b-4ba6-8b2a-dd71f45561ae" width="600" />  
  
06.10.2024  
- Started learning Unity.  
  
06.08.2024  
- Started Designing the game architecture.   
- Conceptualized the core logic for the Holdem game application.  
    
06.04.2024  
- Fully mastered the rules of Texas Holdem.  
  
05.14.2024   
- Started studying FastAPI for backend development  
  
04.24.2024   
- Started learning the rules of Texas Holdem.  
