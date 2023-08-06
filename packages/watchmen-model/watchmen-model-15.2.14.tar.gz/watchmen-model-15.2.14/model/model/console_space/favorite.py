from model.model.common.watchmen_model import WatchmenModel


class Favorite(WatchmenModel):
    connectedSpaceIds: list = []
    dashboardIds: list = []
    userId: str = None
    tenantId: str = None
