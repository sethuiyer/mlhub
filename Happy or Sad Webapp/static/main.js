var img=document.getElementById("img");
img.style.display='none';
var table=document.getElementById("table");
table.style.display='none';
var loading=document.getElementById("loading");
loading.style.display='none';
var btn=document.getElementById("btn_search");
btn.addEventListener("click", classify);
var img_url=document.getElementById("img_url");
function classify() {
    table.innerHTML="";
    img.style.display='block';
    loading.style.display='block';
    img.src=img_url.value;
    var url="classify?imageurl="+img_url.value;
    $.get(url, function(data, status){
      table.style.display='block';
      loading.style.display='none';
      var row = table.insertRow(0);
      var cell1 = row.insertCell(0);
      cell1.innerHTML = data.results;
      var row = table.insertRow(0);
      var cell1 = row.insertCell(0);
      cell1.innerHTML = "Predicted Mood";
    });
}
