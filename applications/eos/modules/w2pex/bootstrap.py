from gluon.sqlhtml import *

StringWidget._class = 'form-control'
IntegerWidget._class = 'form-control'
DoubleWidget._class = 'form-control'
DecimalWidget._class = 'form-control'
TimeWidget._class = 'form-control'
DateWidget._class = 'form-control date'
DatetimeWidget._class = 'form-control datetime'
TextWidget._class = 'form-control'
JSONWidget._class = 'form-control'
BooleanWidget._class = ''
OptionsWidget._class = 'form-control'
ListWidget._class = 'form-control'
MultipleOptionsWidget._class = 'form-control'
RadioWidget._class = ''
CheckboxesWidget._class = ''
PasswordWidget._class = 'form-control'
UploadWidget._class = 'form-control'
AutocompleteWidget._class = 'form-control'

class BootstrapWidgets:
    def __init__(self):
        pass
