from django import forms
from .models import Tenant, TaskAssignment, Room, Task

class TenantForm(forms.ModelForm):
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(tenant__isnull=True),  # only empty rooms
        required=False,
        help_text="Select a room* for this tenant"
    )

    class Meta:
        model = Tenant
        fields = ["name", "email", "room"]
    
    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        return name.title()  # capitalize first letter only


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "room"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Dynamically set help text for the room field
            if self.instance and self.instance.pk:
                current_room = self.instance.room
                if current_room:
                    self.fields["room"].help_text = f"Currently assigned to: {current_room.name}"
                else:
                    self.fields["room"].help_text = "No room currently assigned."
            else:
                self.fields["room"].help_text = "Select a room for this task."


class TaskReassignmentForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        fields = '__all__'

