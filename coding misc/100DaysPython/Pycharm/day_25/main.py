import pandas

data = pandas.read_csv("squirrel_data.csv")
print(data)
gray_squirrels_count = len(data[data["Primary Fur Color"]=='Gray'])
red_squirrels_count = len(data[data["Primary Fur Color"]=='Cinnamon'])
black_squirrels_count = len(data[data["Primary Fur Color"]=='Black'])

data_dict = {
    "Fur Color":['Gray', 'Cinnamon', 'Black'],
    "Count":[gray_squirrels_count, red_squirrels_count, black_squirrels_count]
}

df = pandas.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")