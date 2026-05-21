from rest_framework import serializers
from .models import Customer, Opportunity


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'company', 'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'country', 'postal_code',
            'company_name', 'status', 'notes', 'assigned_to',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OpportunitySerializer(serializers.ModelSerializer):
    weighted_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Opportunity
        fields = [
            'id', 'company', 'customer', 'title', 'description',
            'amount', 'probability', 'weighted_amount', 'status',
            'expected_close_date', 'assigned_to',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'weighted_amount']
