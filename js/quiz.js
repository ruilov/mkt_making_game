var app = angular.module( "quiz", ['ui.bootstrap'] );

app.controller( "quizController", function userController($scope,$http,$location,$filter) {
  var qs = $location.search();
  var quiz_id = qs.id;

  $scope.quiz = {"questions": [], "url": quiz_url(quiz_id), "title": "Make some markets"};

  $scope.add_question = function(question) {
    if(!question.guess_low) question.guess_low = 0;
    if(!question.guess_high) question.guess_high = 0;

    question.guess_low = format_num(question.guess_low,$filter);
    question.guess_high = format_num(question.guess_high,$filter);
    if(question.answer) question.answer = format_num(question.answer,$filter);

    $scope.quiz.questions.push(question);
  };

  quiz_api_cb = function(quiz, status, headers, config) {
    if(quiz.status=="old")
      $scope.quiz.title = new Date(quiz.releaseDate).toDateString();

    $scope.state = quiz.state;
    if($scope.state=="filled") {
      $scope.quiz.title = "Click for live ranking";
    }
    $scope.quiz.questions = [];
    for(var i in quiz.questions) {
      question = quiz.questions[i];
      $scope.add_question(question);
      
    };
  };

  quiz_api_cb($scope.quiz_data);

  // the command where the user submits answers to a quiz
  $scope.submit = function() {
    var req = $http.post("/quiz_api/?id="+quiz_id,$scope.quiz);
    req.success(quiz_api_cb);
  };
});

// Directive for formatting numbers while the user is inputting them
app.directive('format', function ($filter) {
  'use strict';

  return {
    require: '?ngModel',
    link: function (scope, elem, attrs, ctrl) {
      if (!ctrl) {
        return;
      }

      ctrl.$formatters.unshift(function () {
        return $filter('number')(ctrl.$modelValue);
      });

      ctrl.$parsers.unshift(function (viewValue) {
        // get the stuff after the decimal place as filter(number) insists in round to 3 and if I pass fractionSize as an argument
        // then it formats to that size...
        var postfix = "";
        var hasPost = false;
        var idx = viewValue.indexOf(".");
        if(idx!=-1) {
          hasPost = true;
          postfix = viewValue.substr(idx+1);
          var idx2 = postfix.indexOf(".");
          if(idx2!=-1) {
            elem.val("");
            return "";
          }
          if(postfix.length>0 && (isNaN(parseFloat(postfix)) || !isFinite(postfix))) {
            elem.val("");
            return "";
          }
          viewValue = viewValue.substr(0,idx);
        }

        var plainNumber = viewValue.replace(/[\,]/g, '');
        var elemVal = $filter('number')(plainNumber);
        if(elemVal.length==0) {
          elem.val("");
          return "";  // this makes sure we see a validation error on the user screen
        }

        if(hasPost) {
          elemVal += "." + postfix;
          plainNumber = parseFloat(plainNumber) + parseFloat("0."+postfix);
          plainNumber = plainNumber + "";
        }
        elem.val(elemVal);

        // console.log(viewValue + " , " + plainNumber + " , " + elemVal);
        return plainNumber;
      });
    }
  };
});