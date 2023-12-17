$(document).ready(function() {
    loadDataTableForPage();

    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});
// <th>{{=T('#')}}</th>
//                         <th>{{=T('Adjustment_title')}}</th>
//                         <th>{{=T('Station')}}</th>
//                         <th>{{=T('Create by')}}</th>
//                         <th>{{=T('From date')}}</th>
//                         <th>{{=T('To date')}}</th>
//                         <th>{{=T('Hour start')}}</th>
//                         <th>{{=T('Repeat')}}</th>
//                         <th>{{=T('Repeat time')}}</th>
//                         <th>{{=T('Adjustment type')}}</th>
//                         <th>{{=T('Status')}}</th>
function loadDataTableForPage() {
    var aoColumns = [
        {'sWidth' : '3%', 'bSortable' : false},
        {'sWidth' : '8%'},
        {'sWidth' : '14%'},
        {'sWidth' : '7%'},
        {'sWidth' : '9%'},
        {'sWidth' : '9%'},
        {'sWidth' : '8%'},
        {'sWidth' : '7%'},
        {'sWidth' : '14%'},
        {'sWidth' : '9%'},
        {'sWidth' : '9%'},
        // {'sWidth' : '7%'},
        // {'sWidth' : '15%'},   // For check box column
        {'sWidth' : '3%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', 'text-left','' , '', '', '', ''];
    loadDataTable({
        aoColumns: aoColumns,
        aoClass: aoClass,
    });

    return true;
}