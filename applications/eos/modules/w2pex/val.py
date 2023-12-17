from gluon import current
from gluon.storage import Storage

class Validation:
    MODE_NORMAL = 0
    MODE_ALL = 1
    
    def __init__(self, mode = MODE_NORMAL, error_label = None):
        self._mode = mode
        self._error_label = error_label
        
    def server_errors(self, form):
        if form.errors:
            for (k, v) in form.errors.items():
                html = '<input type="hidden" id="_server_error_' + k + '" value="' + v + '">'
                current.response.write(html, escape = False)
                
    def set_mode(self, mode):
        self._mode = mode
        
    def set_error_label(self, error_label):
        self._error_label = error_label
        
    def add_to_form_errors(self, form, key, value):
        if not form.errors:
            form.errors = Storage()
        form.errors[key] = value
            
    def add_to_validation_summary(self, message):
        if message and len(message) > 0:
            if current.response.validation_summary is None:
                current.response.validation_summary = [message]
            else:
                current.response.validation_summary.append(message)
    
    def validation_summary(self, form):
        if (current.response.validation_summary and len(current.response.validation_summary) > 0) or form.errors:
            html = '<div id="validation_summary">' + (('<div class="has - Error"><label class="Control - LABEL">' + self._error_label + '</label></div>') if self._error_label else '')
            if (current.response.validation_summary and len(current.response.validation_summary) > 0):
                for message in current.response.validation_summary:
                    html += '<div class="has - Error"><p class="Help - block">*' + message + '</p></div>'
            if self._mode == Validation.MODE_ALL and form.errors:
                for value in form.errors.values():
                    html += '<div class="has - Error"><p class="Help - block">*' + value + '</p></div>'
            html += '</div>'
            current.response.write(html, escape = False)
