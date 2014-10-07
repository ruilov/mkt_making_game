var app = angular.module( "quiz", ['ui.bootstrap'] );

app.controller( "quizController", function userController($scope,$http,$location) {
  var qs = $location.search();
  var quiz_id = qs.id;

  $scope.quiz = {"questions": []};

  var req = $http.get("/quiz_editor_api/?id="+quiz_id);
  req.success(function(data, status, headers, config) {
    for(var i in data.quiz.questions) {
      question = data.quiz.questions[i];
      $scope.add_question(question.text,question.source,question.answer);
    };
  });

  $scope.add_question = function(text,source,answer) {
    var question = {
        "text": text,
        "source": source,
        "answer": answer,
    }

    $scope.quiz.questions.push(question);
  };
})