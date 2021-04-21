
function go(){
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

    $.post( "/postmethod", {
        kk: k,
        image: img,
        col1: col1,
        col2: col2,
        col3: col3,
        col4: col4,
        col5: col5,
        col6: col6
    });

    $.get("/getpythondata", function(data) {
        kmeans_img = data
        console.log(data)
    })
    console.log("done go funct")
    document.getElementById("res-div").src = "kmeans_img"
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("res-div").classList.remove("hidden");

    // $.get("/getpythondata", function(data) {
    //     kmeans_img = data
    //     console.log(data)
    // })
}

// python -m pip install Flask==1.1.2
// 