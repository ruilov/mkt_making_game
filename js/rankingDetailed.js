var app = angular.module( "rankingDetailed", ['ui.bootstrap','ngTable'] );

app.controller( "rankingDetailedController", function ($scope,$http,$filter,$location,ngTableParams) {
  var qs = $location.search();

  // by the time this controller is instantiate we already have $scope.quiz_data courtesy of the routes in template.js
  $scope.columns = [
    {title: "Player", field: "player", visible: true},
    {title: "Bid", field: "low", visible: true},
    {title: "Offer", field: "high", visible: true},
    {title: "Score", field: "score", visible: true},
  ];

  $scope.changeQ = function(qn) {
    $scope.qnum = qn;
    $scope.question = $scope.quiz_data.questions[$scope.qnum-1];
    $scope.question.answerStr = format_num($scope.question.answer,$filter);    

    $scope.qlinks = [];
    for(var i in $scope.quiz_data.questions) {
      q = (parseInt(i)+1);
      cla = "btn btn-default"
      if(q==$scope.qnum) cla = "btn btn-primary";
      $scope.qlinks.push({qnum: q, clas: cla});
    };

    // it's a mystery to me why this is needed. Otherwise the data table doesn't updste. Weird.
    // tried tablePArams.reloadData(), $scope.apply(), no cigar...
    if($scope.tableParams)
      $scope.tableParams.sorting("score", 'asc');

    $scope.tableParams = new ngTableParams({
      page: 1,                                                  // show first page
      count: $scope.user_data[$scope.qnum-1].length,   // count per page
      sorting: {
        score: 'desc'                                           // initial filter
      }
    }, {
      counts: [], // hide page counts control
      total: 0,  // value less than count hide pagination
      getData: function($defer, params) {
        // use build-in angular filter
        var orderedData = $scope.user_data[$scope.qnum-1];
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
            if(sortCol=="low" || sortCol=="high") {
              if(a!=undefined && a.length!=0) a = parseFloat(a.replace(/,/g,""));
              if(b!=undefined && a.length!=0) b = parseFloat(b.replace(/,/g,""));
            };
            var res = 0;
            if(typeof(a)==typeof(b)) res = a < b ? -1 : a > b;
            else {
              if(a==undefined) res = -1;
              else res = 1;
            };
            if(!asc) res *= -1;
            return res;
          });
        };

        $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
      }
    });
  };

  $scope.qnum = 1;
  var req = $http.get("/api/rankings/?id="+qs.id);
  req.success(function(data, status, headers, config) {
    $scope.user_data = [];
    for(var i in $scope.quiz_data.questions)
      $scope.user_data.push([]);

    for(var user in data) {
      for(var qi in data[user]) {
        user_data = data[user][qi];
        user_data["player"] = user;
        
        user_data["highlight_class"] = "";
        if(user_data.current) user_data["highlight_class"] = "highlighted-row";

        user_data["high"] = format_num(user_data["high"],$filter);
        user_data["low"] = format_num(user_data["low"],$filter);
        $scope.user_data[qi].push(user_data);
      };
    };
    $scope.changeQ(1);
  });
});