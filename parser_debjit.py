# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:20:26 2023

@author: dbho0002
"""

from bs4 import BeautifulSoup
import pandas as pd

## Login to IPL fantasy portal
## Go to Player stats tab
## Right click on any player and select inspect
## Select Elements tab on top left 
## Right click on first line of html code
## Select Copy > Outer HTML
## Open a new notepad file
## Paste content and go to 'Save as'
## Select 'All Files'
## Save as name 'fantasy_points.html'

file_path = "fantasy_points.html"

with open(file_path, 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

divs_name = soup.find_all('div', class_='df-transfer__plyr-name')
divs_pts = soup.find_all('div', class_='df-transfer__plyr-skill')


list_name = []
for div in divs_name:
    # Process the extracted data here
    list_name.append(div.text)
    # print(div.text)
    
list_team = []
list_cat = []
list_total_points = []
for div in divs_pts:
    # Process the extracted data here
    list_team.append(div.text.split(" ")[0])
    list_cat.append(div.text.split(" ")[2])
    list_total_points.append(float(div.text.split("(")[-1].split(" ")[0]))
    
df = pd.DataFrame({
    'Name': list_name,
    'Team': list_team,
    'Category': list_cat,
    'Total points': list_total_points
})

from datetime import date

current_date = date.today()
# print(current_date)

df.to_excel('total_fantasy_points_'+str(current_date)+'.xlsx',index=False)


# divs_match = soup.find_all('div', class_='df-playerStats__box-rgt')
# span_match = soup.find_all('span', class_='df-in')

li_match = soup.find_all('li', class_='df-playerStats-rowHead')
li_match = soup.find_all('li', class_='df-playerStats-rowHead')

list_match = []
for li in li_match:
    span_match = soup.find_all('span', class_='df-in')
    list_match.append(li.text)
list_match = list_match[1:]

# Outer loop to iterate through elements with a specific class
outer_class = 'df-playerStats-rowBody'
outer_elements = soup.find_all('li', class_=outer_class)
list_match_points = []
for outer_element in outer_elements:
    list_match_points.append(outer_element.text)
    
list_match_points = list_match_points[259:]

converted_list = []

for item in list_match_points:
    try:
        converted_list.append(float(item))
    except ValueError:
        converted_list.append(item)

#Match numbers
column_names = list_match

#Number of columns equal to number of matches in the IPL
num_columns = len(column_names)

#Represents number of players
elements_per_column = len(list_name)

data = {}

for i in range(num_columns):
    column_name = f"Column{i+1}"
    start_index = i * elements_per_column
    end_index = start_index + elements_per_column
    column_values = converted_list[start_index:end_index]
    data[column_name] = column_values

df2 = pd.DataFrame(data)
df2.columns = column_names

result = pd.concat([df, df2], axis=1)

result.to_excel('detailed_fantasy_points_'+str(current_date)+'.xlsx',index=False)
