from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted


def clean_name(name):
    return "".join([c for c in name if c.isalpha()])

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"first_name": None}
        return {"first_name": name}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"last_name": None}
        
        first_name = tracker.get_slot("first_name")
        if len(first_name) + len(name) < 3:
            dispatcher.utter_message(text="That's a very short name. We fear a typo. Restarting!")
            return {"first_name": None, "last_name": None}
        return {"last_name": name}
    
class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_project_estimation_form"

    def validate_projectname(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `projectname` value."""

        # If the project name is not in the list, ask the user to provide correct project name.
        projectname = tracker.get_slot("projectname")

        # Load project names from the file
        with open("project_name.txt", "r") as file:
            valid_project_names = [line.strip() for line in file]

        if projectname not in valid_project_names:
            dispatcher.utter_message(text=f"Sorry, '{projectname}' is not a valid project name.")
            return {"projectname": None}
        return {"projectname": projectname}
    
class CustomRestartAction(Action):
    def name(self) -> Text:
        return "action_custom_restart"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Perform any custom actions you want here before restarting the conversation

        # Trigger the conversation reset using action_restart
        return [Restarted()]