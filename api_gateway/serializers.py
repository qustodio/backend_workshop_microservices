import datetime
from marshmallow import Schema, fields, ValidationError


class CustomDateField(fields.Date):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None or value == '':
            return None
        return datetime.date.fromisoformat(value).isoformat()

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return datetime.date.fromisoformat(value).isoformat()
        except ValueError as error:
            raise ValidationError(f"{attr} must be a valid date (format: YYYY-MM-DD)") from error


class AuthorSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    date_of_birth = CustomDateField(required=True, format='%Y-%m-%d')
    date_of_death = CustomDateField(format='%Y-%m-%d')