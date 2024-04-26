from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
	    while True:
	        data = await websocket.receive_bytes()

	        await websocket.send_text(f"Received {len(data)} bytes")
    except WebSocketDisconnect:

        print("WebSocket connection closed")