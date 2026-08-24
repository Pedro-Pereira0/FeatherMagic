class meeting:
    title: str
    creator: str
    description: str
    date: str
    start_time: str
    end_time: str
    num_of_participants: int

    def __init__(self, title: str, creator: str, description: str, date: str, start_time: str, end_time: str, num_of_participants: int):
        self.title = title
        self.creator = creator
        self.description = description
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.num_of_participants = num_of_participants