import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import graphviz
import tempfile
from streamlit_lottie import st_lottie
import emoji

load_dotenv()
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_course_structure(field_of_study):
    prompt = f'''You are an expert academic advisor in {field_of_study}. 
    Your task is to create a course roadmap for the students who want to pursue this field. 
    The course roadmap should be represented as a dictionary, where each key is a course title, 
    and each value is a list of courses that are prerequisites for the key course. 
    The course roadmap should cover all the essential topics and skills that are required for {field_of_study}. 
    For instance:
{{
    "Python Basics": [],
    "Intermediate Python": ["Python Basics"],
    "Advanced Python": ["Intermediate Python"],
    "Data Structures": ["Intermediate Python"],
    "Algorithms": ["Data Structures"],
    "Machine Learning": ["Data Structures", "Algorithms"]
}}
Please construct the curriculum dictionary for {field_of_study}:'''
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text.strip("```")


def generate_course_roadmap(course_structure):
    # Create a Digraph object with custom styling
    dot = graphviz.Digraph(format='svg', graph_attr={'bgcolor': 'transparent'}, node_attr={'style': 'filled', 'fillcolor': '#F8F9FA', 'fontname': 'Arial', 'fontsize': '22', 'shape': 'rect', 'gradientangle': '90', 'penwidth': '2', 'margin': '0.25', 'fontcolor': '#000000', 'fixedsize': 'false', 'width': '1.5'}, edge_attr={'color': '#666666', 'arrowhead': 'open', 'penwidth': '2'})

    for course, prerequisites in course_structure.items():

        label = f"{course}\nPrerequisites: {', '.join(prerequisites)}" if prerequisites else course

        dot.node(course, shape='rect', style='filled', fillcolor='#F8F9FA:#CEE3F6', label=label, tooltip=f"Click to learn more about {course}", fontsize='22', width='1')

        for prereq in prerequisites:
            dot.node(prereq, shape='rect', style='filled', fillcolor='#F8F9FA:#F2CB05', label=prereq, tooltip=f"Click to learn more about {prereq}", fontsize='22', width='0.75')
            dot.edge(prereq, course, color='#666666', style='solid')

    svg_content = dot.pipe().decode('utf-8')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as f:
        f.write(svg_content.encode("utf-8"))
        svg_path = f.name

    return svg_path, svg_content

st.set_page_config(page_title="Course Compass", page_icon="🧭", layout="centered", initial_sidebar_state = "auto")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.header(":red[Course] Compass 🧭",divider= 'rainbow')
st.write("Crafting a Personalized Roadmap Tailored to Your Course.")

# field_of_study = st.text_input("Enter Field of Study", "")
field_of_study = st.chat_input("Enter your course name :")

# if st.button("Generate Course Roadmap"):
if field_of_study:
    with st.spinner("Generating Roadmap..."):
        course_structure = generate_course_structure(field_of_study)
        course_structure = eval(course_structure)
        svg_path, svg_content = generate_course_roadmap(course_structure)
        st.subheader("Your Roadmap : ")
        st.image(svg_path, use_column_width=True)
        # Add a download button for the SVG file
        st.download_button(emoji.emojize("Download RoadMap :arrow_down:"), svg_content, file_name=f"{field_of_study}_course_roadmap.svg", mime="image/svg+xml")
else:
    st.error("Please enter a field of study.")
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        st_lottie("https://lottie.host/e1de7a95-db4b-4844-b7af-04ccc2eabb4f/fsFmquVkPw.json", width=250, height=250)
