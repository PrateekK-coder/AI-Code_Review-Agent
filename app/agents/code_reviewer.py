from langchain_openai import ChatOpenAI
from app.models.review import CodeReview
from app.models.code import CodeFile
from app.prompts.code_review import code_review_prompt
from dotenv import load_dotenv

load_dotenv()

class CodeReviewer:
    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        self.structured_model = self.model.with_structured_output(
            CodeReview
        )



    def review_semantic(self, query: str, code_file: CodeFile, code: str) -> CodeReview:
            return self.review(
                code_file=code_file,
                code=code,
                review_request=query
            )


    
    def review(self, code_file: CodeFile,code:str,context:str="",review_request: str = "Perform a general code review.") -> CodeReview:
        

        messages = code_review_prompt.invoke({
            "file_name": code_file.file_name,
            "file_path": code_file.file_path,
            "language": code_file.language,
            "context": context,
            "code":code,
            "review_request": review_request
            
    })

        result = self.structured_model.invoke(messages)

        return result