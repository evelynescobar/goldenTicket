
var addButton = document.querySelector("#add");
var message = document.getElementById("newMessage");


function showData() {
	fetch('http://localhost:8080/entries', {
		credentials: "include"
	}).then(function(response){
		response.json().then(function(data){
			message.innerHTML ="";
			data.forEach(function(element){
				
				var feed = document.createElement("li");

				var display_entrant_name = document.createElement("h5");
				display_entrant_name.innerHTML = element.entrant_name
				feed.appendChild(display_entrant_name);
				display_entrant_name.style.marginLeft ="10%"
				display_entrant_name.style.width ="15%"
				display_entrant_name.style.float ="Left"

				var display_entrant_age = document.createElement("h5");
				display_entrant_age.innerHTML = element.entrant_age
				feed.appendChild(display_entrant_age);
				display_entrant_age.style.paddingLeft ="10%"
				display_entrant_age.style.width ="15%"
				display_entrant_age.style.float ="Left"

				var display_guest_name = document.createElement("h5");
				display_guest_name.innerHTML = element.guest_name
				feed.appendChild(display_guest_name);
				display_guest_name.style.paddingLeft = "10%"
				display_guest_name.style.float ="Left"
				display_guest_name.style.width ="10%"

				var dayOfWeek = new Date().getDay();
				var ticket_id = element.random_token;
				if(dayOfWeek == ticket_id){
					feed.style.backgroundColor = "gold";
				}

				message.appendChild(feed);
			})
		})
	})
};

showData();

addButton.onclick = function () {
	var new_entrant_name = document.getElementById("entrant_name").value;
	var new_entrant_age = document.getElementById("entrant_age").value;
	var new_guest_name = document.getElementById("guest_name").value;
	//var new_random_token = document.getElementById("random_token").value;

	var bodyStr ="entrant_name=" + encodeURI(new_entrant_name);
	bodyStr += "&entrant_age=" + encodeURI(new_entrant_age);
	bodyStr += "&guest_name=" + encodeURI(new_guest_name);
	//bodyStr += "&random_token=" + encodeURI(new_random_token);

	document.getElementById('entrant_name').value='';
	document.getElementById('entrant_age').value='';
	document.getElementById('guest_name').value='';
	//document.getElementById('random_token').value='';

	
	fetch("http://localhost:8080/entries", {
		method: "POST",
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type":"application/x-www-form-urlencoded"
		}

	}).then(function(winner){
		if (winner.status == 404) {
			alert("It seems that this resource has been lost in the chocolate pipes. An Oopma Loompa will be dispatched promtly to recover the artifacts.")
		}
		else if (winner.status == 403){
			alert("The Oompa Loopas have already received your ticket. Please try again tomorrow.")
		}
		console.log("Server responded!");
		showData();
	})
};
