var app = angular.module( "MyApp", ['ui.bootstrap'] );

app.controller( "quizzesController", function userController($scope,$http,$modal,$log) {
  
  $scope.quiz_name = "";

  $scope.create_quiz_window = function(size) {
    var modalInstance = $modal.open({
      templateUrl: 'create_quiz.html',
      controller: 'CreateQuizController',
      size: size,
    });

    modalInstance.result.then(function (quiz_name) {
      $scope.quiz_name = quiz_name;
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };
})

app.controller('CreateQuizController', function ($scope, $modalInstance) {
  $scope.quiz_name = ""

  $scope.ok = function () {
    $modalInstance.close($scope.quiz_name);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});