quiz_url = function(quiz_id) {
  return "/#/quiz?id="+quiz_id;
};

quiz_editor_url = function(quiz_id) {
  return "/#/quiz_editor?id="+quiz_id;
};

quiz_name = function(quiz_id) {
  return "Quiz " + quiz_id;
};

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
