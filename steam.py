import streamlit as st
from langchain.llms import OpenAI
import pandas as pd



st.title('⚽️ Soccer Genie')

df = pd.read_csv('df.csv')
prompt ='''a dataframe with 20 columns about soccer has an example row  as such 
Rk,Player,Nation,Pos,Squad,Age,Born,MP,Starts,Min,90s,Gls,Ast,G+A,G-PK,PK,PKatt,CrdY,CrdR,xG,npxG,xAG,npxG+xAG,PrgC,PrgP,PrgR,Gls,Ast,G+A,G-PK,G+A-PK,xG,xAG,xG+xAG,npxG,npxG+xAG,Matches,-9999 and more 
1,Brenden Aaronson,us USA,MFFW,Leeds United,22-187,2000,32,28,2296,25.5,1,3,4,1,0,0,2,0,3.7,3.7,4.2,7.9,43,84,147,0.04,0.12,0.16,0.04,0.16,0.14,0.17,0.31,0.14,0.31,Matches,5bc43860
 the rows are explained Rk

 sometimes tottenham is called spurs and Manchester Utd red devils
Nation: Nationality
Pos: Position played
Age: Current age
Born: Year of birth
MP: Matches played
Starts: Games started
Min: Minutes played
90s: Minutes played divided by 90
Gls: Goals scored
Ast: Assists
G+A: Goals + Assists
G-PK: Non-penalty goals
PK: Penalty kicks made
PKatt: Penalty kicks attempted
CrdY: Yellow cards
CrdR: Red cards
xG: Expected goals
npxG: Non-penalty expected goals
xAG: Expected assisted goals
npxG+xAG: Non-penalty expected goals plus assisted goals
PrgC: Progressive carries
PrgP: Progressive passes
PrgR: Progressive passes received
PPA: passes into the penalty area
1/3: passes into the final third
Goals/90: Goals scored per 90 
G+A/90: Goals and assists per 90 minutes
Non-penalty goals/90:
Non-penalty G+A/90: 
xG/90: Expected goals per 90 minutes
xAG/90: Expected assisted goals per 90 minutes
xG+xAG/90: Expected goals plus assisted goals per 90 minutes
npxG/90: Non-penalty expected goals per 90 minutes
npxG+xAG/90: Non-penalty expected goals plus assisted goals per 90 minutes
Tkl: Number of players tackled.
TklW: Tackles won .
Def 3rd: Tackles in defensive 1/3.
Mid 3rd: Tackles in middle 1/3.
Att 3rd: Tackles in attacking 1/3.
Tkl: Dribblers tackled.
Att: Dribbles challenged.
Tkl%: o f dribblers tackled.
Lost: Challenges lost.
Blocks: Total blocks.
Sh: Shots blocked.
Pass: Passes blocked.
Int: Interceptions.
Tkl+Int: Tackles + interceptions.
Clr: Clearances.
Err: Errors leading to opponent's shot.
PrgDist -- Progressive Passing Distance
Att -- Passes Attempted (Short)
KP -- Key Passes
Cmp% -- Pass Completion %
TotDist -- Total Passing Distance
PPA -- Passes into Penalty Area

below are examples of questions, when generting the answer limit the columns to
relatively valuable ones for the relating question.
like number of appearances clubs age and as needed 


Q: Top 5 most goals scored by a defender under 21?\n"
df_defenders_under_21 = df[(df['Pos'].str.contains('DF')) & (df['Age'] < 21)]\n
df_defenders_under_21 = df_defenders_under_21[['Player', 'Squad', 'Pos', 'Age', 'Gls', 'MP']]\n
df_defenders_under_21.sort_values(by='Gls', ascending=False, inplace=True)\n
print(df_defenders_under_21.head(5).T.reset_index().values.T.tolist())

Q: Top 5 most goals scored by an English midfielder under 21 ?\n
df_midfielders_under_21 = df[(df['Pos'].str.contains('MF')) & (df['Age'] < 21) & (df['Nation'] == 'ENG')]\n
df_midfielders_under_21 = df_midfielders_under_21[['Player', 'Squad', 'Pos', 'Age', 'Gls', 'MP']]\n
df_midfielders_under_21.sort_values(by='Gls', ascending=False, inplace=True)\n
print(df_midfielders_under_21.head(5).T.reset_index().values.T.tolist())

Q: Top 5 passes into the final third by a midfielder over 30 ?\n
df_midfielders_over_30 = df[(df['Pos'].str.contains('MF')) & (df['Age'] > 30)]\n
df_midfielders_over_30 = df_midfielders_over_30[['Player', 'Squad', 'Pos', 'Age', '1/3', 'MP']]\n
df_midfielders_over_30.sort_values(by='1/3', ascending=False, inplace=True)\n
print(df_midfielders_over_30.head(5).T.sreset_index().values.T.tolist())

Q: Who is the oldest player with an assist\n
df_assist = df[df['Ast'] > 0]\n
df_assist = df_assist[['Player', 'Squad', 'Pos', 'Age', 'Ast', 'MP']]\n
df_assist.sort_values(by='Age', ascending=False, inplace=True)\n
print(df_assist.head(1).T.reset_index().values.T.tolist())

Q: Who is the top assister amongst these 3 teams, Brighton, Brentford, and Crystal Palace\n
df_teams = df[(df['Squad'] == 'Brighton') | (df['Squad'] == 'Brentford') | (df['Squad'] == 'Crystal Palace')]\n
df_teams = df_teams[['Player', 'Squad', 'Pos', 'Age', 'Ast', 'MP']]\n
df_teams.sort_values(by='Ast', ascending=False, inplace=True)\n
print(df_teams.head(1).T.reset_index().values.T.tolist())

Q: players with most goals from manchester united\n
df_players = df[df['Squad'] == 'Manchester Utd']\n
df_players.sort_values(by='Gls', ascending=False, inplace=True)\n
print(df_players.head(1).T.reset_index().values.T.tolist())

Q: '''
openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
  llm = OpenAI(temperature=0.3, openai_api_key=openai_api_key)
  return (llm(prompt + input_text))
query =''

with st.form('my_form'):
  text = st.text_area('Enter text:', 'Ask about this seasons premier league stats')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
      st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
      query  = generate_response(text.strip()+ '\n')


import io
import sys
old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()

        
try:
    exec(query, globals())
    output = buffer.getvalue()
except Exception as e:
    output = str(e)
finally:
    sys.stdout = old_stdout
import pandas as pd

def string_to_dataframe(data_string):
    # Split the input string into a list of lists
    data_list = eval(data_string)

    # Extract the headers from the first list
    headers = data_list[0]

    # Extract the data from the remaining lists
    data = data_list[1:]

    # Create a Pandas DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df


df = string_to_dataframe(output)


st.write(df)


