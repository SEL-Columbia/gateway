  var sortdir, sortcol;

  function comparer(a, b) { 
    var x = a[sortcol], y = b[sortcol];
/*--
x     y     result
10    1     1
1     10    -1
1     1     0
''    0     -1
0     ''    1
  --*/
    if(x===null) {return -1}
    if(y===null) {return 1}
    return (x === y ? 0 : (x > y ? 1 : -1));
  }; 


  var globalGridOptions = {
    forceFitColumns: false,
    autoHeight: true,
    enableCellNavigation: true,
    enableColumnReorder: true
  };
