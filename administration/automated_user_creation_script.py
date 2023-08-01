from apps.employees.models import Employee
from apps.employees.views import get_random_string
from django.contrib.auth.models import User, Group
from apps.comms.sms_api import send_sms

employees = Employee.objects.filter(designation__name__iexact='Secretary')

for employee in employees:
    if employee.user:
        pass
    else:
        username=str(employee.phone)
        new_password = get_random_string(8)
        if username:
            try:
                user = User.objects.create_user(username=username,password=new_password)
                user.is_active=True
                user.first_name=employee.first_name
                user.last_name=employee.surname
                user.groups.add(Group.objects.get(name__iexact='Secretary'))
                user.save()
                destination = employee.phone
                employee.user=user
                employee.save()
                msg = "Ndugu "+str(employee).title()+", karibu katika mfumo wa skuli. Tumia link stmathias.skuli.co kuingia. Username yako ni "+username+" na password ni "+new_password+" Asante"
                
                if destination:
                    send_sms(msg,destination)
            except:
                print('username exists: ' + str(username))

