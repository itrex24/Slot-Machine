export let playerBalance = 0;
export let walletBalance = 1000;

export function updateBalances() {
    document.getElementById('playerBalance').textContent = playerBalance.toFixed(2);
    document.getElementById('walletBalance').textContent = walletBalance.toFixed(2);
}
