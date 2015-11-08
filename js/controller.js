/*
  - the $scope keeps 4 pieces of state
    1) path: the route of the current page
    2) url_params: the query string of the current page
    3) cache: a complete view of all the backend data. For now this is all the (permissioned) data. Later may be lazily built
    4) views: for each path we keep a view of the cache formatted for that particular page
      - a special view is the 'template' view which holds information required for all views, basically the navigation bar
      - one view per path (eg 'quiz'), NOT one view per url (eg 'quiz/?id=200')

  - user input that modifies the backend data can be handled in two ways:
    a) blow away the cache and do a new lookup with $scope.do_lookup
    b) modify the cache directly and rebuild views as required. More fragile but avoids a server request

  - general organization:
    - functions that respond to user input are available on the $scope, and defined inside the controller
    - view_rebuild is the entry point for rebuilding views. 'path' is an optional argument, typically used to rebuild the 'template'
    - util and directives at the end
*/

var controllerApp = angular.module( "controller", ['ngRoute','ui.bootstrap','ngTable'] );

controllerApp.config(['$routeProvider',function($routeProvider) {
  $routeProvider.
    when('/', { templateUrl: 'loading.html' }).
    when('/login/', { templateUrl: 'login.html'}).
    when('/home/', {templateUrl: 'home.html'}).
    when('/quiz/', {templateUrl: 'quiz.html'}).
    when('/quiz_editor/', {templateUrl: 'quiz_editor.html'}).
    when('/admin/', {templateUrl: 'admin.html'}).
    when('/scores/', {templateUrl: 'scores.html'}).
    when('/scores_detailed/', {templateUrl: 'scores_detailed.html'}).
    when('/suggestions/', {templateUrl: 'suggestions.html'}).
    otherwise({redirectTo: '/'});
}]);

