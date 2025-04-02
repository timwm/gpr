from math import ceil
from datetime import datetime, timedelta
from random import randint, random, sample
from django.utils.lorem_ipsum import paragraphs, sentence, words
from django.utils import timezone
from django.contrib.auth.hashers import make_password

import json, sys, uuid

from core.models import Issue


FACULTY_DATA = {
    "Science": (
        "Physics",
        "Chemistry",
        "Biology",
        "Computer Science",
        "Mathematics",
    ),
    "Engineering": (
        "Mechanical Engineering",
        "Electrical Engineering",
        "Civil Engineering",
        "Computer Engineering",
    ),
    "Arts and Humanities": (
        "History",
        "Philosophy",
        "Literature",
        "Languages",
    ),
    "Bussiness": (
        "Accounting",
        "Finance",
        "Marketing",
        "Management",
    ),
    "Medicine": (
        "Anatomy",
        "Surgery",
        "Pediatrics",
        "Psychiatry",
    ),

}

ROLE_DATA = {
    'REGISTRAR': 'Registrar',
    'LECTURER': 'Lecturer',
    'STUDENT': 'Student',
}

HOST_DATA = [
    # TLDs
    ('ac', 'ac.ug', 'net', 'com', 'dev'),
    # Registered
    ('gmail.com', 'outlook.com', 'yahoomail.com',),
    # Custom authorities
    ('students.uni', 'students.mak', 'example', *(a.lower() for a in words(randint(1, 5), common=False).split())),
]

REGISTRY = {}


def generate_host(staff):
    i = randint(1, len(HOST_DATA)-1)
    if i == 1:
        host = sample_str(HOST_DATA[i], 1)
    else:
        while host := sample_str(HOST_DATA[i], 1):
            if not staff or not host.startswith('student'):
                break
        while tld := sample_str(HOST_DATA[0], 1):
            if not host.startswith('student') or tld.startswith('ac'):
                break
        host += '.' + tld
    return host

def randprob(p, start, stop):
    return randint(start, stop) if random() >= p else 0


def sentences(n):
    return [sentence() for i in range(n)]


def sample_str(it, size, sep=''):
    return sep.join(sample(it, size))


def generate_datetime(created_at=None, delta=None):
    """
    {delta}: A datetime.timedelta specifing the delta between updated_at and created_at
    """
    if created_at is None:
        created_at = timezone.now() + timedelta(days=randint(-100, 0))

    if delta is None:
        kwargs = {
            'days': randint(0, 64),
            'hours': randint(0, 23),
            'minutes': randint(0, 59),
            'seconds': randint(0, 59),
        }
        delta = timedelta(**kwargs)
    elif isinstance(delta, dict):
        delta = timedelta(**delta)

    if created_at + delta > timezone.now():
        updated_at = None
        return created_at.isoformat(), None

    updated_at = created_at + delta
    return created_at.isoformat(), updated_at.isoformat()


def generate_id(size, alphabet=None):
    if alphabet is None:
        alphabet = [chr(c) for c in (*range(48, 57), *range(65, 90), *range(97, 122))]
    return ''.join(sample(alphabet, size))


def truncate(string, max_length, trunc_str=' '):
    """
    {max_length}: maximum number of characters
    {trunc_str}: the string to before which to trucate (starting backwards)
    """
    if not string or len(string) <= max_length:
        return string
    string = string[:max_length]
    if trunc_str:
        index = string.rfind(trunc_str, 0, max_length)
        if index > -1:
            max_length = index
    return string[:max_length]


def generate_description(num_sentences, max_length):
    description = '\n'.join(sentences(num_sentences))
    return truncate(description, max_length)

# ************************************************
# RoleFixture
# ************************************************

