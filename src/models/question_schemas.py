#this package is all  how the  questions shld be passed in proper way

# fine and validate the data model in which data is passed and show to user
from pydantic import BaseModel , Field ,validator
from typing import List

class MCQQuestion(BaseModel):
   # what ur name 
    question: str= Field(description="the question text")
    # options using below 
    options: List[str]= Field(description="list of 4 options")
   #chossing the right answer
    correct_answer: str= Field(description="the correct answer from the options")

    #used to clean or fix  the input before assigning it 
    @validator ('question',pre= True)
    def clean_question(cls,v):
        if isinstance(v,dict): # extract question n convert it to string
            return v.get('desciption',  str(v)) 
        return str(v)
    

class FillBlankQuestion(BaseModel):

    question: str= Field(description="the question text with '__' for the blank")

    answer :str = Field(description= "the correct word or phase for the blank")

    @validator ('question',pre= True)
    def clean_question(cls,v):
        if isinstance(v,dict): # extract question n convert it to string
            return v.get('desciption',  str(v)) 
        return str(v)
    