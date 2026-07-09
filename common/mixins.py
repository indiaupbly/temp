"""Reusable view/service mixins."""


class SerializerContextMixin:
    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
