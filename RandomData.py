import pandas as pd
import geocoder

df = pd.read_csv('Results.csv')

# lowercase all addresses
df['Address'] = df['Address'].str.lower()

df['FirstDraw'] = df['FirstDraw'].str.replace('<', '')  # remove less than symbol where it shows up
df['FirstDraw'] = df['FirstDraw'].replace(r'[A-Za-z].+', pd.NA, regex = True)  # mark non-numeric entries empty

df = df.dropna(subset = ['FirstDraw']).reset_index(drop = True)  # drop empty entries and reset index

blocks = df['Address'].unique()  # list of unique addresses / list of blocks

# group dataframe by address and randomly sample 1 entry from group
# creates a new DataFrame
random = df.groupby("Address").sample(n = 1, random_state = 9).reset_index(drop = True)
# random.to_csv('ResultsRandom.csv', index = False)

random['FirstDraw'] = pd.to_numeric(random['FirstDraw'])

actionLimitNum = len(random[random['FirstDraw'] >= 15])  # number of households w lead over 15 ppb, EPA limit
fdaLimit = len(random[random['FirstDraw'] >= 5])  # number of households w lead over 5 ppb, FDA limit in bottled water

# STATISTICS
sampleProp = actionLimitNum / len(random)
samplePropFDA = fdaLimit / len(random)
standardError = math.sqrt((sampleProp*(1-sampleProp))/len(random))
standardErrorFDA = math.sqrt((samplePropFDA*(1-sampleProp))/len(random))
#
posInterval = sampleProp + 1.96*standardError
negInterval = sampleProp - 1.96*standardError
#
print("EPA Action limit")
print(sampleProp*100)
print(negInterval*100)
print(posInterval*100)
#
posIntervalFDA = samplePropFDA + 1.96*standardErrorFDA
negIntervalFDA = samplePropFDA - 1.96*standardErrorFDA
#
print("Suggested limit")
print(samplePropFDA*100)
print(negIntervalFDA*100)
print(posIntervalFDA*100)
