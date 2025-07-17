
const wdFundsButton = document.querySelector('.wdFunds');
    const overlay2 = document.getElementById('overlay-2');
    if (wdFundsButton && overlay2) {
        wdFundsButton.addEventListener('click', function() {
            overlay2.style.display = 'block';
        });

        overlay2.addEventListener('click', function(event) {
            if (event.target === overlay2) {
                overlay2.style.display = 'none';
            }
        });
    }