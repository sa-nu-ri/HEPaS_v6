"""
File server1.py
"""
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

from Evaluator import Evaluator
from Validator import validate_repeating_unit

# display scores as <unit_code, mark> pairs
def display_scores(unit_scores):
    for score in unit_scores:
        print(score)

# authenticate OUST student and retrieve unit scores
def evaluate_oust_student(user_status, person_id, email):
        # Create server proxy for Server 2
        server2 = ServerProxy("http://localhost:8001")
        results = server2.authenticate_user(person_id, email)
        if not results:
            results = '\nInvalid Person ID or OUST Email!\n'
        else:
            results, repeat_unit_msg = display_evaluation_results(user_status, person_id, results)
        return results, repeat_unit_msg
    
# display evaulation results
def display_evaluation_results(user_status, person_id, unit_scores): 
    scores = []
    evaluation_result = ''
    repeat_unit_msg = ''      
    evaluator = Evaluator(unit_scores)
    try:
        if user_status == 'no': # if user is a non-OUST student
            unit_scores = evaluator.extract_non_oust_scores()
            repeat_unit_msg = validate_repeating_unit(unit_scores)
        # extract scores to a list; OUST or non-OUST
        scores = [unit_score[1] for unit_score in unit_scores]
        print('\n-----------------')
        print('    Unit Scores')
        print('-----------------')
        print('<unit_code, mark>\n')
        if not scores: # if no scores found
            return '\nNo unit scores found!\n', repeat_unit_msg
        else: # if scores found
            display_scores(unit_scores)
            print()      
            evaluation_result = evaluator.check_qualifications(person_id, scores)
            return evaluation_result, repeat_unit_msg
    except:
        return 'Invalid unit scores!', repeat_unit_msg
    # except ValueError:
    #     return 'Invalid unit scores!', repeat_unit_msg

# Create server
server = SimpleXMLRPCServer(("192.168.1.5", 8000))
print("\nServer 1 listening on port 8000...\n")

# Register functions
server.register_function(display_evaluation_results, "display_evaluation_results")
server.register_function(evaluate_oust_student, "evaluate_oust_student")

# Run server
server.serve_forever()    
