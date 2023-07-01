
//Gender Switch functionality

maleBtn = document.querySelectorAll(".form__input-gender")[0]
femaleBtn = document.querySelectorAll(".form__input-gender")[1]
genderInput = document.querySelector("#gender");

// Adding eventListeners to male and female buttons
maleBtn.addEventListener("click", switchMale);
femaleBtn.addEventListener("click", switchFemale);
maleBtn.addEventListener("keypress", switchMale);
femaleBtn.addEventListener("keypress", switchFemale);


//functions switching styles and setting value to hidden gender input
function switchMale(e) {

    if (e.type === "keypress" && e.key !== "Enter") {
        return
    }
    femaleBtn.classList.remove("checked");
    maleBtn.classList.add("checked");
    genderInput.value = maleBtn.innerText.toLowerCase();
}

function switchFemale(e) {
    if (e.type === "keypress" && e.key !== "Enter") {
        return
    }
    maleBtn.classList.remove("checked");
    femaleBtn.classList.add("checked");
    genderInput.value = femaleBtn.innerText.toLowerCase();
}