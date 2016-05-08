angular.module("ciclotourApp").factory('UsersAPI', function($http){
    return{
        get_info: function(){
            return $http.get("/api/user-profile-info/");
        },
        confirmation: function(token){
            return $http.get("/api/confirmation/"+token);
        },
        create_user: function(user){
            return $http.post("/api/create-user/", user);
        }
    }
});