from mongoengine import (
    StringField, IntField, DateTimeField,
    BooleanField, DictField,  Document)
import datetime


class JsonForm(Document):
    user = StringField(required=True)
    institution = IntField(required=True)
    content = DictField()
    module = StringField(required=False)
    available = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def create(user, institution, content, module, available):
        json_form = JsonForm(
            user=user,
            institution=institution,
            content=content,
            module=module,
            available=available,
        )
        return json_form.save()

    def update(id, user, institution, content, module, available):
        json_form = JsonForm.objects(id__iexact=id).first()
        json_form.user = user
        json_form.institution = institution
        json_form.content = content
        json_form.module = module
        json_form.available = available
        return json_form.save()

    def to_json(self):
        return dict(
            id=str(self.id),
            user=self.user,
            institution=self.institution,
            content=self.content,
            module=self.module,
            available=self.available,
            created_at=self.created_at,
            updated_at=self.updated_at)

    def find_form(user, institution):
        return JsonForm.objects(
            user__iexact=user, institution__iexact=institution).first()
