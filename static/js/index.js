"use strict";
let current_page = 0;
let keyword, data;
let ready = false;
let src = `/api/attractions?page=${current_page}`;
let pics_section = document.getElementById("pics-section");

const errorNoResult = function () {
  let errorMessage = document.createElement("P");
  errorMessage.textContent = " ↖︎ 您的查詢沒有結果，請再次查詢 ☺︎";
  errorMessage.classList.add("error-message");
  pics_section.appendChild(errorMessage);
};
// const createElement = function (element) {};
const displayPhotos = function () {
  // let totalDataLength = data.data.length;
  // console.log("total data num: ", totalDataLength);
  data.data.forEach((element) => {
    // console.log(element);
    //創建容器
    // createElement(element);
    let div_box = document.createElement("div");
    let div_img = document.createElement("img");
    let div_p_img_title = document.createElement("P");
    let div_div_info = document.createElement("div");
    let div_div_info_location = document.createElement("P");
    let div_div_info_category = document.createElement("P");
    //放入class name
    div_box.classList.add("box");
    div_img.classList.add("img", "animated-bg");
    div_box.setAttribute(
      "onclick",
      `window.open( '/attraction/${element.id}','_top' ); return false;`
    );
    div_p_img_title.classList.add("img-title");
    div_div_info.classList.add("div-info");
    div_div_info_location.classList.add("mrt");
    div_div_info_category.classList.add("category");

    //放入容器
    pics_section.appendChild(div_box);
    div_box.appendChild(div_img);
    div_box.appendChild(div_p_img_title);
    div_box.appendChild(div_div_info);
    div_div_info.appendChild(div_div_info_location);
    div_div_info.appendChild(div_div_info_category);
    //放入data
    div_img.src = element.images[0];
    div_p_img_title.textContent = element.name;
    div_div_info_location.textContent = element.mrt;
    div_div_info_category.textContent = element.category;
  });
};

async function getPhotos(src) {
  try {
    const response = await fetch(src);
    data = await response.json();
    if (data.data[0]) {
      ready = true;
      displayPhotos();
    } else {
      errorNoResult();
    }
  } catch (error) {
    console.log(error);
  }
}
window.addEventListener("scroll", () => {
  if (
    window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000 &&
    ready
  ) {
    if (data.nextPage) {
      current_page = data.nextPage;
      if (keyword) {
        src = `/api/attractions?page=${current_page}&keyword=${keyword}`;
      } else {
        src = `/api/attractions?page=${current_page}`;
      }
      getPhotos(src);
      ready = false;
    }
  }
});

const getKeywordAttractions = function () {
  //get /api/attractions keywords
  keyword = document.getElementById("keyword").value;
  // console.log(keyword);
  if (keyword) {
    //remove loaded data from on load
    var list = document.getElementById("pics-section");
    while (list.hasChildNodes()) {
      list.removeChild(list.firstChild);
    }
    current_page = 0;
    src = `/api/attractions?page=${current_page}&keyword=${keyword}`;
    getPhotos(src);
  }
};

//on load

getPhotos(src);
