from dataclasses import dataclass

from app.application.interface.gateway.question import IQuestionGateway
from app.application.interface.transaction import ITransaction
from app.domain.question import Question


@dataclass()
class QuestionList:
    limit: int
    offset: int
    total: int
    questions: list[Question]


class QuestionUseCase:
    def __init__(
            self,
            question_gateway: IQuestionGateway,
            transaction: ITransaction,
    ) -> None:
        self.question_gateway = question_gateway
        self.transaction = transaction

    def add_question(self, question: Question) -> None:
        self.question_gateway.add(question)
        self.transaction.commit()

    def get_questions(self, limit: int, offset: int) -> QuestionList:
        total = self.question_gateway.get_total()
        questions = self.question_gateway.get_all(limit, limit * offset)
        return QuestionList(
            limit=limit,
            offset=offset,
            total=total,
            questions=list(questions),
        )

    def get(self, question_id: int) -> Question:
        question = self.question_gateway.get(question_id)
        return question
