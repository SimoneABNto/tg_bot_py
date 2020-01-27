from core.db.submodule.action_counter_log import ActionCounterLog


class CommandsField(object):

    def extract_data(self, raw_data):

        try:
            for key in raw_data.keys():
                setattr(
                    self, key,
                    ActionCounterLog().extract_data(raw_data.get(key, ActionCounterLog().build_data()))
                )
        except Exception as exc:
            print('New User used Commands, db creation exception (accepted): ' + str(exc))
            pass

        return self

    def build_data(self):
        data_out = {}
        attrs = self.__dict__
        for key in attrs.keys():
            data_out[key] = attrs.get(key).build_data()

        return data_out

    def command(self, command_name):
        """
        Get the command object by his name

        :param command_name: the name of the command as in the command declaration file
        :return the command class
        """
        command_name = command_name.replace('.', '_')
        if command_name.replace('.', '_') in self.__dict__.keys():
            return getattr(self, command_name)

    def get_command_interactions(self, command_name):
        command_usage_log = self.command(command_name)
        if command_usage_log:
            return command_usage_log.total_count

    def increment_command_interactions(self, command_name: str, timestamp):
        command = self.command(command_name)
        if command:

            value = (timestamp, 1, 0)
            command.update_log_by_hour(value)
            command.update_log_by_day(value)
            command.update_log_by_month(value)
            command.total_count += 1

        else:
            setattr(
                self,
                command_name,
                ActionCounterLog()
            )