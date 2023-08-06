from django.shortcuts import redirect
from otree.views import Page


class ProlificRedirect(Page):
    """Redirect back to Prolific"""

    def get(self):
        if "prolific_completion_code" in self.participant.vars:
            code = self.participant.vars["prolific_completion_code"]
        elif "prolific_completion_code" in self.session.config:
            code = self.session.config["prolific_completion_code"]
        else:
            raise LookupError(
                "Could not find 'prolific_completion_code' in participant.vars or session.config"
            )
        return redirect(f"https://app.prolific.co/submissions/complete?cc={code}")
