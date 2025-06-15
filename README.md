## Online Outpass Portal
A Flask-based web application for college students to request outpasses, which are then approved in a multi-step flow: **Student → Parent → Warden**
## Features
 Student login and request outpass form from the Student Portal.
 
 Parent approval with screenshot upload via the portal.
 
 Warden dashboard for approving or rejecting outpass requests, with each request routed to the respective warden based on the student's hostel.
 
 SQLite database integration for tracking requests.
 
 Role-based access system(Student, Warden).
## Tech Used
 **Backend:** Python (Flask)
 
 **Frontend:** HTML, CSS, Java Script
 
 **Database:** SQLite
 
 **Hosting:** Render&Local 
## Preview:
![Login Page](https://github.com/user-attachments/assets/436ffd10-6fc3-4fbb-8c7f-d05a2fb895f1)
  ## Student Interface
   ## Login Page
![Student Login Page](https://github.com/user-attachments/assets/51f08939-ec57-4acf-861f-bc760bf8aae4)
   ## New Student Registration
![New Student Register](https://github.com/user-attachments/assets/990e7d97-bcca-49cc-ab1c-a4c2cb964441)
   ## Outpasses 
![Outpass System](https://github.com/user-attachments/assets/84b49d15-3c87-4724-8952-bca0f184eadc)
  ##  Apply for Outpass
![Apply for Outpass](https://github.com/user-attachments/assets/dca7f6ee-4e95-4cb4-b913-1e56ec02b093)
 ## Warden Interface
  ## Warden Login Page
![Warden Login Page](https://github.com/user-attachments/assets/756e3864-69d1-4d60-8ca7-3e29874241c4)
  ## Outpass Request By student
![Outpass Request to respective wardernof all Hostel](https://github.com/user-attachments/assets/e938e11b-4c47-41a4-9515-4de0926929bf)


##  Future Improvements
 # 1. Parent Approval Workflow via Email 
     Implement an email-based approval system where, once a student requests an outpass, an email is sent to their parent.
The email will contain outpass details along with secure approval/rejection links.
Upon parent approval, the request proceeds to the warden for final approval.

# 2. QR Code Based Exit System
  Add a final step where, after approval by warden, the student receives a QR code   or digital pass.
  Security guard can scan or verify the pass before allowing exit.


# Author 
Rujal Gupta




