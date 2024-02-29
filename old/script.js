document.addEventListener('DOMContentLoaded', (event) => {
    let playerBalance = 0; // Player balance starts at $0
    let walletBalance = 1000; // Start with $1000 in the wallet balance

    // Update the UI with the current balances
    const updateBalances = () => {
        document.getElementById('playerBalance').textContent = playerBalance.toFixed(2);
        document.getElementById('walletBalance').textContent = walletBalance.toFixed(2);
    };

    // Initially update the balances
    updateBalances();

    // Add cash button event
    document.getElementById('addCash').addEventListener('click', () => {
        if (walletBalance >= 100) {
            walletBalance -= 100;
            playerBalance += 100;
            updateBalances();
        } else {
            alert('Insufficient funds in wallet.');
        }
    });

    // Cash out button event
    document.getElementById('cashOut').addEventListener('click', () => {
        walletBalance += playerBalance;
        playerBalance = 0;
        updateBalances();
    });

    // Spin button event
    document.getElementById('spinButton').addEventListener('click', () => {
        const lines = parseInt(document.getElementById('linesSelect').value, 10);
        const betPerLine = parseInt(document.getElementById('betInput').value, 10);
        const totalBet = lines * betPerLine;

        if (playerBalance >= totalBet) {
            playerBalance -= totalBet;
            updateBalances();

            // AJAX request to the Flask server
            fetch('/spin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'lines': lines,
                    'bet': betPerLine
                })
            })
            .then(response => response.json())
            .then(data => {
                // Process the response here
                // For example, update the slot machine symbols and display winnings/losses
                console.log(data); // You should replace this with actual UI update code
                // Update player balance after spin
                playerBalance += data.winnings; // Assuming 'data.winnings' is part of the JSON response
                updateBalances();
            })
            .catch((error) => {
                console.error('Error:', error);
            });

        } else {
            alert('Insufficient funds for bet.');
        }
    });
});
