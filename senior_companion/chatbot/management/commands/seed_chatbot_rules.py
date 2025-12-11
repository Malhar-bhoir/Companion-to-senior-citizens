from django.core.management.base import BaseCommand
from chatbot.models import LogicRule

class Command(BaseCommand):
    help = 'Seeds the chatbot with initial logic rules for all site features.'

    def handle(self, *args, **kwargs):
        # Define the rules
        # Format: (pattern, match_type, response, suggested_link, priority)
        rules_data = [
            # --- ACCOUNT / AUTH ---
            (
                'register', 
                'contains', 
                'To create a new account, please click the "Register" link. You will need to provide your email and a password.', 
                '/accounts/register/', 
                10
            ),
            (
                'login', 
                'contains', 
                'You can log in to access your personalized dashboard.', 
                '/accounts/login/', 
                10
            ),
            (
                'profile', 
                'contains', 
                'You can update your personal details, hobbies, and home address in your profile.', 
                '/accounts/profile/', 
                8
            ),
            (
                'address', 
                'contains', 
                'Saving your home address in your profile allows us to find hospitals near you.', 
                '/accounts/profile/', 
                8
            ),

            # --- HOSPITALS & DOCTORS ---
            (
                'hospital', 
                'contains', 
                'You can search for hospitals, view details, and find emergency services near you.', 
                '/hospitals/', 
                9
            ),
            (
                'doctor', 
                'contains', 
                'Looking for a specialist? You can browse doctor profiles and see their visiting hours.', 
                '/hospitals/', 
                9
            ),
            (
                'emergency', 
                'contains', 
                'If this is a medical emergency, please call 100 immediately. You can find nearby emergency hospitals here:', 
                '/hospitals/?nearby_emergency=on', 
                20  # High priority!
            ),

            # --- INSURANCE ---
            (
                'insurance', 
                'contains', 
                'Visit the Insurance Hub to manage your policies or view recommendations.', 
                '/insurance/', 
                9
            ),
            (
                'policy', 
                'contains', 
                'You can add your own insurance policies to track their expiry dates.', 
                '/insurance/', 
                8
            ),
            (
                'suggestion', 
                'contains', 
                'Our AI can suggest the best insurance plan for you based on your profile.', 
                '/insurance/suggest/', 
                9
            ),
            (
                'recommend', 
                'contains', 
                'Get a personalized insurance recommendation here:', 
                '/insurance/suggest/', 
                9
            ),

            # --- LEARNING RESOURCES ---
            (
                'learn', 
                'contains', 
                'Explore our library of articles, videos, and guides on various topics.', 
                '/learning/', 
                9
            ),
            (
                'video', 
                'contains', 
                'We have many educational videos. You can filter by "Video" in the learning section.', 
                '/learning/?content_type=video', 
                8
            ),
            (
                'tutorial', 
                'contains', 
                'Check out our step-by-step tutorials.', 
                '/learning/?content_type=tutorial', 
                8
            ),

            # --- GAMES ---
            (
                'game', 
                'contains', 
                'Keep your mind active with our collection of games!', 
                '/games/', 
                9
            ),
            (
                'play', 
                'contains', 
                'Ready to play? Check out the Memory Match game.', 
                '/games/memory/', 
                8
            ),
            (
                'memory', 
                'contains', 
                'Test your memory with our card matching game.', 
                '/games/memory/', 
                9
            ),

            # --- COMPANIONS & CHAT ---
            (
                'companion', 
                'contains', 
                'Find other seniors to connect with in the Companions section.', 
                '/accounts/companions/', 
                9
            ),
            (
                'friend', 
                'contains', 
                'You can add friends and chat with them in the Companions area.', 
                '/accounts/companions/', 
                9
            ),
            (
                'chat', 
                'contains', 
                'To chat with someone, first add them as a companion, then click the "Chat" button next to their name.', 
                '/accounts/companions/', 
                9
            ),

            # --- REMINDERS ---
            (
                'reminder', 
                'contains', 
                'Never miss a dose! You can set medication reminders here.', 
                '/reminders/', 
                9
            ),
            (
                'medicine', 
                'contains', 
                'Add your medications and we will remind you when to take them.', 
                '/reminders/', 
                9
            ),
            (
                'pill', 
                'contains', 
                'Need to track your pills? Set up a schedule here.', 
                '/reminders/', 
                8
            ),
        ]

        # Loop and create
        count = 0
        for pattern, match_type, response, link, priority in rules_data:
            # Avoid duplicates (simple check)
            if not LogicRule.objects.filter(pattern=pattern).exists():
                LogicRule.objects.create(
                    pattern=pattern,
                    match_type=match_type,
                    response=response,
                    suggested_link=link,
                    priority=priority
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} new logic rules!'))