from fastapi import FastAPI, WebSocket
from prometheus_fastapi_instrumentator import Instrumentator
import json

app = FastAPI()

# Инструментируем приложение
Instrumentator().instrument(app).expose(app)

# Глобальные переменные для хранения статуса
status_data = {
    "coordinates": {"latitude": 0.0, "longitude": 0.0},
    "rsrp": None,
    "mobile_operator": None
}

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/status")
async def get_status():
    """
    Возвращает текущий статус из глобальной переменной.
    """
    return status_data

# WebSocket для приёма JSON данных
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Обрабатывает соединение WebSocket, принимает данные JSON (текст или бинарные) и сохраняет их.
    """
    print("Attempting to accept WebSocket connection...")
    await websocket.accept()
    print("WebSocket connection established")
    
    try:
        while True:
            message = await websocket.receive()
            
            if "text" in message:
                # Обработка текстового сообщения
                data = message["text"]
                print(f"Received text data: {data}")
                
                # Парсим данные JSON
                try:
                    parsed_data = json.loads(data)
                    print(f"Parsed JSON: {parsed_data}")
                    
                    # Сохраняем в файл
                    with open("received_file.json", "w") as file:
                        json.dump(parsed_data, file)
                        print(f"Data written to JSON: {parsed_data}")
                    
                    # Обновляем глобальные данные
                    status_data["coordinates"]["latitude"] = parsed_data.get("latitude", 0.0)
                    status_data["coordinates"]["longitude"] = parsed_data.get("longitude", 0.0)
                    status_data["mobile_operator"] = parsed_data.get("networkOperator", "Unknown")
                    status_data["rsrp"] = parsed_data.get("rsrp", None)
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON received: {e}")
                    await websocket.send_text("Error: Invalid JSON format.")
            elif "bytes" in message:
                # Обработка бинарного сообщения
                data = message["bytes"]
                print(f"Received binary data: {data}")
                
                # Предполагаем, что это JSON-файл
                try:
                    json_data = json.loads(data.decode("utf-8"))
                    print(f"Parsed JSON from binary: {json_data}")
                    
                    # Сохраняем в файл
                    with open("received_file.json", "w") as file:
                        json.dump(json_data, file)
                        print(f"Data written to JSON: {json_data}")
                    
                    # Обновляем глобальные данные
                    status_data["coordinates"]["latitude"] = json_data.get("latitude", 0.0)
                    status_data["coordinates"]["longitude"] = json_data.get("longitude", 0.0)
                    status_data["mobile_operator"] = json_data.get("networkOperator", "Unknown")
                    status_data["rsrp"] = json_data.get("rsrp", None)
                except Exception as e:
                    print(f"Error decoding binary data: {e}")
                    await websocket.send_text("Error: Invalid binary JSON format.")
            else:
                print("Unsupported message type, closing connection.")
                await websocket.close()
                break
    
    except Exception as e:
        print(f"Connection closed with error: {e}")
    finally:
        print("WebSocket connection closed.")
