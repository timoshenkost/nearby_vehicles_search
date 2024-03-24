from django_filters import rest_framework as filters


from .models import Cargo


class CargoFilter(filters.FilterSet):
    miles = filters.NumberFilter(method='nearby_vehicles_filter', label='Miles to vehicle')

    class Meta:
        model = Cargo
        fields = {
            'weight': ['gte', 'lte'],
        }

    def nearby_vehicles_filter(self, queryset, name, value):
        filtered_queryset = Cargo.objects.none()
        for cargo in queryset:
            vehicles = cargo.get_vehicles(value)
            if vehicles:
                filtered_queryset = filtered_queryset.union(Cargo.objects.filter(pk=cargo.pk))
        return filtered_queryset

