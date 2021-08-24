const bookingSectionMain = document.querySelector(".booking-section-main");
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
const user_contact_name = document.querySelector(".user-contact-name");
const user_contact_email = document.querySelector(".user-contact-email");
const user_contact_phone = document.querySelector(".user-contact-phone");
const contactAllinput = document.querySelectorAll(".contact");
const errorMsg = document.querySelector(".error-msg");

const btnSubmit = document.querySelector(".submit-booking-btn");
const containerNumber = document.querySelector(".card-number-group");
const containerDate = document.querySelector(".card-expiration-date-group");
const containerCcv = document.querySelector(".card-ccv-group");
let tripData;
let data;
TPDirect.setupSDK(
  20427,
  "app_Vr2kOR3llK9Fh6xtGhPzGzJ4sjqNHmOjkW224FJmcd8yrc8I7iSHKX84MpjV",
  "sandbox"
);

TPDirect.card.setup({
  fields: {
    number: {
      element: "#card-number",
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      element: document.getElementById("card-expiration-date"),
      placeholder: "MM / YY",
    },
    ccv: {
      element: document.getElementById("card-ccv"),
      placeholder: "CCV",
    },
  },
  styles: {
    input: {
      color: "gray",
    },
    ":focus": {
      color: "black",
    },
    ".valid": {
      color: "#448899",
    },
    ".invalid": {
      color: "#d65350",
    },
  },
});
//event handler
const addRemoveHidden = function (add, remove) {
  add.classList.add("hidden");
  remove.classList.remove("hidden");
};
const setNumberFormGroupToError = function (selector) {
  selector.classList.add("has-error");
  selector.classList.remove("has-success");
};

const setNumberFormGroupToSuccess = function (selector) {
  selector.classList.remove("has-error");
  selector.classList.add("has-success");
};

const setNumberFormGroupToNormal = function (selector) {
  selector.classList.remove("has-error");
  selector.classList.remove("has-success");
};

const checkStatus = function (container, number) {
  switch (number) {
    default:
      setNumberFormGroupToNormal(container);
      break;
    case 0:
      setNumberFormGroupToSuccess(container);
      break;
    case 2:
      setNumberFormGroupToError(container);
      break;
  }
};

//update
TPDirect.card.onUpdate(function (update) {
  if (update.canGetPrime) {
    btnSubmit.removeAttribute("disabled");
  } else {
    btnSubmit.setAttribute("disabled", true);
  }
  checkStatus(containerNumber, update.status.number);
  checkStatus(containerDate, update.status.expiry);
  checkStatus(containerCcv, update.status.ccv);
});
//display
const displayOrderInfo = function (bookingData) {
  // console.log(bookingData);
  booking_user_name.textContent = currentUser.name;
  if (bookingData.data) {
    tripData = bookingData.data;
    addRemoveHidden(no_attraction_ordered, have_attraction_ordered);
    attraction_info_time.textContent =
      bookingData.data.time === "morning"
        ? " 早上九點到下午四點"
        : " 下午兩點到晚上九點";
    attraction_info_name.textContent = bookingData.data.attraction.name;
    attraction_info_date.textContent = bookingData.data.date;
    attraction_info_price.textContent = bookingData.data.price;
    attraction_info_address.textContent = bookingData.data.attraction.address;
    attraction_info_img.setAttribute("src", bookingData.data.attraction.image);

    booking_confirm_total.textContent = bookingData.data.price;
    user_contact_name.value = currentUser.name;
    user_contact_email.value = currentUser.email;
  }
};

//eventListner
contactAllinput.forEach(function (input) {
  input.addEventListener("click", () => {
    input.classList.remove("has-error");
    errorMsg.textContent = "";
  });
});

document
  .querySelector(".submit-booking-btn")
  .addEventListener("click", function (e) {
    e.preventDefault();
    if (!user_contact_name.value) {
      setNumberFormGroupToError(user_contact_name);
      errorMsg.textContent = "請輸入完整訊息";
    } else if (!user_contact_email.value) {
      setNumberFormGroupToError(user_contact_email);
      errorMsg.textContent = "請輸入完整訊息";
    } else if (!user_contact_phone.value) {
      setNumberFormGroupToError(user_contact_phone);
      errorMsg.textContent = "請輸入電話號碼";
    } else if (
      user_contact_phone.value &&
      user_contact_email.value &&
      user_contact_name.value
    ) {
      const tappayStatus = TPDirect.card.getTappayFieldsStatus();
      // console.log(tappayStatus);
      // console.log(tripData);
      if (tappayStatus.canGetPrime === false) {
        // console.log(tappayStatus);
        // console.log("can not get prime");
        return;
      }
      //get prime
      TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
          console.log("get prime error " + result.msg);
          return;
        }
        // console.log("get prime 成功，prime: " + result.card.prime);
        fetch("/api/orders", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prime: result.card.prime,
            order: {
              price: tripData.price,
              trip: {
                attraction: {
                  id: tripData.attraction.id,
                  name: tripData.attraction.name,
                  address: tripData.attraction.address,
                  image: tripData.attraction.image,
                },
                date: tripData.date,
                time: tripData.time,
              },
              contact: {
                name: user_contact_name.value,
                email: user_contact_email.value,
                phone: user_contact_phone.value,
              },
            },
          }),
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (res) {
            if (res.data.payment.message === "付款失敗") {
              // console.log(res);
              errorMsg.textContent =
                "交易失敗，信用卡資訊有錯誤或是其他原因，請再次確認。";
            } else if (res.data.payment.message === "付款成功") {
              deleteOrders();
              window.location = `/thankyou?number=${res.data.number}`;
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      });
    }
  });
const deleteOrders = function () {
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
      // console.log(text);
      addRemoveHidden(have_attraction_ordered, no_attraction_ordered);
    })
    .catch(function (error) {
      console.log(error);
    });
};
document
  .querySelector(".attraction-info-delete")
  .addEventListener("click", deleteOrders);

async function getbookingData() {
  try {
    const response = await fetch("/api/booking", {
      headers: {
        "Content-Type": "application/json",
      },
    });
    data = await response.json();
    if (data.message === "未登入系統，拒絕存取") {
      window.location = "/";
    } else {
      displayOrderInfo(data);
      bookingSectionMain.classList.remove("animated-bg-sm");
    }
  } catch (error) {
    console.log(error);
  }
}

getbookingData();
addRemoveHidden(have_attraction_ordered, no_attraction_ordered);
