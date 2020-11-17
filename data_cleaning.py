import pandas as pd

df = pd.read_csv("glassdoor_job.csv")


# cleaning salary estimate

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
remove_KD = salary.apply(lambda x: x.replace('K','').replace('$',''))
minimum = remove_KD.apply(lambda x: int(x.split('-')[0]))
maximum = remove_KD.apply(lambda x: int(x.split('-')[1]))

df['min_salary'] = minimum
df['max_salary'] = maximum
df['avg_salary'] = (df.min_salary + df.max_salary)/2


# company name text only

df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 
                              else x['Company Name'][:-3], axis = 1)


# separate state and city

df['job_state'] = df['Location'].apply(lambda x: x if ',' not in x else x.split(',')[-1])


# age of company

df['company_age'] = df['Founded'].apply(lambda x: x if x==-1 else 2020 - x)

# parsing of job desc
# Python, Cloud, RStudio, Excel, SQL, PyTorch, TensorFlow 
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['cloud'] = df['Job Description'].apply(lambda x: 1 if 'cloud' in x.lower() 
                                          or 'aws' in x.lower() or
                                          'azure' in x.lower() or 'gcp' in x.lower() else 0)
df['rstudio'] = df['Job Description'].apply(lambda x: 1 if 'rstudio' in x.lower() 
                                            or 'r-studio' in x.lower() 
                                            else 0)
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
df['pytorch'] = df['Job Description'].apply(lambda x: 1 if 'pytorch' in x.lower() else 0)
df['tensorflow'] = df['Job Description'].apply(lambda x: 1 if 'tensorflow' in x.lower() else 0)
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)


# Industry

df = df[df['Industry'] != '-1']

# company size
df = df[df['Size'] != '-1']
df = df[df['Size'] != 'Unknown']


# Job Title
def title_reducer(title):
    if 'scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'machine learning' in title.lower():
        return 'ml engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'

def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower() or 'staff' in title.lower():
        return 'senior'
    elif 'jr' in title.lower() or 'junior' in title.lower() or 'associate' in title.lower():
        return 'junior'
    elif 'intern' in title.lower() or 'co-op' in title.lower():
        return 'intern'
    else:
        return 'na'
    
df['job_simple'] = df['Job Title'].apply(title_reducer)

df['seniority'] = df['Job Title'].apply(seniority)

# Cleaning job state further
def state_cleaner(state):
    if 'united states' in state.lower():
        return 'remote'
    elif 'north carolina' in state.lower():
        return 'NC'
    elif 'colorado' in state.lower():
        return 'CO'
    elif 'new york state' in state.lower():
        return 'NY'
    elif 'virginia'in state.lower():
        return 'VA'
    elif 'california' in state.lower():
        return 'CA'
    elif 'new jersey' in state.lower():
        return 'NJ'
    elif 'north chesterfield' in state.lower():
        return 'VA'
    elif 'arizona' in state.lower():
        return 'AZ'
    elif 'massachusetts' in state.lower():
        return 'MA'
    elif 'new hampshire' in state.lower():
        return 'NH'
    elif 'remote' in state.lower():
        return 'remote'
    else:
        return state.strip()

df['job_state'] = df.job_state.apply(state_cleaner)

df['company_text'] = df.company_text.apply(lambda x: x.replace('\n', ''))

df.to_csv("cleaned_data.csv", index = False)