class RoleFixture:
    model = 'core.role'

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'names': [],
        }) 

    def generate_name(self):
        names = tuple(ROLE_DATA.values())

        if len(self.registry['names']) >= len(names):
            return None
        while (name := sample(names, 1)[0]) in self.registry['names']:
            pass
        self.registry['names'].append(name)
        return name

    def generate_description(self):
        return generate_description(randint(1, 2), 256) # or None

    def generate_role(self):
        name = self.generate_name()
        if name is None:
            return {}

        role = {
            'name': name,
            'description': self.generate_description(),
        }
        return role

    def generate(self): # , *, count=-1):
        # if count < 0:
        #     count = randint(15, 30)

        ret = []
        pk = 1
        while role := self.generate_role():
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': role
            })
            pk += 1
        return ret


# ************************************************
# UserFixture
# ************************************************

class UserFixture:
    model = 'core.user'

    # NAMES = ['John', 'Jane', 'Fidel', 'Alice' ]

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'usernames': [],
            'emails': [],
        }) 

    def generate_username(self, fname, lname):
        alphabet = fname + ''.join(lname.split())
        size = min(randint(2, 5), len(alphabet))
        uname = generate_id(size, alphabet)

        while (u := uname.casefold()) in self.registry['usernames']:
            uname = generate_id(size, alphabet)

        self.registry['usernames'].append(u)
        return uname

    def generate_email(self, fname, lname, is_staff=False):
        lnames = lname.lower().split() 
        email = lnames[0] + '.' + fname.lower()

        for ln in lnames[1:]:
            if email not in self.registry['emails']:
                break
            email += ln
        else:
            i = 1
            e = email
            while email in self.registry['emails']:
                email = e + str(i)
                i += 1
        host = generate_host(is_staff)
        email += '@' + host
        self.registry['emails'].append(email)
        return email

    def generate_password(self, uname):
        p = [*uname]
        p.reverse()
        # return ''.join(p)
        return make_password(''.join(p))

    def generate_name(self):
        name_sz = randint(2, 4) if random() > 0.9 else 2
        fname, lname = words(name_sz, common=False).title().split(maxsplit=1)
        return fname, lname

    def generate_last_login(self):
        _, last_login = generate_datetime() 
        return last_login if random() > 0.25 else None

    def generate_is_staff(self):
        return True if random() > 0.6 else False

    def generate_is_active(self):
        return True if random() > 0.15 else False

    def generate_is_superuser(self, is_staff=False):
        # Always False if not staff
        return True if is_staff and random() > 0.95 else False

    def generate_date_joined(self):
        date_joined, _ = generate_datetime() 
        return date_joined

    def generate_roles(self, roles, is_staff):
        rs = [r['fields']['name'] for r in roles]
        ret = set()
        while not ret:
            ret = set(sample(rs, randint(1, len(rs))))
            if not is_staff:
                ret -= {ROLE_DATA['REGISTRAR'], ROLE_DATA['LECTURER']}
        return [r['pk'] for r in roles if r['fields']['name'] in ret]

    def generate_groups(self):
        #TODO
        return []

    def generate_user_permissions(self):
        #TODO
        return []

    def generate_user(self, roles):
        fname, lname = self.generate_name()
        uname = self.generate_username(fname, lname)
        is_staff = self.generate_is_staff()

        user = {
            'username': uname,
            'email': self.generate_email(fname, lname, is_staff=is_staff),
            'password': self.generate_password(uname),
            'first_name': fname,
            'last_name': lname,
            'last_login': self.generate_last_login(),
            'is_staff': is_staff,
            'is_active': self.generate_is_active(),
            'is_superuser': self.generate_is_superuser(is_staff),
            'date_joined': self.generate_date_joined(),
            'groups': self.generate_groups(),
            'roles': self.generate_roles(roles, is_staff),
            'user_permissions': self.generate_user_permissions(),
        }

        return user

    def generate(self, *, roles, count=-1):
        def normalize(users):
            """
            Does an in-place normalization of the users
            """
            def gen(ul, bound, setting, pred):
                while len(ul) < bound:
                    while (u := sample(users, 1)[0]) and not pred(u['fields']):
                        pass
                    u['fields'].update(setting)
                    ul.append(u)

            staff = []
            superusers = []
            students = []
            for u in users:
                if u['fields']['is_superuser']:
                    superusers.append(u)

                if u['fields']['is_staff']:
                    staff.append(u)
                else:
                    students.append(u)
            num_users = len(users)

            gen(superusers, ceil(num_users * randint(5, 10)/100),
                {'is_superuser': True}, lambda u: not u['is_superuser'],
            )
            gen(staff, ceil(num_users* randint(20, 25)/100),
                {'is_staff': True}, lambda u: not u['is_staff']
            )
            gen(
                students, ceil(num_users* randint(40, 55)/100),
                {'is_staff': False}, lambda u: u['is_staff'] or u['is_superuser']
            )

            return users

        if count < 0:
            count = randint(15, 20)

        ret = []
        for pk in range(1, count+1):
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': self.generate_user(roles),
            })
        return normalize(ret)


