import getpass

from cement import Controller, ex
from cement.utils.version import get_version_banner

from akinoncli.core.exc import AkinonCLIError
from ..core.version import get_version


VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (get_version(), get_version_banner())


# class Users(Controller):
#     class Meta:
#         label = 'user'
#         stacked_type = 'nested'
#         stacked_on = 'base'
#         description = 'this is the users controller namespace'
#
#     @ex(
#         help='User List Command',
#         arguments=[
#             (['-r', '--role'], {
#                 'help': 'Filter by role id',
#                 'action': 'store',
#                 'dest': 'role'
#             })
#         ],
#     )
#     def list(self):
#         qs = {}
#         if self.app.pargs.role:
#             qs['role'] = self.app.pargs.role
#         response = self.app.client.get_users(qs)
#         rows = response.data.get('results', [])
#         for row in rows:
#             row['role_name'] = row['role']['name']
#             row['role_id'] = row['role']['pk']
#         self.app.render(data=response.data, rows=rows,
#                         headers={'pk': 'ID', 'first_name': 'First Name', 'last_name': 'Last Name',
#                                  'email': 'Email', 'role_name': 'Role'},
#                         is_succeed=response.is_succeed)
#
#     @ex(
#         help='User Create Command',
#         arguments=[]
#     )
#     def create(self):
#         first_name = input('First Name:')
#         last_name = input('Last Name:')
#         role = input('Role ID:')
#         email = input('Email:')
#         password = getpass.getpass(prompt='Password:')
#         password2 = getpass.getpass(prompt='Password Confirm:')
#         if password != password2:
#             raise AkinonCLIError("Passwords did not match")
#         data = {
#             'first_name': first_name,
#             'last_name': last_name,
#             'email': email,
#             'password': password,
#             'role': role
#         }
#         response = self.app.client.create_user(data)
#         if response.is_succeed:
#             self.app.render({}, is_text=True, custom_text="User added successfully.")
#         else:
#             errors = ''
#             for key, value in response.data.items():
#                 errors += f'{key}: {value[0]}\n'
#             self.app.render({}, is_text=True, custom_text=errors)
#
#
# class Roles(Controller):
#     class Meta:
#         label = 'role'
#         stacked_type = 'nested'
#         stacked_on = 'base'
#         description = 'this is the roles controller namespace'
#
#     @ex(
#         help='Role List Command',
#         arguments=[],
#     )
#     def list(self):
#         response = self.app.client.get_roles()
#         self.app.render(data=response.data, rows=response.data.get('results', []),
#                         headers={'pk': 'ID', 'name': 'Name'},
#                         is_succeed=response.is_succeed)
#
#     @ex(
#         help='Role Create Command',
#         arguments=[
#             (['name'], {
#                 'help': 'Role Name',
#                 'action': 'store'
#             })
#         ],
#     )
#     def create(self):
#         data = {
#             'name': self.app.pargs.name
#         }
#         response = self.app.client.create_role(data)
#         if response.is_succeed:
#             self.app.render({}, is_text=True, custom_text="Role created successfully.")
#         else:
#             self.app.render({}, is_text=True, custom_text=response.data.get('non_field_errors') or response.data.get('name'))
