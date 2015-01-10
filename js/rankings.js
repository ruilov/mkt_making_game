var app = angular.module( "rankings", ['ui.bootstrap','ngTable'] );

app.controller( "rankingsController", function ($scope,$http,$filter,ngTableParams) {

  $scope.columns = [
    {title: "Player", field: "player", visible: true},
  ];
  $scope.table_data = [];

  var responsePromise = $http.get("/api/rankings/");
  responsePromise.success(function(data, status, headers, config) {
    // get the quiz dates which correspond to the columns
    for(var i in data.quiz_dates) {
      id = data.quiz_dates[i].quiz_id;
      title = new Date(data.quiz_dates[i].releaseDate).toLocaleDateString("en-US"); 
      $scope.columns.push({title: title, link: true, field: id, visible: true});
    };

    // get the data for each user
    for(var user in data.rank_by_user) {
      elem = {"player": user, "highlight_class": ""};
      if(data.rank_by_user[user].current) elem.highlight_class = "highlighted-row";

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
        if(col=="player" || col=="highlight_class") continue;
        if($scope.table_data[i][col]) total += $scope.table_data[i][col];
      };
      $scope.table_data[i].total = total;
    }

    // set up the table parameters
    $scope.tableParams = new ngTableParams({
      page: 1,                                  // show first page
      count: $scope.table_data.length,          // count per page
      sorting: {
        total: 'desc'                          // initial filter
      }
    }, {
      counts: [], // hide page counts control
      total: 0,  // value less than count hide pagination
      getData: function($defer, params) {
        // use build-in angular filter
        var orderedData = $scope.table_data;
        if(params.sorting()) {
          // couldn't figure out the api to extract stuff from the sortCol so just converting to string
          sortCol = params.orderBy()+"";
          asc = true;
          if(sortCol.charAt(0)=="-") {
            asc = false;
            sortCol = sortCol.substr(1);
          };
          if(sortCol.charAt(0)=="+") {
            asc = true;
            sortCol = sortCol.substr(1);
          };

          orderedData.sort(function(v1,v2) {
            // sort assuming it's ascending then multiply at the end if desc
            a = v1[sortCol];
            b = v2[sortCol];
            var res = 0;
            if(typeof(a)==typeof(b)) res = a < b ? -1 : a > b;
            else if(a==undefined) res = -1;
            else res = 1;
            if(!asc) res *= -1;
            return res;
          });
        };

        $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
      }
    });
  });
});