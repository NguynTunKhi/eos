/**
 * Created by ducva on 8/13/2017.
 */
$(document).ready(function () {
   $('label').hide();
   $('#auth_user_remember_me').hide();
   $('#auth_user_password').prop("style","margin-bottom: 10px; width: 300px");
   $('#auth_user_username').prop("style","margin-bottom: 10px");
   $('input[type=submit]').prop("class", "btn btn-primary block full-width m-b");
   $(".toggle-sidebar-collapse").trigger("click");
});