var app = angular.module( "MyApp", ['ui.bootstrap'] );

app.controller( "quizzesController", function userController($scope,$http,$modal,$log) {

  // list of existing quizzes
  getQuizzes($scope,$http,$log);

  // modal window for creation of a new quiz
  $scope.create_quiz_window = function(size) {
    var modalInstance = $modal.open({
      templateUrl: 'create_quiz.html',
      controller: 'CreateQuizController',
      size: size,
    });

    modalInstance.result.then(function (quiz_name) {
      var newQuizz = {"name": quiz_name, "time": "123" };
      $scope.quizzes.push(newQuizz)
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };

  $scope.delete_selected = function() {
    $scope.quizzes = $scope.quizzes.filter(function (elem) { return !elem.selected } );
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


getQuizzes = function(scope,http,log){
  var responsePromise = http.get("/quizzes/");

  responsePromise.success(function(data, status, headers, config) {
    scope.quizzes = data.quizzes;
    for(var i in scope.quizzes) scope.quizzes[i].selected = false;
  });

  responsePromise.error(function(data, status, headers, config) {
      log.info("Ajax call to get quizzes failed");
  });
}