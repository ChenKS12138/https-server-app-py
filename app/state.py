from typing import Optional
from infra.https import HttpsServer


class AppState:
    server: HttpsServer = HttpsServer()
    root_directory: Optional[str] = None
