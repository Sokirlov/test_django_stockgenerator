from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class DateRangeFilter(SimpleListFilter):
    title = _('Date range')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return ()

    def queryset(self, request, queryset):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                return queryset.filter(
                    **{
                        f"{self.parameter_name}__gte": start_date,
                        f"{self.parameter_name}__lte": end_date,
                    }
                )
            except ValueError:
                pass
        return queryset

    def choices(self, changelist):
        return []
