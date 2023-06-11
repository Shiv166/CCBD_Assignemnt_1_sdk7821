from flask import Flask, render_template, request
import csv
import pandas as pd
import os as os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('sdkhome.html')

@app.route("/sdkupload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['csvfile']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', filename))
            return render_template('sdkupload.html', message="CSV file uploaded successfully.")
    return render_template('sdkupload.html')


@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.files['csvfile']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', filename))
            data = []
            with open(os.path.join('static', filename)) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)
            return render_template('data.html', data=data)
    return render_template('data.html')



@app.route("/searchbyname", methods=['GET', 'POST'])
def searchbyname():
    return render_template('searchbyname.html')


@app.route("/sdksearch", methods=['GET', 'POST'])
def sdksearch():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_path = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_path = '../static/' + r['Picture']
        if temp_path != '':
            return render_template('searchbyname.html', image_path=temp_path, message="found")
        else:
            return render_template('searchbyname.html', error="Not found!")


@app.route("/sdksal", methods=['GET', 'POST'])
def sdksal():
    csv_reader = csv.DictReader(open('static/people.csv'))
    temp_path = []

    for r in csv_reader:
        if r['Salary'] == '' or r['Salary'] == ' ':
            r['Salary'] = 99000;
        if int(float(r['Salary'])) < 99000:
            if r['Picture'] != ' ':
                temp_path.append('static/' + r['Picture'])
                print(temp_path)
                print(int(float(r['Salary'])))

    print(len(temp_path))
    if temp_path != '':
        return render_template('sdksal.html', image_path=temp_path,  message="found")
    else:
        return render_template('sdksal.html', error="Picture did not find!")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')


@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_name = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_name = name
        if temp_name != '':
            return render_template('sdk_display.html', name=temp_name)
        else:
            return render_template('sdk_display.html', error="No Record Found!")


# @app.route("/updatedetails", methods=['GET', 'POST'])
# def updatedetails():
#     if request.method == 'POST':
#         name = request.form['name']
#         state = request.form['state']
#         salary = request.form['salary']
#         grade = request.form['grade']
#         room = request.form['room']
#         picture = request.form['picture']
#         keyword = request.form['keyword']
#         cnt = 0

#         temp = [name, state, salary, grade, room, picture, keyword]
#         line = list()

#         with open('static/people.csv', 'r') as f1:
#             csv_reader = csv.reader(f1)
#             for r in csv_reader:
#                 if name == r[0]:
#                     line.append(temp)
#                 else:
#                     line.append(r)
#                 cnt += 1

#             csv_write = open('static/people.csv', 'w')
#             for i in line:
#                 for j in i:
#                     csv_write.write(j + ',')
#                 csv_write.write('\n')

#             if cnt != 0:
#                 return render_template('display.html', update="One Record Updated Successfully.")
#             else:
#                 return render_template('display.html', error="No Record Found!")

@app.route("/sdk_update", methods=['GET', 'POST'])
def sdk_update():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        picture = request.files['picture']  # Access the file using request.files
        keyword = request.form['keyword']
        cnt = 0

        temp = [name, state, salary, grade, room, picture.filename, keyword]  # Use picture.filename to get the filename
        line = []

        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if name == r[0]:
                    line.append(temp)
                else:
                    line.append(r)
                cnt += 1

        with open('static/people.csv', 'w') as csv_write:  # Use with open() to write to the file
            csv_writer = csv.writer(csv_write)
            csv_writer.writerows(line)

        if cnt != 0:
            return render_template('sdk_display.html', update="One Record Updated Successfully.")
        else:
            return render_template('sdk_display.html', error="No Record Found!")



@app.route("/sdkremove", methods=['GET', 'POST'])
def sdkremove():
    return render_template('sdkremove.html')

@app.route("/sdkdelete", methods=['GET', 'POST'])
def sdkdelete():
    if request.method == 'POST':
        name = request.form['name']
        cnt = 0
        line = list()
        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                line.append(r)
                if name == r[0]:
                    line.remove(r)
                    cnt+=1


            csv_write = open('static/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

        if cnt != 0:
            return render_template('sdkdelete.html', message="Record Remove Successfully.")
        else:
            return render_template('sdkdelete.html', error="Record Not Found.")

@app.route("/sdkupload_pic", methods=['GET', 'POST'])
def pic():
    return render_template('sdkupload_pic.html')

@app.route("/sdk_newpic", methods=['GET', 'POST'])
def sdk_newpic():
    if request.method == 'POST':
        file = request.files['img']
        file.save('static/'+file.filename)
        return render_template('sdk_show.html', msg="Image Upload Successfully.")


if __name__ == "__main__":
    app.run(debug=True)
