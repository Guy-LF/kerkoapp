# CF custom module.

from kerko.specs import FieldSpec


class LabeledFieldSpec(FieldSpec):
    """Extends fields to have a label."""

    def __init__(self, *, label, **kwargs):
        super().__init__(**kwargs)
        self.label = label
