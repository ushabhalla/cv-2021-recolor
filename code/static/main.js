
function go(){
    // window.location.reload(true)
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("res-div").classList.add("hidden");
    document.getElementById("res-div").src = ""
    var k = document.getElementById("kmeansval").value;;
    var img = document.getElementById("imgpath").value;
    var col1 = document.getElementById("col1").value;
    var col2 = document.getElementById("col2").value;
    var col3 = document.getElementById("col3").value;
    var col4 = document.getElementById("col4").value;
    var col5 = document.getElementById("col5").value;
    var col6 = document.getElementById("col6").value;

    console.log("done go funct")
    document.getElementById("res-div").src = "kmeans_img"

    $.ajax({
        type:    "POST",
        url:     "/postmethodlol", 
        data:    {
            kk: k,
            image: img,
            col1: col1,
            col2: col2,
            col3: col3,
            col4: col4,
            col5: col5,
            col6: col6
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
}

function load_image(img_src) {
    console.log('load image running', img_src)
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