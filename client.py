"""
File client.py
"""
from xmlrpc.client import ServerProxy
from Validator import validate_person_id, validate_email

# Create server proxy for Server 1
server1 = ServerProxy("http://192.168.1.5:8000")

lyst1 = [ ] # to store unit scores temporarily 
counter = 0 # to track number of units entered
MAX_COUNT = 30 # maximum units count

print('\n-----------------------------------------------------------')
print(' Welcome to Honors Enrolment Pre-assessment System (HEPaS)')
print('     Open University of Science and Technology (OUST)')
print('-----------------------------------------------------------\n')
# confirm user status; OUST student or not
user_status = ''
while user_status not in ('yes', 'no'):
    user_status = input('Are you an OUST student? (enter yes/no): ').lower()

person_id = validate_person_id('Enter your Person ID: ')
evaluation_result = ''
repeat_unit_msg = ''
if user_status == 'no': # for non-OUST students
    # get user input for unit scores
    while counter < MAX_COUNT:
        counter += 1
        v = input('Please enter your mark as a <unit_code, mark> pair (enter -1 to stop): ').upper()
        if not v or v.isspace():
            print('Cannot leave empty!')
            continue
        if v != '-1':
            lyst1.append(v)
        else:
            break
    if counter == 30:
        print('\nCannot enter more than 30 unit scores!\n')
    if lyst1:
        evaluation_result, repeat_unit_msg  = server1.display_evaluation_results(user_status, person_id, lyst1)
    else:
        print('\nNo unit scores found!')
    
elif user_status == 'yes': # for OUST students
    # autheticate user
    email = validate_email('Enter your OUST email address: ')
    evaluation_result, repeat_unit_msg = server1.evaluate_oust_student(user_status, person_id, email)
# display Honor assessment result
if repeat_unit_msg:
    print(repeat_unit_msg)
else:
    print()
if evaluation_result:
    print(evaluation_result)
    print()