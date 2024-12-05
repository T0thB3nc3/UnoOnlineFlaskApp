let inGame = false;

function privMenu() {
    $.ajax({
        url: '/private_menu',
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'Private Menu') {
                $('#game-modes').hide();
                $('#private-menu').show();
            }
        },
        error: function(error) {
            alert('Unable to handle private sessions: ' + error.responseJSON.status);
        }
    });
}

function joinPrivate(){
    TODO
}
function createPrivate(){
    TODO
}

function backToModes(){
    $.ajax({
        url: '/back_to_modes',
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'Back From Private Menu') {
                $('#game-modes').show();
                $('#private-menu').hide();
            }
        },
        error: function(error) {
            alert('Unable to routing back to the game modes: ' + error.responseJSON.status);
        }
    });
}

function joinQuick(){
    TODO
}
function enterLobby() {
    $.ajax({
        url: '/enter_lobby',
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'Entered lobby') {
                $('#main-menu').hide();  // Elrejtjük a főmenüt
                $('#lobby').show();  // Elrejtjük a lobbit 
                $('#game-container').hide();  // Megjelenítjük a játéktér elemeit
                $('#game-end').hide();  // Elrejtjük a főmenüt

                // Frissíthetjük a játékosokat és más adatokat
                $('#game-id').text('Game #661071 (Sample code)');  // A játék azonosítója 
                updateGameState(response);  // Játék állapotának frissítése
                TODO
            }
        },
        error: function(error) {
            alert('Error entering lobby: ' + error.responseJSON.status);
        }
    });
}

function startGame() {
    const numPlayers = parseInt($('#num_players').val());
    $.ajax({
        url: '/start_game',
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'Game started') {
                $('#main-menu').hide();  // Elrejtjük a főmenüt
                $('#lobby').hide();  // Elrejtjük a lobbit (ha aktív volt, mondjuk gyors játéknál előszobából jött)
                $('#game-container').show();  // Megjelenítjük a játéktér elemeit
                $('#game-end').hide();  // Elrejtjük a főmenüt

                // Frissíthetjük a játékosokat és más adatokat
                $('#game-id').text('Game #661071 (Sample code)');  // A játék azonosítója
                updateGameState(response);  // Játék állapotának frissítése
            }
        },
        error: function(error) {
            alert('Error starting game: ' + error.responseJSON.status);
        }
    });
}

function gameEnd() {
    $.ajax({
        url: '/game_end',
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'Game ended') {
                $('#main-menu').hide();  // Elrejtjük a főmenüt
                $('#lobby').hide();  // Elrejtjük a lobbit (ha aktív volt, mondjuk gyors játéknál előszobából jött)
                $('#game-container').hide();  // Megjelenítjük a játéktér elemeit
                $('#game-end').show();  // Elrejtjük a főmenüt

                // Frissíthetjük a játékosokat és más adatokat
                $('#game-id').text('Game #661071 (Sample code)');  // A játék azonosítója
                updateGameState(response);  // Játék állapotának frissítése
                
            }
        },
        error: function(error) {
            alert('Error starting game: ' + error.responseJSON.status);
        }
    });
}

function displayPlayers(players) {
    const playersDiv = $('#players');
    playersDiv.empty();
    players.forEach(player => {
        playersDiv.append(`<p>${player}</p>`);
    });
}

function displayCurrentPlayer(currentPlayer) {
    const currentPlayerDiv = $('#current_player');
    currentPlayerDiv.empty();
    currentPlayerDiv.append(`<p>Current Player: ${currentPlayer}</p>`);
}

function displayOpponentHands(opponentHands, unoStatus) {
    Object.keys(opponentHands).forEach(opponent => {
        const cardsLeft = opponentHands[opponent].length;
        const unoCalled = unoStatus[opponent] || false;

        // Update card count
        $(`#${opponent}-cards-left`).text(cardsLeft);

        // Update UNO status
        const unoStatusElement = $(`#${opponent}-uno-status`);
        if (unoCalled && cardsLeft === 1) {
            unoStatusElement.addClass('active');
        } else {
            unoStatusElement.removeClass('active');
        }
    });
}

