from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
import requests
from decouple import config
from .permissions import IsEmployee, IsJobseeker, IsEmployeeOrJobseeker

logger = logging.getLogger(__name__)

class ChatBotView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]  # Ensure the user is authenticated
    predefined_answers = {
        
        "where are you from": "I exist in the digital world, so I don't have a physical location.",
        "what is the weather today": "Sorry, I can't check the weather at the moment.",
        "help": "How can I assist you? Please tell me your question.",
        "what all the features this application have": "You can post jobs, apply for jobs, connect with employees and employers, build a resume, add a subscription, and more.",
        "features of this application": "You can post jobs, apply for jobs, connect with employees and employers, build a resume, add a subscription, and more.",
        "you can contact skillhunt admin at skillhuntadmin@gmail.com": "You can contact the Skillhunt admin at skillhuntadmin@gmail.com.",
        "tell something about this app": "This is a job portal website called Skillhunt. You can post jobs, apply for jobs, connect with employees and employers, build a resume, add a subscription, and more.",
        "give me an introduction of this application": "You can post a job, apply for a job, connect with employees and employers, build a resume, add a subscription, and more.",

        # FAQ for the job portal website
        "how do i post a job on this platform": "You can post a job by logging into your employer account and navigating to the 'Post a Job' section. Fill out the required details, such as job title, description, location, and qualifications, then submit the listing.",
        "how do i apply for a job": "To apply for a job, log in to your user account, browse available job listings, and click on the 'Apply Now' button. You may need to upload your resume and provide any additional details requested by the employer.",
        "what is the subscription for": "A subscription provides additional features such as priority job listings, advanced resume building tools, and enhanced visibility for both job seekers and employers.",
        "how do i create my resume": "You can create a resume by visiting the 'Resume Builder' section of your profile. Enter your details such as education, work experience, skills, and other relevant information, and then download your resume in your preferred format.",
        "can i edit my job application after submission": "Once your application is submitted, you cannot edit it. However, you can reach out to the employer directly if you need to make changes or add more information.",
        "how do i delete my account": "To delete your account, go to your account settings and select the 'Delete Account' option. Please note that once your account is deleted, all your data will be permanently removed.",
        "can i save job listings for later": "Yes, you can save job listings to your 'Saved Jobs' section, so you can come back to them later.",
        "how do i update my profile information": "You can update your profile information by going to your profile settings. You can edit your name, contact details, resume, and other relevant information.",
        "what types of jobs are listed on this platform": "Our platform features a wide range of jobs across various industries, including IT, healthcare, finance, marketing, engineering, and more.",
        "how do i contact customer support": "If you need assistance, you can contact customer support by emailing support@skillhunt.com or visiting the 'Contact Us' section on the website.",
        "can i apply for multiple jobs at the same time": "Yes, you can apply for as many jobs as you like. Each job application is handled separately by the employer.",
        "is my data secure on this platform": "Yes, we prioritize the security of your personal and professional information. Our platform uses industry-standard encryption methods to ensure that your data is protected.",
        "how do i get a job recommendation": "You will receive job recommendations based on your profile and preferences. You can also filter job listings by category, location, and other criteria.",
        "can i receive job alerts": "Yes, you can set up job alerts to receive notifications about new job postings that match your preferences.",
        "how do i know if my job application has been viewed": "You will receive a notification when your application has been viewed by the employer. You can also track the status of your application through your profile."
    }

    def post(self, request):
        user_input = request.data.get("message", "").lower()
        GEMINI_API_KEY = config("GEMINI_API_KEY")

        logger.info(f"User Input: {user_input}")

        # Check predefined answers
        reply = self.predefined_answers.get(user_input)
        if reply:
            logger.info(f"Predefined reply found: {reply}")
            return Response({"response": reply}, status=status.HTTP_200_OK)

        # Call external API if no predefined answer exists
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                json={
                    "contents": [{"parts": [{"text": user_input}]}]
                },
                headers={"Content-Type": "application/json"}
            )
            logger.info(f"API Response Status: {response.status_code}")
            logger.info(f"API Response Body: {response.text}")

            response.raise_for_status()
            response_data = response.json()

            # Extract reply
            reply = (
                response_data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "Sorry, I couldn't process your request.")
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"API connection error: {e}")
            reply = "Error connecting to the Gemini API."
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            reply = "An unexpected error occurred."

        return Response({"response": reply}, status=status.HTTP_200_OK)
