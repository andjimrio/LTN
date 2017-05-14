/**
 * Created by andre on 20/01/2017.
 */
(function($){
    $(function(){
        $('.button-collapse').sideNav();
        $('.parallax').parallax();
        $('.modal').modal();
        $('select').material_select();
    }); // end of document ready
})(jQuery); // end of jQuery name space


$( document ).ready(function() {
    $("#flag").click(function() {
        var lang = Cookies.get('lang');
        if(lang == 'es-es') {
            Cookies.set('lang', 'en-us');
        } else {
            Cookies.set('lang', 'es-es');
        }
        location.reload(true);
    });
});