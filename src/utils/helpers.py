import os
import streamlit as st
import pandas as pd
from src.generator.question_generator import QuestionGenerator


def rerun(): # it automcatically refresses after some  time
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger',False)

# this manager quiz
class QuizManager:
    def __init__(self):
        self.questions=[]
        self.user_answers=[]
        self.results=[]

    def generate_questions(self, generator:QuestionGenerator , topic:str , question_type:str , difficulty:str , num_questions:int):
        self.questions=[]
        self.user_answers=[]
        self.results=[]
      #how many of question we neeed depending on question type fib or mcq
        try:
            for _ in range(num_questions):
                if question_type == "Multiple Choice":
                    question = generator.generate_mcq(topic,difficulty.lower())

                    self.questions.append({
                        'type' : 'MCQ',
                        'question' : question.question,
                        'options' : question.options,
                        'correct_answer': question.correct_answer
                    })

                else:
                    question = generator.generate_fill_blank(topic,difficulty.lower())

                    self.questions.append({
                        'type' : 'Fill in the blank',
                        'question' : question.question,
                        'correct_answer': question.answer
                    })
        except Exception as e: # eerrror on steamlet page 
            st.error(f"Error generating question {e}")
            return False
        
        return True
    
   # for  recording the answeers  
    def attempt_quiz(self):
      
       for i,q in enumerate(self.questions): 
            #showing  the questions  (because i start from 0 and we adding 1 )
            st.markdown(f"**Question {i+1} : {q['question']}**")

            if q['type']=='MCQ':
                user_answer = st.radio(  #st.radio Function to modify the display of radio options
                    f"Select and answer for Question {i+1}",
                    q['options'],
                    key=f"mcq_{i}"
                )

                self.user_answers.append(user_answer)

            else:
                user_answer=st.text_input(
                    f"Fill in the blank for Question {i+1}",
                    key = f"fill_blank_{i}"
                )

                self.user_answers.append(user_answer)
# empty list using self.results
    def evaluate_quiz(self):

        self.results=[] # are the results  are this self resukts  
         # compare real answers with user given answers  with using result dictornaty
        for i, (q,user_ans) in enumerate(zip(self.questions,self.user_answers)):
            result_dict = {
                #
                'question_number' : i+1,
                'question': q['question'],
                'question_type' :q["type"],
                'user_answer' : user_ans,
                'correct_answer' : q["correct_answer"],
                "is_correct" : False
            }
                # CHECKING THE CORRECTIONS
            if q['type'] == 'MCQ':
                result_dict['options'] = q['options']
                result_dict["is_correct"] = user_ans == q["correct_answer"]

            else:# since we dont have any thing specific same every time we make it empty
                result_dict['options'] = [] # below .strip is to remove extra space before typed #answeer and converting i t    to lower case beofre compararision 
                result_dict["is_correct"] = user_ans.strip().lower() == q['correct_answer'].strip().lower()
            
            self.results.append(result_dict)
            
      # below we  are generating data frame  which contains user reuslts
    def generate_result_dataframe(self):  # if they are no results
        if not self.results:
            return pd.DataFrame()
        
        return pd.DataFrame(self.results) # if they are results 
    
    #  converting data frame to csv 
    def save_to_csv(self, filename_prefix="quiz_results"):    
        if not self.results:# if no result  warningn below 
            st.warning("No results to save !!")
            return None
        #  
        df = self.generate_result_dataframe()

      # we are using data time to save it with time date in which results are saved 
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{filename_prefix}_{timestamp}.csv"

        os.makedirs('results' , exist_ok=True)
        full_path = os.path.join('results' , unique_filename)

        try:
            df.to_csv(full_path,index=False)
            st.success("Results saved sucesfully....")
            return full_path
        
        except Exception as e:
            st.error(f"Failed to save results {e}")
            return None
            