# ************************************************
# StaffFixture
# ************************************************

class StaffFixture:
    model = 'core.staff'

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'users': [],
        }) 

    # def generate_user(self, staff_ids):
    #     while (staff_id := sample(staff_ids, 1)[0]) in self.registry['users']:
    #         pass
    #     self.registry['users'].append(staff_id)
    #     return staff_id

    def generate_departments(self, faculties):
        """
        {faculties}: dictionary of faculty id to list of department ids, eg.
                    {1: (2, 8, 11, 7)}
        """
        # Probability that a staff cross-cuts across faculties
        if random() > 0.7:
            departments = []
            for d in faculties.values():
                departments += d
        else:
            # From pk=1 ... pk=len(faculties)
            departments = faculties[randint(1, len(faculties))]

        num_departments = randint(0, 4) if random() > 0.4 else 1
        departments = sample(departments, num_departments)
        return departments # or None

    def generate_staff(self, staff_ids, faculties):
        staff = {
            # 'user': self.generate_user(staff_ids),
            'departments': self.generate_departments(faculties),
        }
        return staff

    def generate(self, *, users, departments):
        staff_ids = [u['pk'] for u in users if u['fields']['is_staff']]
        faculties = {}
    
        for department in departments:
            d = faculties.setdefault(department['fields']['faculty'], [])
            d.append(department['pk'])
    
        ret = []
        # for pk in range(1, len(staff_ids)+1):
        for pk in staff_ids:
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': self.generate_staff(staff_ids, faculties),
            })
        return ret
    
    
# ************************************************
# StudentFixture
# ************************************************

class StudentFixture:
    model = 'core.student'

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'users': [],
            'student_nos': [],
        }) 

    # def generate_user(self, student_ids):
    #     while (student_id := sample(student_ids, 1)[0]) in self.registry['users']:
    #         pass
    #     self.registry['users'].append(student_id)
    #     return student_id
        
    def generate_student_no(self):
        rand_days = randint(-ceil(365.25 * 3 * random()), 0)
        now, old = generate_datetime(delta={'days': rand_days})
        isoformat = now if old is None else old

        preffix = 'S-'
        suffix = '-%d' % datetime.fromisoformat(isoformat).year 

        while (student_no := preffix + generate_id(5) + suffix) in self.registry['student_nos']:
            pass

        self.registry['student_nos'].append(student_no)
        return student_no
    
    def generate_student(self, user_ids):
        student = {
            # 'user': self.generate_user(user_ids),
            'student_no': self.generate_student_no(),
        }
        return student

    def generate(self, *, users):
        student_ids = [u['pk'] for u in users if not u['fields']['is_staff'] and not u['fields']['is_superuser']]
        ret = []
        # for pk in range(1, len(student_ids)+1):
        for pk in student_ids:
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': self.generate_student(student_ids),
            })
        return ret
    

# ************************************************
# CategoryFixture
# ************************************************

