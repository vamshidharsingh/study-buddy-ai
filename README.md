
### **GGU Practice Portal**

This  application designed to help students practice for tests by generating quizzes. Users can customize the quizzes by selecting a topic, question type (multiple choice or fill-in-the-blank), difficulty level, and the number of questions. The application evaluates the user's answers, provides detailed feedback, and allows them to save their results.

The key technologies used are:
* **Streamlit**: A Python library that allows for the rapid creation of interactive web applications for data science and machine learning.
* **LangChain**: A framework designed for developing applications powered by language models. It helps connect the LLM to other sources of data and tools.
* **Groq**: This is likely the LLM provider being used via `langchain-groq`. Groq's platform is known for fast inference speeds.
* **Pandas**: A data manipulation and analysis library, which is used in the application to create and manage the quiz results in a structured format (a DataFrame) before saving them to a CSV file.
* **Python-dotenv**: A tool for managing environment variables, which is used to securely load API keys or other sensitive information from a `.env` file.

This combination of tools demonstrates an LLMOps approach, where the LLM is integrated into a larger, operational application.

### **Features**

  * **Customizable Quizzes**: Generate quizzes on any topic, such as Python, AWS, or Finance.
  * **Question Types**: Supports both Multiple Choice and Fill-in-the-Blank questions.
  * **Difficulty Levels**: Choose from Easy, Medium, or Hard difficulty.
  * **Number of Questions**: Specify the number of questions from 1 to 10.
  * **Instant Scoring**: Get an immediate score percentage upon submitting the quiz.
  * **Detailed Feedback**: See which questions you got right or wrong, along with the correct answers.
  * **Save Results**: Download quiz results as a CSV file for review.

### **Prerequisites**

  * Python (version 3.x)

### **Installation**

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```
2.  Install the required packages. The `setup.py` file automatically handles this using the dependencies listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    [cite\_start]This command installs `langchain`, `langchain-groq`, `pandas`, `streamlit`, and `python-dotenv`[cite: 1].

### **Usage**

1.  Run the Streamlit application from your terminal:
    ```bash
    streamlit run application.py
    ```
2.  The application will open in your web browser. Use the sidebar to configure your quiz by entering a topic, selecting a question type, choosing a difficulty level, and setting the number of questions.
3.  Click the "Generate Quiz" button to create the quiz.
4.  Answer the questions and click "Submit Quiz" to view your results.
5.  After submission, you can click "Save Results" to download a CSV file containing your score and answers.

### **File Structure**

```
.
├── application.py          # The main Streamlit application script.
├── requirements.txt        # Lists all necessary Python dependencies.
├── setup.py                # Installation script for the package.
├── .env                    # Environment variables (e.g., API keys).
└── src/
    ├── generator/
    │   └── question_generator.py
    └── utils/
        └── helpers.py
```
