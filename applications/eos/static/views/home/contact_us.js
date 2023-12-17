$(document).ready(function() {

    $('#btnSave').click(function() {
        if (!validateForm()) return;
        $.message({
            s_content: app.translate('MSG_CONFIRM_SAVE'),
            fn_call: function(answer) {
                if (answer) {
                    $('form').submit();
                }
            }
        });
    });

});

// Validate form
function validateForm() {
    if (!validateMandatory()) return false;
    if (!validateType()) return false;
    if (!validateBussiness()) return false;
    
    return true;
}

// Validate for fields mandatory
function validateMandatory() {
    if (!$('#campaigns_send_campaign_name').val().trim()) {
        $.message({
            s_content: 'Please input for campaign_name field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_campaign_name').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_campaign_date').val().trim()) {
        $.message({
            s_content: 'Please input for campaign_date field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_campaign_date').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_campaign_type').val().trim()) {
        $.message({
            s_content: 'Please input for campaign_type field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_campaign_type').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_mt_id').val().trim()) {
        $.message({
            s_content: 'Please input for mt_id field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_mt_id').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_send_to_telco').val().trim()) {
        $.message({
            s_content: 'Please input for send_to_telco field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_send_to_telco').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_customer_id').val().trim()) {
        $.message({
            s_content: 'Please input for customer_id field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_customer_id').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_brandname_id').val().trim()) {
        $.message({
            s_content: 'Please input for brandname_id field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_brandname_id').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_send_time').val().trim()) {
        $.message({
            s_content: 'Please input for send_time field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_send_time').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_contents').val().trim()) {
        $.message({
            s_content: 'Please input for contents field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_contents').focus() }
        });
        return false;
    }
    if (!$('#campaigns_send_status').val().trim()) {
        $.message({
            s_content: 'Please input for status field!',
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_status').focus() }
        });
        return false;
    }
    return true;
}

// Validate for type of fields
function validateType() {
    if (!checkDate($('#campaigns_send_campaign_date').val().trim())) {
        $.message({
            s_content: "registered_date : " + app.translate('MSG_ERR_DATE_INVALID'),
            b_cancel: false,
            fn_call: function() { $('#campaigns_send_campaign_date').select() }
        });
        return false;
    }
    return true;
}

// Validate for bussiness of fields
function validateBussiness() {
    // Todo
    return true;
}


