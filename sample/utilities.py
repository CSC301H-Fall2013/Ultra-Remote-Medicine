import mimetypes
import re
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson

MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'


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


# ----------------------- UPLOAD ----------------------- #
def response_mimetype(request):
    """response_mimetype -- Return a proper response mimetype, accordingly to
    what the client accepts, as available in the `HTTP_ACCEPT` header.

    request -- a HttpRequest instance.

    """
    can_json = MIMEJSON in request.META['HTTP_ACCEPT']
    can_json |= MIMEANY in request.META['HTTP_ACCEPT']
    return MIMEJSON if can_json else MIMETEXT


class JSONResponse(HttpResponse):
    """JSONResponse -- Extends HTTPResponse to handle JSON format response.

    This response can be used in any view that should return a json stream of
    data.

    Usage:

        def a_iew(request):
            content = {'key': 'value'}
            return JSONResponse(content, mimetype=response_mimetype(request))

    """
    def __init__(self, obj='', json_opts=None, mimetype=MIMEJSON,
                 *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse('upload-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
    }
