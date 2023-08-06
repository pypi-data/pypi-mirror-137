from marshmallow import (
    Schema,
    fields,
    validate,
)


class CompanyFilingOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    company_filing_id = fields.Integer(required=True)
    updated_at = fields.DateTime(dump_only=True)
