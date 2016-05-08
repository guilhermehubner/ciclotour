angular.module("ciclotourApp").controller('UserEditFormController', function($scope, $state, Message, UsersAPI){
    $scope.email = "";
    $scope.name = "";
    $scope.last_name = "";
    $scope.profile_picture = null;
    $scope.errors = [];

    $scope.save = function(){
        $scope.errors = [];

        var obj = {
            name: $scope.name,
            last_name: $scope.last_name,
            profile_picture: $scope.profile_picture
        };

        UsersAPI.update_user(obj).success(saveSuccess).error(saveError);
    };

    /******************************************
     * Responsible method to show a preview of image
     * to user
     *******************************************/
    $scope.changeImg = function(element){
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result);
        };

        reader.readAsDataURL(element.files[0]);
    };

    function saveSuccess(){
        Message.showSuccess("Usuário alterado com sucesso!", "Dados de usuário atualizados " +
            "com sucesso.");

        $state.go('home');
    }

    function saveError(data){
        console.log(data);
         Message.showError("Falha ao tentar atualizar dados de Usuário",
             "Ocorreu uma falha ao tentar atualizar os dados do usuário.");

        $scope.errors = data;
    }
});