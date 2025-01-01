#api/serializers.py
from .models import User,JobseekerProfile, EmployerProfile
from rest_framework import serializers

# Serializer class for the User model, responsible for converting model instances
# to JSON format and vice versa, as well as handling validation and creation logic.
class UserSerializer(serializers.ModelSerializer):
    
    # Meta class defines metadata for the serializer, including the model and fields to be serialized.
    class Meta:
        model = User  # Specifies the model to be serialized
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'user_type','password', 'is_verified', 'is_subscribed')  # Serializes all fields of the User model
        extra_kwargs = {'password': {'write_only': True}}

    # Overriding the create method to handle custom creation logic, especially password hashing.
    def create(self, validated_data):
        # Extracts the password from the validated data, if present, and removes it from the data dictionary.
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        # Creates a new User instance with the remaining validated data (excluding password).
        instance = self.Meta.model(**validated_data)
        
        # If a password was provided, hash it before storing it.
        if password:
            instance.set_password(password)
        
        # Save the User instance to the database.
        instance.save()
        
        # Return the newly created User instance.
        return instance

    def validate_user_type(self, value):
        if value not in dict(User.USER_TYPE_CHOICES).keys():
            raise serializers.ValidationError("Invalid user type.")
        return value
        

# api/serializers.py
class JobseekerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = JobseekerProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop('user', None)

        # Update JobseekerProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested user data if provided
        if user_data:
            user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        return instance

# api/serializers.py
class EmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EmployerProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        # Extract nested user data
        user_data = validated_data.pop('user', None)

        # Update EmployerProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested user data if provided
        if user_data:
            user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        return instance