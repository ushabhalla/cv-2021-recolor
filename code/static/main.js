
function go(){
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("res-div").classList.add("hidden");
    var k = document.getElementById("kmeansval").value;;
    var img = document.getElementById("imgpath").value;
    console.log(k)
    console.log(img)
    data = [k,img]
    $.post( "/postmethod", {
        kk: k,
        image: img
    });
    console.log("done go funct")
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("res-div").classList.remove("hidden");

    // $.get("/getpythondata", function(data) {
    //     kmeans_img = data
    //     console.log(data)
    // })
}

// python -m pip install Flask==1.1.2
// 