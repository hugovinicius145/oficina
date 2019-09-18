$(document).ready(function() {
    $('#id_servico').select2();
});
$(document).ready(function() {
    $('#id_produto').select2();
});                
$(document).ready(function(){
  var tam = $(window).width();
  if (tam < 768){
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  }
}); 
