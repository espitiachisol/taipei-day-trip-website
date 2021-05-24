"use strict";
//sign logn
let login = document.querySelector(".login");
let signin = document.querySelector(".signin");

let loginSigninModal = document.querySelector(".login-Signin-modal");
let overlay = document.querySelector(".overlay");

let loginErrorMessage = document.querySelector(".loginErrorMessage");
let siginErrorMessage = document.querySelector(".siginErrorMessage");

const signin_username = document.getElementById("signin_username");
const signin_email = document.getElementById("signin_email");
const signin_password = document.getElementById("signin_password");
const login_email = document.getElementById("login_email");
const login_password = document.getElementById("login_password");
const loginSubmit = document.getElementById("login");
const signinSubmit = document.getElementById("signin");

const loginSignin = document.getElementById("loginSignin");
const logOut = document.getElementById("logOut");
const login_sigin_succeeded = document.querySelector(".login-sigin-succeeded");
const bookingPage = document.querySelector(".bookingPage");
let currentUser;

function getCurrentUser() {
  fetch("/api/user", {
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (thisCurrentUser) {
      if (thisCurrentUser.data) {
        // console.log(thisCurrentUser.data);
        loginSignin.classList.add("hidden");
        logOut.classList.remove("hidden");
        currentUser = thisCurrentUser.data.name;
      } else {
        loginSignin.classList.remove("hidden");
        logOut.classList.add("hidden");
        // console.log("not login: ", thisCurrentUser);
        currentUser = null;
      }
    })
    .catch(function (error) {
      console.log(error);
    });
}
bookingPage.addEventListener("click", function () {
  if (currentUser) {
    window.location = "/booking";
  } else {
    showModal();
  }
});
const AllInput = document.querySelectorAll(".login-signin-input");
AllInput.forEach(function (input) {
  input.addEventListener("click", () => {
    input.classList.remove("login-signin-input-error");
  });
});

const displayReturnMessage = function (element, message) {
  element.classList.remove("hidden");
  element.textContent = message;
};
const removeReturnMessage = function (element) {
  element.classList.add("hidden");
  element.textContent = "";
};

logOut.addEventListener("click", function () {
  fetch("/api/user", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (text) {
      if (text.ok) {
        loginSigninModal.classList.remove("hidden");
        overlay.classList.remove("hidden");
        login.classList.add("hidden");
        signin.classList.add("hidden");
        login_sigin_succeeded.textContent = "登出成功";
        login_sigin_succeeded.classList.remove("hidden");
        setTimeout(function () {
          if (window.location.pathname === "/booking") {
            window.location = "/";
          } else {
            window.location = window.location;
          }
        }, 500);
      }
      console.log(text);
    })
    .catch(function (error) {
      console.log(error);
    });

  loginSignin.classList.remove("hidden");
  logOut.classList.add("hidden");
});

// console.log(currentUser);
const switchToLogin = function () {
  login_sigin_succeeded.classList.add("hidden");
  login.classList.remove("hidden");
  signin.classList.add("hidden");
  AllInput.forEach((element) => {
    element.value = "";
    element.classList.remove("login-signin-input-error");
  });
  removeReturnMessage(loginErrorMessage);
};
const switchToSignin = function () {
  login.classList.add("hidden");
  signin.classList.remove("hidden");
  AllInput.forEach((element) => {
    element.value = "";
    element.classList.remove("login-signin-input-error");
  });
  removeReturnMessage(siginErrorMessage);
};
const showModal = function () {
  loginSigninModal.classList.remove("hidden");
  login.classList.remove("hidden");
  overlay.classList.remove("hidden");
};
const closeModal = function () {
  loginSigninModal.classList.add("hidden");
  overlay.classList.add("hidden");
  signin.classList.add("hidden");
  login.classList.add("hidden");
  AllInput.forEach((element) => {
    element.value = "";
    element.classList.remove("login-signin-input-error");
  });
  removeReturnMessage(loginErrorMessage);
  removeReturnMessage(siginErrorMessage);
};

loginSubmit.addEventListener("submit", function (e) {
  e.preventDefault();
  fetch("/api/user", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: login_email.value,
      password: login_password.value,
    }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (text) {
      if (login_email.value && login_password.value) {
        //從後端回傳的錯誤
        if (text.message === "帳號或密碼不正確") {
          login_email.classList.add("login-signin-input-error");
          login_password.classList.add("login-signin-input-error");
          displayReturnMessage(loginErrorMessage, "您的帳號或密碼不正確");
        } else if (text.message === "密碼不正確") {
          login_password.classList.add("login-signin-input-error");
          displayReturnMessage(loginErrorMessage, "您的密碼不正確");
        } else if (text.ok) {
          //登入成功
          loginSubmit.classList.add("hidden");
          login_sigin_succeeded.textContent = "登入成功";
          login_sigin_succeeded.classList.remove("hidden");
          setTimeout(function () {
            window.location = window.location;
          }, 500);
        }
      } else {
        //輸入不完整
        displayReturnMessage(loginErrorMessage, "您的帳號或密碼輸入不完整");
        if (!login_email.value) {
          login_email.classList.add("login-signin-input-error");
        }
        if (!login_password.value) {
          login_password.classList.add("login-signin-input-error");
        }
      }
      if (text.error) {
        console.log(text);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
});

signinSubmit.addEventListener("submit", function (e) {
  e.preventDefault();

  fetch("/api/user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: signin_username.value,
      email: signin_email.value,
      password: signin_password.value,
    }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (text) {
      if (
        signin_username.value &&
        signin_email.value &&
        signin_password.value
      ) {
        if (text.message === "email重複") {
          signin_email.classList.add("login-signin-input-error");
          displayReturnMessage(siginErrorMessage, "電子郵件重複，請嘗試登入");
        } else if (text.ok) {
          signinSubmit.classList.add("hidden");
          login_sigin_succeeded.textContent = "註冊成功";
          login_sigin_succeeded.classList.remove("hidden");
          setTimeout(switchToLogin, 500);
        }
      } else {
        displayReturnMessage(siginErrorMessage, "您的資訊輸入不完整");
        if (!signin_username.value) {
          signin_username.classList.add("login-signin-input-error");
        }
        if (!signin_email.value) {
          signin_email.classList.add("login-signin-input-error");
        }
        if (!signin_password.value) {
          signin_password.classList.add("login-signin-input-error");
        }
      }

      if (text.error) {
        console.log(text.error);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
});

getCurrentUser();
