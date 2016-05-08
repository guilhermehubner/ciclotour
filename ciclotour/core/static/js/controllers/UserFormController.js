angular.module("ciclotourApp").controller('UserFormController', function($scope, Message, UsersAPI){
    $scope.email = "";
    $scope.name = "";
    $scope.last_name = "";
    $scope.password = "";
    $scope.confirm_password = "";
    $scope.errors = [];

    $scope.save = function(){
        $scope.errors = [];

        var obj = {
            email: $scope.email,
            name: $scope.name,
            last_name: $scope.last_name,
            password: $scope.password,
            confirm_password: $scope.confirm_password
        };

        UsersAPI.create_user(obj).success(saveSuccess).error(saveError);
    };

    $scope.clean = function(){
        $scope.email = "";
        $scope.name = "";
        $scope.last_name = "";
        $scope.password = "";
        $scope.confirm_password = "";
        $scope.errors = [];
    };

    function saveSuccess(){
        Message.showSuccess("Usuário cadastrado com sucesso!", "Conta criada com sucesso, você " +
            "receberá um e-mail de confirmação de cadastro.");

        $scope.clean();

        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    }

    function saveError(data){
        $scope.errors = data;
    }
});