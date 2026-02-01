from abc import ABC, abstractmethod
from typing import List
from engine.tokens import Token


class EncryptionRule(ABC):

    @abstractmethod
    def encrypt(self, tokens: List[Token]) -> List[Token]:
        pass

    @abstractmethod
    def decrypt(self, tokens: List[Token]) -> List[Token]:
        pass