controllerApp.controller( "theController", function ($scope,$http,$location,$routeParams,$filter,ngTableParams) {
  $scope.views = {};

  // whenever the URL changes this gets called
  $scope.$on('$locationChangeStart', function(event,next) {
    $scope.path = $location.path().replace(/\//g,"");
    $scope.url_params = $location.search();
    // if we have the cache of data already then build the view. If this is not the first url the user loads
    // we'll probably have the cache
    if($scope.cache) view_rebuild($scope,$filter,ngTableParams);
  });

  $scope.do_lookup = function() {
    $scope.cache = null;
    var responsePromise = $http.get("/api/lookup/");
    responsePromise.success(function(data, status, headers, config) {
      $scope.cache = data;
      console.log(data);
      if(!data.logged) {
        $location.path("/login/");
      } else {
        view_rebuild($scope,$filter,ngTableParams,"template");
        if($scope.path) view_rebuild($scope,$filter,ngTableParams);
        // some of the authentication stuff sends the user to '/'. That means home as long as the user is logged in
        if($location.path()=='/') $location.path("/home/");
      };
    });
  };

  $scope.do_lookup();

  // the scope functions below are the callbacks that respond to form-like user input
  $scope.admin_quiz_change_status = function(quiz,new_status) {
    var qi; // when inside the http callback use qi instead of i as i will have changed by then
    for(var i in $scope.cache.quizzes) {
      if($scope.cache.quizzes[i]==quiz) {
        qi = i;
        if(!confirm("Do you really want to " + new_status + " this quiz?")) return;
        var req = $http.post("/api/quiz_status_update/",{"new_status": new_status, "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.cache.quizzes[qi].status = new_status;
          // rebuild the template as old jobs might have changed
          view_rebuild($scope,$filter,ngTableParams,"template");
          // rebuild the current view
          view_rebuild($scope,$filter,ngTableParams);
        });
      };
    };
  };

  $scope.admin_quiz_delete = function(quiz) {
    var qi; // when inside the http callback use qi instead of i as i will have changed by then
    for(var i in $scope.cache.quizzes) {
      if($scope.cache.quizzes[i]==quiz) {
        qi = i;
        if(!confirm("Do you really want to delete this quiz?")) return;
        var req = $http.post("/api/quiz_status_update/",{"new_status": "delete", "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.cache.quizzes.splice(qi,1);
          // rebuild the template as old jobs might have changed
          view_rebuild($scope,$filter,ngTableParams,"template");
          // rebuild the current view
          view_rebuild($scope,$filter,ngTableParams);
        });
      };
    };
  };

  $scope.editor_add_question = function() {
    $scope.views.quiz_editor.questions.push(empty_question());
  };

  $scope.editor_remove_question = function(question) {
    questions = $scope.views.quiz_editor.questions;
    for(var qi in questions)
      if(questions[qi]==question) questions.splice(qi,1);
  };

  $scope.editor_save_quiz = function() {
    $http.post("/api/save_quiz_editor/",$scope.views.quiz_editor);
    // check if we need to add this quiz to the cache
    for(var qi in $scope.cache.quizzes)
      if($scope.cache.quizzes[qi].id==$scope.views.quiz_editor.id) {
        // should this quiz keep its fillout info?
        $scope.cache.quizzes[qi]=$scope.views.quiz_editor;
        return;
      }
    $scope.cache.quizzes.splice(0,0,$scope.views.quiz_editor);
  };

  // the command where the user submits answers to a quiz
  $scope.quiz_submit = function() {
    var req = $http.post("/api/quiz_submit/",$scope.views.quiz);
    req.success(function() {
      // when the user submits a quiz too much stuff changes. Old jobs in the navibard.
      // User now has access to the answers of this quiz, as well as scores
      // might as well do a new lookup
      // note that quiz fillouts have keys which make them synchrnous, so we know
      // that when we do the look, the fillout will be there
      $scope.do_lookup();
    });
  };

  $scope.quiz_rate_question = function(questionNum,rating) {
    $scope.views.quiz.questions[questionNum].rating = rating;
    var req = $http.post("/api/rate_question/",
      {"quiz_id": $scope.views.quiz.id, "qIdx": questionNum, "rating": rating}
    );
  };

  $scope.suggestions_submit = function(sug) {
    var req = $http.post("/api/suggestion/",{"suggestion": sug});
  };

  $scope.sendmail = function(quiz) {
    if(!confirm("Do you really want to send the emails?")) return;
    var req = $http.post("/api/sendmail/",{"test": true});
    req.success(function(data, status, headers, config) {
      for(var k in data) {
        $scope.email_answer = k;
        return;
      };
    });
  };
});

// ================== MODEL and VIEWS ================

// path is optional
view_rebuild = function($scope,$filter,ngTableParams,path) {
  path = path || $scope.path;
  // console.log("rebuilding " + path);
  $scope.views[path] = view_data($scope.cache,path,$scope.url_params,$filter,ngTableParams);
};

// entry point for taking data from the backend and what url is displaying (= path+params) and constructing
// a version of the data which ia in suitable format for the html display
view_data = function(data,path,params,$filter,ngTableParams) {
  if(path=="template") return template_data(data);
  if(path=="home") return home_data(data);
  if(path=="quiz") return quiz_data(data,params,$filter);
  if(path=="admin") return admin_data(data);
  if(path=="quiz_editor") return quiz_editor_data(data,params);
  if(path=="scores") return scores_data(data,ngTableParams);
  if(path=="scores_detailed") return scores_detailed_data(data,params,$filter,ngTableParams);
};

// template is basically the nagivation bar
template_data = function(data) {
  view = {"old_quizzes": []};
  for(var qi in data.quizzes) {
    var quiz = data.quizzes[qi];
    if(quiz.status!="old" && !("fillout" in quiz)) continue;
    quiz.url = quiz_url(quiz.id);
    quiz.sortableDate = new Date(quiz.releaseDate);
    quiz.date = quiz.sortableDate.toLocaleDateString("en-US");
    view.old_quizzes.push(quiz);
  };
  view.old_quizzes.sort(function(a,b) {
    if(a.sortableDate<b.sortableDate) return 1;
    else if(a.sortableDate>b.sortableDate) return -1;
    return 0;
  });
  return view;
}

// home is the landing page
home_data = function(data) {
  view = {"has_active_quiz": false};
  for(var qi in data.quizzes) {
    var quiz = data.quizzes[qi];
    if(quiz.status=="active") {
      view.has_active_quiz = "true";
      view.active_quiz = quiz;
      view.active_quiz.url = quiz_url(view.active_quiz.id);
    };
  };
  return view;
};

// quiz display a single quiz, whether old or new, filled to to-be-filled
quiz_data = function(data,params,$filter) {
  quiz_id = params.id;
  for(var qi in data.quizzes) {
    var quiz = data.quizzes[qi];
    if(quiz.id!=quiz_id) continue;
    quiz.title = new Date(quiz.releaseDate).toLocaleDateString("en-US");
    quiz.url = quiz_url(quiz.id);

    if(!("user_email" in data)) return null; // we should always have user_email, but just in case
    user_email = data.user_email;

    if("fillout" in quiz) {
      quiz.state = "filled";
      quiz.title = "How did you do?";
      myfill = quiz.fillout;
      for(var ni in quiz.questions) {
        question = quiz.questions[ni];
        question.answer_str = format_num(question.answer,$filter);
        question.guess_low = format_num(myfill.guesses_low[ni],$filter);
        question.guess_high = format_num(myfill.guesses_high[ni],$filter);

        // check accuracy. This is used by the html to display answers in different colors
        question.correctt = "no";
        ansNum = parseFloat(question.answer); // why is answer a string?!
        if(myfill.guesses_low[ni]<=ansNum && myfill.guesses_high[ni]>=ansNum)
          question.correct = "yes";
      };
    } else {
      quiz.state = "to_fill";
      if(quiz.status=="old") quiz.title = "Practice on an old quiz";
      else quiz.title = "Make some markets";
      for(var ni in quiz.questions) {
        question = quiz.questions[ni];
        question.guess_low = 0;
        question.guess_high = 0;
      };
    };

    return quiz;
  };
  return null;
};

// admin lists all past+future quizes and allows me to chnage their status
admin_data = function(data) {
  view = {"quizzes": [] };
  nextID = 0;
  for(var qi in data.quizzes) {
    var quiz = data.quizzes[qi];
    quiz.url = quiz_url(quiz.id);
    quiz.editorUrl = quiz_editor_url(quiz.id);
    view.quizzes.push(quiz);
    nextID = Math.max(nextID,parseInt(quiz.id)+1);
  };
  view.nextURL = quiz_editor_url(nextID);
  view.quizzes.sort(function(a,b) {
    if(a.id<b.id) return 1;
    else if(a.id>b.id) return -1;
    return 0;
  });
  return view;
};

quiz_editor_data = function(data,params) {
  quiz_id = params.id;
  view = {"id": quiz_id, "status": "editor", "questions": []};
  for(var qi in data.quizzes) {
    var quiz = data.quizzes[qi];
    if(quiz.id!=quiz_id) continue;

    view.status = quiz.status;
    for(var ni in quiz.questions) {
      var q = quiz.questions[ni];
      view.questions.push({"text": q.text, "answer": q.answer, "source": q.source});
    }
    return view;
  };

  // this must be a new quiz
  view.questions.push(empty_question());
  return view;
};

// view for when we see the summary of all scores
scores_data = function(data,ngTableParams) {
  view = {"columns": [{title: "Player", field: "player", visible: true}]};
  
  // create one column for each quiz
  for(var qi in data.quizzes) {
    if(!("scores" in data.quizzes[qi])) continue;
    quiz_id = data.quizzes[qi].id;
    title = new Date(data.quizzes[qi].releaseDate).toLocaleDateString("en-US"); 
    view.columns.push({title: title, link: true, field: quiz_id, visible: true});
  };

  // create the rows
  view.table_data = [];
  for(var ui in data.user_names) {
    row = {"player": data.user_names[ui]};
    if(ui==data.user_id) row.highlight_class = "highlighted-row";
    for(var qi in data.quizzes) {
      quiz = data.quizzes[qi];
      if(!("scores" in quiz) || !(ui in quiz.scores)) continue;
      
      total_score = 0
      for(var ni in quiz.scores[ui]) total_score += quiz.scores[ui][ni].score;
      row[quiz.id] = total_score;
    };
    view.table_data.push(row);
  };

  // create the total column
  view.columns.push({title: "Total", field: "total", visible: true});
  for(var i in view.table_data) {
    total = 0;
    for(var col in view.table_data[i]) {
      if(col=="player" || col=="highlight_class") continue;
      if(view.table_data[i][col]) total += view.table_data[i][col];
    };
    view.table_data[i].total = total;
  };

  // set up the table parameters
  view.tableParams = new ngTableParams({
    page: 1,                                  // show first page
    count: view.table_data.length,            // count per page
    sorting: {
      total: 'desc'                           // initial filter
    }
  }, {
    counts: [], // hide page counts control
    total: 0,  // value less than count hide pagination
    getData: function($defer, params) {
      // use build-in angular filter
      var orderedData = view.table_data;
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
          var res = 0;
          if(typeof(a)==typeof(b)) res = a < b ? -1 : a > b;
          else if(a==undefined) res = -1;
          else res = 1;
          if(!asc) res *= -1;
          return res;
        });
      };

      $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
    }
  });

  return view;
};

