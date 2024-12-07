from flask import Flask, render_template, request
import csv

app = Flask(__name__)
api_key = 'AIzaSyDzuFaLQm2fRi8KgjdBh72jiEqEgXziHqc'

@app.route('/', methods= ['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods= ['GET','POST'])
def search():
    if request.method=="POST":
        Year = request.form["Year"]
        Material = request.form["Material"]

        fname = "public-art.csv"
        art_data = []
        with open(fname) as csv_file:
            csv_data = csv.reader(csv_file, delimiter=",")
            csv_data = list(csv_data)[:1]

            i = 0
            if Year == "" and Material == "":
                # no search parameters
                for row in csv_data:
                    art_data.append([i, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                    i += 1
            else:
                # one or the other or both of year and material
                for row in csv_data:
                    if (Year != "" and row[5] == Year) or (Material != "" and row[3] == Material.lower()):
                        art_data.append([i, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                    i += 1


        return render_template('search.html', art_data=art_data, Year=Year, Material=Material, searchBtn="yes")

@app.route('/object', methods= ['GET','POST'])
def object():
    if request.method=="GET":
        rowid = request.args.get("id")

        fname = "public-art.csv"
        with open(fname) as csv_file:
            csv_data = csv.reader(csv_file, delimiter=",")
            # get object data at row rowid, remembering that we've taken out the column header row
            obj_data = list(csv_data)[int(rowid)+1]

        return render_template('object.html', obj_data=obj_data, api_key=api_key, searchBtn="yes")

if __name__ == '__main__':
    app.run(debug = True)