
class DoorError(Exception):
    def __init__(
        self,
        door_type="unset",
        door_state="unset",
        door_pos="unset",
        door_hinge_pos="unset",
    ):
        self.message = f"""\n
        Door TYPE is set to: {door_type}
        Door STATE is set to: {door_state}
        Door POS is set to: {door_pos}
        Door HINGE_POS is et to: {door_hinge_pos}"""
        super().__init__(self.message)