"""
File Evaluator.py
"""
from Validator import validate_number, validate_unit_code

class Evaluator:
    def __init__(self, unit_scores):
        self.MIN_COUNT = 16 # minimum units count
        self.unit_scores = unit_scores

    # store marks and unit codes in separate lists
    def extract_non_oust_scores(self):
        # separate marks and unit codes
        split_unit_scores = []
        validated_scores = []
        for unit_score in self.unit_scores[:len(self.unit_scores)]:
            split_unit_score = [item.strip() for item in unit_score.split(',')]
            split_unit_scores.append(split_unit_score)
        error_msg = 'Invalid score!'
        # validate marks and unit codes pairs and append them as tuples
        for score in split_unit_scores:
            unit = validate_unit_code(score[0], error_msg) # store validated unit codes
            mark = validate_number(score[1], error_msg) # store validated marks as real numbers
            validated_scores.append(tuple([unit, mark]))
        return validated_scores

    # calculate average for a list of marks       
    def calculate_average(self, marks):
        #double average: average of all scores
        #Initialization phase
        total = 0 #total - sum of scores 
        grade_counter = 0 #grade_counter: to track the number of scores in the array lyst[])
        #Processing phase
        n = len(marks)
        i = 0
        if n == 0:
            return 0
        while grade_counter < n:
            grade_value = marks[i]
            total = total + grade_value
            grade_counter += 1
            i += 1
        if grade_counter != 0 :
            average = total / grade_counter
            return average
        else:
            return 0

    # evaluate eligibility for Honors study
    def check_qualifications(self, person_id, scores):
        # find the count of failed units
        fails_counter = 0
        for score in scores:
            if score < 50:
                fails_counter += 1
        
        # calculate the course average
        course_average = round(self.calculate_average(scores), 3)
        # order scores in descending order; highest scores to lowest scores
        scores.sort(reverse = True)
        best8_average = round(self.calculate_average(scores[:8]), 3)
        # check evaluation criteria
        if len(self.unit_scores) < self.MIN_COUNT:
            return '<Person ID: '+ str(person_id) +'>, <course average: '+ str(course_average) +'>, completed less than 16 units! DOES NOT QUALIFY FOR HONORS STUDY!' 
        else:
            if fails_counter >= 6:
                return '<Person ID: '+ str(person_id) +'>, <course average: '+ str(course_average) +'>, with 6 or more Fails! DOES NOT QUALIFY FOR HONORS STUDY!'
            else:
                if course_average >= 70:
                    return '<Person ID: '+ str(person_id) +'>, <course average: '+ str(course_average) +'>, QUALIFIES FOR HONOURS STUDY!'
                else:
                    if course_average >= 65:
                        if best8_average >= 80:
                            return '<Person ID: '+ str(person_id) +'>, <course average: '+ str(course_average) +'>, <best 8 average: '+ str(best8_average) +'>, QUALIFIES FOR HONOURS STUDY!'
                        else:
                            return '<Person ID: '+ str(person_id) +'>, <course average: '+ str(course_average) +'>, <best 8 average: '+ str(best8_average) +'>, MAY HAVE GOOD CHANCE! Need further assessment!'
                    else:
                        if course_average >= 60 and best8_average >= 80:
                            return '<Person ID: '+ str(person_id) +'>, <course average: '+ str(course_average) +'>, <best 8 average: '+ str(best8_average) +'>, MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s permission!'
                        else:
                            return '<Person ID: '+ str(person_id) +'>, <course average: '+ str(course_average) +'>, DOES NOT QUALIFY FOR HONORS STUDY!'
