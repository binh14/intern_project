from rest_framework import serializers
from leaveRequest.models import LeaveRequest
from datetime import datetime


class LeaveRequestSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = LeaveRequest
        fields = ('email', 'start_date', 'end_date', 'reason', 'status', 'rejected_reason', 'other_reason')

class CreateLeaveRequestSerializers(serializers.Serializer):
    reason_forms = [
        ('SICK', 'SICK'),
        ('FAMILY', 'FAMILY'),
        ('ACCIDENT', 'ACCIDENT'),
        ('APPOINTMENT', 'APPOINTMENT'),
        ('OTHER_REASON', 'OTHER_REASON'),
        # Add more choices as needed
    ]

    start_date = serializers.DateField(required=True, format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    end_date = serializers.DateField(required=True, format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    reason = serializers.ChoiceField(required=True, choices=reason_forms)
    other_reason = serializers.CharField(required=False, allow_blank=True)

    def validate_end_date(self, value): #value: end_date
        data = self.initial_data #initial_data lấy data gốc từ request body postman
        start_date_str = data['start_date']
        end_date_str = data['end_date']

        try:
            start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
            end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
        except ValueError:
            raise serializers.ValidationError("Invalid date format. Please use 'dd-mm-yyyy'.")

        if not (start_date <= end_date):
            raise serializers.ValidationError("Start date must be less than or equal to the End Date. Please check your input")
            # raise serializers.ValidationError(value)
        return value #return end_date
        
    
    def to_representation(self, instance):
        # Bỏ qua việc hiển thị other_reason nếu reason không phải là 'OTHER_REASON'
        if self.initial_data.get('reason') != 'OTHER_REASON': #nếu ko phải thì ẩn và ko hiện trong data trả về
            self.fields.pop('other_reason')
        return super().to_representation(instance)

    def validate_reason(self, value):
        valid_reasons = [reason[0] for reason in self.reason_forms] #duyệt tuple(0,1)
        if value not in valid_reasons:
            raise serializers.ValidationError("Invalid 'reason' value. Please choose a valid reason.")
        return value #reason

    def validate_other_reason(self, value):
        reason = self.initial_data.get('reason')  #initial_data  lấy data gốc từ request body postman
        if reason == 'OTHER_REASON':
            if not value:
                raise serializers.ValidationError("Can't be empty when 'Other Reason' is chosen.")
            elif len(value) < 5 or len(value) > 255:
                raise serializers.ValidationError("Please enter a valid 'other_reason' between 5 and 255 characters.")
        return value

    def create(self, validated_data):
        validated_data['start_date'] = validated_data['start_date'].strftime("%d-%m-%Y") #04-02-2024 -> (2024, 2, 4)
        validated_data['end_date'] = validated_data['end_date'].strftime("%d-%m-%Y")

        return LeaveRequest.objects.create(**validated_data)

    def save(self):
        validated_data = self.validated_data
        print("validated_data:")
        print(validated_data)
        user = self.context['request'].user
        print("user:")      
        print(user)
        leave_request = LeaveRequest(
            user=user,
            start_date=validated_data.get('start_date'),
            end_date=validated_data.get('end_date'),
            reason=validated_data.get('reason'),
            other_reason=validated_data.get('other_reason'),
        )
        leave_request.save()


class GetDetailLeaveRequestSerializer(serializers.Serializer):

    def to_representation(self, instance):
        print("email: ",instance.user.email)
        return {
            "id": instance.id,
            "start_date": instance.start_date,
            "end_date": instance.end_date,
            "email": instance.user.email
        }