angular.module("ciclotourApp").factory('UserProfileInfoAPI', function($http){
    return{
        get_info: function(){
            return $http.get("/api/user-profile-info/");
        }
    }
});