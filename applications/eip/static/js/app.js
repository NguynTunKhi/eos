/**
 * Created by Admin on 5/4/2017.
 */


var CommonApp = jQuery.Class({
    appName: '',
    controllerName: '',
    viewName: '',
    fullDateTime: '',
    shortDate: '',

    confirmBack: function() {
        window.history.back();
    },

    showPopup: function (data) {
        var thisInstance = this;
        $.alert({
            title: data.title,
            content: data.content,
            // icon: 'fa fa-check',
            // icon: 'fa fa-warning',
            // icon: 'fa fa-info',
            animation: 'zoom',
            closeAnimation: 'zoom',
            buttons: {
                okay: {
                    text: thisInstance.translate('LBL_OK'),
                    btnClass: 'btn btn-primary'
                }
            }
        });
    },
    
    showNotification: function (data) {
        var thisInstance = this;
        $.alert({
            title: thisInstance.translate("LBL_NOTIFICATION"),
            content: data.content,
            // icon: 'fa fa-check',
            // icon: 'fa fa-warning',
            icon: 'fa fa-info',
            animation: 'zoom',
            closeAnimation: 'zoom',
            buttons: {
                okay: {
                    text: thisInstance.translate('LBL_OK'),
                    btnClass: 'btn btn-primary'
                }
            }
        });
    },

    showError: function (msg) {
        var thisInstance = this;
        var content = msg;
        // console.log('show err');
        // console.log(content);
        if (content == '0: error'){
            content = thisInstance.translate("MSG_ERROR");

        }
        $.alert({
            title: thisInstance.translate("LBL_ERROR"),
            content: "<span style='color: red;'>" + content + "</span>",
            icon: 'fa fa-warning',
            animation: 'zoom',
            closeAnimation: 'zoom',
            buttons: {
                okay: {
                    text: '<i class="fa fa-check"></i>&nbsp;' + thisInstance.translate('LBL_OK'),
                    btnClass: 'btn btn-primary'
                }
            }
        });
    },

    showProgress: function (target) {
        var loadingIcon = $('#hfLoadingIcon').val();
        if (target) {
            $(target).block({
                blockMsgClass: 'blockOnDiv',
                message: this.translate('LBL_PLEASE_WAIT') + '<img style="width: 25px; height: 25px;" src="' + loadingIcon + '" />'
            });
        } else {
            $.blockUI({
                blockMsgClass: 'myBlockUI',
                message: this.translate('LBL_PLEASE_WAIT') + '<img style="width: 25px; height: 25px;" src="' + loadingIcon + '" />'
            });
        }
    },

    hideProgress: function (target) {
        if (target) {
            $(target).unblock();
        } else {
            $.unblockUI();
        }
    },
    
    postAjax: function (options) {
        var thisInstance = this;
		var defaults = {
            url: '',
            data: '',
            showProgress: true,
            processData: true,
            async: true,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            enctype: 'multipart/form-data',
            callback: function (res) {
            }
		};
		options =  $.extend(defaults, options);
		if (options.showProgress){
		    thisInstance.showProgress();
        }
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: options.url,
            data: options.data,
            async: options.async,
            processData: options.processData,
            contentType: options.contentType,
            enctype: options.enctype,
            success: function(data){
                thisInstance.hideProgress();
                options.callback(data);
            },
            error: function(err){
                thisInstance.hideProgress();
                thisInstance.showError(err.status + ": " + err.statusText);
            }
        });
    },

    showConfirmBox: function (data) {
        var thisInstance = this;
		var defaults = {
            title: thisInstance.translate('LBL_CONFIRM_ACTION'),
            icon: 'fa fa-question-circle',
            content: '',
            animation: 'scale',
            closeAnimation: 'scale',
            opacity: 0.5,
            confirm_text: thisInstance.translate('LBL_OK'),
            cancel_text: thisInstance.translate('LBL_CANCEL'),
            callback: function () {
                console.log('Callback');
            },
            cancel_callback: function () {
                console.log('Callback');
            }
		};
		data =  $.extend(defaults, data);
        $.confirm({
            title: data.title,
            content: data.content,
            icon: data.icon,
            animation: data.animation,
            closeAnimation: data.closeAnimation,
            opacity: data.opacity,
            buttons: {
                confirm: {
                    text: '<i class="fa fa-check"></i>' + data.confirm_text,
                    btnClass: 'btn btn-primary',
                    action: function () {
                        data.callback();
                    }
                },
                cancel: {
                    text: '<i class="fa fa-remove"></i>' + data.cancel_text,
                    btnClass: 'btn btn-default',
                    action: function () {
                        data.cancel_callback();
                    }
                }
            }
        });
    },
    
    getItemsOnDatatable: function (iTable, isChecked){
        if (!iTable){
            iTable = 0;
        }
        if (!isChecked){
            isChecked = true;
        }
        var table = $("#custom_datatable_" + iTable);
        var items = null;
        if (isChecked){
            items = table.find("input.select_item:checked");
        } else {
            items = table.find("input.select_item");
        }
        var ret = [];
        var total = items.length;
        if (total > 0){
            for(var i = 0; i < total; i++){
                ret.push($(items[i]).val());
            }
        }
        return ret;
    },
    
    executeFunction: function(instance){
        var thisInstance = this;
        if ($(instance).attr("disabled")){
            return true;
        }
        var iTable = $(instance).attr('data-iTable');
        var ids = thisInstance.getItemsOnDatatable(iTable).join(',');
        if (ids == ''){
            app.showError(app.translate('MSG_SELECT_ATLEAST_ONE_RECORD'));
            return true;
        }
        var messageConfirm = $(instance).attr('data-confirm');
        subExecuteFunction = function(instance, thisInstance){
            var url = $(instance).attr('data-url');
            thisInstance.postAjax({
                url: url,
                data: {ids: ids},
                callback: function (data) {
                    oTable[iTable].fnDraw();
                }
            });
        }
        if (messageConfirm){
            thisInstance.showConfirmBox({
                content: messageConfirm,
                callback: function () {
                    subExecuteFunction(instance, thisInstance);
                },
            });
        } else {
            subExecuteFunction(instance, thisInstance);
        }
    },

    translate: function (key) {
        var ret = key;
        if ($("#js_strings").text() != '' && $("#js_strings").text() != undefined){
            var strings = JSON.parse($("#js_strings").text());
            if(strings[key] != undefined){
                ret =strings[key];
            }
        }
        return ret;
    },

    overwriteValidator: function () {
        var thisInstance = this;
        // Overwrite message for jquery validator
        jQuery.extend(jQuery.validator.messages, {
            required: thisInstance.translate("LBL_INPUT_MANDATORY_FIELD"),
            remote: thisInstance.translate("Please fix this field."),
            email: thisInstance.translate("Please enter a valid email address."),
            url: thisInstance.translate("Please enter a valid URL."),
            date: thisInstance.translate("Please enter a valid date."),
            dateISO: thisInstance.translate("Please enter a valid date (ISO)."),
            number: thisInstance.translate("Please enter a valid number."),
            digits: thisInstance.translate("Please enter only digits."),
            creditcard: thisInstance.translate("Please enter a valid credit card number."),
            equalTo: thisInstance.translate("Please enter the same value again."),
            accept: thisInstance.translate("Please enter a value with a valid extension."),
            maxlength: jQuery.validator.format(thisInstance.translate("Please enter no more than {0} characters.")),
            minlength: jQuery.validator.format(thisInstance.translate("Please enter at least {0} characters.")),
            rangelength: jQuery.validator.format(thisInstance.translate("Please enter a value between {0} and {1} characters long.")),
            range: jQuery.validator.format(thisInstance.translate("Please enter a value between {0} and {1}.")),
            max: jQuery.validator.format(thisInstance.translate("Please enter a value less than or equal to {0}.")),
            min: jQuery.validator.format(thisInstance.translate("Please enter a value greater than or equal to {0}."))
        });
        // Add method check if the phone number is valid
        jQuery.validator.addMethod("phone", function(value, element) {
            var re = new RegExp(/^([+]84|0)[1-9]([0-9]{8})$/);
            phone_number = value.replace(/\s+/g, '');
            return this.optional(element) || re.test(phone_number);
        }, thisInstance.translate('Please enter a valid phone number'));
        // Add method check if the username is valid
        jQuery.validator.addMethod("username", function(value, element) {
            var re = new RegExp(/^[a-zA-Z0-9._]+$/g);
            return re.test(value);
        }, thisInstance.translate('Please enter a valid username'));
    },

    strToDatetime: function(s){
        s = s.split(' ');
        var d = s[0].split('-');
        var dd = d[0];
        var mm = parseInt(d[1]) - 1;
        var yyyy = d[2];
        var t = s[1].split(':');
        var HH = t[0];
        var MM = t[1];
        var SS = t[2];
        return new Date(yyyy, mm, dd, HH, MM, SS);
    },

    showMessageWhenHasError: function () {
        var msg = $("#hfError").val();
        var enableDebugClient = $("#hfEnableDebugClient").val();
        if(msg != undefined && msg != '' && enableDebugClient == 'True'){
            this.showError(msg);
        }
    },

    registerValidateForm: function () {
		// validate signup form on keyup and submit
		$("form").validate({
			rules: {
				firstname: "required",
				lastname: "required",
				username: {
					required: true,
					minlength: 2
				},
				password: {
					required: true,
					minlength: 5
				},
				confirm_password: {
					required: true,
					minlength: 5,
					equalTo: "#password"
				},
				email: {
					required: true,
					email: true
				},
				topic: {
					required: "#newsletter:checked",
					minlength: 2
				},
				agree: "required"
			},
			messages: {
				firstname: "Hãy nhập họ tên!",
				lastname: "Hãy nhập Tên!",
				username: {
					required: "Hãy nhập tên tài khoản đăng nhập!",
					minlength: "Tên tài khoản đăng nhập cần ít nhất 2 ký tự!"
				},
				password: {
					required: "Hãy nhập mật khẩu!",
					minlength: "Mật khẩu cần ít nhất 5 ký tự!"
				},
				confirm_password: {
					required: "Hãy nhập mật khẩu!",
					minlength: "Mật khẩu cần ít nhất 5 ký tự!",
					equalTo: "Mật khẩu không khớp nhau"
				},
				email: "Định dạng email không đúng!",
				agree: "Bạn có đồng chí với chính sách của chúng tôi?",
				topic: "Hãy chọn ít nhất 2 chủ đề!"
			}
		});
    },

    registerEventsForCommonInput: function () {
        var thisInstance = this;

        $('.time').datetimepicker({
            datepicker:false,
            format: 'H:i:s',
            step:5
        });

        $( ".date" ).datetimepicker({
            format: thisInstance.shortDate,
	        timepicker:false,
        });

        $('.datetime').datetimepicker({
            format: thisInstance.fullDateTime
        });

        $("input, textarea, select").click(function () {
            $(this).formError({remove: true});
        });

        $('select').chosen({width: "100%"});
        // Overwrite message for jquery validator
        this.overwriteValidator();
    },

    exportData: function (url, data) {
        var thisInstance = this;
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: url,
            data: data,
            success: function(data){
                if(data.success){
                    var url = data.url;
                    thisInstance.showConfirmBox({
                        title: thisInstance.translate('Information'),
                        icon: 'fa fa-info-circle',
                        content: thisInstance.translate('LBL_EXPORT_DATA_SUCCESSFULLY_CLICK_OK_TO_VIEW'),
                        callback: function () {
                            window.open(url);
                        }
                    });
                } else {
                    thisInstance.showError(".errors").html(data.message);
                }
            },
            error: function(err){
                thisInstance.showError(err.status + ": " + err.statusText);
            }
        });
    },

    convertUrlToDataParams: function (url) {
        var params = {};
        if (typeof url !== 'undefined' && url.indexOf('?') !== -1) {
            var urlSplit = url.split('?');
            url = urlSplit[1];
        }
        var queryParameters = url.split('&');
        for (var index = 0; index < queryParameters.length; index++) {
            var queryParam = queryParameters[index];
            var queryParamComponents = queryParam.split('=');
            params[queryParamComponents[0]] = queryParamComponents[1];
        }
        return params;
    },

    registerEventsForCommonButton: function () {
        var thisInstance = this;

        // Lien quan den chuc nang search cua he thong
        if (1==1) {
            var params = app.convertUrlToDataParams(location.href);
            if (params.search) {
                $("#txtSearch").val(params.search);
            }

            if ($("#hfUrlToSearch").length > 0 && $("#hfUrlToSearch").val() != '') {
                $("#txtSearch").keypress(function (e) {
                    if (e.key == 'Enter') {
                        var url = $("#hfUrlToSearch").val();
                        var search = $(this).val().trim();
                        url += "?search=" + search;
                        location.href = url;
                    }
                });
            } else {
                $("#txtSearch").closest('div').hide();
            }
        }

        // Active menu
        // if (1==1){
            // var controller = $("#hfMenuNameCommon").val();
            // var menuName = controller;
            // if (controller == 'broker'){
                // menuName = 'zookeeper';
            // }
            // $("ul.metismenu li").removeClass("active");
            // var entity = $("ul.metismenu li[data-name='" + menuName + "']");
            // if (entity.length > 0){
                // entity.addClass("active");
            // } else {
                // $("ul.metismenu li[data-name='administrator']").addClass("active");
            // }
        // }

        $("body").undelegate(".btnChoise", "click");
        $("body").delegate(".btnChoise", "click", function () {
            if($(this).attr('disabled')){
                return false;
            }
            if($(".ModalWrap").length == 0){
                $("body").append("<div class='ModalWrap'></div>");
            } else {
                $(".CurrentDialogWrap").remove();
                $("body").append("<div class='ModalWrap'></div>");
            }
            var url = $(this).attr("data-url");
            var target = $(this).attr("data-for");
            var multiple = $(this).attr("data-multiple");
            var callback = $(this).attr("data-callback");
            $(".ModalWrap").load(url, function () {
                var instance = $(this);
                instance.find(".modal").show();
                instance.find(".modal-header span.close, .btnCancel, .btnOK").unbind("click");
                instance.find(".modal-header span.close, .btnCancel").click(function () {
                    instance.remove();
                });
                instance.find(".btnOK").click(function () {
                    var allChecked = instance.find(".select_item:checked");
                    var totalChecked = allChecked.length;
                    if (totalChecked == 0){
                        instance.find(".errors").html(thisInstance.translate('LBL_HAVE_NOT_SELECTED_RECORD_YET'));
                        return;
                    }
                    if(!(multiple == "true" || multiple == "yes" || multiple == "1")){
                        if(totalChecked > 1){
                            instance.find(".errors").html(thisInstance.translate('LBL_ONLY_SELECT_ONE_RECORD'));
                            return;
                        }
                    }
                    var value = '', display = '';
                    allChecked.each(function () {
                        if(value != ''){
                            value += ',';
                            display += '; ';
                        }
                        value +=  $(this).attr("data-value");
                        display +=  $(this).attr("data-display");
                    });
                    $(target).val(value);
                    $(target + "_display").val(display);

                    if(totalChecked == 1) {
                        var currentTable = $(this).closest(".modal").find("table");
                        var currentCheckbox = currentTable.find("input.select_item:checked");
                        var configs = currentTable.attr("data-extend").toLowerCase().trim();
                        configs = configs.split(',');
                        var total = configs.length;
                        for (var i = 0; i < total; i++){
                            config = configs[i].trim();
                            config = config.split(':');
                            if (config[0].trim() != ''){
                                $("#" + config[0]).val(currentCheckbox.attr("data-" + config[0]));
                            }
                        }
                    }
                    
                    // Remove wrap tag
                    instance.remove();
                    
                    // Callback
                    var functionName = callback.split("(")[0];
                    if (callback != undefined && callback != '' && eval("typeof " + functionName) != "undefined"){
                        eval(callback);
                    }
                });
            });
        });

        $("body").undelegate(".btnAddNew", "click");
        $("body").delegate(".btnAddNew", "click", function () {
            if($(".ModalWrap").length == 0){
                $("body").append("<div class='ModalWrap'></div>");
            } else {
                $(".CurrentDialogWrap").remove();
                $("body").append("<div class='ModalWrap'></div>");
            }
            var url = $(this).attr("data-url");
            var target = $(this).attr("data-for");
            var multiple = $(this).attr("data-multiple");
            var params = $(this).attr("data-params");
            var callback = $(this).attr("data-callback");
            var hasScroll = $(this).attr("data-hasScroll");
            if (!hasScroll){
                hasScroll = '';
            }
            hasScroll = hasScroll.toLowerCase();
            if (params){
                if (url.indexOf('?') > -1){
                    url += '&' + params;
                } else {
                    url += '?' + params;
                }
            }
            $(".ModalWrap").load(url, function () {
                // Register events for new controls
                app.registerEventsForCommonInput();

                var instance = $(this);
                instance.find(".modal").show();
                if (hasScroll == '1' || hasScroll == 'true'){
                    $('.scroll_content').slimscroll({
                        height: '450px'
                    });
                }
                instance.find(".modal-header span.close, .btnCancel, .btnSave").unbind("click");
                instance.find(".modal-header span.close, .btnCancel").click(function () {
                    instance.remove();
                });
                instance.find(".btnSave").click(function () {
                    if($(this).closest(".modal").find("form").validate().form() == false){
                        return;
                    }
                    var currentForm = $(this).closest(".modal").find("form");
                    var url = currentForm.attr('action');
                    $.ajax({
                        type: "POST",
                        dataType: 'json',
                        url: url,
                        data: currentForm.serialize(),
                        success: function(data){
                            if(data.success){
                                $(target).val(data.value);
                                $(target + "_display").val(data.display);
                                for(key in data.data){
                                    $("#" + key).val(data[key]);
                                };
                                // Remove wrap tag
                                instance.remove();
                    
                                // Callback
                                var functionName = callback.split("(")[0];
                                if (callback != undefined && callback != '' && eval("typeof " + functionName) != "undefined"){
                                    eval(callback);
                                }
                            } else {
                                instance.find(".errors").html(data.message);
                            }
                        },
                        error: function(err){
                            instance.find(".errors").html(err.status + ": " + err.statusText);
                        }
                     });
                });
            });
        });

        $("body").undelegate(".select_all", "click");
        $("body").delegate(".select_all", "click", function () {
            var currentValue = $(this).prop("checked");
            var group = $(this).attr("group");
            var childrenSelections = ".select_item";
            if (group){
                childrenSelections += "[group='" + group + "']";
            }
            $(this).closest("table").find(childrenSelections).prop("checked", currentValue);
        });

        $("body").undelegate(".select_item", "click");
        $("body").delegate(".select_item", "click", function () {
            var group = $(this).attr("group");
            var parentSelections = ".select_all";
            var groupSelections = ".select_item";
            if (group){
                parentSelections += "[group='" + group + "']";
                groupSelections += "[group='" + group + "']";
            }
            groupSelections += ":not(:checked)";
            var total = $(this).closest("table").find(groupSelections).length;
            if (total == 0){
                $(this).closest("table").find(parentSelections).prop("checked", true);
            } else {
                $(this).closest("table").find(parentSelections).prop("checked", false);
            }
        });

        $("body").undelegate(".column_all", "click");
        $("body").delegate(".column_all", "click", function () {
            var currentValue = $(this).prop("checked");
            var column = $(this).attr("column");
            var childrenSelections = ".column_item";
            if (column){
                childrenSelections += "[column='" + column + "']";
            }
            $(this).closest("table").find(childrenSelections).prop("checked", currentValue);
            var idxTable = $(this).closest('table').attr('id').replace('custom_datatable_', '');
            var customInfo = oTable[idxTable].customInfo;
            if (customInfo && customInfo.selectedColor) {
                var selectedColor = oTable[idxTable].customInfo.selectedColor;
                if (currentValue) {
                    $(this).closest("table").find("tbody tr").css({"background-color": selectedColor});
                } else {
                    $(this).closest("table").find("tbody tr").css({"background-color": ""});
                }
            }
            if($(this).hasClass("select_row_all")){
                $(this).closest('tr').find('input.column_all').prop("checked", currentValue);
                var selectRows = $(this).closest("table").find(".row_all");
                var total = selectRows.length;
                for(var i = 0; i < total; i++){
                    $(selectRows[i]).closest('tr').find('input.column_item').prop("checked", currentValue);
                }
            } else {
                var columnItems = $(this).closest("table").find(childrenSelections);
                for(var i = 0; i < columnItems.length; i++) {
                    var row = $(columnItems[i]).attr("row");
                    parentSelections = ".row_all";
                    groupSelections = ".row_item";
                    if (row) {
                        parentSelections += "[row='" + row + "']";
                        groupSelections += "[row='" + row + "']";
                    }
                    groupSelections += ":not(:checked)";
                    total = $(columnItems[i]).closest("table").find(groupSelections).length;
                    if (total == 0) {
                        $(columnItems[i]).closest("table").find(parentSelections).prop("checked", true);
                    } else {
                        $(columnItems[i]).closest("table").find(parentSelections).prop("checked", false);
                    }
                    var columnItem = $(columnItems[i]).closest("tr").find(parentSelections);
                    parentSelections = ".select_row_all";
                    groupSelections = ".row_all";
                    if (column) {
                        parentSelections += "[column='" + column + "']";
                        groupSelections += "[column='" + column + "']";
                    }
                    groupSelections += ":not(:checked)";
                    total = $(columnItem).closest("table").find(groupSelections).length;
                    if (total == 0) {
                        $(columnItem).closest("table").find(parentSelections).prop("checked", true);
                    } else {
                        $(columnItem).closest("table").find(parentSelections).prop("checked", false);
                    }
                }
                // all
                groupSelections = ".column_item:not(:checked)";
                total = $(this).closest("table").find(groupSelections).length;
                if (total == 0){
                    $(this).closest("table").find(".column_all.select_row_all").prop("checked", true);
                } else {
                    $(this).closest("table").find(".column_all.select_row_all").prop("checked", false);
                }
            }
        });

        $("body").undelegate(".column_item", "click");
        $("body").delegate(".column_item", "click", function () {
            // column
            var column = $(this).attr("column");
            var parentSelections = ".column_all";
            var groupSelections = ".column_item";
            if (column){
                parentSelections += "[column='" + column + "']";
                groupSelections += "[column='" + column + "']";
            }
            groupSelections += ":not(:checked)";
            var total = $(this).closest("table").find(groupSelections).length;
            if (total == 0){
                $(this).closest("table").find(parentSelections).prop("checked", true);
            } else {
                $(this).closest("table").find(parentSelections).prop("checked", false);
            }
            if(!$(this).hasClass("row_all")) {
                // row
                var row = $(this).attr("row");
                parentSelections = ".row_all";
                groupSelections = ".row_item";
                if (column) {
                    parentSelections += "[row='" + row + "']";
                    groupSelections += "[row='" + row + "']";
                }
                groupSelections += ":not(:checked)";
                total = $(this).closest("table").find(groupSelections).length;
                if (total == 0) {
                    $(this).closest("table").find(parentSelections).prop("checked", true);
                } else {
                    $(this).closest("table").find(parentSelections).prop("checked", false);
                }
            }
            // all
            total = $(this).closest("table").find(".column_item:not(:checked)").length;
            if (total == 0) {
                $(this).closest("table").find(".column_all.select_row_all").prop("checked", true);
            } else {
                $(this).closest("table").find(".column_all.select_row_all").prop("checked", false);
            }
            // Fill color
            var idxTable = $(this).closest('table').attr('id').replace('custom_datatable_', '');
            var customInfo = oTable[idxTable].customInfo;
            if (customInfo && customInfo.selectedColor) {
                var selectedColor = oTable[idxTable].customInfo.selectedColor;
                var trParent = $(this).closest("tr");
                if ($(this).prop("checked")) {
                    trParent.css({"background-color": selectedColor});
                } else {
                    trParent.css({"background-color": ""});
                }
            }
        });

        $("body").undelegate(".row_all", "click");
        $("body").delegate(".row_all", "click", function () {
            var state = $(this).prop("checked");
            var selectItems = $(this).closest('tr').find('input.row_item');
            for (var i=0; i < selectItems.length; i++) {
                var selectItem = selectItems[i];
                $(selectItem).prop("checked", state);
                var column = $(selectItem).attr("column");
                var parentSelections = ".column_all";
                var groupSelections = ".row_item";
                if (column) {
                    parentSelections += "[column='" + column + "']";
                    groupSelections += "[column='" + column + "']";
                }
                groupSelections += ":not(:checked)";
                var total = $(selectItem).closest("table").find(groupSelections).length;
                if (total == 0) {
                    $(selectItem).closest("table").find(parentSelections).prop("checked", true);
                } else {
                    $(selectItem).closest("table").find(parentSelections).prop("checked", false);
                }
                var idxTable = $(selectItem).closest('table').attr('id').replace('custom_datatable_', '');
                // fill color
                var customInfo = oTable[idxTable].customInfo;
                if (customInfo && customInfo.selectedColor) {
                    var selectedColor = oTable[idxTable].customInfo.selectedColor;
                    var trParent = $(selectItem).closest("tr");
                    if ($(this).prop("checked")) {
                        trParent.css({"background-color": selectedColor});
                    } else {
                        trParent.css({"background-color": ""});
                    }
                }
            }
            groupSelections = ".row_all:not(:checked)";
            total = $(this).closest("table").find(groupSelections).length;
            if (total == 0){
                $(this).closest("table").find(".column_all.select_row_all").prop("checked", true);
            } else {
                $(this).closest("table").find(".column_all.select_row_all").prop("checked", false);
            }
        });

        // $("body").undelegate("table tbody tr td", "click");
        // $("body").delegate("table tbody tr td", "click", function () {
        //     if ($(this).find("input.column_item").length == 0) {
        //         $(this).parent("tr").find("input.column_item").trigger("click");
        //     }
        // });

        /*
        $("body").undelegate("table tbody tr td", "click");
        $("body").delegate("table tbody tr td", "click", function () {
            if ($(this).find("input.select_item").length == 0) {
                $(this).parent("tr").find("input.select_item").trigger("click");
            }
        });
        */

        $("body").undelegate(".input-group .btnRemove", "click");
        $("body").delegate(".input-group .btnRemove", "click", function () {
            $(this).closest(".input-group").find("input").val("");
            var callback = $(this).attr("data-callback");
            // Callback
            var functionName = callback.split("(")[0];
            if (callback != undefined && callback != '' && eval("typeof " + functionName) != "undefined"){
                eval(callback);
            }
        });

        $("body").undelegate(".btnExport", "click");
        $("body").delegate(".btnExport", "click", function () {
            var url = $(this).attr("data-url");
            var allParams = $(this).attr("data-params").split(",");
            var params = {
                'sSearch': $("#custom_datatable_0_filter input").val(),
                'station_id': $('#cbbStations').val()
            };
            var total = allParams.length;
            for (var i = 0; i < total; i++){
                if (allParams[i].trim()!=""){
                    var item = $("[name='" + allParams[i] + "']").first();
                    if (item.length == 1) {
                        params[allParams[i].trim()] = item.val().trim();
                    }
                }
            }
            if (url.indexOf("?") == -1){
                url += "?";
            }
            url += $.param(params);
            window.open(url);
        });

        $('#go_top').click(function(){
            $('body, html').animate({scrollTop:0},400);
            return false;
        });

        $(window).scroll(function(){
            if( $(window).scrollTop() == 0 ) {
                $('#go_top').stop(false,true).fadeOut(600);
            }else{
                $('#go_top').stop(false,true).fadeIn(600);
            }
        });

        $("body").delegate("form", "submit", function () {
            thisInstance.showProgress();
        });

        $("body").delegate(".btnReset", "click", function () {
            var allInput = $(this).closest("form").find("input");
            var total = allInput.length;
            var tmp = null;
            for(var i = 0; i < total; i++){
                tmp = $(allInput[i]);
                if (tmp.attr("type") != "hidden" && tmp.attr("type") != "checkbox" && tmp.attr("type") != "radio" && tmp.hasClass("hide") == false && tmp.css("display") != "none"){
                    tmp.val("");
                }
            }
            allInput = $(this).closest("form").find("textarea");
            total = allInput.length;
            for(var i = 0; i < total; i++){
                tmp = $(allInput[i]);
                if (tmp.attr("type") != "hidden" && tmp.attr("type") != "checkbox" && tmp.attr("type") != "radio" && tmp.hasClass("hide") == false && tmp.css("display") != "none"){
                    tmp.val("");
                }
            }
        });

        // Luon luon trim khoang trang
        $('input:input, textarea:input').change(function() {
            $(this).val($(this).val().trim());
        });

        $("body").off("click", ".MyMultiCheck");
        $("body").on("click", ".MyMultiCheck", function () {
            var target = $(this).data("for");
            var elements = $("label[data-for='" + target + "'").find("input:checked");
            var total = elements.length;
            var newValue = '';
            for(var i=0; i<total; i++){
                if (newValue){
                    newValue += ",";
                }
                newValue += $(elements[i]).val();
            }
            $("#" + target).val(newValue);
        });
    },

    showMenu: function () {
        var currentUrl = $('#hfCurrentUrl').val();
        var menu = $('.sidebar-collapse ul#side-menu li a[href="' + currentUrl + '"]').first();
        if (menu.length == 0){
            currentUrl2 = currentUrl.substring(0, currentUrl.lastIndexOf('?'));
            if (currentUrl2) {
                menu = $('.sidebar-collapse ul#side-menu li a[href="' + currentUrl2 + '"]').first();
            }
            if (menu.length == 0) {
                currentUrl3 = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
                menu = $('.sidebar-collapse ul#side-menu li span[href="' + currentUrl3 + '"]').closest('li').find('a').first();
            }
        }
        var parrentGroup = menu.closest('ul.nav-second-level');
        if (parrentGroup.length > 0){
            parrentGroup.closest('li').addClass('active');
        }
        menu.closest('li').addClass('active');
    },

    showModal: function (options) {
        var defaults = {
            target: '',
            url: '',
            text: '',
            callback: null,
        };
        $.extend(defaults, options);
        if($(".ModalWrap").length > 0){
            $(".ModalWrap").remove();
        }
        $("body").append("<div class='ModalWrap'></div>");
        if (defaults.url){
            $(defaults.target).load(defaults.url, function () {
                if (typeof defaults.callback == 'function'){
                    defaults.callback();
                }
            });
        } else {
            $(defaults.target).html(defaults.text);
            if (typeof defaults.callback == 'function'){
                defaults.callback();
            }
        }
    },

    registerEvents: function () {
        this.showMessageWhenHasError();
        this.registerEventsForCommonInput();
        this.registerEventsForCommonButton();
        this.showMenu();
    },

    getCommonAvariables: function () {
        this.appName = $("#hfApplicationName").val();
        this.controllerName = $("#hfControllerName").val();
        this.viewName = $("#hfViewName").val();
        this.fullDateTime = $("#hfFullDateTime").val();
        this.shortDate = $("#hfShortDate").val();
    },

    formatTime: function(h, i, s) {
        var a = ':';
        var displayTime = this.formatNumberWithLeadingZeros(h, 2) +
            a + this.formatNumberWithLeadingZeros(i, 2) +
            a + this.formatNumberWithLeadingZeros(s, 2);
        return displayTime;
    },

    formatNumberWithLeadingZeros: function(num, size) {
        var s = num + "";
        while (s.length < size) s = "0" + s;
        return s;
    },

    focusToFirstError: function () {
        $('label.error').first().parent().find('input, select, textarea').first().focus();
    },

    initialize: function () {
        this.getCommonAvariables();
        this.registerEvents();
    }

});

var app = new CommonApp();
app.initialize();

// common validator
// See more: https://jqueryvalidation.org/documentation/
var validator = null;

