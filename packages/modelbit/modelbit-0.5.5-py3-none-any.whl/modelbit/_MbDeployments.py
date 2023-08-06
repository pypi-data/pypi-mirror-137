from . import _Utils

class _MbDeployments:
    mbMain = None
    _deployments = []

    def __init__(self, mbMain):
        self._mbMain = mbMain
        resp = self._mbMain._getJsonOrPrintError("jupyter/v1/deployments/list")
        if resp:
            self._deployments = resp["deployments"]

    def _repr_markdown_(self):
        return self._makeDeploymentsMkTable()

    def _makeDeploymentsMkTable(self):
        import timeago, datetime
        from collections import defaultdict

        if len(self._deployments) == 0:
            return ""
        deploymentsByName = defaultdict(lambda: [])
        for d in self._deployments:
            deploymentsByName[d["name"]].append(d)

        formatStr = (
            "| Name | Owner | Status | Versions | Deployed | \n" + "|:-|:-:|:-|-:|:-|\n"
        )
        for dList in deploymentsByName.values():
            latestDeployment = dList[0]
            versionCount = len(dList)
            connectedAgo = timeago.format(
                datetime.datetime.fromtimestamp(latestDeployment["createdAtMs"] / 1000),
                datetime.datetime.now(),
            )
            ownerInfo = latestDeployment["ownerInfo"]
            ownerImageTag = _Utils.formatImageTag(
                ownerInfo["imageUrl"], ownerInfo["name"]
            )
            formatStr += f'| { latestDeployment["name"] } | { ownerImageTag } | {latestDeployment["environmentStatus"]} | { versionCount } |  { connectedAgo } |\n'
        return formatStr
