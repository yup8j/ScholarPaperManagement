from .login import *

dir_prefix = 'ScholarPaper.resources.'

apis = [
    'login:login',
    'root:root'
]

blueprints = [dir_prefix + api for api in apis]
