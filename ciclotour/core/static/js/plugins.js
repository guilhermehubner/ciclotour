function resizeMainPanel(){
    var mainPanel = $("#main_panel")[0];
    if(!mainPanel) return;
    var maxHeight = $(window).height() - mainPanel.getBoundingClientRect().top - 10;
    mainPanel.style.maxHeight = (maxHeight + 'px');
}

function changeForm(){
    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    resizeMainPanel();
});