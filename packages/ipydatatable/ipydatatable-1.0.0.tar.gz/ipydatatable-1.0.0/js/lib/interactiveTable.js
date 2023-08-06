// No idea how to know Lab vs Notebook
// but came up with this simple thing.
try{
  window.$.fn.modal
  var lab = false;
}
catch{
  var lab = true;
}
console.log("Are we in JupyterLabssss: "+lab);

var widgets = require('@jupyter-widgets/base');

window.$ = window.jQuery = require( 'jquery' );
var dt = require( 'datatables.net' ); 


window.pdfMake = require('pdfmake/build/pdfmake.min');
var vfs = require('pdfmake/build/vfs_fonts');
window.pdfMake.vfs = vfs.pdfMake.vfs;

require('datatables.net-dt');
require('datatables.net-select');
require('datatables.net-colreorder');
require('datatables.net-responsive');
require('datatables.net-datetime')
require('datatables.net-searchbuilder-dt' )
require('jszip' );
require('datatables.net-buttons-dt' );
require('datatables.net-buttons/js/buttons.colVis.js' );
require('datatables.net-buttons/js/buttons.html5.js' );
require('datatables.net-buttons/js/buttons.print.js' );

var screenfull = require('screenfull');
var _ = require('lodash');

// CSS Lab reuirements that would otherwise break Notebook.
if(lab){
  require('fontawesome');
  require('!style-loader!css-loader!bootstrap/dist/css/bootstrap.min.css');
  require( 'bootstrap' );
  
}

// Load datatables styles
require('!style-loader!css-loader!datatables.net-dt/css/jquery.dataTables.css');
require('!style-loader!css-loader!datatables.net-searchbuilder-dt/css/searchBuilder.dataTables.css');
require('!style-loader!css-loader!datatables.net-buttons-dt/css/buttons.dataTables.css');
require('!style-loader!css-loader!datatables.net-datetime/dist/dataTables.dateTime.min.css');

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var InteractiveTableModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'InteractiveTableModel',
        _view_name : 'InteractiveTableView',
        _model_module : 'ipydatatable',
        _view_module : 'ipydatatable',
        _model_module_version : '1.0.0',
        _view_module_version : '1.0.0',
        table : []
    })
});

