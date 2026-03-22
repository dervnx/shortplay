from typing import Dict, Set
from fastapi import WebSocket


class ConnectionManager:
    """WebSocket connection manager for real-time updates."""

    def __init__(self):
        # project_id -> set of websocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: int):
        """Connect a websocket to a project room."""
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = set()
        self.active_connections[project_id].add(websocket)

    def disconnect(self, websocket: WebSocket, project_id: int):
        """Disconnect a websocket from a project room."""
        if project_id in self.active_connections:
            self.active_connections[project_id].discard(websocket)
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]

    async def send_to_project(self, project_id: int, message: dict):
        """Send message to all connections in a project room."""
        if project_id in self.active_connections:
            for connection in self.active_connections[project_id].copy():
                try:
                    await connection.send_json(message)
                except Exception:
                    self.active_connections[project_id].discard(connection)


# Global connection manager instance
manager = ConnectionManager()
