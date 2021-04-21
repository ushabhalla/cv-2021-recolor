
function go(){
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("res-div").classList.add("hidden");
    var k = document.getElementById("kmeansval").value;;
    var img = document.getElementById("imgpath").value;
    console.log(k)
    console.log(img)
    data = [k,img]

    $.ajax({
        type:    "POST",
        url:     "/postmethodlol", 
        data:    {
            kk: k,
            image: img
        },
        success: function(data) {
            load_image(data)
            alert("Data: " + data + "\nStatus: " + status);
        },
        // vvv---- This is the new bit
        error:   function(jqXHR, textStatus, errorThrown) {
              alert("Error, status = " + textStatus + ", " +
                    "error thrown: " + errorThrown
              );
        }
      });

    // $.post( "/postmethod", {
    //     kk: k,
    //     image: img
    // }, 
    // function(){
    //     console.log('callback sucess')
    // }
    // function(data, status){
    //     console.log('callback running');
    //     alert("Data: " + data + "\nStatus: " + status);
    //   })
    //  ) ;


    // $.get("/getpythondata", function(data) {
    //     kmeans_img = data
    //     console.log(data)
    // })
}

function load_image(img_src) {
    console.log('load image running')
    $('#result_image').attr('src', img_src);
    // document.getElementById("result_image").src = img_src;
    console.log(img_src);
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("res-div").classList.remove("hidden");
    // x.src = img_src;
    // img.src = "http://IP:PORT/jpg/image.jpg" + "?_=" + (+new Date());
}

// python -m pip install Flask==1.1.2
// 