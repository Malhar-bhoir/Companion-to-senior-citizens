import re
from .models import LogicRule, UnansweredQuery

class ChatBotEngine:
    def process(self, user_input, user=None):
        """
        Takes raw user input, runs it through the logic rules,
        and returns the best response.
        """
        cleaned_input = user_input.lower().strip()
        
        # 1. Fetch all rules, sorted by priority (high first)
        rules = LogicRule.objects.all().order_by('-priority')
        
        # 2. Iterate through rules (First Order Logic simulation)
        for rule in rules:
            match_found = False
            pattern = rule.pattern.lower()
            
            if rule.match_type == 'exact':
                if cleaned_input == pattern:
                    match_found = True
            
            elif rule.match_type == 'contains':
                # Check if the keyword exists as a distinct word
                if f" {pattern} " in f" {cleaned_input} " or pattern in cleaned_input:
                    match_found = True
            
            elif rule.match_type == 'regex':
                if re.search(pattern, cleaned_input):
                    match_found = True
            
            # 3. If Logic Holds -> Return Result
            if match_found:
                return {
                    'response': rule.response,
                    'link': rule.suggested_link,
                    'found': True
                }
        
        # 4. No Match Found -> Escalate to Admin
        self._log_unanswered(user_input, user)
        
        return {
            'response': "I'm sorry, I don't understand that question yet. I have notified the support staff, and they will look into it.",
            'link': None,
            'found': False
        }

    def _log_unanswered(self, text, user):
        # Don't log tiny gibberish (optional filter)
        if len(text) > 2:
            UnansweredQuery.objects.create(
                user=user if user and user.is_authenticated else None,
                query_text=text
            )