class CategoryFixture:
    model = 'core.category'

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'names': [],
        }) 

    def generate_name(self):
        while (name := sample(words(randint(1, 10), common=False).split(), 1)[0]) in self.registry['names']:
            pass
        self.registry['names'].append(name)
        return name

    def generate_description(self):
        return generate_description(randint(1, 2), 256) # or None

    def generate_category(self):
        category = {
            'name': self.generate_name(),
            'description': self.generate_description(),
        }
        return category

    def generate(self, *, count=-1):
        if count < 0:
            count = randint(15, 30)

        ret = []
        for pk in range(1, count+1):
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': self.generate_category(),
            })
        return ret


# ************************************************
# IssueFixture
# ************************************************

class IssueFixture:
    model = 'core.issue'

    def generate_owner(self, student_ids):
        return sample(student_ids, 1)[0]

    def generate_assignee(self, staff_ids):
        return sample(staff_ids, 1)[0] if random() >= 0.45 else None

    def generate_description(self):
        return generate_description(randint(0, 2), 256) or None

    def generate_title(self):
        num_words = randint(3, 10)
        return words(num_words, common=False)

    def generate_notes(self):
        if random() > 0.55:
            notes = '\n'.join(paragraphs(randint(0, 4), common=False))
        else:
            notes = None
        return truncate(notes, 4096) or None

    def generate_status(self):
        choices = tuple(Issue.STATUS_CHOICES.keys())
        return choices[randint(0, len(choices)-1)]

    def generate_priority(self):
        choices = tuple(Issue.PRIORITY_CHOICES.keys())
        return choices[randint(0, len(choices)-1)]

    def generate_escalation_level(self):
        choices = tuple(Issue.ESCALATION_CHOICES.keys())
        return choices[randint(0, len(choices)-1)]

    def generate_categories(self, category_ids):
        cats = [c for c in sample(category_ids, randint(0, len(category_ids)))]
        return cats

    def generate_issue(self, student_ids, staff_ids, categories):
        category_ids = [c['pk'] for c in categories]
        created_at, updated_at = generate_datetime()

        issue = {
            'owner': self.generate_owner(student_ids),
            'assignee': self.generate_assignee(staff_ids),
            'title': self.generate_title(),
            'description': self.generate_description(),
            'status': self.generate_status(),
            'categories': self.generate_categories(category_ids),
            'priority': self.generate_priority(),
            'escalation_level': self.generate_escalation_level(),
            'notes': self.generate_notes(),
            'created_at': created_at,
            'updated_at': updated_at,
        }
        return issue

    def generate(self, *, students, staff, categories, count=-1):
        if count < 0:
            count = randint(15, 30)

        # student_ids = [s['fields']['user'] for s in students]
        # staff_ids = [s['fields']['user'] for s in staff]
        student_ids = [s['pk'] for s in students]
        staff_ids = [s['pk'] for s in staff]
    
        ret = []
        for pk in range(1, len(student_ids)+1):
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': self.generate_issue(student_ids, staff_ids, categories),
            })
        return ret
    

# ************************************************
# IssueLogFixture
# ************************************************

