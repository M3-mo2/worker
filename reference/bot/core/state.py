# bot_v2/bot/core/state.py
# Manages the conversation state for each user.
# Replaces the global `conversation_state` dictionary from the old project.

from typing import Dict, Any, Optional

class ConversationStateManager:
    """
    Manages the conversation state for each user.
    """
    def __init__(self):
        self._states: Dict[int, Dict[str, Any]] = {}

    def set_state(self, user_id: int, status: str, context: Optional[Dict[str, Any]] = None, message_id: Optional[int] = None):
        """
        Sets the conversation state for a given user.
        :param user_id: The ID of the user.
        :param status: The current status of the conversation (e.g., "awaiting_input").
        :param context: A dictionary to store additional context data for the conversation.
        :param message_id: The ID of the message to be edited later in the conversation.
        """
        self._states[user_id] = {'status': status}
        if context is not None:
            self._states[user_id]['context'] = context
        if message_id is not None:
            self._states[user_id]['message_id'] = message_id

    def get_state(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieves the entire conversation state dictionary for a user.
        Returns an empty dict if no state is found.
        """
        return self._states.get(user_id, {})

    def get_status(self, user_id: int) -> Optional[str]:
        """
        Retrieves only the status of the conversation for a user.
        Returns None if no state or status is found.
        """
        state = self._states.get(user_id)
        return state.get('status') if state else None

    def delete_state(self, user_id: int):
        """
        Deletes the conversation state for a given user.
        """
        if user_id in self._states:
            del self._states[user_id]

    def has_state(self, user_id: int) -> bool:
        """
        Checks if a user has any conversation state.
        """
        return user_id in self._states
    
    def get_value(self, user_id: int, key: str, default=None):
        """
        Gets a specific value from user's state.
        """
        state = self._states.get(user_id, {})
        return state.get(key, default)
    
    def set_value(self, user_id: int, key: str, value):
        """
        Sets a specific value in user's state.
        """
        if user_id not in self._states:
            self._states[user_id] = {}
        self._states[user_id][key] = value
    
    def clear_value(self, user_id: int, key: str):
        """
        Clears a specific value from user's state.
        """
        if user_id in self._states and key in self._states[user_id]:
            del self._states[user_id][key]
        """
        Checks if a user has an active conversation state.
        """
        return user_id in self._states

# Create a global instance of the ConversationStateManager to be imported throughout the app.
conversation_manager = ConversationStateManager()

print("✅ ConversationStateManager initialized.")
