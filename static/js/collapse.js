
$(".collapse-button").on('click',function(){
    let target = $(this).attr('data-target');
    console.log(target);
    if ($(target).hasClass("show-section")) {
        $(target).removeClass("show-section");
        $(target).addClass("hide-section");
        $(`${target}-icon`).text("keyboard_arrow_right");
    }else{
        $(`${target}-icon`).text("keyboard_arrow_down");
        $(target).addClass("show-section");
        $(target).removeClass("hide-section");
    }
});