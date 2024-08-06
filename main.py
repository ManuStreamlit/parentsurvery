import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Parent Attitudes and Perceptions Survey Analysis", page_icon=":bar_chart:", layout="wide")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

@st.cache_data
def load_model(model_name):
    data = pd.read_excel(model_name)
    return data

# Load the data
file_path = 'Parent Attitudes and Perceptions Survey_ Indian School Education  (Responses).xlsx'
data = load_model(file_path)

# Add a new column for school categorization
data['School Category'] = data['Which school does your child (eldest) study at currently?'].apply(lambda x: 'Orchids' if 'orchids' in str(x).lower() else 'Non-Orchids')

# Function to group critical life skills categories
def group_critical_life_skills(value):
    if pd.isna(value):
        return 'Other'
    elif 'communication' in value.lower():
        return 'Communication'
    elif 'problem-solving' in value.lower() or 'cognitive' in value.lower():
        return 'Problem-solving & Cognitive'
    elif 'emotional' in value.lower() or 'empathy' in value.lower():
        return 'Emotional & Empathy'
    elif 'physical' in value.lower() or 'motor' in value.lower():
        return 'Physical & Motor Skills'
    else:
        return 'Other'

# Function to group schools categories
def group_schools(value):
    if pd.isna(value) or not isinstance(value, str):
        return 'Other'
    elif 'orchids' in value.lower():
        return 'Orchids'
    elif 'public' in value.lower():
        return 'Public'
    elif 'private' in value.lower():
        return 'Private'
    elif 'international' in value.lower():
        return 'International'
    else:
        return 'Other'

# Function to group occupations
def group_occupations(value):
    if pd.isna(value):
        return 'Other'
    value = value.lower()
    if 'public' in value:
        return 'Public Sector Employee'
    elif 'private' in value:
        return 'Private Sector Employee'
    elif 'business' in value or 'entrepreneur' in value:
        return 'Businessman'
    elif 'housewife' in value:
        return 'Housewife'
    else:
        return 'Other'

# Function to group ages
def group_ages(age):
    if pd.isna(age):
        return 'Unknown'
    elif age < 30:
        return '<30'
    elif 30 <= age <= 40:
        return '31-40'
    elif 41 <= age <= 50:
        return '41-50'
    else:
        return '>50'

# Apply the grouping functions to the data
data['Grouped Life Skills'] = data['What do you think are the critical life skills which a kid should be trained on?'].apply(group_critical_life_skills)
data['Grouped Schools'] = data['Which school does your child (eldest) study at currently?'].apply(group_schools)
data['Grouped Occupations'] = data['Your Occupation'].apply(group_occupations)
data['Grouped Ages'] = data['Your Age'].apply(group_ages)

# # Set the style for the plots
# sns.set(style="whitegrid")

st.title('Parent Attitudes and Perceptions Survey Analysis')

# Sidebar filters
st.sidebar.header('Filters')
age_filter = st.sidebar.multiselect('Select Age Group', options=data['Grouped Ages'].unique(), default=data['Grouped Ages'].unique())
occupation_filter = st.sidebar.multiselect('Select Occupation Group', options=data['Grouped Occupations'].unique(), default=data['Grouped Occupations'].unique())
education_filter = st.sidebar.multiselect('Select Education Level', options=data['Education'].unique(), default=data['Education'].unique())

# Filter the data based on the selections
filtered_data = data[data['Grouped Ages'].isin(age_filter) & data['Grouped Occupations'].isin(occupation_filter) & data['Education'].isin(education_filter)]



# Data cards for basic stats
st.header('Basic Statistics')
st.write(f'Total Responses: {filtered_data.shape[0]}')
st.write(f'Total Questions: {filtered_data.shape[1]}')

