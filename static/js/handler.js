
var b1 = document.getElementById("b1")
var buttons = document.getElementsByClassName("button")

console.log(buttons)

b1.onclick = function()  {

  fetch('/post', {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({"test":"other"}),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
    .then(function (response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
     }
        response.json().then(function (data) {
          console.log(data);

          var odds = document.getElementsByClassName("odds")
          console.log(odds)
          
          for (team in data){
            console.log(team)
            console.log(odds[team])
            console.log(data[team])
            
            odds[team].innerHTML = data[team]
          }

        });
      })
      .catch(function (error) {
        console.log("Fetch error: " + error);
   }); 

}


