window.onbeforeunload = function () {
  window.scrollTo(0, 0);
};
// Desactiva la restauración de scroll del navegador para evitar el "flash"
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

// Asegúrate de que al recargar, la página comience en la parte superior
window.scrollTo(0, 0);
/*SEARCH BY USING A CITY NAME (e.g. athens) OR A COMMA-SEPARATED CITY NAME ALONG WITH THE COUNTRY CODE (e.g. athens,gr)*/
const form = document.querySelector(".top-banner form");
const input = document.querySelector(".top-banner input");
const msg = document.querySelector(".top-banner .msg");
const list = document.querySelector(".ajax-section .cities");
/*SUBSCRIBE HERE FOR API KEY: https://home.openweathermap.org/users/sign_up*/
const apiKey = "4d8fb5b93d4af21d66a2948710284366";
form.addEventListener("submit", e => {
  window.scrollTo(0, 0);
  e.preventDefault();
  let inputVal = input.value;

  //check if there's already a city
  const listItems = list.querySelectorAll(".ajax-section .city");
  const listItemsArray = Array.from(listItems);

  if (listItemsArray.length > 0) {
    const filteredArray = listItemsArray.filter(el => {
      window.onbeforeunload = function () {
        window.scrollTo(0, 0);
      };
      let content = "";
      //athens,gr
      if (inputVal.includes(",")) {
        window.onbeforeunload = function () {
          window.scrollTo(0, 0);
        };
        //athens,grrrrrr->invalid country code, so we keep only the first part of inputVal
        if (inputVal.split(",")[1].length > 2) {
          window.onbeforeunload = function () {
            window.scrollTo(0, 0);
          };
          inputVal = inputVal.split(",")[0];
          content = el
            .querySelector(".city-name span")
            .textContent.toLowerCase();
        } else {
          window.onbeforeunload = function () {
            window.scrollTo(0, 0);
          };
          content = el.querySelector(".city-name").dataset.name.toLowerCase();
        }
      } else {
        window.onbeforeunload = function () {
          window.scrollTo(0, 0);
        };
        //athens
        content = el.querySelector(".city-name span").textContent.toLowerCase();
      }
      window.scrollTo(0, 0);
      return content == inputVal.toLowerCase();
    });

    if (filteredArray.length > 0) {
      window.onbeforeunload = function () {
        window.scrollTo(0, 0);
      };
      msg.textContent = `You already know the weather for ${
      
        filteredArray[0].querySelector(".city-name span").textContent
      } ...otherwise be more specific by providing the country code as well 😉`;
      form.reset();
      input.focus();
      return;
      
    }
    window.onbeforeunload = function () {
      window.scrollTo(0, 0);
    };
  }

  //ajax here
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${inputVal}&appid=${apiKey}&units=metric`;
  
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const { main, name, sys, weather } = data;
      const icon = `https://s3-us-west-2.amazonaws.com/s.cdpn.io/162656/${
        weather[0]["icon"]
      }.svg`;
      window.onbeforeunload = function () {
        window.scrollTo(0, 0);
      };
      const li = document.createElement("li");
      li.classList.add("city");
      const markup = `
        <h2 class="city-name" data-name="${name},${sys.country}">
          <span>${name}</span>
          <sup>${sys.country}</sup>
        </h2>
        <div class="city-temp">${Math.round(main.temp)}<sup>°C</sup></div>
        <figure>
          <img class="city-icon" src="${icon}" alt="${
        weather[0]["description"]
      }">
          <figcaption>${weather[0]["description"]}</figcaption>
        </figure>
      `;
      li.innerHTML = markup;
      list.appendChild(li);
    })
    .catch(() => {
      window.scrollTo(0, 0);
      msg.textContent = "Please search for a valid city 😩";
    });
    
  msg.textContent = "";
  form.reset();
  input.focus();
});
