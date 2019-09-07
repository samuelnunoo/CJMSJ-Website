
window.addEventListener('DOMContentLoaded', function () {



    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }


      //Initalizes variables
      var avatar = document.getElementById('avatar');
      var image = document.getElementById('image');
      var input = document.getElementById('input');
      var $alert = $('.alert');
      var $modal = $('#modal');
      var cropper;
      var submit = document.getElementById('submit-button');
      var dialog = bootbox.dialog({
                                title: 'Your Profile is being Updated',
                                 message: '<p><i class="fa fa-spin fa-spinner"></i> Loading...</p>',
                                  show: false
                                    });

      var Updated = false;



      //Initalizes tooltip?
      $('[data-toggle="tooltip"]').tooltip();


        //Input Event
      input.addEventListener('change', function (e) {

        var files = e.target.files;
        var done = function (url) {
            input.value= '';
          image.src = url;
          $alert.hide();
          $modal.modal('show');
        };
        var reader;
        var file;
        var url;


        if (files && files.length > 0) {
          file = files[0];

          if (URL) {
            done(URL.createObjectURL(file));
          } else if (FileReader) {
            reader = new FileReader();
            reader.onload = function (e) {
              done(reader.result);
            };
            reader.readAsDataURL(file);
            Updated = true;
          }
        }
      });



      //Event when Modal is shown
      $modal.on('shown.bs.modal', function () {
        cropper = new Cropper(image, {
          aspectRatio: 1,
          viewMode: 3,
        });

        //Destroys Cropper after Modal is hidden
      }).on('hidden.bs.modal', function () {
        cropper.destroy();
        cropper = null;
      });


      // Event when crop button is clicked
      document.getElementById('crop').addEventListener('click', function () {
        var initialAvatarURL;


        $modal.modal('hide');

        if (cropper) {

          //Gets the cropped image
          canvas = cropper.getCroppedCanvas({})
            console.log(canvas)


          //Sets var to the image
          initialAvatarURL = avatar.src;
          //Passes the type of the original image to preserve image dimensions
          avatar.src = canvas.toDataURL();
          //SHows the progress HTML Element
          //$progress.show();

          //$alert.removeClass('alert-success alert-warning');
          //This is the compressopion


        }
        ;

      });


        //Submit Event
      submit.addEventListener('click', function(){
          console.log("started submit")

          var first_name = $('#id_first_name').val()
          var last_name = $("#id_last_name").val()
          var bio = $("#id_bio").val()
          var formData_ = new FormData();
          var Image_Check = $('#avatar').attr('src');
          var updateImage = ( Image_Check === 'https://cjmsj.s3.amazonaws.com/media/pictures/default.jpg' || Updated === true)

          if (updateImage){


              try {
              canvas.toBlob(function (blob) {

                  // Initalizing FormData object
                 // var formData_ = new FormData();


                  //Adding avatar passed blob and avatar.jpg
                  /*
                  let Title = $('#Title').html();
                  var Content = $('iframe').contents().find('body').html();
                  let Image_Check = $('#avatar').attr('src');
                  let Description =  $('#id_Description').val();

                   */

                  // New Fields




                    //Dataset
                  formData_.append('first_name', first_name);
                  formData_.append("last_name", last_name);
                  formData_.append('Image', blob);
                  formData_.append("bio", bio)



                  //Asynchronous JavaScript And XML.
                  $.ajax('/ajax/profile', {
                      method: 'POST',
                      data: formData_,
                      processData: false,
                      contentType: false,
                      beforeSend: function (xhr,settings) {


                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                                // Send the token to same-origin, relative URLs only.
                                // Send the token only if the method warrants CSRF protection
                                // Using the CSRFToken value acquired earlier
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }



                          if (Image_Check == 'https://cjmsj.s3.amazonaws.com/static/img/beautiful-landscape.jpg') {

                               bootbox.alert("Please provide a valid Image",function(){
                                    location.href='#';
                                        });

                              return false
                          }

                          if (first_name == "" || first_name == 'First Name') {
                              bootbox.alert("Please provide your first name",function(){
                                    location.href='#';
                                        });
                              return false
                          }

                          if (last_name == "" || last_name == 'Last Name') {
                              bootbox.alert("Please provide your last name",function(){
                                    location.href='#Content';
                                        });

                              return false
                          }

                          if (bio=="" || bio == "An amazing person from an amazing place!"){
                              bootbox.alert("Please add a valid Description to the Post",function(){
                                    location.href='#id_Description';
                                        });
                              return false
                          }


                          dialog.modal('show')
                      },
                      complete: function () {
                          dialog.modal('hide')
                          console.log("Complete")
                           $.getJSON('/ajax/authorized',function(data){
                                if (data['sign-up']){
                                    console.log("sign up")
                                    bootbox.alert("Please Sign-Up",function(){
                                    location.href='/users/signup/';
                                        });

                                         }
                                else{
                                       bootbox.alert("Your profile has been updated!", function(){
                                        location.href = '/'
                                    })
                                }
                                })

                      }


                  });
              });
          }

              catch(err) {
              // Move to Object

              bootbox.alert("Please provide a valid Image",function(){
                  location.href='#';

              });
          }


          }

          else{

                 //Dataset
              formData_.append('first_name', first_name);
              formData_.append("last_name", last_name);
              formData_.append("bio", bio)

               $.ajax('/ajax/profile', {
                      method: 'POST',
                      data: formData_,
                      processData: false,
                      contentType: false,
                      beforeSend: function (xhr,settings) {


                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                                // Send the token to same-origin, relative URLs only.
                                // Send the token only if the method warrants CSRF protection
                                // Using the CSRFToken value acquired earlier
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }



                          if (Image_Check == 'https://cjmsj.s3.amazonaws.com/static/img/beautiful-landscape.jpg') {

                               bootbox.alert("Please provide a valid Image",function(){
                                    location.href='#';
                                        });

                              return false
                          }

                          if (first_name == "" || first_name == 'First Name') {
                              bootbox.alert("Please provide your first name",function(){
                                    location.href='#';
                                        });
                              return false
                          }

                          if (last_name == "" || last_name == 'Last Name') {
                              bootbox.alert("Please provide your last name",function(){
                                    location.href='#Content';
                                        });

                              return false
                          }

                          if (bio=="" || bio == "An amazing person from an amazing place!"){
                              bootbox.alert("Please add a valid Description to the Post",function(){
                                    location.href='#id_Description';
                                        });
                              return false
                          }


                          dialog.show()
                      },
                      complete: function () {
                          dialog.hide()
                          console.log("Complete")
                           $.getJSON('/ajax/authorized',function(data){
                                if (data['sign-up']){
                                    console.log("sign up")
                                    bootbox.alert("Please Sign-Up",function(){


                                    location.href='/users/signup/';
                                        });

                                         }
                                else{
                                        bootbox.alert("Your profile has been updated!", function(){
                                        location.href = '/'
                                    })
                                }
                                })

                      }


                  });

          }





      })})