from app.agents.code_reviewer import CodeReviewer
from app.models.code import CodeFile


class FileReviewService:

    def __init__(self):
        self.code_reviewer = CodeReviewer()

    def review_file(self, code_file: CodeFile):

        review = self.code_reviewer.review(
            code_file=code_file,
            code=code_file.content,
            context=""
        )

        return review