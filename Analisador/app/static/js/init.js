(function($){
  $(function(){

    $('.sidenav').sidenav();

  }); // end of document ready
})(jQuery); // end of jQuery name space

$(document).ready(function(){
  // $('.collapsible').collapsible();
  $(".collapsible-header").addClass("active"); //manter campos abertos ao iniciar
  $('.collapsible').collapsible({accordion: false}); // accordion serve para não deixar um campo fechar ao abrir outro
});