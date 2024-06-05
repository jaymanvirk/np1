from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

@router.websocket("/upload/images")
async def handle_upload_images(websocket: WebSocket):
    await websocket.accept()
    image_data = b''
    while True:
        try:
            chunk = await websocket.receive_bytes()
            if not chunk:
                break
            image_data += chunk
        except WebSocketDisconnect:
            break

    await websocket.send_text(f"Received {image_data = }")