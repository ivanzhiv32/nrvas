from app.application.interface.gateway.candidate import ICandidateGateway
from app.application.interface.transaction import ITransaction
from app.domain.candidate import Candidate


class CandidateUseCase:
    def __init__(
            self,
            gateway: ICandidateGateway,
            transaction: ITransaction
    ) -> None:
        self.gateway = gateway
        self.transaction = transaction

    def add_candidate(self, candidate: Candidate) -> None:
        self.gateway.add(candidate)
        self.transaction.commit()
