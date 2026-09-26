import pdfplumber
import pandas as pd
import argparse
from datetime import datetime
import random

frenchMonths = {
    "janvier": "January",
    "février": "February",
    "fevrier": "February",
    "mars": "March",
    "avril": "April",
    "mai": "May",
    "juin": "June",
    "juillet": "July",
    "août": "August",
    "aout": "August",
    "septembre": "September",
    "octobre": "October",
    "novembre": "November",
    "décembre": "December",
    "decembre": "December"
}

wordsOfEncouragement = [
    "You’ve got this! All your hard work is about to pay off.",
    "Stay calm and focused. You know more than you think.",
    "Trust yourself. Confidence is your secret weapon.",
    "Every question is an opportunity. Approach it one step at a time.",
    "Mistakes don’t define you. Keep moving forward.",
    "Breathe and believe. You’ve prepared and you’re ready.",
    "Your effort matters more than the score. Give it your best shot.",
    "Focus on progress not perfection. One answer at a time.",
    "Remember your why. Let it guide your focus.",
    "You are capable. You are ready. You can do this!"
]

def convertDate(frDate: str):
    frDate = frDate.replace('er', '')
    parts = frDate.lower().split()
    
    day = parts[0]
    month = frenchMonths[parts[1]]
    year = parts[2]

    englishDate = f"{day} {month} {year}"

    date = datetime.strptime(englishDate, "%d %B %Y")
    return date.strftime("%m/%d/%Y")

def createDf(filePath:str):        
    #construct the dataframe
    table = []
    with pdfplumber.open(filePath) as pdf:
        for page in pdf.pages:
            table.extend(page.extract_table())
    
    df = pd.DataFrame(table[1:], columns=table[0])
    # clean the Remarque column
    remarque = (
        df["Remarque"]
        .str.replace("de: ", "", regex=False)
        .str.replace("à", "", regex=False)
        .str.strip()
        .str.split(n=1))
    df["First Name"] = remarque.str[0]
    df["Second Name"] = remarque.str[1]
    df.drop(columns=['Remarque'], inplace=True)
    
    # since Poly is not using the same terminology... 
    if 'Section' in df.columns:
        pd.DataFrame.rename(df, columns={'Section': 'Groupe'}, inplace=True)
    
    return df

def filterDf(df: pd.DataFrame, course:str, name:str):
    #get all rows that match the sigle
    sigle, group = course.split('-')
    filteredDf = df[(df['Sigle'] == sigle) & (df['Groupe'] == group)]
    
    if filteredDf.shape[0] == 0:
        return None
    if filteredDf.shape[0] != 1:
        # check if a rows contains NaN meaning all student go in the same room
        if filteredDf['Second Name'].isnull().any():
            # there should be only one row with NaN, if not we have a problem :)
            filteredDf = filteredDf[filteredDf['Second Name'].isnull()]
        #find the item where name is included
        else:
            filteredDf = filteredDf[filteredDf['Second Name'] >= name]
    
    return filteredDf

if __name__ == '__main__':
    #parse the input
    parser = argparse.ArgumentParser(description='PolyCsvCalendar')
    parser.add_argument('--name', type=str, required=True, help='Family name')
    parser.add_argument('--classes', nargs='+', required=True,help='sigle-group ex: MTH2304-1')
    parser.add_argument('--midtermsFile', type=str, default=None, help='midterm pdf file path ex: /midterms.pdf')
    parser.add_argument('--finalsFile', type=str, default=None, help='final pdf file path ex: /finals.pdf')

    args = parser.parse_args()
    name = args.name
    courses = args.classes
    midtermsFilePath = args.midtermsFile
    finalsFilePath = args.finalsFile
    
    midtermsDf = None
    finalsDf = None

    if midtermsFilePath is not None:
        midtermsDf = createDf(midtermsFilePath)
    if finalsFilePath is not None:
        finalsDf = createDf(finalsFilePath)
    with open('calendar.csv', 'w', encoding='utf-8') as csv:
        # write the header
        csv.write('Subject, Start Date, Start Time, End Date, End Time, All Day Event, Description, Location\n')
        for course in courses:
            if midtermsDf is not None:
                filteredDf = filterDf(midtermsDf, course, name)
                if filteredDf is not None:
                    csv.write(f'midterm exam for {course[:-2]}, {convertDate(filteredDf.iloc[0,3])}, , {convertDate(filteredDf.iloc[0,3])}, , True, {random.choice(wordsOfEncouragement)}, {filteredDf.iloc[0,5]}\n')
            if finalsDf is not None:
                filteredDf = filterDf(finalsDf, course, name)
                if filteredDf is not None:
                    csv.write(f'Final exam for {course[:-3]}, {convertDate(filteredDf.iloc[0,3])}, , {convertDate(filteredDf.iloc[0,3])}, , True, {random.choice(wordsOfEncouragement)}, {filteredDf.iloc[0,5]}\n')
    
    print('You can find the file in the same repository where the script has been launched!')