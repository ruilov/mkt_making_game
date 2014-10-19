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

  // for(var i in $scope.quiz_data.questions) 
    // $scope.quiz_data.questions[i].table_data = [];
  
  $scope.qnum = qs.q+"";
  $scope.question = $scope.quiz_data.questions[parseInt(qs.q)-1];
  $scope.question.answer = format_num($scope.question.answer,$filter);
  $scope.qlinks = [];
  for(var i in $scope.quiz_data.questions) {
    q = (parseInt(i)+1);
    cla = "btn btn-default"
    if(q+""==$scope.qnum) cla = "btn btn-primary";
    $scope.qlinks.push({link: "/#/ranking_detailed?id="+qs.id+"&q="+q, title: q+"", clas: cla});
  }
  
  var req = $http.get("/rankings_api/?id="+qs.id+"&q="+qs.q);
  req.success(function(data, status, headers, config) {
    $scope.reply = data;
    $scope.table_data = [];
    for(var user in data) {   
      user_data = data[user];
      user_data["player"] = user;
      user_data["high"] = format_num(user_data["high"],$filter);
      user_data["low"] = format_num(user_data["low"],$filter);
      $scope.table_data.push(user_data);
    };

    $scope.tableParams = new ngTableParams({
      page: 1,                                                  // show first page
      count: $scope.table_data.length,   // count per page
      sorting: {
        score: 'desc'                                           // initial filter
      }
    }, {
      counts: [], // hide page counts control
      total: 10,  // value less than count hide pagination
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
  });
});