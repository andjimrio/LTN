/**
 * Created by andre on 20/01/2017.
 */
$( document ).ready(function() {
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('.modal').modal();
    $('select').material_select();

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