var $meanRating=$('#meanStarVal').val()
$('#meanRating').append(getStars($meanRating));

var selector=$(".rating-class");
  
  
selector.each(function(i, obj) {
 
  var ratingVal=$(this).find("input[type=hidden]").val();
  $(this).append(getStars(ratingVal))
});
function getStars(rating){
        
        rating =Math.round(rating*2)/2;
        let output = [];
        //Append all the filled whole stars
        for(var i=rating; i>=1;i--)
            output.push('<i class="fa fa-star" aria-hidden="true" ></i>');

            // If there is a half a star , append it
        if(i==.5) output.push('<i class="fa fa-star-half-o" aria-hidden="true" ></i>');
        for(let i=(5-rating); i>=1;i--)
            output.push('<i class="fa fa-star-o empty" aria-hidden="true" ></i>');
        return output.join('');
        };


  $('.fa-star').on('click', function() {
            $(this).parents('.review-rating').find('.rating-star').removeClass('checked'); // uncheck previously checked star
    
            $(this).addClass('checked'); // check currently selected star
    
            var ratingValue = $(this).attr('data-rating'); // get rating value
            var ratingTarget = $(this).attr('data-target');
    
            // set the rating value to corresponding target radio input
            $('input[name="' + ratingTarget + '"][value="' + ratingValue + '"]').prop('checked', true);
        });

        $('#dropdown').on('click', function(){
            $(this).addClass('fa-minus')
            
        });