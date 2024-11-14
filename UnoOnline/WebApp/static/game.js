let gameStarted = false;

function startGame() {
    const numPlayers = parseInt($('#num_players').val());
    $.ajax({
        url: '/start_game',
        type: 'POST',
        contentType: 'application/json',  // Az adat típusát JSON-ra állítjuk
        data: JSON.stringify({ num_players: numPlayers }),  // JSON formátumban küldjük az adatokat
        success: function(response) {
            gameStarted = true;
            $('#game_log').append('<p>' + response.status + '</p>');
            displayPlayers(response.players);
            displayCurrentPlayer(response.current_player);
            updateGameState();
        },
        error: function(xhr, status, error) {
            console.error("Error: " + error);
            $('#game_log').append('<p>Error: ' + error + '</p>');
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

function updateGameState() {
    if (gameStarted) {
        $.get('/current_game_state', function(response) {
            displayDiscardPile(response.discard_pile);
            displayPlayerHand(response.player_hands[response.current_player]);
            // GYőztes esetén kihirdeti a győztest
            if (response.winner) {
                alert(`${response.winner} won the game!`);
            }
        });
    }
}

function displayDiscardPile(discardPile) {
    const discardDiv = $('#discard_pile');
    discardDiv.empty();
    discardDiv.append(`<p>Discard Pile: ${discardPile[discardPile.length - 1]}</p>`);
}

function displayPlayerHand(hand) {
    const handDiv = $('#player_hand');
    handDiv.empty();
    hand.forEach(card => {
        const cardElement = $('<button>').text(card).on('click', function() {
            playCard(card);  // Kártya lejátszása, üres funkcióval
        });
        handDiv.append(cardElement);
    });
}

function playCard(card) {
    const currentPlayer = $('#current_player p').text().replace('Current Player: ', '');
    $.ajax({
        url: '/play_card',
        type: 'POST',
        contentType: 'application/json',  // JSON típusú adatot küldünk
        data: JSON.stringify({ player: currentPlayer, card: card }),  // JSON formátumban
        success: function(response) {
            $('#game_log').append('<p>' + response.status + '</p>'); // Módosításra kerül a felület létrehozásakor !TODO
            displayCurrentPlayer(response.next_player);
            displayPlayerHand(response.player_hand);
            displayDiscardPile(response.discard_pile);
        },
        error: function(xhr, status, error) {
            console.error("Error: " + error);
            $('#game_log').append('<p>Error: ' + error + '</p>');
        }
    });
}

function drawCard() {
    const currentPlayer = $('#current_player p').text().replace('Current Player: ', '');
    $.ajax({
        url: '/draw_card',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ player: currentPlayer }),  // JSON formátumban
        success: function(response) {
            $('#game_log').append('<p>' + response.status + '</p>');
            if (response.card) {
                $('#game_log').append(`<p>You drew a ${response.card}</p>`);
            }
            displayCurrentPlayer(response.next_player);
            displayPlayerHand(response.player_hand);
        },
        error: function(xhr, status, error) {
            console.error("Error: " + error);
            $('#game_log').append('<p>Error: ' + error + '</p>');
        }
    });
}

function callUno() {
    const currentPlayer = $('#current_player p').text().replace('Current Player: ', '');
    $.ajax({
        url: '/call_uno',
        type: 'POST',
        contentType: 'application/json',  // JSON típusú adatot küldünk
        data: JSON.stringify({ player: currentPlayer }),  // JSON formátumban
        success: function(response) {
            $('#game_log').append('<p>' + response.status + '</p>');
            if (response.uno_called) {
                $('#game_log').append(`<p>${currentPlayer} has called UNO!</p>`);
            }
            displayCurrentPlayer(response.next_player);
            displayPlayerHand(response.player_hand);
        },
        error: function(xhr, status, error) {
            console.error("Error: " + error);
            $('#game_log').append('<p>Error: ' + error + '</p>');
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
