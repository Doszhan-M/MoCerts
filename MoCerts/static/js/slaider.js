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
        if (counter >= boxes.length -3) {counter = -1}
        counter++; 
        slaider.style.transform = 'translateY(' + `${(-stepSize) * counter -15}px)`;
    }

    setInterval(() => autoSlider(), 3000)

    btnRight.addEventListener('click', () => {
        autoSlider()
      })

    btnLeft.addEventListener('click', () => {
        if (counter <= 0) { counter = boxes.length -1}
        counter--;
        slaider.style.transform = 'translateY(' + `${-stepSize * counter -15}px)`;
      })
    })
    
    
    
    
    
    
    
    