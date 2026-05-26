"""TCP Client for Balboa BW50350 Wi-Fi Module."""
import socket
import time
import threading
import logging
from typing import Optional, Dict, Any

from .const import (
    MIN_REQUEST_INTERVAL,
    CONNECTION_TIMEOUT,
    CMD_GET_STATE,
)

_LOGGER = logging.getLogger(__name__)

class BalboaClient:
    """Client to communicate with Balboa BW50350 Wi-Fi module."""

    def __init__(self, host: str, port: int = 4257) -> None:
        """Initialize the client."""
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.lock = threading.Lock()
        self.last_request_time: float = 0
        self._state: Dict[str, Any] = {}

    def connect(self) -> None:
        """Establish a persistent TCP connection to the Balboa module."""
        if self.socket is None:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(CONNECTION_TIMEOUT)
                self.socket.connect((self.host, self.port))
                _LOGGER.debug(
                    "TCP connection established with %s:%s", self.host, self.port
                )
            except (socket.timeout, ConnectionError) as e:
                _LOGGER.error(
                    "Failed to connect to %s:%s: %s", self.host, self.port, e
                )
                self.socket = None
                raise

    def send_command(self, command: str) -> str:
        """Send a command to the Balboa module and return the response."""
        with self.lock:
            # Respect the minimum interval between requests
            elapsed = time.time() - self.last_request_time
            if elapsed < MIN_REQUEST_INTERVAL:
                time.sleep(MIN_REQUEST_INTERVAL - elapsed)

            # Ensure connection is active
            if self.socket is None:
                self.connect()

            try:
                self.socket.sendall((command + "\r\n").encode())
                response = self.socket.recv(4096).decode().strip()
                self.last_request_time = time.time()

                if response == "NAK":
                    _LOGGER.warning(
                        "Received NAK response for command: %s", command
                    )
                    time.sleep(10)  # Wait before retrying
                    return self.send_command(command)
                return response
            except (socket.timeout, ConnectionError) as e:
                _LOGGER.error(
                    "Error sending command %s: %s", command, e
                )
                if self.socket:
                    self.socket.close()
                self.socket = None
                time.sleep(10)  # Wait before reconnecting
                return self.send_command(command)

    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the spa."""
        response = self.send_command(CMD_GET_STATE)
        return self._parse_state(response)

    def _parse_state(self, response: str) -> Dict[str, Any]:
        """Parse the GET STATE response into a dictionary."""
        state = {}
        if not response:
            return state
        for item in response.split(","):
            if ":" in item:
                key, value = item.split(":", 1)
                state[key.strip()] = value.strip()
        return state

    def close(self) -> None:
        """Close the TCP connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
            _LOGGER.debug("TCP connection closed")
