angular.module("ciclotourApp").controller('FriendsController', function($scope, UsersAPI, Message){
    $scope.users = [];
    $scope.userTemp = null;
    $scope.next = null;

    $scope.unfriend = function(user){
        $scope.userTemp = user;
        UsersAPI.unfriend(user.pk).success(unfriendSuccess).error(unfriendFail);
    };

    $scope.init = get_friends;

    function get_friends (){
        if($scope.next == null && $scope.users.length == 0)
            UsersAPI.get_friends().success(getUsersSuccess).error(getUsersFail);
        else if($scope.next && $scope.users.length > 0)
            UsersAPI.get_next_friends($scope.next).success(getUsersSuccess).error(getUsersFail);
    }

    function getUsersSuccess(data){
        $scope.users = data;
    }

    function getUsersFail(data){
        Message.showWarning('Não foi possível obter usuários.', 'Ocorreu uma falha ao tentar ' +
            'obter usuários. Tente novamente.');

        console.log(data);
    }

    function unfriendFail(data){
        Message.showWarning('Não foi possível desfazer amizade.', 'Ocorreu uma falha ao tentar ' +
            'desfazer amizade. Tente novamente.');

        console.log(data);
    }

    function unfriendSuccess(data){
        var index = $scope.users.indexOf($scope.userTemp);

        if (index > -1) {
            $scope.users.splice(index, 1);
        }
    }

    angular.element(document).ready(function () {
        resizeMainPanel();
    });
});