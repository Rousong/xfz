class FormMixin(object):
    def get_errors(self):
        return {key: [message['message']]
                for key, message_dicts in self.errors.get_json_data().items()
                for message in message_dicts}\
            if hasattr(self, 'errors') else dict()
