from mux_demux_ws.secondary_base_consumer import SecondaryDefaultConsumer


class AlertConsumer(SecondaryDefaultConsumer):

    @property
    def default_group_name(self):
        return "alerts_{}".format(self.user.id)
