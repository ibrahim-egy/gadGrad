


const userInput = document.querySelector('.image_input')
userInput.addEventListener('change', displayImage)
const image = document.querySelector(".user-input-image")
const resultButton = document.querySelector(".result-btn")
resultButton.addEventListener('click', getResult)

const resultBox =  document.querySelector(".result")
const result =  document.querySelectorAll(".result-col")[1]


function displayImage(event) {
    flipLoading()
    resultBox.classList.remove('visible')
    const url = URL.createObjectURL(event.target.files[0])
    image.src = url
    image.classList.add('visible')
    resultButton.classList.add('visible')
    flipLoading()
}

async function getResult () {
    flipLoading()
    await uploadFile()
    flipLoading()
}

function flipLoading () {
    const preLoader = document.querySelector(".preloader")
    preLoader.classList.toggle('display')
}

function updateUI(data) {

    result.innerText = data.result
    resultBox.classList.add('visible')
    resultButton.classList.remove('visible')
}

const uploadFile = async() => {

    const file = userInput.files[0]
    const fd = new FormData()
    fd.append('uploadImage', file)
    await postDataFile('/result', fd)
    .then (data => {
        updateUI(data)
    })
}




const postDataFile = async (url='', data) => {

    const response = await fetch(url, {
        method: 'POST',
        body: data,
    })
    try {
        const newData = await response.json()
        return newData
    }
    catch (error) {
        console.log("error: " + error)
    }
}