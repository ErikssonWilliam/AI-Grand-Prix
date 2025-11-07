#!/usr/bin/env python3
import asyncio
import json
import websockets
import logging
import sys
import struct
from enum import IntEnum
from agent import Agent, GameState

# Initialize agent with training mode enabled
# Set training_mode=False to only do inference (no training)
agent = Agent(training_mode=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ActionCode(IntEnum):
    """Action codes for client-server communication"""
    WELCOME = 0x01
    ECHO = 0x02
    PING = 0x03
    MOVE_UP = 0x04
    MOVE_DOWN = 0x05
    MOVE_LEFT = 0x06
    MOVE_RIGHT = 0x07
    ATTACK = 0x08
    DEFEND = 0x09
    STATUS_UPDATE = 0x0A
    SEND_OBSERVATION = 0x0B
    START_GAME = 0x0C
    ERROR = 0xFF

class MessageHandler:
    """Handles message encoding and decoding"""

    @staticmethod
    def encode_action(action_code: ActionCode) -> bytes:
        # Just one byte
        return struct.pack('!B', action_code)

    @staticmethod
    def decode_action(message: bytes) -> tuple[ActionCode, bytes]:
        # C++ message format: [1 byte action] [2 bytes data_length (big-endian)] [data]
        if len(message) < 3:
            raise ValueError("Message too short to contain header (3 bytes required)")
            
        action_code, data_length = struct.unpack('!BH', message[:3])
        
        # Extract data part (optional)
        data = message[3:3 + data_length]
        
        return ActionCode(action_code), data

async def handle_client(websocket):
    client_address = websocket.remote_address
    logger.info(f"New client connected from {client_address}")

    try:
        # Send welcome message - FIXED: 3 bytes with length=0
        welcome_message = struct.pack('!BH', ActionCode.WELCOME, 0)  # 3 bytes!
        await websocket.send(welcome_message)
        logger.info(f"Sent WELCOME action to {client_address}")
        
        # Send START_GAME - CORRECT (already 3 bytes)
        start_game_message = struct.pack('!BH', ActionCode.START_GAME, 0)
        await websocket.send(start_game_message)
        logger.info(f"Sent START_GAME action to {client_address}")

        # --- 2. RL Loop: Listen for Observations and Send Actions ---
        async for message in websocket:
            # The client is sending the full 3-byte header plus observation data
            if isinstance(message, bytes):
                try:
                    action, data = MessageHandler.decode_action(message)
                    #logger.info(f"Decoded action: {action.name} (Data length: {len(data)})")
                    
                    if action == ActionCode.SEND_OBSERVATION:
                        observation = data.decode('utf-8')
                        #logger.info(f"Observation received: {observation}")
                        
                        # TODO: This is where your RL Agent logic goes!
                        # 1. Process the observation (e.g., parse JSON/string)
                        # 2. Feed it to your RL model to get a new action
                        # 3. Send the agent's chosen action back to the client
                        try:
                            obs_dict = json.loads(observation)  # Try JSON first
                        except json.JSONDecodeError:
                            # Fallback: parse simple "key:value, key:value" format
                            obs_dict = {}
                            for item in observation.split(','):
                                if ':' in item:
                                    key, value = item.split(':', 1)
                                    key = key.strip()
                                    value = value.strip()
                                    # Try to convert to float, then int, otherwise keep as string
                                    try:
                                        float_val = float(value)
                                        # Convert to int if it's a whole number
                                        if float_val.is_integer():
                                            obs_dict[key] = int(float_val)
                                        else:
                                            obs_dict[key] = float_val
                                    except ValueError:
                                        obs_dict[key] = value

                        print(obs_dict)
                        # 2. Ask the agent what to do (collects experience if training)
                        # Detect if episode is done (add this based on your game state if available)
                        done = False  # TODO: Set this based on observation if available
                        chosen_action = agent.collect_step(obs_dict, done=done)  # returns 0-4, collects experience
                        
                        # 3. Map to ActionCode (currently only accelerate / MOVE_UP)
                        if chosen_action == 1:  # accelerate
                            action_code = ActionCode.MOVE_UP
                        elif chosen_action == 2:  # brake
                            action_code = ActionCode.MOVE_DOWN
                        elif chosen_action == 3:  # left
                            action_code = ActionCode.MOVE_LEFT
                        elif chosen_action == 4:  # right
                            action_code = ActionCode.MOVE_RIGHT
                        else:
                            action_code = ActionCode.ECHO  # 0 = do nothing
                        
                        # 4. Send action back to client
                        action_to_send = struct.pack('!BH', action_code, 0)
                        await websocket.send(action_to_send)
                        logger.info(f"Sent {action_code.name} to {client_address}")
                        
                    # Handle other messages (e.g., PING)
                    elif action == ActionCode.PING:
                        logger.info(f"Received PING from client.")

                except ValueError as ve:
                    logger.error(f"Message decode error from {client_address}: {ve}")
                except Exception as e:
                    logger.error(f"Unhandled error in receive loop for {client_address}: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                logger.warning(f"Received unexpected text message from {client_address}: {message}")

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client {client_address} disconnected")
    except Exception as e:
        logger.error(f"Error handling client: {e}")
        import traceback
        traceback.print_exc()

async def main_async():
    #host = "127.0.0.1"
    host = "0.0.0.0"
    port = 8080
    
    logger.info(f"Python version: {sys.version}")
    try:
        logger.info(f"Websockets version: {websockets.__version__}")
    except:
        logger.info("Websockets version: unknown")
    
    logger.info(f"Starting Action-based WebSocket server on {host}:{port}")
    logger.info("Action codes supported:")
    for action in ActionCode:
        logger.info(f"  {action.name}: 0x{action:02X}")
    
    async with websockets.serve(handle_client, host, port):
        logger.info("WebSocket server is running. Press Ctrl+C to stop.")
        await asyncio.Future()
def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Server stopped")

if __name__ == "__main__":
    main()