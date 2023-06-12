from flask import Flask, render_template, request
import csv
import pandas as pd
import os as os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('sdkhome.html')

@app.route("/sdkupload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files.get('csvfile')
        if uploaded_file and uploaded_file.filename:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join('static', filename)
            uploaded_file.save(file_path)
            return render_template('sdkupload.html', message="CSV file upload successful.")
    return render_template('sdkupload.html')

@app.route("/sdkdata", methods=['GET', 'POST'])
def sdkdata():
    if request.method == 'POST':
        uploaded_file = request.files.get('csvfile')
        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join('static', filename)
            uploaded_file.save(file_path)
            
            sdkdata = []
            with open(file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    sdkdata.append(row)
            
            return render_template('sdkdata.html', sdkdata=sdkdata)
    return render_template('sdkdata.html')


@app.route("/sdksearchbyname", methods=['GET', 'POST'])
def sdksearchbyname():
    return render_template('sdksearchbyname.html')


@app.route("/sdksearch", methods=['POST'])
def sdksearch():
    name = request.form['name']
    csv_path = 'static/people.csv'
    temp_path = ''

    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if name == row['Name']:
                temp_path = f"../static/{row['Picture']}"
                break

    if temp_path:
        return render_template('sdksearchbyname.html', image_path=temp_path, message="Match found.")
    else:
        return render_template('sdksearchbyname.html', error="No match found.")

@app.route("/sdksal", methods=['GET', 'POST'])
def sdksal():
    csv_reader = csv.DictReader(open('static/people.csv'))
    temp_path = []

    for row in csv_reader:
        salary = row.get('Salary', '')
        if salary == '' or salary == ' ':
            salary = 99000
        if int(float(salary)) < 99000 and row.get('Picture', '') != ' ':
            temp_path.append('static/' + row['Picture'])
            print(temp_path)
            print(int(float(salary)))

    print(len(temp_path))
    if temp_path:
        return render_template('sdksal.html', image_path=temp_path, message="Result found")
    else:
        return render_template('sdksal.html', error="No pictures found")

@app.route("/sdkedit", methods=['GET', 'POST'])
def sdkedit():
    return render_template('sdkedit.html')

@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        found_name = ''
        for row in csv_reader:
            if name == row['Name']:
                found_name = name
                break
        if found_name != '':
            return render_template('sdk_display.html', name=found_name)
        else:
            return render_template('sdk_display.html', error="No matching records found.")

@app.route("/sdk_update", methods=['POST'])
def sdk_update():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        picture = request.files['picture']
        keyword = request.form['keyword']
        count = 0

        new_data = [name, state, salary, grade, room, picture.filename, keyword]
        updated_records = []

        with open('static/people.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if name == row[0]:
                    updated_records.append(new_data)
                else:
                    updated_records.append(row)
                count += 1

        with open('static/people.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(updated_records)

        if count != 0:
            return render_template('sdk_display.html', update="One record updated successfully.")
        else:
            return render_template('sdk_display.html', error="No record found!")

@app.route("/sdkremove", methods=['GET', 'POST'])
def sdkremove():
    return render_template('sdkremove.html')

@app.route("/sdkdelete", methods=['GET', 'POST'])
def sdkdelete():
    if request.method == 'POST':
        name = request.form['name']
        record_found = False
        new_records = []
        with open('static/people.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if name != row[0]:
                    new_records.append(row)
                    return 'Not Found'
                else:
                    record_found = True

        with open('static/people.csv', 'w') as file:
            csv_writer = csv.writer(file)
            for record in new_records:
                csv_writer.writerow(record)

        if record_found:
            return render_template('sdkdelete.html', message="Record successfully removed.")
        else:
            return render_template('sdkdelete.html', error="Record not found.")


@app.route("/sdkupload_pic", methods=['GET', 'POST'])
def pic():
    return render_template('sdkupload_pic.html')

@app.route("/sdk_newpic", methods=['GET', 'POST'])
def sdk_newpic():
    if request.method == 'POST':
        uploaded_image = request.files['img']
        filename = secure_filename(uploaded_image.filename)
        uploaded_image.save(os.path.join('static', filename))
        return render_template('sdk_show.html', msg="Image successfully uploaded.")

if __name__ == "__main__":
    app.run(debug=True,port = 8080)
