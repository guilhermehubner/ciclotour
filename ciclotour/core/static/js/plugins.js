function resizeMainPanel(){
    var mainPanel = $(".main_panel")[0];
    var maxHeight = $(window).height() - mainPanel.getBoundingClientRect().top - 10;

    mainPanel.style.maxHeight = (maxHeight + 'px');
};

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    resizeMainPanel();
});