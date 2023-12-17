default_application = "eos"
default_controller = "master"
default_function = "login"

routes_in = (
    ((r'.*http://enviinfo\.cem\.gov\.vn.* /', r'/eip/default/index')),
    #((r'.*http://enviinfo\.cem\.gov\.vn.* (?P<any>.*)', r'/eip/\g<any>')),
)