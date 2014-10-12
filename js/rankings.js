var app = angular.module( "rankings", ['ui.bootstrap','ngTable'] );

app.controller( "rankingsController", function ($scope,$http,$filter,ngTableParams) {

  $scope.columns = [
    {title: "Player", field: "player", visible: true},
  ];
  $scope.table_data = [];

  var responsePromise = $http.get("/rankings_api/");
  responsePromise.success(function(data, status, headers, config) {
    console.log(data);
    // get the quiz dates which correspond to the columns
    for(var i in data.quiz_dates) {
      id = data.quiz_dates[i].quiz_id;
      title = new Date(data.quiz_dates[i].releaseDate).toDateString(); 
      $scope.columns.push({title: title, field: id, visible: true});
    };

    // get the data for each user
    for(var user in data.rank_by_user) {
      elem = {"player": user};
      for(var i in $scope.columns) {
        col = $scope.columns[i];
        if(col.field=="player") continue;
        elem[col.field] = data.rank_by_user[user][col.field];
      };
      $scope.table_data.push(elem);
    };

    // add the totals
    $scope.columns.push({title: "Total", field: "total", visible: true});
    for(var i in $scope.table_data) {
      total = 0;
      for(var col in $scope.table_data[i]) {
        if(col=="player") continue;
        if($scope.table_data[i][col]) total += $scope.table_data[i][col];
      };
      $scope.table_data[i].total = total;
    }

    // set up the table parameters
    $scope.tableParams = new ngTableParams({
      page: 1,                                  // show first page
      count: $scope.table_data.length,          // count per page
      filter: {
        name: 'player'                          // initial filter
      }
    }, {
      counts: [], // hide page counts control
      total: 0,  // value less than count hide pagination
      getData: function($defer, params) {
        // use build-in angular filter
        var orderedData = params.sorting() ?
          $filter('orderBy')($scope.table_data, params.orderBy()) :
          $scope.table_data;

        $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
      }
    });
  });
});