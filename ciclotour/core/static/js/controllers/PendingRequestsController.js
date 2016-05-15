angular.module("ciclotourApp").controller('PendingRequestsController', function($scope, UsersAPI, Message){
    $scope.users = [];
    $scope.userTemp = null;

    $scope.addFriend = function(user){
        $scope.userTemp = user;
        UsersAPI.add_friend(user.pk).success(addFriendSuccess).error(addFriendFail);
    };

    $scope.refuseRequest = function(user){
        $scope.userTemp = user;
        UsersAPI.refuse_request(user.pk).success(refuseRequestSuccess).error(refuseRequestFail);
    };

    $scope.init = function(){
        UsersAPI.pending_requests().success(getUsersSuccess).error(getUsersFail);
    };

    function getUsersSuccess(data){
        $scope.users = data;
    }

    function getUsersFail(data){
        Message.showWarning('Não foi possível obter usuários.', 'Ocorreu uma falha ao tentar ' +
            'obter usuários. Tente novamente.');

        console.log(data);
    }

    function addFriendSuccess(data){
        var index = $scope.users.indexOf($scope.userTemp);

        if (index > -1) {
            $scope.users.splice(index, 1);
        }
    }

    function addFriendFail(data){
        Message.showWarning('Não foi possível adicionar amigo.', 'Ocorreu uma falha ao tentar ' +
            'adicionar amigo. Tente novamente.');

        console.log(data);
    }

    function refuseRequestFail(data){
        Message.showWarning('Não foi possível recusar solicitação.', 'Ocorreu uma falha ao tentar ' +
            'recusar solicitação. Tente novamente.');

        console.log(data);
    }

    function refuseRequestSuccess(data){
        var index = $scope.users.indexOf($scope.userTemp);

        if (index > -1) {
            $scope.users.splice(index, 1);
        }
    }

    angular.element(document).ready(function () {
        resizeMainPanel();
    });
});