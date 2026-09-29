"""Azure resource listing interface."""

from typing import Protocol

from tag_compliance.models import ResourceRecord


class ResourceProvider(Protocol):
    """Interface for listing Azure resources."""

    def list_resources(self, resource_group: str | None = None) -> list[ResourceRecord]:
        """Return Azure resources, optionally scoped to a resource group."""
        ...


class AzureResourceProvider:
    """Azure SDK implementation of ResourceProvider."""

    def __init__(self, subscription_id: str) -> None:
        """Create a provider for one subscription."""
        self.subscription_id = subscription_id

    def list_resources(self, resource_group: str | None = None) -> list[ResourceRecord]:
        """List Azure resources with their tags."""
        raise NotImplementedError("Challenge 4: implement Azure SDK resource listing")