class IssueLogFixture:
    model = 'core.issuelog'
    _sample_fields = ['assignee', 'categories', 'status', 'priority', 'escalation_level']

    def __init__(self):
        self.issue_gen = IssueFixture()
        self.attachment_gen = AttachmentFixture()

    def generate_assignee(self, users):
        staff_ids = [u['pk'] for u in users if u['fields']['is_staff']]
        return self.issue_gen.generate_assignee(staff_ids)

    def generate_actor(self, issue, users):
        if random() <= 0.85:
            for u in users:
                if u['pk'] == issue['fields']['assignee']:
                    users = [u]
                    break
        while user := sample(users, 1)[0]:
            if user['fields']['is_staff'] or user['fields']['is_superuser']:
                return user['pk']

    def generate_categories(self, category_ids):
        cats = sample(category_ids, ceil(len(category_ids)*randint(0, 70)/100))
        if not cats:
            cats = category_ids
        return self.issue_gen.generate_categories(cats)

    def generate_status(self):
        return self.issue_gen.generate_status()

    def generate_priority(self):
        return self.issue_gen.generate_priority()

    def generate_escalation_level(self):
        return self.issue_gen.generate_escalation_level()

    def generate_attachment(self, issue, attachments):
        if random() > 0.6:
            return None
        attachment = self.attachment_gen.generate(issues=[issue])[0]
        attachments.append(attachment)
        return attachment['fields']['file']

    def generate_issuelog(self, issues, users, attachments):
        num_fields = randint(1, 5) if random() > 0.8 else randint(1, 2)
        fields = {}
        issue = sample(issues, 1)[0]

        while num_fields > 0 and (field := sample(self._sample_fields, 1)[0]) not in fields.keys():
            func = getattr(self, 'generate_' + field)

            args = []
            if field == 'assignee':
                args.append(users)
            elif field == 'categories':
                args.append(issue['fields']['categories'])

            # while (value := func(*args)) == issue['fields'][field]:
            #     pass

            fields[field] = func(*args) # value
            num_fields -= 1

        created_at, _ = generate_datetime()
        while datetime.fromisoformat(created_at) < datetime.fromisoformat(issue['fields']['created_at']):
            created_at, _ = generate_datetime()

        issuelog = {
            'issue_id': issue['pk'],
            'actor': self.generate_actor(issue, users),
            'attachments': self.generate_attachment(issue, attachments),
            'created_at': created_at,
        }
        for field in self._sample_fields:
            issuelog[field] = issue['fields'][field]

        issuelog.update(fields)

        return issuelog

    def generate(self, *, issues, users, attachments, count=-1):
        if count < 0:
            count = randint(15, 100)

        ret = []
        for pk in range(1, count+1):
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': self.generate_issuelog(issues, users, attachments),
            })
        return ret


# ************************************************
# AttachmentFixture
# ************************************************

class AttachmentFixture:
    model = 'core.attachment'

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'files': [],
            'pks': [],
        }) 

    EXTS = {
        'application/pdf': ('pdf',),
        'image/%s': ('png', 'jpeg', 'gif', 'webp'),
        'image/jpeg': ('jpg',),
        'text/plain': ('txt',),
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ('doc', 'docx'),
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': ('ppt', 'pptx'),
    }

    def generate_file(self):
        while (file := str(uuid.uuid4())) in self.registry['files']:
            pass
        self.registry['files'].append(file)
        return file

    def generate_name(self):
        num_words = randint(1, 8)
        name = words(num_words, common=False)
        sep = sample([' ', '-', '_'], 1)[0]

        exts = []
        for e in self.EXTS.values():
            exts += e
        ext = sample(exts, 1)[0]

        filename = '%s.%s' % (sep.join(name.split()), ext)
        return filename

    def generate_type(self, filename):
        _, _, ext = filename.rpartition('.')
        for mimetype, exts in self.EXTS.items():
            if ext in exts:
                return mimetype.replace('%s', ext)
        return 'application/octet-stream'

    def generate_issue_id(self, issue_ids):
        """
        {issues}: list of issue ids
        """
        return sample(issue_ids, 1)[0]

    def generate_size(self):
        upper = 1024 * 1024 * 5 # 5MiB
        if random() > 0.85:
            lower = upper
            upper *= 2 # 10MiB
        else:
            lower = 0
        size = randint(lower, upper)
        return size

    def generate_attachment(self, issue_ids):
        """
        {issues}: list of issue ids
        """
        filename = self.generate_name()
        created_at, _ = generate_datetime()
        attachment = {
            'file': self.generate_file(),
            'issue_id': self.generate_issue_id(issue_ids),
            'name': filename,
            'type': self.generate_type(filename),
            'size': self.generate_size(),
            'created_at': created_at,
        }
        return attachment

    def generate(self, *, issues, count=-1):
        if count < 0:
            count = randint(min(1, len(issues)), len(issues))

        issue_ids = [i['pk'] for i in issues]
        ret = []
        pks = len(self.registry['pks'])

        for i in range(pks, pks + count):
            attachment = self.generate_attachment(issue_ids)
            ret.append({
                'model': self.model,
                'pk': i+1, # issue['file'],
                'fields': attachment,
            })
            self.registry['pks'].append(i+1)
        return ret


