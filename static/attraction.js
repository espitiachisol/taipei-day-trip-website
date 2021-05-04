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
//radio button
timePeriod.forEach(function (e) {
  e.addEventListener("change", function (e) {
    if (e.target.id === "morning") {
      price.textContent = "2000";
    } else if (e.target.id === "afternoon") {
      price.textContent = "2500";
    }
  });
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
};

async function getData(src) {
  try {
    let response = await fetch(src);
    data = await response.json();
    console.log(data);
    displayContent();
    displayPhotos();
    showSlides(slideIndex);
  } catch (error) {
    console.log(error);
  }
}
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
// onload
getData(src);