function updateGameState() {
    if (gameStarted) {
        $.get('/current_game_state', function(response) {
            // Frissítjük a dobópaklit
            displayDiscardPile(response.discard_pile);
            
            // Játékosok kezének megjelenítése
            displayPlayerHand(response.player_hands[response.current_player]);  // Aktuális játékos kártyái
            displayOpponentHands(response.player_hands, response.current_player);  // Többi játékos kártyái
            
            // Ha van nyertes, akkor jelezzük
            if (response.winner) {
                $('#game-status').text(`${response.winner} won the game!`);  // Nyertes kijelzése egy UI elemen
                gameStarted = false;  // Leállítjuk a játékot
            } else {
                $('#game-status').text('Game is ongoing...');
            }
        });
    }
}


function displayDiscardPile(card) {
    let cardImage = `{{ url_for('static', filename='cards/${card.color}_${card.type}.svg') }}`;
    $('#discard-pile').html(`<img src="${cardImage}" alt="Discarded Card">`);
}

let currentIndex = 0;

function displayPlayerHand(playerHand) {
    const handContainer = $('#player-hand');
    handContainer.empty();

    // Display a maximum of 7 cards
    const visibleCards = playerHand.slice(currentIndex, currentIndex + 7);

    visibleCards.forEach((card, index) => {
        const cardImage = card.image_url; // Assume `card.image_url` contains the URL of the card image
        const cardElement = $('<img>')
            .attr('src', cardImage)
            .attr('alt', `${card.color} ${card.type} card`)
            .addClass('card')
            .click(() => playCard(card, index)); // Attach play card event

        handContainer.append(cardElement);
    });

    toggleArrows(playerHand.length);
}

function toggleArrows(cardCount) {
    if (cardCount > 7) {
        $('#left-arrow').toggleClass('visible', currentIndex > 0);
        $('#right-arrow').toggleClass('visible', currentIndex + 7 < cardCount);
    } else {
        $('#left-arrow, #right-arrow').removeClass('visible');
    }
}

function scrollLeft() {
    if (currentIndex > 0) {
        currentIndex--;
        updateGameState(); // Refresh state
    }
}

function scrollRight() {
    const playerHand = getCurrentPlayerHand(); // Replace with the actual function to get the player's hand
    if (currentIndex + 7 < playerHand.length) {
        currentIndex++;
        updateGameState(); // Refresh state
    }
}

function playCard(card, cardIndex) {
    const currentPlayer = $('#current_player p').text().replace('Current Player: ', '');

    $.ajax({
        url: '/play_card',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            player: currentPlayer,
            card: card
        }),
        success: function(response) {
            if (response.status === 'Card played') {
                // Update discard pile
                const cardImage = `{{ url_for('static', filename='cards/${card.color}_${card.type}.svg') }}`;
                $('#discard-pile').html(`<img src="${cardImage}" alt="${card.color} ${card.type} card">`);

                // Refresh player's hand
                displayPlayerHand(response.player_hand);
                updateGameState(response); // Update game state
            }
        },
        error: function(error) {
            alert('Error playing card: ' + error.responseJSON.status);
        }
    });
}

function drawCard() {
    const currentPlayer = $('#current_player p').text().replace('Current Player: ', '');
    $.ajax({
        url: '/draw_card',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            player: currentPlayer
        }),
        success: function(response) {
            if (response.status === 'Card drawn') {
                displayPlayerHand(response.player_hand);  // Refresh the player's hand
                updateGameState(response);  // Update the game state
            }
        },
        error: function(error) {
            alert('Error drawing card: ' + error.responseJSON.status);
        }
    });
}

function callUno() {
    const currentPlayer = $('#current_player p').text().replace('Current Player: ', '');
    $.ajax({
        url: '/call_uno',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            player: currentPlayer
        }),
        success: function(response) {
            if (response.status === 'UNO called successfully') {
                alert('UNO has been called!');
                updateGameState(response);  // Refresh the game state
            }
        },
        error: function(error) {
            alert('Error calling UNO: ' + error.responseJSON.status);
        }
    });
}

function chooseColor(color) {
    const currentPlayer = $('#current_player p').text().replace('Current Player: ', '');
    $.post('/play_card', JSON.stringify({ player: currentPlayer, card: card, color: color }), function(response) {
        $('#game_log').append('<p>' + response.status + '</p>');
        displayCurrentPlayer(response.next_player);
        displayPlayerHand(response.player_hand);
        displayDiscardPile(response.discard_pile);
        $('#color_picker').hide();  // Színválasztó eltüntetése
    });
}
