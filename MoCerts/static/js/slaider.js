// const fon = document.querySelector('#video-bg')
// let common = document.querySelector('.common')

// fon.parentNode.removeChild(fon)
// const insertVideo = () => common.insertAdjacentElement('afterbegin', fon)
// setTimeout(insertVideo, 1000)

window.addEventListener('load', () => {

  // Find buttons
  const btnLeft = document.querySelector('.btn_left')
  const btnRight = document.querySelector('.btn_right')

  // Find post boxes
  const slaider = document.querySelector('.main__left')
  const boxes = document.querySelectorAll('.main__left--article')

  // Calculate image width for step
  const stepSize = boxes[0].clientHeight

  // Move picture
  let counter = 0; // счетчик

  function autoSlider() {
    // Если counter равен длине картинок, то обнуляем счетчик.
    if (counter >= boxes.length - 3) { counter = -1 }
    counter++;
    slaider.style.transform = 'translateY(' + `${(-stepSize) * counter - 15}px)`;
  }

  // таймер для авто слайда
  setInterval(() => autoSlider(), 4000)

  btnRight.addEventListener('click', () => {
    autoSlider()
  })

  btnLeft.addEventListener('click', () => {
    if (counter <= 0) { counter = boxes.length - 1 }
    counter--;
    slaider.style.transform = 'translateY(' + `${-stepSize * counter - 15}px)`;
  })

})







