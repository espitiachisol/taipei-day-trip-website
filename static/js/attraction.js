"use strict";
let id = window.location.pathname.split("/attraction/");
id = Number(id[1]);
let src = `/api/attraction/${id}`;
let attractionName = document.querySelector(".attraction-name");
let attractionCategory = document.querySelector(".attraction-category");
let attractionMrt = document.querySelector(".attraction-mrt");
let attractionDescription = document.querySelector(".attraction-description");
let address = document.querySelector(".address");
let transport = document.querySelector(".transport");
let data;
let slideIndex = 1;
let timePeriod = document.querySelectorAll("input[name=time-period]");
let price = document.getElementById("price");
let date = document.querySelector("input[type='date']");
let data_price = 2000;
let data_time_period = "morning";

const disablePreviousDates = function () {
  const today = new Date();
  const month =
    today.getMonth() + 1 < 10
      ? "0" + (today.getMonth() + 1)
      : today.getMonth() + 1;
  // console.log(today.getDate());
  const day = today.getDate() < 10 ? "0" + today.getDate() : today.getDate();
  const year = today.getFullYear();
  date.setAttribute("min", `${year}-${month}-${day}`);
};
disablePreviousDates();
//radio button
timePeriod.forEach(function (e) {
  e.addEventListener("change", function (e) {
    if (e.target.id === "morning") {
      price.textContent = "2000";
    } else if (e.target.id === "afternoon") {
      price.textContent = "2500";
      data_price = 2500;
      data_time_period = "afternoon";
    }
  });
});
date.addEventListener("click", () => {
  date.classList.remove("date-error");
});

const displayPhotos = function () {
  let carouselImagesContainer = document.querySelector(
    ".booking-section-carousel-images"
  );
  let dotsContainer = document.querySelector(".dots-container");
  let imgCount = 1;
  data.images.forEach((img) => {
    // console.log(img);
    //創建容器
    let div_img_box = document.createElement("div");
    let div_img = document.createElement("img");
    let dot = document.createElement("span");
    //放入class name & data
    div_img_box.classList.add("mySlides", "fade");
    dot.classList.add("dot");
    dot.setAttribute("onclick", `currentSlide(${imgCount})`);
    div_img.setAttribute("src", img);

    // 放入容器
    dotsContainer.appendChild(dot);
    div_img_box.appendChild(div_img);
    carouselImagesContainer.appendChild(div_img_box);
    imgCount++;
  });
  carouselImagesContainer.classList.remove("animated-bg");
};

const displayContent = function () {
  data = data.data;
  attractionName.textContent = data.name;
  attractionCategory.textContent = data.category;
  if (data.mrt) {
    attractionMrt.textContent = data.mrt;
  } else {
    attractionMrt.textContent = "[ ☹︎ 無資料 ]";
  }
  attractionDescription.textContent = data.description;
  address.textContent = data.address;
  if (data.transport) {
    transport.textContent = data.transport;
  } else {
    transport.textContent = "[ ☹︎ 無資料 ]";
  }
};

async function getData(src) {
  try {
    let response = await fetch(src);
    data = await response.json();
    // console.log(data);
    displayContent();
    displayPhotos();
    showSlides(slideIndex);
  } catch (error) {
    console.log(error);
  }
}

//slides images
function plusSlides(n) {
  showSlides((slideIndex += n));
}
function currentSlide(n) {
  showSlides((slideIndex = n));
}
function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  //若滑到最後一張再往右會變回第一張
  if (n > slides.length) {
    slideIndex = 1;
  }
  //若滑到第一張再往左滑會變到最後一張
  if (n < 1) {
    slideIndex = slides.length;
  }
  //把所有的img都不顯示
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  //只顯示目前選取的圖片
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}
//booking
document
  .querySelector(".booking-section-info-order")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    if (currentUser !== null) {
      if (date.value && price.textContent) {
        fetch("/api/booking", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            attractionId: data.id,
            date: date.value,
            time: data_time_period,
            price: data_price,
          }),
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (text) {
            window.location = "/booking";
            if (text.error) {
              console.log(text.error);
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      } else {
        date.classList.add("date-error");
      }
    } else {
      showModal();
    }
  });
// onload
getData(src);
