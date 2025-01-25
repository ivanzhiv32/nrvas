from dataclasses import dataclass

from app.application.interface.gateway.answer import IAnswerGateway
from app.application.interface.gateway.question import IQuestionGateway
from app.application.interface.transaction import ITransaction
from app.domain.answer import Answer


@dataclass
class QuestionAndAnswer:
    question: str
    answer: str


class AnswerUseCase:
    def __init__(
            self,
            answer_gateway: IAnswerGateway,
            question_gateway: IQuestionGateway,
            transaction: ITransaction,
    ) -> None:
        self.answer_gateway = answer_gateway
        self.question_gateway = question_gateway
        self.transaction = transaction

    def add_answer(self, question_id: int, answer: str) -> None:
        question_model = self.question_gateway.get(question_id)
        self.answer_gateway.add(
            Answer(
                question_id=question_model.id,
                answer=answer
            )
        )
        question_model.is_answer = True
        self.question_gateway.update_is_answer(question_model)
        self.transaction.commit()
