window.ideaoverflow = new Object();

window.lib = function (str, object)
{
  // return a global object with the name window.ideaoverflow.*str*
  // e.g. getObject('sitting.chat') will create/get the object window.ideaoverflow.sitting.chat, merge the passed object to it, then return it.
  var ret = window.ideaoverflow;
  
  // currently only works for one depth. (don't use dots in the name)
  if(typeof ret[str] == 'undefined' || ret[str] == null)
    ret[str] = new Object();
    
  if(typeof object != 'undefined' && object != null)
    jQuery.extend(true, ret[str], object);  
    
  return ret[str];
}

window.locals = new Object();

String.prototype.strip=function(){return this.replace(/^\s+|\s+$/g, '');};

$(document).ready(function() {
  $.fn.serializeObject = function()
  {
      var o = {};
      var a = this.serializeArray();
      $.each(a, function() {
          if (o[this.name] !== undefined) {
              if (!o[this.name].push) {
                  o[this.name] = [o[this.name]];
              }
              o[this.name].push(this.value || '');
          } else {
              o[this.name] = this.value || '';
          }
      });
      return o;
  };
});
