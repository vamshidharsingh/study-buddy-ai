#llm text output to convert in to proper structrure output
from langchain.output_parsers import PydanticOutputParser
from src.models.question_schemas import MCQQuestion ,FillBlankQuestion #data models define structure
# will tell llm how to form your answers
from src.prompts.templates import mcq_prompt_template,fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm  # call llm 
from src.config.settings import settings #  to get api key and tempt , max retries
from src.common.logger  import get_logger  
from src.common.custom_exeption import CustomException
from dotenv import load_dotenv
import os

load_dotenv()  


class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)
        
    def _retry_and_parse(self,prompt,parser,topic,difficulty):

        for attempt in range (settings.MAX_RETRIES):
            try:
                self.logger.info(f"generating question for topic {topic}  with difficult {difficulty} ")

                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty ))

                parsed = parser.parse(response.content)

                self.logger.info("successfully parsed the question")

                return parsed

            except Exception as e:
                self.logger.error(f"error coming :{str(e)} ")
                if attempt == settings.MAX_RETRIES-1: # if its ur attempt 2 show below
                    raise CustomException(f"Generation failed after {settings.MAX_RETRIES} attempts ")
                
        # 2 main method are present below
    def generate_mcq(self,topic:str,difficulty:str='medium') -> MCQQuestion:

        try:
            #pydantic takes the unstructured text output from a large language model (LLM) and transforming it into a structured, validated Python object defined by a Pydantic model. post getting it we pass as mcq question
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)

            question = self._retry_and_parse(mcq_prompt_template,parser,topic,difficulty)

            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            
            self.logger.info("Generated a valid MCQ Question")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ : {str(e)}")
            raise CustomException("MCQ generation failed" , e)
        

    def generate_fill_blank(self,topic:str,difficulty:str='medium') -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)

            question = self._retry_and_parse(fill_blank_prompt_template,parser,topic,difficulty)


            if "___" not in question.question:
                raise ValueError("fill in the blanks should contain '___'")
          
            self.logger.info("Generated a valid fib Question")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate fillups : {str(e)}")
            raise CustomException("fill in the blanks generation failed" , e)