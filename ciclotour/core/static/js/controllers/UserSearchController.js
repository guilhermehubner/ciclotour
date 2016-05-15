angular.module("ciclotourApp").controller('UserSearchController', function($scope, UsersAPI, Message){
    $scope.users = [];
    $scope.next = null;
    $scope.filter = "";
    $scope.filterApplied = "";

    $scope.getNext = get_users;

    $scope.userTemp = null;

    $scope.search = function(){
        $scope.users = [];
        $scope.filterApplied = $scope.filter;
        get_users();
    };

    $scope.addFriend = function(user){
        $scope.userTemp = user;
        UsersAPI.add_friend(user.pk).success(addFriendSuccess).error(addFriendFail);
    };

    function get_users(){
        if($scope.filterApplied == "")
            return;

        if($scope.next == null && $scope.users.length == 0)
            UsersAPI.search_users($scope.filterApplied).success(getUsersSuccess).error(getUsersFail);
        else if($scope.next && $scope.users.length > 0)
            UsersAPI.get_next_users($scope.filterApplied, $scope.next)
                .success(getUsersSuccess).error(getUsersFail);
    }

    function getUsersSuccess(data){
        $scope.next = data.next;
        $scope.users = $scope.users.concat(data.results);
    }

    function getUsersFail(data){
        Message.showWarning('Não foi possível obter usuários.', 'Ocorreu uma falha ao tentar ' +
            'obter usuários. Tente novamente.');

        console.log(data);
    }

    function addFriendSuccess(data){
        $scope.userTemp.friendship_status = "P";
    }

    function addFriendFail(data){
        Message.showWarning('Não foi possível adicionar amigo.', 'Ocorreu uma falha ao tentar ' +
            'adicionar amigo. Tente novamente.');

        console.log(data);
    }

    angular.element(document).ready(function () {
        resizeMainPanel();
    });
});