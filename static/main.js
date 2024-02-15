// https://docs.djangoproject.com/en/3.2/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

jQuery(function ($){
 // $("spinner-border").fadeIn(500);
 // let loading = ` <div class="spinner-border"> <div/>&nbsp;&nbsp; Please wait..`
$(document).ajaxSend(function(event, jqXHR, ajaxSettings, thrownError){

        if (ajaxSettings.data && ajaxSettings.data.includes("go_get")){
             console.log("go_get")
        }else {
             $("#bg-spinner").fadeIn(250);
        }



      // if (Array.isArray(ajaxSettings.data) && !ajaxSettings.data.length){
      //
      //      $("#bg-spinner").fadeIn(250);
      // }

     // if (!ajaxSettings.data.includes("go_get"))

});
$(document).ajaxComplete(function(){
    $("#bg-spinner").fadeOut(250);
});
    $(document).ajaxError(function (event, jqXHR, ajaxSettings, thrownError) {
        // toastr.error("ERROR", "<li>" + thrownError + "</li>");
          $("#bg-spinner").fadeOut(250);
        console.log("ajaxError")
    });
})

 // let MY_TOAST = $.toast({
 //                heading: 'Can I add <em>icons</em>?',
 //                text: 'Yben geldim len t .',
 //                hideAfter: false,
 //                icon: 'success',
 //                position:"top-right"
 //            })

function MyToastInfo(text){
    $.toast({
    heading: 'Information',
    text: text,
    icon: 'info',
    loader: true,        // Change it to false to disable loader
    loaderBg: '#9EC600'  // To change the background
})
}

function MyToastWarn(text){
    $.toast({
    heading: 'Warning',
    text: text,
    icon: 'warning',
    loader: true,        // Change it to false to disable loader
    // loaderBg: '#9EC600',  // To change the backgroundshowHideTransition: 'plain',
    showHideTransition: 'plain',
})
}
function MyToastSuccess(text){
    $.toast({
    heading: 'Success',
    text: text,
    icon: 'success',
    loader: true,        // Change it to false to disable loader
    showHideTransition: 'slide',
})
}

function MyToastError(text){
    $.toast({
    heading: 'Error',
    text: text,
    icon: 'error',
    loader: true,        // Change it to false to disable loader
    showHideTransition: 'fade',
})
}

/*function getApartment(url) {
  $.ajax({
    url: url,
    type: "GET",
    dataType: "json",
    success: (data) => {
      const todoList = $("#todoList");
      todoList.empty();

      (data.context).forEach(todo => {
        const todoHTMLElement = `
          <li>
            <p>Task: ${todo.task}</p>
            <p>Completed?: ${todo.completed}</p>
          </li>`
        todoList.append(todoHTMLElement);
      });
    },
    error: (error) => {
      console.log(error);
    }
  });
}


function getAllTodos(url) {
  $.ajax({
    url: url,
    type: "GET",
    dataType: "json",
    success: (data) => {
      const todoList = $("#todoList");
      todoList.empty();

      (data.context).forEach(todo => {
        const todoHTMLElement = `
          <li>
            <p>Task: ${todo.task}</p>
            <p>Completed?: ${todo.completed}</p>
          </li>`
        todoList.append(todoHTMLElement);
      });
    },
    error: (error) => {
      console.log(error);
    }
  });
}

**/
