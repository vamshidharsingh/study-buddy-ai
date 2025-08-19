import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator
load_dotenv()


def main():
    st.set_page_config(page_title="GGU Practice Portal" , page_icon="📚🏛️")

    if 'quiz_manager'not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
 # Boolean flag: True if a quiz has been successfully generated, False otherwise.
    if 'quiz_generated'not in st.session_state:
        st.session_state.quiz_generated = False

    if 'quiz_submitted'not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger'not in st.session_state:
        st.session_state.rerun_trigger = False
        

    st.title("Pratice portal for 🏫Golden Gate Uni👨🏻‍🎓 ")

    st.sidebar.header("Quiz Settings")
# Creates a dropdown (select box)s for the user to choose the type of questions.
    question_type = st.sidebar.selectbox(
        "Select Questions Type" ,
        ["Multiple Choice" , "Fill in the Blank"],
        index=0
    )

    topic = st.sidebar.text_input("Enter Topic" , placeholder="Ex:Python,AWS,Finance")

    difficulty = st.sidebar.selectbox(
        "Dificulty Level",
        ["Easy" , "Medium" , "Hard"],
        index=1
    )
  # Createss a numeric inputys field for the user to specify the number of questions.
    num_questions=st.sidebar.number_input(
        "Number of Questions",
        min_value=1,  max_value=10 , value=5
    )

    
# beloww block executes when the "Generate Quiz" button in the sidebar is clicked.
    
    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False

        generator = QuestionGenerator()
        succces = st.session_state.quiz_manager.generate_questions(
            generator,
            topic,question_type,difficulty,num_questions
        )

        st.session_state.quiz_generated= succces
        rerun()

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()          
 # Button to submit the quiz.
        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()
   # This block conditionally displays the quiz results after submission.
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()
 # Checks if the results DataFrame is not empty before proceeding to display.
        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count/total_questions)*100
            st.write(f"Score : {score_percentage}")
                # Iterates through each question's result to show individual feedback.
            for _, result in results_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:   # question number is store in result  n if correct shows a ticks  bfore question 
                    st.success(f"✅ Question {question_num} : {result['question']}")
                else:
                    st.error(f"❌ Question {question_num} : {result['question']}")
                    st.write(f"Your answer : {result['user_answer']}")
                    st.write(f"Correct answer : {result['correct_answer']}")
                
                st.markdown("-------") # the line between 2 questions 

               # Button to save the quiz results to a file.
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv() # using function save to csv in helpers.py
                if saved_file:
                    with open(saved_file,'rb') as f:
                        st.download_button(
                            label="Downlaod Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime='text/csv'
                        )
                else:
                    st.warning("No results avialble")
# Ensures that the main() function runs only when the script is executed directly,
# not when it's imported as a module into another script.
if __name__=="__main__":
    main()

        