# ************************************************
# FacultyFixture
# ************************************************

class FacultyFixture:
    model = 'core.faculty'

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'names': [],
        }) 

    def generate_name(self):
        names = tuple(FACULTY_DATA.keys())

        if len(self.registry['names']) >= len(names):
            return None
        while (name := sample(names, 1)[0]) in self.registry['names']:
            pass
        self.registry['names'].append(name)
        return name
        
    def generate_description(self):
        return generate_description(randint(1, 2), 256) # or None

    def generate_faculty(self):
        name = self.generate_name()
        if name is None:
            return {}

        created_at, _ = generate_datetime()

        faculty = {
            'name': name,
            'description': self.generate_description(),
            'created_at': created_at,
        }
        return faculty

    def generate(self): # *, count=-1):
        ret = []
        pk = 1
        while faculty := self.generate_faculty():
            ret.append({
                'model': self.model,
                'pk': pk,
                'fields': faculty
            })
            pk += 1
        return ret
    
    
# ************************************************
# DepartmentFixture
# ************************************************

class DepartmentFixture:
    model = 'core.department'

    def __init__(self):
        self.registry = REGISTRY.setdefault(self.__class__, {
            'departments': {},
        }) 

    def generate_name(self, faculty):
        """
        {faculty}: Faculty name
        """
        if (fd_departments := FACULTY_DATA.get(faculty, None)) is None:
            return None

        departments = self.registry['departments'].setdefault(faculty, [])

        if len(departments) >= len(fd_departments):
            return None
        while (name := sample(fd_departments, 1)[0]) in departments:
            pass

        departments.append(name)
        return name

    def generate_description(self):
        return generate_description(randint(1, 2), 256) # or None

    def generate_faculty(self, faculty):
        """
        {faculty}: Faculty name
        """
        return 1 + list(self.registry['departments'].keys()).index(faculty)

    def generate_department(self, faculty):
        """
        {faculty}: Faculty name
        """
        if (name := self.generate_name(faculty)) is None:
            return {}

        created_at, updated_at = generate_datetime()

        department = {
            'name': name,
            'description': self.generate_description(),
            'faculty': self.generate_faculty(faculty),
            'created_at': created_at,
            'updated_at': updated_at,
        }
        return department

    def generate(self, *, faculties): # , count=-1):
        ret = []
        pk = 1
        for faculty in faculties:
            while department := self.generate_department(faculty['fields']['name']):
                # if count > -1:
                #     if count == 0:
                #         return ret
                #     count -= 1
                ret.append({
                    'model': self.model,
                    'pk': pk,
                    'fields': department
                })
                pk += 1
        return ret
    


# *****************************************************

def main():
    
    roles = RoleFixture().generate()
    users = UserFixture().generate(roles=roles)
    faculties = FacultyFixture().generate()
    departments = DepartmentFixture().generate(faculties=faculties)
    staff = StaffFixture().generate(users=users, departments=departments)
    students = StudentFixture().generate(users=users)
    categories = CategoryFixture().generate()
    issues = IssueFixture().generate(students=students, staff=staff, categories=categories)
    attachments = AttachmentFixture().generate(issues=issues)
    issuelogs = IssueLogFixture().generate(issues=issues, users=users, attachments=attachments)

    data = [
        *roles, *users, *faculties, *departments,
        *staff, *students, *categories, *issues,
        *attachments, *issuelogs
    ]
    json.dump(data, sys.stdout) #, indent=2)


if __name__ == '__main__':
    main()
