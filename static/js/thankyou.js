const orderNumber = document.querySelector(".thankyou-info-orderNumber");
//orderinfo
const orderIMG = document.querySelector(".thankyou-img");
const orderName = document.querySelector(".thankyou-info-name");
const orderDate = document.querySelector(".thankyou-info-date");
const orderTime = document.querySelector(".thankyou-info-time");
const orderPrice = document.querySelector(".thankyou-info-price");
const orderAddress = document.querySelector(".thankyou-info-address");
const userName = document.querySelector(".thankyou-userName");
//contact
const contactName = document.querySelector(".thankyou-user-contact-name");
const contactEmail = document.querySelector(".thankyou-user-contact-email");
const contactPhone = document.querySelector(".thankyou-user-contact-phone");
//get form query string
const urlParams = new URLSearchParams(window.location.search);
const queryNumber = urlParams.get("number");
let data;
//go to attaction page
const moreAttractionInfo = document.querySelector(".more-attraction-info");

async function getOrder() {
  try {
    const response = await fetch(`/api/order/${queryNumber}`, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    data = await response.json();
    if (currentUser) {
      if (data.data.status === 0) {
        data = data.data;
        displayPayInfo(data);
      } else {
      }
    } else {
      window.location = "/";
    }
  } catch (error) {
    console.log(error);
  }
}
const displayPayInfo = function (data) {
  userName.textContent = currentUser.name;
  orderIMG.setAttribute("src", data.trip.attraction.image);
  orderNumber.textContent = data.number;
  orderName.textContent = data.trip.attraction.name;
  orderDate.textContent = data.trip.date;
  orderTime.textContent =
    data.trip.time === "morning"
      ? " 早上九點到下午四點"
      : " 下午兩點到晚上九點";
  orderPrice.textContent = data.price;
  orderAddress.textContent = data.trip.attraction.address;
  contactName.textContent = data.contact.name;
  contactEmail.textContent = data.contact.email;
  contactPhone.textContent = data.contact.phone;
};
//event

getOrder();
moreAttractionInfo.addEventListener("click", function () {
  window.location = `/attraction/${data.trip.attraction.id}`;
});
