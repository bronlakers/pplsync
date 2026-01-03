from django.contrib import admin
from .models import Attachment, PettyCashFund, PettyCashVoucher, PettyCashBill, BillAllocation, PettyCashReconciliation

admin.site.register(Attachment)
admin.site.register(PettyCashFund)
admin.site.register(PettyCashVoucher)
admin.site.register(PettyCashBill)
admin.site.register(BillAllocation)
admin.site.register(PettyCashReconciliation)
