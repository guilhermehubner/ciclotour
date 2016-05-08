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
        },
        update_user: function(user){
            var fd = new FormData();

            for (var key in user) {
                if(user[key])
                    fd.append(key, user[key]);
            }

            return $http.patch("/api/update-user/", fd,{
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            });
        }
    }
});