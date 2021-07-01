// main menu //
function main_menu() {
    var tabsNewAnim = $('#navbarSupportedContent');
    var activeItemNewAnim = tabsNewAnim.find('.active');
    var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
    var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
    var itemPosNewAnimTop = activeItemNewAnim.position();
    var itemPosNewAnimLeft = activeItemNewAnim.position();
    itemPosNewAnimLeft.left = itemPosNewAnimLeft.left;
    $(".hori-selector").css({
        "top": itemPosNewAnimTop.top + "px",
        "left": itemPosNewAnimLeft.left + "px",
        "height": activeWidthNewAnimHeight + "px",
        "width": activeWidthNewAnimWidth + "px"
    });
    $("#navbarSupportedContent").on("click", "li", function (e) {

        $('#navbarSupportedContent ul li').removeClass("active");
        $(this).addClass('active');
        var activeWidthNewAnimHeight = $(this).innerHeight();
        var activeWidthNewAnimWidth = $(this).innerWidth();
        var itemPosNewAnimTop = $(this).position();
        var itemPosNewAnimLeft = $(this).position();
        $(".hori-selector").css({
            "top": itemPosNewAnimTop.top + "px",
            "left": itemPosNewAnimLeft.left + "px",
            "height": activeWidthNewAnimHeight + "px",
            "width": activeWidthNewAnimWidth + "px"
        });
        $('.navbar-collapse').collapse('hide');
        $('.pagination').addClass("d-none");
        $('#home').addClass("d-none");
        sortby = $(this).find('a').text();
        $('#' + sortby).removeClass('d-none');
    });
}

// alert //

function alertfun(type, focus, string) {
    return '<div class="alert alert-' + type + ' alert-dismissible fade show m-0" role="alert"><strong>' + focus + '</strong>' + '&nbsp;' + string + '<button type="button" class="close" data-bs-dismiss="alert" aria-label="Close">&times;</button></div>'
}

$(document).on('click', '.close', function (e) {
    $(this).parent().alert('close')
})

//_______________//
$(document).ready(function () {
    setTimeout(function () { main_menu(); });
});
$(window).on('resize', function () {
    setTimeout(function () { main_menu(); }, 500);
});
$(".navbar-toggler").click(function () {
    setTimeout(function () { main_menu(); });
});
