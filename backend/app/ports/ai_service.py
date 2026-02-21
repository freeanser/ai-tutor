# ports/ai_service.py (抽象接口)

from abc import ABC, abstractmethod

class AIServicePort(ABC):
    @abstractmethod
    def grade_essay(self, content: str) -> dict:
        pass