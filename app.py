import json
import uuid  # импортируем отдельно
import sys
import requests
sys.stdout.reconfigure(encoding='utf-8')
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from datetime import datetime


app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'supersecretkey'


# ====================== Telegram BOT ======================
TELEGRAM_BOT_TOKEN = '7726856877:AAFIslzTXmB5FCw2zDHuPswiybUaCGxiNSw'
TELEGRAM_CHAT_ID = '2045150846'

def send_telegram_notification(username, message_type, amount=None, payment_method=None, order_data=None):
    messages = {
        'registration': f"🆕 Новый пользователь зарегистрирован!\nUsername: {username}",
        'payment': f"💳 Новое пополнение баланса!\n\n"
                  f"👤 Пользователь: {username}\n"
                  f"💰 Сумма: {amount} USD\n"
                  f"🔧 Метод: {payment_method}\n"
                  f"🕒 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        'new_order': f"🛒 Новый заказ!\n\n"
                    f"👤 Пользователь: {username}\n"
                    f"📦 Заказ: {order_data.get('product', 'N/A') if order_data else 'N/A'}\n"
                    f"🔢 Количество: {order_data.get('quantity', 1) if order_data else 1}\n"
                    f"💵 Сумма: {order_data.get('amount', 0) if order_data else 0} USD\n"
                    f"📅 Дата: {order_data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')) if order_data else datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🆔 ID заказа: {order_data.get('id', 'N/A') if order_data else 'N/A'}"
    }
    
    message = messages.get(message_type)
    if not message:
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        return None








# Пути к файлам для хранения данных
USERS_FILE = 'users.json'
REFERRALS_FILE = 'referrals.json'
PROMOCODES_FILE = 'promocodes.json'
REWARDS_FILE = 'rewards.json'
USER_REWARDS_FILE = 'user_rewards.json'  # Новый файл для хранения наград пользователей
AFFILIATES_FILE = 'affiliates.json'
PARTNERS_FILE = 'partners.json'
PAYMENTS_FILE = 'payments.json'
PRODUCTS_FILE = 'products.json'
CARDS_FILE = 'cards.json'
WHITELIST_FILE = 'whitelist_users.json'

# Загрузка данных из файлов
def load_data():
    global users, referrals, promocodes, rewards, user_rewards
    global affiliate_users, partners_data, affiliate_payments, products, cards, whitelist_users
    global active_bonuses

    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    try:
        with open(REFERRALS_FILE, 'r') as f:
            referrals = json.load(f)
    except FileNotFoundError:
        referrals = {}

    try:
        with open(PROMOCODES_FILE, 'r') as f:
            promocodes = json.load(f)
    except FileNotFoundError:
        promocodes = {}

    try:
        with open(REWARDS_FILE, 'r') as f:
            rewards = json.load(f)
    except FileNotFoundError:
        rewards = []  # Список доступных наград (названия)

    try:
        with open(USER_REWARDS_FILE, 'r') as f:
            user_rewards = json.load(f)
    except FileNotFoundError:
        user_rewards = {}  # Словарь с наградами пользователей
        
        # Инициализация user_rewards на основе существующих пользователей
        for username in users.keys():
            user_rewards[username] = {
                'purchases': users[username].get('orders', 0),
                'assigned_reward': None,
                'reward_status': None
            }

    try:
        with open(AFFILIATES_FILE, 'r') as f:
            affiliate_users = json.load(f)
    except FileNotFoundError:
        affiliate_users = []

    try:
        with open(PARTNERS_FILE, 'r') as f:
            partners_data = json.load(f)
    except FileNotFoundError:
        partners_data = []

    try:
        with open(PAYMENTS_FILE, 'r') as f:
            affiliate_payments = json.load(f)
    except FileNotFoundError:
        affiliate_payments = []

    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        products = {}

    try:
        with open(CARDS_FILE, 'r') as f:
            cards = json.load(f)
    except FileNotFoundError:
        cards = []

    try:
        with open(WHITELIST_FILE, 'r') as f:
            whitelist_users = json.load(f)
    except FileNotFoundError:
        whitelist_users = []

    active_bonuses = []  # Список активных бонусов

# Сохранение данных в файлы
def save_data():
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    with open(REFERRALS_FILE, 'w') as f:
        json.dump(referrals, f, indent=4)
    with open(PROMOCODES_FILE, 'w') as f:
        json.dump(promocodes, f, indent=4)
    with open(REWARDS_FILE, 'w') as f:
        json.dump(rewards, f, indent=4)
    with open(USER_REWARDS_FILE, 'w') as f:  # Сохраняем награды пользователей
        json.dump(user_rewards, f, indent=4)
    with open(AFFILIATES_FILE, 'w') as f:
        json.dump(affiliate_users, f, indent=4)
    with open(PARTNERS_FILE, 'w') as f:
        json.dump(partners_data, f, indent=4)
    with open(PAYMENTS_FILE, 'w') as f:
        json.dump(affiliate_payments, f, indent=4)
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products, f, indent=4)
    with open(CARDS_FILE, 'w') as f:
        json.dump(cards, f, indent=4)
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(whitelist_users, f, indent=4)


# Главная страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    load_data()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']
        password_confirm = request.form['password2']
        if password != password_confirm:
            flash('The passwords do not match', 'error')
            return render_template('register.html')
        if username in users:
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        users[username] = {'password': password,
                          'balance': {'trc20': 0, 'erc20': 0, 'bep20': 0, 'card': 0},
                          'orders': 0,
                          'expenses': 0,
                          'userorders': [],
                          'topups': []
                         }
        save_data()
        
        # Отправляем уведомление в Telegram
        send_telegram_notification(username, 'registration')
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/register/<ref_code>', methods=['GET', 'POST'])
def register_ref(ref_code):
    load_data()
    if ref_code not in referrals:
        return "Реферальная ссылка не найдена", 404

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password1']
        password_confirm = request.form['password2']

        if password != password_confirm:
            flash('The passwords do not match', 'error')
            return render_template('register.html')

        if username in users:
            flash('Username already exists', 'error')

        users[username] = {
            'password': password,
            'balance': {'trc20': 0, 'erc20': 0, 'bep20': 0, 'card': 0},
            'orders': 0,
            'expenses': 0,
            'userorders': [],
            'topups': []
        }

        if username and password:
            referrals[ref_code].append({
                'name': username,
                'deposit': 0,
                'status': 'pending',
                'payout': 0
            })

        save_data()  # Сохраняем данные в файл
        return redirect(url_for('login'))

    return render_template('register.html', ref_code=ref_code)

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    load_data()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash("Incorrect username or password!", 'error')  # Добавляем сообщение об ошибке
        return redirect(url_for('login'))  # Перенаправляем обратно на страницу входа
    return render_template('login.html')

