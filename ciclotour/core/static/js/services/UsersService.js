angular.module("ciclotourApp").factory('UsersAPI', function($http){
    return{
        get_info: function(){
            return $http.get("/api/user-profile-info/");
        },
        search_users: function(filter){
            return $http.get("/api/user-search/?search="+filter);
        },
        get_next_users: function(filter, next){
            return $http.get("/api/user-search/?page="+next+"&search="+filter);
        },
        get_friends: function(){
            return $http.get("/api/get-friends/")
        },
        get_next_friends: function(next){
            return $http.get("/api/get-friends/?page="+next);
        },
        pending_requests: function(){
            return $http.get("/api/pending-requests/");
        },
        confirmation: function(token){
            return $http.get("/api/confirmation/"+token);
        },
        create_user: function(user){
            return $http.post("/api/create-user/", user);
        },
        add_friend: function(userId){
            return $http.get("/api/add-friend/"+userId);
        },
        refuse_request: function(userId){
            return $http.get("/api/refuse-request/"+userId);
        },
        unfriend: function(userId){
            return $http.get("/api/unfriend/"+userId);
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