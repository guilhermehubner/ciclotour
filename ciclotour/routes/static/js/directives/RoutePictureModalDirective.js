angular.module("ciclotourApp").directive("routepictureModal",function(){
    return {
        templateUrl: "static/js/views/route_picture_modal.html",
        restrict: "E",
        replace:true,
        scope:{visible:'=', onHide: '&'},
        controller: function($scope, $stateParams, RoutesAPI){
            $scope.route = $stateParams.id;
            $scope.image = null;
            $scope.description = "";

            /******************************************
             * Responsible method to show a preview of image
             * to user
             *******************************************/
            $scope.changeImg = function(element){
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#preview').attr('src', e.target.result);
                };

                reader.readAsDataURL(element.files[0]);
            };

            /******************************************
             * Submit form data to server
             *******************************************/
            $scope.save = function(){
                var obj = {
                    route: $scope.route,
                    image: $scope.image,
                    description: $scope.description
                };

                RoutesAPI.save_route_picture(obj).success(saveRoutePictureSuccess).error(saveRoutePictureFail);
            };

            /******************************************
             * Responsible method to alert success to user
             * on saving route's picture
             *******************************************/
            function saveRoutePictureSuccess(data){
                $('#myModal .modal-title').text('Imagem enviada com sucesso!');
                $('#myModal #modal-content').text('A Imagem foi enviada com sucesso.');
                $("#myModal").modal('show');

                $scope.visible=false;
            }

            /******************************************
             * Responsible method to alert errors to user
             * on saving route's picture
             *******************************************/
            function saveRoutePictureFail(data){
                $('#myModal .modal-title').text('Falha ao enviar Imagem');
                $('#myModal #modal-content').text('Ocorreu uma falha ao tentar enviar a imagem.');
                $("#myModal").modal('show');
            }
        },
        link:function postLink(scope, element, attrs){

            $(element).modal({
                show: false
            });

            scope.$watch(function(){return scope.visible;}, function(value){

                if(value == true){
                    $(element).modal('show');
                }else{
                    $(element).modal('hide');
                }
            });

            $(element).on('shown.bs.modal', function(){
                scope.$apply(function(){
                    scope.$parent[attrs.visible] = true;
                });
            });

            $(element).on('hidden.bs.modal', function(){
                scope.$apply(function(){
                    scope.$parent[attrs.visible] = false;

                    scope.onHide({});

                    scope.image = null;
                    scope.description = "";
                });

                $('#preview').removeAttr("src");
            });
        }
    };
});