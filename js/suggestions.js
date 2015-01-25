var app = angular.module( "suggestions", ['ui.bootstrap'] );

app.controller( "suggestionsController", function userController($scope,$http) {
  $scope.suggestionText = "";
  $scope.submit = function() {
    var req = $http.post("/api/suggestion/",{"suggestion": $scope.suggestionText});
  };
})