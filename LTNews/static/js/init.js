/**
 * Created by andre on 20/01/2017.
 */
$( document ).ready(function() {
    $(".button-collapse").sideNav();
    $(".parallax").parallax();
    $(".modal").modal();
    $("select").material_select();

    $("#flag").click(function() {
        var lang = Cookies.get("lang");

        if(lang === "en-us") {
            Cookies.set("lang", "es-es");
        } else {
            Cookies.set("lang", "en-us");
        }
        location.reload(true);
    });
});