// view for seeing the score of a single quizz
scores_detailed_data = function(data,params,$filter,ngTableParams) {
  quiz_id = params.id;
  quiz = null;
  for(var qi in data.quizzes) {
    if(data.quizzes[qi].id == quiz_id) {
      quiz = data.quizzes[qi];
      break;
    };
  };
  if(quiz==null || !("scores" in quiz)) return;
  
  view = { "columns": [
    {title: "Player", field: "player", visible: true},
    {title: "Bid", field: "low", visible: true},
    {title: "Offer", field: "high", visible: true},
    {title: "Score", field: "score", visible: true},
  ] };

  view.score_by_q = [];
  for(var ni in quiz.questions) {
    q_scores = [];
    for(var ui in quiz.scores) {
      guess = quiz.scores[ui][ni];
      row = {
          "player": data.user_names[ui],
          "low": format_num(guess.low,$filter),
          "high": format_num(guess.high,$filter),
          "score": guess.score
      };
      q_scores.push(row);
    };
    view.score_by_q.push(q_scores);
  };

  view.changeQ = function(qn) {
    view.qnum = qn;
    view.question = quiz.questions[view.qnum-1];
    view.question.answerStr = format_num(view.question.answer,$filter);    

    view.qlinks = [];
    for(var i in quiz.questions) {
      q = (parseInt(i)+1);
      cla = "btn btn-default"
      if(q==view.qnum) cla = "btn btn-primary";
      view.qlinks.push({qnum: q, clas: cla});
    };

    // it's a mystery to me why this is needed. Otherwise the data table doesn't updste. Weird.
    // tried tableParams.reloadData(), $scope.apply(), no cigar...
    // It's working now, but I'll leave it here to add to the mystery
    // if(view.tableParams) view.tableParams.sorting("score", 'asc');

    view.tableParams = new ngTableParams({
      page: 1,                                                  // show first page
      count: view.score_by_q[view.qnum-1].length,               // count per page
      sorting: {
        score: 'desc'                                           // initial filter
      }
    }, {
      counts: [], // hide page counts control
      total: 0,  // value less than count hide pagination
      getData: function($defer, params) {
        // use build-in angular filter
        var orderedData = view.score_by_q[view.qnum-1];
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

  view.changeQ(1);

  return view;
}

// ================= UTIL functions ======================

quiz_url = function(quiz_id) {
  return "/#/quiz/?id="+quiz_id;
};

quiz_editor_url = function(quiz_id) {
  return "/#/quiz_editor/?id="+quiz_id;
};

empty_question = function() {
  return {"text": "", "answer": "", "source": ""};
}

format_num = function(num,filter) {
  num = num + "";

  var idx = num.indexOf(".");
  var postfix = "";
  var hasPost = false;
  if(idx!=-1) {
    hasPost = true;
    postfix = num.substr(idx+1);
    num = num.substr(0,idx);
  }

  num = filter('number')(num);
  if(hasPost) num += "." + postfix;
  return num;
}

// ================== DIRECTIVES ==============

// directive for the star ratings
controllerApp.directive("starRating", function() {
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
controllerApp.directive('format', function ($filter) {
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
        return plainNumber;
      });
    }
  };
});