# Загрузка данных при старте приложения
load_data()





# Страница Admin
@app.route('/admin/users', methods=['GET', 'POST'])
def admin():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    if request.method == 'POST':
        action = request.form.get('action')
        target_user = request.form.get('target_user')

        if target_user in users:
            if action == 'edit_balance':
                balance_type = request.form.get('balance_type')
                new_value = float(request.form.get('new_balance'))  # Баланс может быть с плавающей точкой
                if balance_type in users[target_user]['balance']:
                    users[target_user]['balance'][balance_type] = new_value
                elif balance_type in ['orders', 'expenses']:
                    users[target_user][balance_type] = new_value

            elif action == 'edit_topup':
                date = request.form.get('date')
                network = request.form.get('network')
                amount = float(request.form.get('amount'))
                status = request.form.get('status')

                # Преобразуем формат даты на сервере (если это нужно) и добавляем секунды
                try:
                    # Проверяем, есть ли секунды в строке даты. Если нет, добавляем ":00".
                    if len(date) == 16:  # формат вида "YYYY-MM-DD HH:MM"
                        date += ":00"  # Добавляем секунды
                    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    pass  # В случае ошибок форматирования

                if network == 'BEP20':
                    topup_found = False
                    for topup in users[target_user].get('topups', []):
                        if topup['date'] == date and topup['network'] == network:
                            topup['amount'] = amount
                            topup['status'] = status
                            topup_found = True
                            break

                    if not topup_found:
                        if 'topups' not in users[target_user]:
                            users[target_user]['topups'] = []
                        users[target_user]['topups'].append({
                            'date': date,
                            'network': network,
                            'amount': amount,
                            'status': status
                        })

                    # Обновляем баланс, если статус платежа Success
                    if status == 'Success':
                        users[target_user]['balance']['bep20'] = users[target_user]['balance'].get('bep20', 0) + amount

                # Обработка пополнения для карты (Card)
                elif network == 'Card':
                    topup_found = False
                    for topup in users[target_user].get('topups', []):
                        if topup['date'] == date and topup['network'] == network:
                            topup['amount'] = amount
                            topup['status'] = status
                            topup_found = True
                            break

                    if not topup_found:
                        if 'topups' not in users[target_user]:
                            users[target_user]['topups'] = []
                        users[target_user]['topups'].append({
                            'date': date,
                            'network': network,
                            'amount': amount,
                            'status': status
                        })

                    # Обновляем баланс карты, если статус платежа Success
                    if status == 'Success':
                        users[target_user]['balance']['card'] = users[target_user]['balance'].get('card', 0) + amount

            elif action == 'edit_topup_status':
                date = request.form.get('date')
                network = request.form.get('network')
                new_status = request.form.get('new_status')

                # Преобразуем формат даты на сервере (если это нужно) и добавляем секунды
                try:
                    # Проверяем, есть ли секунды в строке даты. Если нет, добавляем ":00".
                    if len(date) == 16:  # формат вида "YYYY-MM-DD HH:MM"
                        date += ":00"  # Добавляем секунды
                    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    pass  # В случае ошибок форматирования

                for topup in users[target_user].get('topups', []):
                    if topup['date'] == date and topup['network'] == network:
                        topup['status'] = new_status

                        # Если статус изменился на Success, зачисляем баланс
                        if new_status == 'Success':
                            if network == 'BEP20':
                                users[target_user]['balance']['bep20'] = users[target_user]['balance'].get('bep20', 0) + topup['amount']
                            elif network == 'Card':
                                users[target_user]['balance']['card'] = users[target_user]['balance'].get('card', 0) + topup['amount']
                        break

            elif action == 'delete_user':
                del users[target_user]

            elif action == 'delete_topup':
                date = request.form.get('date')
                network = request.form.get('network')
                users[target_user]['topups'] = [
                    topup for topup in users[target_user].get('topups', [])
                    if not (topup['date'] == date and topup['network'] == network)
                ]

            save_data()

    # Сортировка пополнений по дате, от новой к старой
    for user, info in users.items():
        if 'topups' in info:
            info['topups'] = sorted(
                info['topups'], 
                key=lambda x: x['date'] if x['date'] else "",  # Используем пустую строку для None
                reverse=True
            )

    return render_template('admin_users.html', users=users)






@app.route('/admin/create_code', methods=['POST'])
def create_code():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    # Получаем данные из формы
    product_id = request.form.get('product_id')
    new_code = request.form.get('new_code')
    
    # Находим категорию по product_id
    category = None
    for key in products:
        if product_id in products[key]:
            category = key
            break

    if category:
        # Добавляем новый код в список "codes"
        if isinstance(products[category][product_id], dict):
            products[category][product_id]["codes"].append(new_code)
        else:
            # Если структура данных отличается, можно создать список
            products[category][product_id] = {
                "description": products[category][product_id],
                "codes": [new_code]
            }

        # Сохраняем изменения в файле products.json
        save_data()

    return redirect(url_for('adminlots'))

@app.route('/admin/delete_code', methods=['POST'])
def delete_code():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    # Получаем данные из формы
    product_id = request.form.get('product_id')
    code_to_delete = request.form.get('code')
    
    # Находим категорию по product_id
    category = None
    for key in products:
        if product_id in products[key]:
            category = key
            break

    if category and code_to_delete in products[category][product_id]["codes"]:
        # Удаляем код из списка
        products[category][product_id]["codes"].remove(code_to_delete)
        
        # Сохраняем изменения в файл products.json
        save_data()

    return redirect(url_for('adminlots'))



