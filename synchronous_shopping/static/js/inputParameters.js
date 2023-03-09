const numShops = document.getElementById("numShops");
const numRoads = document.getElementById("numRoads");
const numFish = document.getElementById("numFish");
const shopsDiv = document.getElementById("shops_fish");
const roadsDiv = document.getElementById("roads_time");
const resultDiv = document.getElementById("result");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendParameters() {
    var data_form = new FormData(document.getElementById("form-parameters"));
    const n_numRoads = numRoads.value;
    const n_numShops = numShops.value;
    const n_numFish = numFish.value;
    var parameters = "";
    var shoping_centers = "";
    var roads = "";

    //Create URL POST
    parameters = n_numShops + "," + n_numRoads + "," + n_numFish;
    for (let i = 0; i < n_numShops; i++) {
        if (shoping_centers == "") {
            shoping_centers = document.getElementById(`shoppingCenter${i}`).value;
        } else {
            shoping_centers = shoping_centers + "-" + document.getElementById(`shoppingCenter${i}`).value;
        }
    }

    for (let i = 0; i < n_numRoads; i++) {
        if (roads == "") {
            roads = document.getElementById(`road${i}`).value;
        } else {
            roads = roads + "-" + document.getElementById(`road${i}`).value;
        }
    }

    fetch("/api/v1/synchronous_shopping/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: "parameters=" + parameters + "&shoping_centers=" + shoping_centers + "&roads=" + roads,
    })
        .then(function (response) {
            return response.json();
        })
        .then((data) => {
            console.log(data);
            resultDiv.innerHTML = "The minimum time is: " + data.minimum_time;
            resultDiv.style.display = ""; // show
        });
}

numShops.addEventListener("change", function () {
    const n_numShops = numShops.value;
    shopsDiv.innerHTML = "";
    const h5 = document.createElement("h5");
    h5.innerHTML = `Available types of fish:`;
    shopsDiv.appendChild(h5);
    shopsDiv.appendChild(document.createElement("br"));
    for (let i = 0; i < n_numShops; i++) {
        const div = document.createElement("div");
        div.setAttribute("class", "form-group");
        const label = document.createElement("label");
        label.setAttribute("for", `shoppingCenter${i}`);
        label.innerHTML = `Shopping center ${i + 1}:`;
        const input = document.createElement("input");
        input.setAttribute("class", "form-control");
        input.setAttribute("type", "text");
        input.setAttribute("id", `shoppingCenter${i}`);
        input.setAttribute("name", `shoppingCenter${i}`);
        input.setAttribute("required", "");

        div.appendChild(label);
        div.appendChild(input);
        shopsDiv.appendChild(div);
    }
});

numRoads.addEventListener("change", function () {
    const n_numRoads = numRoads.value;
    roadsDiv.innerHTML = "";
    const h5 = document.createElement("h5");
    h5.innerHTML = `Travel time between shopping centers (a,b):`;
    roadsDiv.appendChild(h5);
    roadsDiv.appendChild(document.createElement("br"));
    for (let i = 0; i < n_numRoads; i++) {
        const div = document.createElement("div");
        div.setAttribute("class", "form-group");
        const label = document.createElement("label");
        label.setAttribute("for", `road${i}`);
        label.innerHTML = `Road ${i + 1}:`;
        const input = document.createElement("input");
        input.setAttribute("class", "form-control");
        input.setAttribute("type", "text");
        input.setAttribute("placeholder", "Shop_a,Shop_b,time");
        input.setAttribute("id", `road${i}`);
        input.setAttribute("name", `road${i}`);
        input.setAttribute("required", "");

        div.appendChild(label);
        div.appendChild(input);
        roadsDiv.appendChild(div);
    }
});
