var end="http://127.0.0.1:8000";
var endpoint=end + "/record/sale/";
var endpointprod=end + "/products/api/detail/";
var cartTotal=$("#cartTotal");
var cartList=$(".header-cart-list");
$(".cart-div").each(function (key,obj){
  var cartTest=$(obj).find(".incarttest").val();
  
  if (cartTest){
    $(obj).find(".cart-form").css("display","none");
  };
});
$(".cart-form").each(function (key,obj){
  $(this).find(".main-cart-btn").on("click", function (event){
    event.preventDefault();
    var productVal=$(obj).find("input[name=product_name]").val();
  var productQty=$(obj).find("input[name=product_quantity]").val();
  var productPrice=$(obj).find("input[name=product_price]").val();
  var productCsrf=$(obj).find("input[name=product_csrf]").val();
  
  datum={
        "user":1,
        "product": productVal,
        "quantity": productQty,
        "price": productPrice,
        csrfmiddlewaretoken: productCsrf
        
    };
    var btnCli=$(obj).find(".main-cart-btn");
$.ajax({
    type: "POST",
    url: endpoint ,
    data: datum,
    dataType : "json",
    success: function(output){
        
       // $(this).css("display":"none");
       filterObject(output);
         btnCli.prev().append('<a href="/cart/" class="default-btn add-to-cart pull-right" style="background-color:#30323A;" ><i class="fa fa-shopping-cart"></i> Added To Cart </a>');
         
     
         btnCli.css("display","none");
        
         
        
    },
    error: function(output){
        alert("error");
    }
});
  });
  
  
});

function filterObject(ajaxOutput){
  $.ajax({
    type: "GET",
    url: endpointprod+ajaxOutput.product+"/" ,
    success: function(product){
      alert(cartList);
      cartList.prepend( '<div class="product product-widget"> <div class="product-thumb"><img src="'+product.image+'" alt=""> </div><div class="product-body"><h3 class="product-price">$'+ product.price+'<span class="qty">x'+ajaxOutput.quantity+'</span></h3><h2 class="product-name"><a href="/products/'+product.product.get_absolute_url+'">'+product.product+'</a></h2></div><form class="cart clearfix" method="post" action=""><input type="hidden" name="product_name" value="'+product.id+'" /><button class="cancel-btn"><i class="fa fa-trash"></i></button></form></div>');
    },
    error: function(output){
      console.log("error product"+output.error);
  }
   });
}
  
    