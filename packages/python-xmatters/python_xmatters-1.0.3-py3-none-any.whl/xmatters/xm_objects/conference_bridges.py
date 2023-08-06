import xmatters.xm_objects.common
import xmatters.connection


class ConferenceBridge(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(ConferenceBridge, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.toll_number = data.get('tollNumber')
        self.toll_free_number = data.get('tollFreeNumber')
        self.preferred_connection_type = data.get('preferredConnectionType')
        self.pause_before_bridge_prompt = data.get('pauseBeforeBridgePrompt')
        self.static_bridge_number = data.get('staticBridgeNumber')
        self.bridge_number = data.get('bridgeNumber')
        self.dial_after_bridge = data.get('dialAfterBridge')
        links = data.get('links')
        self.links = xmatters.xm_objects.common.SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
