angular.module("ciclotourApp").factory('UsersAPI', function($http){
    return{
        get_info: function(){
            return $http.get("/api/user-profile-info/");
        }
    }
});