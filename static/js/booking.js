"use strict";
const booking_user_name = document.querySelector(".booking-user-name");
const attraction_info_img = document.querySelector(".attraction-info-img");
const attraction_info_name = document.querySelector(".attraction-info-name");
const attraction_info_date = document.querySelector(".attraction-info-date");
const attraction_info_time = document.querySelector(".attraction-info-time");
const attraction_info_price = document.querySelector(".attraction-info-price");
const attraction_info_address = document.querySelector(
  ".attraction-info-address"
);
const booking_confirm_total = document.querySelector(".booking-confirm-total");
const have_attraction_ordered = document.querySelector(
  ".have-attraction-ordered"
);
const no_attraction_ordered = document.querySelector(".no-attraction-ordered");

function getbookingData() {
  fetch("/api/booking", {
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (bookingData) {
      if (bookingData.message === "未登入系統，拒絕存取") {
        window.location = "/";
      } else {
        console.log(bookingData);
        booking_user_name.textContent = currentUser;
        if (bookingData.data) {
          have_attraction_ordered.classList.remove("hidden");
          no_attraction_ordered.classList.add("hidden");
          attraction_info_time.textContent =
            bookingData.data.time === "morning"
              ? " 早上九點到下午四點"
              : " 下午兩點到晚上九點";
          attraction_info_name.textContent = bookingData.data.attraction.name;
          attraction_info_date.textContent = bookingData.data.date;
          attraction_info_price.textContent = bookingData.data.price;
          attraction_info_address.textContent =
            bookingData.data.attraction.address;
          attraction_info_img.setAttribute(
            "src",
            bookingData.data.attraction.image
          );

          booking_confirm_total.textContent = bookingData.data.price;
        }
      }
    })
    .catch(function (error) {
      console.log(error);
    });
}
document
  .querySelector(".attraction-info-delete")
  .addEventListener("click", function () {
    fetch("/api/booking", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (text) {
        console.log(text);
        have_attraction_ordered.classList.add("hidden");
        no_attraction_ordered.classList.remove("hidden");
      })
      .catch(function (error) {
        console.log(error);
      });
  });

getbookingData();

have_attraction_ordered.classList.add("hidden");
no_attraction_ordered.classList.remove("hidden");
