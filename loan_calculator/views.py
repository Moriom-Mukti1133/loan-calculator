from decimal import Decimal, InvalidOperation
from django.shortcuts import render, HttpResponse
from .models import Loan


def calculate_loan(amount, interest_rate, loan_term):
    monthly_interest_rate = (interest_rate/100) / 12
    num_payments = loan_term
    monthly_payment = (amount * monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / (
            (1 + monthly_interest_rate) ** num_payments - 1)
    total_repayment = monthly_payment * num_payments
    return monthly_payment, total_repayment,

def loan_calculator(request):
    result = None
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST['amount'])
            interest_rate = Decimal(request.POST['interest_rate'])
            loan_term = int(request.POST['loan_term'])

            monthly_payment, total_repayment = calculate_loan(amount, interest_rate, loan_term)

            # Calculate the loan details here (e.g., monthly payment, total repayment, etc.)

            loan = Loan(amount=amount, interest_rate=interest_rate, loan_term=loan_term)
            loan.save()
            result = {
                'monthly_payment': round(monthly_payment,2),
                'total_repayment': round(total_repayment,2),
            }
        # return result

        except InvalidOperation:
            return HttpResponse("Invalid input. Please enter valid decimal numbers.")

    return render(request, 'loan_calculator.html', {'result': result})
