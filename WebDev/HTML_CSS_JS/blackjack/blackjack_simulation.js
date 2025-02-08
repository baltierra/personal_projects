//Define global variables
var DEALER_POINTS  = 0;
var PLAYER_POINTS  = 0;
var HIDDEN;
var DECK;
var STAND = 0;
var GAME_ENDED = 0;

//Load the game and call functions to facilitate the game
window.onload = function () {
    newGameDeck (); //Create a new deck
    deckShuffling (); //Shuffle the newly created deck
    startNewGame (); //Start a new game between a player and the dealer
}

//First, we need to create a new deck for each game
function newGameDeck () {
    //Create array with all the possible values for a card
    let values = ["ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "jack", "queen", "king"];

    //Array with all possible suits (names are taken from card's file names)
    let suits = ["clubs", "diamonds", "hearts", "spades"];

    //Declare an empty array to store our deck, using a global variable
    DECK = [];

    //Build the deck using a double for loop
    for (let suit = 0; suit < suits.length; suit++) {
        for (let value = 0; value < values.length; value++) {
            DECK.push(values[value] + "_of_" + suits[suit]);
        }
    }
}

//Let's now build an aux function to read the value of any deck's card
function getCardValue(card) {
    let card_info = card.split("_of_");
    let card_value = card_info[0];

    if (isNaN(card_value)) {
        if (card_value === "ace") {
            return 11;
        } else {
            return 10;
        }
    } else {
        return parseInt(card_value);
    }
}

//Now we shuffle the deck so we can a play a different game each time
function deckShuffling () {
    for (let card = 0; card < DECK.length; card++) {
        let swap = Math.floor(Math.random() * DECK.length);
        let aux = DECK[card];
        DECK[card] = DECK[swap];
        DECK[swap] = aux;
    }
}

//Function that initializes the game and deals cards
function startNewGame () {
    //Put the initial score 0-0 on screen
    document.getElementById("player-points").innerText = PLAYER_POINTS;
    document.getElementById("dealer-points").innerText = DEALER_POINTS;
    
    //Put cards for player and dealer, alternately, and update scores
    PLAYER_POINTS += drawCard("Player");
    document.getElementById("player-points").innerText = PLAYER_POINTS;

    DEALER_POINTS += drawCard("Dealer");
    document.getElementById("dealer-points").innerText = DEALER_POINTS;

    PLAYER_POINTS += drawCard("Player");
    document.getElementById("player-points").innerText = PLAYER_POINTS;

    //Let's check if the player got blackjack at with the first two cards
    if (PLAYER_POINTS === 21) {
        STAND = 1;
        document.getElementById("results").innerText = "Player Wins!";
        document.getElementById('player_hit').removeEventListener('click', oneMoreCard);
        reStartGame();
    }
    //Or if the player loses
    //We only have this case because we are not implementing the aces 1 or 11 rule
    if (PLAYER_POINTS === 22) {
        STAND = 1;
        document.getElementById("results").innerText = "House wins!";
        document.getElementById('player_hit').removeEventListener('click', oneMoreCard);
        reStartGame();
    }

    DEALER_POINTS += drawCard("Dealer");
    document.getElementById("dealer-points").innerText = DEALER_POINTS;

    //Lets check if the dealer wins with the first CanvasCaptureMediaStreamTrack.
    if (DEALER_POINTS === 21) {
        STAND = 1;
        document.getElementById("results").innerText = "House Wins!";
        document.getElementById('player_hit').removeEventListener('click', oneMoreCard);
        reStartGame();
    }

    //Next card in the deck goes to the dealer, as hidden
    HIDDEN = DECK.pop();

    //We can only Stand if the game goes on
    if (GAME_ENDED == 0 && STAND == 0) {
        document.getElementById('player_hit').addEventListener('click', oneMoreCard);
        document.getElementById('player_stand').addEventListener('click', stand, { once: true });
    }
}

function drawCard (whom) {
    let card_image = document.createElement("img");
    let card = DECK.pop();
    //Route to retrieve cards from files
    card_image.src = "images/" + card + ".png";
    if (whom == "Dealer") {
        document.getElementById("dealer_cards").append(card_image);
        return getCardValue(card);
    }
    if (whom == "Player") {
        document.getElementById("player_cards").append(card_image);
        return getCardValue(card);
    }
}

function oneMoreCard () {
    if (PLAYER_POINTS < 21 && STAND ===0) {
        PLAYER_POINTS += drawCard("Player");
        document.getElementById("player-points").innerText = PLAYER_POINTS;
        if (PLAYER_POINTS === 21) {
            document.getElementById("results").innerText = "Player Wins!";
            document.getElementById('player_hit').removeEventListener('click', oneMoreCard);
            document.getElementById('player_stand').removeEventListener('click', stand);
            reStartGame();
        } else if (PLAYER_POINTS > 21) {
            document.getElementById("results").innerText = "House Wins!";
            document.getElementById('player_hit').removeEventListener('click', oneMoreCard);
            document.getElementById('player_stand').removeEventListener('click', stand);
            reStartGame();
        }
    }
}

function stand () {
    STAND = 1;
    message = '';

    //Unveil hidden card if 17 is not yet reached
    if (DEALER_POINTS <17) {
        //add that value to dealer's points
        DEALER_POINTS += getCardValue(HIDDEN);
        let card_image = document.createElement("img");
        card_image.src = "images/" + HIDDEN + ".png";
        document.getElementById("dealer_cards").append(card_image);
    }

    //Dealer get more cards until get 17 or more
    while (DEALER_POINTS < 17) {
        DEALER_POINTS += drawCard("Dealer");
    }

    if (DEALER_POINTS == 21) {
        message = "House Wins!";
        reStartGame();
    }
    //both you and dealer <= 21
    else if (DEALER_POINTS > 21) {
        message = "Player Wins!";
        reStartGame();
    }
    else if (PLAYER_POINTS == DEALER_POINTS) {
        message = "Tie!";
        reStartGame();
    }
    else if (PLAYER_POINTS > DEALER_POINTS) {
        message = "Player Wins!";
        reStartGame();
    }
    else if (PLAYER_POINTS < DEALER_POINTS) {
        message = "House Wins!";
        reStartGame();
    }
    
    document.getElementById("dealer-points").innerText = DEALER_POINTS;
    document.getElementById("player-points").innerText = PLAYER_POINTS;
    document.getElementById("results").innerText = message;
}

function reStartGame () {
    GAME_ENDED = 1;

    // Let's create a reload button
    var reload_button = document.createElement("button");
    reload_button.innerHTML = "New Game";
    reload_button.classList = "ms-3 btn btn-primary btn-success";
    document.getElementById("new-game").append(reload_button);
    reload_button.addEventListener ("click", function() {
        window.location.reload();
    });
}