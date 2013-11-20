# ----------------------- CASES ----------------------- #
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


# ----------------------- COMMENTS ----------------------- #
class BoxedInteger():
    ''' Helper datatype intended to act liek a reference in C++. Usage: pass
        this around so that its value is maintained. Modify self.value, rather
        than creating new BoxedIntegers. '''

    def __init__(self, start_value):
        self.value = start_value


class CommentEntry():
    ''' A class that contains a comment that has been cleaned for displaying in
        a view.'''

    def __init__(self, comment_reference, index):
        ''' Initializes this CommentEntry. Does not recurse through
            children.'''

        self.comment_reference = comment_reference
        self.cleaned_time = comment_reference.time_posted
        self.children = []

        # Index of this comment in the set of all comments displayed on the
        # page.
        self.index = index


class CommentGroupEntry():
    ''' A class that contains a comment that has been cleaned for displaying in
        a view.'''

    def __init__(self):
        ''' Initializes this CommentGroupEntry. Does not recurse through
            children.'''

        self.contents = []


def create_comment_entries(comments, index=BoxedInteger(0)):
    ''' Creates view-ready comment entries that correspond to the given list
        of comments. This will recurse through children as well. At all levels,
        the comments are sorted by time posted. index is a BoxedInteger for
        tracking the current assigned comment index.
        '''

    sorted_comments = comments.order_by('-time_posted')

    entries = []
    for comment in sorted_comments:
        entry = CommentEntry(comment, index.value)
        index.value += 1

        entry.children = create_comment_entries(comment.children)
        entries.append(entry)

    return entries


def create_comment_group_entries(comment_groups, index=BoxedInteger(0)):
    ''' Creates view-ready comment group entries that correspond to the given
        list of comment groups. This will recurse through the comments and
        their children as well. At all levels, the comments are sorted by time
        posted. The groups are sorted by the latest time posted. index is a
        BoxedInteger for tracking the current assigned comment index.

        comments may be of type django.db.models.manager.Manager or Comment.'''

    entries = []
    for comment_group in comment_groups:
        entry = CommentGroupEntry()
        entry.contents = create_comment_entries(comment_group.comments, index)
        entries.append(entry)

    # The function to use in order to sort groups according to which has last
    # been updated.
    def compare_group(x, y):
        x_older = (x.contents[0].comment_reference.time_posted <
                   y.contents[0].comment_reference.time_posted)

        if x_older:
            return 1
        else:
            return -1

    entries.sort(cmp=compare_group)
    return entries
