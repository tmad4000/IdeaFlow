lib('util', {
  clone: function(templateId) {
    return document.getElementById(templateId).firstChild.cloneNode(true); 
  },
  
  post: function(url, data, success, complete, error) {
    
    data['csrfmiddlewaretoken'] = window.locals.csrf_token;
    
    $.ajax({
      type:'POST',
      url: url,
      data: data,
      success: success,
      error: error,
      complete: complete
    });
  },
  
  async: function(func) {
    setTimeout(func, 0);
  }
});
