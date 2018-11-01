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

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, options);
  });

  // Or with jQuery

  $(document).ready(function(){
    $('.modal').modal();
  });