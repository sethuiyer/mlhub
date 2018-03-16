var table=document.getElementById("table");
table.style.display='none';
var loading=document.getElementById("loading");
loading.style.display='none';
var btn=document.getElementById("btn_search");
btn.addEventListener("click", classify);
var img_url=document.getElementById("img_url");
img_url.addEventListener("keyup",function(event) {
  if(event.keyCode === 13){
    btn.click();
  }
})

function classify() {
    table.innerHTML="";
    loading.style.display='block';
    var url="findtype?pokename="+img_url.value;
    $.get(url, function(data, status){
      table.style.display='block';
      loading.style.display='none';
      var row = table.insertRow(0);
      var cell1 = row.insertCell(0);
      cell1.innerHTML = data.results;
      var row = table.insertRow(0);
      var cell1 = row.insertCell(0);
      cell1.innerHTML = "Predicted Pokemon Type";
    });
}
