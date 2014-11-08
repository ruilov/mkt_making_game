var app = angular.module( "quiz", ['ui.bootstrap'] );

app.controller( "quizController", function userController($scope,$http,$location,$filter) {
  var qs = $location.search();
  var quiz_id = qs.id;

  $scope.quiz = {
      "questions": [], 
      "url": quiz_url(quiz_id), 
      "title": "Make some markets"
  };

  $scope.add_question = function(question) {
    if(!question.guess_low) question.guess_low = 0;
    if(!question.guess_high) question.guess_high = 0;

    question.guess_low = format_num(question.guess_low,$filter);
    question.guess_high = format_num(question.guess_high,$filter);
    if(question.answer) question.answer = format_num(question.answer,$filter);
    $scope.quiz.questions.push(question);
  };

  quiz_api_cb = function(quiz, status, headers, config) {
    if(quiz.status=="old") {
      $scope.quiz.title = new Date(quiz.releaseDate).toLocaleDateString();
      if(quiz.state=="to_fill") 
          $scope.quiz.title = "Practice quiz from " + $scope.quiz.title + ". Score will not count.";
    };
    $scope.state = quiz.state;
    if($scope.state=="filled") $scope.quiz.title = "Click for scores";
    $scope.quiz.questions = [];
    for(var i in quiz.questions) $scope.add_question(quiz.questions[i]);
  };

  quiz_api_cb($scope.quiz_data);

  // the command where the user submits answers to a quiz
  $scope.submit = function() {
    var req = $http.post("/api/quiz/?id="+quiz_id,$scope.quiz);
    req.success(quiz_api_cb);
  };

  // deal with the star rating for the quiz
  $scope.rateQuestion = function(questionNum,rating) {
    $scope.quiz.questions[questionNum].rating = rating;
    var req = $http.post("/api/rate_question/?id="+quiz_id,
      {"question": questionNum, "rating": rating}
    );
  };
});

// directive for the star ratings
app.directive("starRating", function() {
  return {
    restrict : "A",
    template : "<ul class='rating'>" +
               "  <li ng-repeat='star in stars' ng-class='star' ng-click='toggle($index)' ng-mouseover='hover($index)' ng-mouseleave='stopHover()''>" +
               "    <i class='fa fa-star'></i>" +
               "  </li>" +
               "</ul>",
    scope : {
      ratingValue : "=",
      max : "=",
      onRatingSelected : "&",
      questionNum : "=",
    },
    link : function(scope, elem, attrs) {
      scope.hoverIdx = -1;
      scope.stars = [];
      for(var i=0; i<scope.max; i++) scope.stars.push({});

      var updateStars = function() {
        for(var i=0; i<scope.max; i++) {
          scope.stars[i].filled = (i < scope.ratingValue) && scope.hoverIdx==-1;
          scope.stars[i].selecting = i < scope.hoverIdx;
        };
      };

      scope.toggle = function(index) {
        scope.hoverIdx = -1;
        scope.ratingValue = index + 1;
        updateStars();
        scope.onRatingSelected({rating: index + 1});
      };

      scope.hover = function(idx) {
        scope.hoverIdx = idx + 1;
        updateStars();
      };

      scope.stopHover = function() {
        scope.hoverIdx = -1;
        updateStars();
      };

      scope.$watch("ratingValue", function(oldVal, newVal) {
        if (newVal) { updateStars(); }
      });
    }
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