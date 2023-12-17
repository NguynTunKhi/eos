$(document).ready(function() {
    
    // Todo : dang loi js jqval
    
    jqval.validateForm("form",
        {
            username: {
                required: true,
                rangelength: [1, 64],
                server: true
            },
            password: {
                required: true,
                rangelength: [1, 64],
                server: true
            },
            password_again: {
                required: true,
                rangelength: [1, 64],
                matchpassword: true,
                server: true
            }
        }, 
        {
            username: {
                required: "{{=T('MSG_ERR_NOT_EMPTY')}}",
                rangelength: "{{=T('ERR_MIN_MAX_1_64')}}",
            },
            password: {
                required: "{{=T('MSG_ERR_NOT_EMPTY')}}",
                rangelength: "{{=T('ERR_MIN_MAX_1_64')}}",
            },
            password_again: {
                required: "{{=T('MSG_ERR_NOT_EMPTY')}}",
                rangelength: "{{=T('ERR_MIN_MAX_1_64')}}",
                matchpassword: "{{=T('MSG_ERR_UNMATCHED_PASSWORD')}}",
            }
        });
    jqval.enableServerErrors("form");
});