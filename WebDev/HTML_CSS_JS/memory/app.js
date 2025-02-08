document.addEventListener('DOMContentLoaded', () => {
    //list all card options
    const cardArray = [
    {name: 'ale_mug', img: 'images/ale_mug.png'},
    {name: 'apple', img: 'images/apple.png'},
    {name: 'bread', img: 'images/bread.png'},
    {name: 'cheese', img: 'images/cheese.png'},
    {name: 'meat', img: 'images/meat.png'},
    {name: 'turkey', img: 'images/turkey.png'},
    {name: 'wine_bottle', img: 'images/wine_bottle.png'},
    {name: 'wine_pitcher', img: 'images/wine_pitcher.png'},
    {name: 'ale_mug', img: 'images/ale_mug.png'},
    {name: 'apple', img: 'images/apple.png'},
    {name: 'bread', img: 'images/bread.png'},
    {name: 'cheese', img: 'images/cheese.png'},
    {name: 'meat', img: 'images/meat.png'},
    {name: 'turkey', img: 'images/turkey.png'},
    {name: 'wine_bottle', img: 'images/wine_bottle.png'},
    {name: 'wine_pitcher', img: 'images/wine_pitcher.png'}
    ]

    cardArray.sort(() => 0.5 - Math.random())

    const grid = document.querySelector('.grid')
    const resultDisplay = document.querySelector('#result')
    let cardsChosen = []
    let cardsChosenId = []
    let cardsWon = []

    //create your board
    function boardStarter() {
        for (let i = 0; i < cardArray.length; i++) {
            const card = document.createElement('img')
            card.setAttribute('src', 'images/back.png')
            card.setAttribute('data-id', i)
            card.addEventListener('click', cardFlipper)
            grid.appendChild(card)
        }
    }

    //check for matches
    function matchChecker() {
      const cards = document.querySelectorAll('img')
      const optionOneId = cardsChosenId[0]
      const optionTwoId = cardsChosenId[1]

      if(optionOneId == optionTwoId) {
        cards[optionOneId].setAttribute('src', 'images/back.png')
        cards[optionTwoId].setAttribute('src', 'images/back.png')
        alert('You have clicked the same image!')
      }
      else if (cardsChosen[0] === cardsChosen[1]) {
        alert('You found a match')
        cards[optionOneId].setAttribute('src', 'images/blank.png')
        cards[optionTwoId].setAttribute('src', 'images/blank.png')
        cards[optionOneId].removeEventListener('click', cardFlipper)
        cards[optionTwoId].removeEventListener('click', cardFlipper)
        cardsWon.push(cardsChosen)
      } else {
        cards[optionOneId].setAttribute('src', 'images/back.png')
        cards[optionTwoId].setAttribute('src', 'images/back.png')
        alert('Sorry, try again')
      }
      cardsChosen = []
      cardsChosenId = []
      resultDisplay.textContent = cardsWon.length
      if  (cardsWon.length === cardArray.length/2) {
        resultDisplay.textContent = 'Congratulations! You found them all!'
      }
    }

    //flip your card
    function cardFlipper() {
      let cardId = this.getAttribute('data-id')
      cardsChosen.push(cardArray[cardId].name)
      cardsChosenId.push(cardId)
      this.setAttribute('src', cardArray[cardId].img)
      if (cardsChosen.length ===2) {
        setTimeout(matchChecker, 500)
      }
    }

    boardStarter()
  })