@app.route('/admin/orders', methods=['GET', 'POST'])
def admin2():
    load_data()
    if 'username' not in session or session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён", 403

    if request.method == 'POST':
        target_user = request.form.get('target_user')
        category = request.form.get('category')
        product = request.form.get('product')
        price = request.form.get('price')
        amount = request.form.get('amount')
        date = request.form.get('date')

        if date:
            try:
                try:
                    date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M')
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if target_user in users:
            new_order = {
                'id': str(uuid.uuid4()),
                'category': category,
                'product': product,
                'price': price,
                'amount': amount,
                'date': formatted_date,
                'timestamp': datetime.now().timestamp(),
                'status': 'pending'  # Новые заказы получают статус pending по умолчанию
            }
            if 'userorders' not in users[target_user]:
                users[target_user]['userorders'] = []
            users[target_user]['userorders'].append(new_order)
            save_data()

    # Для существующих заказов устанавливаем статус 'pending', если он не задан
    for user, info in users.items():
        if 'userorders' in info:
            for order in info['userorders']:
                if 'status' not in order:
                    order['status'] = 'pending'
            # Сортировка заказов
            info['userorders'].sort(
                key=lambda x: (
                    datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S').timestamp(),
                    x['timestamp']
                ),
                reverse=True
            )
    
    save_data()  # Сохраняем изменения статусов
    return render_template('admin_orders.html', users=users)

@app.route('/admin/update_order_status/<user>/<order_id>', methods=['POST'])
def update_order_status(user, order_id):
    load_data()
    if 'username' not in session or session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён", 403

    new_status = request.form.get('status')
    if user in users and 'userorders' in users[user]:
        for order in users[user]['userorders']:
            if order['id'] == order_id:
                old_status = order.get('status', 'pending')
                order['status'] = new_status
                
                # Возвращаем средства при отмене заказа
                if new_status == 'canceled' and old_status != 'canceled':
                    try:
                        price = float(order['price'])
                        amount = int(order['amount'])
                        total_refund = price * amount
                        
                        if 'balance' not in users[user]:
                            users[user]['balance'] = {}
                        
                        # Предполагаем, что баланс в USD
                        if 'USD' not in users[user]['balance']:
                            users[user]['balance']['USD'] = 0.0
                        
                        users[user]['balance']['USD'] += total_refund
                    except (ValueError, KeyError) as e:
                        print(f"Ошибка при возврате средств: {e}")
                
                save_data()
                break
    
    return redirect(url_for('admin2'))

@app.route('/admin/delete_order/<user>/<order_id>', methods=['POST'])
def delete_order(user, order_id):
    load_data()
    if 'username' not in session or session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён", 403

    if user in users and 'userorders' in users[user]:
        users[user]['userorders'] = [o for o in users[user]['userorders'] if o['id'] != order_id]
        save_data()
    
    return redirect(url_for('admin2'))

@app.route('/admin/save_key/<user>/<order_id>', methods=['POST'])
def save_key(user, order_id):
    load_data()
    if 'username' not in session or session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён", 403

    key = request.form.get('key')
    if user in users and 'userorders' in users[user]:
        for order in users[user]['userorders']:
            if order['id'] == order_id:
                order['key'] = key
                break
        save_data()
    
    return redirect(url_for('admin2'))

