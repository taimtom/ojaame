(function($) {

    var endpoint='/products/api/';
 $.ajax({
    type:'GET',
    url:endpoint,
    success:function(data){
        alert('sucess');  
        
    },
    error:function(){
        alert('error loading review');
    }
 })
  })(jQuery);
  
  
  