def create_alarm(self, new_alarm: Alarm) -> Alarm:
    result_alarm: Alarm
    with Session(self.engine, future=True) as session:
        alarm_schema: AlarmSchema = alarm_to_schema(new_alarm)
        session.add(alarm_schema)
        session.flush()
        result_alarm = schema_to_alarm(alarm_schema)
        session.commit()
    return result_alarm


def get_alarm_by_id(self, alarm_id: int) -> Alarm:
    alarm_schema: AlarmSchema
    with Session(self.engine) as session:
        stmt = select(AlarmSchema).where(AlarmSchema.id == alarm_id)
        alarm_schema = session.execute(stmt).scalars().first()
    return schema_to_alarm(alarm_schema)


def get_all_alarms(self) -> list[Alarm]:
    alarms: list[Alarm]
    with Session(self.engine) as session:
        stmt = select(AlarmSchema)
        alarms = [schema_to_alarm(a) for a in session.execute(stmt).scalars().all()]
    return alarms


def update_alarm(self, updated_alarm: Alarm) -> Alarm:
    return self.update_alarm_by_id(updated_alarm.alarm_id, updated_alarm)


def update_alarm_by_id(self, alarm_id: int, alarm: Alarm) -> Alarm:
    result_alarm: Optional[Alarm]
    with Session(self.engine) as session:
        alarm_in_db: AlarmSchema = session.get(AlarmSchema, alarm_id)
        alarm_in_db = alarm_to_schema(alarm)
        session.flush()
        result_alarm = schema_to_alarm(alarm_in_db)
        session.commit()
    return result_alarm


def delete_alarm_by_id(self, alarm_id: int) -> None:
    with Session(self.engine) as session:
        alarm_in_db = session.get(AlarmSchema, alarm_id)
        session.delete(alarm_in_db)
        session.commit()
