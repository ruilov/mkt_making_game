var app = angular.module( "quiz", ['ui.bootstrap'] );

app.controller( "quizController", function userController($scope,$http,$location,$route) {
  var qs = $location.search();
  var quiz_id = qs.id;

  $scope.quiz = {"questions": [], "url": quiz_url(quiz_id)};

  quiz_api_cb = function(quiz, status, headers, config) {
    $scope.quiz["questions"] = [];
    for(var i in quiz.questions) {
      question = quiz.questions[i];
      $scope.add_question(question);
      $scope.has_fillout = quiz.has_fillout
    };
  };

  var req = $http.get("/quiz_api/?id="+quiz_id);
  req.success(quiz_api_cb);

  $scope.add_question = function(question) {
    if(!question.guess_low) question.guess_low = 0;
    if(!question.guess_high) question.guess_high = 0;
    $scope.quiz.questions.push(question);
  };

  $scope.submit = function() {
    var req = $http.post("/quiz_api/?id="+quiz_id,$scope.quiz);
    req.success(quiz_api_cb);
  };
})