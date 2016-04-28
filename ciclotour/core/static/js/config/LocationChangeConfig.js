angular.module("ciclotourApp").run(function($rootScope, $urlRouter, $state, Auth) {
    $rootScope.$on('$locationChangeSuccess', function(event) {
        event.preventDefault();

        Auth.isLoggedIn().success(
            function(data){
                if(data.logged){
                    if($state.current.name === "login")
                        $state.go("home");

                    $urlRouter.sync();
                }
                else {
                    $state.go("login");
                }
            }
        ).error(
            function(){
                $state.go("login");
            }
        );
    });
});