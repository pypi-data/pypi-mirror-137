class QualityReportError:
    def __init__(self) -> None:
        self.error_list = list()

    def add(self, parameter: str) -> None:
        self.error_list.append(parameter)

    def is_empty(self) -> bool:
        if len(self.error_list) == 0:
            return True
        return False

    def to_string(self) -> str:
        return "\n".join(self.error_list)
