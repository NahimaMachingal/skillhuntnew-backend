# job/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import JobSerializer, JobApplicationSerializer
from .models import Job, JobApplication
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from api.models import EmployerProfile
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmployee, IsJobseeker, IsEmployeeOrJobseeker

class PostJobView(APIView):
    permission_classes = [IsEmployee]

    def post(self, request):
        employer = EmployerProfile.objects.filter(user=request.user).first()
        if not employer:
            return Response({'error': 'Only employers can post jobs'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['employer'] = employer.user_id
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateJobView(APIView):
    permission_classes = [IsEmployee]

    def put(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, employer__user=request.user)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found or you do not have permission to update this job."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobSerializer(job, data=request.data, partial=True)  # `partial=True` allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, employer__user=request.user)
            job.is_active = False  # Set the job to inactive instead of deleting
            job.save()
            return Response({"message": "Job deleted successfully."}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found or you do not have permission to delete this job."},
                status=status.HTTP_404_NOT_FOUND
            )


class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsEmployeeOrJobseeker]

    def get_queryset(self):
        # Get the currently logged-in user
        user = self.request.user
        # Find the employer profile associated with the user
        employer = EmployerProfile.objects.filter(user=user).first()
        if employer:
            # Return jobs associated with the employer
            return Job.objects.filter(employer=employer)
        # If no employer profile is found, return an empty queryset
        return Job.objects.none()

# job/views.py
class PendingJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Return only jobs that are not approved
        return Job.objects.filter(is_approved=False)

# job/views.py
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Use 'id' field to look up the job


class ApproveJobView(APIView):
    permission_classes = [IsAdminUser]  # Ensure only admin users can access this

    def post(self, request, id):
        try:
            job = Job.objects.get(id=id)
            job.is_approved = True
            job.save()
            return Response({'message': 'Job approved successfully.'}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found.'}, status=status.HTTP_404_NOT_FOUND)

# job/views.py
class ApprovedJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsEmployeeOrJobseeker]

    def get_queryset(self):
        # Return only jobs that are approved
        return Job.objects.filter(is_approved=True)
        
# job/views.py
class JobSeekerJobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(is_approved=True, status='open')  # Only show approved and open jobs
    serializer_class = JobSerializer
    permission_classes = [IsEmployeeOrJobseeker]
    lookup_field = 'id'  # Use 'id' field to look up the job

class CheckJobApplicationView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request, job_id):
        user = request.user
        applied = JobApplication.objects.filter(job_id=job_id, applicant=user).exists()
        return Response({'is_applied': applied})

class JobApplicationCreateView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def post(self, request):
        # Automatically set the applicant from the authenticated user
        serializer = JobApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(applicant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminJobListView(generics.ListAPIView):
    """
    View to list all jobs in the system for the admin.
    """
    serializer_class = JobSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this view

    def get_queryset(self):
        # Return all jobs for the admin view
        return Job.objects.all()


class AppliedCandidatesView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsEmployeeOrJobseeker]

    def get_queryset(self):
        # Get the currently logged-in employer user
        employer = EmployerProfile.objects.filter(user=self.request.user).first()
        if employer:
            # Get all jobs posted by the employer
            jobs = Job.objects.filter(employer=employer)
            # Get all job applications for those jobs
            return JobApplication.objects.filter(job__in=jobs)
        return JobApplication.objects.none()


class UpdateApplicationStatusView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def patch(self, request, application_id):
        try:
            application = JobApplication.objects.get(id=application_id)
            # Check if the authenticated user is the employer for the related job
            if application.job.employer.user != request.user:
                return Response({'detail': 'Not authorized to update this application.'}, status=status.HTTP_403_FORBIDDEN)

            # Update the status
            new_status = request.data.get('status')
            if new_status in dict(JobApplication.STATUS_CHOICES).keys():
                application.status = new_status
                application.save()
                serializer = JobApplicationSerializer(application)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        except JobApplication.DoesNotExist:
            return Response({'detail': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)

# job/views.py
class UserAppliedJobsView(generics.ListAPIView):
    """
    View to list all job applications for the authenticated user.
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [IsEmployeeOrJobseeker]

    def get_queryset(self):
        # Filter job applications by the currently authenticated user
        return JobApplication.objects.filter(applicant=self.request.user)

class RejectedJobsView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request):
        rejected_jobs = JobApplication.objects.filter(applicant=request.user, status="Rejected")
        serializer = JobApplicationSerializer(rejected_jobs, many=True)
        return Response(serializer.data)
        

from rest_framework.permissions import IsAdminUser

class AdminJobApplicationsView(generics.ListAPIView):
    """
    View to list all job applications in the system for the admin.
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this view

    def get_queryset(self):
        # Return all job applications for the admin view
        return JobApplication.objects.all()

class ApplicantsForJobView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request, job_id):
        """
        Fetch all applicants for a specific job by job_id.
        """
        try:
            # Filter job applications for the given job_id
            applications = JobApplication.objects.filter(job__id=job_id)
            serializer = JobApplicationSerializer(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobApplication.DoesNotExist:
            return Response(
                {"error": "No applicants found for this job."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateReasonView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def patch(self, request, application_id):
        try:
            application = JobApplication.objects.get(id=application_id)
            # Check if the authenticated user is the employer for the related job
            if application.job.employer.user != request.user:
                return Response({'detail': 'Not authorized to update this application.'}, status=status.HTTP_403_FORBIDDEN)

            # Update the reason
            reason = request.data.get('reason', '').strip()
            if reason:
                application.reason = reason
                application.save()
                serializer = JobApplicationSerializer(application)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Reason is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except JobApplication.DoesNotExist:
            return Response({'detail': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)
