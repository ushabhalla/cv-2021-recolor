
function go(){
    var k = document.getElementById("kmeansval").value;;
    var img = document.getElementById("imgpath").value;
    console.log(k)
    console.log(img)
    data = [k,img]
    $.post( "/postmethod", {
        kk: k,
        image: img
    });
    $.get("/getpythondata", function(data) {
        kmeans_img = data
        console.log(data)
    })
}

// python -m pip install Flask==1.1.2
// 