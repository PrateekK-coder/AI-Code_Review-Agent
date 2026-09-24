from pydantic import BaseModel




class CodeFile(BaseModel):
    file_name:str
    file_path:str
    language:str
    content:str