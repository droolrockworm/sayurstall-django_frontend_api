from django import forms
# from locations.models import Location, HistoricalKWInfo, Client, UserProfile, Dealer, Device

class EmailForm(forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()
    email = forms.EmailField()
    econfirm = forms.EmailField()
    phone = forms.CharField(max_length=12)
    pconfirm = forms.CharField(max_length=12)

    # def clean_email(self):
    #     print()
    #     email = self.cleaned_data['email']
    #     if UserProfile.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email already exists")
    #     return email

    def clean(self):

        cleaned_data = super(EmailForm, self).clean()
        fname = cleaned_data.get("fname")
        lname = cleaned_data.get("lname")

        email = cleaned_data.get("email")
        econfirm = cleaned_data.get("econfirm")
        phone = cleaned_data.get("phone")
        pconfirm = cleaned_data.get("pconfirm")

        if email and econfirm:
            # Only do something if both fields are valid so far.
            # if UserProfile.objects.filter(email=email).exists():
            #     raise forms.ValidationError("Email already exists")
            if email != econfirm:
                raise forms.ValidationError("Emails must match")

        if phone and pconfirm:
            # Only do something if both fields are valid so far.
            # if UserProfile.objects.filter(phone=phone).exists():
            #     raise forms.ValidationError("Phone number already exists")
            if phone != pconfirm:
                raise forms.ValidationError("Phone numbers must match")
        # if email:

        # form_data = self.cleaned_data
        # print(form_data)
        # if form_data['confirm'] != None:
        #
        #     if form_data['email'] != form_data['confirm']:
        #         self._errors['confirm'] = ["Emails must match"] # Will raise a error message
        #         del form_data['password']
        return cleaned_data
