import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from .models import Account, Category, Institution, Statement, Transaction
from .forms import UploadFileForm
from django.urls import reverse

from ofxparse import OfxParser
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    model = Transaction
    template_name = "cashflow/index.html"
    context_object_name = "transactions"

    def get_queryset(self):
        """ """
        return Transaction.objects.all()


class CategoriesView(generic.ListView):
    model = Category
    context_object_name = "categories"

    def get_queryset(self):
        """ """
        return Category.objects.all()


def handle_uploaded_file(file_handle):
    ofx = OfxParser.parse(file_handle)

    institutions_created = []
    accounts_created = []
    statements_created = []
    transactions_created = []

    for _account in ofx.accounts:

        _institution = _account.institution

        institution, created = Institution.objects.get_or_create(
            fid=_institution.fid, organization=_institution.organization
        )
        if created:
            institutions_created.append(institution)

        account, created = Account.objects.get_or_create(
            id=_account.account_id,
            account_type=_account.account_type,
            routing_number=_account.routing_number,
            number=_account.number,
            type=_account.type,
            branch_id=_account.branch_id,
            institution=institution,
        )

        if created:
            accounts_created.append(account)

        _statement = _account.statement

        statement, created = Statement.objects.get_or_create(
            account=account,
            start_date=_statement.start_date,
            end_date=_statement.end_date,
            balance=_statement.balance,
            balance_date=_statement.balance_date,
            currency=_statement.currency,
        )

        if created:
            statements_created.append(statement)

        for _transaction in _statement.transactions:
            transaction, created = Transaction.objects.get_or_create(
                id=_transaction.id,
                statement=statement,
                amount=_transaction.amount,
                payee=_transaction.payee,
                checknum=_transaction.checknum,
                mcc=_transaction.mcc,
                sic=_transaction.sic,
                memo=_transaction.memo,
                type=_transaction.type,
                date=_transaction.date,
            )


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            # return HttpResponseRedirect("/success/url/")
            return HttpResponseRedirect(reverse("cashflow:index"))
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


def simple_upload(request):
    if request.method == "POST" and request.FILES["file"]:

        # myfile = request.FILES["myfile"]
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)

        handle_uploaded_file(request.FILES["file"])

        uploaded_file_url = "Carlos"

        return render(
            request, "cashflow/simple_upload.html", {"uploaded_file_url": uploaded_file_url}
        )
    return render(request, "cashflow/simple_upload.html")


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "polls/detail.html"
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "polls/results.html"
