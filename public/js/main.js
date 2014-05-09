$(document).ready(function(){
  $('a.option').click(function() {
    var pinID = $(this).attr('pin');
    $.get('/switch', { pin:pinID }, function(data) {
       // ...
    });
    return false; // prevent default
  });
});