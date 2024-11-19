# importing dependencies
import streamlit as st  # app development framework
import google.generativeai as genai  # LLM provider
import time

# accessing the API key
# API key is confidential, hence stored in a text file in the project folder and not explicitly written
f = open(r"C:\Users\itsja\OneDrive\Desktop\Innomatics\key.txt")
key = f.read()
# configuring the API key
genai.configure(api_key=key)

# instruction to the model
sys_prompt = """You are an expert, helpful and sensible AI Python Code Reviewer. 
User will give you the Python code written by them. 
You should analyze the code and identify all the bugs or errors. 
You will most probably receive any of the following 3 cases of inputs - incorrect code, correct code or irrelevant out of scope request.
In case 1 , that is, if you receive an incorrect code, organize your response into 3 sections; 'Bug Report', 'Corrected code' and 'Suggestions'. 
In the 'Bug Report' section, mention the name of the error, the corresponding erroneous part in the given code and a brief description about the error. 
By the name of error, I mean the standard names like 'key error', 'Name error', 'Type error' etc. 
Errors can be even spelling errors. If you receive just one line or only a few lines of code, you should point out mistakes in it although it may not be complete. 
You can put this in the form of a 3 column table also for better readability. 
The section title 'Bug Report' should be in boldface and in red color.
In the 'Corrected Code' section, provide the corrected code with proper comments within the code.
The section title 'Corrected Code' should be in boldface and in green color.
In the 'Suggestions' section, provide user-friendly feedback that helps them to improve their code, code writing style etc. Keep the 3rd section brief. 
The section title 'Suggestions' should be in boldface and in Blue color. 
The section titles shall have a comparatively higher font size, say 28.
Sometimes, the user might have already defined a variable which may be anything including a dataframe. But user may give you some line in between as the input. Skillfully identify such things and communicate with the user and provide a sensible output. 
In case 2, that is, if there are no mistakes or bugs, just describe the code and mention general suggestions. In this case, no need to organise content into 3 sections as said above.
In case 3, that is, the user provides a code in any other language other than Python or some irrelevant content out of scope, politely decline their request."""

# to do the code reviewing task, we need the help of an LLM
# here, we have chosen gemini-1.5-flash model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", 
                              system_instruction=sys_prompt)

# giving a title to the app's UI
st.markdown(""" <h1 style='color: darkgoldenrod; font-family: "Lucida Handwriting", "Brush Script MT", cursive;'> 👾 AI Code Reviewer</h1> """, unsafe_allow_html=True)
st.sidebar.title("📝 How to Use")
st.sidebar.markdown("""
1. Paste your Python code in the text area below.
2. Click **Submit** to generate a code review.
3. Receive detailed feedback on bugs and suggestions for improvement.
""")
st.sidebar.markdown("---")
st.sidebar.write("### About This App")
st.sidebar.markdown("""
This app uses **Google Generative AI** to review your Python code, identify bugs, and suggest improvements to make your code cleaner and more efficient.
""")

# enabling a menubar like feature in the UI
tab_1, tab_2 = st.tabs([':violet[:memo:__Raw Code__]', ':violet[:page_facing_up:__Code File__]'])

# assigning & wrapping the desired functionalities within UI of each tab
with tab_1:
    # a small instruction
    st.markdown('<p style="font-size: 20px; color: #6c757d;"><b>Enter your Python code below:</b></p>', unsafe_allow_html=True)
    # ask the user to enter their code & collect it in the variable 'user_prompt'
    user_prompt = st.text_area("", placeholder="Type or paste your code here...", height=250)
    # displaying a button to the user to submit the code
    btn_click_1 = st.button("Submit", "tab_1")
    # suppose the user clicks the button, the following need to be done
    if btn_click_1:
        # display a message to the user
        with st.spinner(':green[__Please wait :hourglass_flowing_sand: while I :robot_face: go through :mag: your code ...__]'):
            time.sleep(7)
            # ask the model to generate response from the user_prompt
            response = model.generate_content(user_prompt)
            # display the response
            st.markdown(response.text, unsafe_allow_html=True)

with tab_2:
    # small instruction to the user 
    st.markdown('<p style="font-size: 20px; color: #6c757d;"><b>Choose a .py file</b></p>', unsafe_allow_html=True)
    st.write(":warning:__Only 1 file shall be uploaded__")
    uploaded_file = st.file_uploader("")
    # display the name of the file once the user uploads it
    if uploaded_file:
        st.write("filename:", uploaded_file.name)
    btn_click_2 = st.button("Submit", "tab_2")
    if btn_click_2:
        # display a message to the user
        with st.spinner(':green[__Please wait :hourglass_flowing_sand: while I :robot_face: go through :mag: your code file ...__]'):
            time.sleep(7)
        # extract the text code from the .py file into the variable bytes data
        bytes_data = uploaded_file.getvalue().decode("utf-8")
        response = model.generate_content(bytes_data)
        # display the LLM's response
        st.markdown(response.text, unsafe_allow_html=True)