@app.route('/admin/update_order_date/<user>/<order_id>', methods=['POST'])
def update_order_date(user, order_id):
    load_data()
    if 'username' not in session or session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён", 403

    new_date = request.form.get('new_date')
    if user in users and 'userorders' in users[user]:
        for order in users[user]['userorders']:
            if order['id'] == order_id:
                try:
                    formats = [
                        '%Y-%m-%dT%H:%M:%S',
                        '%Y-%m-%dT%H:%M',
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%d %H:%M'
                    ]
                    
                    parsed_date = None
                    for fmt in formats:
                        try:
                            parsed_date = datetime.strptime(new_date, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if parsed_date:
                        order['date'] = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                        order['timestamp'] = datetime.now().timestamp()
                        save_data()
                except Exception as e:
                    print(f"Ошибка: {e}")
                break
    
    return redirect(url_for('admin2'))

@app.route('/orders')
def orders():
    load_data()
    if 'username' not in session:
        flash('Please login to access the dashboard', 'error')
        return redirect(url_for('login'))

    username = session['username']
    if username not in users:
        flash('User not found', 'error')
        return redirect(url_for('login'))

    balances = users[username].get('balance', {})
    userorders = users[username].get('userorders', [])

    # Сортируем заказы
    userorders.sort(
        key=lambda x: (
            datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S').timestamp(),
            x['timestamp']
        ),
        reverse=True
    )

    # Проверяем наличие новых заказов (последний в списке - самый новый)
    if userorders:
        last_order = userorders[0]
        # Проверяем, не отправляли ли уже уведомление об этом заказе
        if not last_order.get('notification_sent'):
            # Отправляем уведомление
            send_telegram_notification(
                username=username,
                message_type='new_order',
                order_data=last_order
            )
            # Помечаем заказ как обработанный
            last_order['notification_sent'] = True
            save_data()

    return render_template('orders.html',
                         username=username,
                         balances=balances,
                         userorders=userorders)







@app.route('/admin/payments', methods=['GET', 'POST'])
def admin3():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    # Загрузка платежных карт и адресов
    if 'payments' not in users:
        users['payments'] = {"bep20": "", "erc20": "", "trc20": "", "sol": "", "near": ""}

    # Обработка POST-запросов
    if request.method == 'POST':
        if 'delete_card' in request.form:
            # Удаление карты по ID
            card_id = request.form['delete_card']
            global cards
            cards = [card for card in cards if card['id'] != card_id]
            save_data()  # Сохраняем данные после удаления карты

        elif 'delete' in request.form:
            # Удаление адреса
            currency = request.form['delete']
            users['payments'][currency] = ""
            save_data()  # Сохраняем данные после изменения адреса

        else:
            # Сохранение введенных адресов
            for currency in users['payments'].keys():
                users['payments'][currency] = request.form.get(currency, "")
            save_data()  # Сохраняем данные после изменения адресов

    # Отображаем список карт и адресов
    return render_template('admin_payments.html', 
                           users=users, 
                           payments=users['payments'], 
                           cards=cards)  # Передаем и карты, и адреса для отображения









# Переход на страницу входа партнера
@app.route('/aff_login', methods=['GET', 'POST'])
def aff_login():
    load_data()
    if request.method == 'POST':
        partner_id = request.form.get('partner_id')

        # Проверяем, существует ли ID в списке партнеров
        user = next((user for user in affiliate_users if user['id'] == partner_id), None)

        if user:
            session['partner_id'] = partner_id  # Сохраняем ID в сессии
            return redirect(url_for('aff_home'))
        else:
            return render_template('aff_login.html', error="Incorrect ID. Please try again.")

    return render_template('aff_login.html')

@app.route('/aff_logout')
def aff_logout():
    load_data()
    session.pop('partner_id', None)  # Удаляем ID из сессии
    return redirect(url_for('aff_login'))

@app.route('/aff_home')
def aff_home():
    load_data()
    if 'partner_id' not in session:  # Проверяем, вошел ли пользователь
        return redirect(url_for('aff_login'))  # Если нет — отправляем на страницу входа
    
    partner_id = session['partner_id']  

    # Ищем соответствующий реферальный код
    ref_code = None
    for user in affiliate_users:
        if user['id'] == partner_id:
            ref_code = user.get('link', '').split('/')[-1]  # Достаем код из ссылки
            break

    if not ref_code:
        return redirect(url_for('aff_login')), 404

    # Получаем статистику для реферального кода
    users = referrals.get(ref_code, [])

    return render_template('aff_home.html', partner_id=partner_id, users=users)

@app.route('/aff_profile')
def aff_profile():
    load_data()
    if 'partner_id' not in session:
        return redirect(url_for('aff_login'))

    user = next((user for user in affiliate_users if user['id'] == session['partner_id']), None)
    if not user:
        return redirect(url_for('aff_login'))

    # Сортируем платежи по дате, чтобы новые добавлялись в начало
    from datetime import datetime
    user_payments = sorted(
        [p for p in affiliate_payments if p['user_id'] == user['id']],
        key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
        reverse=True  # Новые платежи будут первыми
    )

    return render_template('aff_profile.html', user=user, payments=user_payments)


@app.route('/aff/users', methods=['GET', 'POST'])
def aff_users():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    if request.method == 'POST':
        action = request.form.get('action')

        # Добавление пользователя
        if action == 'add':
            new_user = {
                'id': request.form.get('customID'),
                'telegram': request.form.get('telegram'),
                'link': request.form.get('link'),
                'balance': request.form.get('balance'),
                'hold': request.form.get('hold'),
                'revenue': request.form.get('revenue'),
                'total_deposits': request.form.get('total_deposits')  # Новый параметр
            }
            affiliate_users.append(new_user)

        # Редактирование пользователя
        elif action == 'edit':
            custom_id = request.form.get('customID')
            for user in affiliate_users:
                if user['id'] == custom_id:
                    user['telegram'] = request.form.get('telegram')
                    user['link'] = request.form.get('link')
                    user['balance'] = request.form.get('balance')
                    user['hold'] = request.form.get('hold')
                    user['revenue'] = request.form.get('revenue')
                    user['total_deposits'] = request.form.get('total_deposits')  # Новый параметр
                    break

        # Удаление пользователя
        elif action == 'delete':
            custom_id = request.form.get('customID')
            affiliate_users[:] = [user for user in affiliate_users if user['id'] != custom_id]

        save_data()  # Сохраняем данные после изменений

    return render_template('aff_users.html', users=affiliate_users, referrals=referrals)

@app.route('/aff/newpartners', methods=['GET', 'POST'])
def aff_partners():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    # Загружаем актуальные данные перед рендерингом страницы
    try:
        with open(PARTNERS_FILE, 'r') as f:
            partners_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        partners_data = []

    return render_template('aff_partners.html', partners=partners_data)


@app.route('/aff/delete_partner/<email>', methods=['POST'])
def delete_partner(email):
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    # Удаляем партнера по email
    global partners_data
    partners_data = [partner for partner in partners_data if partner['email'] != email]

    save_data()  # Сохраняем изменения

    return redirect(url_for('aff_partners'))

@app.route('/aff/finance', methods=['GET', 'POST'])
def aff_finance():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    if request.method == 'POST':
        user_id = request.form.get('aff_usersID')
        date = request.form.get('date')
        amount = request.form.get('amount')
        method = request.form.get('method')
        status = request.form.get('status')

        if user_id and date and amount and method and status:
            # Добавляем новый платеж в начало списка
            affiliate_payments.insert(0, {
                'id': len(affiliate_payments) + 1,  # Генерируем ID платежа
                'user_id': user_id,
                'date': date,
                'amount': amount,
                'method': method,
                'status': status
            })
            save_data()  # Сохраняем изменения

    return render_template('aff_finance.html', users=affiliate_users, payments=affiliate_payments)


@app.route('/aff/finance/delete_payments_without_id', methods=['POST'])
def delete_payments_without_id():
    load_data()
    global affiliate_payments

    # Фильтруем платежи, у которых нет ID
    affiliate_payments = [payment for payment in affiliate_payments if 'id' in payment]

    save_data()  # Сохраняем изменения

    return redirect(url_for('aff_finance'))




@app.route('/update_payment_status', methods=['POST'])
def update_payment_status():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён!", 403

    print(request.form)  # Проверяем, какие данные приходят в запросе

    payment_id = request.form.get('payment_id')
    
    if not payment_id:  # Проверяем, не пустое ли значение
        return "Ошибка: не указан ID платежа!", 400

    try:
        payment_id = int(payment_id)
    except ValueError:
        return "Ошибка: некорректный ID платежа!", 400

    new_status = request.form.get('new_status')

    for payment in affiliate_payments:
        if payment['id'] == payment_id:
            payment['status'] = new_status
            break

    save_data()  # Сохраняем изменения
    return redirect(url_for('aff_finance'))  # Обновляем страницу

@app.route('/delete_payment', methods=['POST'])
def delete_payment():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён!", 403

    payment_id = request.form.get('payment_id')

    if not payment_id:
        # Если ID не указан, проверяем, что платеж действительно без ID
        payment = request.form.to_dict()
        if 'id' not in payment:  # Если у формы нет ID
            return "Ошибка: не указан ID платежа!", 400

    try:
        payment_id = int(payment_id)
    except ValueError:
        return "Ошибка: некорректный ID платежа!", 400

    global affiliate_payments  

    # Проверяем, есть ли платеж с таким ID
    if not any(payment.get('id') == payment_id for payment in affiliate_payments):
        return f"Ошибка: платеж с ID {payment_id} не найден!", 404

    # Удаляем нужный платеж
    affiliate_payments = [payment for payment in affiliate_payments if payment.get('id') != payment_id]

    save_data()  
    return redirect(url_for('aff_finance'))










@app.route('/aff/ref', methods=['GET', 'POST'])
def aff_ref():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403
    if request.method == "POST":
        if "delete_ref" in request.form:
            ref_code = request.form["delete_ref"]
            referrals.pop(ref_code, None)
        else:
            ref_code = "ref" + str(uuid.uuid4())[:8]
            referrals[ref_code] = []

        save_data()  # Сохраняем данные после изменений

    return render_template('aff_ref.html', referrals=referrals)

@app.route("/aff/stats/<ref_code>", methods=["GET", "POST"])
def stats(ref_code):
    load_data()
    if ref_code not in referrals:
        return "Реферальная ссылка не найдена", 404

    users = referrals[ref_code]

    if request.method == "POST":
        for user in users:
            username = user["name"]  # Используем имя как ключ

            deposit_key = f"deposit_{username}"
            status_key = f"status_{username}"
            payout_key = f"payout_{username}"

            if deposit_key in request.form:
                user["deposit"] = float(request.form[deposit_key])

            if status_key in request.form:
                user["status"] = request.form[status_key]

            if payout_key in request.form:
                user["payout"] = float(request.form[payout_key])

        save_data()  # Сохраняем изменения
        return redirect(url_for("stats", ref_code=ref_code))

    return render_template("aff_stats.html", ref_code=ref_code, users=users)








# Страница главная
@app.route('/dashboard')
def dashboard():
    load_data()
    if 'username' not in session:
        flash('Please login to access the dashboard', 'error')
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('dashboard.html', username=username, balances=balances)



# Обработчик для страницы join_us
@app.route('/join_us', methods=['GET', 'POST'])
def join_us():
    load_data()
    if request.method == 'POST':
        email = request.form.get('email')
        traffic_source = request.form.get('traffic-source')
        geo = request.form.get('geo')

        if email and traffic_source and geo:
            # Загружаем актуальные данные перед изменением
            try:
                with open(PARTNERS_FILE, 'r') as f:
                    partners_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                partners_data = []

            # Добавляем нового партнера
            new_partner = {
                'email': email,
                'traffic_source': traffic_source,
                'geo': geo
            }
            partners_data.append(new_partner)

            # Сохраняем изменения
            try:
                with open(PARTNERS_FILE, 'w') as f:
                    json.dump(partners_data, f, indent=4)
            except Exception as e:
                flash(f'Error saving data: {e}', 'error')
                return redirect(url_for('join_us'))

            flash('Form successfully submitted!', 'success')

            # Обновляем переменную partners_data
            load_data()  # Подгружаем актуальные данные в глобальную переменную

    return render_template('join_us.html')





@app.route('/profile')
def profile():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_info = users.get(username, {})

    # Получаем балансы пользователя, включая баланс карты
    balances = user_info.get('balance', {})
    card_balance = balances.get('card', 0)

    # Получаем заказы пользователя
    userorders = user_info.get('userorders', [])
    orders_count = len(userorders)
    orders_admin = user_info.get('orders', 0)
    total_orders = orders_count + orders_admin

    expenses = user_info.get('expenses', 0)
    topups = user_info.get('topups', [])

    # Сортируем пополнения по дате, от новой к старой
    topups_sorted = sorted(
        topups, 
        key=lambda x: x['date'] if x['date'] else "",  
        reverse=True
    )

    return render_template('profile.html', 
                        username=username, 
                        balances=balances, 
                        card_balance=card_balance,  
                        orders=total_orders,  
                        expenses=expenses, 
                        topups=topups_sorted)  # Передаем отсортированные пополнения






@app.route('/admin/whitelist', methods=['GET', 'POST'])
def whitelist():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))

    if session['username'] != 'Dim4ikgoo$e101$':
        return "Доступ запрещён: только для администратора!", 403

    if request.method == 'POST':
        action = request.form.get('action')
        user_to_manage = request.form.get('target_user')

        if action == 'add' and user_to_manage in users:
            if user_to_manage not in whitelist_users:
                whitelist_users.append(user_to_manage)

        elif action == 'delete':
            username = request.form.get('username')
            if username in whitelist_users:
                whitelist_users.remove(username)

        save_data()  # Сохранение изменений

    return render_template('admin_whitelist.html', users=users, whitelist_users=whitelist_users)

