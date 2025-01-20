from dataclasses import dataclass

from app.application.interface.gateway.faq import IFAQGateway
from app.application.interface.transaction import ITransaction
from app.domain.faq import FAQ


@dataclass()
class FAQList:
    limit: int
    offset: int
    total: int
    faq: list[FAQ]


class FAQUseCase:
    def __init__(
            self,
            gateway: IFAQGateway,
            transaction: ITransaction
    ) -> None:
        self.gateway = gateway
        self.transaction = transaction

    def get_faq_list(self, limit: int, offset: int) -> FAQList:
        faq = self.gateway.get_all(limit, limit * offset)
        total = self.gateway.total()
        return FAQList(
            limit=limit,
            offset=offset,
            total=total,
            faq=list(faq)
        )

    def get_faq(self, id: int) -> FAQ:
        faq = self.gateway.get(id)
        return faq