// Custom View. Renders the widget model.
var InteractiveTableView = widgets.DOMWidgetView.extend({
    // Defines how the widget gets rendered into the DOM
    render: function() {
      var self = this;
      // Keeps the order of the columns for filtering.
      // This is important for when we move the columns.
      self.column_order = [];
      // Loading CSS for library.
      self.create_style_jinteractive();
      // Get table data from Python
      var table_data = self.model.get('table');
      // Selected data variable.
      self.selected_data = []

      // Creating a wrapper element
      self.wrapper = document.createElement('div');
      self.wrapper.id = "wrapper_"+self.cid;
      self.wrapper.style.display = "none";
      self.wrapper.style.width = '100%';
      self.wrapper.style.setProperty('color', 'black', 'important');
      self.wrapper.style.backgroundColor="white";

      // Creating table element
      self.tbl = document.createElement('table');
      self.tbl.style.width = '100%';
      self.tbl.style.setProperty('color', 'black', 'important');
      self.tbl.style.wordWrap = "break-word";
      self.tbl.id = "example_"+self.cid;
      self.tbl.className = "display";

      // All the columns of the data.
      self.cols = [];
      //  Basically means it will hace a child row.
      self.dropdown = false;
      // Columns in the data
      self.columns = [""];

      // Creating table
      // Adding body
      var tbdy = document.createElement('tbody');
      // Iterate through the table data.
      $.each(table_data,(i, value) => {
        self.dropdown = false;
        var tr = document.createElement('tr');
        // Go through each column of a row and add them to the element
        Object.keys(value).forEach(function(key) {
          var td = document.createElement('td');
          
          // Formatting the data
          if(typeof value[key] === 'string' || value[key] instanceof String){
            var temp_value = value[key];
          }
          else if (value[key] == null){
            var temp_value = "";
          }
          else{
            var temp_value = value[key].toString();
          }

          // Checking to see if data is overflowed on limit or is group.
          // Makes it so you will have a child row.
          if(key == "group"){
            self.dropdown = true;
          }else if(temp_value.length > self.model.get("text_limit")){
            self.dropdown = true;
            self.cols.push("over_length")
            td.appendChild(document.createTextNode(temp_value));
          }else{
            td.appendChild(document.createTextNode(temp_value));
          }

          // Storing the columns in the cols variable.
          if(!self.cols.includes(key) && key != "group"){
            self.cols.push(key)
          }
          if(key!="group"){
            tr.appendChild(td);
          }
        });
        // Adding the openning child column at beginning.
        if(self.dropdown){
          var td = document.createElement('td');
          td.appendChild(document.createTextNode("+"));
          td.className = "show_details";

          $(tr).prepend(td)
        }
        else{
          var td = document.createElement('td');
          $(tr).prepend(td)
        }

        tbdy.appendChild(tr);
      })
      // end Body

      // start heading
      var thead = document.createElement('thead');
      var tr = document.createElement('tr');
      var append_first = false;
      $.each(self.cols,(i, value) => {
        var td = document.createElement('th');
        if(value != "group" && value != "over_length"){
          self.columns.push(value)
          append_first = true;
          td.appendChild(document.createTextNode(value))
          tr.appendChild(td)
        }
        else{
          append_first = true;
          td.orderable = false;
        }
      });

      if(append_first){
        var td = document.createElement('td');
        $(tr).prepend(td)
      }
      thead.appendChild(tr);

      self.tbl.appendChild(thead);
      self.tbl.appendChild(tbdy);
      self.wrapper.appendChild(self.tbl);
      self.el.appendChild(this.wrapper)
      // Finished creating table

      // Initializing everything
      $(document).ready( function () {
        // Code for when fullScreen goes on.
        var calcDataTableHeight = function() {
          return $(window).height() - 200;
        };
        
        $(window).on('resize', function(){
          if(screen.width === window.innerWidth){
            //$('#example_'+self.cid).dataTable().fnSettings().oScroll.sY = calcDataTableHeight();
            //$('.dataTables_scrollBody:has(#example_'+self.cid+')').height(calcDataTableHeight());  
            $('#example_'+self.cid+'_wrapper .dataTables_scrollBody').css("height",calcDataTableHeight()+"px").css("max-height",calcDataTableHeight()+"px");
            console.log("1");
          }
          else{
            //$('#example_'+self.cid).dataTable().fnSettings().oScroll.sY = '400px';
            //$('.dataTables_scrollBody:has(#example_'+self.cid+')').height('400px');  
            console.log($('#example_'+self.cid+'_wrapper .dataTables_scrollBody'))
            $('#example_'+self.cid+'_wrapper .dataTables_scrollBody').css("height",400+"px").css("max-height",400+"px");
            console.log("2");
          }
        });

        // Add event listener for opening and closing details
        $('#example_'+self.cid+' tbody').on('click', 'td.show_details', function(){
          var column_index = table.columns().header().toArray().map(x => x.innerText)

          // Child on click
          function format ( d, index ) {
            // Get Child grouping select value
            let child_select = self.model.get("child_group_select");
            var tbl = document.createElement('table');
            tbl.style.paddingLeft = '50px';
            tbl.style.borderSpacing = '0';

            if(child_select){
              var btn_group = document.createElement('div');
              btn_group.classList.add('btn-group');
              btn_group.classList.add('btn-group-toggle');
              btn_group.setAttribute("data-toggle","buttons");
            }
            $.each(d, (i, value) => {
              if(value.length > self.model.get("text_limit")){
                // If not child select put column and row as format, else 
                // add buttons for selection.
                let tr = document.createElement('tr');
                let td_col = document.createElement('td');
                let td_value = document.createElement('td');
                
                td_col.appendChild(document.createTextNode(column_index[i]));
                td_value.appendChild(document.createTextNode(value));
                tr.appendChild(td_col);
                tr.appendChild(td_value);
                tbl.appendChild(tr);
              }
            })
            var t_row = self.model.get('table')[index];

            if(t_row.hasOwnProperty('group')){
              $.each(t_row["group"], (i, value) => {
                if(!child_select){
                  let tr = document.createElement('tr');
                  let td_col = document.createElement('td');
                  let td_value = document.createElement('td');
                  
                  td_col.appendChild(document.createTextNode(i));
                  td_value.appendChild(document.createTextNode(value));
                  tr.appendChild(td_col);
                  tr.appendChild(td_value);
                  tbl.appendChild(tr);
                }else{
                  let label = document.createElement('label');
                  label.style.marginRight = '10px'
                  label.classList.add('btn');
                  label.classList.add('btn-primary'); 
                  label.classList.add('group-buttons'); 

                  let input = document.createElement('input');
                  input.setAttribute("type","checkbox");
                  input.setAttribute("name","options");
                  input.setAttribute("autocomplete","off")
                  input.setAttribute("id",'group_'+self.cid+"_"+index);

                  let selected_group = [...self.model.get("selected_group")];
                  $.each(selected_group,function(i_group, item_group){
                    if(item_group == index+":"+i+":"+value){
                      label.classList.add('active'); 
                    }
                  });
                  
                  label.appendChild(input);
                  label.appendChild(document.createTextNode(value));
                  label.onclick = function(){
                    let selected_group = [...self.model.get("selected_group")];
                    
                    if(selected_group.indexOf(index+":"+i+":"+value)<0){
                      selected_group.push(index+":"+i+":"+value);
                      self.model.set('selected_group', selected_group);
                      self.touch();
                    }
                    else{
                      selected_group.splice(selected_group.indexOf(index+":"+i+":"+value),1);
                      self.model.set('selected_group', selected_group);
                      self.touch();
                    }
                  }
                  btn_group.appendChild(label);
                }
              })
            }

            if(child_select){
              let div = document.createElement('div');
              div.appendChild(tbl);
              div.appendChild(btn_group)
              return div;
            }
            return tbl;
          }

          // changing the clicky thing
          if(table.cell( this ).data() == "-"){
            table.cell( this ).data("+")
          }
          else{
            table.cell( this ).data("-")
          }

          // Getting the proper row.
          var tr = $(this).closest('tr');
          var row = table.row( tr );

          if(row.child.isShown()){
              // This row is already open - close it
              row.child.hide();
              tr.removeClass('shown');
          } else {
              // Open this row
              row.child(format(row.data(), row.index())).show();
              tr.addClass('shown');
          }
          if(!lab){
            $('.group-buttons').click(function () {
              $(this).toggleClass("active"); 
            })
          }
        });
        // End of open row.

        self.selected = [...self.model.get("selected_index_row")];
        // Selecting a row action
        $('#example_'+self.cid+' tbody').on( 'click', 'tr', function () {
            var temp = []
            if(self.selected.includes(table.row( this ).index() )){
              self.selected.splice(self.selected.indexOf(table.row( this ).index() ),1)
            }else{
              self.selected.push(table.row( this ).index() );
            }
            $.each(self.selected,(i, value)=>{
              temp.push(table_data[value])
            })
            self.model.set('selected_data', temp);
            self.model.set('selected_index_row', [...self.selected]);
            self.touch();
        } );
        // End selected data

        // Adding column filtering spaces to table
        if(self.model.get("column_filter")){
          // First column in the child opening
          self.column_order.push(0);
          $('#example_'+self.cid+' thead tr').clone(true).appendTo( '#example_'+self.cid+' thead' );
          $('#example_'+self.cid+' thead tr:eq(1) th').each( function (i) {
            var title = $(this).text();
            self.column_order.push(i+1);
            $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
            // Adding the search mechanism
            $( 'input', this ).on( 'keyup change clear', function () {
                if ( table.column(self.column_order.indexOf(i+1)).search() !== this.value ) {
                    table
                        .column(self.column_order.indexOf(i+1))
                        .search( this.value )
                        .draw();
                }
            } );
          } );
        }

        // Column index for sorting.
        var sort_col = self.columns.indexOf(self.model.get("sort_column")) > -1 ? self.columns.indexOf(self.model.get("sort_column")) : 1;
        // Initialize hiding columns
        var hide_cols = []
        $.each(self.columns, (i, item) => {
          if(item != ""){
            if(self.model.get("init_state") == "hide"){
              if(self.model.get("columns").includes(item) ){
                hide_cols.push(i)
              }
            }
            else{
              if(!self.model.get("columns").includes(item)){
                hide_cols.push(i)
              }
            }
          }
        });

        // Creating table object
        var table = $('#example_'+self.cid).DataTable({
          dom: 'Blfrtip',
          buttons: [
            {
              text: 'Full Screen',
              action: function ( e, dt, node, config ) {
                if (screenfull.isEnabled) {
                  screenfull.request($('#wrapper_'+self.cid)[0]);
                }
              }
            },
            {
              extend: 'selectAll',
              action: function ( e, dt, node, config ) {
                var temp = []
                self.selected = [];
                dt.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
                  var data = this.data();
                  self.selected.push( rowIdx );
                  temp.push(data);
                } );
                self.model.set('selected_data', temp);
                self.model.set('selected_index_row', [...self.selected]);
                self.touch();
                window.$.fn.dataTable.ext.buttons.selectAll.action.call(this, e, dt, node, config);
              }
            },
            {
              extend: 'selectNone',
              action: function ( e, dt, node, config ) {
                window.$.fn.dataTable.ext.buttons.selectNone.action.call(this, e, dt, node, config);
                let temp = []
                self.selected = [];
                self.model.set('selected_data', temp);
                self.model.set('selected_index_row', []);
                self.touch();
              }
            },
            {
              extend: 'colvis', 
              columns: ':not(.notToggleVis)',
            }, 
            'searchBuilder','copy', 'csv', 'excel', 'pdf', 'print'
          ],
          orderCellsTop: true,
          //"autoWidth": false,
          order: [[ sort_col , "desc" ]],
          "lengthMenu": [[10, 25, 50, 100, 500, -1], [10, 25, 50, 100, 500, "All"]],
          fixedHeader: true,
          scrollY: 400,
          scrollResize: true,
          "scrollCollapse": true,
          scrollX: true,
          select:{
            style: 'multi'
          },
          colReorder: true,
          //responsive:true,
          columnDefs: [ 
            { width: 10, targets: 0, orderable: false, className:"notToggleVis" },
            { targets: hide_cols, visible: false },
            {
                targets:"_all",
                render: function ( data, type, row ) {
                  return data.length > self.model.get("text_limit") ?
                    data.substr( 0, self.model.get("text_limit") ) +'…' :
                    data;
                }
            } 
          ]
        });
        $('#example_'+self.cid+' td').css('white-space','initial');
        $('#example_'+self.cid+' td').css('word-break','break-word');

        // Initalizing the selection of the data on the table.
        let selected_data = []
        $.each(self.model.get("selected_index_row"),(index, val) => {
          selected_data.push(self.model.get("table")[val])
          
          table.row( val ).select()
        })
        self.model.set('selected_data', selected_data);
        self.touch();
        // Ending selection data
        
        table.on( 'column-reorder', function ( e, settings, details ) {
          var curr = details.mapping;

          var temp = []
          $.each(settings['aoColumns'],(index, val) => {
            temp.push(val['_ColReorder_iOrigCol']);
          });

          self.column_order = temp;
        } );

        self.wrapper.style.display = "block";
        // Only for JupyterLab to make table not be gigantic.
        if(lab){
          self.wrapper.style.width = (document.getElementById("wrapper_"+self.cid).parentNode.parentNode.parentNode.parentElement.clientWidth-100)+"px";
          self.wrapper.style.setProperty('color', 'black', 'important');
        }        
        table.columns.adjust();
      } );
    },

    create_style_jinteractive: function(){
      if(lab){
        var fa = 'Font Awesome\ 5 Free'
      }else{
        var fa = "fontawesome"
      }
      var style = `
      div.dataTables_scrollHead table.dataTable thead th.sorting_asc::after,
      div.dataTables_scrollHead table.dataTable thead th.sorting_desc::after {
        content:"" !important;
      }
      div.dataTables_scrollHead table.dataTable thead .sorting:after {
        content: "\\f0dc";
        float: left;
        font-family: '${fa}';
        padding-right:5px;
      }
      div.dataTables_scrollHead table.dataTable thead th.sorting_asc:after {
        font-family: '${fa}';
        float: left;
        content: "\\f0de" !important;
        padding-right:5px;
      }
      div.dataTables_scrollHead table.dataTable thead th.sorting_desc:after {
        font-family: '${fa}';
        float: left;
        content: "\\f0dd" !important;
        padding-right:5px;
      }
      div.dt-button-collection {
        max-height: 200px !important;
        overflow-y: auto !important;
      }
      `;
      this.style_context = document.createElement('style');
      this.style_context.innerHTML = style;
      this.el.appendChild(this.style_context);
    }
});

module.exports = {
    InteractiveTableModel: InteractiveTableModel,
    InteractiveTableView: InteractiveTableView
};