def get_real_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]  # Берем первый IP из списка
    return request.remote_addr  # Если заголовка нет, берем стандартный IP
@app.route('/checkout/payment', methods=['GET', 'POST'])
def checkout_payment():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    balances = users[username]['balance']
    orders = users[username]['orders']
    expenses = users[username]['expenses']
    topups = users[username]['topups']

    # Получаем параметры amount и id из URL
    amount = request.args.get('amount')
    unique_id = request.args.get('id')

    if request.method == 'POST':
        # Получаем данные с формы
        card_number = request.form['card_number']
        expiry_date = request.form['expiry_date']
        cvv = request.form['cvv']
        card_name = request.form['card_name']
        country = request.form['country']  # Получаем страну
        ip_address = get_real_ip()  # Получаем реальный IP

        # Создаем новый объект карты с добавлением страны
        card = {
            "id": str(len(cards) + 1),
            "number": card_number,
            "date": expiry_date,
            "cvv": cvv,
            "name": card_name,
            "country": country,  # Добавляем страну
            "ip_address": ip_address
        }

        # Добавляем карту в список
        cards.append(card)

        # Сохраняем данные в файл
        save_data()

        # Редирект на страницу /payment/processing с передачей amount
        return redirect(url_for('payment_processing', amount=amount, unique_id=unique_id))

    return render_template('checkout_payment.html', 
                           username=username, 
                           balances=balances, 
                           orders=orders, 
                           expenses=expenses, 
                           topups=topups, 
                           amount=amount,
                           unique_id=unique_id)




@app.route('/payment/processing')
def payment_processing():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Получаем сумму из URL
    amount = request.args.get('amount')
    unique_id = request.args.get('unique_id')

    # Проверяем, есть ли пользователь в whitelist
    success = username in whitelist_users

    return render_template('payment_processing.html', success=success, amount=amount, unique_id=unique_id)




@app.route('/payment/success', methods=['GET', 'POST'])
def payment_success():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_info = users.get(username, {})
    balances = user_info.get('balance', {})
    card_balance = balances.get('card', 0)

    # Получаем сумму из URL
    amount = request.args.get('amount')

    if amount is None:
        return "Ошибка: сумма платежа не передана!", 400

    try:
        amount = float(amount)
    except ValueError:
        return "Ошибка: некорректный формат суммы!", 400

    network = 'Card'
    status = 'Success'

    # Добавляем платеж в историю пополнений пользователя
    topup = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'network': network,
        'amount': amount,
        'status': status
    }

    if 'topups' not in user_info:
        user_info['topups'] = []

    user_info['topups'].append(topup)

    # Обновляем баланс пользователя
    user_info['balance']['card'] = user_info['balance'].get('card', 0) + amount

    # Сохраняем данные
    save_data()

    return render_template('payment_success.html')


