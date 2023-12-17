/**
 * Created by Admin on 5/13/2017.
 */
var loadDataTable;
var oTable = new Array();
var oTable_aoColumns = new Array();
var oTable_aoColumns_added = new Array();
var oTable_aoColumns_option = new Array();
var addedColumns = new Array();
var reloadDT = new Array();

var isDbClick = new Array();
loadDataTable = function (variable_options) {
	var options = {};
	if (variable_options) options = variable_options;
	if(options.iTable == undefined || options.iTable == null || options.iTable == ''){
		options.iTable = 0;
	}
	var tbl_id = '#custom_datatable_' + options.iTable;
	addedColumns[options.iTable] = $('select.added_columns[data-forTable=' + options.iTable + ']').val();
	if (reloadDT[options.iTable] == undefined){
		reloadDT[options.iTable] = true;
	}
	if (!oTable_aoColumns_added[options.iTable]){
		oTable_aoColumns_added[options.iTable] = [];
	}
	if (!oTable_aoColumns_option[options.iTable]){
		oTable_aoColumns_option[options.iTable] = variable_options;
	}
	var sAjaxSource = $("#custom_datatable_" + options.iTable).attr("data-url");
	var defaults = {
		//Số lượng bản ghi trên 1 trang.
		"iDisplayLength": 10,
		"aLengthMenu": [10, 20, 50, 100],
		"bServerSide": true,
		"bDestroy": true,
		"bAutoWidth": false,
		"stateSave": true,
		"bSort": false,//Cho phép sắp xếp
		"bFilter": true,//Sử dụng bộ lọc dữ liệu(Ẩn/hiện thuộc tính tìm kiếm)
		"sDom": "<'row middle't><'clear'><'row bottom' <'col-sm-6 text-left' li><'col-sm-6 text-right' p>><'clear'>",//Định nghĩa css cho các phần của bảng
		"bDeferRender": true,//Cho phép định nghĩa lại từng dòng khi render dữ liệu
		"sPaginationType": "full_numbers",//Kiểu phân trang - Mặc định là phân trang dạng navigation
		//URL dùng để lấy dữ liệu từ server. Có kiểu trả về là json
		"aoClass": [],
		"sAjaxSource": sAjaxSource,
		"sAjaxDataProp": "aaData",//Dữ liệu trả về từ server. Có định dạng là list<list<string>>
		doNotShowProgress:false,
		"fnServerData": function (sSource, aoData, fnCallback) {
			if (!options.doNotShowProgress) {
				app.showProgress();
			}
			if (typeof(options.fnCustomServerData) == "function"){
				options.fnCustomServerData(sSource, aoData, fnCallback);
			}
			var fields = $('[data-forDT="' + options.iTable + '"]');
			var total = fields.length;
			for(var i = 0; i < total; i++){
				var fieldName = $(fields[i]).attr('name');
				if (fieldName != 'added_columns' && fieldName != undefined) {
					if ($(fields[i]).attr('type') == 'checkbox'){
						if ($(fields[i]).prop('checked')){
							$(fields[i]).attr('value', 1);
						} else {
							$(fields[i]).attr('value', '');
						}
					}
                    var fieldId = $(fields[i]).attr('id');
                    aoData.push({
                        "name": fieldName, "value": $('#' + fieldId).val()
                    });
                }
			}
			var params = app.convertUrlToDataParams(location.href);
			var added_columns_element = $('select.added_columns[data-forDT=' + options.iTable + ']');
			var added_columns = added_columns_element.val();
			if (added_columns == undefined){
				added_columns = $('select.added_columns').not('[data-forDT]').val();
			}
			if (added_columns == undefined){
				added_columns = '';
			}
			if (reloadDT[options.iTable]){
				oTable_aoColumns_added[options.iTable] = [];
				$(tbl_id + ' thead th.added_columns').remove();
				$(tbl_id + ' thead th.quick_view').remove();
				$(tbl_id + ' tbody').html('');
				var chk_added_column = $(tbl_id).attr('data-chk_added_column');
				var total = added_columns.length;
				var idx_column = 0;
				for(var i = 0; i < total; i++){
					if (added_columns[i]){
						var columnName = added_columns_element.find('option[value="' + added_columns[i] + '"]').html();
						var html = '<th class="added_columns" style = "position:sticky; top: 0; z-index:999">';
						html += columnName;
						if (checkEnabled(chk_added_column)){
							idx_column += 1
							html += '<br /><input type="checkbox" column="' + idx_column + '" class="column_all" value="' + columnName + '" />';
						}
						html += '</th>';
						$(tbl_id + ' thead tr').append(html);
						oTable_aoColumns_added[options.iTable].push({'sWidth' : '5%'});
					}
				}
				$('#real_time tr').append('<th class="quick_view" colspan="3" style="width: 8%">Quick view</th>');
				reloadDT[options.iTable] = false;
				// oTable[options.iTable].fnDestroy();
				$(tbl_id).DataTable().clear().destroy();
				loadDataTable(oTable_aoColumns_option[options.iTable]);
				app.hideProgress();
				return false;
			}
			aoData.push({
				"name": "added_columns", "value": added_columns
			});
			if (typeof(options.fnCustomAoData) == "function"){
				options.fnCustomAoData(aoData);
			};
			if (params.search){
				aoData.push({
					"name": "search", "value": params.search
				});
			}
			$.ajax({
				"dataType": 'json',
				"type": "POST",
				"url": sSource,
				"data": aoData,
				"success": function(data) {
					app.hideProgress();
					if(data.success) {
						if (typeof(options.fnCustomCallback) == "function"){
							options.fnCustomCallback(data);
						}
						fnCallback(data);
					} else {
						app.showError(data.message);
					}
				},
				"error": function(ex) {
					app.hideProgress();
					app.showError(ex.status + ': ' + ex.statusText);
				}
			});
		},
		"fnRowCallback": function (nRow, aData, iDisplayIndex, iDisplayIndexFull) {
			$(nRow).attr('data-id', aData[aData.length-1]);
			//Tùy chỉnh các thẻ tr thi datatables đưa ra dữ liệu
			var totalColums = options.aoColumns.length;
			for (var i = 0; i < totalColums; i++) {
				$($(nRow).children()[i]).addClass(options.aoClass[i]);
			}
			if (typeof(options.fnCustomRowCallback) == "function"){
				options.fnCustomRowCallback(nRow, aData, iDisplayIndex, iDisplayIndexFull);
			}
			return nRow;
		},
		//Tùy chọn các cột
		"aoColumns": [],
		"oLanguage": {
			"sZeroRecords": app.translate("JS_DT_NO_RECORD"),
			"sInfoEmpty": "",
			"sInfo": app.translate("JS_DT_DISPLAY") + " _START_ - _END_ (" + app.translate("JS_DT_IN") +" _TOTAL_)",
			"sInfoFiltered": "(Filter _MAX_ from results)",
			"sInfoPostFix": "",
			"sSearch": app.translate("JS_DT_SEARCH"),
			"sLengthMenu": "_MENU_",
			"sUrl": "",
			"oPaginate": {
				"sFirst": app.translate("JS_DT_FIRST"),
				"sPrevious": app.translate("JS_DT_PREVIOUS"),
				"sNext": app.translate("JS_DT_NEXT"),
				"sLast": app.translate("JS_DT_LAST")
			}
		},
		"fnDrawCallback": function() {
			if (oTable[options.iTable].find('tbody').find("td.dataTables_empty").length){
				oTable[options.iTable].closest('.wrapper').find("#btnDelete").attr("disabled", "disabled");
			} else {
				oTable[options.iTable].closest('.wrapper').find("#btnDelete").removeAttr("disabled");
			}
			$(tbl_id).find('input.select_all').prop('checked', false);
			if (typeof(options.fnCustomDrawCallback) == "function"){
				options.fnCustomDrawCallback();
			}
		}
	};
	//Gán giá trị vào options
	options =  $.extend(defaults, options);
	if (!oTable_aoColumns[options.iTable]){
		oTable_aoColumns[options.iTable] = options.aoColumns.slice(0);
	}
	if (oTable_aoColumns_added[options.iTable]){
		if (oTable_aoColumns_added[options.iTable].length > 0){
			var options_aoColumns = oTable_aoColumns[options.iTable].slice(0);
			for (var i2 = 0; i2 < oTable_aoColumns_added[options.iTable].length; i2++){
				options_aoColumns.push(oTable_aoColumns_added[options.iTable][i2]);
			}
			options.aoColumns = options_aoColumns;
		}
	}
	oTable[options.iTable] = $(tbl_id).dataTable(options);
	if (typeof options.fnDeferInjectDataToTable == "function"){
		options.fnDeferInjectDataToTable();
	}
}

