var app = angular.module( "index", ['ui.bootstrap'] );

app.controller( "indexController", function userController($scope,$http,$location) {
  var responsePromise = $http.get("/is_logged_api");
  responsePromise.success(function(data, status, headers, config) {
    if(!data.logged) {
      $location.path("/login");
      return;
    };

    $location.path("/home/");
  });
})