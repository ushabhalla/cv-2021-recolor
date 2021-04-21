// import '../static/main.css'

var user_image_loaded = 0;
var loadFile = function(event) {
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
    user_image = image.src; 
    console.log('hello please log', user_image);
};

function readURL(input) 
{
    document.getElementById("bannerImg").style.display = "block";

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById('bannerImg').src =  e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
        user_image_loaded = 1;
    }
}

function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    var dataURL = canvas.toDataURL("image/png");
    console.log('this is datAURL', dataURL);
    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

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

    user_image = document.getElementById('bannerImg');
    imgData = getBase64Image(user_image);
    console.log('this is the imgData:', imgData)
    localStorage.setItem("imgData", imgData);

    if (user_image_loaded == 1){
        img = imgData;
    }

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
            col6: col6,
            userImage: user_image_loaded,
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
