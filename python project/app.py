import os
from werkzeug.utils import secure_filename
from flask import Flask,session,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///outpass.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class User(db.Model):
      id = db.Column(db.Integer,primary_key =True)
      enrollment = db.Column(db.Integer,unique = True,nullable= False)
      password = db.Column(db.String(100),nullable = False)
      name = db.Column(db.String(500),nullable=False)
      email = db.Column(db.String(200),unique = True ,nullable = False)
      hostel = db.Column(db.String(50),nullable = False)



      def __init__(self,email,password,name,enrollment,hostel) :
          self.enrollment=enrollment
          self.name = name
          self.email = email
          self.hostel = hostel
          self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())


      def check_password(self,password):
          return bcrypt.checkpw(password.encode('utf-8'),self.password)



class Warden(db.Model):
      id = db.Column(db.Integer,primary_key =True)
      employeenumber = db.Column(db.Integer,unique = True,nullable= False)
      password = db.Column(db.String(100),nullable = False)
      name = db.Column(db.String(500),nullable=False)
      email = db.Column(db.String(200),unique = True ,nullable = False)
      hostel = db.Column(db.String(50),nullable = False)



      def __init__(self,email,password,name,employeenumber,hostel) :
          self.employeenumber=employeenumber
          self.name = name
          self.email = email
          self.hostel = hostel
          self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())


      def check_password(self,password):
          return bcrypt.checkpw(password.encode('utf-8'),self.password)



     
class Outpass(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(400), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.enrollment'), nullable=False) 
    roomno = db.Column(db.Integer, nullable=False)  
    reason = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="Pending")  
    request_date = db.Column(db.DateTime, default=datetime.now)
    approval_date = db.Column(db.DateTime, nullable=True)
    consent_file_path = db.Column(db.String(400), nullable=False)

    student = db.relationship('User', backref='outpasses', lazy=True)

    def __init__(self, name, student_id, roomno, reason, status, request_date, approval_date, consent_file_path):
        self.name = name
        self.student_id = student_id
        self.roomno = roomno
        self.reason = reason
        self.status = status
        self.request_date = request_date
        self.approval_date = approval_date
        self.consent_file_path = consent_file_path


with app.app_context():
    db.create_all()



@app.route('/fill', methods=['GET', 'POST'])
def fill():
    if request.method == 'POST':
        name = request.form.get('name')
        student_id = request.form.get('roll_no')  
        roomno = request.form.get('roomno')
        reason = request.form.get('reason').strip()
        request_date = datetime.now()
        approval_date = None
        consent_file = request.files['consent_file']

        if consent_file:
            consent_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(consent_file.filename))
            consent_file.save(consent_file_path) 

            new_outpass = Outpass(
                name=name,
                student_id=student_id,
                roomno=roomno,
                  status="Pending",  
                request_date=request_date,
                approval_date=approval_date,
                reason=reason,
                consent_file_path=consent_file_path
            )

            db.session.add(new_outpass)
            db.session.commit()
            return redirect('/studenthome')
    return render_template('outpass.html')


''' @app.before_first_request
    def create_tables():
     db.create_all()'''

@app.route('/')
def hello_world():
    return render_template('index.html')
   # return'hello Worlld!'

