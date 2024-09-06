from django.shortcuts import render, redirect
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
import logging


# @login_required
# def dashboard(request):
#     account = Account.objects.get(user=request.user)
#     recent_transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
#     notifications = ["Notification 1", "Notification 2"]  # Example notifications
#     return render(request, 'dashboard.html', {
#         'account_balance': account.balance,
#         'recent_transactions': recent_transactions,
#         'notifications': notifications
#     })


# Initialize logger
logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    try:
        # Fetch account details for the logged-in user
        account = Account.objects.get(user=request.user)
        
        # Log account details
        logger.info(f'Account found: {account.account_number}, balance: {account.balance}')
        
        # Fetch recent transactions and notifications
        recent_transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
        notifications = ["Notification 1", "Notification 2"]
        
        # Render dashboard.html with context
        return render(request, 'dashboard.html', {
            'account_balance': account.balance,
            'recent_transactions': recent_transactions,
            'notifications': notifications
        })
    except Account.DoesNotExist:
        # Log error if account does not exist for the user
        logger.error('Account does not exist for user.')
        return redirect('some_error_page')  # Replace 'some_error_page' with your actual error page name

@login_required
def transfer(request):
    if request.method == 'POST':
        recipient = request.POST['recipient']
        recipient_account_number = request.POST['recipient_account_number']
        amount = request.POST['amount']
        transfer_type = request.POST['transfer_type']
        description = request.POST['description']
        
        try:
            recipient_account = Account.objects.get(account_number=recipient_account_number)
            sender_account = Account.objects.get(user=request.user)
            
            if sender_account.balance >= float(amount):
                sender_account.balance -= float(amount)
                recipient_account.balance += float(amount)
                sender_account.save()
                recipient_account.save()
                
                Transaction.objects.create(
                    account=sender_account,
                    amount=amount,
                    transaction_type=transfer_type,
                    description=description,
                    recipient=recipient
                )
                
                Transaction.objects.create(
                    account=recipient_account,
                    amount=amount,
                    transaction_type=transfer_type,
                    description=description,
                    sender=request.user.username
                )
                
                return redirect('banking:dashboard.html')
            else:
                return render(request, 'transfer.html', {'error': 'Insufficient balance'})
        
        except Account.DoesNotExist:
            return render(request, 'transfer.html', {'error': 'Recipient account not found'})

    return render(request, 'transfer.html')

@login_required
def bill_payment(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        bill_type = request.POST['bill_type']
        account = Account.objects.get(user=request.user)
        if account.balance >= float(amount):
            account.balance -= float(amount)
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type=bill_type)
            return redirect('dashboard.html')
    return render(request, 'bill_payment.html')

@login_required
def account_management(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'account_management.html', {'account': account, 'transactions': transactions})

@login_required
def customer_support(request):
    return render(request, 'customer_support.html')
