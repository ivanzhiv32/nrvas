from abc import abstractmethod
from typing import Protocol

from app.domain.candidate import Candidate


class ICandidateGateway(Protocol):
    @abstractmethod
    def add(self, candidate: Candidate) -> Candidate: ...
