$(document).ready(function() {
  $('.postmsg').click(function() {
    $.ajax({
      type:'POST',
      url:'/post',
      data:"msg="+$('#messages').find(":selected").attr('n'),
      success: function(resp) { alert(resp['response']); }
    })

  });
});