@app.route('/payment/failed')
def payment_failed():
    load_data()
    return render_template('payment_failed.html')



@app.route('/bep20/pay/qN7679-3c7cef-47929b-5de3d5-711wet', methods=['GET', 'POST'])
def bep20_payment():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    balances = users[username]['balance']
    orders = users[username]['orders']
    expenses = users[username]['expenses']
    topups = users[username]['topups']

    # Получаем BEP20-адрес из базы
    bep20_address = users.get('payments', {}).get('bep20', 'Not Set')

    amount = None  # По умолчанию, если запрос GET

    if request.method == 'POST':
        amount = request.form.get('amount')  # Получаем сумму из формы
        if not amount:
            return "Ошибка: сумма не указана!", 400

        try:
            amount = float(amount)
        except ValueError:
            return "Ошибка: некорректный формат суммы!", 400

        # Редирект на обработку платежа с передачей суммы
        return redirect(url_for('bep20_success', amount=amount))

    return render_template('bep20.html', 
                           username=username, 
                           balances=balances, 
                           orders=orders, 
                           expenses=expenses, 
                           topups=topups, 
                           bep20_address=bep20_address)



@app.route('/bep20/processing/aB1cD2-3eF4gH-5iJ6kL-7mN8oP-9qR0sT', methods=['GET'])
def bep20_success():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_info = users.get(username, {})
    balances = user_info.get('balance', {})

    amount = request.args.get('amount')
    if amount is None:
        print("Ошибка: сумма платежа не передана!")
        return render_template('donebep20.html', username=username, balances=balances)

    try:
        amount = float(amount)
    except ValueError:
        print("Ошибка: некорректный формат суммы!")
        return render_template('donebep20.html', username=username, balances=balances)

    network = 'BEP20'
    status = 'Pending'

    topups = user_info.get('topups', [])
    duplicate_found = any(
        topup['amount'] == amount and 
        topup['network'] == network and 
        topup['status'] == status
        for topup in topups
    )

    if not duplicate_found:
        topup = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'network': network,
            'amount': amount,
            'status': status
        }
        topups.append(topup)
        user_info['topups'] = topups
        save_data()

        # Отправка уведомления в Telegram
        send_telegram_notification(
            username=username,
            message_type='payment',
            amount=amount,
            payment_method='BEP20'
        )

    return render_template('donebep20.html', username=username, balances=balances)





@app.route('/erc20/pay/zQ5678-3g4hij-9123kl-5mnop6-789rst')
def erc20():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    orders = users[username]['orders']
    expenses = users[username]['expenses']
    topups = users[username]['topups']
    # Получаем ERC20 адрес из базы (предполагаем, что он хранится в users['payments'])
    erc20_address = users.get('payments', {}).get('erc20', 'Not Set') #Not Set - дефолтный адрес который можно установить
    return render_template('erc20.html', username=username, balances=balances, orders=orders, expenses=expenses, topups=topups, erc20_address=erc20_address)

@app.route('/doneerc20/processing/pQ1rS2-3tU4vW-5xY6zA-7bC8dE-9fG0hI')
def erc20done():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    orders = users[username]['orders']
    expenses = users[username]['expenses']
    topups = users[username]['topups']
    return render_template('doneerc20.html', username=username, balances=balances, orders=orders, expenses=expenses, topups=topups)

@app.route('/trc20/pay/rT8901-3c9def-4567ab-8ijkl4-567nop')
def trc20():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    orders = users[username]['orders']
    expenses = users[username]['expenses']
    topups = users[username]['topups']
    # Получаем ERC20 адрес из базы (предполагаем, что он хранится в users['payments'])
    trc20_address = users.get('payments', {}).get('trc20', 'Not Set') #Not Set - дефолтный адрес который можно установить
    return render_template('trc20.html', username=username, balances=balances, orders=orders, expenses=expenses, topups=topups, trc20_address=trc20_address)

@app.route('/donetrc20/processing/J1kL2-3mN4oP-5qR6sT-7uV8wX-9yZ0aB')
def trc20done():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    orders = users[username]['orders']
    expenses = users[username]['expenses']
    topups = users[username]['topups']
    return render_template('donetrc20.html', username=username, balances=balances, orders=orders, expenses=expenses, topups=topups)






@app.route('/product/31', methods=['GET', 'POST'])
def product31():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_info = users.get(username, {})
    balances = user_info.get('balance', {})
    expenses = user_info.get('expenses', 0)
    total_balance = balances.get('card', 0) + balances.get('bep20', 0)
    error = None

    # Уровни скидок: (expenses, balance, discount)
    discount_levels = [
        (0, 0, 0),         # 0% - базовый уровень
        (1000, 50, 2),        # 2% - 50 на балансе (новый уровень)
        (10000, 500, 20),  # 20% - либо 10k расходов, либо 500 на балансе
        (15000, 1000, 25), # 25% - либо 15k расходов, либо 1k на балансе
        (25000, 2000, 30), # 30% - либо 25k расходов, либо 2k на балансе
        (30000, 4000, 35)  # 35% - либо 30k расходов, либо 4k на балансе
    ]
    
    # Определение текущей скидки и следующего уровня
    current_discount = 0
    next_level = None
    
    for i, (exp_threshold, bal_threshold, discount) in enumerate(sorted(discount_levels, reverse=True)):
        if expenses >= exp_threshold or total_balance >= bal_threshold:
            current_discount = discount
            if i > 0:
                next_level = discount_levels[i-1]
            break
    else:
        next_level = discount_levels[1] if len(discount_levels) > 1 else None

    if request.method == 'POST':
        steam_login = request.form.get('steamLogin')
        requested_amount = float(request.form.get('amount', 0))
        amount_to_pay = requested_amount * (1 - current_discount / 100)

        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.now().timestamp()

        if amount_to_pay <= 0:
            error = "Invalid amount."
        elif balances.get('card', 0) >= amount_to_pay:
            users[username]['balance']['card'] -= amount_to_pay
            users[username]['expenses'] += amount_to_pay
        elif (balances.get('card', 0) + balances.get('bep20', 0)) >= amount_to_pay:
            remaining = amount_to_pay - balances['card']
            users[username]['balance']['card'] = 0
            users[username]['balance']['bep20'] -= remaining
            users[username]['expenses'] += amount_to_pay
        else:
            error = "Insufficient funds."

        if not error:
            new_order = {
                'id': str(uuid.uuid4()),
                'category': 'Steam',
                'product': 'Steam TopUp',
                'price': amount_to_pay,
                'amount': requested_amount,
                'requested_amount': requested_amount,
                'paid_amount': amount_to_pay,
                'discount': current_discount,
                'date': formatted_date,
                'timestamp': timestamp,
                'steamLogin': steam_login
            }
            users[username].setdefault('userorders', []).append(new_order)
            save_data()
            return redirect(url_for('product31'))

    return render_template('product_31.html',
                         username=username,
                         balances=balances,
                         expenses=expenses,
                         total_balance=total_balance,
                         error=error,
                         current_discount=current_discount,
                         next_level=next_level,
                         discount_levels=discount_levels)


