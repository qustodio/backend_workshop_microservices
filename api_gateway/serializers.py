import datetime

from marshmallow import Schema, fields, ValidationError, validate, post_dump

isbn_regex_validator = r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$'


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


class BookSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    title = fields.Str(required=True)
    isbn = fields.Str(required=True, validate=validate.Regexp(isbn_regex_validator))
    summary = fields.Str(allow_none=True)
    author = fields.Int(required=True)
    language = fields.Int(required=True)
    genre = fields.List(fields.Int, required=True)
    image = fields.Str(allow_none=True)


class AuthorSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    date_of_birth = CustomDateField(required=True, format='%Y-%m-%d')
    date_of_death = CustomDateField(format='%Y-%m-%d')


class LoanSchema(Schema):
    id = fields.UUID(dump_only=True)
    book = fields.Int(required=True)
    imprint = fields.Str(required=True)
    borrower = fields.Int(allow_none=True)
    due_back = CustomDateField(allow_none=True, format="%Y-%m-%d")
    status = fields.Str(validate=validate.OneOf(["d", "o", "a", "r"]))

    @post_dump
    def convert_fields(self, data, **_):
        if 'borrower' in data and data['borrower'] == 0:
            data['borrower'] = None

        return data


class RenewLoanSchema(Schema):
    id = fields.UUID(dump_only=True)
    due_back = CustomDateField(required=True, format="%Y-%m-%d")
    book = fields.Int(dump_only=True)
    imprint = fields.Str(dump_only=True)
    borrower = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)


class RecommendationSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    isbn = fields.Str()
    summary = fields.Str()
    author = fields.Int()
    language = fields.Int()
    genre = fields.List(fields.Int)
    image = fields.Str()


class LanguageSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