# Helper function to create count plots
def create_count_plot(column_name, title):
    if column_name in filtered_data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        plot = sns.countplot(y=column_name, data=filtered_data, order=filtered_data[column_name].value_counts().index, palette='Set2', ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Count')
        ax.set_ylabel(column_name)
        for p in plot.patches:
            ax.annotate(format(p.get_width(), '.0f'), (p.get_width(), p.get_y() + p.get_height() / 2.), 
                        ha='center', va='center', xytext=(20, 0), textcoords='offset points')
        st.pyplot(fig)
    else:
        st.write(f"Column '{column_name}' not found in the dataset.")

# Helper function to create pie charts
def create_pie_chart(column_name, title):
    if column_name in filtered_data.columns:
        fig = px.pie(filtered_data, names=column_name, title=title)
        st.plotly_chart(fig)
    else:
        st.write(f"Column '{column_name}' not found in the dataset.")

# Helper function to create line charts
def create_line_chart(column_name, title):
    if column_name in filtered_data.columns:
        fig = px.line(filtered_data[column_name].value_counts().sort_index().reset_index(), x='index', y=column_name, title=title)
        st.plotly_chart(fig)
    else:
        st.write(f"Column '{column_name}' not found in the dataset.")

# Helper function to create bar charts
def create_bar_chart(column_name, title):
    if column_name in filtered_data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        counts = filtered_data[column_name].value_counts()
        plot = counts.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title(title)
        ax.set_xlabel(column_name)
        ax.set_ylabel('Count')
        for i in ax.containers:
            ax.bar_label(i, label_type='edge')
        st.pyplot(fig)
    else:
        st.write(f"Column '{column_name}' not found in the dataset.")

# Helper function to create a gauge chart
def create_gauge_chart(column_name, title):
    if column_name in filtered_data.columns:
        yes_count = data[column_name].value_counts().get('Yes', 0)
        total_count = data[column_name].notna().sum()
        yes_percentage = yes_count / total_count * 100
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=yes_percentage,  # Example: use mean value for demonstration
            title={'text': title},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        st.plotly_chart(fig)
    else:
        st.write(f"Column '{column_name}' not found in the dataset.")
        
        
# Helper function to create a treemap chart
def create_treemap(column_name, title):
    if column_name in filtered_data.columns:
        fig = px.treemap(data, path=['Grouped Ages'], values=column_name, title=title)
        st.plotly_chart(fig)
    else:
        st.write(f"Column '{column_name}' not found in the dataset.")

# Layout the plots horizontally using Streamlit's columns
col1, col2 = st.columns(2)

with col1:
    # 1. Age Distribution of Parents
    st.header('Age Distribution of Parents',divider='rainbow')
    create_bar_chart('Grouped Ages', 'Age Distribution of Parents')

with col2:
    # 2. Grouped Occupation of Parents
    st.header('Grouped Occupation of Parents',divider='rainbow')
    create_count_plot('Grouped Occupations', 'Grouped Occupation of Parents')

col3, col4 = st.columns(2)

with col3:
    # 3. Education Level of Parents
    st.header('Education Level of Parents',divider='rainbow')
    create_pie_chart('Education', 'Education Level of Parents')

with col4:
    # 4. Household Income Distribution using Bar Chart
    st.header('Household Income Distribution',divider='rainbow')
    create_bar_chart('Household Income:', 'Household Income Distribution')

col5, col6 = st.columns(2)

with col5:
    # 5. Number of School-Going Kids
    st.header('Number of School-Going Kids',divider='rainbow')
    create_count_plot('How many school going kids do you have? ', 'Number of School-Going Kids')

with col6:
    # 6. Grouped Distribution of Schools Attended by Kids
    st.header('Schools Attended by Kids',divider='rainbow')
    create_count_plot('Grouped Schools', 'Schools Attended by Kids')

col7, col8 = st.columns(2)

with col7:
    # 7. Grouped Critical Life Skills Perceived by Parents
    st.header('Critical Life Skills Perceived by Parents',divider='rainbow')
    create_pie_chart('Grouped Life Skills', 'Critical Life Skills Perceived by Parents')

with col8:
    # 8. Opinion on Early Life Skills Education
    st.header('Opinion on Early Life Skills Education',divider='rainbow')
    create_count_plot('Do you think kids should be taught life skills at an early age itself?', 'Opinion on Early Life Skills Education')

col9, col10 = st.columns(2)

with col9:
    # 9. Separate Coaching for Life Skills
    st.header('Separate Coaching for Life Skills',divider='rainbow')
    create_count_plot('Is your kid taking separate coaching for any of life skills?', 'Separate Coaching for Life Skills')

with col10:
    # 10. Approach to Child Education
    st.header('Approach to Child Education',divider='rainbow')
    grouped_counts = filtered_data.groupby('Which in your opinion best describes your approach? ')['Timestamp'].count().reset_index(name='count')
    st.write(grouped_counts)
 

col11, col12 = st.columns(2)    

with col11:
    # Early Life Skills Education
    st.header('Early Life Skills Education', divider='rainbow')
    create_gauge_chart('Do you think kids should be taught life skills at an early age itself?', 'Yes Percentage for Early Life Skills Education')

with col12:
    # Analysis for School Category
    st.header('School Category',divider='rainbow')
    create_count_plot('School Category', 'Categorization by School (Orchids vs Non-Orchids)')

# Add analysis for all remaining columns based on exact column names
remaining_columns = [
    'What in your opinion is the most important phase of a child’s education for the child’s success?',
    'If you were a parent (or if you are) of a kid in early education phase [pre-school-UKG], which of the following would you prioritize given the school has a safe and hygienic environment?',
    'Have you observed improvements in your child\'s emotional well-being due to interactions with well-trained educators?',
    'Which of the following applies to your child if he knows three or more languages?  ',
    'At what age did they begin learning a third language?  ',
    'Do you agree that learning multiple languages has improved your child’s problem-solving & cognitive skills?'
]

for column in remaining_columns:
    st.header(column,divider='rainbow')
    create_count_plot(column, column)


st.subheader('DATASET', divider='rainbow',)   
with st.expander("VIEW DATASET"):
    showData=st.multiselect('Filter: ',filtered_data.columns, default=filtered_data.columns.tolist())
    st.dataframe(filtered_data[showData],use_container_width=True)