$(document).ready(function (e) {
	$('body').on('change', '.added_columns', function (e) {
		var idx = $(this).data('forDT');
		if (idx == undefined){
			idx = 0;
		}
		reloadDT[idx] = true;
    });

	$('body').on('click', '.btnSearch', function (e) {
		var idx = $(this).data('forDT');
		if (idx == undefined){
			idx = 0;
		}
		oTable[idx].fnFilter();
    });

	registerEventForCustomDatatables();
});



function registerEventForCustomDatatables() {
	var custom_datatables = $('.custom_datatable');
	var total = custom_datatables.length;
	for (var i=0; i<total; i++){
		var custom_datatable = $(custom_datatables[i]);
    	var sAjaxSource = custom_datatable.attr("data-url");
    	var aoColumns = eval(custom_datatable.attr("data-aoColumns"));
    	var aoClass = eval(custom_datatable.attr("data-aoClass"));
    	var iTable = custom_datatable.attr('data-iTable');
    	var sDom = custom_datatable.attr('data-sDom');
    	var fnCustomDrawCallback = custom_datatable.attr('data-fnCustomDrawCallback');
    	var fnCustomServerData = custom_datatable.attr('data-fnCustomServerData');
		loadDataTable({
			sAjaxSource: sAjaxSource,
			aoColumns: aoColumns,
			aoClass: aoClass,
			iTable: iTable,
			sDom: sDom,
			fnCustomDrawCallback: function () {
				if (fnCustomDrawCallback) {
					eval(fnCustomDrawCallback);
				}
			},
			fnCustomServerData: function (sSource, aoData, fnCallback) {
				if (fnCustomServerData) {
                    eval(fnCustomServerData);
                }
            }
		});
	}
}