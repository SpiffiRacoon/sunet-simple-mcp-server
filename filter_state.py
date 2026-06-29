import threading

class RuntimeConfig:
    def __init__(self):
        self._lock = threading.Lock()
        # Default starting configurations
        self.entities = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]
        self.tokens = {
            "PERSON": "[NAMN_REDAKTERAT]",
            "EMAIL_ADDRESS": "[EPOST_REDAKTERAT]",
            "PHONE_NUMBER": "[TELEFON_REDAKTERAT]",
        }

    def update(self, entities: list, tokens: dict):
        with self._lock:
            self.entities = entities
            self.tokens = tokens

    def get_current(self):
        with self._lock:
            return self.entities.copy(), self.tokens.copy()

# Single source of truth instance
runtime_config = RuntimeConfig()