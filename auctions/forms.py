from django import forms
from .models import Listing, Bidding, Comment, Category, Transactions, Address

CATEGORY = Category.objects.all().values_list('name', 'name')
CATEGORY1 = {
    ('', '')
}

categories = []

for item in CATEGORY:
    categories.append(item)
for item in CATEGORY1:
    categories.append(item)

class ListingForm(forms.ModelForm):
    class  Meta:
        model = Listing
        labels = {
            'productnames': 'Productname',
            'descriptions': 'Description',
            'startingbids': 'Starting Bids',
            'images': 'Image URL',
            'category': 'Category',
            'timer': "Bid Closing Time",
            'minimum_charge': "Minimum fee to register"
        }
        fields = [
            'productnames',
            'descriptions',
            'startingbids',
            'images',
            'category',
            'timer',
            'minimum_charge'
        ]
        widgets = {
            'category': forms.Select(choices=categories, attrs={'class': 'form-control'})
        }
    

class BiddingForm(forms.ModelForm):
    class  Meta:
        model = Bidding
        labels = {
            'bidprice' : ''
        }
        fields = [
            'bidprice'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {
            'comment' : ''
        }
        fields = [
            'comment'
        ]


class AddCoinForm(forms.ModelForm):
    class Meta:
        model = Transactions
        labels = {
            'coins': 'coins'
        }
        fields = [
            'coins'
        ]

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'first_name',
            'last_name',
            'street_address',
            'city',
            'state',
            'pin_code',
            'mobile_no',
            'alternate_no'
            # Add any other fields you want to include from Transactions
        ]
        labels = {
            'first_name': 'Billing First Name',
            'last_name': 'Billing Last Name',
            'street_address': 'Billing Street Address',
            'city': 'Billing City',
            'state': 'Billing State',
            'pin_code': 'Billing Pin Code',
            'mobile_no': "Mobile No",
            'alternate_no': "Alternate No"

        }

    def clean(self):
        cleaned_data = super().clean()

        # Check if shipping address is required based on a logic (e.g., checkbox)
        # ... Implement your validation logic here ...

        return cleaned_data

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'first_name',
            'last_name',
            'street_address',
            'city',
            'state',
            'pin_code',
            'mobile_no',
            'alternate_no'
            # Add any other fields you want to include from Transactions
        ]
        labels = {
            'first_name': 'Shipping First Name',
            'last_name': 'Shipping Last Name',
            'street_address': 'Shipping Street Address',
            'city': 'Shipping City',
            'state': 'Shipping State',
            'pin_code': 'Shipping Pin Code',
            'mobile_no': "Mobile No",
            'alternate_no': "Alternate No"

        }

    def clean(self):
        cleaned_data = super().clean()

        # Check if shipping address is required based on a logic (e.g., checkbox)
        # ... Implement your validation logic here ...

        return cleaned_data

# from django import forms
# from .models import Address  # Replace with your actual address model

class SelectAddressForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        label="Select Billing Address",
        empty_label="Choose..."
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('username', None)
        super(SelectAddressForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(username=user)