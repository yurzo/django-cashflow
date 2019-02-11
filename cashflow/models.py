from django.db import models


class Institution(models.Model):
    fid = models.CharField(max_length=200, primary_key=True)
    organization = models.CharField(max_length=200)

    def __str__(self):
        return self.organization


class Account(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    account_type = models.CharField(max_length=200)
    routing_number = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    type = models.IntegerField()
    branch_id = models.CharField(max_length=200)
    institution = models.ForeignKey("Institution", on_delete=models.CASCADE)
    # warnings
    # curdef
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        tokens = [self.institution.organization]
        if self.account_type:
            tokens.append(self.account_type.lower())
        tokens.append(self.number[-4:])
        return " - ".join(tokens)


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Statement(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    balance = models.DecimalField(max_digits=10, decimal_places=2)
    balance_date = models.DateField()

    currency = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.account}: {self.start_date} / {self.end_date}"


class Transaction(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    statement = models.ForeignKey("Statement", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payee = models.CharField(max_length=200)
    checknum = models.CharField(max_length=200)

    mcc = models.CharField(max_length=200)
    sic = models.CharField(max_length=200, null=True)

    memo = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    date = models.DateField()

    links = models.ManyToManyField("self", null=True)
