class CaseAttribute():
    ''' A class that contains pre-processed information about a case.
    This is transmitted to the display template. '''

    def __init__(self, case_reference):
        self.case_ref = case_reference
        self.patient_ref = case_reference.patient

        if case_reference.priority == 10:
            self.priority_text = "High"
        elif case_reference.priority == 20:
            self.priority_text = "Medium"
        elif case_reference.priority == 30:
            self.priority_text = "Low"

        # TODO: Make this value correspond to the actual age.
        self.age = 30


def create_case_attributes(cases):
    ''' Creates a list of CaseAttributes that correspond to the given sub-set
        of cases.'''

    attributes = [CaseAttribute(case) for case in cases.all()]
    return attributes