@app.route('/student')
def student():
    return render_template('index2.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
      enrollment = request.form.get('enrollment')
      password = request.form.get('password')
     
      print(f"Enrollment: {enrollment}, Password: {password}")
      
      
      
     
      user = User.query.filter_by(enrollment=enrollment).first()

      if user and user.check_password(password):
         session['name'] = user.name
         session['enrollment'] = user.enrollment
         return redirect('/studenthome')
      else:
         return render_template('index2.html',error = "Invalid user")
      
    return render_template('index.html')
         

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
 

     name = request.form.get('name').strip()

     enrollment = request.form.get('enrollment')
     email = request.form.get('email')
     password = request.form.get('password')
     hostel = request.form.get('hostel')
    

     print(f"Name: {name}, enrollment: {enrollment}, Email: {email}, Password: {password}")

     new_user = User(name=name,email=email,password=password,enrollment=enrollment,hostel=hostel)
     db.session.add(new_user)
     db.session.commit()
     return redirect('/student')


    return render_template('index2.html')


@app.route('/wardenregister', methods=['GET', 'POST'])
def warden_register():
    if request.method == "POST":
        name = request.form.get('name').strip()
        employeenumber = request.form.get('employeenumber')
        email = request.form.get('email')
        password = request.form.get('password')
        hostel = request.form.get('hostel')

        print(f"Name: {name}, Employee Number: {employeenumber}, Email: {email}, Password: {password}")

        new_warden = Warden(name=name, email=email, password=password, employeenumber=employeenumber, hostel=hostel)
        db.session.add(new_warden)
        db.session.commit()
        return redirect('/wardenlogin')

    return render_template('warden.html')



@app.route('/wardenlogin', methods=['GET', 'POST'])
def warden_login():
    if request.method == "POST":
        employeenumber = request.form.get('employeenumber')
        password = request.form.get('password')
        
        wardens = Warden.query.filter_by(employeenumber=employeenumber).first()

        if wardens and wardens.check_password(password):
            session['warden_name'] = wardens.name
            session['warden_hostel'] = wardens.hostel
            return redirect('/view')
        else:
            return render_template('warden.html', error="Invalid warden credentials")
    return render_template('warden.html')


@app.route('/studenthome')
def home():
    status = 'Pending'
    return render_template('studenthome.html',status=status)


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    return render_template('outpass.html') 


@app.route('/warden')
def warden():
   return render_template('warden.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        enrollment_number = request.form.get('enrollment')
        email = request.form.get('email')
        
        user = User.query.filter_by(enrollment=enrollment_number, email=email).first()
        if user:
            return redirect(url_for('reset_password', enrollment=enrollment_number, email=email))
        else:
            return render_template('forgotpassword.html', error="User not found.")
    
    return render_template('forgotpassword.html')






@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        enrollment_number = request.form.get('enrollment')
        email = request.args.get('email')
        
        if new_password == confirm_password:
            user = User.query.filter_by(enrollment=enrollment_number, email=email).first()
            if user:
                user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                db.session.commit()
                return "Password successfully changed!"
            else:
                return "User not found."
        else:
            return "Passwords do not match. Please try again."

    return render_template('resetpassword.html')




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/home')
def enter():
    return render_template('studenthome.html')

@app.route('/admin')
def admin():
    return render_template('sign.html')


@app.route('/view', methods=['GET'])
def view_pending_outpasses():
    hostel = session.get('warden_hostel') 
    if not hostel:
        return redirect(url_for('warden_login')) 
    
    outpasses = Outpass.query.filter_by(status='Pending').join(User).filter(User.hostel == hostel).all()
     

    return render_template('view_outpasses.html', outpasses=outpasses)



@app.route('/update_outpass/<int:outpass_id>/<string:action>', methods=['POST'])
def update_outpass(outpass_id, action):
    outpass = Outpass.query.get(outpass_id)

    if not outpass:
        return "Outpass request not found", 404

    if outpass.status == 'Pending':
        if action == 'approve':
            outpass.status = 'Approved'
            outpass.approval_date = datetime.now()  
        elif action == 'reject':
            outpass.status = 'Rejected'
        else:
            return "Invalid action", 400
        
        
        db.session.commit()

    return redirect(url_for('view_pending_outpasses'))  


@app.route('/view',methods=['GET','POST'])
def loggin():
    return render_template('view_outpasses.html')

@app.route('/pendingrequest',methods=['GET','POST'])
def pendingrequest():
   enrollment = session.get('enrollment')
   if not enrollment:
       return redirect(url_for('login'))
   
   outpass = Outpass.query.filter_by(student_id=enrollment,status='Pending').all()
   return render_template("pending.html",outpasses=outpass,status='Pending')
    

@app.route('/approvedrequest',methods=['GET','POST'])
def approvedrequest():
    enrollment=session.get('enrollment')
    if not enrollment:
        return render_template(url_for('login'))
    
    outpass=Outpass.query.filter_by(student_id=enrollment,status='Approved').all()
    return render_template('approved.html',outpasses=outpass,status='Approved')
    




if __name__=="__main__":
    app.run(debug=True) 