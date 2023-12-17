$(document).ready(function() {
    loadDataTableForPage();
    
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });



});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%', 'bSortable' : false},
        {'sWidth' : '10%'},
        {'sWidth' : '8%'},
        {'sWidth' : '6%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '10%'},
        {'sWidth' : '6%'},
        {'sWidth' : '6%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},
        {'sWidth' : '3%'},
        {'sWidth' : '3%'},
        {'sWidth' : '3%'},
    ];

    var aoClass = ['', 'text-left td-station-name', '', '', 'text-left', 'text-left','', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "type", "value": $('#type').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#province_id').val()
            });
            aoData.push({
                "name": "status", "value": $('#status').val()
            });
            aoData.push({
                "name": "using_status", "value": $('#using_status').val()
            });
            aoData.push({
                "name": "ftp_connection_status", "value": $('#ftp_connection_status').val()
            });
        },
        
    });
    
    return true;
}

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("custom_datatable_0");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc";
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function sortStation(n){
        var x = document.getElementById("sorts")
        if (x.getAttribute('sort') === 'True'){
            document.getElementById("sorts").setAttribute('sort', 'False');
            var sort_type = 0
        }
        else {
            document.getElementById("sorts").setAttribute('sort', 'True');
            var sort_type = 1
        }

        var sAjaxSource = $("#custom_datatable_0").attr("data-url")+"_sort";
        var aoColumns = [
        {'sWidth' : '3%', 'bSortable' : false},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '8%'},
        {'sWidth' : '6%'},
        {'sWidth' : '3%'},   // For check box column
    ];

    var aoClass = ['', 'text-left td-station-name', '', '', 'text-left', 'text-left','', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "type", "value": $('#type').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#province_id').val()
            });
            aoData.push({
                "name": "status", "value": $('#status').val()
            });
            aoData.push({
                "name": "ftp_connection_status", "value": $('#ftp_connection_status').val()
            });
            aoData.push({
                "name": "sort_type", "value": sort_type
            });
        },

    });

    return true;
}


function ftp_click(ftp_url) {
    var witdth = screen.width /2;
    var heigh = screen.height /2;
    var top = screen.height/4;
    var left = screen.width/4;
    var param = 'width='+ witdth +',height=' + heigh +', top=' + top +', left=' +left;

    window.open(ftp_url,'popup',param)
}