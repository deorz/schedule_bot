from pydantic import BaseModel, Field, validator


class Schedule(BaseModel):
    date: str
    kind_of_work: str = Field(alias='kindOfWork')
    lecturer: str
    begin_lesson: str = Field(alias='beginLesson')
    end_lesson: str = Field(alias='endLesson')
    day_of_week: str = Field(alias='dayOfWeekString')
    discipline: str
    stream: str

    @validator('stream', pre=True)
    def validate_stream(cls, value):
        if value is None:
            value = 'Это не потоковая лекция'
        return value
