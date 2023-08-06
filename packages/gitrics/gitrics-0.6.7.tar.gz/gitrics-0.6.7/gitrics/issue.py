import networkx as nx

from glapi import configuration
from glapi.issue import GitlabIssue

class gitricsIssue(GitlabIssue):
    """
    gitricsIssue is a Gitlab Issue with opinionated enrichment for the gitrics ecosystem.
    """

    def __init__(self, id: str = None, iid: str = None, issue: dict = None, group_id: str = None, group_graph: nx.DiGraph = None, notes: list = None, ownership: list = None, token: str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            id (string): GitLab Issue id
            iid (string): GitLab Issue iid
            group_id (string): Gitlab Group id
            group_graph (DiGraph): networkx directional graph
            issue (dictionary): GitLab Issue
            notes (list): dictionaries of GitLab notes (comments)
            ownership (list): classes of GitlabUser
            token (string): GitLab personal access, ci, or deploy token
            version (string): GitLab API version as base url
        """
        self.gitlab_type = "issue"
        self.group_graph = group_graph
        self.ownership = ownership

        # initialize inheritance
        super(gitricsIssue, self).__init__(
            issue=issue,
            notes=notes,
            token=token,
            version=version
        )
