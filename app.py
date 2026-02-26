from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
accounts = {}

class Account:
    def __init__(self, accountNo, holderName, balance, isKYCVerified):
        self.accountNo = accountNo
        self.holderName = holderName
        self.balance = balance
        self.isKYCVerified = isKYCVerified

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', accounts=accounts.values())
@app.route('/remove_account/<accountNo>', methods=['POST'])
def remove_account(accountNo):
    if accountNo in accounts:
        del accounts[accountNo]
        flash('Account removed successfully!', 'success')
    else:
        flash('Account not found!', 'error')
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        accountNo = request.form['accountNo']
        holderName = request.form['holderName']
        balance = float(request.form['balance'])
        isKYCVerified = request.form.get('isKYCVerified') == 'on'
        if accountNo in accounts:
            flash('Account number already exists!', 'error')
        else:
            accounts[accountNo] = Account(accountNo, holderName, balance, isKYCVerified)
            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/transaction', methods=['GET'])
def transaction_screen():
    return render_template('transaction.html')

@app.route('/deposit', methods=['POST'])
def deposit():
    accountNo = request.form['accountNo']
    amount = float(request.form['amount'])
    account = accounts.get(accountNo)
    if account:
        account.balance += amount
        flash('Deposit successful!', 'success')
    else:
        flash('Account not found!', 'error')
    return redirect(url_for('index'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    accountNo = request.form['accountNo']
    amount = float(request.form['amount'])
    account = accounts.get(accountNo)
    if account:
        if account.balance >= amount:
            account.balance -= amount
            flash('Withdrawal successful!', 'success')
        else:
            flash('Insufficient balance!', 'error')
    else:
        flash('Account not found!', 'error')
    return redirect(url_for('index'))

@app.route('/transfer', methods=['POST'])
def transfer():
    sender = accounts.get(request.form['senderAccount'])
    receiver = accounts.get(request.form['receiverAccount'])
    amount = float(request.form['amount'])
    if not sender:
        flash('Sender account not found!', 'error')
    elif not receiver:
        flash('Receiver account not found!', 'error')
    elif not sender.isKYCVerified:
        flash('Sender must be KYC verified!', 'error')
    elif sender.balance < amount:
        flash('Sender has insufficient balance!', 'error')
    else:
        sender.balance -= amount
        receiver.balance += amount
        flash('Transfer successful!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