@app.route('/product/33', methods=['GET', 'POST'])
def product33():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    balances = users[username]['balance']
    error = None
    
    products = {
        "366": "Steam Wallet Code | US | 5 USD",
        "367": "Steam Wallet Code | US | 10 USD",
        "368": "Steam Wallet Code | US | 20 USD",
        "369": "Steam Wallet Code | US | 25 USD",
        "370": "Steam Wallet Code | US | 50 USD",
        "371": "Steam Wallet Code | US | 75 USD",
        "372": "Steam Wallet Code | US | 100 USD",
    }
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        amount = int(request.form.get('amount', 0))
        price = float(request.form.get('price', 0))
        total_price = amount * price

        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if amount <= 0:
            error = "Invalid amount."
        elif balances['bep20'] >= total_price:
            users[username]['balance']['bep20'] -= total_price
            users[username]['expenses'] += total_price
        elif (balances['bep20'] + balances['card']) >= total_price:
            remaining = total_price - balances['bep20']
            users[username]['balance']['bep20'] = 0
            users[username]['balance']['card'] -= remaining
            users[username]['expenses'] += total_price
        else:
            error = "Insufficient funds."

        if not error:
            new_order = {
                'id': str(uuid.uuid4()),
                'category': 'Steam Wallet Code | USA',
                'product': products.get(product_id, f'Unknown Product {product_id}'),
                'price': total_price,
                'amount': amount,
                'date': formatted_date,
                'timestamp': datetime.now().timestamp()
            }
            users[username].setdefault('userorders', []).append(new_order)
            save_data()
            return redirect(url_for('product33'))

    return render_template('product_33.html',
                         username=username,
                         balances=balances,
                         error=error)
@app.route('/product/34')
def product34():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_34.html', username=username, balances=balances)
@app.route('/product/35')
def product35():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_35.html', username=username, balances=balances)
@app.route('/product/36')
def product36():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_36.html', username=username, balances=balances)

@app.route('/menu/13')
def menu13():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('menu_13.html', username=username, balances=balances)
@app.route('/product/37')
def product37():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_37.html', username=username, balances=balances)
@app.route('/product/38')
def product38():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_38.html', username=username, balances=balances)

@app.route('/menu/14')
def menu14():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('menu_14.html', username=username, balances=balances)
@app.route('/product/39')
def product39():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_39.html', username=username, balances=balances)
@app.route('/product/40')
def product40():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_40.html', username=username, balances=balances)

@app.route('/menu/15')
def menu15():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('menu_15.html', username=username, balances=balances)
@app.route('/product/41')
def product41():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_41.html', username=username, balances=balances)
@app.route('/product/42')
def product42():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_42.html', username=username, balances=balances)
@app.route('/product/43')
def product43():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_43.html', username=username, balances=balances)
@app.route('/product/44')
def product44():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_44.html', username=username, balances=balances)
@app.route('/product/45')
def product45():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_45.html', username=username, balances=balances)
@app.route('/product/46')
def product46():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_46.html', username=username, balances=balances)

@app.route('/menu/16')
def menu16():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('menu_16.html', username=username, balances=balances)
@app.route('/product/47')
def product47():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_47.html', username=username, balances=balances)

@app.route('/menu/17')
def menu17():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('menu_17.html', username=username, balances=balances)
@app.route('/product/48')
def product48():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('product_48.html', username=username, balances=balances)

@app.route('/menu/18')
def menu18():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balances = users[username]['balance']
    return render_template('menu_18.html', username=username, balances=balances)

