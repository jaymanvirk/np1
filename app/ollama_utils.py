import asyncio

async def stream_ollama_output(websocket, process):
    """Function to stream output from the Ollama subprocess."""
    try:
        while True:
            output = await asyncio.get_event_loop().run_in_executor(None, process.stdout.readline)
            if output:
                await websocket.send_text(output.strip())
            else:
                break
    except Exception as e:
        print(f"Error while reading output: {e}")

