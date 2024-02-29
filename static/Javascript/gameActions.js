import { playerBalance, walletBalance, updateBalances } from './balanceManager.js';
import { showAlert } from './uiUpdates.js';

export function setupEventListeners() {
    document.getElementById('addCash').addEventListener('click', addCash);
    document.getElementById('cashOut').addEventListener('click', cashOut);
    document.getElementById('spinButton').addEventListener('click', spin);
}

function addCash() {
    if (walletBalance >= 100) {
        walletBalance -= 100;
        playerBalance += 100;
        updateBalances();
    } else {
        showAlert('Insufficient funds in wallet.');
    }
}

function cashOut() {
    walletBalance += playerBalance;
    playerBalance = 0;
    updateBalances();
}

function spin() {
    // Include AJAX call and related logic here
}
