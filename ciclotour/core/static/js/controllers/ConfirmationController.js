angular.module("ciclotourApp").controller('ConfirmationController', function($scope, $state, $stateParams, UsersAPI, Message){
    $scope.init = function(){
        UsersAPI.confirmation($stateParams.token).success(confirmationSuccess).error(confirmationFail);
    };

    function confirmationSuccess(data){
        if(data.success)
            Message.showSuccess("Usuário confirmado com sucesso!",
            "Sua conta foi confirmada com sucesso!! Você já pode logar no Ciclotour.");
    }

    function confirmationFail(data){
        $state.go("login")
    }
});