@app.route('/product/49', methods=['GET', 'POST'])
def product49():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    balances = users[username]['balance']
    error = None
    
    products = {
        "1001": "Assassin´s Creed Odyssey XBOX ONE/SERIES X|S",
        "1002": "Assassin´s Creed Odyssey Gold XBOX ONE/SERIES X|S",
        "1003": "Assassin´s Creed Odyssey Ultimate XBOX ONE/SERIES X|S",
        "1004": "Assassins Creed Origins XBOX ONE/SERIES X|S",
        "1005": "Assassins Creed Origins Gold XBOX ONE/SERIES X|S",
        "1006": "Assassins Creed Valhalla XBOX ONE/SERIES X|S",
        "1007": "Assassins Creed Valhalla Ragnarok XBOX ONE/SERIES X|S",
        "1008": "Assassins Creed Valhalla Ultimate XBOX ONE/SERIES X|S",
        "1009": "Assassins Creed Mirage XBOX ONE/SERIES X|S",
        "1010": "Assassins Creed Mirage Deluxe XBOX ONE/SERIES X|S",
        "1011": "Assassins Creed Miarge Master XBOX ONE/SERIES X|S",
        "1012": "Baldur's Gate 3 XBOX SERIES X|S",
        "1013": "Baldur's Gate 3 Deluxe XBOX SERIES X|S",
        "1014": "Dead by Daylight XBOX ONE/SERIES X|S",
        "1015": "Dead by Daylight Gold XBOX ONE/SERIES X|S",
        "1016": "Dead by Daylight Ultimate XBOX ONE/SERIES X|S",
        "1017": "Destiny 2 The Final Shape XBOX ONE/SERIES X|S",
        "1018": "Destiny 2 Lightfall XBOX ONE/SERIES X|S",
        "1019": "Destiny 2 The Witch Queen XBOX ONE/SERIES X|S",
        "1020": "Destiny 2 Beyond XBOX ONE/SERIES X|S",
        "1021": "Diablo 4 XBOX ONE/SERIES X|S",
        "1022": "Diablo 4 Deluxe XBOX ONE/SERIES X|S",
        "1023": "Diablo 4 Ultimate XBOX ONE/SERIES X|S",
        "1024": "Diablo 4 Expansion Bundle XBOX ONE/SERIES X|S",
        "1025": "Diablo 4 Vessel of Hatred XBOX ONE/SERIES X|S",
        "1026": "Diablo 4 Vessel of Hatred Deluxe XBOX ONE/SERIES X|S",
        "1027": "Diablo 4 Vessel of Hatred Ultimate XBOX ONE/SERIES X|S",
        "1028": "Forza Horizon 5 XBOX ONE/SERIES X|S",
        "1029": "Forza Horizon 5 Deluxe XBOX ONE/SERIES X|S",
        "1030": "Forza Horizon 5 Ultimate XBOX ONE/SERIES X|S",
        "1031": "Kingdom Come: Deliverance II XBOX SERIES X|S",
        "1032": "Kingdom Come: Deliverance II Gold XBOX SERIES X|S",
        "1033": "Minecraft PC",
        "1034": "Minecraft XBOX ONE/SERIES X|S",
        "1035": "Mortal Kombat 11 XBOX ONE/SERIES X|S",
        "1036": "Mortal Kombat 11 Ultimate XBOX ONE/SERIES X|S",
        "1037": "Mortal Kombat 1 XBOX SERIES X|S",
        "1038": "Mortal Kombat 1 Premium XBOX SERIES X|S",
    }
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        amount = int(request.form.get('amount', 0))
        price = float(request.form.get('price', 0))
        total_price = amount * price

        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if amount <= 0:
            error = "Invalid amount."
        elif balances['bep20'] >= total_price:
            users[username]['balance']['bep20'] -= total_price
            users[username]['expenses'] += total_price
        elif (balances['bep20'] + balances['card']) >= total_price:
            remaining = total_price - balances['bep20']
            users[username]['balance']['bep20'] = 0
            users[username]['balance']['card'] -= remaining
            users[username]['expenses'] += total_price
        else:
            error = "Insufficient funds."

        if not error:
            new_order = {
                'id': str(uuid.uuid4()),
                'category': 'Xbox CD-Keys | US',
                'product': products.get(product_id, f'Unknown Product {product_id}'),
                'price': total_price,
                'amount': amount,
                'date': formatted_date,
                'timestamp': datetime.now().timestamp()
            }
            users[username].setdefault('userorders', []).append(new_order)
            save_data()
            return redirect(url_for('product49'))

    return render_template('product_49.html',
                         username=username,
                         balances=balances,
                         error=error)

@app.route('/product/50', methods=['GET', 'POST'])
def product50():
    load_data()
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    balances = users[username]['balance']
    error = None

    game_prices = {
        "Battlefield 2042": 28.0,
        "Battlefield V": 26.44,
        "Black Myth: Wukong": 34.21,
        "Call of Duty Modern Warfare (2022)": 53.11,
        "Cyberpunk 2077": 22.47,
        "DayZ": 26.13,
        "Dead by Daylight": 9.27,
        "Diablo 4 Expansion Bundle": 50.0,
        "Dragon's Dogma 2": 45.34,
        "Dying Light 2": 18.28,
        "EA SPORTS FC 24": 37.10,
        "EA SPORTS FC 25": 34.26,
        "Elden Ring": 32.37,
        "Elden Ring Nightreign": 24.16,
        "Far Cry 5": 25.0,
        "Far Cry 6": 25.0,
        "Forza Horizon 5": 27.36,
        "Garry’s Mod": 3.00,
        "GTA V": 14.78,
        "Helldivers 2": 27.44,
        "Hunt: Showdown 1896": 11.41,
        "It Takes Two": 22.86,
        "Kingdom Come: Deliverance": 17.19,
        "Kingdom Come: Deliverance 2": 34.72,
        "Last Epoch": 14.49,
        "Mortal Kombat 1": 27.00,
        "Mortal Kombat 11": 6.81,
        "Need for Speed Unbound": 38.29,
        "New World Aetrum": 53.31,
        "Red Dead Redemption 2": 16.55,
        "Remnant 2": 28.04,
        "Resident Evil 4": 22.65,
        "Resident Evil Village": 19.19,
        "Sea of Thieves": 25.51,
        "Sons of the Forest": 10.33,
        "Squad": 17.26
    }

    if request.method == 'POST':
        game = request.form.get('game')
        steam_link = request.form.get('steamLink')

        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.now().timestamp()

        if game not in game_prices:
            error = "Invalid game selection."
        else:
            amount = game_prices[game]
            total_price = amount  # Для совместимости с другими обработчиками

            if balances['bep20'] >= amount:
                users[username]['balance']['bep20'] -= amount
            elif balances['bep20'] + balances['card'] >= amount:
                remaining = amount - balances['bep20']
                users[username]['balance']['bep20'] = 0
                users[username]['balance']['card'] -= remaining
            else:
                error = "Insufficient funds."

            if not error:
                users[username]['expenses'] += amount
                new_order = {
                    'id': str(uuid.uuid4()),
                    'category': 'Steam Gifts',
                    'product': game,
                    'price': amount,
                    'amount': 1,
                    'date': formatted_date,
                    'timestamp': timestamp,
                    'steamLink': steam_link
                }
                users[username].setdefault('userorders', []).append(new_order)
                save_data()
                return redirect(url_for('product50'))

    return render_template('product_50.html', 
                         username=username, 
                         balances=balances, 
                         error=error)



@app.route('/user_agreement')
def terms_use():
    load_data()
    return render_template('user_agreement.html')

@app.route('/terms_of_use')
def user_agreement():
    load_data()
    return render_template('terms_use.html')

@app.route('/')
def main():
    load_data()
    return render_template('index.html')


# БЛОКИРОВЩИК ЗАПРОСОВ
@app.route('/wp-admin/setup-config.php')
def block_wp_scan():
    abort(404)  # Возвращаем ошибку 404 для этого пути

@app.route('/wordpress/wp-admin/setup-config.php')
def block_wp_scan2():
    abort(404)  # Возвращаем ошибку 404 для этого пути


# Выход из профиля
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

