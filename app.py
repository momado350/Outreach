from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#outreach_deploy

app = Flask(__name__)

# Configuration
ENV = 'prod'  # Change to 'dev' for development environment
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/lexus2'
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kcpl2021Dataaws@data-analysis-db.c6jqnuecx3su.us-east-2.rds.amazonaws.com:5432/outreach_db_test'#Python2020

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

# Models
class OutreachStat(db.Model):
    __tablename__ = 'outreach_stat'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100))
    program_cat = db.Column(db.String(100))
    activity = db.Column(db.String(100))
    stats = db.Column(db.Integer)
    month_year = db.Column(db.String(100))

    def __init__(self, department, program_cat, activity, stats, month_year):
        self.department = department
        self.program_cat = program_cat
        self.activity = activity
        self.stats = stats
        self.month_year = month_year

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_bulk', methods=['POST'])
def submit_bulk():
    department = request.form.get('department')
    program_cats = request.form.getlist('program_cat[]')
    activities = request.form.getlist('activity[]')
    stats_list = request.form.getlist('stats[]')
    month_year = request.form.get('month_year')

    # Validate required fields
    if not department or not month_year or not program_cats or not activities or not stats_list:
        return "All fields are required!", 400

    # Insert data into the database
    for program_cat, activity, stats in zip(program_cats, activities, stats_list):
        new_stat = OutreachStat(
            department=department,
            program_cat=program_cat,
            activity=activity,
            stats=int(stats),
            month_year=month_year
        )
        db.session.add(new_stat)

    db.session.commit()
    return "Data submitted successfully!"


# Run the app
application = app
if __name__ == '__main__':
    app.run()
