document.addEventListener('DOMContentLoaded', function() {
    // Кнопка копирования реферального кода
    const refCodeBtn = document.querySelector('.ref-codeBTN');
    if (refCodeBtn) {
        refCodeBtn.addEventListener('click', function() {
            const button = this;
            const originalText = button.textContent;
            
            navigator.clipboard.writeText(originalText).then(() => {
                button.textContent = 'Copied';
                setTimeout(() => {
                    button.textContent = originalText;
                }, 1000);
            }).catch(err => {
                console.error('Ошибка при копировании текста: ', err);
            });
        });
    }

    // Окно пополнения
    const addFundsButton = document.querySelector('.addFunds');
    const overlay = document.getElementById('overlay-1');
    if (addFundsButton && overlay) {
        addFundsButton.addEventListener('click', function() {
            overlay.style.display = 'block';
        });

        overlay.addEventListener('click', function(event) {
            if (event.target === overlay) {
                overlay.style.display = 'none';
            }
        });
    }

    // Окно вывода
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

    

    // Выбор крипто-сети
    const form = document.querySelector('.choose-crypto');
    if (form) {
        const select = form.querySelector('select');
        const amountInput = form.querySelector('#amountInput');
        
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const selectedOption = select.value;
            const amount = amountInput.value;
            let url;

            switch(selectedOption) {
                case 'bep20':
                    url = '/bep20/pay/qN7679-3c7cef-47929b-5de3d5-711wet';
                    break;
                case 'erc20':
                    url = '/erc20/pay/zQ5678-3g4hij-9123kl-5mnop6-789rst';
                    break;
                case 'trc20':
                    url = '/trc20/pay/rT8901-3c9def-4567ab-8ijkl4-567nop';
                    break;
                case 'sol':
                    url = '/sol/pay/pQ9012-3r7stx-4568kl-9mnop5-123uvw';
                    break;
                case 'near':
                    url = '/near/pay/mN1234-3p5qrs-7890tu-4vwxyz-rut';
                    break;
                default:
                    console.log('We are faced with a problem');
                    return;
            }

            // Добавляем сумму в URL
            url += `?amount=${amount}`;

            window.location.href = url;
        });
    }


    // Таймер на странице оплаты
    const minutesDisplay = document.getElementById('minutes');
    const secondsDisplay = document.getElementById('seconds');
    if (minutesDisplay && secondsDisplay) {
        let minutes = 10;
        let seconds = 0;

        function updateTimer() {
            if (minutes === 0 && seconds === 0) {
                clearInterval(timerInterval);
                return;
            }

            if (seconds === 0) {
                minutes--;
                seconds = 59;
            } else {
                seconds--;
            }

            minutesDisplay.textContent = minutes.toString().padStart(2, '0');
            secondsDisplay.textContent = seconds.toString().padStart(2, '0');
        }

        const timerInterval = setInterval(updateTimer, 1000);
    }
    const minutesDisplay1 = document.getElementById('minutes-1');
    const secondsDisplay1 = document.getElementById('seconds-1');
    if (minutesDisplay1 && secondsDisplay1) {
        let minutes = 0;
        let seconds = 15;

        function updateTimer() {
            if (minutes === 0 && seconds === 0) {
                clearInterval(timerInterval);
                window.location.href = '/profile';
                return;
            }

            if (seconds === 0) {
                minutes--;
                seconds = 59;
            } else {
                seconds--;
            }

            minutesDisplay1.textContent = minutes.toString().padStart(2, '0');
            secondsDisplay1.textContent = seconds.toString().padStart(2, '0');
        }

        const timerInterval = setInterval(updateTimer, 1000);
    }



    // BEP20 оплата 
    const confirmButton = document.querySelector('.btn-red');
    if (confirmButton) {
        confirmButton.addEventListener('click', function() {
            window.location.href = '/bep20/processing/aB1cD2-3eF4gH-5iJ6kL-7mN8oP-9qR0sT';
        });
    }
    // ERC20 оплата 
    const confirmButton2 = document.querySelector('.btn-red-2');
    if (confirmButton2) {
        confirmButton2.addEventListener('click', function() {
            window.location.href = '/doneerc20/processing/pQ1rS2-3tU4vW-5xY6zA-7bC8dE-9fG0hI';
        });
    }
    // TRC20 оплата 
    const confirmButton3 = document.querySelector('.btn-red-3');
    if (confirmButton3) {
        confirmButton3.addEventListener('click', function() {
            window.location.href = '/donetrc20/processing/J1kL2-3mN4oP-5qR6sT-7uV8wX-9yZ0aB';
        });
    }
    // SOLANA оплата 
    const confirmButton4 = document.querySelector('.btn-red-4');
    if (confirmButton4) {
        confirmButton4.addEventListener('click', function() {
            window.location.href = '/donesol/processing/yZ6789-3t4uvw-1234xy-5zabc6-789def';
        });
    }
    // NEAR оплата 
    const confirmButton5 = document.querySelector('.btn-red-5');
    if (confirmButton5) {
        confirmButton5.addEventListener('click', function() {
            window.location.href = '/donenear/processing/tU9012-3l4opq-5678mn-9vwxyz-123rst';
        });
    }
    const confirmButton1 = document.querySelector('.btn-red-1');
    if (confirmButton1) {
        confirmButton1.addEventListener('click', function() {
            window.location.href = '/profile';
        });
    }

    
});


