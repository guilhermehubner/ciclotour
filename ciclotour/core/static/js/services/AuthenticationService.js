angular.module("ciclotourApp").factory('Auth', function($http){
    return{
        authenticate : function(username, password, success, error){
            obj ={
                "username":username,
                "password":password
            };

            return $http.post("/api/token-auth/", JSON.stringify(obj)).success(success).error(error);
        },
        isLoggedIn : function(){
            return $http.get("/api/user-is-logged/");
        }
    }
});