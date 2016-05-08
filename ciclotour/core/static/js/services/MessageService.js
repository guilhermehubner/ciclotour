angular.module("ciclotourApp").factory('Message', function(){
    return{
        showSuccess : function(title, message){
            $('#messageIcon').removeClass().addClass('fa fa-check messageSuccess');
            $('#myModal .modal-title').text(title);
            $('#myModal #modal-content').text(message);
            $("#myModal").modal('show');
        },
        showWarning : function(title, message){
            $('#messageIcon').removeClass().addClass('fa fa-warning messageWarning');
            $('#myModal .modal-title').text(title);
            $('#myModal #modal-content').text(message);
            $("#myModal").modal('show');
        },
        showError : function(title, message){
            $('#messageIcon').removeClass().addClass('fa fa-close messageError');
            $('#myModal .modal-title').text(title);
            $('#myModal #modal-content').text(message);
            $("#myModal").modal('show');
        }
    }
});