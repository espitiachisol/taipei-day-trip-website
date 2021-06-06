let AllOrdersdata;
const historyNoData = document.querySelector(".history-no-data");
const memberSectionMain = document.querySelector(".member-section-main");
const memberHistoriesContainer = document.querySelector(
  ".member-histories-container"
);
const displayNoData = function () {
  historyNoData.classList.remove("hidden");
  memberSectionMain.classList.remove("animated-bg-sm");
};
const displayHistoryContent = function (data) {
  data.forEach((element) => {
    const html = `<div class="history">
    <img
      src='${element.data.attraction.image}'
      alt="${element.data.attraction.name}"
      class="history-img"
    />
    <div class="history-info">
      <div class="block">
        <h4>訂單號碼：</h4>
        <h4 class="history-info-orderNumber">${element.data.number}</h4>
      </div>
      <div class="block">
        <h4>台北一日遊：</h4>
        <p class="history-info-name">${element.data.attraction.name}</p>
      </div>
      <div class="block">
        <h4>日期：</h4>
        <p class="history-info-date">${element.data.date}</p>
      </div>
    </div>
    <a href="/thankyou?number=${element.data.number}" class="history-info-btn">詳細資訊</a>
  </div>`;
    memberHistoriesContainer.insertAdjacentHTML("beforeBegin", html);
    memberSectionMain.classList.remove("animated-bg-sm");
  });
};
async function getAllOrders() {
  try {
    const response = await fetch("/api/orders", {
      headers: {
        "Content-Type": "application/json",
      },
    });
    AllOrdersdata = await response.json();
    if (AllOrdersdata.error) {
      displayNoData();
    } else {
      displayHistoryContent(AllOrdersdata);
    }
  } catch (error) {
    console.log(error);
  }
}

getAllOrders();
