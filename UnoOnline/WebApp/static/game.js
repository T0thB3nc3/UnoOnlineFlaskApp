let gameStarted = false;

function startGame() {
    const numPlayers = parseInt($('#num_players').val());
    $.ajax({
        url: '/start_game',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ num_players: numPlayers }),
        success: function(response) {
            if (response.status === 'Game started') {
                $('#main-menu').hide();  // Elrejtjük a főmenüt
                $('#game-container').show();  // Megjelenítjük a játéktér elemeit

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

function displayOpponentHands(opponentHands, playerAvatars) {
    Object.keys(opponentHands).forEach(opponent => {
        const cardsContainer = $(`#${opponent}-cards`);
        cardsContainer.empty(); // Törli a korábbi kártyákat
        for (let i = 0; i < opponentHands[opponent].length; i++) {
            const cardBack = $('<div>').addClass('card-back'); // Hátlapok
            cardsContainer.append(cardBack);
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

function displayPlayerHand(playerHand) {
    const handContainer = $('#player-hand');
    handContainer.empty(); // kéz kiürítése

    playerHand.forEach(card => {
        // img tag az összes kártyához
        const cardImage = `{{ url_for('static', filename='cards/${card.color}_${card.type}.svg') }}`;
        const cardElement = $('<img>')
            .attr('src', cardImage)
            .attr('alt', `${card.color} ${card.type} card`)
            .addClass('card')
            .click(() => playCard(card)); // Kattintás akció hozzáadása

        // Kártya hozzáadása a kézhez
        handContainer.append(cardElement);
    });
}


function playCard(card) {
    const selectedCard = card;  // A kijátszott kártya

    $.ajax({
        url: '/play_card',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            player: 'Player',  // A játékos azonosítása
            card: selectedCard
        }),
        success: function(response) {
            if (response.status === 'Card played') {
                displayPlayerHand(response.player_hand);  // Frissítjük a játékos kezét
                updateGameState(response);  // Játék állapotának frissítése
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
            player: 'Player'
        }),
        success: function(response) {
            if (response.status === 'Card drawn') {
                displayPlayerHand(response.player_hand);  // Frissítjük a játékos kezét
                updateGameState(response);  // Játék állapotának frissítése
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
            player: 'Player'
        }),
        success: function(response) {
            if (response.status === 'UNO called successfully') {
                alert('UNO has been called!');
                updateGameState(response);  // Játék állapotának frissítése
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
